// node seeds/cajas/preparar-api.mjs S3|S4|S5
// Arma por API los estados de partida S3…S5 a partir del canon anterior, con las MISMAS acciones,
// usuarios y textos que el recorrido por la UI de explorar.py v3…v5 (estados/S3…S5.sql originales).
// Sirve para rehacer la serie en una base nueva (alta-empresa.mjs → sembrar-s0.mjs) sin navegador.
//   S3 = S1 + yohanna abre Caja Principal (5,000), entrada 2,000 y salida 6,500 (ITBIS 991.53) por aprobar
//   S4 = S3 + carmen aprueba la salida y transfiere 3,000 de Mostrador 2 a Principal (recibida)
//   S5 = S4 + conteo de cierre de yohanna: 3,480 (−20, «Faltan 20 pesos en monedas»), sesión cerrada
// Después de cada uno: `node fijar.mjs S#`.
import { execFileSync } from 'node:child_process';
import { AQUI, EMPRESA, api, sql, idDe, log, CUENTA_INGRESOS, CUENTA_GASTOS, EFECTIVO } from './_lib.mjs';

const estado = process.argv[2];
const node = (...a) => execFileSync('node', a, { cwd: AQUI, stdio: 'inherit' });
const uno = q => sql(q)[0]?.[0];
const caja = code => +uno(`SELECT id FROM cashiers WHERE company_id=${EMPRESA} AND code='${code}' AND deleted_at IS NULL`);
const sesionAbierta = code => +uno(`SELECT id FROM cashier_sessions WHERE company_id=${EMPRESA} AND cashier_id=${caja(code)} AND isOpen=1 AND deleted_at IS NULL`);

const PREVIO = { S3: 'S1', S4: 'S3', S5: 'S4' }[estado];
if (!PREVIO) { console.error('uso: node preparar-api.mjs S3|S4|S5'); process.exit(2); }
node('restaurar.mjs', PREVIO);

if (estado === 'S3') {
  const s = await api('yohanna.peralta', 'POST', 'v1/cashiers/sessions/open', { cashier: caja('CAJA-01'), initialCash: 5000, notes: 'Turno de la mañana' });
  const sesion = idDe(s);
  await api('yohanna.peralta', 'POST', 'v1/cashiers/movements', {
    cashierSession: sesion, type: 'IN', amount: 2000, notes: 'Cambio en monedas traído del banco', counterpartAccount: CUENTA_INGRESOS,
  });
  await api('yohanna.peralta', 'POST', 'v1/cashiers/movements', {
    cashierSession: sesion, type: 'OUT', amount: 6500, taxAmount: 991.53,
    notes: 'Pago del mantenimiento del aire acondicionado', counterpartAccount: CUENTA_GASTOS,
  });
} else if (estado === 'S4') {
  const salida = uno(`SELECT id FROM cash_movements WHERE company_id=${EMPRESA} AND status='PENDING_APPROVAL' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
  await api('carmen.rosario', 'POST', `v1/cashiers/movements/${salida}/approve`, {});
  const t = await api('carmen.rosario', 'POST', 'v1/cash-transfers', { sourceCashier: caja('CAJA-02'), targetCashier: caja('CAJA-01'), amount: 3000 });
  await api('carmen.rosario', 'POST', `v1/cash-transfers/${idDe(t)}/receive`, {});
} else if (estado === 'S5') {
  await api('yohanna.peralta', 'POST', 'v1/cashier-reconciliation', {
    cashierSession: sesionAbierta('CAJA-01'), reconciliationType: 'CLOSING',
    details: [{ paymentMethod: EFECTIVO, actualAmount: '3480', justification: 'Faltan 20 pesos en monedas' }],
  });
}
log(`${estado} preparado. Fijar con: node fijar.mjs ${estado}`);
