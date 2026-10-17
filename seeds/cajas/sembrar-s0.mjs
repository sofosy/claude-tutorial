// Siembra el estado S0 de la serie de Cajas en la EMPRESA DEMO (43, «Ferretería El Progreso»).
// Operaciones de negocio por API con el usuario que las haría en la vida real (asientos, auditoría,
// numeración y alertas reales). SQL solo para retroceder fechas de filas de la empresa 43.
// Se corre UNA vez sobre la empresa recién creada (ver README). Después: `node fijar.mjs S0`.
import { api, sql, idDe, log, EMPRESA, CUENTA_INGRESOS, CUENTA_GASTOS, EFECTIVO } from './_lib.mjs';

const ya = sql(`SELECT COUNT(*) FROM cashier_sessions WHERE company_id=${EMPRESA}`)[0][0];
if (+ya > 0 && !process.argv.includes('--forzar')) {
  console.error(`La empresa ${EMPRESA} ya tiene ${ya} sesiones: S0 ya sembrado. Usa restaurar.mjs S0.`);
  process.exit(1);
}

// ── 1. Política de cajas (misma que la empresa 29 del plan original) ──────────────────────────
await api('admin.progreso', 'POST', 'v1/cashier-config', {
  defaultInitialCash: 5000, toleranceAmount: 50, tolerancePercentage: 1, toleranceMode: 'AMOUNT',
  maxConsecutiveDifferences: 3, maxSessionDurationMinutes: 720,
  maxWithdrawalWithoutApproval: 5000, maxDepositWithoutApproval: 10000,
  requireNotesForWithdrawal: true, requireReconciliationForClose: true, blindCount: false,
  requireJustificationForDifference: true, reconciliationConfirmationHours: 24,
  allowOperationOnHolidays: false,
});
log('cashier_config OK');

// ── 2. Cajas ───────────────────────────────────────────────────────────────────────────────────
async function caja(code, name, location, extra = {}) {
  const hay = sql(`SELECT id FROM cashiers WHERE company_id=${EMPRESA} AND code='${code}' AND deleted_at IS NULL`);
  if (hay.length) return +hay[0][0];
  const c = await api('admin.progreso', 'POST', 'v1/cashiers', {
    code, name, location, acceptCash: true, acceptCard: true, acceptTransfer: false, ...extra,
  });
  return idDe(c);
}
const PRINCIPAL = await caja('CAJA-01', 'Caja Principal', 'Mostrador de entrada — frente a la puerta', { acceptTransfer: true });
const MOSTRADOR2 = await caja('CAJA-02', 'Caja Mostrador 2', 'Área de pinturas y herramientas');
const SANTIAGO = await caja('CAJA-SAN', 'Caja Sucursal Santiago', 'Sucursal Santiago — Av. Estrella Sadhalá');
log('cajas', { PRINCIPAL, MOSTRADOR2, SANTIAGO });

// ── 3. Historia de días previos: turno → movimientos → conteo del cajero → cuadre de carmen ─────
async function turno({ cajero, cashier, fondo = 5000, movs = [], contado, justif, nota }) {
  const s = await api(cajero, 'POST', 'v1/cashiers/sessions/open', { cashier, initialCash: fondo, notes: nota });
  const sesion = idDe(s);
  const ids = [];
  for (const m of movs) {
    const mv = await api(cajero, 'POST', 'v1/cashiers/movements', {
      cashierSession: sesion, type: m.tipo, amount: m.monto, notes: m.nota,
      counterpartAccount: m.tipo === 'IN' ? CUENTA_INGRESOS : CUENTA_GASTOS,
      ...(m.itbis ? { taxAmount: m.itbis } : {}),
    });
    ids.push(idDe(mv));
  }
  if (contado === undefined) return { sesion, movs: ids };
  const rec = await api(cajero, 'POST', 'v1/cashier-reconciliation', {
    cashierSession: sesion, reconciliationType: 'CLOSING',
    details: [{ paymentMethod: EFECTIVO, actualAmount: String(contado), ...(justif ? { justification: justif } : {}) }],
  });
  const recId = idDe(rec);
  await api('carmen.rosario', 'PATCH', `v1/cashier-reconciliation/${recId}/confirm`, { accepted: true });
  return { sesion, movs: ids, rec: recId };
}

const historia = [
  // [días atrás, turno]
  [3, { cajero: 'yohanna.peralta', cashier: PRINCIPAL, nota: 'Turno de la mañana',
        movs: [{ tipo: 'IN', monto: 1500, nota: 'Cambio en monedas traído del banco' }], contado: 6500 }],
  [3, { cajero: 'luis.batista', cashier: MOSTRADOR2, nota: 'Turno de la tarde',
        movs: [{ tipo: 'OUT', monto: 800, nota: 'Compra de fundas y material de empaque' }], contado: 4200 }],
  [2, { cajero: 'yohanna.peralta', cashier: PRINCIPAL, nota: 'Turno de la mañana',
        movs: [{ tipo: 'OUT', monto: 1180, itbis: 180, nota: 'Pago de fletes de mercancía a domicilio' }],
        contado: 3790, justif: 'Faltan 30 pesos: vuelto mal entregado a un cliente' }],
  [2, { cajero: 'luis.batista', cashier: MOSTRADOR2, nota: 'Turno de la tarde',
        movs: [{ tipo: 'IN', monto: 2500, nota: 'Reposición de cambio desde la oficina' }], contado: 7500 }],
  [1, { cajero: 'yohanna.peralta', cashier: PRINCIPAL, nota: 'Turno de la mañana',
        movs: [{ tipo: 'IN', monto: 3000, nota: 'Cambio para el fin de semana' },
               { tipo: 'OUT', monto: 650, nota: 'Compra de agua y café para clientes' }], contado: 7350 }],
  [1, { cajero: 'luis.batista', cashier: MOSTRADOR2, nota: 'Turno de la tarde', movs: [], contado: 5010,
        justif: 'Sobran 10 pesos en monedas' }],
];

const retro = [];
for (const [dias, t] of historia) {
  const r = await turno(t);
  retro.push({ dias, ...r, cajero: t.cajero });
  log(`D-${dias} ${t.cajero} sesión ${r.sesion} movs ${r.movs} cuadre ${r.rec}`);
}

// Retroceder fechas (SOLO filas de la empresa 43, por id). Hora base: 08:00 mañana / 14:00 tarde.
let s = '';
for (const r of retro) {
  const base = r.cajero === 'yohanna.peralta' ? '08:05:00' : '14:02:00';
  const d = `TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL ${r.dias} DAY), '${base}')`;
  const cierre = `DATE_ADD(${d}, INTERVAL 5 HOUR)`;
  s += `UPDATE cashier_sessions SET openedAt=${d}, created_at=${d}, closedAt=${cierre}, updated_at=${cierre} WHERE id=${r.sesion} AND company_id=${EMPRESA};\n`;
  r.movs.forEach((m, i) => {
    const t = `DATE_ADD(${d}, INTERVAL ${60 + i * 75} MINUTE)`;
    s += `UPDATE cash_movements SET created_at=${t}, updated_at=${t}, approved_at=IF(approved_at IS NULL,NULL,${t}) WHERE id=${m} AND company_id=${EMPRESA};\n`;
    s += `UPDATE journal_entries SET date=DATE(${t}), postingDate=IF(postingDate IS NULL,NULL,${t}), created_at=${t}, updated_at=${t} WHERE company_id=${EMPRESA} AND documentNumber=(SELECT movement_number FROM cash_movements WHERE id=${m});\n`;
  });
  const rc = `DATE_ADD(${d}, INTERVAL 290 MINUTE)`;
  const conf = `DATE_ADD(${d}, INTERVAL 320 MINUTE)`;
  s += `UPDATE cashier_reconciliations SET created_at=${rc}, count_started_at=IF(count_started_at IS NULL,NULL,${rc}), count_completed_at=IF(count_completed_at IS NULL,NULL,${rc}), cashier_signed_at=IF(cashier_signed_at IS NULL,NULL,${rc}), supervisor_signed_at=IF(supervisor_signed_at IS NULL,NULL,${conf}), updated_at=${conf} WHERE id=${r.rec} AND company_id=${EMPRESA};\n`;
  s += `UPDATE cashier_reconciliation_details SET created_at=${rc}, updated_at=${conf} WHERE company_id=${EMPRESA} AND reconciliation_id=${r.rec};\n`;
}
retroFechas(s);

function retroFechas(texto) {
  try { sql(texto); } catch (e) {
    // columnas de enlace distintas a las supuestas: se reintenta línea a línea y se informa
    for (const l of texto.split('\n').filter(Boolean)) {
      try { sql(l); } catch (e2) { console.error('retro-fecha omitida:', l.slice(0, 140), '\n  ', String(e2.message).split('\n')[0]); }
    }
  }
}
log('fechas retrocedidas');

// ── 4. Santiago: bloqueada por la supervisora ─────────────────────────────────────────────────
await api('carmen.rosario', 'POST', `v1/cashiers/${SANTIAGO}/block`, {
  reason: '[Auditoría pendiente] Faltante de efectivo en el último arqueo; pendiente de revisión con la gerencia',
});
// «Última actividad» de la tarjeta = cashiers.updated_at: se lleva al último hecho real de cada caja.
sql(`UPDATE cashiers SET blocked_at=TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL 1 DAY),'16:40:00'), updated_at=TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL 1 DAY),'16:40:00') WHERE id=${SANTIAGO} AND company_id=${EMPRESA};
UPDATE cashier_alerts SET created_at=TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL 1 DAY),'16:40:00'), updated_at=TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL 1 DAY),'16:40:00') WHERE cashier_id=${SANTIAGO} AND company_id=${EMPRESA};
UPDATE cashiers SET updated_at=(SELECT MAX(closedAt) FROM cashier_sessions WHERE cashier_id=${PRINCIPAL} AND company_id=${EMPRESA}) WHERE id=${PRINCIPAL} AND company_id=${EMPRESA};`);
log('Santiago bloqueada');

// ── 5. Hoy: luis.batista con Caja Mostrador 2 abierta desde hace 2 h ──────────────────────────
const hoy = await turno({
  cajero: 'luis.batista', cashier: MOSTRADOR2, nota: 'Turno de la mañana',
  movs: [{ tipo: 'IN', monto: 1500, nota: 'Cambio para la gaveta' },
         { tipo: 'OUT', monto: 450, itbis: 68.64, nota: 'Compra de agua y café para clientes' }],
});
// Zona: el API lee los timestamp como instantes de la sesión MySQL (UTC-5) y los entrega en RD
// (UTC-4); NOW() de MySQL es coherente con esa lectura (medido: literal 02:53 → API «03:53-04:00»).
sql(`SET @rd := NOW();
UPDATE cashier_sessions SET openedAt=DATE_SUB(@rd, INTERVAL 2 HOUR), created_at=DATE_SUB(@rd, INTERVAL 2 HOUR) WHERE id=${hoy.sesion} AND company_id=${EMPRESA};
UPDATE cash_movements SET created_at=DATE_SUB(@rd, INTERVAL 95 MINUTE), updated_at=DATE_SUB(@rd, INTERVAL 95 MINUTE) WHERE id=${hoy.movs[0]} AND company_id=${EMPRESA};
UPDATE cash_movements SET created_at=DATE_SUB(@rd, INTERVAL 40 MINUTE), updated_at=DATE_SUB(@rd, INTERVAL 40 MINUTE) WHERE id=${hoy.movs[1]} AND company_id=${EMPRESA};`);
log('Mostrador 2 abierta', hoy);
log('S0 sembrado. Siguiente: node fijar.mjs S0');
