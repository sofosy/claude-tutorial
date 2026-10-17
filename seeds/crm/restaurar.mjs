// node seeds/crm/restaurar.mjs [--sin-siembra]
// Devuelve la empresa demo al punto de partida de las series CRM · Éxito del Cliente · Mesa de Ayuda:
//   1. MARCA DE AGUA (estados/M0.json, medida con seeds/seguridad/_medir.mjs antes de sembrar nada):
//      en cada tabla con company_id, borra las filas de la empresa con id > el máximo de M0; en cada
//      tabla SIN company_id que haya crecido, borra id >= su AUTO_INCREMENT de M0 (hijas: etiquetas de
//      prospecto, adjuntos…) salvo las de sesión/cola, que no son de la demo.
//   2. CANON C0 (seeds/crm/_canon.mjs): devuelve las filas de configuración que los videos editan.
//   3. Vuelve a sembrar (sembrar.mjs), con fechas relativas a HOY.
// Sin binlog (R14) y con FOREIGN_KEY_CHECKS=0 dentro de la sesión.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { EMPRESA, sql, log } from './_lib.mjs';
import { AQUI } from './_estado.mjs';

const t0 = Date.now();
const M0 = JSON.parse(fs.readFileSync(path.join(AQUI, 'estados', 'M0.json'), 'utf8'));
const ahoraF = path.join(os.tmpdir(), `crm-medida-${process.pid}.json`);
execFileSync(process.execPath, [path.join(AQUI, '..', 'seguridad', '_medir.mjs'), ahoraF], { stdio: 'inherit' });
const AHORA = JSON.parse(fs.readFileSync(ahoraF, 'utf8'));
fs.unlinkSync(ahoraF);

// Tablas que NUNCA se tocan por marca de agua: identidad, sesiones, colas y contadores ajenos a la demo.
const INTOCABLES = /^(users|user_companies|user_company_roles|profiles|company_user_activity_daily|sys_sequences|migrations|companies|subscriptions)$|session|token|refresh|login|otp|auth|queue|job|lock|rate_limit|cache|permission/i;

let q = 'SET FOREIGN_KEY_CHECKS=0;\n';
const tocadas = [];
for (const [t, ahora] of Object.entries(AHORA)) {
  const antes = M0[t];
  if (antes === undefined || antes === ahora || INTOCABLES.test(t)) continue;
  if (ahora.startsWith('ai:')) {
    const ai0 = +antes.slice(3), ai1 = +ahora.slice(3);
    if (ai1 > ai0) { q += `DELETE FROM \`${t}\` WHERE id >= ${ai0};\n`; tocadas.push(t); }
    continue;
  }
  const max0 = +(antes.split('|')[2] || 0), max1 = +(ahora.split('|')[2] || 0);
  if (max1 > max0) { q += `DELETE FROM \`${t}\` WHERE company_id=${EMPRESA} AND id > ${max0};\n`; tocadas.push(t); }
}
q += 'SET FOREIGN_KEY_CHECKS=1;\n';
sql(q);
log(`marca de agua: ${tocadas.length} tablas limpiadas (${tocadas.join(', ')})`);

execFileSync(process.execPath, [path.join(AQUI, '_canon.mjs'), 'C0'], { stdio: 'inherit' });
if (!process.argv.includes('--sin-siembra')) {
  execFileSync(process.execPath, [path.join(AQUI, 'sembrar.mjs')], { stdio: 'inherit' });
}
log(`✓ restaurado en ${((Date.now() - t0) / 1000).toFixed(1)} s`);
