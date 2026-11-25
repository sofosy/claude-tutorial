// node seeds/existencias/preparar.mjs — deja la empresa 1 como «Repuestos Germiva, SRL», la importadora
// ficticia de la serie Existencias: dos almacenes con ubicación, siete repuestos sin existencia, el
// proveedor del contenedor y el inventario inicial abierto. Se corre UNA vez sobre la base sembrada
// (`up.sh --source seed`); restaurar.mjs vuelca el canon la primera vez y lo recarga entre tomas.
import { sql, uno, api, log, EMPRESA, CENTRAL, SANTIAGO, PROVEEDORES, PRODUCTOS, idProducto, idSocio, idAlmacen } from './_lib.mjs';

// ── 1. Ajustes de la base que la cámara vería ──────────────────────────────────────────────────────
sql(`
UPDATE companies SET legalName='Repuestos Germiva, SRL', tradeName='Repuestos Germiva', rnc='130555050',
  email='ventas@repuestos.germiva.com', website='https://germiva.com' WHERE id=${EMPRESA};
UPDATE users SET email='admin@germiva.com', current_company_id=${EMPRESA} WHERE id=1;
UPDATE subscriptions SET expirationDate='2027-12-31 23:00:00', nextBillingDate='2027-12-31 23:00:00'
  WHERE company_id=${EMPRESA} AND status='ACTIVE';
UPDATE user_company_preferences SET incomplete_config_notice_seen_at=COALESCE(incomplete_config_notice_seen_at, NOW())
  WHERE company_id=${EMPRESA};
-- La importadora solo vende repuestos: el catálogo y los almacenes sembrados no salen en cámara.
UPDATE products SET deleted_at=NOW() WHERE company_id=${EMPRESA} AND deleted_at IS NULL
  AND (code IS NULL OR code NOT IN (${PRODUCTOS.map((p) => `'${p.code}'`).join(',')}));
UPDATE warehouse SET deleted_at=NOW() WHERE company_id=${EMPRESA} AND deleted_at IS NULL AND code NOT IN ('${CENTRAL}','${SANTIAGO}');
`);
log('ajustes SQL listos');

// ── 2. Almacenes (cada uno nace con su «Ubicación Principal») ───────────────────────────────────────
async function almacen(code, name, isPrimary) {
  const id = idAlmacen(code);
  if (id) return id;
  const r = await api('POST', 'v1/warehouse', { code, name, type: 'PHYSICAL', status: 'ACTIVE', isPrimary });
  log('almacén', name, r.id);
  return r.id;
}
const central = await almacen(CENTRAL, 'Almacén Central', true);
const santiago = await almacen(SANTIAGO, 'Sucursal Santiago', false);
const ubicacion = +uno(`SELECT id FROM inventory_location WHERE warehouse_id=${central} AND deleted_at IS NULL ORDER BY id LIMIT 1`);
sql(`UPDATE company_configs SET default_warehouse_id=${central}, default_inventory_location_id=${ubicacion} WHERE company_id=${EMPRESA};`);

// ── 3. Proveedores (el primero despacha el contenedor del video 8) ──────────────────────────────────
for (const p of PROVEEDORES) {
  if (idSocio(p.tin)) continue;
  const r = await api('POST', 'v1/partner', { ...p, legalName: p.name, partnerType: ['SUPPLIER'], partnerCategory: 'BUSINESS' });
  log('proveedor', p.name, r.id);
}

// ── 4. Repuestos, sin existencia ────────────────────────────────────────────────────────────────────
const BASE = {
  category: 'PRODUCT', managesInventory: true, usesExpirationDate: false, usesBatchControl: false,
  visibleInStore: false, searchEngineIndexable: true, additionalTaxCodes: [], descriptionHtml: null,
  incomeAccount: null, purchaseExpenseAccount: null, presumptiveTaxRegime: null, unitMeasureValue: null,
  tariffCode: null, originCountry: null, netWeight: null, grossWeight: null, volume: null,
  tax: 1, purchaseTax: 1, unitMeasure: 43, productType: 11,
};
for (const { proveedor, ...p } of PRODUCTOS) {
  const partners = [idSocio(proveedor)];
  const id = idProducto(p.code);
  if (!id) {
    const r = await api('POST', 'v1/product', { ...BASE, ...p, partners });
    log('producto', p.code, r.id);
  } else {
    await api('PATCH', `v1/product/${id}`, { partners });
  }
}

// ── 5. Inventario inicial abierto y sin cargas previas ──────────────────────────────────────────────
sql(`UPDATE company_configs SET inventory_initial_closed_at=NULL, inventory_initial_closed_by_user_id=NULL WHERE company_id=${EMPRESA};`);
log('listo:', { central, santiago, ubicacion, productos: PRODUCTOS.length });
