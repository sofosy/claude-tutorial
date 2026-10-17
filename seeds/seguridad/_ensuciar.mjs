// node seeds/seguridad/_ensuciar.mjs
// Hace por API TODO lo que escriben los videos de la serie (02a…08g) para medir qué tablas tocan
// (_medir.mjs antes/después) y para probar que restaurar.mjs E0 lo deshace. NO usar mientras se graba
// (revoca las sesiones de los usuarios demo). Después: node seeds/seguridad/restaurar.mjs E0
import { api, uno, log, permisoId, leerJson, IDS, API } from './_lib.mjs';

const ids = leerJson(IDS, {});
const R = ids.roles, U = ids.usuarios;
const ROSA = 'rosa.almanzar';
const P = c => permisoId(c);

// 02a/02b · clonar, crear rol y dar permisos con alcance
const contador = +uno(`SELECT id FROM roles WHERE company_id IS NULL AND code='ACCOUNTANT'`);
const clon = await api(ROSA, 'POST', `role/${contador}/clone`, { name: 'Contador externo', description: 'x' });
const cob = await api(ROSA, 'POST', 'role', { name: 'Cobrador', description: 'Cobra facturas a domicilio' });
await api(ROSA, 'PATCH', `role/${cob.id}/permissions`, { grant: [{ permissionId: P('PARTNER_VIEW'), scope: 'OWN' }, { permissionId: P('INVOICE_VIEW'), scope: 'ALL' }] });
// 03 · rol hijo, exclusión y borrado
const hijo = await api(ROSA, 'POST', 'role', { name: 'Vendedor en práctica', description: 'x', parentRole: R.vendedor });
await api(ROSA, 'PATCH', `role/${hijo.id}/permissions`, { revoke: [P('QUOTE_CREATE')] });
await api(ROSA, 'DELETE', `role/${hijo.id}`);
// 04b · persona: crear, editar, rol, desactivar/activar, eliminar
const julio = await api(ROSA, 'POST', 'user', { username: 'julio.santana', email: 'julio.santana@germiva.demo', name: 'Julio', lastName: 'Santana', password: 'Demo2026!', active: true, roles: [R.vendedor] });
const jid = julio.id ?? julio.data?.id;
await api(ROSA, 'PATCH', `user/${jid}`, { password: 'Otra2026!' });
await api(ROSA, 'PATCH', `user/add-role/${jid}`, { roles: [R.almacen] });
await api(ROSA, 'PATCH', `user/${jid}`, { active: false });
await api(ROSA, 'PATCH', `user/${jid}`, { active: true });
await api(ROSA, 'DELETE', `user/${jid}`);
// 04c · equipo
const zn = await api(ROSA, 'POST', 'v1/team', { name: 'Zona Norte', description: 'Vendedores de Santiago y Puerto Plata' });
await api(ROSA, 'POST', `v1/team/${zn.id}/members`, { userIds: [U['carlos.pimentel'], U['hector.vargas']] });
await api(ROSA, 'DELETE', `v1/team/${zn.id}/members`, { userIds: [U['hector.vargas']] });
await api(ROSA, 'PATCH', `v1/team/${zn.id}`, { description: 'Santiago' });
await api(ROSA, 'DELETE', `v1/team/${zn.id}`);
// 06a/06b/06c · credenciales
const cr = await api(ROSA, 'POST', 'v1/integration-users', { integrationName: 'Programa del contador', integrationDescription: 'x' });
const cid = cr.user.id;
await api(ROSA, 'DELETE', `v1/integration-users/${cid}/permissions/PURCHASE_INVOICE_CREATE`);
const tl = await fetch(`${API}/auth/integration/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ apiKey: cr.credentials.apiKey, apiSecret: cr.credentials.apiSecret }) }).then(r => r.json());
const tok = tl.token ?? tl.data?.token;
for (const ruta of ['v1/invoices/sales', 'v1/product']) log('integración', ruta, (await fetch(`${API}/${ruta}`, { headers: { Authorization: `Bearer ${tok}` } })).status);
await api(ROSA, 'POST', `v1/integration-users/${cid}/permissions/PRODUCT_VIEW`);
await api(ROSA, 'POST', `v1/integration-users/${cid}/regenerate-credentials`);
await api(ROSA, 'PATCH', `v1/integration-users/${cid}/deactivate`);
await api(ROSA, 'PATCH', `v1/integration-users/${cid}/activate`);
await api(ROSA, 'DELETE', `v1/integration-users/${ids.credenciales.tienda.id}`);
// 08d/08f/08g · alcance, herencia y cambio en vivo sobre Vendedor
await api(ROSA, 'PATCH', `role/${R.vendedor}/permissions`, { rescope: [{ permissionId: P('QUOTE_VIEW'), scope: 'TEAM' }], grant: [{ permissionId: P('PARTNER_CREATE') }], revoke: [P('PRODUCT_VIEW')] });
await api(ROSA, 'PATCH', `role/${R.senior}/permissions`, { revoke: [P('PARTNER_CREATE')] });
// 08e · Carlos aprueba Q1
await api('carlos.pimentel', 'PATCH', `v1/quotes/approve/${ids.cotizaciones.Q1.numero}`, {});
// sesiones de todos (entradas en cámara)
for (const u of ['ana.mejia', 'pedro.nunez', 'marta.guzman', 'carlos.pimentel']) await api(u, 'GET', 'v1/quotes?page=1&limit=5', undefined, { permitir: [403] });
log('✓ ensuciado (restaurar con: node seeds/seguridad/restaurar.mjs E0)');
