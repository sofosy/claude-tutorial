// QUÉ se fija y restaura del estado del video «Punto de venta» (P0…) de la empresa demo 43.
// = todas las tablas de la serie de Cajas (cajas/_estado.mjs) + las que escriben la siembra del POS y
// una venta del POS (medido con _medir.mjs antes/después de sembrar y de la prueba de punta a punta).
// Mismos modos que en cajas/_estado.mjs ('filas' | 'solo-update' | 'secuencia').
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { TABLAS as CAJAS, W, snap } from '../cajas/_estado.mjs';

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
export { W, snap };

export const TABLAS = [
  ...CAJAS,
  // catálogo y existencias (sembrar.mjs + la salida de inventario de cada venta)
  ['product_types', 'filas'],
  ['product_variants', 'filas'],
  ['inventory', 'filas'],
  ['inventory_movement', 'filas'],
  ['inventory_reservations', 'filas'],
  ['product_batch', 'filas'],
  ['invoice_detail_inventory_allocations', 'filas'], // de qué lote salió cada línea vendida
  ['subscription_resource_usage', 'solo-update'],     // contadores del plan (Product / InvoiceSent del mes)
  ['media', 'filas'],                  // fotos subidas (el archivo en disco NO se borra al restaurar)
  ['product_media', 'filas'],
  // clientes, crédito y descuentos
  ['partners', 'filas'],               // saldo usado del crédito (usedCredit/availableCredit) y clientes creados en el POS
  ['partner_customer_profiles', 'filas'],
  ['customer_analytics', 'filas'],
  ['customer_interactions', 'filas'],
  ['credit_lines', 'filas'],           // usedCredit sube con la venta a crédito
  ['credit_requests', 'filas'],
  ['discounts', 'filas'],
  ['discount_versions', 'filas'],
  ['discount_apply', 'filas'],
  ['discount_analytics', 'filas'],
  // rol complementario de la cajera (maestro; se vuelca para que un estado viejo no lo pierda)
  ['roles', 'filas'],
  ['user_company_roles', 'filas'],
];
