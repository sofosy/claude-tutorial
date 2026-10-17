// node seeds/cajas/con-cerrojo.mjs "<etiqueta>" -- <comando> [args…]   (autor video 8, 2026-09-23)
// Toma seeds/_puertas/NAVEGADOR.lock en modo exclusivo (espera sondeando cada 20 s si lo tiene otro),
// ejecuta el comando con este proceso VIVO como dueño y suelta el cerrojo SOLO si su contenido sigue
// siendo el propio (R27). Sale con el código del comando.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { AQUI } from './_lib.mjs';

const LOCK = path.join(AQUI, '..', '_puertas', 'NAVEGADOR.lock');
const sep = process.argv.indexOf('--');
const etiqueta = process.argv[2];
if (!etiqueta || sep < 0 || sep === process.argv.length - 1) { console.error('uso: con-cerrojo.mjs "<etiqueta>" -- cmd args…'); process.exit(2); }
const [cmd, ...args] = process.argv.slice(sep + 1);
const mio = `${etiqueta} ${process.pid} ${new Date().toISOString()}`;
const dormir = ms => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

for (let avisado = false; ;) {
  try { const fd = fs.openSync(LOCK, 'wx'); fs.writeSync(fd, mio); fs.closeSync(fd); break; }
  catch (e) {
    if (e.code !== 'EEXIST') throw e;
    if (!avisado) { let c = ''; try { c = fs.readFileSync(LOCK, 'utf8'); } catch {} console.log(`[cerrojo] ocupado por «${c.trim()}», espero…`); avisado = true; }
    dormir(20000);
  }
}
console.log(`[cerrojo] tomado: ${mio}`);
let codigo = 1;
try {
  const r = spawnSync(cmd, args, { stdio: 'inherit', shell: false });
  codigo = r.status ?? 1;
  if (r.error) console.error(r.error);
} finally {
  let c = ''; try { c = fs.readFileSync(LOCK, 'utf8'); } catch {}
  if (c === mio) { fs.unlinkSync(LOCK); console.log('[cerrojo] soltado'); }
  else console.log('[cerrojo] NO se suelta: el contenido ya no es el mío');
}
process.exit(codigo);
