// Utilidades de la serie «Productos» (v3, 07/10/2026): empresa 1 «Tienda Germiva», usuario admin.
// Sin dependencias npm. SQL sin binlog (R14); API por el login de desarrollo.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
export const API = process.env.GERMIVA_API || 'http://localhost:3001/api';
export const MYSQL = 'C:/Program Files/MySQL/MySQL Server 9.7/bin/mysql.exe';
export const DUMP = MYSQL.replace(/mysql\.exe$/, 'mysqldump.exe');
export const CANON = path.join(AQUI, 'canon-productos.sql');
export const EMPRESA = 1;

const ENV = fs.readFileSync('C:/Users/isaac/Desktop/sofosy/germiva/Germiva-api/.env', 'utf8');
process.env.MYSQL_PWD = (ENV.match(/^DB_PASSWORD=(.*)$/m)?.[1] ?? '').trim().replace(/^"|"$/g, '');

export function sql(texto) {
  const out = execFileSync(MYSQL, ['-u', 'root', '--default-character-set=utf8mb4', '-N', '-B',
    '--init-command=SET SESSION sql_log_bin=0', 'germiva'], { input: texto, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
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
  if (!r.ok) throw new Error(`${metodo} ${ruta} → ${r.status}: ${txt.slice(0, 600)}`);
  return j?.data !== undefined && j?.statusCode === undefined ? j.data : j;
}

export const idProducto = nombre =>
  +uno(`SELECT id FROM products WHERE company_id=${EMPRESA} AND name='${nombre}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
export const idSocio = rnc =>
  +uno(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND tin='${rnc}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
export const UBICACION = 44; // «Pasillo A - Estante 1» · Almacén Sur
export const MOTIVO_COMPRA = 1; // «Compras de mercancía»

export function log(...a) { console.log(new Date().toISOString().slice(11, 19), ...a); }
