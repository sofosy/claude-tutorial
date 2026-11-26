// node seeds/cajas/alta-empresa.mjs
// Da de alta la EMPRESA DEMO de la serie en una base que no la tiene (p. ej. la base sembrada del
// API en un contenedor): «Ferretería El Progreso SRL», id 43, con sus cuatro usuarios
// (guiones/_DATOS-CAJAS.md §0.1–0.2). Idempotente. Después: `node sembrar-s0.mjs` → `node fijar.mjs S0`.
//
// - Los ids que la serie da por fijos (empresa 43, cajas 49/50/51) se respetan subiendo el
//   AUTO_INCREMENT antes de crear, solo si la base todavía no llegó a ese número.
// - El alta es el flujo real (`POST auth/dev/register`, solo con NODE_ENV=local|test); los
//   compañeros se crean como en «Nuevo usuario» (`POST user`) con su rol de sistema por código.
import { API, CLAVE, EMPRESA, api, sql, log } from './_lib.mjs';

const RNC = '130555021';
const DOMINIO = 'germiva.demo';
const ADMIN = 'admin.progreso';
const uno = q => sql(q)[0]?.[0];

const subirA = (tabla, id) => {
  const max = +(uno(`SELECT IFNULL(MAX(id),0) FROM ${tabla}`) ?? 0);
  if (max < id) sql(`ALTER TABLE ${tabla} AUTO_INCREMENT=${id}`);
};

let cia = uno(`SELECT id FROM companies WHERE rnc='${RNC}' AND deleted_at IS NULL LIMIT 1`);
if (!cia) {
  subirA('companies', EMPRESA);
  const r = await fetch(`${API}/auth/dev/register`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: `${ADMIN}@${DOMINIO}`, password: CLAVE, name: 'Ramón', lastName: 'Almonte',
      phones: ['8095550142'], legalName: 'Ferretería El Progreso SRL', tradeName: 'Ferretería El Progreso',
      rnc: RNC, address: 'Av. Duarte 214, Ensanche La Fe, Santo Domingo', phone: '809-555-0142',
    }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(`dev/register → ${r.status}: ${JSON.stringify(j).slice(0, 500)}`);
  cia = uno(`SELECT id FROM companies WHERE rnc='${RNC}' AND deleted_at IS NULL LIMIT 1`);
  log('empresa creada', cia);
}
if (+cia !== EMPRESA) throw new Error(`la empresa quedó con id ${cia}, no ${EMPRESA}: los estados de la serie no servirían`);

// El registro usa el correo como username → «admin.progreso», como en la serie.
const adminId = uno(`SELECT id FROM users WHERE email='${ADMIN}@${DOMINIO}' AND deleted_at IS NULL`);
if (uno(`SELECT username FROM users WHERE id=${adminId}`) !== ADMIN) {
  sql(`UPDATE users SET username='${ADMIN}' WHERE id=${adminId}`);
  log('username →', ADMIN);
}

// Configuración inicial (catálogo, períodos) si quedó pendiente.
if (uno(`SELECT setup_status FROM companies WHERE id=${EMPRESA}`) !== 'COMPLETED') {
  await api(ADMIN, 'POST', `v1/company/test/setup-initial-config/${EMPRESA}`, {});
  log('setup inicial completado');
}

const rol = code => +uno(`SELECT id FROM roles WHERE code='${code}' AND company_id IS NULL AND deleted_at IS NULL LIMIT 1`);
const COMPANEROS = [
  ['yohanna.peralta', 'Yohanna', 'Peralta', 'CASHIER'],
  ['luis.batista', 'Luis', 'Batista', 'CASHIER'],
  ['carmen.rosario', 'Carmen', 'Rosario', 'CASHIER_SUPERVISOR'],
];
// El plan 2 «Emprendedor» admite un solo usuario: como en la serie original, los compañeros se crean
// por SQL (profiles + users + user_companies + user_company_roles), con la clave de la serie.
const HASH = '$2b$10$exuwIKzeyyqc9BLQ5Lqw3ODfAdANY8GDom5XxTAmDOPoUFg5QRt1W'; // bcrypt de «Demo2026!»
for (const [u, nombre, apellido, code] of COMPANEROS) {
  if (uno(`SELECT id FROM users WHERE username='${u}' AND deleted_at IS NULL LIMIT 1`)) continue;
  sql(`INSERT INTO profiles (created_at, updated_at, is_internal, name, first_name, active)
VALUES (NOW(), NOW(), 0, '${nombre}', '${apellido}', 1);
SET @p := LAST_INSERT_ID();
INSERT INTO users (created_at, updated_at, is_internal, username, email, password, active, emailVerified,
                   current_company_id, profile_id, userType, is_default_password, termsAccepted)
VALUES (NOW(), NOW(), 0, '${u}', '${u}@${DOMINIO}', '${HASH}', 1, 1, ${EMPRESA}, @p, 'NORMAL', 0, 1);
SET @u := LAST_INSERT_ID();
INSERT INTO user_companies (user_id, company_id, is_internal) VALUES (@u, ${EMPRESA}, 0);
INSERT INTO user_company_roles (user_id, company_id, role_id, created_at, is_internal, active)
VALUES (@u, ${EMPRESA}, ${rol(code)}, NOW(), 0, 1);`);
  log('usuario', u);
}

// Sin el aviso «Configuración incompleta» ni contraseña por defecto al entrar (R18).
for (const u of [ADMIN, ...COMPANEROS.map(c => c[0])]) {
  const id = uno(`SELECT id FROM users WHERE username='${u}' AND deleted_at IS NULL`);
  sql(`UPDATE users SET current_company_id=${EMPRESA}, is_default_password=0, emailVerified=1 WHERE id=${id};
INSERT INTO user_company_preferences (user_id, company_id, incomplete_config_notice_seen_at, created_at, updated_at, is_internal, active)
SELECT ${id}, ${EMPRESA}, NOW(), NOW(), NOW(), 0, 1 FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM user_company_preferences WHERE user_id=${id} AND company_id=${EMPRESA});
UPDATE user_company_preferences SET incomplete_config_notice_seen_at=IFNULL(incomplete_config_notice_seen_at, NOW()) WHERE user_id=${id} AND company_id=${EMPRESA};`);
}

subirA('cashiers', 49);
log('listo: empresa', EMPRESA, '· siguiente: node sembrar-s0.mjs');
