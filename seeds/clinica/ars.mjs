// node seeds/clinica/ars.mjs <base|guardar NOMBRE|restaurar NOMBRE|B|C|D|E>
// Estados de la serie «Seguros de salud (ARS)». Facturas, asientos y cuentas por cobrar no se
// pueden desandar con un DELETE limpio, así que cada estado se guarda como un volcado de la base
// (.estados/<nombre>.sql.gz, fuera de git) y se restaura antes de cada toma (~2 min).
//   base  servicios del centro (exentos de ITBIS) y secuencias B01/B02; sin aseguradoras (video 1).
//   B     base + ARS Humano y ARS Senasa importadas y el tarifario de Humano (video 2).
//   C     B + Rosa afiliada a Humano con una autorización aprobada (video 3).
//   D     C + la factura de Rosa cobrada y otras dos autorizaciones facturadas (video 4).
//   E     D + reclamadas en una remesa y la factura a ARS Humano emitida (video 5).
import { execSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { sql, uno, api, login, log, empresa } from './_lib.mjs';

const [, , orden, nombre] = process.argv;
const DIR = new URL('../../.estados/', import.meta.url).pathname;
const E = empresa();

export const SERVICIOS = [
  { code: 'SRV-CONSULTA', name: 'Consulta de medicina general', price: 2500 },
  { code: 'SRV-HEMOGRAMA', name: 'Hemograma completo', price: 800 },
  { code: 'SRV-SONO-ABD', name: 'Sonografía abdominal', price: 3500 },
  { code: 'SRV-EKG', name: 'Electrocardiograma', price: 1800 },
];

function guardar(n) {
  mkdirSync(DIR, { recursive: true });
  execSync(`docker exec germiva-dev-mysql mysqldump -uroot --single-transaction --quick --skip-lock-tables germiva | gzip -1 > ${DIR}${n}.sql.gz`, { stdio: 'inherit', shell: '/bin/bash' });
  log('estado guardado:', n);
}
function restaurar(n) {
  execSync(`zcat ${DIR}${n}.sql.gz | docker exec -i germiva-dev-mysql mysql -uroot germiva`, { stdio: 'inherit', shell: '/bin/bash' });
  log('estado restaurado:', n);
}

async function secuencia(tipo) {
  const lista = await api('GET', 'v1/ncf/secuentials?limit=100');
  if ((lista ?? []).some(s => s.ncfType?.id === tipo)) return;
  await api('POST', 'v1/ncf/secuential', { secuentialFrom: '00000001', secuentialTo: '00099999', dateExpire: '2027-12-31', ncfType: tipo });
}

async function servicio({ code, name, price }) {
  const ya = uno(`SELECT id FROM products WHERE company_id=${E} AND code='${code}' AND deleted_at IS NULL`);
  if (ya) return +ya;
  const p = await api('POST', 'v1/product', { category: 'SERVICE', name, code, description: name, tax: 4, managesInventory: false });
  await api('POST', 'v1/price', { product: p.id, price: String(price), customerType: 'REGULAR', priority: 1, taxIncluded: false });
  return p.id;
}

async function base() {
  await login();
  await secuencia(1); // B01 crédito fiscal (la factura a la ARS)
  await secuencia(2); // B02 consumo (la factura del paciente)
  for (const s of SERVICIOS) await servicio(s);
  log('base lista:', SERVICIOS.length, 'servicios y secuencias B01/B02');
}

// ── B: lo que deja el video 1, completo ─────────────────────────────────────────────────────────
export const TARIFAS = [ // plan Humano Básico: [código, precio, cubre, copago, exige autorización, código ARS]
  ['SRV-CONSULTA', 2500, 2000, 500, true, 'CONS-001'],
  ['SRV-HEMOGRAMA', 800, 640, 160, false, 'LAB-1020'],
  ['SRV-SONO-ABD', 3500, 2800, 700, true, 'IMG-3050'],
  ['SRV-EKG', 1800, 1440, 360, false, 'CAR-2010'],
];
const prod = code => +uno(`SELECT id FROM products WHERE company_id=${E} AND code='${code}' AND deleted_at IS NULL`);
export const aseguradora = n => +uno(`SELECT id FROM partners WHERE company_id=${E} AND name='${n}' AND deleted_at IS NULL ORDER BY id LIMIT 1`);
export const plan = codigo => +uno(`SELECT id FROM health_insurance_plans WHERE company_id=${E} AND plan_code='${codigo}' AND deleted_at IS NULL ORDER BY id LIMIT 1`);

async function estadoB() {
  await login();
  if (!aseguradora('ARS HUMANO')) await api('POST', 'v1/health-insurer-catalog/import', { codes: ['HUMANO', 'SENASA'] });
  await api('PATCH', `v1/partner/${aseguradora('ARS HUMANO')}`, { insurerProviderCode: 'PSS-10458', insurerClaimDeadlineDays: 60 });
  const humano = plan('HUMANO-P01');
  for (const [code, precio, cubre, copago, aut, codigoArs] of TARIFAS) {
    const ya = uno(`SELECT id FROM health_insurer_agreements WHERE company_id=${E} AND plan_id=${humano} AND product_id=${prod(code)} AND deleted_at IS NULL`);
    if (ya) continue;
    await api('POST', 'v1/health-insurer-agreements', {
      plan: humano, product: prod(code), insurerCode: codigoArs, pricingType: 'FIXED_AMOUNT',
      agreedPrice: precio, coverageAmount: cubre, patientCopay: copago, requiresAuthorization: aut,
    });
  }
  log('estado B listo: Humano y Senasa, tarifario de Humano Básico con', TARIFAS.length, 'servicios');
}

if (orden === 'guardar') guardar(nombre);
else if (orden === 'B') await estadoB();
else if (orden === 'restaurar') restaurar(nombre);
else if (orden === 'base') await base();
else { console.error('orden desconocida'); process.exit(1); }
