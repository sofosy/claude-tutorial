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

if (orden === 'guardar') guardar(nombre);
else if (orden === 'restaurar') restaurar(nombre);
else if (orden === 'base') await base();
else { console.error('orden desconocida'); process.exit(1); }
