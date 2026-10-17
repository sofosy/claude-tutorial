#!/usr/bin/env node
/**
 * Deja la base local lista para grabar el video del REGISTRO.
 *
 *   node seeds/registro/restaurar.mjs
 *
 * El video crea de verdad una empresa y su usuario. Para volver a grabar hay
 * que liberar lo que el registro exige que sea único —el correo, el usuario,
 * el teléfono de WhatsApp, el RNC y el slug de la empresa— sin desarmar el
 * grafo de catálogos que el alta levantó: se renombran y se dan de baja
 * lógica, no se borran.
 *
 * También asegura lo que el formulario necesita y la base local no trae:
 *  - el contribuyente FICTICIO en el padrón (el padrón local tiene personas
 *    reales; en cámara no puede salir una empresa real registrándose);
 *  - los planes de empresa (Facturación y ERP) publicados en el catálogo.
 *
 * Credenciales: el archivo de opciones de MySQL que indique TUT_MY_CNF
 * (por defecto %TEMP%/claude/tut-my.cnf), nunca la clave en la línea.
 */
import { execFileSync } from 'node:child_process';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const MYSQL = process.env.TUT_MYSQL ?? 'C:/Program Files/MySQL/MySQL Server 9.7/bin/mysql.exe';
const CNF = process.env.TUT_MY_CNF ?? join(tmpdir(), 'claude', 'tut-my.cnf');
const DB = process.env.TUT_DB ?? 'germiva';

export const DEMO = {
  email: 'ana.martinez@ferreteriaelfaro.do',
  telefono: '8095550142',
  rnc: '130555099',
  nombreLegal: 'FERRETERIA EL FARO SRL',
};

const PLANES_EMPRESA = ['FACT_BASICO', 'FACT_PLUS', 'FACT_PRO', 'ERP_ESENCIAL', 'ERP_EMPRESARIAL', 'ERP_ENTERPRISE'];

function sql(query) {
  return execFileSync(MYSQL, [`--defaults-extra-file=${CNF}`, '--default-character-set=utf8mb4', DB, '-N', '-e', query], { encoding: 'utf8' }).trim();
}

const sello = Date.now().toString(36);

const usuarios = sql(`SELECT id FROM users WHERE (email='${DEMO.email}' OR username='${DEMO.email}' OR whatsapp_phone LIKE '%${DEMO.telefono}') AND email NOT LIKE '%.retirado-%'`);
for (const id of usuarios.split(/\s+/).filter(Boolean)) {
  sql(`UPDATE users SET email=CONCAT(email,'.retirado-${sello}'), username=CONCAT(username,'.retirado-${sello}'),
       whatsapp_phone=NULL, deleted_at=COALESCE(deleted_at, NOW()) WHERE id=${id}`);
  console.log(`usuario ${id} retirado`);
}

const empresas = sql(`SELECT id FROM companies WHERE rnc='${DEMO.rnc}'`);
for (const id of empresas.split(/\s+/).filter(Boolean)) {
  sql(`UPDATE companies SET rnc=CONCAT('R${sello}-',id), slug=IF(slug IS NULL, NULL, CONCAT(slug,'-retirado-${sello}')),
       custom_domain=NULL, deleted_at=COALESCE(deleted_at, NOW()) WHERE id=${id}`);
  console.log(`empresa ${id} retirada`);
}

sql(`INSERT INTO taxpayers (rnc, legalName, economicActivity, operationDate, status, paymentRegime)
     VALUES ('${DEMO.rnc}', '${DEMO.nombreLegal}', 'VENTA AL POR MENOR DE ARTICULOS DE FERRETERIA', '12/03/2019', 'ACTIVO', 'NORMAL')
     ON DUPLICATE KEY UPDATE legalName=VALUES(legalName), status='ACTIVO', deleted_at=NULL`);

const lista = PLANES_EMPRESA.map((c) => `'${c}'`).join(',');
const sinPublicar = sql(`SELECT code FROM plans WHERE code IN (${lista}) AND (lifecycle_status<>'ACTIVE' OR publicly_visible=0)`);
if (sinPublicar) {
  sql(`UPDATE plans SET lifecycle_status='ACTIVE', publicly_visible=1 WHERE code IN (${lista})`);
  console.log(`planes publicados: ${sinPublicar.replace(/\s+/g, ' ')} (reinicia el API si cachea el catálogo)`);
}

// Los nombres de la línea Facturación, como en el catálogo de producción
// (api.germiva.com/api/v1/plans/public, revisado el 2026-10-05): la base local
// trae los nombres viejos y salen en el diálogo de cambio de plan.
for (const [codigo, nombre] of [['FACT_PLUS', 'Crecimiento'], ['FACT_PRO', 'Expansión']]) {
  sql(`UPDATE plans SET name='${nombre}' WHERE code='${codigo}' AND name<>'${nombre}'`);
}

const quedan = sql(`SELECT (SELECT COUNT(*) FROM users WHERE email='${DEMO.email}') + (SELECT COUNT(*) FROM companies WHERE rnc='${DEMO.rnc}')`);
if (quedan !== '0') {
  console.error('ERROR: el correo o el RNC de la demo siguen ocupados');
  process.exit(1);
}
console.log('registro listo para grabar');
