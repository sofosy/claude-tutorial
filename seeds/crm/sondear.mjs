// Foto rápida del estado CRM / Éxito / Mesa de Ayuda de la empresa demo.
import { api, log } from '../seguridad/_lib.mjs';

const U = 'rosa.almanzar';
const q = async (ruta) => {
  try { return await api(U, 'GET', ruta); } catch (e) { return `ERR ${e.message.slice(0, 200)}`; }
};
const corto = (x) => JSON.stringify(x).slice(0, 700);

log('workspaces', corto(await q('v1/crm-workspaces')));
log('stages', corto(await q('v1/pipeline-stages/all')));
log('leads', corto(await q('v1/leads?page=1&limit=3')));
log('opps', corto(await q('v1/opportunities?page=1&limit=3')));
log('cc settings', corto(await q('v1/customer-care/settings')));
log('cc summary', corto(await q('v1/customer-care/summary')));
log('hd workspaces', corto(await q('v1/helpdesk/workspaces')));
log('hd statuses', corto(await q('v1/helpdesk/statuses')));
log('tickets', corto(await q('v1/helpdesk/tickets?page=1&limit=3')));
log('lead-tags', corto(await q('v1/lead-tags')));
