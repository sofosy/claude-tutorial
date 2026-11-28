// node seeds/clinica/citas.mjs <A|B|C>
// Deja «Centro Médico Los Prados» en el estado que pide cada video de «Citas y turnos».
//   A  Luis Gómez sin precio, sin horario, sin bloqueos; sin «Consultorio Pediátrico» (video 1).
//   B  A + lo que deja el video 1 (Luis: RD$2,000, L-V 8-12 en Consultorio Pediátrico), sin citas (video 2).
//   C  B + agenda llena: citas de hoy en varios estados y de los próximos días, una reserva sin ficha (videos 3-5).
import { sql, uno, api, login, log, fecha, empresa } from './_lib.mjs';

const estado = (process.argv[2] || 'A').toUpperCase();
const E = empresa();
const id = (n, a) => +uno(`SELECT id FROM partners WHERE company_id=${E} AND name='${n}' AND firstLastName='${a}' AND deleted_at IS NULL ORDER BY id LIMIT 1`);
const LUIS = id('Luis', 'Gómez');
await login();

// ── Limpieza común: agenda de la empresa ──────────────────────────────────────────────────────────
const borrarCitas = `
DELETE FROM patient_tickets WHERE company_id=${E};
DELETE FROM appointment_reminders WHERE appointment_id IN (SELECT id FROM appointments WHERE company_id=${E});
DELETE FROM bookings WHERE booking_page_id IN (SELECT id FROM booking_pages WHERE company_id=${E});
DELETE FROM appointments WHERE company_id=${E};
DELETE FROM schedule_events WHERE company_id=${E} AND title LIKE 'Reserva:%';
-- Cuenta del portal de Gabriela (la crea su reserva en línea del video 2): sin ella, la reserva vuelve a pedir el código.
DELETE FROM patient_portal_sessions WHERE account_id IN (SELECT id FROM patient_portal_accounts WHERE company_id=${E} AND email LIKE 'gabriela.%');
DELETE FROM patient_portal_result_reads WHERE account_id IN (SELECT id FROM patient_portal_accounts WHERE company_id=${E} AND email LIKE 'gabriela.%');
DELETE FROM patient_portal_access WHERE account_id IN (SELECT id FROM patient_portal_accounts WHERE company_id=${E} AND email LIKE 'gabriela.%');
DELETE FROM patient_portal_accounts WHERE company_id=${E} AND email LIKE 'gabriela.%';`;
sql(borrarCitas + `
DELETE FROM schedule_exceptions WHERE company_id=${E};
DELETE FROM staff_schedules WHERE staff_id=${LUIS};
UPDATE appointment_types_catalog SET base_price=NULL, requires_authorization=0 WHERE company_id=${E} AND code='CONSULTA-STAFF-${LUIS}';
DELETE FROM consultorios WHERE company_id=${E} AND code NOT IN ('CONS-01','CONS-02','CONS-03');
DELETE FROM company_notifications WHERE company_id=${E};`);
log('estado A listo');
if (estado === 'A') process.exit(0);

// ── B: lo que deja el video 1 ─────────────────────────────────────────────────────────────────────
let ped = uno(`SELECT id FROM consultorios WHERE company_id=${E} AND code='CONS-PED' AND deleted_at IS NULL`);
if (!ped) ped = (await api('POST', 'v1/consultorio', { code: 'CONS-PED', name: 'Consultorio Pediátrico', active: true })).id;
await api('PUT', `v1/booking-pages/staff/${LUIS}/consultation`, { price: 2000, requiresAuthorization: false, allowOnlineBooking: true });
for (const dia of ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']) {
  await api('POST', 'v1/staff-schedule', {
    staffId: LUIS, consultorioId: +ped, dayOfWeek: dia, startTime: '08:00', endTime: '12:00', slotDurationMinutes: 30,
    maxClientsPerSlot: 1, specialtyIds: [4], effectiveFrom: '2026-01-01', allowOnlineBooking: true, allowSameDayBooking: true,
  });
}
log('estado B listo');
if (estado === 'B') process.exit(0);

// ── C: agenda con citas ──────────────────────────────────────────────────────────────────────────
// Hora local de Santo Domingo → ISO UTC.
const iso = (dia, hhmm) => new Date(`${dia}T${hhmm}:00-04:00`).toISOString();
const sumar = (hhmm, min) => { const [h, m] = hhmm.split(':').map(Number); const t = h * 60 + m + min; return `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`; };
const MED = { ana: id('Ana', 'Pérez'), jorge: id('Jorge', 'Medina'), marta: id('Marta', 'Reyes'), pablo: id('Pablo', 'Santos'), elias: id('Elías', 'Tavárez') };
const DUR = { ana: 30, jorge: 30, marta: 30, pablo: 30, elias: 20 };
async function cita(paciente, medico, dias, hora, motivo, extra = {}) {
  const [n, a] = paciente.split('|');
  const dia = fecha(dias);
  return api('POST', 'v1/appointment', {
    patientId: id(n, a), staffId: MED[medico], scheduledStartTime: iso(dia, hora),
    scheduledEndTime: iso(dia, sumar(hora, DUR[medico])), durationMinutes: DUR[medico], reasonForVisit: motivo,
    priority: 'NORMAL', source: 'PHONE', ...extra,
  });
}
// Próximo día laborable (lunes a sábado) desde hoy + n.
const habil = n => { let d = n; for (;;) { const w = new Date(`${fecha(d)}T12:00:00-04:00`).getUTCDay(); if (w !== 0) return d; d++; } };
const hoy = habil(0) === 0 ? 0 : null;
const D1 = habil(1), D2 = habil(D1 + 1);
const citas = [
  ['Rosa Elena|Martínez', 'ana', D1, '08:00', 'Chequeo general'],
  ['Juan Carlos|Batista', 'ana', D1, '08:30', 'Dolor de cabeza', { isConfirmed: true, confirmationMethod: 'PHONE' }],
  ['Carolina|Méndez', 'marta', D1, '09:00', 'Control ginecológico'],
  ['Miguel Ángel|Rosario', 'pablo', D1, '14:00', 'Dolor en el pecho'],
  ['Paola|Jiménez', 'elias', D1, '08:20', 'Manchas en la piel'],
  ['Rafael Antonio|Núñez', 'ana', D2, '10:30', 'Tos persistente'],
  ['Francisco Javier|Cabrera', 'jorge', D2, '15:00', 'Control de presión'],
  ['Héctor Manuel|Vargas', 'jorge', D2, '16:00', 'Resultados de laboratorio'],
  ['Altagracia|Peralta', 'marta', D2, '10:00', 'Control ginecológico'],
];
if (hoy === 0) {
  citas.push(
    ['Yesenia|Castillo', 'ana', 0, '11:00', 'Fiebre'],
    ['Daniel Alberto|Polanco', 'ana', 0, '11:30', 'Chequeo general', { isConfirmed: true, confirmationMethod: 'PHONE' }],
    ['Mariela|Guzmán', 'jorge', 0, '16:30', 'Dolor abdominal'],
  );
}
for (const c of citas) await cita(...c);
log('estado C listo:', citas.length, 'citas');
