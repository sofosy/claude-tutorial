# Informe de autor — cajas-06-cuadre-y-desbloqueo

- **Graba**: carmen.rosario (Supervisora de Caja). **Parte de S5** (`restaurar.mjs S5`), **llega a S6**.
- **Escribe**: aprobación de REC-2026-00007 (con su asiento del faltante), arqueo sorpresa REC-2026-00008 por 3,050 sobre la sesión abierta de luis.batista (queda Pendiente), desbloqueo de «Caja Sucursal Santiago» (nota «Arqueo revisado con la gerencia», contador reseteado). Restaurar S5 entre tomas.
- **Pasos**: 01-aprobar-cuadre (Por aprobar → detalle → Resultado, motivo, «Reconteo de supervisión» y «Corregir el conteo» señalados sin usar, «Rechazar»/«Aprobar» explicados, bloqueo automático a 3 → Aprobar + segunda confirmación → toast) · 02-arqueo-sorpresa (Historial › Cuadres › «Nuevo cuadre» → sesión Mostrador 2, tipo «Arqueo sorpresa», «Continuar», 3050, «Siguiente», «Generar cuadre» → toast) · 03-desbloquear (tablero filtrado Bloqueadas → «Desbloquear» → diálogo → toast → «Todas» → tarjeta Cerrada).
- **AVISOS justificados**: primer paso sin `button.panel-collapse` (no existe en Cajas).
- **Hallazgos evitados**: H-13 («Bloqueado por Sistema») no se nombra ni se marca (solo la razón y la fecha); H-06 (texto genérico de la segunda confirmación) se muestra sin leerlo; H-11 no se menciona.
- **Riesgo conocido**: «Continuar» de Generar cuadre choca con el FAB (H-09); ver resultado del ensayo.
