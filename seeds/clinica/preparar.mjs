// node seeds/clinica/preparar.mjs
// Arma la clínica de demo «Centro Médico Los Prados» (perfil Centro Médico) sobre la empresa que creó
// /auth/dev/register con admin.losprados@regisalud.test. Idempotente: lo que ya existe no se duplica.
// Deja: consultorios 1-3, seis médicos con su consulta y su horario (Luis Gómez sin configurar: lo hace
// el video 1 de Citas) y los pacientes de demo. Las citas de cada video las arma citas.mjs.
import { sql, uno, api, login, log, esc, empresa } from './_lib.mjs';

const E = empresa();
log('empresa', E);
await login();

sql(`UPDATE companies SET slug='los-prados', medical_profile='MEDICAL_CENTER' WHERE id=${E};
     UPDATE subscriptions SET expirationDate='2027-12-31 23:00:00', nextBillingDate='2027-12-31 23:00:00', status='ACTIVE' WHERE company_id=${E};`);

// ── Consultorios ──────────────────────────────────────────────────────────────────────────────────
const CONSULTORIOS = [['CONS-01', 'Consultorio 1', '1'], ['CONS-02', 'Consultorio 2', '1'], ['CONS-03', 'Consultorio 3', '2']];
const consultorio = {};
for (const [code, name, floor] of CONSULTORIOS) {
  let id = uno(`SELECT id FROM consultorios WHERE company_id=${E} AND code='${code}' AND deleted_at IS NULL`);
  if (!id) id = (await api('POST', 'v1/consultorio', { code, name, floor, active: true, isMainBranch: code === 'CONS-01' })).id;
  consultorio[code] = +id;
}
log('consultorios', consultorio);

// ── Médicos ──────────────────────────────────────────────────────────────────────────────────────
// [clave, nombre, apellido, segundo, cédula, género, especialidades, exequátur, precio, franjas]
const MEDICOS = [
  ['ana', 'Ana', 'Pérez', 'Ramírez', '001-0555101-1', 'F', [3], 'EXQ-10233', 1500,
    [{ dias: 'L-S', ini: '08:00', fin: '12:00', turno: 30, cons: 'CONS-01', esp: 3 }]],
  ['jorge', 'Jorge', 'Medina', 'Castro', '001-0555102-2', 'M', [1, 3], 'EXQ-10871', 2000,
    [{ dias: 'L-S', ini: '14:00', fin: '18:00', turno: 30, cons: 'CONS-02', esp: 1 }]],
  ['marta', 'Marta', 'Reyes', 'Almonte', '001-0555103-3', 'F', [6], 'EXQ-11342', 2500,
    [{ dias: 'L-S', ini: '08:00', fin: '13:00', turno: 30, cons: 'CONS-02', esp: 6 }]],
  ['pablo', 'Pablo', 'Santos', 'Lora', '001-0555104-4', 'M', [7], 'EXQ-09815', 3500,
    [{ dias: 'L-S', ini: '14:00', fin: '18:00', turno: 30, cons: 'CONS-03', esp: 7 }]],
  ['elias', 'Elías', 'Tavárez', 'Mejía', '001-0555105-5', 'M', [10], 'EXQ-12077', 2200,
    [{ dias: 'L-S', ini: '08:00', fin: '12:00', turno: 20, cons: 'CONS-03', esp: 10 }]],
  ['luis', 'Luis', 'Gómez', 'Herrera', '001-0555106-6', 'M', [4], 'EXQ-12450', null, []],
];
const DIAS = { 'L-S': ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'], 'L-V': ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'] };
export const medico = {};
for (const [clave, nombre, ap1, ap2, ced, g, esp, exq, precio, franjas] of MEDICOS) {
  let id = uno(`SELECT id FROM partners WHERE company_id=${E} AND isMedicalStaff=1 AND tin='${ced.replace(/-/g, '')}' AND deleted_at IS NULL`)
    || uno(`SELECT id FROM partners WHERE company_id=${E} AND isMedicalStaff=1 AND name='${esc(nombre)}' AND firstLastName='${esc(ap1)}' AND deleted_at IS NULL`);
  if (!id) {
    id = (await api('POST', 'v1/partner/medical-staff', {
      name: nombre, firstLastName: ap1, secondLastName: ap2, documentType: 'CEDULA', documentNumber: ced,
      birthDate: '1980-05-10', gender: g, medicalLicenseNumber: exq, medicalLicenseExpiry: '2030-12-31',
      medicalSpecialtyIds: esp, personalMobilePhone: '809-555-02' + String(MEDICOS.findIndex(m => m[0] === clave)).padStart(2, '0'),
      // La doctora Ana Pérez entra al sistema: con su sesión se graba el consentimiento informado.
      ...(clave === 'ana' ? { access: { username: 'ana.perez.losprados', email: 'ana.perez@regisalud.test',
        password: 'AnaPerez2026!', roleIds: [+uno(`SELECT id FROM roles WHERE company_id=${E} AND name='Médico'`)] } } : {}),
    })).id;
  }
  medico[clave] = +id;
  if (precio !== null) {
    await api('PUT', `v1/booking-pages/staff/${id}/consultation`, { price: precio, requiresAuthorization: false, allowOnlineBooking: true });
  }
  const tiene = +uno(`SELECT COUNT(*) FROM staff_schedules WHERE staff_id=${id} AND deleted_at IS NULL`);
  if (!tiene) {
    for (const f of franjas) for (const dia of DIAS[f.dias]) {
      await api('POST', 'v1/staff-schedule', {
        staffId: +id, consultorioId: consultorio[f.cons], dayOfWeek: dia, startTime: f.ini, endTime: f.fin,
        slotDurationMinutes: f.turno, maxClientsPerSlot: 1, specialtyIds: [f.esp], effectiveFrom: '2026-01-01',
        allowOnlineBooking: true, allowSameDayBooking: true,
      });
    }
  }
}
log('médicos', medico);

// ── Pacientes de demo (cédulas inventadas, serie 402-0555…) ──────────────────────────────────────
export const PACIENTES = [
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
  // Ficha sin correo: su reserva por internet no se reconoce y espera en «Reservas sin ficha» (Citas 2).
  ['Gabriela', 'Fernández', '402-0555016-6', 'F', '1994-07-08', '829-555-0166', null],
];
const paciente = {};
for (const [nombre, ap, ced, g, nac, tel, sinCorreo] of PACIENTES) {
  const limpio = ced.replace(/-/g, '');
  let id = uno(`SELECT id FROM partners WHERE company_id=${E} AND partnerType='PATIENT' AND REPLACE(tin,'-','')='${limpio}' AND deleted_at IS NULL`);
  if (!id) {
    const correo = `${nombre.split(' ')[0]}.${ap}`.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase() + '@correo.test';
    id = (await api('POST', 'v1/patients', {
      name: nombre, firstLastName: ap, documentType: 'CEDULA', documentNumber: ced, birthDate: nac, gender: g,
      personalMobilePhone: tel, personalEmail: sinCorreo === null ? undefined : correo, password: 'Paciente2026!',
    })).id;
  }
  paciente[`${nombre} ${ap}`] = +id;
}
log('pacientes', Object.keys(paciente).length);

// ── Perfil «Centro Médico» con su menú de fábrica (como la pantalla Perfil del consultorio) ──────────
await api('PATCH', 'v1/company-menu-profile/me', {
  medicalProfile: 'MEDICAL_CENTER', hiddenMenuKeys: ['purchases', 'accounting', 'payroll', 'hr', 'crm', 'credit'],
});
// La dueña solo administra: no es médico (con «Centro Médico» el dueño no aparece en Médicos).
sql(`UPDATE partners SET isMedicalStaff=0 WHERE company_id=${E} AND name='Carmen' AND firstLastName LIKE 'Pe%';
     DELETE FROM company_notifications WHERE company_id=${E};`);
log('perfil Centro Médico aplicado');
