// Definición de QUÉ se fija y restaura de la empresa demo (medido: conteos/auto_increment de las
// 622 tablas antes y después de sembrar S0 y de recorrer S1…S6; ver README).
import { EMPRESA } from './_lib.mjs';

/** Tablas que el flujo de Cajas escribe. Todas tienen company_id. Modo:
 *  - 'filas'     : se vuelca la fila completa; restaurar = borrar las nuevas, UPDATE de las que
 *                  cambiaron, re-INSERT de las borradas.
 *  - 'solo-update': nunca se borra ni inserta (fila de configuración única de la empresa).
 *  - 'secuencia' : sys_sequences tiene trigger que PROHÍBE DELETE → UPDATE; las nuevas vuelven a
 *                  current_value = initial_value.
 *  - 'marca'     : tabla grande de solo inserción (auditoría) → DELETE id > marca. */
export const TABLAS = [
  ['cashiers', 'filas'],               // incluye bloqueo, isOpen, contador y los campos de IMPRESORA
  ['cashier_sessions', 'filas'],
  ['cash_movements', 'filas'],
  ['cash_transfers', 'filas'],
  ['cashier_reconciliations', 'filas'],
  ['cashier_reconciliation_details', 'filas'],
  ['cash_counts', 'filas'],
  ['cash_count_details', 'filas'],
  ['cashier_alerts', 'filas'],
  ['cashier_config', 'filas'],
  ['cash_denominations', 'filas'],     // SOLO las de company_id=43 (las globales tienen company_id NULL)
  ['cashier_device_requests', 'filas'],
  ['journal_entries', 'filas'],
  ['journal_entry_details', 'filas'],
  ['general_ledger', 'filas'],
  ['auto_posting_logs', 'filas'],
  ['accounting_periods', 'filas'],
  ['account_period_balances', 'filas'],
  ['user_company_preferences', 'filas'], // last_visited_route: a dónde aterriza cada usuario al entrar
  ['company_configs', 'solo-update'],  // cashier_station_mode (política «Estaciones de trabajo»)
  ['sys_sequences', 'secuencia'],      // MOV / REC / TRF / ALT / ASI de la empresa 43
  ['audit_logs', 'filas'],             // «Análisis › Auditoría» del video 7 necesita las filas de S1…S6
  // ── Video 8 «Cobrar una factura en la caja» (S8, autor video 8, 2026-09-23). Medido con conteos de
  // las 540 tablas con company_id antes/después de crear+emitir la factura y de cobrarla (efectivo+tarjeta).
  // En S0…S6 la empresa 43 tiene 0 filas en todas estas → restaurar un estado viejo las deja vacías (correcto).
  // NO se añaden `partners`/`partner_customer_profiles` (S0 ya trae «Consumidor Final» y «Proveedor Genérico»:
  // el cliente «Constructora Los Pinos» es maestro persistente) ni `customer_analytics`/`credit_settings`.
  ['products', 'filas'],
  ['prices', 'filas'],
  ['price_history', 'filas'],
  ['product_history', 'filas'],
  ['invoices', 'filas'],               // estado EMITIDA ↔ PAGADA
  ['invoice_details', 'filas'],
  ['invoice_tax_group', 'filas'],
  ['invoice_versions', 'filas'],
  ['entity_versions', 'filas'],
  ['accounts_receivable', 'filas'],    // saldo de la CxC que el cobro lleva a 0
  ['ar_payment_history', 'filas'],
  ['payment_applications', 'filas'],
  ['payments', 'filas'],               // recibo RCP-2026-…
  ['payment_details', 'filas'],        // una línea por método (efectivo / tarjeta)
  ['payment_changes', 'filas'],
  ['ncf', 'filas'],                    // NCF emitidos (B0100000001)
  ['customer_timeline_events', 'filas'],
  ['secuentials', 'solo-update'],      // rangos NCF: nacen con la empresa (21 filas en S0) → solo el contador
  ['subscriptions', 'solo-update'],    // S8 lleva el plan 15 (ver plan-s8.mjs); S0…S6 no la vuelcan → no la tocan
];

export const W = `company_id=${EMPRESA}`;
export const snap = t => `snap_${t}`;
