// node seeds/seguridad/fijar.mjs <E#>
// Fija el estado ACTUAL de la empresa demo de Seguridad como canon del estado E#: vuelca con mysqldump
// las filas de las tablas de _estado.mjs (cada una con su WHERE) a estados/<E#>.sql (renombradas a
// snap_<tabla>) y guarda conteos y hora en estados/<E#>.json. Solo LEE la BD.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { EMPRESA, MYSQL, sql, log } from './_lib.mjs';
import { AQUI, TABLAS, snap } from './_estado.mjs';

const estado = process.argv[2];
if (!/^E\d+[a-z]?$/.test(estado || '')) { console.error('uso: node seeds/seguridad/fijar.mjs E0|E2a|E6c'); process.exit(2); }
const DUMP = MYSQL.replace(/mysql\.exe$/i, 'mysqldump.exe');
const dir = path.join(AQUI, 'estados');
fs.mkdirSync(dir, { recursive: true });
const t0 = Date.now();

const contar = () => Object.fromEntries(sql(TABLAS.map(([t, , w]) => `SELECT '${t}', COUNT(*) FROM ${t} WHERE ${w}`).join(' UNION ALL ')).map(([t, n]) => [t, +n]));
// la auditoría del API se escribe DESPUÉS de responder, en lotes cada 2 s (FLUSH_INTERVAL_MS de
// audit-buffer.service.ts): la ventana de «quieto» tiene que ser MÁS larga que ese intervalo, o se fija
// un estado sin los eventos del último lote (pasó con E2a: 671 en vez de 800).
const quieto = () => { for (let i = 0; i < 20; i++) { const a = JSON.stringify(contar()); Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 2600); if (JSON.stringify(contar()) === a) return a; } throw new Error('la BD no se queda quieta'); };
const grupos = new Map(); // where → tablas (mysqldump admite un solo --where por invocación)
for (const [t, , w] of TABLAS) grupos.set(w, [...(grupos.get(w) ?? []), t]);
let dump, conteos;
for (let intento = 1; ; intento++) {
  const antes = quieto();
  dump = '';
  for (const [w, tablas] of grupos) {
    dump += execFileSync(DUMP, [
      '-h', '127.0.0.1', '-u', 'root', '--default-character-set=utf8mb4',
      '--no-create-info', '--complete-insert', '--skip-triggers', '--compact', '--skip-tz-utc',
      '--hex-blob', '--single-transaction', '--set-gtid-purged=OFF', `--where=${w}`, 'germiva', ...tablas,
    ], { encoding: 'utf8', maxBuffer: 512 * 1024 * 1024 }) + '\n';
  }
  if (JSON.stringify(contar()) === antes) { conteos = JSON.parse(antes); break; }
  if (intento === 3) throw new Error('los conteos cambiaron durante el volcado 3 veces');
}
for (const [t] of TABLAS) dump = dump.split(`INSERT INTO \`${t}\` `).join(`INSERT INTO \`${snap(t)}\` `);
fs.writeFileSync(path.join(dir, `${estado}.sql`), dump);
const [[ahora]] = sql(`SELECT NOW()`);
fs.writeFileSync(path.join(dir, `${estado}.json`), JSON.stringify({ estado, empresa: EMPRESA, fijado_en: ahora, conteos }, null, 2));
log(`${estado} fijado en ${((Date.now() - t0) / 1000).toFixed(1)} s →`, JSON.stringify(conteos));
