// node seeds/fabricacion/preparar.mjs [A|B|C] [--sin-reset]
// Deja la base local en el estado de partida de la serie «Fabricación»:
//   A  panadería con materia prima en la Despensa y el bizcocho SIN lista de materiales (video 1).
//   B  A + la lista de materiales del bizcocho publicada (video 2).
//   C  B + una orden cerrada (24 bizcochos) y otra con el material reservado (video 3).
// Parte SIEMPRE de la instantánea sembrada del dev-env (Germiva-api/.dev-env/seeded.sql.gz), salvo --sin-reset.
import { execSync, execFileSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { sql, uno, api, login, idProducto, idUbicacion, log, EMPRESA } from './_lib.mjs';

const estado = (process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'A').toUpperCase();
const t0 = Date.now();
const LIBRA = 23, UNIDAD = 43, ITBIS = 1, EXENTO = 4, ALIMENTOS = 8, MOTIVO_COMPRA = 1, ALMACEN = 1;
const BASE = '/v1/inventory/manufacturing'.slice(1);

if (!process.argv.includes('--sin-reset')) {
  // La instantánea del dev-env puede ir por detrás del código: tras restaurarla se aplican las migraciones
  // (lo mismo que hace up.sh) y el resultado se guarda como base local de la serie, para que las siguientes
  // restauraciones tarden segundos. Borra .dev-env/fabricacion-base.sql.gz cuando cambie el esquema.
  const apiDir = path.resolve(process.env.GERMIVA_API_DIR || '../Germiva-api');
  const base = path.join(apiDir, '.dev-env/fabricacion-base.sql.gz');
  const M = 'docker exec -i germiva-dev-mysql mysql -uroot';
  const cargar = archivo => {
    execSync(`${M} -e "DROP DATABASE IF EXISTS germiva; CREATE DATABASE germiva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"`);
    execSync(`gunzip -c "${archivo}" | ${M} germiva`, { shell: '/bin/bash' });
  };
  if (fs.existsSync(base)) cargar(base);
  else {
    cargar(path.join(apiDir, '.dev-env/seeded.sql.gz'));
    execSync('npx typeorm migration:run -d ./dist/config/typeorm.js --transaction all && node dist/scripts/sync-permissions-additive.js'
      + ' && node --env-file=.env scripts/dev-env/ensure-db-routines.cjs', { cwd: apiDir, stdio: 'ignore', shell: '/bin/bash' });
    execSync(`docker exec germiva-dev-mysql mysqldump -uroot --single-transaction --routines --triggers --events --hex-blob`
      + ` --set-gtid-purged=OFF --default-character-set=utf8mb4 germiva | gzip > "${base}"`, { shell: '/bin/bash' });
    log('base local de la serie guardada');
  }
  log(`base restaurada en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
// Redis corre en Docker o suelto, según la máquina: se prueba en ese orden.
try { execFileSync('docker', ['exec', 'germiva-dev-redis', 'redis-cli', 'FLUSHALL'], { stdio: 'ignore' }); }
catch { try { execFileSync('redis-cli', ['FLUSHALL'], { stdio: 'ignore' }); } catch { log('AVISO: no se pudo vaciar Redis'); } }

sql(`
UPDATE companies SET legalName='Panadería Germiva Demo S.R.L.', tradeName='Panadería Germiva', rnc='130555001',
  email='ventas@panaderia.germiva.com', website='https://germiva.com' WHERE id=${EMPRESA};
-- Productos sembrados con el mismo nombre que la materia prima de la serie: saldrían duplicados en los buscadores.
UPDATE products SET deleted_at=NOW() WHERE company_id=${EMPRESA} AND id<100 AND name IN ('Harina de Trigo','Azúcar Refinada') AND deleted_at IS NULL;
UPDATE users SET email='admin@germiva.com', current_company_id=${EMPRESA} WHERE id=1;
UPDATE subscriptions SET expirationDate='2027-12-31 23:00:00', nextBillingDate='2027-12-31 23:00:00'
  WHERE company_id=${EMPRESA} AND status='ACTIVE';
UPDATE user_company_preferences SET incomplete_config_notice_seen_at=COALESCE(incomplete_config_notice_seen_at, NOW())
  WHERE company_id=${EMPRESA};
`);
await login();

for (const position of ['Despensa', 'Vitrina']) {
  if (!idUbicacion(position)) await api('POST', 'v1/inventory/location', { position, warehouse: ALMACEN });
}
const DESPENSA = idUbicacion('Despensa'), VITRINA = idUbicacion('Vitrina');
let proveedor = +uno(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND tin='130555201' AND deleted_at IS NULL LIMIT 1`);
if (!proveedor) proveedor = (await api('POST', 'v1/partner', { name: 'Molinos Germiva del Caribe', tin: '130555201', partnerType: ['SUPPLIER'], partnerCategory: 'BUSINESS' })).id;

const COMUN = {
  category: 'PRODUCT', managesInventory: true, usesExpirationDate: false, usesBatchControl: true,
  visibleInStore: false, productType: ALIMENTOS, unitMeasureValue: '1',
};
async function producto(name, unitMeasure, costo, tax, existencia, lote) {
  let id = idProducto(name);
  if (!id) {
    await api('POST', 'v1/product', { ...COMUN, name, description: name, unitMeasure, tax, purchaseTax: tax, purchasePrice: costo.toFixed(2) });
    id = idProducto(name);
    log('producto', name, id);
    if (existencia) {
      await api('POST', 'v1/inventory/movement/entry', {
        product: id, batchNumber: lote, quantity: existencia, inventoryLocation: DESPENSA, order: 1,
        inventoryMovementType: MOTIVO_COMPRA, notes: 'Compra a Molinos Germiva del Caribe', partner: proveedor, unitPrice: costo,
      });
    }
  }
  return id;
}
const harina = await producto('Harina de trigo', LIBRA, 30, EXENTO, 60, 'HAR-1101');
const azucar = await producto('Azúcar crema', LIBRA, 38, EXENTO, 40, 'AZU-1101');
const huevos = await producto('Huevos', UNIDAD, 9.5, EXENTO, 150, 'HUE-1115');
const mantequilla = await producto('Mantequilla', LIBRA, 140, ITBIS, 10, 'MAN-1110');
const bizcocho = await producto('Bizcocho de vainilla', UNIDAD, 0, ITBIS, 0);

const LISTA = {
  productId: bizcocho, yieldQty: 12, tolerance: 5, laborMinutes: 90, laborRate: 400, overheadCost: 120,
  ingredients: [
    { productId: harina, quantity: 8 }, { productId: azucar, quantity: 5 },
    { productId: huevos, quantity: 30 }, { productId: mantequilla, quantity: 3 },
  ],
};
if (estado === 'B' || estado === 'C') {
  const receta = await api('POST', `${BASE}/recipes`, LISTA);
  const recetaId = receta.id ?? receta.recipe?.id ?? +uno(`SELECT MAX(id) FROM manufacturing_recipes WHERE company_id=${EMPRESA}`);
  log('lista de materiales publicada', recetaId);
  if (estado === 'C') {
    const orden = async planned => {
      const o = await api('POST', `${BASE}/orders`, { requestKey: crypto.randomUUID(), recipeId: recetaId, planned, originId: DESPENSA, destinationId: VITRINA });
      const id = o.id ?? o.order?.id ?? +uno(`SELECT MAX(id) FROM manufacturing_orders WHERE company_id=${EMPRESA}`);
      await api('POST', `${BASE}/orders/${id}/reserve`, {});
      return id;
    };
    const primera = await orden(24);
    const det = await api('GET', `${BASE}/orders/${primera}`);
    console.log(JSON.stringify(det).slice(0, 3000));
  }
}
log(`estado ${estado} listo en ${((Date.now() - t0) / 1000).toFixed(0)} s (Despensa ${DESPENSA}, Vitrina ${VITRINA})`);
