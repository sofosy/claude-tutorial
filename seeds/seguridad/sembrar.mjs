// node seeds/seguridad/sembrar.mjs
// Siembra la empresa demo de la serie «Seguridad» (plan: guiones/_SERIE-SEGURIDAD.md §2–§6):
// «Distribuidora Las Palmas SRL», RNC 130555036, administradora rosa.almanzar.
// IDEMPOTENTE: cada paso busca antes lo que ya existe (por RNC / nombre / username / código) y solo crea
// lo que falta. Todo por el API con los payloads del front y la SESIÓN DE QUIEN FIGURA COMO AUTOR
// (el alcance filtra por created_by_user_id). SQL solo para: lecturas, plan de la suscripción,
// fechas retrocedidas (Héctor, credencial vieja) y R18 (aviso «Configuración incompleta» visto).
// Escribe ids.json (con los secretos de las credenciales: demo local, fuera de git).
import fs from 'node:fs';
import path from 'node:path';
import {
  AQUI, API, CLAVE, RNC, DOMINIO, IDS, NAVEGADOR_UA, sql, uno, esc, empresa, login, api, permisoId, log, leerJson, espera,
} from './_lib.mjs';

const POS = path.join(AQUI, '..', 'pos');
const catalogo = JSON.parse(fs.readFileSync(path.join(POS, 'catalogo.json'), 'utf8'));
const ids = leerJson(IDS, {});
const ROSA = 'rosa.almanzar';
const guardar = () => fs.writeFileSync(IDS, JSON.stringify(ids, null, 2));

// ── 1. Alta de la empresa + administradora (POST auth/dev/register, A-063). Throttle 1/min.
let CIA = empresa();
if (!CIA) {
  const r = await fetch(`${API}/auth/dev/register`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: `rosa.almanzar@${DOMINIO}`, password: CLAVE, name: 'Rosa', lastName: 'Almánzar',
      phones: ['8095550188'], legalName: 'Distribuidora Las Palmas SRL', tradeName: 'Distribuidora Las Palmas',
      rnc: RNC, address: 'Calle Duarte 88, Villa Mella, Santo Domingo Norte', phone: '809-555-0188', selectedPlanId: 15,
    }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(`dev/register → ${r.status}: ${JSON.stringify(j).slice(0, 500)}`);
  CIA = empresa();
  log('empresa creada', CIA, 'usuario', j.userId);
}
ids.empresa = CIA;
// el registro usa el correo como username → se deja «rosa.almanzar» (Editar usuario)
const rosaId = +uno(`SELECT id FROM users WHERE email='rosa.almanzar@${DOMINIO}' AND deleted_at IS NULL`);
if (uno(`SELECT username FROM users WHERE id=${rosaId}`) !== ROSA) {
  const t = await login(`rosa.almanzar@${DOMINIO}`);
  const r = await fetch(`${API}/user/${rosaId}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${t}` }, body: JSON.stringify({ username: ROSA }) });
  if (!r.ok) throw new Error(`renombrar rosa → ${r.status} ${(await r.text()).slice(0, 300)}`);
  log('username → rosa.almanzar');
}

// ── 2. Plan 15 «Empresarial» (SALES_QUOTE, INVOICING, PRODUCTS, API_ACCESS): lo cambia la plataforma → SQL
sql(`UPDATE subscriptions SET plan_id=15 WHERE company_id=${CIA} AND plan_id<>15`);
log('plan', uno(`SELECT CONCAT(s.id,' plan ',s.plan_id,' ',s.status) FROM subscriptions s WHERE s.company_id=${CIA} ORDER BY id DESC LIMIT 1`));

// ── 3. La empresa exige aprobación de cotizaciones (Preferencias › Facturación)
if (uno(`SELECT quote_requires_approval FROM company_configs WHERE company_id=${CIA}`) !== '1') {
  await api(ROSA, 'POST', 'v1/company/config/upsert', { quoteRequiresApproval: true });
  log('quote_requires_approval → 1');
}

// ── 4. Catálogo del POS: categorías, productos + precio, existencias (creados por Rosa)
// DEFECTO ERP (D-ENT-1): ProductTypeService.create/update validan nombre+categoría SIN company_id →
// «Herramientas» da 409 porque ya la tiene la empresa 43. Se usan nombres propios de esta empresa.
const NOMBRE_CAT = { 'Herramientas': 'Herramientas de trabajo', 'Electricidad': 'Material eléctrico', 'Plomería': 'Plomería y agua',
  'Pintura': 'Pinturas', 'Construcción': 'Construcción y obra', 'Jardín': 'Jardinería' };
const tipos = {};
for (const base of catalogo.categorias) {
  const nombre = NOMBRE_CAT[base];
  let id = uno(`SELECT id FROM product_types WHERE company_id=${CIA} AND name='${esc(nombre)}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) id = (await api(ROSA, 'POST', 'product-types', { name: nombre, category: 'PRODUCT', description: `Artículos de ${nombre.toLowerCase()} de la distribuidora` })).id;
  tipos[base] = +id;
}
const DOP = +uno(`SELECT id FROM currencies WHERE code='DOP' LIMIT 1`);
const ITBIS18 = 1, EXENTO = 4;
for (const p of catalogo.productos) {
  const tax = p.exento ? EXENTO : ITBIS18;
  let id = uno(`SELECT id FROM products WHERE company_id=${CIA} AND code='${esc(p.sku)}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) {
    id = (await api(ROSA, 'POST', 'v1/product', {
      category: 'PRODUCT', name: p.nombre, code: p.sku, descriptionHtml: null,
      tax, purchaseTax: tax, managesInventory: true, usesExpirationDate: false, usesBatchControl: false,
      visibleInStore: false, purchasePrice: p.costo, productType: tipos[p.categoria], active: true,
      fiscalAttributes: {}, presumptiveTaxRegime: null,
    })).id;
    log('producto', p.sku, id);
  }
  p.id = +id;
  if (!uno(`SELECT id FROM prices WHERE product_id=${id} AND deleted_at IS NULL AND customerType='REGULAR' LIMIT 1`)) {
    await api(ROSA, 'POST', 'v1/price', { product: p.id, customerType: 'REGULAR', price: String(p.precio), taxIncluded: false, priority: 1, description: '', active: true, currency: DOP });
  }
  p.precioId = +uno(`SELECT id FROM prices WHERE product_id=${id} AND deleted_at IS NULL AND customerType='REGULAR' ORDER BY priority, id LIMIT 1`);
}
const UBIC = +uno(`SELECT l.id FROM inventory_location l JOIN warehouse w ON w.id=l.warehouse_id WHERE l.company_id=${CIA} AND w.isPrimary=1 AND l.deleted_at IS NULL ORDER BY l.id LIMIT 1`);
for (const p of catalogo.productos) {
  const actual = Number(uno(`SELECT IFNULL(SUM(quantity),0) FROM inventory WHERE product_id=${p.id} AND company_id=${CIA} AND deleted_at IS NULL`) ?? 0);
  if (actual === 0 && p.stock > 0 && !+uno(`SELECT COUNT(*) FROM inventory_movement m JOIN inventory i ON i.id=m.inventory_id WHERE i.product_id=${p.id}`)) {
    await api(ROSA, 'POST', 'v1/inventory/movement/entry', {
      product: p.id, batchNumber: `INI-${p.sku}`, quantity: p.stock, inventoryLocation: UBIC, order: 1,
      inventoryMovementType: 17, unitPrice: p.costo, notes: 'Saldo inicial de la distribuidora',
    });
  }
}
ids.productos = Object.fromEntries(catalogo.productos.map(p => [p.sku, p.id]));
ids.categorias = tipos;
log('catálogo listo:', catalogo.productos.length, 'productos');

// ── 4b. Fotos (como la pestaña «Imágenes»: POST v1/media/upload + POST v1/product/:id/media)
{
  const token = await login(ROSA);
  for (const p of catalogo.productos) {
    if (!p.slug) continue;
    if (uno(`SELECT pm.id FROM product_media pm WHERE pm.product_id=${p.id} AND pm.isPrimary=1 AND pm.deleted_at IS NULL LIMIT 1`)) continue;
    const archivo = path.join(POS, 'imagenes', `${p.slug}.jpg`);
    if (!fs.existsSync(archivo)) { log('✗ falta', archivo); continue; }
    const fd = new FormData();
    fd.append('file', new Blob([fs.readFileSync(archivo)], { type: 'image/jpeg' }), `${p.slug}.jpg`);
    const r = await fetch(`${API}/v1/media/upload`, { method: 'POST', headers: { Authorization: `Bearer ${token}` }, body: fd });
    const txt = await r.text();
    if (!r.ok) throw new Error(`upload ${p.sku} → ${r.status} ${txt.slice(0, 200)}`);
    const m = JSON.parse(txt);
    await api(ROSA, 'POST', `v1/product/${p.id}/media`, { media: [{ media: +(m.id ?? m.data?.id), isPrimary: true, sortOrder: 1 }] });
  }
  log('fotos:', uno(`SELECT COUNT(*) FROM product_media WHERE company_id=${CIA} AND isPrimary=1 AND deleted_at IS NULL`));
}

// ── 5. Clientes (RNC ficticios del plan: dígito DGII válido, ausentes de taxpayers)
const CLIENTES = [
  ['Constructora Mirador', 'Constructora Mirador SRL', '130555044'],
  ['Ferretería Doña Luz', 'Ferretería Doña Luz SRL', '130555052'],
  ['Inversiones Barahona', 'Inversiones Barahona SRL', '130555087'],
  ['Colmado La Esquina', 'Colmado La Esquina SRL', '130555095'],
];
ids.clientes = {};
for (const [nombre, legal, rnc] of CLIENTES) {
  if (+uno(`SELECT COUNT(*) FROM taxpayers WHERE rnc='${rnc}'`)) throw new Error(`${rnc} está en taxpayers`);
  let id = uno(`SELECT id FROM partners WHERE company_id=${CIA} AND name='${esc(nombre)}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) id = (await api(ROSA, 'POST', 'v1/partner', { name: nombre, legalName: legal, tin: rnc, documentType: 'RNC', partnerType: ['CUSTOMER'], customerType: 'REGULAR', partnerCategory: 'BUSINESS', ncfType: 1 })).id;
  ids.clientes[nombre] = +id;
}
ids.clientes['Consumidor Final'] = +uno(`SELECT id FROM partners WHERE company_id=${CIA} AND isInternalPartner=1 AND partnerType='CUSTOMER' LIMIT 1`);
guardar();

// ── 6. Roles de la empresa (§4). Permisos por el guardado en lote del editor (PATCH role/:id/permissions)
const V = 'ALL';
async function rol(nombre, descripcion, padre = null) {
  let id = uno(`SELECT id FROM roles WHERE company_id=${CIA} AND name='${esc(nombre)}' AND deleted_at IS NULL AND IFNULL(is_integration_role,0)=0 LIMIT 1`);
  if (!id) { id = (await api(ROSA, 'POST', 'role', { name: nombre, description: descripcion, parentRole: padre })).id; log('rol', nombre, id); }
  return +id;
}
async function conceder(rolId, lista) { // lista: [código, alcance?]
  // concedido (directo o heredado) → código ⇒ [alcance, origen]. Un heredado con otro alcance se
  // «rescope» (así lo hace el editor: cambiar el alcance lo vuelve DIRECTO, A-008); un grant sobre un
  // heredado no hace nada.
  const tiene = new Map(sql(`SELECT p.code, rp.scope, rp.source FROM role_permissions rp JOIN permission p ON p.id=rp.permission_id WHERE rp.role_id=${rolId}`).map(([c, s, o]) => [c, [s, o]]));
  const grant = [], rescope = [];
  for (const [code, scope] of lista) {
    const pid = permisoId(code);
    if (!tiene.has(code)) grant.push(scope ? { permissionId: pid, scope } : { permissionId: pid });
    else if (scope && (tiene.get(code)[0] !== scope || tiene.get(code)[1] !== 'DIRECT')) rescope.push({ permissionId: pid, scope });
  }
  if (grant.length || rescope.length) await api(ROSA, 'PATCH', `role/${rolId}/permissions`, { grant, rescope });
  return grant.length + rescope.length;
}
const R = {};
R.vendedor = await rol('Vendedor', 'Vende en la calle: cotiza a sus clientes y consulta el catálogo');
await conceder(R.vendedor, [['QUOTE_VIEW', 'OWN'], ['QUOTE_CREATE'], ['QUOTE_UPDATE'], ['PARTNER_VIEW', V], ['PRODUCT_VIEW', V]]);
R.senior = await rol('Vendedor sénior', 'Vendedor con experiencia: aprueba cotizaciones y las convierte en factura', R.vendedor);
await conceder(R.senior, [['QUOTE_VIEW', V], ['QUOTE_APPROVE'], ['QUOTE_REJECT'], ['QUOTE_ACCEPT'], ['QUOTE_CONVERT_DIRECTLY_TO_INVOICE'], ['INVOICE_VIEW', V], ['INVOICE_CREATE']]);
R.almacen = await rol('Almacén', 'Encargados del almacén: mantienen el catálogo y las existencias');
await conceder(R.almacen, [['PRODUCT_VIEW', V], ['PRODUCT_CREATE'], ['PRODUCT_UPDATE'], ['PRODUCT_IMPORT'], ['INVENTORY_VIEW', V]]);
R.auditor = await rol('Auditor (solo lectura)', 'Revisa todo sin poder cambiar nada');
await conceder(R.auditor, [['QUOTE_VIEW', V], ['INVOICE_VIEW', V], ['PRODUCT_VIEW', V], ['PARTNER_VIEW', V], ['USER_VIEW', V], ['TEAM_VIEW'], ['ROLE_VIEW', V], ['AUDIT_LOG_READ', V]]);
R.mensajero = await rol('Mensajero', 'Reparte pedidos a los clientes');
ids.roles = R;
ids.roles_sistema = Object.fromEntries(sql(`SELECT code, id FROM roles WHERE company_id IS NULL AND code IN ('ADMIN','ACCOUNTANT')`).map(([c, i]) => [c, +i]));
guardar();

// ── 7. Usuarios (§3) creados por Rosa (Nuevo › Usuario)
const PERSONAS = [
  ['ana.mejia', 'Ana', 'Mejía', [R.vendedor], true],
  ['jose.cabrera', 'José', 'Cabrera', [R.vendedor, R.almacen], true],
  ['carlos.pimentel', 'Carlos', 'Pimentel', [R.senior], true],
  ['pedro.nunez', 'Pedro', 'Núñez', [R.almacen], true],
  ['marta.guzman', 'Marta', 'Guzmán', [R.auditor], true],
  ['hector.vargas', 'Héctor', 'Vargas', [R.vendedor], true],
  ['luisa.feliz', 'Luisa', 'Féliz', [], true],
  ['sonia.reyes', 'Sonia', 'Reyes', [R.mensajero], false],
];
ids.usuarios = { [ROSA]: rosaId };
for (const [u, nombre, apellido, roles, activo] of PERSONAS) {
  let id = uno(`SELECT id FROM users WHERE username='${u}' AND deleted_at IS NULL LIMIT 1`);
  if (!id) {
    id = idDe(await api(ROSA, 'POST', 'user', { username: u, email: `${u}@${DOMINIO}`, name: nombre, lastName: apellido, password: CLAVE, active: activo, roles }));
    log('usuario', u, id);
  }
  ids.usuarios[u] = +id;
}
function idDe(o) { return o?.id ?? o?.data?.id ?? o?.user?.id; }
guardar();

// ── 8. Equipo «Zona Este» (Ana y José)
let zona = uno(`SELECT id FROM teams WHERE company_id=${CIA} AND name='Zona Este' AND deleted_at IS NULL LIMIT 1`);
if (!zona) zona = idDe(await api(ROSA, 'POST', 'v1/team', { name: 'Zona Este', description: 'Vendedores del este: Villa Mella y Los Alcarrizos' }));
const faltanEq = [ids.usuarios['ana.mejia'], ids.usuarios['jose.cabrera']].filter(u => !+uno(`SELECT COUNT(*) FROM team_members WHERE team_id=${zona} AND user_id=${u}`));
if (faltanEq.length) await api(ROSA, 'POST', `v1/team/${zona}/members`, { userIds: faltanEq });
ids.equipos = { 'Zona Este': +zona };
guardar();

// ── 9. Cotizaciones (§6), cada una con la sesión de su autor
const P = sku => catalogo.productos.find(p => p.sku === sku);
const hoy = new Date(); const ymd = d => d.toISOString().slice(0, 10);
const vence = ymd(new Date(hoy.getTime() + 30 * 864e5));
const COT = [
  ['Q1', 'ana.mejia', 'Constructora Mirador', [['FER-1001', 10], ['FER-1004', 5]], 'DRAFT'],
  ['Q2', 'ana.mejia', 'Colmado La Esquina', [['FER-2001', 12], ['FER-3001', 4]], 'DRAFT'],
  ['Q3', 'ana.mejia', 'Ferretería Doña Luz', [['FER-1002', 20], ['FER-4001', 6]], 'APPROVED'],
  ['Q4', 'jose.cabrera', 'Inversiones Barahona', [['FER-5001', 30], ['FER-5002', 15]], 'DRAFT'],
  ['Q5', 'jose.cabrera', 'Constructora Mirador', [['FER-1006', 2], ['FER-1003', 6]], 'ACCEPTED'],
  ['Q6', 'carlos.pimentel', 'Ferretería Doña Luz', [['FER-4002', 10], ['FER-4003', 10]], 'APPROVED'],
  ['Q7', 'carlos.pimentel', 'Inversiones Barahona', [['FER-6001', 8], ['FER-6002', 4]], 'DRAFT'],
  ['Q8', 'rosa.almanzar', 'Colmado La Esquina', [['FER-2002', 10], ['FER-3002', 5]], 'CANCELLED'],
];
ids.cotizaciones = ids.cotizaciones ?? {};
const estadoCot = n => uno(`SELECT s.code FROM quotes q JOIN quote_status s ON s.id=q.quote_status_id WHERE q.company_id=${CIA} AND q.invoice_number='${n}'`);
for (const [q, autor, cliente, lineas, meta] of COT) {
  let num = ids.cotizaciones[q]?.numero;
  if (!num || !uno(`SELECT id FROM quotes WHERE company_id=${CIA} AND invoice_number='${num}' AND deleted_at IS NULL`)) {
    const r = await api(autor, 'POST', 'v1/quotes', {
      partner: ids.clientes[cliente], expiryDate: vence, currency: DOP, quoteType: 'QUOTATION',
      details: lineas.map(([sku, qty]) => ({ product: P(sku).id, quantity: qty, priceId: P(sku).precioId })),
    });
    num = r.quoteNumber ?? r.data?.quoteNumber;
    ids.cotizaciones[q] = { numero: num, id: +(r.id ?? r.data?.id), autor, cliente };
    log('cotización', q, num, 'por', autor);
  }
  const est = estadoCot(num);
  if (meta === 'APPROVED' || meta === 'ACCEPTED') {
    if (est === 'DRAFT') await api('carlos.pimentel', 'PATCH', `v1/quotes/approve/${num}`, {});
    if (meta === 'ACCEPTED' && estadoCot(num) === 'APPROVED') await api('carlos.pimentel', 'PATCH', `v1/quotes/accept/${num}`);
  }
  if (meta === 'CANCELLED' && est !== 'CANCELLED') await api(ROSA, 'PATCH', `v1/quotes/cancel/${num}`);
  ids.cotizaciones[q].estado = estadoCot(num);
  if (ids.cotizaciones[q].estado !== meta) log(`✗ ${q} quedó ${ids.cotizaciones[q].estado} (esperado ${meta})`);
}
guardar();

// ── 10. Facturas: F1 B01 de Carlos emitida · F2 B02 de Rosa emitida · F3 borrador de Carlos
const B01 = +uno(`SELECT id FROM ncf_type WHERE name='B01'`), B02 = +uno(`SELECT id FROM ncf_type WHERE name='B02'`);
const FAC = [
  ['F1', 'carlos.pimentel', 'Constructora Mirador', B01, [['FER-5001', 20], ['FER-1001', 4]], 'EMITTED'],
  ['F2', 'rosa.almanzar', 'Consumidor Final', B02, [['FER-2003', 3], ['FER-4004', 2]], 'EMITTED'],
  ['F3', 'carlos.pimentel', 'Ferretería Doña Luz', B01, [['FER-3003', 6]], 'DRAFT'],
];
ids.facturas = ids.facturas ?? {};
const estadoFac = n => uno(`SELECT s.code FROM invoices i JOIN invoice_status s ON s.id=i.invoice_status_id WHERE i.company_id=${CIA} AND i.invoice_number='${n}'`);
for (const [f, autor, cliente, ncf, lineas, meta] of FAC) {
  let num = ids.facturas[f]?.numero;
  if (!num || !uno(`SELECT id FROM invoices WHERE company_id=${CIA} AND invoice_number='${num}' AND deleted_at IS NULL`)) {
    const r = await api(autor, 'POST', 'v1/invoices', {
      ncfType: ncf, partner: ids.clientes[cliente], currency: DOP,
      details: lineas.map(([sku, qty]) => ({ product: P(sku).id, quantity: qty, priceId: P(sku).precioId })),
    });
    num = r.invoiceNumber ?? r.data?.invoiceNumber;
    ids.facturas[f] = { numero: num, id: +(r.id ?? r.data?.id), autor, cliente };
    log('factura', f, num, 'por', autor);
  }
  if (meta === 'EMITTED' && estadoFac(num) === 'DRAFT') {
    const r = await api(autor, 'PATCH', `v1/invoices/change-status/${num}`, { invoiceStatusCode: 'EMITTED' }, { permitir: [403] });
    if (r?._status === 403) { log(`${f}: ${autor} no puede emitir (403) → emite Rosa`); await api(ROSA, 'PATCH', `v1/invoices/change-status/${num}`, { invoiceStatusCode: 'EMITTED' }); ids.facturas[f].emitida_por = ROSA; }
  }
  ids.facturas[f].estado = estadoFac(num);
  ids.facturas[f].ncf = uno(`SELECT IFNULL(ncf,'') FROM invoices WHERE company_id=${CIA} AND invoice_number='${num}'`);
}
guardar();

// ── 11. Credencial «Tienda en línea anterior» (plantilla por defecto), luego envejecida por SQL
let tienda = uno(`SELECT id FROM users WHERE company_id=${CIA} AND userType='INTEGRATION' AND integrationName='Tienda en línea anterior' AND deleted_at IS NULL LIMIT 1`);
if (!tienda) {
  const r = await api(ROSA, 'POST', 'v1/integration-users', { integrationName: 'Tienda en línea anterior', integrationDescription: 'Sincronizaba pedidos de la tienda web (ya no se usa)' });
  tienda = r.user?.id;
  ids.credenciales = { ...(ids.credenciales ?? {}), tienda: { id: +tienda, apiKey: r.credentials.apiKey, apiSecret: r.credentials.apiSecret, prefijo: r.credentials.apiKeyPrefix } };
  log('credencial tienda', tienda);
}
sql(`UPDATE users SET created_at=NOW(6) - INTERVAL 120 DAY, lastApiCall=NOW() - INTERVAL 80 DAY, apiCallCount=GREATEST(apiCallCount, 412)
  WHERE id=${tienda} AND company_id=${CIA} AND userType='INTEGRATION'`);

// ── 12. Héctor: creado hace 45 días y nunca entró (NEVER_LOGGED_IN usa created_at < hoy-30)
sql(`UPDATE users SET created_at=NOW(6) - INTERVAL 45 DAY WHERE id=${ids.usuarios['hector.vargas']}`);

// ── 13. Ingresos: cada persona activa entra al menos una vez, salvo Héctor (nunca) — Luisa «entró 1 vez».
// users.login_date nace NULL desde R22 (migración 1810000001031) y lo llena el primer ingreso; el Resumen
// cuenta los eventos AUTH/LOGIN_SUCCESS de audit_logs → se comprueba ahí.
const entro = u => +uno(`SELECT COUNT(*) FROM audit_logs WHERE company_id=${CIA} AND user_id=${ids.usuarios[u]} AND action='AUTH' AND event='LOGIN_SUCCESS'`);
for (const u of ['ana.mejia', 'jose.cabrera', 'carlos.pimentel', 'pedro.nunez', 'marta.guzman', 'luisa.feliz', 'sonia.reyes']) {
  if (entro(u)) continue;
  const inactiva = uno(`SELECT active FROM users WHERE id=${ids.usuarios[u]}`) === '0';
  if (inactiva) await api(ROSA, 'PATCH', `user/${ids.usuarios[u]}`, { active: true });
  await login(u, { forzar: true }); log('ingreso', u);
}
// Sonia entró alguna vez y hoy está INACTIVA (vista «Inactivas»; no cuenta en «Nunca entraron»)
if (uno(`SELECT active FROM users WHERE id=${ids.usuarios['sonia.reyes']}`) === '1') {
  await api(ROSA, 'PATCH', `user/${ids.usuarios['sonia.reyes']}`, { active: false }); log('sonia.reyes → inactiva');
}

// ── 14. Un guardado en lote real: Rosa concede «Productos · Exportar» a Almacén. Va el ÚLTIMO para que
// «Cambió permisos» encabece la actividad reciente del Resumen (video 01) y la bitácora (07).
await espera(1500);
if (await conceder(R.almacen, [['PRODUCT_EXPORT']])) log('Almacén + PRODUCT_EXPORT (lote)');

// ── 15. R18: aviso «Configuración incompleta» ya visto por TODOS (usuario×empresa)
const todos = Object.values(ids.usuarios);
sql(`INSERT INTO user_company_preferences (user_id, company_id, incomplete_config_notice_seen_at)
  VALUES ${todos.map(u => `(${u}, ${CIA}, NOW())`).join(',')}
  ON DUPLICATE KEY UPDATE incomplete_config_notice_seen_at=IFNULL(incomplete_config_notice_seen_at, NOW())`);
guardar();
await espera(1500);

// ── 16. Canon de «Actividad reciente» (D-S13). El Resumen lista los 10 eventos más nuevos de la empresa:
// el «Cambió permisos» de Almacén (paso 14) tiene que ser lo ÚLTIMO sembrado, para que en la toma quede
// 2.º, debajo solo del ingreso de quien graba. Una re-ejecución (el login de Rosa del paso 4b) o una
// verificación por API después de la siembra dejan ingresos DESPUÉS del cambio: son ruido de preparación,
// no parte del plan (cada persona ya tiene su ingreso del paso 13), y se quitan.
{
  const cambio = sql(`SELECT id, created_at FROM audit_logs WHERE company_id=${CIA} AND entity_name='roles'
    AND entity_id='${R.almacen}' AND event='PERMISSIONS_CHANGED' ORDER BY created_at DESC LIMIT 1`)[0];
  if (cambio) {
    const [, cuando] = cambio;
    const n = uno(`SELECT COUNT(*) FROM audit_logs WHERE company_id=${CIA} AND action='AUTH' AND event='LOGIN_SUCCESS' AND created_at > '${cuando}'`);
    if (+n) {
      sql(`DELETE FROM audit_logs WHERE company_id=${CIA} AND action='AUTH' AND event='LOGIN_SUCCESS' AND created_at > '${cuando}'`);
      log('ingresos de preparación posteriores al cambio de permisos quitados:', n);
    }
  }
  // Canon sembrado antes de D-S13: sus eventos llevan el user-agent de Node → como el navegador del paso 13.
  sql(`UPDATE audit_logs SET user_agent='${esc(NAVEGADOR_UA)}' WHERE company_id=${CIA} AND (user_agent IS NULL OR user_agent='node')`);
  // login_date = último ingreso de verdad (NULL si nunca entró: Héctor), como lo deja el API desde R22
  const humanos = Object.values(ids.usuarios).join(',');
  sql(`UPDATE users u LEFT JOIN (SELECT user_id, MAX(created_at) ult FROM audit_logs WHERE company_id=${CIA}
      AND action='AUTH' AND event='LOGIN_SUCCESS' GROUP BY user_id) a ON a.user_id=u.id
    SET u.login_date = a.ult WHERE u.id IN (${humanos})`);
}
log('✓ siembra completa → seeds/seguridad/ids.json');
console.log(JSON.stringify({ empresa: CIA, roles: R, usuarios: ids.usuarios, equipos: ids.equipos }, null, 0));
