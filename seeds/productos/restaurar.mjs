// node seeds/productos/restaurar.mjs [estado] [--sin-canon]
// Devuelve la base al canon de la serie Productos v3 (carga completa sin binlog, R14), vacía la caché
// de Redis y aplica el ESTADO que pide el video:
//   A  (por defecto) canon tal cual: el Refresco se vende solo por unidad.
//   B  + el Refresco con «Caja ×24» (compra ★, 1 decimal, código y precio propio) y «Paquete ×6» (venta ★),
//        mínimo y máximo capturados en cajas.
//   C  B + 10 cajas compradas (240 unidades) para vender.
import { execFileSync, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import { MYSQL, CANON, api, login, idProducto, idSocio, log, UBICACION, MOTIVO_COMPRA } from './_lib.mjs';

const estado = (process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'A').toUpperCase();
const sinCanon = process.argv.includes('--sin-canon');
const t0 = Date.now();

if (!sinCanon) {
  // Por redirección de cmd: el volcado (~650 MB) no pasa por la memoria de Node.
  const archivo = process.env.CANON_ARCHIVO || CANON;
  const r = spawnSync('cmd', ['/s', '/c', `""${MYSQL}" -u root --default-character-set=utf8mb4 --init-command="SET SESSION sql_log_bin=0" germiva < "${archivo}""`],
    { encoding: 'utf8', windowsVerbatimArguments: true });
  if (r.status !== 0) { console.error(String(r.stderr).slice(0, 2000)); process.exit(1); }
  log(`canon cargado en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
try { execFileSync('docker', ['exec', 'germiva-redis', 'redis-cli', 'FLUSHALL'], { stdio: 'ignore' }); } catch { log('AVISO: no se pudo vaciar Redis'); }

await login();

export const EMPAQUES_REFRESCO = [
  { unitMeasure: 6, label: 'Caja ×24', factor: 24, quantityDecimals: 1, barcode: '7460001000243', salePrice: 780,
    salePriceTaxIncluded: true, forPurchase: true, forSale: true, isDefaultPurchase: true, isDefaultSale: false,
    active: true, netWeight: null, grossWeight: null, volume: null },
  { unitMeasure: 31, label: 'Paquete ×6', factor: 6, quantityDecimals: 0, barcode: null, salePrice: null,
    salePriceTaxIncluded: false, forPurchase: false, forSale: true, isDefaultPurchase: false, isDefaultSale: true,
    active: true, netWeight: null, grossWeight: null, volume: null },
];

if (estado === 'B' || estado === 'C') {
  const refresco = idProducto('Refresco Caribe Cola lata');
  const unidades = await api('PUT', `v1/product/${refresco}/units`, { units: EMPAQUES_REFRESCO });
  log('Refresco con empaques', (unidades?.units ?? unidades)?.length ?? '');
  if (estado === 'C') {
    const lista = await api('GET', `v1/product/${refresco}/units`);
    const caja = (lista?.units ?? lista).find(u => +u.factor === 24 && u.active !== false);
    await api('POST', 'v1/inventory/movement/entry', {
      product: refresco, batchNumber: 'LOT-EMB-0925', quantity: 10, inventoryLocation: UBICACION, order: 1,
      inventoryMovementType: MOTIVO_COMPRA, notes: 'Compra a Embotelladora del Caribe', partner: idSocio('130555101'),
      unitPrice: 528, productUnit: caja.id,
    });
    log('Refresco: 10 cajas en existencia (240 unidades)');
  }
}
log(`estado ${estado} listo en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
