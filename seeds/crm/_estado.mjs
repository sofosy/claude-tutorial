// QUÉ restaura el canon de configuración (C0) de las series CRM · Éxito del Cliente · Mesa de Ayuda.
//
// Son las filas que YA existían antes de la marca de agua (estados/M0.json) y que los videos pueden
// EDITAR: columnas del tablero, espacios, ajustes de Éxito del Cliente, plantillas, secuencias,
// estados y avisos de la Mesa de Ayuda, y los clientes (el gerente de cuenta vive en el cliente).
// Lo CREADO después de M0 lo borra restaurar.mjs por marca de agua; esto sólo devuelve lo editado.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EMPRESA } from './_lib.mjs';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
if (!EMPRESA) throw new Error('no existe la empresa demo (RNC 130555036): node seeds/seguridad/sembrar.mjs');
export const W = `company_id=${EMPRESA}`;

/** [tabla, modo, where] — mismos modos que seeds/seguridad/_estado.mjs */
export const TABLAS = [
  ['crm_workspaces', 'filas', W],
  ['pipeline_stages', 'filas', W],
  ['crm_goals', 'filas', W],
  ['crm_ai_configs', 'filas', W],
  ['customer_care_settings', 'filas', W],
  ['customer_onboarding_templates', 'filas', W],
  ['customer_playbooks', 'filas', W],
  ['helpdesk_workspaces', 'filas', W],
  ['helpdesk_ticket_statuses', 'filas', W],
  ['ticket_notification_rules', 'filas', W],
  ['surveys', 'filas', W],
  ['partners', 'filas', W],
];
export const snap = t => `snap_${t}`;
