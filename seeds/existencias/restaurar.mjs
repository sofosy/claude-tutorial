// node seeds/existencias/restaurar.mjs [estado] [--volcar]
// Devuelve la base al canon de la serie Existencias (Repuestos Germiva) y aplica el ESTADO del video.
// Cada estado deja además en seeds/existencias/archivos/ el Excel que el video sube, generado de la
// plantilla REAL del sistema en ese estado (así la vista previa reconoce el archivo como exportado y,
// en un conteo, compara contra la existencia del momento).
//
//   A  canon: siete repuestos sin existencia, inventario inicial abierto.        → video 1
//        archivos: inicial-central.xlsx
//   B  A + inventario inicial del Almacén Central (FA-210, PF-88, BJ-14) y de la Sucursal Santiago.
//        Al Central le faltan la correa y el amortiguador.                       → video 2
//        archivos: complemento-central.xlsx (plantilla «Sin existencia»)
//   C  B + el complemento aplicado y el inventario inicial CERRADO.              → videos 3, 4 y 8
//        archivos: conteo-santiago.xlsx, sobrante-central.xlsx, recepcion-contenedor.xlsx
//   D  B + un complemento con un cero de más (140 amortiguadores en vez de 40) y cerrado. → video 5
//        archivos: correccion-central.xlsx
//   E  B (inventario inicial abierto).                                            → video 6
//        archivos: productos-nuevos.xlsx (plantilla de productos con existencia)
//   F  C + la cuenta de «Otros ingresos por ajuste de inventario» apuntando a una agrupadora. → video 7
//        archivos: sobrante-central.xlsx
//
// --volcar: guarda la base ACTUAL como canon (después de preparar.mjs) y termina.
import { execSync, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {
  CANON, ARCHIVOS, EMPRESA, CENTRAL, SANTIAGO, PROVEEDOR_2, ExcelJS, api, login, libro, encabezados,
  llenarExistencias, guardar, aplicarCarga, idAlmacen, sql, log,
} from './_lib.mjs';

const M = 'docker exec -i germiva-dev-mysql mysql -uroot';
if (process.argv.includes('--volcar')) {
  execSync(`docker exec germiva-dev-mysql mysqldump -uroot --single-transaction --routines --triggers --events --hex-blob`
    + ` --set-gtid-purged=OFF --default-character-set=utf8mb4 germiva | gzip > "${CANON}"`, { shell: '/bin/bash' });
  log('canon guardado en', CANON);
  process.exit(0);
}
if (!fs.existsSync(CANON)) {
  console.error(`Falta el canon ${CANON}: sobre una base sembrada corre preparar.mjs y luego restaurar.mjs --volcar.`);
  process.exit(1);
}

const estado = (process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'A').toUpperCase();
const t0 = Date.now();
execSync(`${M} -e "DROP DATABASE IF EXISTS germiva; CREATE DATABASE germiva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"`);
execSync(`gunzip -c "${CANON}" | ${M} --default-character-set=utf8mb4 germiva`, { shell: '/bin/bash' });
try { execFileSync('redis-cli', ['FLUSHALL'], { stdio: 'ignore' }); } catch { log('AVISO: no se pudo vaciar Redis'); }
log(`canon cargado en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
await new Promise((ok) => setTimeout(ok, 1500));
await login();
fs.rmSync(ARCHIVOS, { recursive: true, force: true });
fs.mkdirSync(ARCHIVOS, { recursive: true });

const central = idAlmacen(CENTRAL);
const santiago = idAlmacen(SANTIAGO);
const plantilla = (mode, warehouse, stockFilter = 'ALL') =>
  libro(`v1/inventory/stock-bulk-update/template?mode=${mode}&warehouseMode=SINGLE&warehouse=${warehouse}&stockFilter=${stockFilter}`);

async function carga(nombre, mode, warehouse, filtro, filas, opciones) {
  const archivo = await guardar(llenarExistencias(await plantilla(mode, warehouse, filtro), filas), nombre);
  if (opciones) await aplicarCarga(archivo, { warehouse, ...opciones });
  return archivo;
}
const INICIAL = { reason: 'INITIAL_INVENTORY' };

// ── Estado A: el archivo del inventario inicial del Almacén Central ─────────────────────────────────
const INICIAL_CENTRAL = { 'FA-210': { cantidad: 1200, costo: 185 }, 'PF-88': { cantidad: 400, costo: 650 }, 'BJ-14': { cantidad: 2500, costo: 95 } };
if (estado === 'A') await carga('inicial-central.xlsx', 'ADD', central, 'ALL', INICIAL_CENTRAL);

// ── B y siguientes: los dos almacenes cargados como inventario inicial ──────────────────────────────
if (estado !== 'A') {
  await carga('_inicial-central.xlsx', 'ADD', central, 'ALL', INICIAL_CENTRAL,
    { ...INICIAL, reference: 'Inventario inicial Almacén Central' });
  await carga('_inicial-santiago.xlsx', 'ADD', santiago, 'ALL', {
    'BJ-14': { cantidad: 500, costo: 95 }, 'CD-305': { cantidad: 60, costo: 1250 },
    'FA-210': { cantidad: 40, costo: 185 }, 'PF-88': { cantidad: 150, costo: 650 },
  }, { ...INICIAL, reference: 'Inventario inicial Sucursal Santiago' });
}
const COMPLEMENTO = (amortiguadores) => ({ 'CD-305': { cantidad: 60, costo: 1250 }, 'AM-410': { cantidad: amortiguadores, costo: 2300 } });
if (estado === 'B') await carga('complemento-central.xlsx', 'ADD', central, 'WITHOUT_STOCK', COMPLEMENTO(40));

const cerrar = () => api('POST', 'v1/inventory/stock-load/initial-phase/close');
if (estado === 'C' || estado === 'F') {
  await carga('_complemento-central.xlsx', 'ADD', central, 'WITHOUT_STOCK', COMPLEMENTO(40),
    { ...INICIAL, reference: 'Complemento del inventario inicial: estante de correas y amortiguadores' });
  await cerrar();
  log('inventario inicial cerrado');
}
if (estado === 'D') {
  await carga('_complemento-central.xlsx', 'ADD', central, 'WITHOUT_STOCK', COMPLEMENTO(140),
    { ...INICIAL, reference: 'Complemento del inventario inicial: estante de correas y amortiguadores' });
  await cerrar();
  log('inventario inicial cerrado (con 140 amortiguadores)');
  await carga('correccion-central.xlsx', 'COUNT', central, 'WITH_STOCK', { 'AM-410': { cantidad: 40 } });
}

// ── C: los archivos del conteo, del sobrante y del contenedor ───────────────────────────────────────
const SOBRANTE = { 'BJ-14': { cantidad: 36, costo: 95 }, 'FA-210': { cantidad: 10, costo: 185 } };
if (estado === 'C') {
  await carga('conteo-santiago.xlsx', 'COUNT', santiago, 'WITH_STOCK', {
    'CD-305': { cantidad: 62 }, 'BJ-14': { cantidad: 488 }, 'FA-210': { cantidad: 0 }, 'PF-88': { cantidad: 150 },
  });
  await carga('sobrante-central.xlsx', 'ADD', central, 'ALL', SOBRANTE);
  await recepcion();
}
if (estado === 'F') {
  await carga('sobrante-central.xlsx', 'ADD', central, 'ALL', SOBRANTE);
  romperCuentaDeIngreso();
}
if (estado === 'E') await productosNuevos();

/** Plantilla de la recepción (la misma que baja el diálogo «Importar líneas desde Excel»). */
async function recepcion() {
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet('Lineas');
  ws.addRow(['codigo', 'cantidad', 'costo_unitario', 'lote', 'vencimiento', 'fabricacion', 'nota']);
  ws.addRow(['FA-210', 1800, 172, null, null, null, 'Contenedor MSCU-2611']);
  ws.addRow(['PF-88', 600, 610, null, null, null, 'Contenedor MSCU-2611']);
  await guardar(wb, 'recepcion-contenedor.xlsx');
}

/** Plantilla de productos con dos kits de embrague nuevos y su existencia. */
async function productosNuevos() {
  const wb = await libro('v1/product/bulk/template/xlsx');
  const ws = wb.getWorksheet('Plantilla');
  const h = encabezados(ws);
  const filas = [
    { codigo: 'KE-500', nombre: 'Kit de embrague sedán', existencia: 30, precio_compra: 4800, precio: 7900 },
    { codigo: 'KE-520', nombre: 'Kit de embrague SUV', existencia: 20, precio_compra: 5350, precio: 8900 },
  ];
  filas.forEach((f, i) => {
    const row = ws.getRow(3 + i);
    const poner = (col, v) => { if (h[col]) row.getCell(h[col]).value = v; };
    poner('codigo', f.codigo); poner('nombre', f.nombre); poner('marca', 'Germiva Parts'); poner('itbis', 18);
    poner('unidad_medida', 'Unidad'); poner('tipo_producto', 'Automotriz'); poner('precio_compra', f.precio_compra);
    poner('maneja_inventario', 1); poner('existencia', f.existencia); poner('almacen', 'Almacén Central');
    poner('rnc_proveedor', PROVEEDOR_2.tin); poner('nombre_proveedor', PROVEEDOR_2.name);
    poner('Precio · Precio regular', f.precio);
    row.commit();
  });
  await guardar(wb, 'productos-nuevos.xlsx');
}

/** Video 7: el mapeo de la ganancia por ajuste apunta a la cuenta padre (agrupadora). */
function romperCuentaDeIngreso() {
  const fila = sql(`SELECT m.id, a.id, a.code, p.id, p.code FROM account_mappings m
    JOIN accounting_chart a ON a.id=m.account_id LEFT JOIN accounting_chart p ON p.id=a.parent_id
    WHERE m.company_id=${EMPRESA} AND m.required_mapping_type='inventory_adjustment_gain_other_income' AND m.deleted_at IS NULL LIMIT 1`)[0];
  if (!fila || !fila[3]) throw new Error('No encontré el mapeo de ganancia por ajuste o su cuenta padre');
  sql(`UPDATE account_mappings SET account_id=${fila[3]} WHERE id=${fila[0]};`);
  log(`mapeo de ganancia por ajuste: ${fila[2]} → ${fila[4]} (agrupadora)`);
}

log(`estado ${estado} listo en ${((Date.now() - t0) / 1000).toFixed(0)} s; archivos:`, fs.readdirSync(ARCHIVOS).filter((f) => !f.startsWith('_')).join(', '));
