// node seeds/clinica/consentimiento.mjs
// Deja a Rosa Elena Martínez sin consentimientos: el video crea el suyo desde cero (RC-2026-00001).
import { sql, uno, log, empresa } from './_lib.mjs';

const E = empresa();
const ROSA = +uno(`SELECT id FROM partners WHERE company_id=${E} AND name='Rosa Elena' AND firstLastName='Martínez' AND deleted_at IS NULL ORDER BY id LIMIT 1`);
const registros = `SELECT id FROM clinical_records WHERE company_id=${E}`;
sql(`
DELETE FROM consent_request_events WHERE request_id IN (SELECT id FROM consent_requests WHERE clinical_record_id IN (${registros}));
DELETE FROM consent_requests WHERE clinical_record_id IN (${registros});
DELETE FROM clinical_record_values WHERE record_id IN (${registros});
DELETE FROM odontogram_records WHERE clinical_record_id IN (${registros});
DELETE FROM clinical_records WHERE company_id=${E};
UPDATE sys_sequences SET current_value=0 WHERE company_id=${E} AND code='CLINICAL_RECORD';
DELETE FROM company_notifications WHERE company_id=${E};`);
log('consentimiento listo: Rosa', ROSA, 'sin registros clínicos');
