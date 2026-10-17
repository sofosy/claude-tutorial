// node seeds/citas/restaurar.mjs [A|B|C]
// Deja la clínica demo (empresa 31 «Centro Médico Los Prados», RegiSalud) en el estado que pide cada video
// de la serie «Citas». No recarga la base entera: limpia la agenda de la empresa y la vuelve a armar por API,
// con fechas relativas a HOY (la grabación ve siempre «hoy» con citas).
//   A  servicios base (sin «Consulta pediátrica»), cinco médicos con su servicio y horario, Luis Gómez sin
//      configurar, modo de agenda SIMPLE, sin citas en octubre.
//   P  A + «Consulta pediátrica» creada (como termina la parte 1); Luis Gómez sin configurar.
//   B  A + «Consulta pediátrica» y Luis Gómez ofreciéndola (L-V 8-12, Consultorio Pediátrico): como termina
//      la parte 2. Sigue en SIMPLE.
//   C  B + modo AVANZADO (portal del centro) + agenda llena: citas de hoy en todos los estados y de los
//      próximos días, y una reserva hecha desde el portal.
import { sql, uno, api, login, log, EMPRESA, fecha, esc, API } from './_lib.mjs';
import { execFileSync } from 'node:child_process';

const estado = (process.argv[2] || 'A').toUpperCase();
const t0 = Date.now();
const E = EMPRESA;
const ADMIN_USER = 269;

// ── Catálogo fijo de la serie ─────────────────────────────────────────────────────────────────────
const MEDICOS = { ana: 321, luis: 322, marta: 332, pablo: 333, jorge: 334, elias: 335 };
const SERVICIOS = [
  // id fijo cuando reutiliza una fila existente
  { id: 1, code: 'CONSULTA-GENERAL', name: 'Consulta general', dur: 30, price: 1500, color: '#1E88E5', icon: 'medical_services',
    desc: 'Evaluación médica general para síntomas nuevos, chequeos y orientación.', type: 'FIRST_VISIT', order: 1 },
  { id: 2, code: 'CONTROL', name: 'Control de seguimiento', dur: 15, price: 800, color: '#43A047', icon: 'event_repeat',
    desc: 'Seguimiento breve de un paciente ya atendido: resultados, ajuste de tratamiento.', type: 'FOLLOW_UP', order: 2 },
  { code: 'CONSULTA-GINECOLOGICA', name: 'Consulta ginecológica', dur: 30, price: 2500, color: '#D81B60', icon: 'female',
    desc: 'Control ginecológico y obstétrico.', type: 'FIRST_VISIT', order: 3 },
  { code: 'EVALUACION-CARDIOLOGICA', name: 'Evaluación cardiológica', dur: 30, price: 3500, color: '#E53935', icon: 'monitor_heart',
    desc: 'Consulta con el cardiólogo; incluye la lectura del electrocardiograma.', type: 'EXAMINATION', order: 4 },
  { code: 'CONSULTA-DERMATOLOGICA', name: 'Consulta dermatológica', dur: 20, price: 2200, color: '#8E24AA', icon: 'face',
    desc: 'Evaluación de piel, cabello y uñas.', type: 'FIRST_VISIT', order: 5 },
  { id: 3, code: 'URGENCIA', name: 'Urgencia', dur: 20, price: 500, color: '#FB8C00', icon: 'emergency', online: 0,
    desc: 'Atención no programada. No se reserva por internet.', type: 'EMERGENCY', order: 9 },
];
const PEDIATRIA = { code: 'CONSULTA-PEDIATRICA', name: 'Consulta pediátrica', dur: 30, price: 2000, color: '#00ACC1', icon: 'child_care',
  desc: 'Control de niño sano y consulta de enfermedad para menores de 18 años.', type: 'FIRST_VISIT', order: 6 };

const L_S = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
const L_V = L_S.slice(0, 5);
// médico → servicios con su franja
const OFERTAS = [
  { medico: 'ana', code: 'CONSULTA-GENERAL', dias: L_S, ini: '08:00', fin: '12:00', turno: 30, cons: 'CONS-01' },
  { medico: 'ana', code: 'CONTROL', dias: L_S, ini: '14:00', fin: '16:00', turno: 15, cons: 'CONS-01' },
  { medico: 'jorge', code: 'CONSULTA-GENERAL', dias: L_S, ini: '14:00', fin: '18:00', turno: 30, cons: 'CONS-02' },
  { medico: 'jorge', code: 'CONTROL', dias: L_S, ini: '08:00', fin: '10:00', turno: 15, cons: 'CONS-02' },
  { medico: 'marta', code: 'CONSULTA-GINECOLOGICA', dias: L_S, ini: '10:00', fin: '13:00', turno: 30, cons: 'CONS-02' },
  { medico: 'pablo', code: 'EVALUACION-CARDIOLOGICA', dias: L_S, ini: '14:00', fin: '18:00', turno: 30, cons: 'CONS-03' },
  { medico: 'elias', code: 'CONSULTA-DERMATOLOGICA', dias: L_S, ini: '08:00', fin: '12:00', turno: 20, cons: 'CONS-03' },
];
const OFERTA_LUIS = { medico: 'luis', code: 'CONSULTA-PEDIATRICA', dias: L_V, ini: '08:00', fin: '12:00', turno: 30, cons: 'CONS-PED' };

// Pacientes de demo (cédulas inventadas, serie 402-0555…)
const PACIENTES = [
  ['Rosa Elena', 'Martínez', '402-0555001-1', 'F', '1985-04-12', '809-555-0111'],
  ['Juan Carlos', 'Batista', '402-0555002-2', 'M', '1978-09-03', '809-555-0122'],
  ['Carolina', 'Méndez', '402-0555003-3', 'F', '1992-01-25', '829-555-0133'],
  ['Miguel Ángel', 'Rosario', '402-0555004-4', 'M', '1969-11-30', '809-555-0144'],
  ['Paola', 'Jiménez', '402-0555005-5', 'F', '1995-06-18', '849-555-0155'],
  ['Rafael Antonio', 'Núñez', '402-0555006-6', 'M', '1958-02-07', '809-555-0166'],
  ['Yesenia', 'Castillo', '402-0555007-7', 'F', '1988-08-22', '829-555-0177'],
  ['Héctor Manuel', 'Vargas', '402-0555008-8', 'M', '1974-03-14', '809-555-0188'],
  ['Laura Patricia', 'Santana', '402-0555009-9', 'F', '1990-12-01', '809-555-0199'],
  ['Daniel Alberto', 'Polanco', '402-0555010-0', 'M', '1983-05-09', '849-555-0110'],
  ['Mariela', 'Guzmán', '402-0555011-1', 'F', '1999-10-16', '829-555-0121'],
  ['Francisco Javier', 'Cabrera', '402-0555012-2', 'M', '1965-07-27', '809-555-0132'],
  ['Altagracia', 'Peralta', '402-0555013-3', 'F', '1961-03-02', '809-555-0143'],
  ['Mateo', 'Batista', '402-0555014-4', 'M', '2019-02-11', '809-555-0122'],
  ['Valeria', 'Méndez', '402-0555015-5', 'F', '2021-09-05', '829-555-0133'],
];

// ── 1. Limpieza por SQL ───────────────────────────────────────────────────────────────────────────
const desde = fecha(-14);
sql(`
UPDATE subscriptions SET expirationDate='2027-12-31 23:00:00', nextBillingDate='2027-12-31 23:00:00', status='ACTIVE'
  WHERE company_id=${E};
UPDATE companies SET slug='los-prados' WHERE id=${E};
UPDATE company_configs SET agenda_mode='SIMPLE' WHERE company_id=${E};
UPDATE user_company_preferences SET incomplete_config_notice_seen_at=COALESCE(incomplete_config_notice_seen_at, NOW())
  WHERE company_id=${E};
-- Médicos: fuera la cuenta de QA y la administradora; Luis Gómez (Pediatría) activo.
UPDATE partners SET isMedicalStaff=0 WHERE company_id=${E} AND id IN (315, 342);
UPDATE partners SET active=1 WHERE id=${MEDICOS.luis};
-- Pacientes de QA fuera de la vista.
UPDATE partners SET deleted_at=NOW() WHERE company_id=${E} AND deleted_at IS NULL AND partnerType='PATIENT'
  AND (name LIKE 'QA %' OR name LIKE 'UI %' OR name LIKE '%QA%' OR name IN ('Ñandú','Regresion','Altagracia')
       OR firstLastName IN ('Test','Sindocumento','Opcional'));
-- Agenda de la empresa: reservas, citas recientes, enlaces, horarios y bloqueos.
-- Cola de la «Operación del Día»: los turnos que dejaron las tomas anteriores (la cita se borra, el turno no).
DELETE FROM patient_tickets WHERE company_id=${E};
-- Eventos de calendario que crea cada reserva en línea («Reserva: …»), visibles con «Eventos» encendido.
DELETE FROM schedule_events WHERE company_id=${E} AND title LIKE 'Reserva:%';
UPDATE partners SET deleted_at=NOW() WHERE company_id=${E} AND deleted_at IS NULL AND name LIKE 'Prueba Fuga%';
DELETE FROM bookings WHERE booking_page_id IN (SELECT id FROM booking_pages WHERE company_id=${E});
DELETE FROM bookings WHERE appointment_id IN (SELECT id FROM appointments WHERE company_id=${E} AND scheduled_date >= '${desde}');
DELETE FROM appointments WHERE company_id=${E} AND scheduled_date >= '${desde}';
DELETE FROM staff_schedules WHERE company_id=${E};
DELETE FROM booking_pages WHERE company_id=${E};
DELETE FROM schedule_exceptions WHERE company_id=${E};
-- Consultorios: el principal, el 2 y el 3; el pediátrico lo crea el video 2.
UPDATE consultorios SET name='Consultorio 1', deleted_at=NULL WHERE id=1;
UPDATE consultorios SET name='Consultorio 2', deleted_at=NULL WHERE id=3;
DELETE FROM consultorios WHERE company_id=${E} AND code NOT IN ('CONS-01','CONS-02','CONS-03');
`);
if (!uno(`SELECT id FROM consultorios WHERE company_id=${E} AND code='CONS-03'`)) {
  sql(`INSERT INTO consultorios (company_id, created_by_user_id, code, name, is_active, is_main_branch, active)
       VALUES (${E}, ${ADMIN_USER}, 'CONS-03', 'Consultorio 3', 1, 0, 1);`);
}

// Servicios: los de la serie quedan exactamente así; cualquier otro, borrado.
const codigos = SERVICIOS.map(s => `'${s.code}'`).join(',');
sql(`UPDATE appointment_types_catalog SET code=CONCAT('X', id, '-', code) WHERE company_id=${E} AND id NOT IN (1,2,3) AND code IN (${codigos});
     DELETE FROM appointment_types_catalog WHERE company_id=${E} AND id NOT IN (1,2,3) AND code NOT IN (${codigos});`);
function upsertServicio(s) {
  const campos = `code='${s.code}', name='${esc(s.name)}', description='${esc(s.desc)}', default_duration_minutes=${s.dur},
    color='${s.color}', icon='${s.icon}', requires_authorization=0, allow_online_booking=${s.online ?? 1}, allow_telemedicine=0,
    base_price=${s.price}, buffer_minutes=0, max_patients_per_slot=1, display_order=${s.order}, is_active=1, active=1,
    appointment_type='${s.type}', deleted_at=NULL`;
  const id = s.id ?? uno(`SELECT id FROM appointment_types_catalog WHERE company_id=${E} AND code='${s.code}'`);
  if (id) sql(`UPDATE appointment_types_catalog SET ${campos} WHERE id=${id};`);
  else sql(`INSERT INTO appointment_types_catalog SET company_id=${E}, created_by_user_id=${ADMIN_USER}, ${campos};`);
}
SERVICIOS.forEach(upsertServicio);
if (estado === 'A') sql(`DELETE FROM appointment_types_catalog WHERE company_id=${E} AND code='${PEDIATRIA.code}';`);
else upsertServicio(PEDIATRIA);

// Pacientes de demo
for (const [nombre, apellido, ced, g, nac, tel] of PACIENTES) {
  const id = uno(`SELECT id FROM partners WHERE company_id=${E} AND tin='${ced}' ORDER BY id LIMIT 1`);
  const campos = `name='${esc(nombre)}', firstLastName='${esc(apellido)}', gender='${g}', birthDate='${nac} 12:00:00',
    personal_mobile_phone='${tel}', isActivePatient=1, active=1, deleted_at=NULL, isMinor=${nac >= '2008' ? 1 : 0}`;
  if (id) sql(`UPDATE partners SET ${campos} WHERE id=${id};`);
  else sql(`INSERT INTO partners SET company_id=${E}, tin='${ced}', partnerType='PATIENT', partnerCategory='PERSON',
    document_type='CEDULA', created_by_user_id=${ADMIN_USER}, firstVisitDate='2026-03-02', ${campos};`);
}
// La reserva del video 3 la hace una paciente nueva: que no exista de una toma anterior.
sql(`UPDATE partners SET deleted_at=NOW() WHERE company_id=${E} AND deleted_at IS NULL AND
     (personal_email='gabriela.fernandez@correo.test' OR (name LIKE 'Gabriela%' AND firstLastName LIKE 'Fern%'));`);
try { execFileSync('docker', ['exec', 'germiva-redis', 'redis-cli', 'FLUSHALL'], { stdio: 'ignore' }); } catch { log('AVISO: no se pudo vaciar Redis'); }
log('limpieza SQL lista');

// ── 2. Servicios por médico y horarios (por API, como la ficha del médico) ──────────────────────────
await login();
const idServicio = code => +uno(`SELECT id FROM appointment_types_catalog WHERE company_id=${E} AND code='${code}' AND deleted_at IS NULL`);
const idConsultorio = code => +uno(`SELECT id FROM consultorios WHERE company_id=${E} AND code='${code}' AND deleted_at IS NULL`);
const paginas = {};
async function ofrecer(o) {
  const staffId = MEDICOS[o.medico];
  const page = await api('POST', `v1/booking-pages/staff/${staffId}`, { appointmentTypeId: idServicio(o.code) });
  paginas[`${o.medico}/${o.code}`] = page;
  for (const dia of o.dias) {
    await api('POST', 'v1/staff-schedule', {
      staffId, bookingPageId: page.id, dayOfWeek: dia, effectiveFrom: desde,
      startTime: o.ini, endTime: o.fin, slotDurationMinutes: o.turno, maxClientsPerSlot: 1,
      consultorioId: idConsultorio(o.cons), strictMode: false, allowOnlineBooking: true, allowSameDayBooking: true,
    });
  }
  log(`  ${o.medico} ofrece ${o.code} (${o.dias.length} días ${o.ini}-${o.fin}) → ${page.slug}`);
}
for (const o of OFERTAS) await ofrecer(o);
if (estado === 'B' || estado === 'C') {
  sql(`INSERT INTO consultorios (company_id, created_by_user_id, code, name, is_active, is_main_branch, active)
       VALUES (${E}, ${ADMIN_USER}, 'CONS-PED', 'Consultorio Pediátrico', 1, 0, 1);`);
  await ofrecer(OFERTA_LUIS);
}

// ── 3. Estado C: portal avanzado y agenda llena ────────────────────────────────────────────────────
if (estado === 'C') {
  sql(`UPDATE company_configs SET agenda_mode='ADVANCED' WHERE company_id=${E};`);
  const paciente = ced => +uno(`SELECT id FROM partners WHERE company_id=${E} AND tin='${ced}' AND deleted_at IS NULL ORDER BY id LIMIT 1`);
  const P = i => paciente(PACIENTES[i][2]);
  // Días hábiles: `dia` cuenta días de consulta (lunes a sábado) desde hoy; negativo hacia atrás.
  const diaSemana = f => new Date(`${f}T12:00:00Z`).getUTCDay();
  const habil = dia => { if (dia === 0) return fecha(0); let k = 0, d = 0; const paso = Math.sign(dia);
    while (k < Math.abs(dia)) { d += paso; if (diaSemana(fecha(d)) !== 0) k++; } return fecha(d); };
  const iso = (dia, hhmm) => `${habil(dia)}T${hhmm}:00-04:00`;
  const masMin = (hhmm, min) => { const [h, m] = hhmm.split(':').map(Number); const t = h * 60 + m + min;
    return `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`; };
  const MOTIVOS = ['Dolor de cabeza frecuente', 'Chequeo anual', 'Revisión de análisis de sangre', 'Presión alta',
    'Tos y fiebre desde hace tres días', 'Dolor en el pecho al hacer ejercicio', 'Control de tratamiento', 'Manchas en la piel'];
  let n = 0;
  async function cita(dia, medico, code, hhmm, pac, fin, extra = {}) {
    const dur = SERVICIOS.concat(PEDIATRIA).find(s => s.code === code).dur;
    try {
      const a = await api('POST', 'v1/appointment', {
        patientId: P(pac), staffId: MEDICOS[medico], appointmentTypeCatalogId: idServicio(code),
        scheduledStartTime: iso(dia, hhmm), scheduledEndTime: iso(dia, masMin(hhmm, dur)), durationMinutes: dur,
        reasonForVisit: MOTIVOS[n++ % MOTIVOS.length], source: extra.source ?? 'PHONE',
      });
      for (const paso of fin) {
        try {
          if (paso === 'confirm') await api('POST', `v1/appointment/${a.id}/confirm`, { confirmationMethod: 'PHONE' });
          else if (paso === 'cancel') await api('POST', `v1/appointment/${a.id}/cancel`, { cancellationReason: 'PATIENT_REQUEST', cancellationNotes: 'La paciente pidió otra fecha' });
          else if (paso === 'check-in') await api('POST', `v1/appointment/${a.id}/check-in`, {});
          // Finalizar exige nota clínica firmada: la demo la da por atendida directo en la base.
          else if (paso === 'complete') sql(`UPDATE appointments SET status='COMPLETED', actual_end_time=scheduled_end_time WHERE id=${a.id};
            UPDATE patient_tickets SET status='COMPLETED', finished_at=NOW() WHERE appointment_id=${a.id};`);
          else await api('POST', `v1/appointment/${a.id}/${paso}`, {});
        } catch (e) { log(`    AVISO ${hhmm} ${medico} ${paso}: ${String(e.message).slice(0, 200)}`); }
      }
      return a;
    } catch (e) { log(`  AVISO cita ${habil(dia)} ${hhmm} ${medico}: ${String(e.message).slice(0, 300)}`); }
  }
  const HECHA = ['confirm', 'check-in', 'call', 'start', 'complete'];
  // Hoy
  await cita(0, 'ana', 'CONSULTA-GENERAL', '08:00', 0, HECHA);
  await cita(0, 'ana', 'CONSULTA-GENERAL', '08:30', 1, HECHA);
  await cita(0, 'ana', 'CONSULTA-GENERAL', '09:00', 2, ['confirm', 'check-in', 'call', 'start']);
  await cita(0, 'ana', 'CONSULTA-GENERAL', '09:30', 3, ['confirm', 'check-in']);
  await cita(0, 'ana', 'CONSULTA-GENERAL', '10:00', 4, ['confirm']);
  await cita(0, 'ana', 'CONSULTA-GENERAL', '10:30', 5, []);
  await cita(0, 'ana', 'CONSULTA-GENERAL', '11:00', 6, []);
  await cita(0, 'ana', 'CONTROL', '14:00', 7, []);
  await cita(0, 'jorge', 'CONTROL', '08:15', 8, HECHA);
  await cita(0, 'jorge', 'CONSULTA-GENERAL', '14:00', 9, ['confirm']);
  await cita(0, 'jorge', 'CONSULTA-GENERAL', '14:30', 10, ['cancel']);
  await cita(0, 'jorge', 'CONSULTA-GENERAL', '15:00', 11, []);
  await cita(0, 'marta', 'CONSULTA-GINECOLOGICA', '10:00', 12, ['confirm', 'check-in']);
  await cita(0, 'marta', 'CONSULTA-GINECOLOGICA', '10:30', 4, ['no-show']);
  await cita(0, 'pablo', 'EVALUACION-CARDIOLOGICA', '14:00', 5, ['confirm']);
  await cita(0, 'pablo', 'EVALUACION-CARDIOLOGICA', '15:00', 3, []);
  await cita(0, 'elias', 'CONSULTA-DERMATOLOGICA', '08:00', 10, HECHA);
  await cita(0, 'elias', 'CONSULTA-DERMATOLOGICA', '09:00', 7, ['confirm']);
  await cita(0, 'luis', 'CONSULTA-PEDIATRICA', '08:30', 13, ['confirm', 'check-in']);
  await cita(0, 'luis', 'CONSULTA-PEDIATRICA', '09:30', 14, []);
  // Próximos días
  await cita(1, 'ana', 'CONSULTA-GENERAL', '08:30', 9, ['confirm']);
  await cita(1, 'ana', 'CONSULTA-GENERAL', '09:00', 11, []);
  await cita(1, 'jorge', 'CONSULTA-GENERAL', '15:30', 0, []);
  await cita(1, 'pablo', 'EVALUACION-CARDIOLOGICA', '16:00', 1, ['confirm']);
  await cita(1, 'marta', 'CONSULTA-GINECOLOGICA', '11:00', 2, []);
  await cita(2, 'ana', 'CONTROL', '14:30', 2, []);
  await cita(2, 'elias', 'CONSULTA-DERMATOLOGICA', '10:00', 6, []);
  await cita(3, 'luis', 'CONSULTA-PEDIATRICA', '10:00', 14, ['confirm']);
  await cita(3, 'jorge', 'CONSULTA-GENERAL', '16:00', 8, []);
  await cita(3, 'pablo', 'EVALUACION-CARDIOLOGICA', '14:30', 6, []);
  await cita(4, 'ana', 'CONSULTA-GENERAL', '10:00', 1, []);
  // Ayer (historia)
  await cita(-1, 'ana', 'CONSULTA-GENERAL', '09:00', 9, HECHA);
  await cita(-1, 'jorge', 'CONSULTA-GENERAL', '14:00', 3, HECHA);
  await cita(-1, 'pablo', 'EVALUACION-CARDIOLOGICA', '15:00', 11, ['no-show']);
  // Una reserva desde el portal (el próximo día de consulta, con Ana Pérez: cae en la semana visible)
  const pag = paginas['ana/CONSULTA-GENERAL'];
  const [doc, mot] = pag.slug.split('/');
  try {
    const tipos = await (await fetch(`${API}/v1/booking/${doc}/${mot}/event-types`)).json();
    const et = (tipos?.data ?? tipos)?.[0];
    const r = await fetch(`${API}/v1/booking/${doc}/${mot}/book`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bookerName: 'Natalia Ramírez', bookerEmail: 'natalia.ramirez@correo.test', bookerPhone: '809-555-0177',
        startTime: iso(1, '11:00'), endTime: iso(1, '11:30'), bookingEventType: { id: et?.id }, recaptchaToken: 'dev-bypass',
        customAnswers: { 'Motivo de la consulta': 'Chequeo general' } }),
    });
    log(`  reserva en línea: ${r.status} ${(await r.text()).slice(0, 160)}`);
  } catch (e) { log('  AVISO reserva en línea: ' + e.message); }
  log(`  citas: ${uno(`SELECT COUNT(*) FROM appointments WHERE company_id=${E} AND scheduled_date >= '${fecha(-1)}'`)}`);
}
sql(`UPDATE partners SET deleted_at=NOW() WHERE company_id=${E} AND deleted_at IS NULL AND personal_email='natalia.ramirez@correo.test' AND ${estado === 'C' ? '0' : '1'};`);
try { execFileSync('docker', ['exec', 'germiva-redis', 'redis-cli', 'FLUSHALL'], { stdio: 'ignore' }); } catch { /* */ }
log(`estado ${estado} listo en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
