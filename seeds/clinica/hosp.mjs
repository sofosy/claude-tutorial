// node seeds/clinica/hosp.mjs H
// Estado del video «Hospitalización · Facturar los cargos del ingreso» (RegiSalud).
//   H  sobre cualquier estado con los servicios de ars.mjs (base o posterior): Daniel Polanco, sin seguro,
//      ingresado con la doctora Ana y tres cargos: hemograma y electrocardiograma aprobados, sonografía pendiente.
// Todo por el API, como en pantalla. Se guarda con `node seeds/clinica/ars.mjs guardar H`.
import { api, login, log, uno, empresa } from './_lib.mjs';

const E = empresa();
const ANA = 576;
const prod = code => +uno(`SELECT id FROM products WHERE company_id=${E} AND code='${code}' AND deleted_at IS NULL`);
const paciente = (n, a) => +uno(`SELECT id FROM partners WHERE company_id=${E} AND name='${n}' AND firstLastName='${a}' AND deleted_at IS NULL ORDER BY id LIMIT 1`);

async function estadoH() {
  await login();
  const daniel = paciente('Daniel Alberto', 'Polanco');
  const adm = await api('POST', 'v1/admission', {
    patient: daniel, attendingPhysician: ANA, admissionType: 'ELECTIVE', admissionSource: 'OUTPATIENT',
    chiefComplaint: 'Dolor abdominal', admissionDiagnosis: 'Dolor abdominal en estudio', admissionDate: new Date().toISOString(),
  });
  const ahora = new Date().toISOString();
  const cargos = [
    ['SRV-HEMOGRAMA', 'LABORATORY', 'Hemograma completo', 800, true],
    ['SRV-EKG', 'LABORATORY', 'Electrocardiograma', 1800, true],
    ['SRV-SONO-ABD', 'LABORATORY', 'Sonografía abdominal', 3500, false],
  ];
  for (const [code, chargeType, description, unitPrice, aprobar] of cargos) {
    const c = await api('POST', 'v1/admission-charge', {
      admission: adm.id, chargeType, chargeDate: ahora, description, product: prod(code), quantity: 1, unitPrice,
    });
    if (aprobar) await api('POST', `v1/admission-charge/${c.id}/approve`, {});
  }
  log('estado H listo: ingreso', adm.admissionNumber, 'de Daniel con dos cargos aprobados y uno pendiente');
}

if (process.argv[2] === 'H') await estadoH();
else { console.error('orden desconocida'); process.exit(1); }
