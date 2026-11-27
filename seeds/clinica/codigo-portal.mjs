// node seeds/clinica/codigo-portal.mjs <correo>  → imprime el código de 6 dígitos vigente del portal del paciente.
// El API guarda solo un HMAC del código (patient-portal.service.ts › codeHash); en el entorno local el secreto
// está en el .env del API, así que se recupera probando el millón de combinaciones (≈1 s). Solo para grabar.
import { createHmac } from 'node:crypto';
import fs from 'node:fs';
import { uno, empresa } from './_lib.mjs';

const correo = (process.argv[2] || '').trim().toLowerCase();
if (!correo) throw new Error('Falta el correo');
const env = fs.readFileSync(new URL('../../../Germiva-api/.env', import.meta.url), 'utf8');
const clave = (env.match(/^JWT_SECRET=(.*)$/m)?.[1] ?? '').trim().replace(/^"|"$/g, '');
const E = empresa();
const hash = uno(`SELECT challenge_hash FROM patient_portal_accounts WHERE company_id=${E} AND LOWER(email)='${correo}'`);
if (!hash) throw new Error(`Sin código pendiente para ${correo}`);
for (let i = 0; i < 1_000_000; i++) {
  const code = String(i).padStart(6, '0');
  const d = createHmac('sha256', clave).update(JSON.stringify(['patient-portal', E, correo, code])).digest('hex');
  if (d === hash) { console.log(code); process.exit(0); }
}
throw new Error('No se encontró el código');
