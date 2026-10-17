// node seeds/cajas/plan-s8.mjs on|off|ver   (autor video 8, 2026-09-23)
// Plan de la suscripción de la empresa demo 43 para el video 8 «Cobrar una factura en la caja».
//   on  → plan 15 «Empresarial» (ERP_ENTERPRISE, el que se PIDIÓ al crear la demo: _DATOS-CAJAS §0.1
//         «El selectedPlanId:15 se ignoró»). Trae el módulo SALES_CREDIT («Venta a Crédito»).
//   off → plan 2 «Emprendedor» (el que tiene la demo en S0…S6 y con el que se grabaron los videos 1–7).
// Por qué: con el plan 2, abrir CUALQUIER factura guardada lanza el diálogo «Módulo No Disponible — Su plan
// no incluye este módulo» (el formulario pide GET /v1/accounts-receivable/payment-history, permiso
// ACCOUNTS_RECEIVABLE_READ del módulo SALES_CREDIT, sin SKIP_PLAN_ALERT) → hallazgo H-17. El video no
// puede enseñar ese defecto como si fuera normal.
// S8 guarda la fila de `subscriptions` (modo 'solo-update' en _estado.mjs) → `restaurar.mjs S8` deja el
// plan 15. Los estados S0…S6 NO la guardan: después de ensayar o grabar el video 8, `plan-s8.mjs off`.
import { sql, log, EMPRESA } from './_lib.mjs';

const modo = process.argv[2];
const PLAN = { on: 15, off: 2 };
if (modo in PLAN) {
  sql(`UPDATE subscriptions SET plan_id=${PLAN[modo]} WHERE company_id=${EMPRESA} AND status IN ('TRIAL','ACTIVE')`);
} else if (modo !== 'ver') {
  console.error('uso: node plan-s8.mjs on|off|ver'); process.exit(2);
}
const [[id, plan, nombre]] = sql(`SELECT s.id, s.plan_id, p.name FROM subscriptions s JOIN plans p ON p.id=s.plan_id WHERE s.company_id=${EMPRESA} AND s.status IN ('TRIAL','ACTIVE') ORDER BY s.id DESC LIMIT 1`);
log(`empresa ${EMPRESA}: suscripción ${id} → plan ${plan} «${nombre}»`);
