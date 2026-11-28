// Utilidades de las series de la clínica (Citas, Pacientes, Consentimiento, ARS) sobre el entorno
// del contenedor (Germiva-api/scripts/dev-env/up.sh --source regisalud-seed --web).
// Empresa: «Centro Médico Los Prados», creada por /auth/dev/register (ver preparar.mjs).
import { execFileSync } from 'node:child_process';

export const API = process.env.GERMIVA_API || 'http://localhost:3001/api';
export const USUARIO = 'admin.losprados@regisalud.test';
export const CLAVE = 'LosPrados2026!';

export function sql(texto) {
  const out = execFileSync('docker', ['exec', '-i', 'germiva-dev-mysql', 'mysql', '-uroot',
    '--default-character-set=utf8mb4', '-N', '-B', 'germiva'], { input: texto, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
  return out.split(/\r?\n/).filter(Boolean).map(l => l.split('\t'));
}
export const uno = s => sql(s)[0]?.[0];

let token = null;
export async function login(usuario = USUARIO, clave = CLAVE) {
  const r = await fetch(`${API}/auth/dev/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: usuario, password: clave }),
  });
  const j = await r.json();
  if (!j.accessToken) throw new Error('login: ' + JSON.stringify(j).slice(0, 300));
  token = j.accessToken;
  return token;
}

export async function api(metodo, ruta, cuerpo) {
  if (!token) await login();
  const r = await fetch(`${API}/${ruta}`, {
    method: metodo,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
  });
  const txt = await r.text();
  let j; try { j = JSON.parse(txt); } catch { j = txt; }
  if (r.status === 401) { token = null; return api(metodo, ruta, cuerpo); }
  if (!r.ok) throw new Error(`${metodo} ${ruta} → ${r.status}: ${txt.slice(0, 600)}`);
  return j?.data !== undefined && j?.statusCode === undefined ? j.data : j;
}

export function log(...a) { console.log(new Date().toISOString().slice(11, 19), ...a); }

// Fecha local (America/Santo_Domingo, UTC-4) desplazada `dias` desde hoy: 'YYYY-MM-DD'.
export function fecha(dias = 0) {
  return new Date(Date.now() - 4 * 3600e3 + dias * 86400e3).toISOString().slice(0, 10);
}
export const esc = s => String(s).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
export const empresa = () => +uno(`SELECT company_id FROM users WHERE email='${USUARIO}'`) || +uno(`SELECT id FROM companies WHERE rnc='131456789' ORDER BY id DESC LIMIT 1`);
