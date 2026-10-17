// node seeds/pos/sembrar.mjs [--desde-s0]
// Siembra el estado del video «Punto de venta» (/pos) sobre la empresa demo 43 «Ferretería El Progreso».
// IDEMPOTENTE: cada paso busca antes lo que ya existe (por código / nombre / RNC) y solo crea o corrige
// lo que falta. Todo por el API, con los mismos payloads que los formularios del front; SQL directo solo
// para lecturas y para el plan de la suscripción (no tiene endpoint de empresa: lo cambia la plataforma).
//   --desde-s0 → antes de sembrar devuelve la empresa al estado S0 de la serie de Cajas.
// Las imágenes van aparte (imagenes.mjs): dependen de la descarga de fotos.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { api, sql, log, EMPRESA } from '../cajas/_lib.mjs';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const CAJAS = path.join(AQUI, '..', 'cajas');
const ADMIN = 'admin.progreso';
const uno = s => sql(s)[0]?.[0];
const esc = s => String(s).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
const catalogo = JSON.parse(fs.readFileSync(path.join(AQUI, 'catalogo.json'), 'utf8'));

if (process.argv.includes('--desde-s0')) {
  execFileSync('node', [path.join(CAJAS, 'restaurar.mjs'), 'S0'], { stdio: 'inherit' });
}

// ── 1. Plan 15 «Empresarial»: el 2 «Emprendedor» no trae SALES_CREDIT («Crédito del cliente», H-17)
//       ni SALES_DISCOUNT (descuentos globales del ticket). Mismo cambio que cajas/plan-s8.mjs.
execFileSync('node', [path.join(CAJAS, 'plan-s8.mjs'), 'on'], { stdio: 'inherit' });

// ── 2. Categorías (product_types de la empresa) — formulario «Tipo de producto»
const tipos = {};
for (const nombre of catalogo.categorias) {
  let id = uno(`SELECT id FROM product_types WHERE company_id=${EMPRESA} AND name='${esc(nombre)}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) {
    const r = await api(ADMIN, 'POST', 'product-types', { name: nombre, category: 'PRODUCT', description: `Artículos de ${nombre.toLowerCase()} de la ferretería` });
    id = r.id; log('categoría', nombre, id);
  }
  tipos[nombre] = +id;
}

// ── 3. Productos + precio regular (formulario de producto: POST v1/product y luego POST v1/price)
const DOP = +uno(`SELECT id FROM currencies WHERE code='DOP' LIMIT 1`);
const ITBIS18 = 1, EXENTO = 4; // taxes: «ITBIS Tasa General» 18 % / «Exento de ITBIS» (codeNumber 4)
for (const p of catalogo.productos) {
  const tax = p.exento ? EXENTO : ITBIS18;
  let id = uno(`SELECT id FROM products WHERE company_id=${EMPRESA} AND code='${esc(p.sku)}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) {
    const r = await api(ADMIN, 'POST', 'v1/product', {
      category: 'PRODUCT', name: p.nombre, code: p.sku, descriptionHtml: null,
      tax, purchaseTax: tax, managesInventory: true, usesExpirationDate: false, usesBatchControl: false,
      visibleInStore: false, purchasePrice: p.costo, productType: tipos[p.categoria], active: true,
      fiscalAttributes: {}, presumptiveTaxRegime: null,
    });
    id = r.id; log('producto', p.sku, id);
  } else if (!+uno(`SELECT COUNT(*) FROM products WHERE id=${id} AND name='${esc(p.nombre)}' AND tax_id=${tax} AND purchase_tax_id=${tax}
      AND product_type_id=${tipos[p.categoria]} AND purchasePrice=${p.costo} AND active=1 AND managesInventory=1`)) {
    // corrige lo que el canon pide (nombre, categoría, impuesto, costo, activo) si alguien lo cambió
    await api(ADMIN, 'PATCH', `v1/product/${id}`, { name: p.nombre, tax, purchaseTax: tax, purchasePrice: p.costo, productType: tipos[p.categoria], managesInventory: true, active: true });
  }
  p.id = +id;
  const precio = sql(`SELECT id, price FROM prices WHERE product_id=${id} AND deleted_at IS NULL AND customerType='REGULAR' ORDER BY priority, id LIMIT 1`)[0];
  if (!precio) {
    await api(ADMIN, 'POST', 'v1/price', { product: p.id, customerType: 'REGULAR', price: String(p.precio), taxIncluded: false, priority: 1, description: '', active: true, currency: DOP });
  } else if (Number(precio[1]) !== p.precio) {
    await api(ADMIN, 'PATCH', `v1/price/${precio[0]}`, { customerType: 'REGULAR', price: String(p.precio), taxIncluded: false, priority: 1, description: '', active: true, currency: DOP });
  }
}

// ── 4. Existencias en el Almacén Principal: entrada «Carga inicial de existencias» (tipo 17) o
//       ajuste (3 positivo / 9 negativo) por la diferencia — mismo endpoint que «Movimiento rápido».
const UBIC = +uno(`SELECT l.id FROM inventory_location l JOIN warehouse w ON w.id=l.warehouse_id WHERE l.company_id=${EMPRESA} AND w.isPrimary=1 AND l.deleted_at IS NULL ORDER BY l.id LIMIT 1`);
const disponible = pid => Number(uno(`SELECT IFNULL(SUM(quantity - reservedStock),0) FROM inventory WHERE product_id=${pid} AND company_id=${EMPRESA} AND deleted_at IS NULL`) ?? 0);
for (const p of catalogo.productos) {
  const actual = disponible(p.id);
  const delta = p.stock - actual;
  if (delta > 0) {
    const tieneMov = +uno(`SELECT COUNT(*) FROM inventory_movement m JOIN inventory i ON i.id=m.inventory_id WHERE i.product_id=${p.id} AND m.company_id=${EMPRESA}`) > 0;
    await api(ADMIN, 'POST', 'v1/inventory/movement/entry', {
      product: p.id, batchNumber: `INI-${p.sku}`, quantity: delta, inventoryLocation: UBIC, order: 1,
      inventoryMovementType: tieneMov ? 3 : 17, unitPrice: p.costo,
      notes: tieneMov ? 'Ajuste al canon del video de Punto de venta' : 'Saldo inicial de la ferretería',
    });
    log('existencia', p.sku, actual, '→', p.stock);
  } else if (delta < 0) {
    await api(ADMIN, 'POST', 'v1/inventory/movement/exit', {
      product: p.id, quantity: -delta, inventoryLocation: UBIC, order: 1, inventoryMovementType: 9,
      notes: 'Ajuste al canon del video de Punto de venta',
    });
    log('existencia', p.sku, actual, '→', p.stock);
  }
}

// ── 5. Clientes (formulario de socio: POST v1/partner)
const dvRnc = b8 => { const w = [7, 9, 8, 6, 5, 4, 3, 2]; const r = [...b8].reduce((a, d, i) => a + d * w[i], 0) % 11; return b8 + (r === 0 ? 2 : r === 1 ? 1 : 11 - r); };
const dvCedula = b10 => { const s = [...b10].reduce((a, d, i) => { const m = +d * (i % 2 ? 2 : 1); return a + (m > 9 ? m - 9 : m); }, 0); return b10 + ((10 - (s % 10)) % 10); };
const libre = doc => !+uno(`SELECT COUNT(*) FROM taxpayers WHERE rnc='${doc}'`) && !+uno(`SELECT COUNT(*) FROM partners WHERE tin='${doc}' AND company_id=${EMPRESA}`);
async function cliente(nombre, crear) {
  let id = uno(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND name='${esc(nombre)}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) { const r = await api(ADMIN, 'POST', 'v1/partner', crear()); id = r.id; log('cliente', nombre, id, r.tin); }
  return +id;
}
const pena = await cliente('Constructora Hermanos Peña', () => {
  let rnc; for (let n = 13055520; !rnc || !libre(rnc); n++) rnc = dvRnc(String(n));
  return { name: 'Constructora Hermanos Peña', legalName: 'Constructora Hermanos Peña SRL', tin: rnc, documentType: 'RNC',
    partnerType: ['CUSTOMER'], customerType: 'REGULAR', partnerCategory: 'BUSINESS', ncfType: 1 };
});
const maria = await cliente('María Fernández', () => {
  let ced; for (let n = 4022510731; !ced || !libre(ced); n++) ced = dvCedula(String(n));
  return { name: 'María Fernández', tin: ced, documentType: 'CEDULA', partnerType: ['CUSTOMER'],
    customerType: 'REGULAR', partnerCategory: 'PERSON', ncfType: 2 };
});

// Línea de crédito de la Constructora (RD$150,000 a 30 días): solicitud + aprobación (Ventas › Crédito)
if (!uno(`SELECT id FROM credit_lines WHERE company_id=${EMPRESA} AND partnerId=${pena} AND deleted_at IS NULL AND status='ACTIVE' LIMIT 1`)) {
  let sol = uno(`SELECT id FROM credit_requests WHERE company_id=${EMPRESA} AND partnerId=${pena} AND status IN ('PENDING','IN_REVIEW') AND deleted_at IS NULL LIMIT 1`);
  if (!sol) {
    const r = await api(ADMIN, 'POST', 'v1/credit-requests', { partner: pena, requestedCreditLimit: '150000.00', requestedPaymentTermDays: 30, paymentTerm: '30 días' });
    sol = r.id; log('solicitud de crédito', sol);
  }
  // la política de la empresa exige analizarla antes de aprobar («En revisión»)
  if (uno(`SELECT status FROM credit_requests WHERE id=${sol}`) === 'PENDING') await api(ADMIN, 'PATCH', `v1/credit-requests/${sol}/evaluate`);
  const ap = await api(ADMIN, 'PATCH', `v1/credit-requests/${sol}/approve`, { approvedCreditLimit: '150000.00', approvedPaymentTermDays: 30, expirationDate: '2027-12-31' });
  log('solicitud aprobada', ap.status, JSON.stringify(ap.approvalProgress ?? ''));
}

// ── 6. Descuentos globales del ticket (formulario de descuento: alcance «Toda la factura», sin
//       aprobación, sin aplicación automática → el cajero los elige en el ticket)
for (const d of [
  { name: 'Descuento de mostrador 5 %', pct: 5, category: 'PROMOTIONAL', priority: 10, description: 'Rebaja que el cajero puede dar en mostrador' },
  { name: 'Cliente frecuente 10 %', pct: 10, category: 'LOYALTY', priority: 20, description: 'Para clientes que compran todas las semanas' },
]) {
  if (uno(`SELECT id FROM discounts WHERE company_id=${EMPRESA} AND name='${esc(d.name)}' AND deleted_at IS NULL LIMIT 1`)) continue;
  const r = await api(ADMIN, 'POST', 'v1/discounts', {
    scope: 'INVOICE', name: d.name, description: d.description, category: d.category, active: true, priority: d.priority,
    valueType: 'PERCENTAGE', percentageValue: d.pct, rules: { restrictions: { applyToAllProducts: true } },
  });
  log('descuento', d.name, r.id);
}

// ── 7. Configuración de caja: exigir turno abierto para vender (Configuración › Caja y pagos)
if (uno(`SELECT require_cashier_session_for_sale FROM company_configs WHERE company_id=${EMPRESA}`) !== '1') {
  await api(ADMIN, 'POST', 'v1/company/config/upsert', { requireCashierSessionForSale: true });
  log('require_cashier_session_for_sale → 1');
}

// ── 8. Rol complementario de la cajera (ver README: hallazgo del rol Cajero)
const EXTRA = ['MEDIA_VIEW', 'COMPANY_VIEW', 'INVOICE_RETURN_CREATE', 'INVOICE_RETURN_VIEW'];
let rol = uno(`SELECT id FROM roles WHERE company_id=${EMPRESA} AND name='Cajero POS demo' AND deleted_at IS NULL LIMIT 1`);
if (!rol) {
  const r = await api(ADMIN, 'POST', 'role', { name: 'Cajero POS demo', description: 'Permisos que el punto de venta usa y el rol Cajero no trae (demo del video POS)' });
  rol = r.id; log('rol', rol);
}
const faltan = EXTRA.filter(c => !+uno(`SELECT COUNT(*) FROM role_permissions rp JOIN permission p ON p.id=rp.permission_id WHERE rp.role_id=${rol} AND p.code='${c}'`));
if (faltan.length) {
  const ids = sql(`SELECT id FROM permission WHERE code IN (${faltan.map(c => `'${c}'`).join(',')})`).map(([i]) => +i);
  await api(ADMIN, 'PATCH', `role/add-permission/${rol}`, { permissions: ids, scope: 'ALL' });
  log('permisos al rol', faltan.join(','));
}
const YOH = +uno(`SELECT id FROM users WHERE username='yohanna.peralta'`);
if (!+uno(`SELECT COUNT(*) FROM user_company_roles WHERE user_id=${YOH} AND company_id=${EMPRESA} AND role_id=${rol}`)) {
  await api(ADMIN, 'PATCH', `user/add-role/${YOH}`, { roles: [+rol] });
  log('rol asignado a yohanna');
}

// ── 9. Caja Principal: cerrada, sin conteo por denominaciones; política sin conteo a ciegas
const [caja] = sql(`SELECT isOpen, require_denomination_control, is_blocked FROM cashiers WHERE id=49 AND company_id=${EMPRESA}`);
const [ciega] = sql(`SELECT blind_count FROM cashier_config WHERE company_id=${EMPRESA}`);
log('Caja Principal isOpen/estricta/bloqueada =', caja.join('/'), '· blind_count =', ciega[0]);

fs.writeFileSync(path.join(AQUI, 'ids.json'), JSON.stringify({
  empresa: EMPRESA, categorias: tipos, productos: Object.fromEntries(catalogo.productos.map(p => [p.sku, p.id])),
  clientes: { constructora: pena, maria, consumidorFinal: +uno(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND isInternalPartner=1 AND partnerType='CUSTOMER' LIMIT 1`) },
  descuentos: Object.fromEntries(sql(`SELECT name, id FROM discounts WHERE company_id=${EMPRESA} AND deleted_at IS NULL`).map(([n, i]) => [n, +i])),
  rol: +rol, caja: 49, ubicacion: UBIC,
}, null, 2));
log('siembra POS completa → seeds/pos/ids.json');
