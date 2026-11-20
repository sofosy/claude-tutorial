// Utilidades de la serie «Fabricación» (nov. 2026): empresa 1 «Panadería Germiva», usuario admin.
// Sin dependencias npm. Pensado para el entorno de Germiva-api/scripts/dev-env/up.sh (MySQL y Redis en Docker).
import { execFileSync } from 'node:child_process';

export const API = process.env.GERMIVA_API || 'http://localhost:3001/api';
export const EMPRESA = 1;
const MYSQL = ['exec', '-i', 'germiva-dev-mysql', 'mysql', '-uroot', '--default-character-set=utf8mb4', '-N', '-B', 'germiva'];

export function sql(texto) {
  const out = execFileSync('docker', MYSQL, { input: texto, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  return out.split(/\r?\n/).filter(Boolean).map(l => l.split('\t'));
}
export const uno = s => sql(s)[0]?.[0];

let token = null;
export async function login() {
  const r = await fetch(`${API}/auth/dev/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin' }),
  });
  const j = await r.json();
  if (!j.accessToken) throw new Error('login admin: ' + JSON.stringify(j).slice(0, 300));
  token = j.accessToken;
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
  if (!r.ok) throw new Error(`${metodo} ${ruta} → ${r.status}: ${txt.slice(0, 600)}`);
  return j?.data !== undefined && j?.statusCode === undefined ? j.data : j;
}
export const idProducto = nombre =>
  +uno(`SELECT id FROM products WHERE company_id=${EMPRESA} AND name='${nombre}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
export const idUbicacion = posicion =>
  +uno(`SELECT id FROM inventory_location WHERE company_id=${EMPRESA} AND position='${posicion}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
export function log(...a) { console.log(new Date().toISOString().slice(11, 19), ...a); }
