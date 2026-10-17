// node seeds/cajas/preparar.mjs S1|S2i
// Construye por API un estado a partir del canon anterior (restaura primero). Solo S1 se arma aquí:
// S3…S6 se fijaron desde el recorrido REAL por la UI de explorar.py (mismas acciones que los videos).
//   S1 = S0 + umbrales de alerta 1,000 / 60,000 (lo que guarda el video 2; la denominación «Veinte»
//        y la «Caja Mostrador 3» del video 1 NO se arrastran).
import { execFileSync } from 'node:child_process';
import { api, AQUI, log } from './_lib.mjs';

const estado = process.argv[2];
const node = (...a) => execFileSync('node', a, { cwd: AQUI, stdio: 'inherit' });

if (estado === 'S1') {
  node('restaurar.mjs', 'S0');
  await api('admin.progreso', 'POST', 'v1/cashier-config', {
    defaultInitialCash: 5000, toleranceAmount: 50, tolerancePercentage: 1, toleranceMode: 'AMOUNT',
    maxConsecutiveDifferences: 3, maxSessionDurationMinutes: 720,
    maxWithdrawalWithoutApproval: 5000, maxDepositWithoutApproval: 10000,
    requireNotesForWithdrawal: true, requireReconciliationForClose: true, blindCount: false,
    requireJustificationForDifference: true, reconciliationConfirmationHours: 24,
    allowOperationOnHolidays: false, alertThresholdLow: 1000, alertThresholdHigh: 60000,
  });
  log('S1 preparado (umbrales 1,000 / 60,000). Fijar con: node fijar.mjs S1');
} else if (estado === 'S2i') {
  // Paso «Impresora de esta estación» (solo Admin tiene CASHIER_UPDATE, ver _HALLAZGOS H-01):
  // S0 + sesión del admin en Caja Principal (el ⋮ «Ajustes de este equipo» solo sale con sesión propia en modo Flexible).
  node('restaurar.mjs', 'S0');
  await api('admin.progreso', 'POST', 'v1/cashiers/sessions/open', { cashier: 49, initialCash: 5000, notes: 'Prueba de impresora' });
  log('S2i preparado (admin con sesión en Caja Principal). Fijar con: node fijar.mjs S2i');
} else {
  console.error('uso: node preparar.mjs S1|S2i');
  process.exit(2);
}
