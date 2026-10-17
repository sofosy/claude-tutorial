// node seeds/seguridad/_medir.mjs <salida.json> [--comparar <antes.json>]
// Mide qué tablas toca un flujo: por cada tabla con columna company_id, COUNT y MAX(updated_at) de la
// empresa demo de Seguridad (y MAX(id)); por cada tabla SIN company_id, AUTO_INCREMENT global. Con --comparar lista las diferencias.
// Solo LEE la BD.
import fs from 'node:fs';
import { sql, EMPRESA } from './_lib.mjs';

const [salida, flag, antesF] = process.argv.slice(2);
const conCia = sql(`SELECT c.table_name, SUM(c2.column_name='updated_at'), (SELECT COUNT(*) FROM information_schema.columns c3 WHERE c3.table_schema=c.table_schema AND c3.table_name=c.table_name AND c3.column_name='id') FROM information_schema.columns c
  JOIN information_schema.tables t ON t.table_schema=c.table_schema AND t.table_name=c.table_name AND t.table_type='BASE TABLE'
  LEFT JOIN information_schema.columns c2 ON c2.table_schema=c.table_schema AND c2.table_name=c.table_name AND c2.column_name='updated_at'
  WHERE c.table_schema='germiva' AND c.column_name='company_id' GROUP BY c.table_name`);
const partes = conCia.map(([t, u, i]) => `SELECT '${t}', COUNT(*), ${+u ? 'IFNULL(MAX(updated_at),0)' : "''"}, ${+i ? 'IFNULL(MAX(id),0)' : "''"} FROM \`${t}\` WHERE company_id=${EMPRESA}`);
const med = {};
for (let i = 0; i < partes.length; i += 80) for (const [t, n, u, m] of sql(partes.slice(i, i + 80).join(' UNION ALL '))) med[t] = `${n}|${u}|${m}`;
for (const [t, a] of sql(`SET SESSION information_schema_stats_expiry=0; SELECT table_name, IFNULL(auto_increment,0) FROM information_schema.tables WHERE table_schema='germiva' AND table_type='BASE TABLE'`)) if (!(t in med)) med[t] = `ai:${a}`;
fs.writeFileSync(salida, JSON.stringify(med, null, 0));
if (flag === '--comparar') {
  const antes = JSON.parse(fs.readFileSync(antesF, 'utf8'));
  for (const t of Object.keys(med).sort()) if (antes[t] !== med[t]) console.log(t.padEnd(40), antes[t], '→', med[t]);
}
