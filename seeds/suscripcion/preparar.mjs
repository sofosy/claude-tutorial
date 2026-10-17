#!/usr/bin/env node
/**
 * Deja una empresa de demo EN PRUEBA para grabar los videos de suscripción
 * (cambiar de plan y pagar).
 *
 *   node seeds/suscripcion/preparar.mjs [--plan ERP_EMPRESARIAL] [--ciclo MONTHLY]
 *
 * 1. Libera lo de la toma anterior con seeds/registro/restaurar.mjs (mismo
 *    correo, mismo RNC ficticio, mismos planes publicados).
 * 2. Da de alta la empresa por /auth/dev/register, que en local también
 *    verifica el correo y corre la configuración inicial: queda igual que una
 *    empresa recién registrada desde la pantalla.
 * 3. Marca como visto el modal «Configuración incompleta» (R18): no es el tema
 *    de estos videos y taparía la primera pantalla.
 *
 * /auth/dev/register admite UNA llamada por minuto: si responde 429, espera.
 */
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const API = process.env.TUT_API ?? 'http://localhost:3001/api';
const MYSQL = process.env.TUT_MYSQL ?? 'C:/Program Files/MySQL/MySQL Server 9.7/bin/mysql.exe';
const CNF = process.env.TUT_MY_CNF ?? join(tmpdir(), 'claude', 'tut-my.cnf');
const AQUI = dirname(fileURLToPath(import.meta.url));

const arg = (n, d) => { const i = process.argv.indexOf(`--${n}`); return i > 0 ? process.argv[i + 1] : d; };
const PLAN = arg('plan', 'ERP_EMPRESARIAL');
const CICLO = arg('ciclo', 'MONTHLY');

const sql = (q) => execFileSync(MYSQL, [`--defaults-extra-file=${CNF}`, '--default-character-set=utf8mb4', 'germiva', '-N', '-e', q], { encoding: 'utf8' }).trim();

execFileSync(process.execPath, [join(AQUI, '..', 'registro', 'restaurar.mjs')], { stdio: 'inherit' });

const planId = Number(sql(`SELECT id FROM plans WHERE code='${PLAN}' AND deleted_at IS NULL`));
const cuerpo = {
  email: 'ana.martinez@ferreteriaelfaro.do',
  password: 'Faro2026!',
  name: 'Ana',
  lastName: 'Martínez',
  phones: ['8095550142'],
  legalName: 'FERRETERIA EL FARO SRL',
  tradeName: 'Ferretería El Faro',
  rnc: '130555099',
  selectedPlanId: planId,
  selectedBillingCycle: CICLO,
};

let r;
for (let intento = 1; intento <= 3; intento++) {
  r = await fetch(`${API}/auth/dev/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify(cuerpo),
  });
  if (r.status !== 429) break;
  console.log('dev/register limitado (1/min): espero 62 s');
  await new Promise((ok) => setTimeout(ok, 62000));
}
const json = await r.json().catch(() => ({}));
if (!r.ok) {
  console.error('ERROR alta:', r.status, JSON.stringify(json).slice(0, 400));
  process.exit(1);
}

const usuario = sql(`SELECT id FROM users WHERE email='${cuerpo.email}' AND deleted_at IS NULL ORDER BY id DESC LIMIT 1`);
const empresa = sql(`SELECT company_id FROM users WHERE id=${usuario}`);
sql(`UPDATE users SET emailVerified=1 WHERE id=${usuario}`);
const tablaPref = sql("SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='germiva' AND TABLE_NAME='user_company_preferences' AND COLUMN_NAME='incomplete_config_notice_seen_at'");
if (tablaPref === '1') {
  const hay = sql(`SELECT COUNT(*) FROM user_company_preferences WHERE user_id=${usuario} AND company_id=${empresa}`);
  if (hay === '0') {
    sql(`INSERT INTO user_company_preferences (user_id, company_id, incomplete_config_notice_seen_at) VALUES (${usuario}, ${empresa}, NOW())`);
  } else {
    sql(`UPDATE user_company_preferences SET incomplete_config_notice_seen_at=NOW() WHERE user_id=${usuario} AND company_id=${empresa}`);
  }
}
// --activa: la prueba se paga por transferencia y el equipo la aprueba, igual
// que en la vida real (lo que enseña el video de pagar). Deja la suscripción
// ACTIVA, con su pago en el historial y sin cambios pendientes.
if (process.argv.includes('--activa')) {
  const login = async (username, password) => {
    const res = await fetch(`${API}/auth/dev/login`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }),
    });
    return (await res.json()).accessToken;
  };
  const tokenAna = await login(cuerpo.email, cuerpo.password);
  const form = new FormData();
  const { readFileSync } = await import('node:fs');
  form.append('file', new Blob([readFileSync(join(AQUI, 'comprobante-transferencia.png'))], { type: 'image/png' }), 'comprobante-transferencia.png');
  form.append('bankName', 'Banco de mi empresa');
  form.append('referenceNumber', 'TRF-00458213');
  const dec = await fetch(`${API}/v1/subscriptions/my-company/transfer-proof`, {
    method: 'POST', headers: { Authorization: `Bearer ${tokenAna}` }, body: form,
  });
  const decl = await dec.json();
  if (!dec.ok) { console.error('ERROR al declarar la transferencia:', dec.status, JSON.stringify(decl).slice(0, 300)); process.exit(1); }
  const tokenAdmin = await login('admin', 'admin');
  const pagoId = decl.paymentId ?? decl.id;
  const rev = await fetch(`${API}/v1/subscriptions/admin/transfer-proofs/${pagoId}/review`, {
    method: 'PATCH', headers: { Authorization: `Bearer ${tokenAdmin}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ approve: true }),
  });
  if (!rev.ok) { console.error('ERROR al aprobar:', rev.status, (await rev.text()).slice(0, 300)); process.exit(1); }
  console.log(`transferencia ${pagoId} declarada y aprobada`);
}

const sub = sql(`SELECT CONCAT(s.id,' ',s.status,' ',p.code,' ',s.billingCycle,' fin prueba ',IFNULL(s.trialEndDate,'-')) FROM subscriptions s JOIN plans p ON p.id=s.plan_id WHERE s.company_id=${empresa} AND s.deleted_at IS NULL ORDER BY s.id DESC LIMIT 1`);
console.log(`empresa ${empresa} · usuario ${usuario} · suscripción ${sub}`);
