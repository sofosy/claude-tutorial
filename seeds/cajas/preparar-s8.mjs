// node seeds/cajas/preparar-s8.mjs [--sin-sesion]
// Estado S8 del video 8 «Cobrar una factura en la caja: pago combinado» (autor video 8, 2026-09-23).
//   S8 = S1 + plan 15 + factura de CONTADO en BORRADOR (Constructora Los Pinos, RD$8,850.00 con ITBIS)
//        + sesión de admin.progreso abierta en Caja Principal con fondo 5,000 (graba el ADMIN: la cajera no
//        tiene Ventas en su menú y al abrir la factura le sale «Acceso Denegado», ver _HALLAZGOS H-16/H-17).
// Datos MAESTROS que se crean una sola vez y NO se restauran (no salen en ninguna pantalla de Cajas):
//   cliente «Constructora Los Pinos» (partners). La secuencia B01 ya viene con la empresa (secuentials,
//   solo-update en _estado.mjs: S8 guarda su contador).
// Productos y precios SÍ van en _estado.mjs (en S0…S6 la empresa 43 no tiene ninguno).
// Todo por API (flujo real): admin.progreso crea la factura en borrador y abre su caja.
import { execFileSync } from 'node:child_process';
import { api, AQUI, sql, log, EMPRESA } from './_lib.mjs';

const node = (...a) => execFileSync('node', a, { cwd: AQUI, stdio: 'inherit' });
const ADMIN = 'admin.progreso';
const uno = s => sql(s)[0]?.[0];

node('restaurar.mjs', 'S1');
node('plan-s8.mjs', 'on');   // sin SALES_CREDIT abrir la factura lanza «Módulo No Disponible» (H-17)

// ── 1. Secuencia de comprobantes B01 (crédito fiscal) — maestro de la empresa
if (!uno(`SELECT id FROM secuentials WHERE company_id=${EMPRESA} AND ncf_type_id=1 AND deleted_at IS NULL LIMIT 1`)) {
  await api(ADMIN, 'POST', 'v1/ncf/secuential', { secuentialFrom: '00000001', secuentialTo: '00000500', dateExpire: '2027-12-31', ncfType: 1 });
  log('secuencia B01 creada');
}
// S1 no guarda el contador de los rangos (secuentials es 'solo-update' y S1 no lo volcó): si ya no queda
// ningún B01 emitido, el rango vuelve a empezar para que la factura salga siempre con B0100000001.
sql(`UPDATE secuentials SET totalCodesUsed=0, totalCodesAvailable=totalCodes WHERE company_id=${EMPRESA} AND ncf_type_id=1
  AND NOT EXISTS (SELECT 1 FROM ncf WHERE company_id=${EMPRESA} AND ncf_type_id=1)`);

// ── 2. Cliente (maestro, persiste)
// RNC ficticio del rango demo 1305550… con dígito verificador DGII válido
const rnc = (b8 => { const w = [7, 9, 8, 6, 5, 4, 3, 2]; const r = [...b8].reduce((a, d, i) => a + d * w[i], 0) % 11; return b8 + (r === 0 ? 2 : r === 1 ? 1 : 11 - r); })('13055507');
let cliente = uno(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND name='Constructora Los Pinos' AND deleted_at IS NULL LIMIT 1`);
if (!cliente) {
  const p = await api(ADMIN, 'POST', 'v1/partner', {
    name: 'Constructora Los Pinos', legalName: 'Constructora Los Pinos SRL', tin: rnc, documentType: 'RNC',
    partnerType: ['CUSTOMER'], customerType: 'REGULAR', partnerCategory: 'BUSINESS',
  });
  cliente = p.id ?? p?.data?.id;
  log('cliente creado', cliente, rnc);
}

// ── 3. Productos con precio (se restauran por _estado.mjs)
const productos = [
  { name: 'Cemento gris Portland 42.5 kg', code: 'CEM-425', precio: 450, cantidad: 10 },
  { name: 'Varilla corrugada 3/8" x 20 pies', code: 'VAR-038', precio: 150, cantidad: 20 },
];
for (const pr of productos) {
  pr.id = uno(`SELECT id FROM products WHERE company_id=${EMPRESA} AND code='${pr.code}' AND deleted_at IS NULL LIMIT 1`);
  if (!pr.id) {
    const r = await api(ADMIN, 'POST', 'v1/product', {
      category: 'PRODUCT', name: pr.name, code: pr.code, description: pr.name, tax: 1, managesInventory: false,
      usesBatchControl: false, purchasePrice: Math.round(pr.precio * 0.7),
    });
    pr.id = r.id ?? r?.data?.id;
    await api(ADMIN, 'POST', 'v1/price', { product: pr.id, customerType: 'REGULAR', price: String(pr.precio), priority: 1, taxIncluded: false });
    log('producto', pr.code, pr.id);
  }
}

// ── 4. Factura de CONTADO en BORRADOR (B01), preparada por ventas: la caja la abre con «Editar» y la
// cobra con «Guardar y Cobrar»; el NCF se le asigna al cobrar (payment.service.ts: DRAFT = «emite NCF al
// cobrar»). Una factura EMITIDA no sirve para el video: su única acción en el listado, «Ver Detalles», abre
// la vista de solo lectura sin panel de cobro (H-20), y «Cobros › Registrar cobro» dice «Pago directo (sin
// caja)» aunque el cobro entra a la caja abierta (H-21).
const f = await api(ADMIN, 'POST', 'v1/invoices', {
  partner: +cliente, rnc, legalName: 'Constructora Los Pinos SRL', paymentType: 1, ncfType: 1,
  incomeType: 1, notes: 'Materiales para la obra de Los Pinos',
  details: productos.map(p => ({ product: +p.id, quantity: p.cantidad,
    priceId: +uno(`SELECT id FROM prices WHERE product_id=${p.id} AND deleted_at IS NULL ORDER BY id LIMIT 1`) })),
});
const numero = f.invoiceNumber ?? f?.data?.invoiceNumber;
log('factura en borrador', numero, f.total ?? f?.data?.total, f?.invoiceStatus?.code ?? '');

// ── 5. Sesión de quien cobra (admin.progreso) en Caja Principal (fondo 5,000)
if (!process.argv.includes('--sin-sesion')) {
  await api(ADMIN, 'POST', 'v1/cashiers/sessions/open', { cashier: 49, initialCash: 5000, notes: 'Turno de la mañana' });
  log('sesión de admin.progreso abierta en Caja Principal');
}
log(`S8 preparado (factura ${numero}). Fijar con: node fijar.mjs S8 y luego node plan-s8.mjs off`);
