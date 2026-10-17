// Utilidades de la serie «Seguridad»: API, logins y SQL acotados a la EMPRESA DEMO
// «Distribuidora Las Palmas SRL» (RNC 130555036). Sin dependencias npm.
// La empresa se crea con sembrar.mjs; su id se lee de ids.json (o de la BD por RNC).
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
export const API = process.env.GERMIVA_API || 'http://localhost:3001/api';
export const CLAVE = 'Demo2026!';
export const RNC = '130555036';
export const DOMINIO = 'germiva.demo';
export const MYSQL = process.env.MYSQL_BIN || 'C:/Program Files/MySQL/MySQL Server 9.7/bin/mysql.exe';
export const IDS = path.join(AQUI, 'ids.json');

// D-S13: lo sembrado son ingresos y acciones de PERSONAS en su oficina, no de un script. Sin esto la
// bitácora guarda el user-agent de Node («node») y el Resumen/Auditoría lo pintan «Cliente de API».
// Toda petición de la siembra (api(), login() y los fetch directos de sembrar.mjs) sale como Chrome
// de escritorio en Windows, igual que las tomas grabadas con el navegador.
export const NAVEGADOR_UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';
if (!globalThis.fetch.__seguridadUA) {
  const fetchOriginal = globalThis.fetch;
  globalThis.fetch = (url, init = {}) => {
    const headers = new Headers(init.headers ?? {});
    if (!headers.has('User-Agent')) headers.set('User-Agent', NAVEGADOR_UA);
    return fetchOriginal(url, { ...init, headers });
  };
  globalThis.fetch.__seguridadUA = true;
}

/** SQL contra la BD local SIN binlog (R14). Devuelve filas TSV sin cabecera. */
export function sql(texto, { db = 'germiva' } = {}) {
  const out = execFileSync(MYSQL, [
    '-h', '127.0.0.1', '-u', 'root', '--default-character-set=utf8mb4', '-N', '-B',
    '--init-command=SET SESSION sql_log_bin=0', db,
  ], { input: texto, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
  return out.split(/\r?\n/).filter(Boolean).map(l => l.split('\t'));
}
export const uno = s => sql(s)[0]?.[0];
export const esc = s => String(s).replace(/\\/g, '\\\\').replace(/'/g, "\\'");

/** id de la empresa demo (null si aún no existe). */
export function empresa() {
  const id = uno(`SELECT id FROM companies WHERE rnc='${RNC}' AND deleted_at IS NULL LIMIT 1`);
  return id ? +id : null;
}
export const EMPRESA = empresa();

const tokens = {};
/** Login por el endpoint de desarrollo. OJO: revoca la sesión previa del MISMO usuario (R26). */
export async function login(usuario, { forzar = false } = {}) {
  if (tokens[usuario] && !forzar) return tokens[usuario];
  const r = await fetch(`${API}/auth/dev/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: usuario, password: CLAVE }),
  });
  const j = await r.json();
  if (!j.accessToken) throw new Error(`login ${usuario}: ${JSON.stringify(j).slice(0, 300)}`);
  const cia = empresa();
  if (cia && j.session?.currentCompanyId !== cia) throw new Error(`${usuario} no está en la empresa ${cia}`);
  tokens[usuario] = j.accessToken;
  return j.accessToken;
}

/** Llamada al API como `usuario`. Devuelve el cuerpo (desenvuelve {data}). */
export async function api(usuario, metodo, ruta, cuerpo, { permitir = [] } = {}) {
  const t = await login(usuario);
  const r = await fetch(`${API}/${ruta}`, {
    method: metodo,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${t}` },
    body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
  });
  const txt = await r.text();
  let j; try { j = JSON.parse(txt); } catch { j = txt; }
  if (!r.ok && !permitir.includes(r.status)) throw new Error(`${metodo} ${ruta} (${usuario}) → ${r.status}: ${txt.slice(0, 500)}`);
  if (!r.ok) return { _status: r.status, ...(typeof j === 'object' ? j : { txt: j }) };
  return j?.data !== undefined && j?.statusCode === undefined ? j.data : j;
}

export const permisoId = code => {
  const id = uno(`SELECT id FROM permission WHERE code='${code}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) throw new Error(`permiso ${code} no existe`);
  return +id;
};

export function log(...a) { console.log(new Date().toISOString().slice(11, 19), ...a); }
export function leerJson(p, def) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return def; } }
export const espera = ms => new Promise(r => setTimeout(r, ms));
