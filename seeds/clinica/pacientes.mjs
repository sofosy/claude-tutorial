// node seeds/clinica/pacientes.mjs
// Deja los pacientes de demo como al principio de la serie «Pacientes»: borra las fichas que crean los videos
// (Sofía Ramírez, Mateo Batista, y los registrados por enlace) con lo que cuelga de ellas, los enlaces de registro,
// los accesos y resultados del portal, y las alergias/medicación/alertas de los pacientes de demo.
import { sql, log, empresa } from './_lib.mjs';
const E = empresa();
const nuevos = `SELECT id FROM partners WHERE company_id=${E} AND partnerType='PATIENT' AND (
  (name='Sofía' AND firstLastName='Ramírez') OR (name='Mateo' AND firstLastName='Batista') OR
  (name='Valeria' AND firstLastName='Méndez') OR (name='Tomás' AND firstLastName='Polanco'))`;
const tablas = sql(`SELECT DISTINCT table_name FROM information_schema.columns WHERE table_schema='germiva'
  AND column_name='patient_id' AND table_name NOT IN ('appointments')`).map(r => r[0]);
const ids = sql(nuevos).map(r => r[0]);
if (ids.length) {
  const lista = ids.join(',');
  sql(`SET FOREIGN_KEY_CHECKS=0;
    ${tablas.map(t => `DELETE FROM \`${t}\` WHERE patient_id IN (${lista});`).join('\n')}
    DELETE FROM appointments WHERE patient_id IN (${lista});
    DELETE FROM partners WHERE id IN (${lista});
    SET FOREIGN_KEY_CHECKS=1;`);
}
sql(`DELETE FROM patient_intake_links WHERE company_id=${E};
     DELETE FROM patient_allergies WHERE patient_id IN (SELECT id FROM partners WHERE company_id=${E});
     DELETE FROM patient_medications WHERE patient_id IN (SELECT id FROM partners WHERE company_id=${E});
     DELETE FROM patient_medical_alerts WHERE patient_id IN (SELECT id FROM partners WHERE company_id=${E});
     UPDATE partners SET active=1, isActivePatient=1 WHERE company_id=${E} AND partnerType='PATIENT';
     DELETE FROM company_notifications WHERE company_id=${E};`);
log('pacientes listos; fichas borradas:', ids.length);
