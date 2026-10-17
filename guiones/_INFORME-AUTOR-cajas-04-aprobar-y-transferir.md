# Informe del autor — cajas-04-aprobar-y-transferir (2026-09-23)

- **Graba:** `carmen.rosario` (Supervisora de Caja). **Parte de:** S3 (`node seeds/cajas/restaurar.mjs S3`).
- **Pasos:** 01-por-aprobar · 02-nueva-transferencia · 03-recibir. Duración prevista 2:57 (revisar.mjs, 3 p/s).
- **Qué escribe:** aprueba MOV-2026-00010 (asiento ASI de la salida; nace ALT-2026-00002 saldo bajo 500 < 1,000);
  TRF-2026-00001 3,000 Caja Mostrador 2 → Caja Principal, recibida (MOV-00011/00012; la alerta se resuelve sola).
  Cierra en el tablero: Principal RD$3,500.00, Mostrador 2 RD$3,050.00.
- **Puertas:** `tut verificar` 0 errores · `revisar.mjs` 0 ERROR · ensayo bajo NAVEGADOR.lock (restaurar S3 → ensayar →
  restaurar) 39 acciones OK, 0 fallos, todo «visible=entero». BD al terminar idéntica a S4 (foto sin ids ni fechas
  comparada con `restaurar S4`).
- **AVISO justificado:** «el primer paso no contrae el menú» — en Cajas no existe `button.panel-collapse` (riel fijo).
- **HALLAZGO NUEVO H-15 (no corregido):** la nota de «Nueva transferencia» NO se guarda. El front envía `notes`
  (`germiva-website/.../cash-transfer-form/cash-transfer-form.component.ts:343`) y el DTO espera `reason`
  (`Germiva-api/src/modules/cashiers/dto/create-cash-transfer.dto.ts:55`): `cash_transfers.notes` y `.reason` quedan NULL
  (también en el canon S4). El guion deja las notas en blanco («son opcionales; esta vez las dejo en blanco»).
  Conviene añadirlo a `_HALLAZGOS-CAJAS.md` (no lo toqué para no pisar a los otros autores).
- **Dudas:** «Como no pasa del límite de cinco mil, no necesita aprobación» sale del plan de la serie (la transferencia
  de 3,000 nace «Por recibir» sin aprobación, verificado); no probé una de más de 5,000.
