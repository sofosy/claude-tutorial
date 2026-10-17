// node seeds/cajas/con-cerrojo.mjs "ENSAYO cajas-08-cobro-factura" -- node seeds/cajas/ensayo-v8.mjs
// (autor video 8, 2026-09-23) Ensayo del video 8 con restauración antes y después:
//   restaurar S8 (deja el plan 15) → ensayar.py → restaurar S8 → plan-s8 off (S0…S6 esperan el plan 2).
// Log completo en salida/cajas-08-cobro-factura/ensayo/ensayo.log. Sale con el código de ensayar.py.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { AQUI } from './_lib.mjs';

const RAIZ = path.join(AQUI, '..', '..');
const DIR = path.join(RAIZ, 'salida', 'cajas-08-cobro-factura', 'ensayo');
fs.mkdirSync(DIR, { recursive: true });
const run = (cmd, args, opts = {}) => spawnSync(cmd, args, { cwd: RAIZ, encoding: 'utf8', ...opts });
const node = (...a) => { const r = run('node', [path.join(AQUI, a[0]), ...a.slice(1)]); process.stdout.write(r.stdout + r.stderr); if (r.status) throw new Error(`${a.join(' ')} falló`); };

let codigo = 1;
try {
  node('restaurar.mjs', 'S8');
  node('plan-s8.mjs', 'ver');
  const r = run(path.join(RAIZ, '.venv', 'Scripts', 'python.exe'), ['seeds/_puertas/ensayar.py', 'cajas-08-cobro-factura', ...process.argv.slice(2)], { maxBuffer: 64 * 1024 * 1024 });
  fs.writeFileSync(path.join(DIR, 'ensayo.log'), r.stdout + r.stderr);
  process.stdout.write(r.stdout + r.stderr);
  codigo = r.status ?? 1;
} finally {
  node('restaurar.mjs', 'S8');
  node('plan-s8.mjs', 'off');
}
process.exit(codigo);
