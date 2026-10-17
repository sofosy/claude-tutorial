// Utilidades de la serie de Cajas: API, logins y SQL acotados a la EMPRESA DEMO.
// Sin dependencias npm (node:child_process + fetch nativo).
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
export const EMPRESA = 43; // «Ferretería El Progreso» (RNC 130555021) — la ÚNICA empresa que tocan estos scripts
export const API = process.env.GERMIVA_API || 'http://localhost:3001/api';
export const CLAVE = 'Demo2026!';
export const MYSQL = process.env.MYSQL_BIN || 'C:/Program Files/MySQL/MySQL Server 9.7/bin/mysql.exe';
export const CUENTA_INGRESOS = 116; // 4.02.01.02 «Otros ingresos diversos» (catálogo global)
export const CUENTA_GASTOS = 167;   // 6.03.21 «Otros gastos generales» (catálogo global)
export const EFECTIVO = 1;          // payment_methods.id Efectivo (CASH)

/** Ejecuta SQL (texto) contra la BD local sin binlog. Devuelve filas TSV sin cabecera. */
export function sql(texto, { db = 'germiva' } = {}) {
  const out = execFileSync(MYSQL, [
    '-h', '127.0.0.1', '-u', 'root', '--default-character-set=utf8mb4', '-N', '-B',
    '--init-command=SET SESSION sql_log_bin=0', db,
  ], { input: texto, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
  return out.split(/\r?\n/).filter(Boolean).map(l => l.split('\t'));
}

const tokens = {};
/** Login por el endpoint de desarrollo. OJO: revoca la sesión previa del mismo usuario. */
export async function login(usuario) {
  if (tokens[usuario]) return tokens[usuario];
  const r = await fetch(`${API}/auth/dev/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: usuario, password: CLAVE }),
  });
  const j = await r.json();
  if (!j.accessToken) throw new Error(`login ${usuario}: ${JSON.stringify(j).slice(0, 300)}`);
  if (j.session?.currentCompanyId !== EMPRESA) throw new Error(`${usuario} no está en la empresa ${EMPRESA}`);
  tokens[usuario] = j.accessToken;
  return j.accessToken;
}

export async function api(usuario, metodo, ruta, cuerpo) {
  const t = await login(usuario);
  const r = await fetch(`${API}/${ruta}`, {
    method: metodo,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${t}` },
    body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
  });
  const txt = await r.text();
  let j; try { j = JSON.parse(txt); } catch { j = txt; }
  if (!r.ok) throw new Error(`${metodo} ${ruta} (${usuario}) → ${r.status}: ${txt.slice(0, 400)}`);
  return j?.data !== undefined && j?.statusCode === undefined ? j.data : j;
}

export const idDe = o => o?.id ?? o?.data?.id;

export function log(...a) { console.log(new Date().toISOString().slice(11, 19), ...a); }

export function leerJson(p, def) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return def; } }
