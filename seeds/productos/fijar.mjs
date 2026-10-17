// node seeds/productos/fijar.mjs — vuelca la base ENTERA como canon de la serie Productos v3.
// Correr con la base en reposo (nadie grabando ni ensayando).
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import { DUMP, CANON, log } from './_lib.mjs';

const t0 = Date.now();
execFileSync(DUMP, ['-u', 'root', '--single-transaction', '--routines', '--triggers', '--events', '--hex-blob',
  '--set-gtid-purged=OFF', '--default-character-set=utf8mb4', `--result-file=${CANON}`, 'germiva'], { stdio: 'inherit' });
log(`canon: ${(fs.statSync(CANON).size / 1048576).toFixed(0)} MB en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
