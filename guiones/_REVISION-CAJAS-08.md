# Revisión semántica — Cajas 08 · «Cobrar una factura con pago combinado» (REVISOR, 2026-09-23)

Video ya pasado por la puerta mecánica (`veredicto.mjs` → PUBLICABLE, 1 falso positivo conocido
descartado). Esta revisión es la parte semántica: SRT completo (75 líneas) leído como novato, 24
fotogramas extraídos con `ffmpeg` en `scratchpad/revision-semantica-8/` en los instantes exactos de
cada cifra/estado verificable (offset de video = 3 s de marca de entrada + tiempo acumulado del
informe), más lectura de `informe-video.md`, `revisar.log`, `veredicto.log`, `youtube-video.txt`,
`cajas-08-cobro-factura.json`, `_INFORME-AUTOR-cajas-08-cobro-factura.md` y `_HALLAZGOS-CAJAS.md`.
Pedido del usuario: verificar la conexión factura↔caja, el pago combinado y las 6 preguntas
puntuales de su encargo.

## cajas-08-cobro-factura — VEREDICTO: PUBLICABLE

### (1) Conexión factura↔caja, clara para un novato — SÍ
El guion arma la idea en el orden correcto: "cuando cobras una factura, el dinero entra a la caja
que tienes abierta" (0:03) → muestra Mi caja con cobros en cero y esperado = solo el fondo (0:14-
0:27, fotograma f_22.5.png: FONDO INICIAL RD$5,000 / COBROS EN EFECTIVO RD$0.00 marcado) → abre la
factura y señala la etiqueta verde "Caja Principal · Sesión #523" diciendo "ahí va a entrar este
dinero" (1:12-1:19) → cobra → vuelve a Mi caja y cierra el círculo: "los cobros en efectivo subieron
a cinco mil... el efectivo esperado ahora es diez mil" (3:28-3:38, fotogramas f_203.5.png/f_206.4.png:
COBROS EN EFECTIVO RD$5,000 / EFECTIVO ESPERADO RD$10,000, exacto). La tarjeta se explica aparte y
correctamente: "¿Y la tarjeta? Aquí no suma, porque ese dinero no está en la gaveta: lo deposita el
banco" (3:33-3:40) y el cuadre confirma el reparto por método (fotograma check_237.6.png/check_241.9.png:
Efectivo esperado RD$10,000 / Tarjeta esperado RD$3,850, ambos "Sin diferencia"). NCF, ITBIS, B01 y
sesión quedan definidos la primera vez que se nombran, con fonética correcta en el guion
(`itebís`, `ene-ce-efe`, `de-ge-i-i`, `be cero uno`). Pago combinado se explica por la acción misma
("el cliente paga una parte en efectivo y otra con tarjeta, así que marco «Pago combinado»").

### (2) Cifras contra fotograma — TODAS COINCIDEN
Verificado con ≥10 fotogramas (24 extraídos): fondo 5,000 y esperado 5,000 antes de cobrar
(f_22.5.png); factura Borrador RD$8,850.00 en el listado (f_41.9.png); banner del NCF/B01 y líneas
de producto 10×cemento+20×varilla con ITBIS 1,350 visibles (h_79.4.png); "Falta RD$3,850.00" tras
cargar el efectivo (h_115.5.png, exacto con la voz "tres mil ochocientos cincuenta"); diálogo
"Cobro procesado" con Efectivo RD$5,000 + Tarjeta RD$3,850 (g_155.3.png) y clic en Aceptar
perfectamente centrado en el botón (g_160.3.png); factura recargada "Pagada" con NCF
B0100000001 (g_164.0.png/g_167.4.png); pestaña Pagos con recibo RCP-2026-000001, dos líneas
5,000 efectivo / 3,850 tarjeta (f_182.7.png/f_185.5.png); Mi caja después (f_203.5.png/f_206.4.png);
cuadre con Cobros del turno RD$8,850 y desglose por método (f_212.3.png/f_225.2.png/check_237.6.png).
Ningún desfase de contenido.

### (3) Franja naranja «Facturación electrónica deshabilitada» — NO se explica, riesgo bajo
Confirmado en fotograma (f_55.0.png, h_79.4.png, g_164.0.png): la franja ocupa dos líneas justo
debajo del encabezado de la factura, TODO el tiempo que la factura está en pantalla (borrador y ya
pagada), exactamente en la zona donde segundos después la voz explica NCF/DGII. La voz nunca la
nombra. No dice nada falso (no confunde activamente), pero es un elemento visualmente prominente y
temáticamente adyacente al NCF que un espectador atento notará sin que se le aclare qué es "e-CF" ni
por qué está deshabilitado. El informe del autor ya lo documentó como decisión consciente
("informativa y fija... no se comenta"). **MEJORA, no bloqueante**: una frase de 3-4 s bastaría
("La franja naranja de arriba avisa que esta empresa no emite el comprobante electrónico a la DGII;
aun así, el NCF sí se asigna y la factura queda válida").

### (4) Pantalla en blanco tras «Aceptar» — BREVE, no bloquea
Medido fotograma a fotograma (0.5 s de paso): blanco puro de t≈160.3s a t≈161.7s (~1.4 s), luego
esqueleto de carga (`skeleton`) hasta t≈163.8s (~2.1 s más), contenido real ya legible en t=164.0s.
Total ~3.5 s de pantalla no definitiva, de los cuales solo ~1.4 s es blanco puro — muy por debajo
del límite de 10 s de R0. La narración cubre el hueco: "Pulso «Aceptar»" termina en el SRT a 2:41.9
y la siguiente frase ("Al aceptar, la factura se vuelve a cargar, ya cobrada") empieza a 2:43.3,
dejando ~1.4 s de silencio que coincide justo con el tramo en blanco. No es un defecto.

### (5) Ningún hallazgo H-xx enseñado como correcto — CONFIRMADO
H-19 (RD$0.00 + "Este dato es requerido" en rojo tras el último método, fotograma check_142.8.png):
la voz lo cubre ANTES de que aparezca ("el formulario de arriba se vacía, listo para otro método,
pero ya no hace falta"), sin llamarlo error ni afirmar que está vacío por otra razón — correcto.
H-22 ("Total esperado en caja" RD$13,850, visible en fotograma f_225.2.png/check_237.6.png): la
cifra está en pantalla pero la voz nunca la nombra ni la usa como si fuera el efectivo esperado;
solo dice "Cobros del turno... ocho mil ochocientos cincuenta, sin importar el método" (que sí es
correcto) y explica el efectivo/tarjeta por separado. No se enseña ningún dato incorrecto como
válido. H-18 (columna ESTADO vacía en Pagos) tampoco se señala ni se afirma nada sobre ella.

### Falsos positivos del informe descartados con fotograma
- `informe-video.md` marca la alerta "Cobro procesado" (102.8s) como "no se señaló ni se explicó".
  Es el patrón conocido: la marca `resaltar` cae a 102.78s, la sonda detecta el diálogo 0.03s
  después (102.81s) — `veredicto.log` ya lo descarta explícitamente como falso positivo. Confirmado
  con fotograma (g_155.3.png): el diálogo está completo en pantalla, con el clic en "Aceptar"
  perfectamente anclado (g_160.3.png). No es un hallazgo real.
- `revision/clics.png` (hoja de contactos) muestra 2 miniaturas en blanco/negras para
  "02-cobro-combinado 90.4s «factura»" y "04-caja-y-cuadre 39.1s/43.5s". Verificado por `ffmpeg`
  directo sobre `video.mp4` en esos mismos instantes (check_142.8.png, check_237.6.png,
  check_241.9.png): el contenido real está completo y correcto. Es un artefacto de la herramienta de
  contacto (fallo de captura puntual en `revision/`), no un defecto del video publicado.

### (6) youtube-video.txt
4 capítulos (00:00, 00:52, 02:43, 03:18) y coinciden con los arranques reales de cada paso (±0.5s);
descripción en español, sin `localhost` ni usuarios de QA; duración anunciada 04:21 = duración real
del archivo (261.47s = 4:21.47). En orden.

### Mejoras opcionales (no bloqueantes)
- Añadir una frase breve sobre la franja naranja de facturación electrónica deshabilitada (punto 3).

No hay hallazgos BLOQUEANTES. Verdicto se mantiene: **PUBLICABLE**.
