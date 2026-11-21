// node seeds/compras-facturas/preparar.mjs [A|B] [--sin-reset]
// Deja la base local en el estado de partida de la serie «Compras · Entrada de facturas» (nov. 2026):
//   A  Ferretería Germiva con sus proveedores ficticios (RNC 130555xxx, también en el padrón local),
//      una orden de Cementos Germiva del Cibao ya recibida y procesada SIN factura (video del cotejo),
//      y el producto «Pintura acrílica blanca galón» (video de la mercancía por recibir).
//   B  A + historia para el video de presentación: las dos facturas de la plantilla con entrada, y pendientes
//      los tres e-CF del reporte de la DGII y la factura de Ferremateriales leída con IA.
// Parte SIEMPRE de la instantánea sembrada del dev-env (Germiva-api/.dev-env/seeded.sql.gz), salvo --sin-reset.
//
// La lectura con IA necesita una credencial real: exporta OPENAI_API_KEY antes de correrlo y el script
// la registra como credencial de plataforma de la base LOCAL. La clave nunca se escribe en el repositorio.
import { execSync, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sql, uno, api, login, idProducto, idUbicacion, log, EMPRESA, API } from '../fabricacion/_lib.mjs';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const estado = (process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'A').toUpperCase();
const t0 = Date.now();
const UNIDAD = 43, ITBIS = 1, EXENTO = 4, MATERIALES = 7, ALMACEN = 1;
const hoy = () => new Date(Date.now() - 4 * 3600e3).toISOString().slice(0, 10);
const dias = n => new Date(Date.now() - 4 * 3600e3 + n * 864e5).toISOString().slice(0, 10);

if (!process.argv.includes('--sin-reset')) {
  // Igual que la serie de Fabricación: la instantánea + migraciones se guarda como base local de la serie
  // para que cada restauración tarde segundos. Borra .dev-env/compras-facturas-base.sql.gz si cambia el esquema.
  const apiDir = path.resolve(process.env.GERMIVA_API_DIR || '../Germiva-api');
  const base = path.join(apiDir, '.dev-env/compras-facturas-base.sql.gz');
  const M = 'docker exec -i germiva-dev-mysql mysql -uroot';
  const cargar = archivo => {
    execSync(`${M} -e "DROP DATABASE IF EXISTS germiva; CREATE DATABASE germiva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"`);
    execSync(`gunzip -c "${archivo}" | ${M} germiva`, { shell: '/bin/bash' });
  };
  if (fs.existsSync(base)) cargar(base);
  else {
    cargar(path.join(apiDir, '.dev-env/seeded.sql.gz'));
    execSync('npx typeorm migration:run -d ./dist/config/typeorm.js --transaction all && node dist/scripts/sync-permissions-additive.js'
      + ' && node --env-file=.env scripts/dev-env/ensure-db-routines.cjs', { cwd: apiDir, stdio: 'ignore', shell: '/bin/bash' });
    execSync(`docker exec germiva-dev-mysql mysqldump -uroot --single-transaction --routines --triggers --events --hex-blob`
      + ` --set-gtid-purged=OFF --default-character-set=utf8mb4 germiva | gzip > "${base}"`, { shell: '/bin/bash' });
    log('base local de la serie guardada');
  }
  log(`base restaurada en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
}
try { execFileSync('docker', ['exec', 'germiva-dev-redis', 'redis-cli', 'FLUSHALL'], { stdio: 'ignore' }); }
catch { try { execFileSync('redis-cli', ['FLUSHALL'], { stdio: 'ignore' }); } catch { log('AVISO: no se pudo vaciar Redis'); } }

// ── Empresa ──────────────────────────────────────────────────────────────────────────────
sql(`
UPDATE companies SET legalName='Ferretería Germiva Demo S.R.L.', tradeName='Ferretería Germiva', rnc='130555001',
  email='compras@ferreteria.germiva.com', website='https://germiva.com' WHERE id=${EMPRESA};
UPDATE users SET email='admin@germiva.com', current_company_id=${EMPRESA} WHERE id=1;
UPDATE subscriptions SET expirationDate='2027-12-31 23:00:00', nextBillingDate='2027-12-31 23:00:00'
  WHERE company_id=${EMPRESA} AND status='ACTIVE';
UPDATE user_company_preferences SET incomplete_config_notice_seen_at=COALESCE(incomplete_config_notice_seen_at, NOW())
  WHERE company_id=${EMPRESA};
-- El seeder de la empresa principal creaba el «Proveedor Genérico» sin su marca (corregido en
-- fix/compras-entrada-de-facturas); sin ella el gasto menor sin proveedor no se guarda. Hasta que la
-- instantánea semanal se regenere con el seeder corregido, se marca aquí.
UPDATE partners SET is_generic_supplier=1, isInternalPartner=1
  WHERE company_id=${EMPRESA} AND name='Proveedor Genérico' AND deleted_at IS NULL
    AND NOT EXISTS (SELECT 1 FROM (SELECT id FROM partners WHERE company_id=${EMPRESA} AND is_generic_supplier=1) g);
`);
await login();

// ── Credencial de IA (solo base local) ───────────────────────────────────────────────────
if (process.env.OPENAI_API_KEY) {
  const existe = uno(`SELECT id FROM platform_ai_credentials WHERE name='Tutoriales OpenAI' AND deleted_at IS NULL LIMIT 1`);
  const cuerpo = { name: 'Tutoriales OpenAI', provider: 'openai', apiKey: process.env.OPENAI_API_KEY, defaultModel: 'gpt-4.1' };
  if (existe) await api('PUT', `v1/platform-ai/credentials/${existe}`, cuerpo);
  else await api('POST', 'v1/platform-ai/credentials', cuerpo);
  await api('PUT', 'v1/platform-ai/purposes/INVOICE_IMPORT', { enabled: true, credential: +uno(`SELECT id FROM platform_ai_credentials WHERE name='Tutoriales OpenAI' AND deleted_at IS NULL LIMIT 1`) });
  log('credencial de IA lista (INVOICE_IMPORT)');
} else log('AVISO: sin OPENAI_API_KEY, la lectura con IA no va a responder');

// ── Proveedores (RNC del rango ficticio 130555) ──────────────────────────────────────────
// Los que salen en el padrón local para que el buscador los ofrezca «Del padrón de la DGII».
const PADRON = [
  ['130555109', 'SEGURIDAD GERMIVA DEL CARIBE SRL', 'SERVICIOS DE VIGILANCIA'],
  ['130555117', 'FERREMATERIALES GERMIVA SRL', 'VENTA AL POR MAYOR DE MATERIALES DE CONSTRUCCION'],
  ['130555125', 'PAPELERIA GERMIVA SRL', 'VENTA AL POR MENOR DE ARTICULOS DE OFICINA'],
  ['130555133', 'LUBRICANTES GERMIVA SRL', 'VENTA AL POR MAYOR DE LUBRICANTES'],
  ['130555141', 'CLIMATIZACION GERMIVA SRL', 'INSTALACION Y MANTENIMIENTO DE AIRES ACONDICIONADOS'],
  ['130555151', 'LIMPIEZA GERMIVA SRL', 'VENTA DE PRODUCTOS DE LIMPIEZA'],
  ['130555168', 'MANTENIMIENTO GERMIVA SRL', 'SERVICIOS DE MANTENIMIENTO'],
  ['130555176', 'CEMENTOS GERMIVA DEL CIBAO SRL', 'FABRICACION DE CEMENTO'],
  ['130555184', 'PINTURAS GERMIVA SRL', 'FABRICACION DE PINTURAS'],
];
sql(PADRON.map(([rnc, nombre, act]) => `INSERT INTO taxpayers (rnc, legalName, economicActivity, operationDate, status, paymentRegime)
  VALUES ('${rnc}', '${nombre}', '${act}', '01/02/2015', 'ACTIVO', 'NORMAL')
  ON DUPLICATE KEY UPDATE legalName=VALUES(legalName), status='ACTIVO', deleted_at=NULL;`).join('\n'));

const cuenta = nombre => +uno(`SELECT id FROM accounting_chart WHERE (company_id=${EMPRESA} OR company_id IS NULL) AND deleted_at IS NULL
  AND allowsMovement=1 AND name='${nombre}' ORDER BY company_id DESC, id LIMIT 1`);
async function proveedor({ name, tin, legalName, plazo = null, cat606 = null, gasto = null, extra = {} }) {
  let id = +uno(`SELECT id FROM partners WHERE company_id=${EMPRESA} AND ${tin ? `tin='${tin}'` : `name='${name}'`} AND deleted_at IS NULL LIMIT 1`);
  if (!id) id = (await api('POST', 'v1/partner', { name, legalName: legalName ?? name, ...(tin ? { tin } : {}),
    partnerType: ['SUPPLIER'], partnerCategory: 'BUSINESS', ...extra })).id;
  sql(`UPDATE partners SET paymentTermDays=${plazo ?? 'NULL'}, default_goods_606_category=${cat606 ? `'${cat606}'` : 'NULL'},
    default_expense_account_id=${gasto || 'NULL'} WHERE id=${id}`);
  return id;
}
// Video 2 (manual por totales): ficha con plazo, categoría 606 y cuenta de gasto.
await proveedor({ name: 'Seguridad Germiva del Caribe', legalName: 'Seguridad Germiva del Caribe S.R.L.', tin: '130555109',
  plazo: 30, cat606: '02', gasto: cuenta('Vigilancia y seguridad') });
// Video 3 (por líneas, al contado): sin plazo.
await proveedor({ name: 'Papelería Germiva', legalName: 'Papelería Germiva S.R.L.', tin: '130555125', cat606: '09' });
// Video 7 (cotejo con la recepción) y video 8 (mercancía por recibir).
const cementos = await proveedor({ name: 'Cementos Germiva del Cibao', legalName: 'Cementos Germiva del Cibao S.R.L.', tin: '130555176', plazo: 30, cat606: '09' });
await proveedor({ name: 'Pinturas Germiva', legalName: 'Pinturas Germiva S.R.L.', tin: '130555184', plazo: 15, cat606: '09' });
// Video 9 (Comprobante de Compras B11/E41): persona sin RNC, con cédula.
await proveedor({ name: 'Ramón Germiva Almonte', tin: '00113055503', documentType: 'CEDULA',
  extra: { isInformalTaxpayer: true, partnerCategory: 'PERSON', documentType: 'CEDULA' } });
// Video 11 (Pagos al exterior B17/E47): proveedor del exterior con documento extranjero.
await proveedor({ name: 'Germiva Cloud Hosting LLC', extra: { documentType: 'DOCUMENTO_EXTRANJERO', foreignDocumentNumber: 'US-88-1305550' } });
// Ferremateriales (130555117) NO tiene ficha: la crea el buzón al dar entrada a la factura leída con IA (video 4).
// Lubricantes y Climatización llegan por la plantilla; Limpieza y Mantenimiento, por el reporte de la DGII.

// Video 11 (Pagos al exterior): el dólar activo y la tasa del día.
try { await api('PATCH', 'v1/company-currencies/admin/1/activate', {}); } catch (e) { log('AVISO moneda USD:', e.message.slice(0, 160)); }
await api('POST', 'v1/exchange-rates/quick', { fromCurrencyCode: 'USD', toCurrencyCode: 'DOP', rate: 60.5, effectiveDate: hoy(), source: 'manual' });

// ── Inventario: patio del almacén, cemento y varilla, pintura ────────────────────────────
if (!idUbicacion('Patio')) await api('POST', 'v1/inventory/location', { position: 'Patio', warehouse: ALMACEN });
const PATIO = idUbicacion('Patio');
async function producto(name, costo, tax = ITBIS) {
  let id = idProducto(name);
  if (!id) {
    await api('POST', 'v1/product', { category: 'PRODUCT', managesInventory: true, usesExpirationDate: false, usesBatchControl: false,
      visibleInStore: false, productType: MATERIALES, unitMeasureValue: '1', name, description: name, unitMeasure: UNIDAD,
      tax, purchaseTax: tax, purchasePrice: costo.toFixed(2) });
    id = idProducto(name);
  }
  return id;
}
const cemento = await producto('Cemento gris Portland 42.5 kg', 395);
const varilla = await producto('Varilla de acero 3/8 x 20 pies', 245);
await producto('Pintura acrílica blanca galón', 890);
// Video 9 (Comprobante de Compras): el servicio que presta el proveedor informal.
if (!idProducto('Flete y acarreo de mercancía')) {
  await api('POST', 'v1/product', { category: 'SERVICE', managesInventory: false, usesExpirationDate: false, usesBatchControl: false,
    visibleInStore: false, productType: 25, unitMeasureValue: '1', name: 'Flete y acarreo de mercancía', description: 'Flete y acarreo de mercancía',
    unitMeasure: UNIDAD, tax: EXENTO, purchaseTax: EXENTO, purchasePrice: '0.00' });
}

// Orden de compra a Cementos Germiva del Cibao → recepción aceptada y procesada a inventario, sin factura.
if (!+uno(`SELECT COUNT(*) FROM purchase_receipts WHERE company_id=${EMPRESA} AND deleted_at IS NULL`)) {
  const oc = await api('POST', 'v1/orders', { orderType: 'PURCHASE', partnerId: cementos, requestedDeliveryDate: dias(2), warehouseId: ALMACEN,
    orderLines: [{ productId: cemento, quantity: 100, unitPrice: 395 }, { productId: varilla, quantity: 50, unitPrice: 245 }] });
  await api('POST', `v1/orders/${oc.id}/approve-from-draft`, {});
  await api('PATCH', `v1/orders/${oc.id}/fast-forward/READY_TO_RECEIVE`, {});
  const orden = await api('GET', `v1/orders/${oc.id}`);
  const lineas = orden.orderLines ?? orden.lines ?? [];
  const rc = await api('POST', 'v1/purchase-receipts', { purchaseOrder: oc.id, receiptDate: hoy(),
    lines: lineas.map(l => ({ orderLine: l.id, receivedQuantity: +l.quantity, location: PATIO })) });
  await api('POST', `v1/purchase-receipts/${rc.id}/accept`, {});
  await api('POST', `v1/purchase-receipts/${rc.id}/process-to-inventory`, {});
  log('orden', orden.orderNumber, '→ recepción', rc.receiptNumber, 'procesada');
}

// ── Estado B: historia para el video de presentación ─────────────────────────────────────
async function subir(archivo, ruta = 'import') {
  const { readFileSync } = fs;
  const form = new FormData();
  const tipo = archivo.endsWith('.jpg') ? 'image/jpeg'
    : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
  form.append('file', new Blob([readFileSync(archivo)], { type: tipo }), path.basename(archivo));
  const { accessToken } = await (await fetch(`${API}/auth/dev/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'admin' }) })).json();
  const r = await fetch(`${API}/v1/supplier-document-inbox/${ruta}`, { method: 'POST', headers: { Authorization: `Bearer ${accessToken}` }, body: form });
  const t = await r.text();
  if (!r.ok) throw new Error(`importar ${path.basename(archivo)} → ${r.status}: ${t.slice(0, 400)}`);
  return JSON.parse(t);
}
// Los archivos que suben los videos 5 y 6 (y el estado B) se rehacen con fechas de hoy.
execFileSync('python3', [path.join(AQUI, 'archivos.py')], { stdio: 'ignore' });
if (estado === 'B') {
  await subir(path.join(AQUI, 'facturas-plantilla.xlsx'));
  await subir(path.join(AQUI, 'reporte-dgii-ecf-recibidos.xlsx'));
  log('plantilla y reporte de la DGII importados');
  if (process.env.OPENAI_API_KEY) {
    const leida = await subir(path.join(AQUI, 'factura-ferremateriales.jpg'), 'upload');
    log('factura de Ferremateriales leída con IA', leida?.inbox?.status ?? '');
  }
  // Las dos de la plantilla ya con entrada: el listado de Facturas y el buzón muestran historia.
  const plantilla = sql(`SELECT id FROM supplier_document_inbox WHERE company_id=${EMPRESA} AND ncf IN ('E310000002201','E310000088410')`).map(f => +f[0]);
  await login(); // `subir` abrió otra sesión del mismo usuario y cerró la de `api`
  if (plantilla.length) await api('POST', 'v1/supplier-document-inbox/enter-batch', { ids: plantilla });
  log('entrada por lote a las facturas de la plantilla', plantilla.join(', '));
}
log(`estado ${estado} listo en ${((Date.now() - t0) / 1000).toFixed(0)} s`);
