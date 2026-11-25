// Utilidades de la serie «Existencias» (cargas masivas de existencias, 11/2026): empresa 1 renombrada
// «Repuestos Germiva, SRL», usuario admin. SQL sin binlog (R14); API por el login de desarrollo.
// Sin dependencias npm propias: exceljs se toma del node_modules de Germiva-api.
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
export const RAIZ = path.resolve(AQUI, '../..');
export const ARCHIVOS = path.join(AQUI, 'archivos');
export const API = process.env.GERMIVA_API || 'http://localhost:3001/api';
export const API_DIR = path.resolve(process.env.GERMIVA_API_DIR || path.join(RAIZ, '../../Germiva-api'));
export const CANON = path.join(API_DIR, '.dev-env/existencias-canon.sql.gz');
export const EMPRESA = 1;

const requireApi = createRequire(path.join(API_DIR, 'package.json'));
export const ExcelJS = requireApi('exceljs');

export function sql(texto) {
  const out = execFileSync('docker', ['exec', '-i', 'germiva-dev-mysql', 'mysql', '-uroot', '--default-character-set=utf8mb4',
    '-N', '-B', '--init-command=SET SESSION sql_log_bin=0', 'germiva'], { input: texto, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
  return out.split(/\r?\n/).filter(Boolean).map((l) => l.split('\t'));
}
export const uno = (s) => sql(s)[0]?.[0];

let token = null;
export async function login() {
  const r = await fetch(`${API}/auth/dev/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin' }),
  });
  const j = await r.json();
  if (!j.accessToken) throw new Error('login admin: ' + JSON.stringify(j).slice(0, 300));
  token = j.accessToken;
  return token;
}

async function pedir(metodo, ruta, init = {}) {
  if (!token) await login();
  const r = await fetch(`${API}/${ruta}`, { method: metodo, ...init, headers: { Authorization: `Bearer ${token}`, ...(init.headers ?? {}) } });
  return r;
}

export async function api(metodo, ruta, cuerpo) {
  const r = await pedir(metodo, ruta, {
    headers: { 'Content-Type': 'application/json' },
    body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
  });
  const txt = await r.text();
  let j; try { j = JSON.parse(txt); } catch { j = txt; }
  if (!r.ok) throw new Error(`${metodo} ${ruta} → ${r.status}: ${txt.slice(0, 600)}`);
  return j?.data !== undefined && j?.statusCode === undefined ? j.data : j;
}

/** Descarga un archivo del API (plantillas) y lo devuelve como libro de exceljs. */
export async function libro(ruta) {
  const r = await pedir('GET', ruta);
  if (!r.ok) throw new Error(`GET ${ruta} → ${r.status}: ${(await r.text()).slice(0, 400)}`);
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(Buffer.from(await r.arrayBuffer()));
  return wb;
}

export function encabezados(ws) {
  const h = {};
  ws.getRow(1).eachCell((c, i) => (h[String(c.value).trim()] = i));
  return h;
}

/** Llena una plantilla de existencias: { codigo: { cantidad, costo } } en la columna del modo. */
export function llenarExistencias(wb, filas) {
  const ws = wb.getWorksheet('Existencias');
  const h = encabezados(ws);
  const columna = h.cantidad_a_ingresar ?? h.existencia_contada;
  const usados = new Set();
  ws.eachRow((row, n) => {
    if (n === 1) return;
    const dato = filas[String(row.getCell(h.codigo).value)];
    if (!dato) return;
    row.getCell(columna).value = dato.cantidad;
    if (dato.costo !== undefined) row.getCell(h.costo_unitario).value = dato.costo;
    usados.add(String(row.getCell(h.codigo).value));
  });
  const faltan = Object.keys(filas).filter((c) => !usados.has(c));
  if (faltan.length) throw new Error(`La plantilla no trae: ${faltan.join(', ')}`);
  return wb;
}

export async function guardar(wb, nombre) {
  fs.mkdirSync(ARCHIVOS, { recursive: true });
  const destino = path.join(ARCHIVOS, nombre);
  await wb.xlsx.writeFile(destino);
  return destino;
}

/** Aplica una carga de existencias por el API (vista previa → aplicar → espera el resultado). */
export async function aplicarCarga(archivo, opciones) {
  const form = () => {
    const f = new FormData();
    f.append('file', new Blob([fs.readFileSync(archivo)]), path.basename(archivo));
    f.append('reason', opciones.reason);
    f.append('reference', opciones.reference);
    f.append('postingMode', opciones.postingMode ?? 'CONSOLIDATED');
    if (opciones.warehouse) f.append('warehouse', String(opciones.warehouse));
    if (opciones.confirmZeroing) f.append('confirmZeroing', 'true');
    return f;
  };
  const base = 'v1/inventory/stock-bulk-update';
  const r = await pedir('POST', `${base}/apply`, { body: form() });
  const txt = await r.text();
  if (!r.ok) throw new Error(`apply ${path.basename(archivo)} → ${r.status}: ${txt.slice(0, 600)}`);
  const { jobId } = JSON.parse(txt);
  for (let i = 0; i < 240; i++) {
    const job = await api('GET', `${base}/jobs/${jobId}`);
    if (['COMPLETED', 'FAILED', 'ABORTED_VALIDATION'].includes(job.status)) {
      if (job.status !== 'COMPLETED') throw new Error(`carga ${jobId}: ${job.status} ${job.errorMessage ?? ''}`);
      const posting = job.result?.posting;
      log(`carga #${jobId} ${path.basename(archivo)}: ${job.result?.applied} aplicadas, asiento ${posting?.status ?? '—'} ${posting?.entryNumber ?? ''}`);
      return job;
    }
    await new Promise((ok) => setTimeout(ok, 500));
  }
  throw new Error(`carga ${jobId}: no terminó`);
}

export const idProducto = (codigo) =>
  +uno(`SELECT id FROM products WHERE company_id=${EMPRESA} AND code='${codigo}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
export const idSocio = (rnc) =>
  +uno(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND tin='${rnc}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
export const idAlmacen = (codigo) =>
  +uno(`SELECT id FROM warehouse WHERE company_id=${EMPRESA} AND code='${codigo}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);

export function log(...a) { console.log(new Date().toISOString().slice(11, 19), ...a); }

// ── Datos de la serie ────────────────────────────────────────────────────────────────────────────────
export const CENTRAL = 'ALM-CENTRAL';
export const SANTIAGO = 'SUC-SANTIAGO';
export const PROVEEDOR = { name: 'Autopartes del Caribe Germiva, SRL', tin: '130555301' };
export const PROVEEDOR_2 = { name: 'Repuestos del Cibao Germiva, SRL', tin: '130555302' };
export const PROVEEDORES = [PROVEEDOR, PROVEEDOR_2];
// Cada repuesto con su proveedor habitual (la ficha y la importación de productos lo guardan).
export const PRODUCTOS = [
  { code: 'FA-210', name: 'Filtro de aceite', brand: 'Germiva Parts', purchasePrice: 185, proveedor: PROVEEDOR.tin },
  { code: 'PF-88', name: 'Pastillas de freno delanteras (juego)', brand: 'Germiva Parts', purchasePrice: 650, proveedor: PROVEEDOR.tin },
  { code: 'BJ-14', name: 'Bujía de iridio', brand: 'Germiva Parts', purchasePrice: 95, proveedor: PROVEEDOR_2.tin },
  { code: 'CD-305', name: 'Correa de distribución', brand: 'Germiva Parts', purchasePrice: 1250, proveedor: PROVEEDOR_2.tin },
  { code: 'AM-410', name: 'Amortiguador delantero', brand: 'Germiva Parts', purchasePrice: 2300, proveedor: PROVEEDOR.tin },
  { code: 'LF-04', name: 'Líquido de frenos DOT 4', brand: 'Germiva Parts', purchasePrice: 240, proveedor: PROVEEDOR_2.tin },
  { code: 'RD-90', name: 'Radiador de aluminio', brand: 'Germiva Parts', purchasePrice: 6800, proveedor: PROVEEDOR.tin },
];
