// node seeds/productos/preparar.mjs — deja la empresa 1 «Tienda Germiva» en el estado de partida de la
// serie Productos v3 (unidades y empaques, DP-033). Se corre UNA vez sobre base-limpia.sql y luego
// fijar.mjs vuelca el canon. Entre tomas: restaurar.mjs [estado].
import { sql, uno, api, idProducto, idSocio, log, EMPRESA, UBICACION, MOTIVO_COMPRA } from './_lib.mjs';

// ── 1. Ajustes de la base que la cámara vería ──────────────────────────────────────────────────────
sql(`
UPDATE subscriptions SET expirationDate='2027-12-31 23:00:00', nextBillingDate='2027-12-31 23:00:00'
  WHERE company_id=${EMPRESA} AND status='ACTIVE';
-- Unidades de QA en el catálogo global: salen en todos los selectores de unidad.
UPDATE unit_measures SET deleted_at=NOW() WHERE deleted_at IS NULL AND (name LIKE 'QA %' OR name LIKE 'QA unidad%');
-- Ubicación de QA en el Almacén Sur.
UPDATE inventory_location SET deleted_at=NOW() WHERE id=32 AND position='QA-01';
-- La empresa trabaja con empaques: sin esto la app cachea «sin empaques» al iniciar sesión y los selectores de
-- unidad no aparecen hasta recargar (ver H-VP-01 en productos-02).
UPDATE company_configs SET advanced_units_enabled=1 WHERE company_id=${EMPRESA};
-- R18: el aviso de configuración incompleta ya se vio.
UPDATE user_company_preferences SET incomplete_config_notice_seen_at=COALESCE(incomplete_config_notice_seen_at, NOW())
  WHERE company_id=${EMPRESA};
`);
log('ajustes SQL listos');

// ── 2. Socios ───────────────────────────────────────────────────────────────────────────────────────
async function socio(cuerpo) {
  const id = idSocio(cuerpo.tin);
  if (id) return id;
  const r = await api('POST', 'v1/partner', cuerpo);
  log('socio', cuerpo.name, r.id);
  return r.id;
}
const proveedor = await socio({ name: 'Embotelladora del Caribe S.R.L.', tin: '130555101', partnerType: ['SUPPLIER'], partnerCategory: 'BUSINESS' });
await socio({ name: 'Colmado La Esquina', tin: '130555102', partnerType: ['CUSTOMER'], partnerCategory: 'BUSINESS', customerType: 'REGULAR' });
await socio({ name: 'Agroindustrial del Cibao S.R.L.', tin: '130555103', partnerType: ['SUPPLIER'], partnerCategory: 'BUSINESS' });
await socio({ name: 'Galletera Nacional S.A.', tin: '130555104', partnerType: ['SUPPLIER'], partnerCategory: 'BUSINESS' });

// ── 3. Productos de partida ─────────────────────────────────────────────────────────────────────────
const BASE = {
  category: 'PRODUCT', managesInventory: true, usesExpirationDate: false, usesBatchControl: false,
  visibleInStore: false, searchEngineIndexable: true, additionalTaxCodes: [], descriptionHtml: null,
  incomeAccount: null, purchaseExpenseAccount: null, presumptiveTaxRegime: null, unitMeasureValue: null,
  tariffCode: null, originCountry: null, netWeight: null, grossWeight: null, volume: null,
};
async function producto(datos, precio) {
  let id = idProducto(datos.name);
  if (!id) {
    const r = await api('POST', 'v1/product', { ...BASE, ...datos });
    id = r.id;
    log('producto', datos.name, id);
  }
  const tienePrecio = +uno(`SELECT COUNT(*) FROM prices WHERE product_id=${id} AND deleted_at IS NULL`);
  if (!tienePrecio && precio) {
    const neto = precio.incluido ? (precio.monto / (1 + precio.tasa)).toFixed(2) : precio.monto.toFixed(2);
    await api('POST', 'v1/price', {
      product: id, priceListId: 1, price: neto, taxIncluded: !!precio.incluido, priority: 1, description: '',
      active: true, currency: 32, ...(precio.incluido ? { originalGrossAmount: String(precio.monto) } : {}),
    });
  }
  return id;
}
async function entrada(producto, cantidad, costo, partner, productUnit) {
  await api('POST', 'v1/inventory/movement/entry', {
    product: producto, batchNumber: `LOT-SEM-${producto}-${Date.now() % 100000}`, quantity: cantidad,
    inventoryLocation: UBICACION, order: 1, inventoryMovementType: MOTIVO_COMPRA, notes: '', partner,
    unitPrice: costo, ...(productUnit ? { productUnit } : {}),
  });
}

// Refresco: se vende hoy por unidad; el video 2 le agrega la caja y el paquete.
await producto({ name: 'Refresco Caribe Cola lata', brand: 'Caribe Cola', tax: 1, purchaseTax: 1, unitMeasure: 43,
  productType: 8, purchasePrice: 22, minStock: 48, maxStock: 240 }, { monto: 35, incluido: true, tasa: 0.18 });

// Galletas: se llevan en CAJAS (unidad base Caja/Cajón); el video 5 las convierte a unidades sueltas.
const galletas = await producto({ name: 'Galletas soda Crocante', brand: 'Crocante', tax: 1, purchaseTax: 1, unitMeasure: 6,
  productType: 8, purchasePrice: 180, minStock: 5, maxStock: 40 }, { monto: 300, incluido: true, tasa: 0.18 });
if (!+uno(`SELECT COUNT(*) FROM inventory_movement im JOIN inventory i ON i.id=im.inventory_id WHERE i.product_id=${galletas}`)) {
  await entrada(galletas, 20, 180, idSocio('130555104'));
  log('entrada galletas 20 cajas');
}

// Habichuelas: se llevan por libra, exentas de ITBIS; el video 5 agrega el saco y el kilo.
const habichuelas = await producto({ name: 'Habichuelas rojas', brand: 'La Finca', tax: 4, purchaseTax: 4, unitMeasure: 23,
  productType: 8, purchasePrice: 52, minStock: 100, maxStock: 600 }, { monto: 85, incluido: false, tasa: 0 });
if (!+uno(`SELECT COUNT(*) FROM inventory_movement im JOIN inventory i ON i.id=im.inventory_id WHERE i.product_id=${habichuelas}`)) {
  await entrada(habichuelas, 250, 52, idSocio('130555103'));
  log('entrada habichuelas 250 lb');
}

log('listo. Ahora: node seeds/productos/fijar.mjs');
