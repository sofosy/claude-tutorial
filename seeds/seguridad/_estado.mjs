// QUÉ se fija y restaura de la empresa demo de Seguridad (E0, E2a, E6c).
// Medido con _medir.mjs antes/después de _ensuciar.mjs (todo lo que escriben los videos 02a…08g):
// cambian audit_logs, entity_versions, profiles, quote_approvals, quote_versions, quotes, roles,
// role_permissions (ai), role_permission_exclusions (ai), teams, team_members, user_companies,
// user_company_roles y users. Se añaden por seguridad las vecinas que el mismo flujo podría tocar
// (líneas de cotización, precios, preferencias del usuario, productos, configuración, plan, secuencias).
// Modos:
//   'filas'      → borrar las nuevas, UPDATE de las cambiadas, re-INSERT de las borradas (clave id)
//   'reemplazo'  → tabla puente sin id (clave compuesta): DELETE de las de la empresa + INSERT del canon
//   'solo-update'→ fila única de configuración: solo UPDATE
//   'secuencia'  → sys_sequences (trigger anti-DELETE): UPDATE; las nuevas vuelven a initial_value
// El ORDEN importa: las tablas cuyo filtro es una subconsulta sobre `roles` van ANTES que `roles`.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EMPRESA } from './_lib.mjs';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
if (!EMPRESA) throw new Error('no existe la empresa demo (RNC 130555036): node seeds/seguridad/sembrar.mjs');
export const W = `company_id=${EMPRESA}`;
const DE_ROLES = `role_id IN (SELECT id FROM roles WHERE company_id=${EMPRESA})`;

/** [tabla, modo, where] */
export const TABLAS = [
  ['role_permissions', 'filas', DE_ROLES],            // sin company_id: por los roles de la empresa
  ['role_permission_exclusions', 'filas', DE_ROLES],  // exclusiones de la herencia (03, 08f)
  ['roles', 'filas', W],                               // roles propios + rol propio de cada credencial
  ['team_members', 'filas', W],
  ['teams', 'filas', W],
  // E-4: visibilidad del menú de «Mi perfil» (video 09). Una fila por usuario×empresa (UNIQUE user_id,
  // company_id; el servicio siempre graba la empresa activa): usuarios de la empresa demo EN la empresa demo.
  // Va ANTES que user_company_roles/user_companies/users para que la subconsulta aún vea a las personas creadas en un video.
  ['user_menu_visibility', 'filas', `${W} AND user_id IN (SELECT user_id FROM user_companies WHERE company_id=${EMPRESA})`],
  ['user_company_roles', 'filas', W],
  ['user_companies', 'reemplazo', W],
  ['user_company_preferences', 'filas', W],            // R18 (aviso visto) y última ruta
  ['profiles', 'filas', W],
  ['users', 'filas', W],                               // personas + credenciales (clave, secreto, activo, lastApiCall)
  ['quotes', 'filas', W],
  ['quote_details', 'filas', W],
  ['quote_detail_inventory_allocations', 'filas', W],
  ['quote_approvals', 'filas', W],
  ['quote_versions', 'filas', W],
  ['entity_versions', 'filas', W],
  ['prices', 'filas', W],
  ['price_history', 'filas', W],
  ['products', 'filas', W],
  ['company_configs', 'solo-update', W],               // quote_requires_approval
  ['subscriptions', 'solo-update', W],                 // plan 15
  ['sys_sequences', 'secuencia', W],
  ['audit_logs', 'filas', W],                          // bitácora de la empresa (particionada, ver README)
];
export const snap = t => `snap_${t}`;
