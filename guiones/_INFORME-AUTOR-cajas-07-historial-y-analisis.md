# Informe de autor — cajas-07-historial-y-analisis

- **Graba**: carmen.rosario. **Parte de S6** (`restaurar.mjs S6`). **Solo lectura**: no reconoce alertas ni reabre nada; no hace falta restaurar (se restaura igual por higiene).
- **Pasos**: 01-historial-de-una-caja (⋮ de Caja Principal › «Sesiones» → Historial filtrado; «Ver detalles» y «Reabrir» señalados; Movimientos; Cuadres con «Anular cuadre» señalado) · 02-analisis (cifras en vivo, Reporte diario con Período «Este mes», Cuadres y análisis, Rendimiento) · 03-alertas-auditoria (alerta de saldo bajo **Resuelta** — la voz lo dice —, la de caja bloqueada resuelta, filtro Estado; Auditoría y sus filtros).
- **AVISOS justificados**: primer paso sin `button.panel-collapse` (no existe en Cajas).
- **Hallazgos evitados**: H-02 (columna «Autorizado por») no se marca ni se nombra; H-12: la voz dice la regla real de «Reabrir» sin pulsarlo; H-10: la voz dice «Este mes».
- **Dudas**: la IP «::1» sale en la columna IP de Auditoría (no es dato personal; se deja).
