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

// ── C, D, E ────────────────────────────────────────────────────────────────────────────────────
const paciente = (n, a) => +uno(`SELECT id FROM partners WHERE company_id=${E} AND name='${n}' AND firstLastName='${a}' AND deleted_at IS NULL ORDER BY id LIMIT 1`);
const tarifa = code => TARIFAS.find(t => t[0] === code);

async function afiliar(pac, poliza, afiliado) {
  const ya = uno(`SELECT id FROM patient_insurances WHERE company_id=${E} AND patient_id=${pac} AND deleted_at IS NULL LIMIT 1`);
  if (ya) return +ya;
  const r = await api('POST', 'v1/patient-insurances', {
    patient: pac, plan: plan('HUMANO-P01'), policyNumber: poliza, memberNumber: afiliado, isPrimary: true,
    effectiveDate: new Date().toISOString().slice(0, 10),
  });
  return r.id;
}

async function autorizar(afiliacion, codes, codigoArs) {
  const r = await api('POST', 'v1/insurance-authorizations', {
    patientInsurance: afiliacion,
    details: codes.map(code => {
      const [, precio, cubre, copago] = tarifa(code);
      return { product: prod(code), quantity: 1, unitPrice: precio, coverageType: 'FIXED_AMOUNT', coverageValue: cubre,
               maxCoveredAmount: cubre, patientCopay: copago };
    }),
  });
  // Como en pantalla: «Guardar y Aprobar» con el código de la ARS y treinta días de vigencia.
  const hoy = new Date(); const fin = new Date(hoy.getTime() + 30 * 86400000);
  const cubre = codes.reduce((t, c) => t + tarifa(c)[2], 0);
  await api('POST', `v1/insurance-authorizations/${r.id}/approve`, {
    insurerAuthorizationNumber: codigoArs, approvedAmount: cubre,
    validFrom: hoy.toISOString().slice(0, 10), validUntil: fin.toISOString().slice(0, 10),
  });
  return api('GET', `v1/insurance-authorizations/${r.id}`);
}

async function catalogos() {
  const inc = await api('GET', 'v1/income-type?limit=20');
  const pay = await api('GET', 'v1/payment/types?limit=50');
  const cur = await api('GET', 'v1/company-currencies/local');
  const rows = x => x?.data ?? x ?? [];
  return {
    incomeType: (rows(inc).find(i => i.isDefault) ?? rows(inc)[0])?.id,
    paymentType: (rows(pay).find(p => /contado|efectivo|cash/i.test(p.name ?? '')) ?? rows(pay)[0])?.id,
    creditPaymentType: (rows(pay).find(p => /cr[eé]dito/i.test(p.name ?? '')) ?? rows(pay)[0])?.id,
    currency: cur?.currency?.id ?? cur?.id,
  };
}

// Factura del paciente desde su autorización, emitida y cobrada en efectivo.
async function facturarPaciente(cat, pac, afiliacion, aut) {
  const r = await api('POST', 'v1/medical-invoices', {
    ncfType: 2, incomeType: cat.incomeType, paymentType: cat.paymentType, currency: cat.currency,
    partner: pac, patientInsurance: afiliacion,
    details: aut.details.map(d => ({ product: d.productId ?? d.product?.id, quantity: 1, unitPriceOverride: Number(d.unitPrice) })),
    coverageOverrides: aut.details.map((d, i) => ({ detailIndex: i, authorizationDetail: d.id })),
  });
  const numero = r.invoiceNumber ?? r.invoice?.invoiceNumber;
  await api('PATCH', `v1/invoices/change-status/${numero}`, { invoiceStatusCode: 'EMITTED' });
  const copago = +uno(`SELECT total FROM invoices WHERE invoice_number='${numero}' AND company_id=${E}`);
  if (copago > 0) await api('POST', 'v1/payment', { invoiceNumber: numero, amount: copago.toFixed(2), amountReceived: copago.toFixed(2), paymentMethodCode: 'CASH' });
  return numero;
}

async function estadoC() {
  await login();
  const rosa = paciente('Rosa Elena', 'Martínez');
  const af = await afiliar(rosa, 'HUM-778812', '88120455');
  if (!uno(`SELECT id FROM insurance_authorizations WHERE company_id=${E} AND patient_insurance_id=${af} AND deleted_at IS NULL LIMIT 1`))
    await autorizar(af, ['SRV-CONSULTA'], 'AUT-551207');
  log('estado C listo: Rosa afiliada a Humano con su autorización aprobada');
}

async function estadoD() {
  await login();
  const cat = await catalogos();
  const rosa = paciente('Rosa Elena', 'Martínez');
  const afRosa = +uno(`SELECT id FROM patient_insurances WHERE company_id=${E} AND patient_id=${rosa} AND deleted_at IS NULL LIMIT 1`);
  const autRosa = await api('GET', `v1/insurance-authorizations/${uno(`SELECT id FROM insurance_authorizations WHERE company_id=${E} AND patient_insurance_id=${afRosa} AND deleted_at IS NULL ORDER BY id LIMIT 1`)}`);
  await facturarPaciente(cat, rosa, afRosa, autRosa);
  // Otras dos pacientes de Humano con lo suyo ya facturado: «Por reclamar» con más de una.
  for (const [n, a, pol, afi, codes, codigo] of [
    ['Juan Carlos', 'Batista', 'HUM-662041', '88119321', ['SRV-SONO-ABD'], 'AUT-551388'],
    ['Carolina', 'Méndez', 'HUM-701553', '88124507', ['SRV-CONSULTA', 'SRV-HEMOGRAMA'], 'AUT-551402'],
  ]) {
    const pac = paciente(n, a);
    const af = await afiliar(pac, pol, afi);
    const aut = await autorizar(af, codes, codigo);
    await facturarPaciente(cat, pac, af, aut);
  }
  log('estado D listo: tres autorizaciones de Humano facturadas al paciente');
}

async function estadoE() {
  await login();
  const cat = await catalogos();
  const auts = sql(`SELECT id FROM insurance_authorizations WHERE company_id=${E} AND deleted_at IS NULL ORDER BY id`).map(r => +r[0]);
  await api('POST', 'v1/insurer-invoices/claims', { authorizationIds: auts });
  const claims = sql(`SELECT id FROM insurance_claims WHERE company_id=${E} AND deleted_at IS NULL ORDER BY id`).map(r => +r[0]);
  const fi = await api('POST', 'v1/insurer-invoices/from-claims', {
    insurer: aseguradora('ARS HUMANO'), claimIds: claims, incomeType: cat.incomeType, paymentType: cat.creditPaymentType,
  });
  await api('POST', `v1/insurer-invoices/${fi.invoice?.id ?? fi.id}/emit`);
  log('estado E listo:', claims.length, 'reclamaciones en la factura a ARS Humano, emitida');
}

if (orden === 'guardar') guardar(nombre);
else if (orden === 'E') await estadoE();
else if (orden === 'C') await estadoC();
else if (orden === 'D') await estadoD();
else if (orden === 'B') await estadoB();
else if (orden === 'restaurar') restaurar(nombre);
else if (orden === 'base') await base();
else { console.error('orden desconocida'); process.exit(1); }
