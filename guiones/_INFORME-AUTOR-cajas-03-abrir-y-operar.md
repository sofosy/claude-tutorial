# Informe del autor — cajas-03-abrir-y-operar (2026-09-23)

- **Graba:** `yohanna.peralta` (Cajera). **Parte de:** S1 (`node seeds/cajas/restaurar.mjs S1`).
- **Pasos:** 01-abrir-sesion · 02-entrada · 03-salida-pendiente · 04-resumen. Duración prevista 3:59 (revisar.mjs, 3 p/s).
- **Qué escribe:** sesión de yohanna en Caja Principal (fondo 5,000, «Turno de la mañana»); MOV-2026-00009 entrada 2,000
  (cuenta 116, «Cambio en monedas traído del banco»); MOV-2026-00010 salida 6,500 / ITBIS 991.53 (cuenta 167,
  «Pago del mantenimiento del aire acondicionado») **POR APROBAR**; esperado 7,000.
- **Puertas:** `tut verificar` 0 errores · `revisar.mjs` 0 ERROR · ensayo bajo NAVEGADOR.lock (restaurar S1 → ensayar →
  restaurar) 48 acciones OK, 0 fallos, todo «visible=entero». La BD al terminar el ensayo es idéntica a S3 en montos,
  estados, cuentas, notas, asientos y secuencias (foto sin ids ni fechas comparada con `restaurar S3`).
- **AVISO justificado:** «el primer paso no contrae el menú» — en Cajas no existe `button.panel-collapse` (riel fijo).
- **No se enseñan defectos:** no se abre «Detalle del movimiento» (H-02: «Autorizado por» sale el cajero); el panel
  «Abrir mi caja» muestra el correo (H-14) y la voz solo dice «a tu nombre»; el aviso naranja de contrapartida pisa la
  etiqueta (H-03) — se marca el campo «Contrapartida», no el aviso.
- **Dudas:** ninguna bloqueante. Si la voz real sale más lenta de 3 p/s el video podría pasar de 4:00; margen hasta 4:10.
