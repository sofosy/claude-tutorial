// node seeds/cajas/restaurar.mjs <S#> [--sin-desplazar]
// Devuelve la empresa demo (43) al canon fijado con fijar.mjs. TODO acotado a company_id=43:
//   filas nuevas → DELETE; filas cambiadas → UPDATE desde el volcado; filas borradas → INSERT;
//   sys_sequences (trigger anti-DELETE) → UPDATE; audit_logs → DELETE id > marca.
// Una sola sesión mysql, sin binlog (sql_log_bin=0), FOREIGN_KEY_CHECKS=0 dentro de la sesión.
// Además DESPLAZA en el tiempo las sesiones ABIERTAS (y sus movimientos) lo transcurrido desde el
// fijado, para que «Abierta hace 2 h» siga diciendo lo mismo en cada toma (--sin-desplazar lo evita).
import fs from 'node:fs';
import path from 'node:path';
import { AQUI, EMPRESA, sql, log } from './_lib.mjs';
import { TABLAS, W, snap } from './_estado.mjs';

const estado = process.argv[2];
const dir = path.join(AQUI, 'estados');
const fSql = path.join(dir, `${estado}.sql`), fMeta = path.join(dir, `${estado}.json`);
if (!estado || !fs.existsSync(fSql)) { console.error(`uso: node restaurar.mjs S#  (no existe ${fSql})`); process.exit(2); }
const meta = JSON.parse(fs.readFileSync(fMeta, 'utf8'));
if (meta.empresa !== EMPRESA) throw new Error('el canon es de otra empresa');
const t0 = Date.now();
// la auditoría del API llega tarde: se espera a que deje de crecer
// (created_at de audit_logs va en hora RD, así que se compara el MAX(id), no la hora)
const ultimo = () => sql(`SELECT IFNULL(MAX(id),0) FROM audit_logs WHERE ${W}`)[0][0];
for (let i = 0, a = ultimo(); i < 10; i++) { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 300); const b = ultimo(); if (b === a) break; a = b; }

// columnas (sin las generadas) de cada tabla
const cols = {};
for (const [t, c] of sql(`SET SESSION group_concat_max_len=1000000; SELECT table_name, GROUP_CONCAT(column_name ORDER BY ordinal_position)
  FROM information_schema.columns WHERE table_schema='germiva'
  AND table_name IN (${TABLAS.map(([t]) => `'${t}'`).join(',')})
  AND extra NOT LIKE '%VIRTUAL GENERATED%' AND extra NOT LIKE '%STORED GENERATED%' GROUP BY table_name`)) cols[t] = c.split(',');

let q = 'SET FOREIGN_KEY_CHECKS=0;\nSET SESSION sql_mode=REPLACE(@@sql_mode,\'STRICT_TRANS_TABLES\',\'\');\n';
// canon viejo (auditoría por marca de agua, sin filas volcadas) → se respeta su modo
const volcado = fs.readFileSync(fSql, 'utf8');
const modoDe = (t, m) => (t === 'audit_logs' && m === 'filas' && meta.marca_audit_logs
  && !volcado.includes('INSERT INTO `snap_audit_logs`') ? 'marca' : m);
// CREATE … SELECT … LIMIT 0: copia columnas sin índices ni particiones (audit_logs está particionada)
for (const [t, modo] of TABLAS) if (modoDe(t, modo) !== 'marca') {
  q += `CREATE TEMPORARY TABLE ${snap(t)} SELECT * FROM ${t} LIMIT 0;\nALTER TABLE ${snap(t)} ADD PRIMARY KEY (id);\n`;
}
q += volcado + '\n';
for (const [t, modo0] of TABLAS) {
  const modo = modoDe(t, modo0);
  const c = cols[t].filter(x => x !== 'id');
  const lista = cols[t].map(x => `\`${x}\``).join(',');
  const set = c.map(x => `g.\`${x}\`=s.\`${x}\``).join(',');
  if (modo === 'marca') { q += `DELETE FROM ${t} WHERE ${W} AND id > ${meta.marca_audit_logs};\n`; continue; }
  if (modo === 'filas') q += `DELETE FROM ${t} WHERE ${W} AND id NOT IN (SELECT id FROM ${snap(t)});\n`;
  q += `UPDATE ${t} g JOIN ${snap(t)} s ON s.id=g.id SET ${set} WHERE g.${W};\n`;
  if (modo === 'filas') q += `INSERT INTO ${t} (${lista}) SELECT ${cols[t].map(x => `s.\`${x}\``).join(',')} FROM ${snap(t)} s LEFT JOIN ${t} g ON g.id=s.id WHERE g.id IS NULL;\n`;
  if (modo === 'secuencia') q += `UPDATE ${t} SET current_value=initial_value WHERE ${W} AND id NOT IN (SELECT id FROM ${snap(t)});\n`;
}
if (!process.argv.includes('--sin-desplazar')) {
  q += `SET @d := TIMESTAMPDIFF(SECOND, '${meta.fijado_en}', NOW());
UPDATE cash_movements m JOIN cashier_sessions s ON s.id=m.cashier_session_is AND s.isOpen=1 AND s.${W}
  SET m.created_at=m.created_at + INTERVAL @d SECOND, m.updated_at=m.updated_at + INTERVAL @d SECOND,
      m.approved_at=IF(m.approved_at IS NULL, NULL, m.approved_at + INTERVAL @d SECOND) WHERE m.${W};
UPDATE cashier_sessions SET openedAt=openedAt + INTERVAL @d SECOND, created_at=created_at + INTERVAL @d SECOND
  WHERE ${W} AND isOpen=1;\n`;
}
q += 'SET FOREIGN_KEY_CHECKS=1;\n';
q += TABLAS.map(([t]) => `SELECT '${t}', COUNT(*) FROM ${t} WHERE ${W}`).join(' UNION ALL ') + ';\n';

const filas = sql(q);
// sys_sequences no admite DELETE: una secuencia nacida después del canon queda (en su valor inicial)
const mal = filas.filter(([t, n]) => meta.conteos[t] !== undefined && +n !== meta.conteos[t] && !(t === 'sys_sequences' && +n > meta.conteos[t]));
const seg = ((Date.now() - t0) / 1000).toFixed(1);
if (mal.length) { console.error(`✗ ${estado} restaurado con diferencias en ${seg} s:`, mal.map(([t, n]) => `${t} ${n}≠${meta.conteos[t]}`).join(', ')); process.exit(1); }
log(`✓ ${estado} restaurado y verificado (${filas.length} tablas, conteos iguales al canon) en ${seg} s`);
