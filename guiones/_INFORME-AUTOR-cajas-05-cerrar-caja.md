# Informe de autor — cajas-05-cerrar-caja

- **Graba**: yohanna.peralta (Cajera). **Parte de S4** (`node seeds/cajas/restaurar.mjs S4`), **llega a S5**.
- **Escribe**: conteo de cierre REC-2026-00007 (3,480; −20 dentro de ±50; justificación «Faltan 20 pesos en monedas») PENDIENTE y la sesión de Caja Principal CERRADA. Restaurar S4 entre tomas.
- **Pasos**: 01-cerrar-caja (desglose hasta el esperado 3,500 → «Cerrar caja» → «Conteo de cierre requerido» → «Iniciar conteo») · 02-ingresar-montos (resumen, «Ver cálculo», 3480, diferencia y tolerancia, justificación, «Siguiente») · 03-registrar-conteo (totales, aviso verde, «Registrar conteo», toast, vuelta a Mi caja sin sesión).
- **AVISOS justificados**: «el primer paso no contrae el menú» — en Cajas no existe `button.panel-collapse` (riel fijo, ver _BRIEF).
- **Hallazgos evitados**: H-04 («0 transacciones» bajo el esperado) no se nombra; se marca la cabecera «Monto esperado», no la celda.
- **Dudas**: ninguna de contenido. Las cifras se dicen en palabras (la voz leería «3,500» como decimal).
