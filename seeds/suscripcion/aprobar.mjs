#!/usr/bin/env node
/**
 * Aprueba, como el equipo de Germiva, el comprobante de transferencia que la
 * empresa de demo acaba de subir en el video.
 *
 *   node seeds/suscripcion/aprobar.mjs
 *
 * Es lo que en la vida real hace una persona desde la bandeja de
 * transferencias (normalmente el mismo día hábil). El video lo corre como
 * `setup` del paso que enseña la suscripción ya activa.
 */
const API = process.env.TUT_API ?? 'http://localhost:3001/api';

const login = async (username, password) => {
  const r = await fetch(`${API}/auth/dev/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }),
  });
  return (await r.json()).accessToken;
};

const admin = await login('admin', 'admin');
const pend = await (await fetch(`${API}/v1/subscriptions/admin/transfer-proofs/pending`, {
  headers: { Authorization: `Bearer ${admin}` },
})).json();
const mio = (Array.isArray(pend) ? pend : []).find((p) => /ferreteria-el-faro|ana\.martinez@ferreteriaelfaro/i.test(JSON.stringify(p)));
if (!mio) {
  console.error('ERROR: no hay comprobante pendiente de la demo');
  process.exit(1);
}
const r = await fetch(`${API}/v1/subscriptions/admin/transfer-proofs/${mio.paymentId}/review`, {
  method: 'PATCH', headers: { Authorization: `Bearer ${admin}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ approve: true }),
});
if (!r.ok) {
  console.error('ERROR al aprobar:', r.status, (await r.text()).slice(0, 300));
  process.exit(1);
}
console.log(`comprobante ${mio.paymentId} aprobado (RD$${mio.amount})`);
