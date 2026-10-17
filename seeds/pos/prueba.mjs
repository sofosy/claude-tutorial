// node seeds/pos/prueba.mjs [--sin-restaurar]
// Prueba de punta a punta del punto de venta POR API, como la cajera (yohanna.peralta) y con los mismos
// payloads que el front (pos-shift → sessions/open; pos-checkout.service paySale / creditSale):
//   1. abre turno en Caja Principal (fondo 5,000 contado en 5 billetes de 1,000)
//   2. venta de contado a consumidor final (B02) con el descuento «mostrador 5 %» → debe quedar PAGADA con NCF
//   3. venta a crédito a Constructora Hermanos Peña (B01) → creada y luego EMITIDA, con NCF y CxC
// Verifica en la BD, y al final restaura P0 (--sin-restaurar lo evita) y comprueba que todo volvió.
// OJO: el login de yohanna revoca la sesión que tenga abierta en el navegador.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { api, sql, log, EMPRESA } from '../cajas/_lib.mjs';
import { AQUI } from './_estado.mjs';

const CAJERA = 'yohanna.peralta';
const uno = s => sql(s)[0]?.[0];
const ids = JSON.parse(fs.readFileSync(path.join(AQUI, 'ids.json'), 'utf8'));
const cat = JSON.parse(fs.readFileSync(path.join(AQUI, 'catalogo.json'), 'utf8')).productos;
const precioDe = pid => +uno(`SELECT id FROM prices WHERE product_id=${pid} AND deleted_at IS NULL AND active=1 ORDER BY priority, id LIMIT 1`);
const r2 = v => Math.round(v * 100) / 100;
let fallos = 0;
const chk = (ok, msg) => { if (!ok) fallos++; console.log(ok ? '  ✓' : '  ✗', msg); };
const antes = {
  invoices: uno(`SELECT COUNT(*) FROM invoices WHERE company_id=${EMPRESA}`),
  sesiones: uno(`SELECT COUNT(*) FROM cashier_sessions WHERE company_id=${EMPRESA}`),
  stock: sql(`SELECT p.code, IFNULL(SUM(i.quantity - i.reservedStock),0) FROM products p LEFT JOIN inventory i ON i.product_id=p.id AND i.deleted_at IS NULL
    WHERE p.company_id=${EMPRESA} AND p.code LIKE 'FER-%' GROUP BY p.code ORDER BY p.code`).map(r => r.join('=')).join(' '),
};

// ── 1. Turno
const [[B1000]] = sql(`SELECT id FROM cash_denominations WHERE company_id IS NULL AND currency='DOP' AND valueCount=1000 AND deleted_at IS NULL LIMIT 1`);
const ses = await api(CAJERA, 'POST', 'v1/cashiers/sessions/open', {
  cashier: ids.caja, initialCash: 5000, notes: 'Prueba del punto de venta', deviceCode: 'prueba-pos-api',
  denominations: [{ cashDenomination: +B1000, quantity: 5 }],
});
const sesion = ses.id ?? ses.session?.id;
chk(uno(`SELECT isOpen FROM cashier_sessions WHERE id=${sesion} AND company_id=${EMPRESA}`) === '1', `turno ${sesion} abierto en la BD`);

// ── 2. Contado, consumidor final, B02, descuento 5 %: Martillo ×2 (450) + Fertilizante exento ×1 (380)
const martillo = ids.productos['FER-1001'], fert = ids.productos['FER-6002'];
const neto = 450 * 2 + 380, desc = r2(neto * 0.05);
const total = r2((900 - 45) * 1.18 + (380 - 19)); // descuento prorrateado; ITBIS solo en el martillo
const contado = await api(CAJERA, 'POST', 'v1/invoices', {
  ncfType: 2, notes: undefined, discounts: [+ids.descuentos['Descuento de mostrador 5 %']],
  details: [{ product: martillo, quantity: 2, priceId: precioDe(martillo) }, { product: fert, quantity: 1, priceId: precioDe(fert) }],
  paymentType: 1,
  payment: { amount: total.toFixed(2), paymentMethodCode: 'CASH', amountReceived: '1500.00', cashierSession: sesion },
});
const [f1] = sql(`SELECT i.invoice_number, s.code, i.ncf, i.ncf_type_code, i.total, i.discount_amount, i.partner_id FROM invoices i JOIN invoice_status s ON s.id=i.invoice_status_id WHERE i.id=${contado.id}`);
console.log('  contado:', f1.join(' | '));
chk(f1[1] === 'PAID', 'venta de contado PAGADA');
chk(/^B02\d{8}$/.test(f1[2]), `NCF B02 asignado (${f1[2]})`);
chk(Math.abs(+f1[4] - total) < 0.005 && Math.abs(+f1[5] - desc) < 0.005, `total ${f1[4]} = ${total.toFixed(2)} y descuento ${f1[5]} = ${desc.toFixed(2)}`);
const [pg] = sql(`SELECT p.payment_number, p.totalAmountPaid, pd.amountReceived, pd.amountChange, p.cashier_session_id FROM payments p
  JOIN payment_details pd ON pd.payment_id=p.id WHERE p.invoice_id=${contado.id} AND p.company_id=${EMPRESA} LIMIT 1`).concat([[]]);
console.log('  cobro (número | pagado | recibido | cambio | turno):', (pg ?? []).join(' | '));
chk(+pg?.[3] === r2(1500 - total) && +pg?.[4] === sesion, `cambio ${pg?.[3]} = ${(1500 - total).toFixed(2)} y cobro en el turno ${sesion}`);
chk(+uno(`SELECT IFNULL(SUM(quantity - reservedStock),0) FROM inventory WHERE product_id=${martillo} AND deleted_at IS NULL`) === 36, 'existencia del martillo 38 → 36');

// ── 3. Crédito, Constructora Hermanos Peña, B01: Cemento ×10 (540) + Varilla ×20 (310)
const cem = ids.productos['FER-5001'], vari = ids.productos['FER-5002'];
const vence = new Date(Date.now() + 30 * 86400000 - 4 * 3600000).toISOString().slice(0, 10);
const credito = await api(CAJERA, 'POST', 'v1/invoices', {
  ncfType: 1, partner: ids.clientes.constructora,
  details: [{ product: cem, quantity: 10, priceId: precioDe(cem) }, { product: vari, quantity: 20, priceId: precioDe(vari) }],
  paymentType: 2, paymentDueDate: vence, terms: '30 días',
});
await api(CAJERA, 'PATCH', `v1/invoices/change-status/${credito.invoiceNumber}`, { invoiceStatusCode: 'EMITTED' });
const [f2] = sql(`SELECT i.invoice_number, s.code, i.ncf, i.total, i.payment_due_date, i.partner_id FROM invoices i JOIN invoice_status s ON s.id=i.invoice_status_id WHERE i.id=${credito.id}`);
console.log('  crédito:', f2.join(' | '));
chk(f2[1] === 'EMITTED', 'venta a crédito EMITIDA');
chk(/^B01\d{8}$/.test(f2[2]), `NCF B01 asignado (${f2[2]})`);
chk(Math.abs(+f2[3] - 13688) < 0.005, `total ${f2[3]} = 13688.00`);
const [cxc] = sql(`SELECT documentNumber, outstandingAmount, dueDate FROM accounts_receivable WHERE invoice_id=${credito.id} AND company_id=${EMPRESA}`).concat([[]]);
chk(!!cxc?.[0], `cuenta por cobrar creada (${(cxc ?? []).join(' · ')})`);
console.log('  línea de crédito:', sql(`SELECT creditLimit, usedCredit, availableCredit FROM credit_lines WHERE partnerId=${ids.clientes.constructora} AND company_id=${EMPRESA}`)[0].join(' / '));

// ── Restaurar P0 y comprobar
if (!process.argv.includes('--sin-restaurar')) {
  execFileSync('node', [path.join(AQUI, 'restaurar.mjs'), 'P0'], { stdio: 'inherit' });
  const despues = {
    invoices: uno(`SELECT COUNT(*) FROM invoices WHERE company_id=${EMPRESA}`),
    sesiones: uno(`SELECT COUNT(*) FROM cashier_sessions WHERE company_id=${EMPRESA}`),
    stock: sql(`SELECT p.code, IFNULL(SUM(i.quantity - i.reservedStock),0) FROM products p LEFT JOIN inventory i ON i.product_id=p.id AND i.deleted_at IS NULL
      WHERE p.company_id=${EMPRESA} AND p.code LIKE 'FER-%' GROUP BY p.code ORDER BY p.code`).map(r => r.join('=')).join(' '),
  };
  chk(JSON.stringify(antes) === JSON.stringify(despues), `P0 restaurado: facturas ${despues.invoices}, sesiones ${despues.sesiones}, existencias iguales al canon`);
  chk(uno(`SELECT isOpen FROM cashiers WHERE id=${ids.caja}`) === '0', 'Caja Principal cerrada otra vez');
}
log(fallos ? `✗ ${fallos} fallo(s)` : '✓ prueba del POS completa');
process.exit(fallos ? 1 : 0);
