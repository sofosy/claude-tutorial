# Revisión semántica — Cajas 01, 02, 03, 04 (REVISOR, 2026-09-23)

Los cuatro videos ya pasaron la puerta mecánica (`veredicto.mjs` → PUBLICABLE). Esta revisión es
la parte semántica: SRT leído completo como novato, más 8-12 fotogramas por video extraídos con
`ffmpeg` en el instante exacto de cada afirmación verificable de la voz (cifras, estados, nombres
de botón, atribuciones), comparados contra la pantalla. Foco pedido por el usuario: el paso
«Configurar la impresora» del video 2, y si alguna columna/texto de la tabla del panel de
Configuración sale recortada al abrir el menú de una fila (video 1).

---

## cajas-01-tablero — VEREDICTO: NO PUBLICABLE

Presentación correcta («Este es el tablero de cajas», caja/sesión definidas antes de operar).
Cifras verificadas por fotograma y todas coinciden con la voz: 3 cajas (Abierta/Bloqueada/Cerrada),
Caja Mostrador 2 con Luis Batista y RD$6,050.00 (t=10s-38s), formulario de «Nueva caja» con Nombre
"Caja Mostrador 3", Código "CAJA-03", Ubicación "área de ventas, piso 2", métodos Efectivo+Tarjeta+
Transferencia, Fondo fijo vacío, mínimo 1,000/máximo 60,000 (t=89s-141s, todos los campos casan
con el guion). Capítulos de `youtube-video.txt`: 3, cumple.

### Hallazgos BLOQUEANTES
- **La tabla del panel «Configuración de cajas» queda recortada por la izquierda en cuanto se abre
  el menú de los tres puntos de una fila, y NO se recupera hasta que termina el paso.** Confirmado
  en fotogramas: a t=162s/174s/177s (antes de abrir el menú) la tabla se ve completa — «Caja
  Mostrador 3», «CAJA-03», «Caja Sucursal Santiago», «CAJA-SAN». En cuanto se pulsa el botón
  `more_vert` de la fila (t=191s, absoluto = 150.4s + 40.97s del informe), la tabla se desplaza
  ~15-20 px a la derecha y el primer carácter de la columna CAJA se pierde bajo el borde del panel:
  se lee «aja Mostrador 3», «AJA-03», «aja Sucursal Santiago», «AJA-SAN», «aja Mostrador 2»,
  «AJA-02» — la "C" inicial de cada nombre y cada código desaparece, y el encabezado de columna
  también queda «AJA» en vez de «CAJA». El recorte sigue igual en t=194s («Ver detalles»), t=199s
  («Archivar»), t=202s («Bloquear»), t=204s (con el menú ya cerrado, tab «Archivadas») y t=208s
  (cierre del panel con la equis) — es decir, se mantiene durante TODO el resto del paso
  03-panel-configuracion, justo mientras la voz dice «En los tres puntos de la fila de Caja
  Mostrador 3 están Ver detalles… Bloquear… y Archivar»: el espectador no puede leer el nombre
  completo de la fila que la voz está nombrando. Fotogramas guardados en
  `scratchpad/revision-semantica-1-4/v1/f_191.png`, `f_194.png`, `f_199.png`,
  `w_202.png`, `w_208.png`. No es ninguno de los falsos positivos conocidos (no es una fila ancha
  saliéndose por la derecha, ni la barra fija del pie): es la tabla completa desplazándose
  horizontalmente y perdiendo su borde izquierdo. `verificar.py`/`veredicto.mjs` no lo detectan
  porque miden visibilidad vertical, no este scroll horizontal.
  **Corrección sugerida**: en el guion, evitar que el clic en `more_vert` dispare el
  autoscroll horizontal de la tabla (fijar la columna CAJA o desplazar la tabla ANTES del clic,
  no dejar que el motor centre el botón del menú llevándose el borde izquierdo), o regrabar el
  grupo 03-panel-configuracion tras el ajuste. Bloqueante porque ocurre exactamente durante el
  tramo que el usuario pidió revisar.

### Mejoras opcionales
- A t≈33-36s (dentro de 01-tablero, marcas sobre `.board-card__amount` y `.board-card__holder` de
  Caja Mostrador 2), un tooltip nativo del navegador aparece encima del valor resaltado: a t=33s
  tapa «RD$6,050.00» con una fecha («23/09/2026 04:42», probablemente el título nativo de un campo
  vecino) y a t=34-36s tapa «luis.batista» con un tooltip truncado. La voz no afirma una cifra falsa
  en ese instante (dice solo «el efectivo que debería haber», sin número), así que no es un
  hallazgo de contenido, pero la marca pierde su propósito demostrativo un par de segundos.
  Fotogramas: `v1/f_33.png`, `v1/z_34.png`, `v1/z_35.png`. No bloquea publicación; para una futura
  regrabación, quitar el `title` nativo del elemento o acortar el `durante_ms` de esas dos marcas.

### Checklist youtube-video.txt
- capítulos: 3 (cumple)
- descripción en español: sí
- nombres internos/localhost: ninguno

---

## cajas-02-configuracion — VEREDICTO: PUBLICABLE

Presentación correcta («Este video reúne los ajustes que el administrador hace una sola vez»,
denominación definida antes de usarla). Foco pedido por el usuario — paso «Configurar impresora»
(desde 175.9s) — verificado a fondo: las dos casillas quedan claras en pantalla y en la voz
(«Imprimir recibo al facturar», ya marcada, saca el recibo al cobrar; «Abrir gaveta al facturar»,
sin marcar, abre la gaveta), fotogramas t=201s/206s casan exacto con «ya marcada»/sin marcar. El
botón «Detectar» se resalta (t=211s/223s) mientras la voz explica qué hace y POR QUÉ no se pulsa
aquí («pide permiso al navegador, así que aquí no lo pulso y los escribo a mano») — no hay ninguna
afirmación de que se haya detectado nada, y en pantalla los campos siguen vacíos hasta que se
escriben a mano. Vendor ID "0483" (t=228s) y Product ID "070b" (t=235s) coinciden letra por letra
con la voz («cero cuatro ochenta y tres», «cero setenta b»); Tipo de conexión "USB Directo
(WebUSB)" (t=244s) coincide con «USB Directo, la más común». El resto del video también verificado:
denominación «Veinte» / RD$20 creada y aparece al final de Billetes (6→7, t=12s/51s); Fondo inicial
por defecto RD$5000, Tolerancia RD$50, Diferencias consecutivas 3, Duración máxima 720 min (12
horas), «Permitir operación en días feriados» sin marcar — coincide con «en los días feriados no
se abre caja» (t=118s).

### Hallazgos BLOQUEANTES
- Ninguno.

### Mejoras opcionales
- Ninguna.

### Checklist youtube-video.txt
- capítulos: 4 (cumple) — 00:00 Denominaciones, 00:56 Políticas: fondo y tolerancias, 01:58
  Políticas: aprobaciones y cuadre, 02:58 Configurar la impresora
- descripción en español: sí
- nombres internos/localhost: ninguno

---

## cajas-03-abrir-y-operar — VEREDICTO: PUBLICABLE

Presentación correcta («Esta es la pantalla de Cajas», caja/sesión definidas antes de abrir una).
Fotogramas verificados: panel «Abrir mi caja» con Caja Principal ya elegida y Fondo inicial "5000"
(t=40s); desglose del efectivo tras abrir: Fondo inicial RD$5,000.00, Efectivo esperado RD$5,000.00
(t=95s); tras registrar la entrada de RD$2,000: Entradas (1) RD$2,000.00, Efectivo esperado
RD$7,000.00 (t=145s) — coincide con «sube a siete mil pesos»; panel de salida con Monto "6500",
Saldo disponible RD$7,000.00 (t=155s); ITBIS calculado con el botón de porcentaje: "991.53" exacto
(t=177s), coincide con «novecientos noventa y uno con cincuenta y tres»; tras crear la salida, el
Efectivo esperado sigue en RD$7,000.00 (t=218s), coincide con «no toca tu saldo… sigue en siete
mil»; lista de Movimientos con la Salida en naranja «Por aprobar» y la Entrada en verde
«Completado» (t=218s), coincide exacto con la voz. El campo «Cajero» del panel «Abrir mi caja»
muestra el correo (yohanna.peralta@germiva.demo, t=40s) en vez del username que usa el resto del
sistema — es el hallazgo conocido H-14 del ERP, la voz no afirma nada sobre ese formato, así que no
es un defecto del guion.

### Hallazgos BLOQUEANTES
- Ninguno.

### Mejoras opcionales
- Ninguna adicional (H-14 es defecto del ERP, no del video; ya documentado en `_HALLAZGOS-CAJAS.md`).

### Checklist youtube-video.txt
- capítulos: 4 (cumple) — 00:00 Abrir la caja, 01:14 Registrar una entrada, 02:30 Salida con ITBIS
  por aprobar, 03:43 Movimientos y resumen del turno
- descripción en español: sí
- nombres internos/localhost: ninguno

---

## cajas-04-aprobar-y-transferir — VEREDICTO: PUBLICABLE

Presentación correcta («Esta es la bandeja Por aprobar de la supervisora», con «cuatro ojos»
explicado antes de aprobar). Fotogramas verificados: cifras iniciales 1 movimiento por aprobar / 0
transferencias / 0 cuadres / 1 alerta activa / 1 caja bloqueada (t=12s), coincide exacto con «un
movimiento por aprobar, ninguna transferencia ni cuadre pendiente, una alerta activa y una caja
bloqueada»; fila MOV-2026-00010, RD$6,500.00, Caja Principal, solicitado por yohanna.peralta, nota
de mantenimiento del aire — coincide con «la cajera Yohanna Peralta, con su nota»; tras aprobar,
0 movimientos y 2 alertas activas (t=72s), coincide con «ahora son dos»; formulario de transferencia
con Caja origen "Mostrador 2", Saldo disponible en sesión RD$6,050.00 (t=118s/127s) — coincide con
«seis mil cincuenta pesos»; tras crear la transferencia, fila TRF-2026-00001 en estado «Por recibir»
(t=145s); diálogo «Recibir transferencia» con monto RD$3,000.00, origen Mostrador 2, destino
Principal (t=168s), coincide con la voz; balances finales en el tablero: Caja Principal
RD$3,500.00 (t=195s) y Caja Mostrador 2 RD$3,050.00 (t=204s, la marca sobre Mostrador 2 llega unos
segundos después de lo estimado por el informe pero SÍ aparece antes de que termine el video),
coinciden exacto con «tres mil quinientos» / «tres mil cincuenta». Las notas de la transferencia se
dejan en blanco a propósito y la voz dice que son opcionales — evita mostrar el bug conocido H-15
(la nota no se guarda por un desajuste `notes`/`reason` entre front y API); no hay afirmación falsa.

### Hallazgos BLOQUEANTES
- Ninguno.

### Mejoras opcionales
- Ninguna.

### Checklist youtube-video.txt
- capítulos: 3 (cumple) — 00:00 Aprobar una salida, 01:23 Crear una transferencia, 02:31 Recibir la
  transferencia
- descripción en español: sí
- nombres internos/localhost: ninguno

---

## Resumen para publicar

**3 de 4 PUBLICABLES sin cambios**: cajas-02-configuracion, cajas-03-abrir-y-operar y
cajas-04-aprobar-y-transferir tienen cero afirmaciones falsas, cero marcas apuntando a lo contrario
de lo que dice la voz, cero dato real o «QA-*», cero defecto conocido del ERP enseñado como si fuera
correcto, y sus `youtube-video.txt` ya cumplen (≥3 capítulos, español, sin nombres internos).

**cajas-01-tablero queda NO PUBLICABLE por un solo bloqueante real**: la tabla del panel
«Configuración de cajas» se desplaza y recorta la columna CAJA (nombre y código) desde que se abre
el menú de los tres puntos de una fila hasta el cierre del panel — justo durante el tramo que
enseña «Ver detalles / Bloquear / Archivar» de Caja Mostrador 3. No es un falso positivo conocido
de la skill; hace falta ajustar el guion (evitar el autoscroll horizontal al abrir el menú, o fijar
la columna) y regrabar el grupo `03-panel-configuracion` antes de publicar. El resto del video
(tablero, alta de caja) está limpio; hay además una mejora opcional no bloqueante sobre un tooltip
nativo que tapa dos marcas del tablero durante 2-3 s.
