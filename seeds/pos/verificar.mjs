// node seeds/pos/verificar.mjs [--cajera]
// Verifica, con el usuario que graba (yohanna.peralta; OJO: su login revoca la sesión abierta en el
// navegador) o con admin.progreso por defecto, lo que el punto de venta lee del API:
//   catálogo (misma consulta y mismo cálculo que pos-catalog.service.ts toItem()), descuentos del ticket
//   (evaluate-for-invoice con el consumidor final), comprobantes B01/B02 del form-bootstrap y permisos.
// Solo LEE (el evaluate no escribe). Sale con código 1 si algo no cuadra.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { api, sql, log, EMPRESA, API, login } from '../cajas/_lib.mjs';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const USUARIO = process.argv.includes('--cajera') ? 'yohanna.peralta' : 'admin.progreso';
const catalogo = JSON.parse(fs.readFileSync(path.join(AQUI, 'catalogo.json'), 'utf8'));
const r2 = v => Math.round(v * 100) / 100;
let fallos = 0;
const mal = (...a) => { fallos++; console.log('  ✗', ...a); };

// ── Catálogo, igual que PosCatalogService.load() + toItem()
const res = await api(USUARIO, 'GET', 'v1/product?active=true&flattenVariants=true&limit=500&orderBy=name&orderDirection=ASC');
const filas = res.data ?? res;
const porCodigo = new Map(filas.map(f => [f.code, f]));
for (const p of catalogo.productos) {
  const f = porCodigo.get(p.sku);
  if (!f) { mal(p.sku, 'no sale en el catálogo del POS'); continue; }
  const rate = Number(f.tax?.percentage ?? 0);
  const precio = (f.prices ?? []).filter(x => x.active && !x.currency)
    .sort((a, b) => (Number(b.customerType === 'REGULAR') - Number(a.customerType === 'REGULAR')) || ((a.priority ?? 99) - (b.priority ?? 99)))[0];
  const display = f.selectedVariant?.price != null
    ? r2(Number(f.selectedVariant.price) * (1 + rate / 100)) : precio ? r2(Number(precio.price) * (1 + rate / 100)) : 0;
  const disp = (!f.managesInventory || f.hasInfiniteStock) ? null
    : f.selectedVariant?.stock ? Number(f.selectedVariant.stock.available ?? 0) : Number(f.totalAvailable ?? 0);
  const esperado = r2(p.precio * (p.exento ? 1 : 1.18));
  const img = f.selectedVariant?.media?.id ?? f.primaryImage?.id ?? null;
  const etiqueta = disp === null ? '—' : disp === 0 ? 'Agotado' : disp < 5 ? `Quedan ${disp}` : `${disp} en existencia`;
  const ok = display === esperado && disp === p.stock && f.productType?.name === p.categoria && rate === (p.exento ? 0 : 18);
  if (!ok) mal(p.sku, { display, esperado, disp, stock: p.stock, cat: f.productType?.name, rate, currency: precio?.currency });
  else console.log(`  ✓ ${p.sku} ${p.nombre.padEnd(34)} RD$${display.toFixed(2).padStart(9)}  ${etiqueta.padEnd(16)} img=${img ?? '—'}`);
}
console.log(`catálogo (${USUARIO}): ${filas.length} filas, total=${res.total}`);

// ── Descuentos del ticket: el POS evalúa con el cliente interno «consumidor final»
let interno = null;
try { interno = await api(USUARIO, 'GET', `v1/company/${EMPRESA}/internal-partner`); } catch (e) { mal('internal-partner:', e.message.slice(0, 160)); }
const partner = interno?.id ?? +sql(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND isInternalPartner=1 AND partnerType='CUSTOMER' LIMIT 1`)[0][0];
const p1 = filas.find(f => f.code === 'FER-1001');
const ev = await api(USUARIO, 'POST', 'v1/discounts/evaluate-for-invoice', {
  partner, details: [{ product: p1.id, quantity: 2, priceId: p1.prices?.[0]?.id, unitPrice: Number(p1.prices?.[0]?.price), productCost: 0 }],
});
const lista = (ev.discounts || ev.applicableDiscounts || []).filter(d => (d.scope ?? d.discount?.scope) === 'INVOICE' && !d.requiresApproval);
console.log(`descuentos del ticket (consumidor final ${partner}):`, lista.map(d => `${d.name ?? d.discount?.name} [${d.id ?? d.discountId ?? d.discount?.id}]`).join(' · ') || 'NINGUNO');
if (lista.length < 2) mal('se esperaban los 2 descuentos globales');

// ── Comprobantes y tipos de pago (form-bootstrap)
const boot = await api(USUARIO, 'GET', 'v1/invoices/form-bootstrap');
const ncf = (boot.ncfTypes ?? []).map(t => t.name);
console.log('ncfTypes:', ncf.join(','), '· paymentTypes:', (boot.paymentTypes ?? []).map(t => `${t.code}:${t.description}`).join(', '));
for (const c of ['B01', 'B02']) if (!ncf.includes(c)) mal('falta', c, 'en form-bootstrap');

// ── Permisos efectivos de quien graba (del login)
if (USUARIO === 'yohanna.peralta') {
  const r = await fetch(`${API}/auth/dev/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: USUARIO, password: 'Demo2026!' }) });
  const perms = (await r.json()).session.permissionCodes;
  const pide = ['INVOICE_CREATE', 'INVOICE_VIEW', 'INVOICE_CHANGE_STATUS', 'CASHIER_SESSION_VIEW', 'CASHIER_SESSION_CREATE', 'CASH_MOVEMENT_CREATE',
    'CASHIER_RECONCILIATION_CREATE', 'PRODUCT_VIEW', 'MEDIA_VIEW', 'COMPANY_VIEW', 'COMPANY_CONFIG_VIEW', 'PARTNER_VIEW', 'DISCOUNT_VIEW',
    'INVOICE_RETURN_CREATE', 'CASH_DENOMINATION_VIEW', 'PAYMENT_CREATE'];
  const faltan = pide.filter(c => !perms.includes(c));
  console.log(`permisos de ${USUARIO}: ${perms.length} · faltan: ${faltan.join(',') || 'ninguno'}`);
  if (faltan.length) mal('faltan permisos', faltan.join(','));
}
log(fallos ? `✗ ${fallos} fallo(s)` : '✓ todo cuadra');
process.exit(fallos ? 1 : 0);
