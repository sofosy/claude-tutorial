// node seeds/productos/restaurar.mjs [estado] [--sin-canon]
// Devuelve la base al canon de la serie Productos v3 (carga completa sin binlog, R14), vacía la caché
// de Redis y aplica el ESTADO que pide el video:
//   A  (por defecto) canon tal cual: el Refresco se vende solo por unidad.
//   B  + el Refresco con «Caja ×24» (compra ★, 1 decimal, código y precio propio) y «Paquete ×6» (venta ★),
//        mínimo y máximo capturados en cajas.
//   C  B + 10 cajas compradas (240 unidades) para vender.
import { execFileSync, execSync, spawnSync } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
import { MYSQL, CANON, WINDOWS, API_DIR, AQUI, api, login, idProducto, idSocio, log, ubicacion, MOTIVO_COMPRA } from './_lib.mjs';

const estado = (process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'A').toUpperCase();
const sinCanon = process.argv.includes('--sin-canon');
const t0 = Date.now();

if (!sinCanon && WINDOWS) {
  // Por redirección de cmd: el volcado (~650 MB) no pasa por la memoria de Node.
  const archivo = process.env.CANON_ARCHIVO || CANON;
  const r = spawnSync('cmd', ['/s', '/c', `""${MYSQL}" -u root --default-character-set=utf8mb4 --init-command="SET SESSION sql_log_bin=0" germiva < "${archivo}""`],
    { encoding: 'utf8', windowsVerbatimArguments: true });
  if (r.status !== 0) { console.error(String(r.stderr).slice(0, 2000)); process.exit(1); }
  log(`canon cargado en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
} else if (!sinCanon) {
  // Fuera de Windows: el canon se arma una vez sobre la instantánea del dev-env (migraciones + preparar.sql +
  // preparar.mjs) y se guarda en Germiva-api/.dev-env/productos-canon.sql.gz. Bórralo si cambia el esquema.
  const M = 'docker exec -i germiva-dev-mysql mysql -uroot';
  const cargar = archivo => {
    execSync(`${M} -e "DROP DATABASE IF EXISTS germiva; CREATE DATABASE germiva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"`);
    execSync(`gunzip -c "${archivo}" | ${M} --default-character-set=utf8mb4 germiva`, { shell: '/bin/bash' });
  };
  if (!fs.existsSync(CANON)) {
    cargar(path.join(API_DIR, '.dev-env/seeded.sql.gz'));
    execSync('npx typeorm migration:run -d ./dist/config/typeorm.js --transaction all && node dist/scripts/sync-permissions-additive.js'
      + ' && node --env-file=.env scripts/dev-env/ensure-db-routines.cjs', { cwd: API_DIR, stdio: 'ignore', shell: '/bin/bash' });
    try { execFileSync('redis-cli', ['FLUSHALL'], { stdio: 'ignore' }); } catch { /* sin Redis local */ }
    execSync(`${M} --default-character-set=utf8mb4 germiva < "${path.join(AQUI, 'preparar-linux.sql')}"`, { shell: '/bin/bash' });
    execSync(`node "${path.join(AQUI, 'preparar.mjs')}"`, { stdio: 'inherit' });
    execSync(`docker exec germiva-dev-mysql mysqldump -uroot --single-transaction --routines --triggers --events --hex-blob`
      + ` --set-gtid-purged=OFF --default-character-set=utf8mb4 germiva | gzip > "${CANON}"`, { shell: '/bin/bash' });
    log('canon armado y guardado');
  } else cargar(CANON);
  log(`canon cargado en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
try { execFileSync('redis-cli', ['FLUSHALL'], { stdio: 'ignore' }); } catch { /* Redis en Docker: abajo */ }
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
      product: refresco, batchNumber: 'LOT-EMB-0925', quantity: 10, inventoryLocation: ubicacion(), order: 1,
      inventoryMovementType: MOTIVO_COMPRA, notes: 'Compra a Embotelladora del Caribe', partner: idSocio('130555101'),
      unitPrice: 528, productUnit: caja.id,
    });
    log('Refresco: 10 cajas en existencia (240 unidades)');
  }
}
log(`estado ${estado} listo en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
