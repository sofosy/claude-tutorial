// node seeds/crm/sembrar.mjs
// Datos de demo de las series CRM · Éxito del Cliente · Mesa de Ayuda, sobre la empresa demo
// «Distribuidora Las Palmas SRL» (50, la de la serie Seguridad). Todo por API y con la sesión de
// quien lo haría en la vida real (Rosa, administradora; Ana, vendedora). Las fechas son relativas
// a HOY: los seguimientos «para hoy» y «vencidos» siempre lo son (R13).
//
// No toca filas que ya existían antes de la marca de agua `estados/M0.json`: los clientes que usa
// (Constructora Mirador, Ferretería Doña Luz, Inversiones Barahona, Colmado La Esquina) se
// REFERENCIAN, no se editan. `restaurar.mjs` borra lo sembrado y vuelve a llamar a este script.
import fs from 'node:fs';
import path from 'node:path';
import { api, log, uno, EMPRESA, leerJson } from '../seguridad/_lib.mjs';

const AQUI = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, '$1'));
const IDS = leerJson(path.join(AQUI, '..', 'seguridad', 'ids.json'), {});
const ROSA = 'rosa.almanzar', ANA = 'ana.mejia';
const U = IDS.usuarios;
const C = IDS.clientes;
if (!U || !C) throw new Error('falta seeds/seguridad/ids.json');
if (+uno(`SELECT COUNT(*) FROM leads WHERE company_id=${EMPRESA} AND deleted_at IS NULL`) > 0) {
  console.error('la empresa ya tiene prospectos: node seeds/crm/restaurar.mjs'); process.exit(1);
}

const dia = (d, h = 10, m = 0) => {
  const x = new Date(); x.setDate(x.getDate() + d); x.setHours(h, m, 0, 0);
  const p = n => String(n).padStart(2, '0');
  return `${x.getFullYear()}-${p(x.getMonth() + 1)}-${p(x.getDate())}T${p(h)}:${p(m)}:00-04:00`;
};
const fecha = d => dia(d).slice(0, 10);

const stages = await api(ROSA, 'GET', 'v1/pipeline-stages/all');
const st = Object.fromEntries(stages.map(s => [s.name, s.id]));
const [ws] = await api(ROSA, 'GET', 'v1/crm-workspaces');

// ── Etiquetas ──
const tags = {};
for (const [name, color] of [['Constructora', '#f59e0b'], ['Hotelería', '#06b6d4'], ['Volumen alto', '#10b981'], ['Educación', '#8b5cf6']]) {
  tags[name] = (await api(ROSA, 'POST', 'v1/lead-tags', { name, color })).id;
}

// ── Prospectos ──
const LEADS = [
  { firstName: 'Ramón', lastName: 'Peralta', companyName: 'Constructora Peralta & Asociados', jobTitle: 'Gerente de compras', phone: '8095550171', email: 'rperalta@peralta.ejemplo.com', source: 'website', priority: 'high', estimatedValue: 450000, stage: 'Nuevo', user: ROSA, tags: ['Constructora', 'Volumen alto'], seguimiento: [0, 15, 'Llamar para confirmar la cotización de varillas'] },
  { firstName: 'Yesenia', lastName: 'Durán', companyName: 'Hotel Playa Dorada', jobTitle: 'Encargada de mantenimiento', phone: '8095550172', email: 'compras@playadorada.ejemplo.com', source: 'referral', priority: 'medium', estimatedValue: 320000, stage: 'Nuevo', user: ROSA, tags: ['Hotelería'] },
  { firstName: 'Félix', lastName: 'Almonte', companyName: 'Ferretería Almonte', phone: '8095550173', source: 'phone_call', priority: 'low', estimatedValue: 85000, stage: 'Nuevo', user: null },
  { firstName: 'Carolina', lastName: 'Méndez', companyName: 'Residencial Las Colinas', jobTitle: 'Administradora', phone: '8095550174', email: 'cmendez@lascolinas.ejemplo.com', source: 'social_media', priority: 'high', estimatedValue: 600000, stage: 'Contactado', user: ROSA, tags: ['Constructora'], seguimiento: [-1, 11, 'Enviar catálogo de pinturas y precios por galón'] },
  { firstName: 'Luis', lastName: 'Ventura', companyName: 'Taller Ventura', phone: '8095550175', source: 'trade_show', priority: 'medium', estimatedValue: 60000, stage: 'Contactado', user: ANA },
  { firstName: 'Gisela', lastName: 'Rosario', companyName: 'Colegio San Marcos', jobTitle: 'Directora administrativa', phone: '8095550176', email: 'grosario@sanmarcos.ejemplo.com', source: 'email_campaign', priority: 'medium', estimatedValue: 150000, stage: 'Calificado', user: ROSA, tags: ['Educación'], seguimiento: [2, 9, 'Visita para medir los baños del segundo piso'] },
  { firstName: 'Manuel', lastName: 'Tejada', companyName: 'Agroindustrial Tejada', phone: '8095550177', source: 'referral', priority: 'high', estimatedValue: 280000, stage: 'Contactado', user: ROSA, tags: ['Volumen alto'], moverA: 'Propuesta' },
  { firstName: 'Patricia', lastName: 'Gómez', companyName: 'Plaza Comercial Bella Vista', phone: '8095550178', source: 'advertising', priority: 'low', estimatedValue: 120000, stage: 'Propuesta', user: ANA },
];
const leads = {};
for (const l of LEADS) {
  const creado = await api(ROSA, 'POST', 'v1/leads', {
    firstName: l.firstName, lastName: l.lastName, companyName: l.companyName, jobTitle: l.jobTitle,
    phone: l.phone, email: l.email, source: l.source, priority: l.priority, estimatedValue: l.estimatedValue,
    stageId: st[l.stage], workspace: ws.id, assignedUser: l.user ? U[l.user] : undefined,
    expectedCloseDate: fecha(30),
  });
  leads[`${l.firstName} ${l.lastName}`] = creado.id;
  if (l.tags) await api(ROSA, 'PATCH', `v1/leads/${creado.id}/tags`, { tagIds: l.tags.map(t => tags[t]) });
  await api(ROSA, 'POST', `v1/leads/${creado.id}/activities`, {
    leadId: creado.id, activityType: 'CALL', completedAt: dia(-3, 16),
    description: `Primer contacto con ${l.firstName}: con interés en materiales para ${l.companyName}.`,
  });
  // Llega a su columna MOVIÉNDOSE, como en el tablero: Propuesta convierte y nace la oportunidad.
  if (l.moverA) await api(ROSA, 'PATCH', `v1/leads/${creado.id}/move`, { stageId: st[l.moverA] });
  if (l.seguimiento) {
    const [d, h, texto] = l.seguimiento;
    await api(ROSA, 'POST', `v1/leads/${creado.id}/activities`, {
      leadId: creado.id, activityType: 'FOLLOW_UP', scheduledAt: dia(d, h), description: texto,
    });
  }
}
log(`prospectos: ${Object.keys(leads).length}`);

// ── Oportunidades ──
const OPS = [
  { name: 'Suministro de cemento y varillas — Torre Mirador', partner: C['Constructora Mirador'], amount: 1250000, stage: 'proposal', probability: 60, priority: 'high', type: 'new_business' },
  { name: 'Reposición mensual de herramientas', partner: C['Colmado La Esquina'], amount: 180000, stage: 'negotiation', probability: 75, priority: 'medium', type: 'existing_business' },
  { name: 'Equipamiento eléctrico — Plaza Barahona', partner: C['Inversiones Barahona'], amount: 540000, stage: 'qualification', probability: 30, priority: 'medium', type: 'new_business' },
  { name: 'Pinturas para remodelación del local', partner: C['Ferretería Doña Luz'], amount: 95000, stage: 'prospecting', probability: 15, priority: 'low', type: 'up_sell' },
  { name: 'Contrato anual de suministro de plomería', partner: C['Ferretería Doña Luz'], amount: 360000, stage: 'negotiation', probability: 80, priority: 'high', type: 'new_business' },
];
const ops = {};
for (const o of OPS) {
  const creada = await api(ROSA, 'POST', 'v1/opportunities', {
    ...o, expectedCloseDate: fecha(20), assignedUser: U[ROSA], workspace: ws.id,
  });
  ops[o.name] = creada.id;
}
log(`oportunidades: ${Object.keys(ops).length}`);

// ── Éxito del Cliente ──
// Un cliente llega por el camino real: se gana la oportunidad y pasa con su bienvenida.
const ganada = ops['Contrato anual de suministro de plomería'];
await api(ROSA, 'POST', `v1/opportunities/${ganada}/close-won`, {
  accountManagerId: U[ROSA], createOnboarding: true, createTicket: false, createProject: false,
  note: 'Compra mensual de plomería para sus tres sucursales. Prefieren entregas los martes.',
});
// Dos clientes de siempre se incorporan a mano, con su gerente de cuenta.
for (const nombre of ['Constructora Mirador', 'Inversiones Barahona']) {
  await api(ROSA, 'POST', `v1/customer-care/customers/${C[nombre]}/enroll`);
  await api(ROSA, 'PATCH', `v1/customer-care/customers/${C[nombre]}/profile`, { accountManagerId: U[ROSA] });
}
await api(ROSA, 'POST', `v1/customer-care/customers/${C['Constructora Mirador']}/follow-ups`, {
  type: 'call', performedAt: dia(-5, 10), note: 'Revisamos el avance de la obra; necesitarán más varillas en dos semanas.',
  nextActionAt: dia(0, 14), nextActionSubject: 'Confirmar fecha de la próxima entrega',
});
await api(ROSA, 'POST', `v1/customer-care/customers/${C['Inversiones Barahona']}/follow-ups`, {
  type: 'visit', performedAt: dia(-40, 9), note: 'Visita a la plaza: conformes con el servicio.',
  nextActionAt: dia(-2, 10), nextActionSubject: 'Llamar para la renovación del contrato',
});
// Un contrato activo que vence pronto: alimenta «Renovaciones».
await api(ROSA, 'POST', 'v1/sales-contracts', {
  contractNumber: 'CTR-2026-014', title: 'Suministro eléctrico — Plaza Barahona', type: 'product_supply',
  status: 'active', startDate: fecha(-320), endDate: fecha(45), totalValue: 480000, currency: 'DOP',
  renewalType: 'notification', renewalPeriodMonths: 12, renewalNotificationDays: 60, signedDate: fecha(-325),
  client: C['Inversiones Barahona'], accountManager: U[ROSA],
});
await api(ROSA, 'POST', 'v1/customer-care/health/recalculate');
log('éxito del cliente: 3 clientes, 1 contrato por renovar');

// ── Mesa de Ayuda ──
const TICKETS = [
  { subject: 'Factura con ITBIS mal calculado', description: 'La factura de la semana pasada cobra ITBIS sobre el flete. Piden nota de crédito.', type: 'BILLING_INQUIRY', priority: 'HIGH', source: 'PHONE', customer: 'Ferretería Doña Luz', asignar: ROSA },
  { subject: 'Entrega incompleta del pedido de varillas', description: 'Llegaron 80 de las 120 varillas de 3/8. La obra se detiene el jueves si no llegan.', type: 'ORDER_ISSUE', priority: 'URGENT', source: 'CHAT', customer: 'Constructora Mirador', asignar: ROSA, estado: 'IN_PROGRESS' },
  { subject: 'Devolución de taladro defectuoso', description: 'El taladro percutor no enciende desde el primer día. Tienen la factura.', type: 'REFUND_REQUEST', priority: 'NORMAL', source: 'IN_PERSON', customer: 'Colmado La Esquina', asignar: null },
  { subject: 'Cambio de dirección de entrega', description: 'A partir del lunes las entregas van a la sucursal de la avenida Duarte.', type: 'ACCOUNT_ISSUE', priority: 'LOW', source: 'EMAIL', customer: 'Ferretería Doña Luz', asignar: ANA, estado: 'WAITING_CUSTOMER' },
  { subject: 'Consulta de precios por volumen', description: '¿Qué descuento aplica comprando más de 500 sacos de cemento al mes?', type: 'PRODUCT_INQUIRY', priority: 'LOW', source: 'EMAIL', customer: 'Inversiones Barahona', asignar: ROSA, estado: 'RESOLVED', resolucion: 'Se envió la escala de descuentos por volumen: 4 % desde 500 sacos y 6 % desde 1.000.' },
];
for (const t of TICKETS) {
  const caso = await api(ROSA, 'POST', 'v1/helpdesk/tickets', {
    subject: t.subject, description: `<p>${t.description}</p>`, type: t.type, priority: t.priority,
    source: t.source, customerId: C[t.customer], assignedToUser: t.asignar ? U[t.asignar] : undefined,
  });
  const id = caso.id ?? caso.ticket?.id;
  if (t.estado) await api(ROSA, 'PATCH', `v1/helpdesk/tickets/${id}/status`, { status: t.estado, resolution: t.resolucion });
}
log(`mesa de ayuda: ${TICKETS.length} casos`);
fs.writeFileSync(path.join(AQUI, 'ids.json'), JSON.stringify({ leads, ops, tags, sembrado: new Date().toISOString() }, null, 2));
log('✓ siembra terminada');
