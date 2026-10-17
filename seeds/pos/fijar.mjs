// node seeds/pos/fijar.mjs <P#>   (copia de cajas/fijar.mjs con la lista de tablas de pos/_estado.mjs)
// Fija el estado ACTUAL de la empresa demo (43) como canon del estado S#: vuelca con mysqldump las
// filas company_id=43 de las tablas de _estado.mjs a estados/<S#>.sql (renombradas a snap_<tabla>)
// y guarda la marca de agua de audit_logs y la hora de fijado en estados/<S#>.json.
// Solo LEE la BD. No toca ninguna otra empresa.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { EMPRESA, MYSQL, sql, log } from '../cajas/_lib.mjs';
import { AQUI } from './_estado.mjs';
import { TABLAS, W, snap } from './_estado.mjs';

const estado = process.argv[2];
if (!/^P\d+[a-z]?$/.test(estado || '')) { console.error('uso: node seeds/pos/fijar.mjs P0|P1|…'); process.exit(2); }
const DUMP = MYSQL.replace(/mysql\.exe$/i, 'mysqldump.exe');
const dir = path.join(AQUI, 'estados');
fs.mkdirSync(dir, { recursive: true });
const t0 = Date.now();

const volcar = TABLAS.filter(([, m]) => m !== 'marca').map(([t]) => t);
const contar = () => Object.fromEntries(sql(TABLAS.map(([t]) => `SELECT '${t}', COUNT(*) FROM ${t} WHERE ${W}`).join(' UNION ALL ')).map(([t, n]) => [t, +n]));
// La auditoría del API se escribe DESPUÉS de responder: se espera a que los conteos se queden
// quietos antes y después del volcado (si no, el canon pierde la última fila y restaurar lo detecta).
const quieto = () => { for (let i = 0; i < 20; i++) { const a = JSON.stringify(contar()); Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 700); if (JSON.stringify(contar()) === a) return a; } throw new Error('la BD no se queda quieta'); };
let dump, conteos;
for (let intento = 1; ; intento++) {
  const antes = quieto();
  dump = execFileSync(DUMP, [
    '-h', '127.0.0.1', '-u', 'root', '--default-character-set=utf8mb4',
    '--no-create-info', '--complete-insert', '--skip-triggers', '--compact', '--skip-tz-utc',
    '--hex-blob', '--single-transaction', '--set-gtid-purged=OFF', `--where=${W}`, 'germiva', ...volcar,
  ], { encoding: 'utf8', maxBuffer: 512 * 1024 * 1024 });
  if (JSON.stringify(contar()) === antes) { conteos = JSON.parse(antes); break; }
  if (intento === 3) throw new Error('los conteos cambiaron durante el volcado 3 veces');
}
for (const t of volcar) dump = dump.split(`INSERT INTO \`${t}\` `).join(`INSERT INTO \`${snap(t)}\` `);
fs.writeFileSync(path.join(dir, `${estado}.sql`), dump);

const [[marca, ahora]] = sql(`SELECT IFNULL(MAX(id),0), NOW() FROM audit_logs`);
const meta = { estado, empresa: EMPRESA, fijado_en: ahora, marca_audit_logs: +marca, conteos };
fs.writeFileSync(path.join(dir, `${estado}.json`), JSON.stringify(meta, null, 2));
log(`${estado} fijado en ${((Date.now() - t0) / 1000).toFixed(1)} s →`, JSON.stringify(conteos));
