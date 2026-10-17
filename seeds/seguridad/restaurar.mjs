// node seeds/seguridad/restaurar.mjs <E#>
// Devuelve la empresa demo de Seguridad al canon fijado con fijar.mjs. TODO acotado a esa empresa
// (cada tabla con su WHERE de _estado.mjs): filas nuevas → DELETE; cambiadas → UPDATE desde el volcado;
// borradas → INSERT; tablas puente → reemplazo; sys_sequences → UPDATE. Incluye audit_logs de la
// empresa (particionada: las temporales se crean con CREATE … SELECT … LIMIT 0, sin particiones).
// Una sola sesión mysql, sin binlog (sql_log_bin=0), FOREIGN_KEY_CHECKS=0 dentro de la sesión.
// No restaura las sesiones de auth (cada toma entra de nuevo) ni company_user_activity_daily.
import fs from 'node:fs';
import path from 'node:path';
import { EMPRESA, sql, log } from './_lib.mjs';
import { AQUI, TABLAS, snap } from './_estado.mjs';

const estado = process.argv[2];
const dir = path.join(AQUI, 'estados');
const fSql = path.join(dir, `${estado}.sql`), fMeta = path.join(dir, `${estado}.json`);
if (!estado || !fs.existsSync(fSql)) { console.error(`uso: node seeds/seguridad/restaurar.mjs E#  (no existe ${fSql})`); process.exit(2); }
const meta = JSON.parse(fs.readFileSync(fMeta, 'utf8'));
if (meta.empresa !== EMPRESA) throw new Error(`el canon es de la empresa ${meta.empresa}, la demo es ${EMPRESA}`);
const t0 = Date.now();
// la auditoría del API llega tarde: se espera a que deje de crecer
const ultimo = () => sql(`SELECT IFNULL(MAX(id),0) FROM audit_logs WHERE company_id=${EMPRESA}`)[0][0];
// (el API vuelca la auditoría en lotes cada 2 s: la ventana tiene que cubrir un lote entero)
for (let i = 0, a = ultimo(); i < 6; i++) { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 2300); const b = ultimo(); if (b === a) break; a = b; }

const cols = {};
for (const [t, c] of sql(`SET SESSION group_concat_max_len=1000000; SELECT table_name, GROUP_CONCAT(column_name ORDER BY ordinal_position)
  FROM information_schema.columns WHERE table_schema='germiva'
  AND table_name IN (${TABLAS.map(([t]) => `'${t}'`).join(',')})
  AND extra NOT LIKE '%VIRTUAL GENERATED%' AND extra NOT LIKE '%STORED GENERATED%' GROUP BY table_name`)) cols[t] = c.split(',');

let q = 'SET FOREIGN_KEY_CHECKS=0;\nSET SESSION sql_mode=REPLACE(@@sql_mode,\'STRICT_TRANS_TABLES\',\'\');\n';
for (const [t, modo] of TABLAS) {
  q += `CREATE TEMPORARY TABLE ${snap(t)} SELECT * FROM ${t} LIMIT 0;\n`;
  if (modo !== 'reemplazo') q += `ALTER TABLE ${snap(t)} ADD PRIMARY KEY (id);\n`;
}
q += fs.readFileSync(fSql, 'utf8') + '\n';
for (const [t, modo, w] of TABLAS) {
  const lista = cols[t].map(x => `\`${x}\``).join(',');
  const sel = cols[t].map(x => `s.\`${x}\``).join(',');
  if (modo === 'reemplazo') { q += `DELETE FROM ${t} WHERE ${w};\nINSERT INTO ${t} (${lista}) SELECT ${sel} FROM ${snap(t)} s;\n`; continue; }
  const set = cols[t].filter(x => x !== 'id').map(x => `g.\`${x}\`=s.\`${x}\``).join(',');
  // el WHERE se evalúa sobre la tabla real (alias g) para las subconsultas sobre roles
  const wg = w.replace(/^(\w+)(?=[ =])/, 'g.$1');
  if (modo === 'filas') q += `DELETE g FROM ${t} g WHERE ${wg} AND g.id NOT IN (SELECT id FROM ${snap(t)});\n`;
  q += `UPDATE ${t} g JOIN ${snap(t)} s ON s.id=g.id SET ${set};\n`;
  if (modo === 'filas') q += `INSERT INTO ${t} (${lista}) SELECT ${sel} FROM ${snap(t)} s LEFT JOIN ${t} g ON g.id=s.id WHERE g.id IS NULL;\n`;
  if (modo === 'secuencia') q += `UPDATE ${t} SET current_value=initial_value WHERE ${w} AND id NOT IN (SELECT id FROM ${snap(t)});\n`;
}
q += 'SET FOREIGN_KEY_CHECKS=1;\n';
q += TABLAS.map(([t, , w]) => `SELECT '${t}', COUNT(*) FROM ${t} WHERE ${w}`).join(' UNION ALL ') + ';\n';

const filas = sql(q);
const mal = filas.filter(([t, n]) => meta.conteos[t] !== undefined && +n !== meta.conteos[t] && !(t === 'sys_sequences' && +n > meta.conteos[t]));
const seg = ((Date.now() - t0) / 1000).toFixed(1);
if (mal.length) { console.error(`✗ ${estado} restaurado con diferencias en ${seg} s:`, mal.map(([t, n]) => `${t} ${n}≠${meta.conteos[t]}`).join(', ')); process.exit(1); }
log(`✓ ${estado} restaurado y verificado (${filas.length} tablas, conteos iguales al canon) en ${seg} s`);
