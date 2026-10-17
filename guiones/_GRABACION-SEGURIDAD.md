# Grabación · serie «Seguridad»

## Tanda 1 (OPERADOR-GRABACIÓN, 2026-09-27)

Build final: API `dist` en :3001 y front estático en :4200, sin reiniciar. Se grabó con
`seeds/seguridad/grabar-serie.sh` (copia adaptada de `seeds/cajas/grabar-serie2.sh`), lanzado DESACOPLADO con
`Start-Process` (R19). El script pasa la puerta 1, toma el cerrojo con dueño, restaura, graba, restaura E0 y emite
el veredicto. Log: `seeds/seguridad/serie.log`.

Se lanzaron tres corridas: 16:42 (los seis videos), 17:19 (00, 01 y 02a) y 17:36 (02a). Cada `video.mp4` es
posterior al arranque de su corrida. Al terminar quedaron **E0** restaurado y el cerrojo libre.

Antes de grabar se repitió el ensayo con el build final: restaurar, revisar, `ensayar.py` bajo cerrojo y restaurar.
Resultado: **0 fallos y 0 CORTADO** en los seis. `tut.py verificar` dio 0 errores y 0 avisos. Las capturas del
ensayo están en `germiva/qa-seguridad-grabacion-2026-09-27/_ensayo/`. En los seis videos, `huecos.mjs` da 0 tramos
de más de 10 s.

| Guion | Duración (con marca 3+3 s) | Veredicto | Tomas | Regrabaciones (motivo) | OCR |
|---|---|---|---|---|---|
| seguridad-00-introduccion | **3:32** (contenido 3:26) | PUBLICABLE | 2 | 1 · la fase 6 del diagrama salió 9,3 s antes: el ancla «credencial de API» no casaba | 0 |
| seguridad-01-resumen | **3:46** (3:40) | PUBLICABLE | 2 | 1 · el candado entró +1,0 s tarde (paso 01) y la marca «Credenciales de API» salió −1,0 s (paso 04) | 0 |
| seguridad-02a-roles | **3:51** (3:45) | PUBLICABLE | 3 | 2 · el candado y la pestaña entraron +1,5 s tarde; luego el diálogo «Crear Rol» quedó sin marca | 0 |
| seguridad-02b-editor-permisos | **4:33** (4:27) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-03-herencia | **4:34** (4:27) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-09-lo-que-se-movio | **3:20** (3:14) | PUBLICABLE | 1 | 0 | 3 lecturas justificadas: `130955036` es el RNC ficticio 130555036 mal leído porque el cursor tapa el «5» (fotograma de 133 s) |

Las regrabaciones fueron de videos enteros, porque cada paso encadena estado y sesión.

### Capítulos (`salida/<guion>/youtube-video.txt`)

- **00-introduccion**:
  - 00:00 Bienvenida
  - 00:41 Los seis conceptos
  - 01:43 La consola
  - 02:38 Caso práctico: las cinco pestañas
- **01-resumen**:
  - 00:00 Las cinco cifras
  - 01:04 Requiere atención
  - 01:58 Actividad reciente
  - 03:01 Caso práctico: la revisión semanal
- **02a-roles**:
  - 00:00 La lista de roles
  - 01:11 Un rol del sistema
  - 02:00 Duplicar un rol
  - 02:43 Crear un rol nuevo
- **02b-editor-permisos**:
  - 00:00 Cómo se lee el editor
  - 01:14 Conceder permisos
  - 02:11 El alcance
  - 02:52 Buscar un permiso
  - 03:33 Guardar y revisar
- **03-herencia**:
  - 00:00 Qué es la herencia
  - 00:59 Crear un rol hijo
  - 01:54 Excluir un permiso heredado
  - 02:37 Eliminar un rol
  - 03:14 Caso práctico: quién tiene el rol
  - 03:53 Caso práctico: qué le cambiaron
- **09-lo-que-se-movio**:
  - 00:00 Tu contraseña, en Mi perfil
  - 00:59 Visibilidad del menú
  - 01:54 Perfil del Consultorio
  - 02:24 El enlace viejo del historial
  - 02:50 Caso práctico: los enlaces viejos

### Cambios en los guiones

- **02b · paso 01 (E-1)**: la voz ahora dice «al elegir un rol, el editor abre el primer módulo donde ya concede
  algo: aquí, Clientes y Proveedores». Lleva una marca nueva, `.rpe__module.gm-rail-btn--active`, al decir «primer
  módulo». El fotograma de 29,9 s confirma que Vendedor abre «Clientes y Proveedores 1/33».
- **03 (E-1)**: solo cambia el `_comentario`. La voz no nombra el módulo con que se abre el editor, así que sigue
  siendo cierta: Vendedor sénior abre «Clientes y Proveedores».
- **00 · paso 02**: el ancla «credencial de API» pasa a «Y la credencial».
- **01 · paso 04**: el ancla «Credenciales de API» pasa a «Credenciales». El paso 01 abre con «En este video
  recorremos el Resumen de Seguridad.».
- **02a · paso 01**: abre con «En este video vemos los roles de tu empresa.». En el paso 04 se añade una marca
  `mat-dialog-container` al decir «Se abre Crear Rol» (R10).
- **E-12**: no afectó a ninguna marca de estos seis guiones (0 CORTADO en ensayo y en toma).

### Lecciones para las tandas 2 y 3

- **El motor no aplica la `pronunciacion` del guion a las anclas.** `grabar.py: instante` llama a
  `m_narrar.para_voz(clave)` sin el mapa `extra` del guion, así que solo usa el mapa global. Con una sigla que solo
  está en el `pronunciacion` del guion (API, IP…), un ancla como «de API» nunca casa y la acción se dispara en
  cuanto puede, sin avisar. `revisar.mjs` no lo detecta. Mientras no se arregle el motor, **no pongas siglas del
  `pronunciacion` del guion dentro de un `al_decir`**. Atención con 06a/06b/06c: la API sale por todas partes.
- **El primer clic de un video no cae antes de ~2,3 s.** Si la palabra del primer clic suena antes de ~3 s, el
  clic llega tarde. Hay que dejar una frase de entrada antes.
- **Un diálogo de trabajo necesita una marca en ≤ 8 s.** Si no la tiene, `veredicto.mjs` decide según cómo la
  sonda detecte el diálogo en esa toma: en unas lo descarta como falso positivo y en otras lo cuenta como FALLO
  (02a: toma 1 descartado, toma 2 FALLO).

## Tanda 2 (OPERADOR-GRABACIÓN, 2026-09-27)

Build final (API `dist` :3001, front estático :4200), sin reiniciar. Mismo procedimiento que la tanda 1: re-ensayo con
`ensayar.py` bajo cerrojo (restaurar antes y después; E6c + `preparar.mjs --estatico` en 06b/06c), `tut.py verificar`
0 errores, grabación DESACOPLADA con `Start-Process` → `seeds/seguridad/grabar-serie.sh`, veredicto, `huecos.mjs`,
`tut.py auditar --video` y revisión visual propia (10–12 fotogramas y una hoja `_hoja.png` por video en
`germiva/qa-seguridad-grabacion-2026-09-27/<guion>/`; capturas del ensayo en `…/_ensayo/`). Corridas: 18:24 (los
siete), 19:18 (04b, 06a, 06b, 06c; 06c no pasó la puerta 1), 19:38 (06c) y 19:59 (04b, 06a). Cada `video.mp4` es
posterior al arranque de su corrida. Al terminar: **E0** restaurado y cerrojo libre. `huecos.mjs`: 0 tramos > 10 s en
los siete.

`grabar-serie.sh` corre ahora `node marca/demo-integracion/preparar.mjs --estatico` después de restaurar E6c (antes no
lo hacía).

| Guion | Duración (con marca 3+3 s) | Veredicto | Tomas | Regrabaciones (motivo) | OCR |
|---|---|---|---|---|---|
| seguridad-04a-personas | **4:11** (4:05) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-04b-alta-y-edicion | **5:02** (4:56) | PUBLICABLE | 3 | 2 · toma 1: las escrituras de usuarios tardaron ≈2,5× el ensayo (alta 21,7 s, eliminar ≈19 s) → 11 fallos de tiempo; toma 2 PUBLICABLE pero la voz decía «vuelve a Activa» y la fila dice «Pendiente» (G-11) | 0 |
| seguridad-04c-equipos | **3:58** (3:52) | PUBLICABLE | 1 | 0 | 1 lectura justificada: `pIenel@yertiiva.uenie` es carlos.pimentel@germiva.demo mal leído |
| seguridad-05-acceso-efectivo | **2:59** (2:53) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-06a-credenciales | **4:30** (4:24) | PUBLICABLE | 3 | 2 · toma 1: generar la credencial tardó 12 s y la página de permisos 8,4 s; toma 2 PUBLICABLE pero la marca de relleno caía detrás del diálogo (G-12) | 0 |
| seguridad-06b-rotar-pausar-revocar | **3:27** (3:21) | PUBLICABLE | 2 | 1 · rotar 11,5 s, desactivar/activar 10,5–11 s y revocar 12,2 s: marcas +4 a +6 s tarde y un tramo quieto de 11 s | 0 |
| seguridad-06c-caso-integracion | **3:14** (3:08) | PUBLICABLE | 2 | 1 · la lámina servida con `rutas_locales` no llegaba al API (Chromium bloquea el loopback, G-9) y el paso 04 se alargó 74 s por la pasada de privacidad sobre la página de permisos (G-10) | 12 lecturas justificadas: `1000000003`, `B0200000001` y `B0100000001` son los números de comprobante ficticios de F3, F2 y F1 leídos como RNC |

04b dura más de 4:10 porque la voz tiene que cubrir las escrituras lentas del entorno local (G-8). Si en producción
tardan lo que en el ensayo, este video se puede recortar.

### Capítulos (`salida/<guion>/youtube-video.txt`)

- **04a-personas**: 00:00 La lista de personas y sus vistas · 01:10 Buscar y filtrar por rol · 02:00 La ficha de una
  persona · 03:06 Ver su actividad · 03:31 Caso práctico: la cuenta que nunca se usó
- **04b-alta-y-edicion**: 00:00 Dar de alta a una persona · 01:46 Editar y cambiar la contraseña · 02:33 Asignar otro
  rol · 03:19 Desactivar y activar · 04:19 Eliminar y caso práctico
- **04c-equipos**: 00:00 Qué es un equipo · 00:55 Crear un equipo · 01:35 Agregar miembros · 02:17 Quitar, editar y
  eliminar · 03:09 Cuando no queda ningún equipo
- **05-acceso-efectivo**: 00:00 Cómo se calcula · 00:51 La herencia en la ficha · 01:31 Dos roles suman · 02:09 El
  equipo no suma · caso práctico
- **06a-credenciales**: 00:00 Qué es una credencial de API · 00:52 Crear una credencial · 02:00 Guardar el secreto ·
  02:41 El panel de la credencial · 03:23 Quitarle lo que no necesita
- **06b-rotar-pausar-revocar**: 00:00 Rotar el secreto · 00:59 Pausar y reactivar · 01:51 Revocar una credencial ·
  02:39 La documentación de la API
- **06c-caso-integracion**: 00:00 El programa del contador · 00:42 Consulta permitida · 01:15 Consulta no permitida ·
  01:47 Conceder el permiso · 02:41 La misma consulta, ahora permitida

### Cambios en los guiones

- **04c (E-6)**: en el paso 01 la voz dice «a su lado dice cuántas personas lo forman», con una marca sobre el botón de
  Zona Este. El paso 03 cierra con «Y en el riel, Zona Norte ya dice dos personas», con su marca.
- **06a**: el paso 01 abre con «En este video vemos las credenciales.», para que el primer clic no caiga antes de 3 s.
  El paso 05 ya no usa el buscador (G-5). Baja a «Registrar Facturas de Compra» dentro de Facturación, que sale
  abierto, y la desmarca. En el paso 02 hay voz de relleno durante «Generando…», con una marca sobre ese botón. En el
  paso 05 se explica que la página tarda porque trae más de mil permisos.
- **06c**: se quitó `rutas_locales` (G-9). El paso 04 abre el módulo Productos (0/42) y marca su primera casilla,
  «Productos», sin usar el buscador. Termina con «Volver a Integraciones», donde el panel ya cuenta cinco permisos
  (G-10). El paso 05 añade una marca en «valió al instante».
- **04b, 06a, 06b (G-8)**: cada operación lenta tiene ahora voz de relleno y una marca cada ≤ 8 s, sobre elementos que
  existen tanto si la operación tarda 3 s como si tarda 20. El aviso sin ancla va después del relleno. En 04b se
  quitaron la aclaración del WhatsApp y la de «si el usuario ya existe». La voz de «Activar» dice ahora «vuelve a
  Pendiente» (G-11).
- **06b (E-7)**: el paso 04 no cambió. La documentación ya se ve dentro del shell, con el índice entero y el título «API
  externa de Germiva — Referencia de endpoints». La voz no lee el título.
- **Anclas con «API»**: el motor ya aplica la `pronunciacion` del guion (commit 1f700d7). En 06b, el ancla
  «Documentación de la API» cayó en su palabra.

### Lecciones para la tanda 3

- **Las escrituras son 2,5–3 veces más lentas en la toma que en el ensayo.** Hay que calcular cada espera con los
  tiempos de G-8, no con los del ensayo. Un aviso sin ancla espera como mucho 15 s desde la acción anterior, así que
  necesita relleno con marcas antes.
- **`revisar.mjs` sin `--audio` es la puerta de `grabar-serie.sh`.** Un guion que pasa con `--audio` puede fallar sin
  él, como le pasó a 06c. Hay que pasar las dos.
- **No uses `rutas_locales` para una página que llama al API local:** sírvela desde el estático.
- **No termines un paso en la página de permisos entera:** la pasada de privacidad tarda más de un minuto.
- **Revisa con fotograma el estado que la voz afirma.** Una cuenta que nunca entró sale «Pendiente» y no «Activa».

## Tanda 4 · regrabación con el build 4 (OPERADOR-REGRABACIÓN, 2026-09-27)

Build 4 (API `dist` :3001 PID 10444, estático :4200 PID 7752), sin reiniciar. Cambios del ERP/motor que motivan la
tanda: G-1 (etiquetas «Inventario · Productos»… también en eventos viejos), contador «N de M permisos» del editor, G-5
(el buscador de Permisos de Integración filtra), G-6 (esqueletos en lugar de «Todas · 0» / «Sin equipos todavía» /
«0 eventos»), G-7 («1 llamada»), cartel sobre lámina en la primera esquina libre y `mapa_fijo` ::1→192.168.1.25.

**Revisión B de la tanda 2** (fotogramas en +0,3/0,8/1,4/2,2 s de cada entrada a Personas/Auditoría/Integraciones y
de cada panel de credencial, `germiva/qa-seguridad-grabacion-2026-09-27/_revision-t2/`): 04a («Todas · 0», «Sin
equipos todavía», «Mostrando 0» a 9,1 s y «0 eventos» a 193 s), 04b, 04c y 05 («Todas · 0» + «Sin equipos todavía»
al cargar) y 06c («1 llamadas en total», 2:40) → **se regrabaron**. 06b: sin ninguno de esos estados (paneles «0
llamadas» y «412 llamadas») → **sin cambios**. 06a: `_INVENTARIO-SEGURIDAD-FE.md` F-191 incluye el buscador «Buscar
permisos» y la cobertura asigna F-191 a 06a/05 → se añadió el tramo del buscador y **se regrabó**.

Procedimiento: puerta 1 (`revisar.mjs` con y sin `--audio` + `tut.py verificar`, 0 errores) → re-ensayo de los diez
con `ensayar.py` bajo cerrojo (restaurar antes y después; E2a en 02b, E6c + `preparar.mjs --estatico` en 06c):
**0 fallos, 0 CORTADO** (capturas y logs en `…/_ensayo-t4/<guion>/`) → `grabar-serie.sh` DESACOPLADO con
`Start-Process` (corridas 20:59 los diez, 21:59 04c, 22:22 02b y 03) → veredicto → `huecos.mjs` (0 tramos > 10 s en
los diez) → `tut.py auditar --video` → 8–10 fotogramas propios por video (`…/<guion>/t4-*.png` y hoja
`t4-_hoja.png`). Cada video es posterior al arranque de su corrida. Al terminar: **E0** restaurado y cerrojo libre.

| Guion | Duración (con marca 3+3 s) | Veredicto | Tomas | Regrabaciones (motivo) | OCR |
|---|---|---|---|---|---|
| seguridad-00-introduccion | **3:32** (3:26) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-02b-editor-permisos | **4:16** (4:10) | PUBLICABLE | 2 | 1 · G-14: «Cada bloque» y «cada botón» marcaban la cabecera del rol / las filas de abajo | 0 |
| seguridad-03-herencia | **4:36** (4:30) | PUBLICABLE | 2 | 1 · G-14: «vienen heredados» salía como caja vacía sobre los filtros | 0 |
| seguridad-09-lo-que-se-movio | **3:20** (3:14) | PUBLICABLE | 1 | 0 | 3 lecturas justificadas: `130955036` = RNC 130555036 con el «5» tapado por el cursor |
| seguridad-04a-personas | **4:11** (4:05) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-04b-alta-y-edicion | **5:02** (4:56) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-04c-equipos | **3:58** (3:52) | PUBLICABLE | 2 | 1 · G-13: el diálogo «Editar Equipo» sin marca → «alerta sin explicar» | 1 lectura justificada: carlos.pimentel@germiva.demo mal leído |
| seguridad-05-acceso-efectivo | **2:59** (2:53) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-06a-credenciales | **4:41** (4:35) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-06c-caso-integracion | **3:14** (3:08) | PUBLICABLE | 1 | 0 | 5 lecturas justificadas: 1000000003 y B0200000001 (comprobantes ficticios) leídos como RNC |

**00: el archivo bueno es `salida/seguridad-00-introduccion/video-20260927-2104.mp4`.** El `video.mp4` (toma de T1,
17:24) lo tenía abierto el Reproductor de Windows Media durante toda la tanda y el motor escribió la toma nueva con
otro nombre. El veredicto y la auditoría OCR se corrieron sobre `video-20260927-2104.mp4`. Al cerrar el reproductor
hay que renombrarlo a `video.mp4` (`youtube-video.txt`, `video.srt` y la miniatura ya son los de esa toma).

Fotogramas que confirman lo pedido: 00 · el cartel «Consejo» sobre la lámina sale arriba a la derecha, libre de
«Alcance» y del subtítulo (`t4-04-99.5s.png`, `t4-05-102.0s.png`). 02b · «MÓDULOS 5 de 1103 permisos» en Vendedor y
«N de 1103» al editar Cobrador. 03 · Historial «Inventario · Productos / Ventas · Cotizaciones / Clientes y Proveedores ·
Socios», con la marca sobre el guion rojo «–» al decir «guion rojo» (G-3) y sobre «Ventas · Cotizaciones». 09 · los tres
eventos de Rol #79 con IP 192.168.1.25 (G-2). 04a/04b/04c/05 · al entrar a Personas, «Todas» sin número y esqueletos,
luego «Todas · 9»; Auditoría con esqueleto y «75 eventos». 06a · «Registrar Facturas» deja 3 casillas y se desmarca la
de Facturación; el panel queda en «PERMISOS 4». 06c · «1 llamada en total».

### Capítulos (`salida/<guion>/youtube-video.txt`)

- **00-introduccion**: 00:00 Bienvenida · 00:41 Los seis conceptos · 01:43 La consola · 02:38 Caso práctico: las cinco pestañas
- **02b-editor-permisos**: 00:00 Cómo se lee el editor · 01:12 Conceder permisos · 02:07 El alcance · 02:42 Buscar un permiso · 03:18 Guardar y revisar
- **03-herencia**: 00:00 Qué es la herencia · 00:59 Crear un rol hijo · 01:51 Excluir un permiso heredado · 02:34 Eliminar un rol · 03:11 Caso práctico: quién tiene el rol · 03:47 Caso práctico: qué le cambiaron
- **09-lo-que-se-movio**: 00:00 Tu contraseña, en Mi perfil · 00:59 Visibilidad del menú · 01:54 Perfil del Consultorio · 02:24 El enlace viejo del historial · 02:50 Caso práctico: los enlaces viejos
- **04a-personas**: 00:00 La lista de personas y sus vistas · 01:10 Buscar y filtrar por rol · 02:00 La ficha de una persona · 03:06 Ver su actividad · 03:31 Caso práctico: la cuenta que nunca se usó
- **04b-alta-y-edicion**: 00:00 Dar de alta a una persona · 01:46 Editar y cambiar la contraseña · 02:33 Asignar otro rol · 03:19 Desactivar y activar · 04:19 Eliminar y caso práctico
- **04c-equipos**: 00:00 Qué es un equipo · 00:55 Crear un equipo · 01:35 Agregar miembros · 02:17 Quitar, editar y eliminar · 03:09 Cuando no queda ningún equipo
- **05-acceso-efectivo**: 00:00 Cómo se calcula · 00:51 La herencia en la ficha · 01:31 Dos roles suman · 02:09 El equipo no suma · caso práctico
- **06a-credenciales**: 00:00 Qué es una credencial de API · 00:52 Crear una credencial · 02:00 Guardar el secreto · 02:41 El panel de la credencial · 03:23 Quitarle lo que no necesita
- **06c-caso-integracion**: 00:00 El programa del contador · 00:42 Consulta permitida · 01:15 Consulta no permitida · 01:47 Conceder el permiso · 02:41 La misma consulta, ahora permitida

### Cambios en los guiones (copia previa en el scratchpad, `bak-t4/`)

- **02b**: recortes de apartes (−≈70 palabras, sin quitar F-137/F-141/F-150): 4:33 → 4:16. G-14: «Cada bloque» marca
  `.rpe__resource-name` de Cotizaciones y «cada botón» el botón «Aprobar» (antes `.rpe__resource-head` y `.rpe__actions`).
- **03**: G-3 corregido en la voz («A la izquierda, el antes: aquí un guion rojo, porque no tenía nada; y tras la flecha,
  el después en verde»); con G-1 la voz nombra el módulo («como Inventario, Productos», «Cotizaciones, dentro de
  Ventas»); anclas «guion rojo» y «dentro de Ventas». Recortes en 02 y 05. G-14: «vienen heredados» marca el primer
  heredado (`.rpe__act--inherited`). Queda en 4:36: la frase de G-3 suma ≈9 s y lo demás es cobertura.
- **06a paso 05**: vuelve al buscador (G-5 corregido): «En Buscar permisos escribo registrar facturas» → 3 casillas
  (Facturación, Facturación Electrónica y Compras) → marca la de Facturación y la de Compras → la desmarca. 4:30 → 4:41.
- **04c paso 04 (G-13)**: marca `mat-dialog-container:has-text('Editar Equipo')` al decir «el mismo formulario».
- 00, 09, 04a, 04b, 05 y 06c: sin cambios de guion.

### Lecciones

- **Un bloque del editor de permisos más alto que el trozo visible de su panel no se puede marcar** (G-14): el motor
  lo centra en la ventana, el panel interior se desplaza y el recurso queda debajo de la leyenda fija. La caja sale
  sobre la cabecera del rol o vacía. `ensayar.py` lo da por «visible=entero». En el editor, marca el nombre del
  recurso o un botón, nunca `.rpe__resource-head` ni `.rpe__actions` de un recurso con más de una fila de acciones.
- **Todo diálogo de trabajo lleva su marca**, aunque en una toma anterior el veredicto lo descartara (G-13; ya estaba en
  las lecciones de T1).
- **Antes de grabar, comprueba que ningún `video.mp4` de la tanda está abierto** en un reproductor: el motor escribe
  con otro nombre y `grabar-serie.sh` da «GRABACIÓN FALLÓ (video.mp4 viejo)» aunque la toma sea buena.

## Tanda 3 · 07 y casos 08a–08h con el build 4 (OPERADOR-GRABACIÓN, 2026-09-27/28)

Build 4 (API `dist` :3001 PID 10444, estático :4200 PID 7752), sin reiniciar. Procedimiento: puerta 1 (`revisar.mjs` +
`tut.py verificar`, 0 errores) → re-ensayo de los nueve con `ensayar.py` bajo cerrojo (restaurar E0 antes y después):
**0 fallos, 0 CORTADO** (capturas y logs en `germiva/qa-seguridad-grabacion-2026-09-27/_ensayo-t3/<guion>/`) →
`grabar-serie.sh` DESACOPLADO con `Start-Process` (Git Bash; ojo: `bash` a secas en PowerShell es el de WSL y no arranca)
→ veredicto → `huecos.mjs` (0 tramos > 10 s en los nueve) → `tut.py auditar --video` (0 posibles datos reales) → 8–10
fotogramas propios por video (`…/<guion>/t3-NN-*.png` y hojas `t3-hoja-N.png`). Corridas: 22:58 (los nueve), 23:54 (08a,
08d, 08e), 00:13 (08a) y 00:21 (08a). Cada `video.mp4` es posterior al arranque de su corrida; ninguno quedó bloqueado
por un reproductor. Al terminar: **E0** restaurado y verificado, cerrojo libre.

| Guion | Duración (con marca 3+3 s) | Veredicto | Tomas | Regrabaciones (motivo) | OCR |
|---|---|---|---|---|---|
| seguridad-07-auditoria | **4:13** (4:07) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-08a-vista | **4:24** (4:18) | PUBLICABLE | 4 | 3 · toma 1: FALLO falso por R20 (dos marcas `aside.sidebar`, G-15); toma 2: el login de Marta pasó de 15 s y el paso 04 abortó (G-16); toma 3 PUBLICABLE pero la voz decía «Ya estamos en el Inicio de Pedro» 6 s antes de que entrara (G-17) | 0 |
| seguridad-08b-crear-editar-anular | **3:18** (3:12) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-08c-exportar-eliminar | **3:57** (3:51) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-08d-alcance | **4:41** (4:35) | PUBLICABLE | 2 | 1 · logins de 14–16 s: tres clics +1,0 a +1,4 s tarde y 11 s quietos en 05 (G-16) | 0 |
| seguridad-08e-aprobar-y-estado | **3:57** (3:51) | PUBLICABLE | 2 | 1 · login de Carlos lento: dos clics +1,2 s tarde en 04 (G-16) | 0 |
| seguridad-08f-herencia | **3:12** (3:06) | PUBLICABLE | 1 | 0 | 0 |
| seguridad-08g-cambio-en-vivo | **4:12** (4:06) | PUBLICABLE | 1 | 0 (puentes de login añadidos antes de su turno) | 0 |
| seguridad-08h-administrar-la-seguridad | **4:40** (4:34) | PUBLICABLE | 1 | 0 (puente de login añadido antes de su turno) | 0 |

07, 08a, 08d, 08g y 08h pasan de 4:10 porque la voz cubre logins de 13–20 s en cámara (en el ensayo eran 5–11 s). Si en
producción el login tarda lo del ensayo, los puentes «Mientras entra…» se pueden quitar.

Fotogramas que confirman lo pedido: 07 · pestañas estables (el clic en «Auditoría» entra a la primera), esqueleto →
«671 eventos», IP 192.168.1.25, detalle «Qué cambió · Inventario · Productos» con el antes tachado, cartel abajo a la
izquierda sin tapar el detalle. 08a · Ana «1 – 3 de 3»; Pedro sin Ventas y toast «No tienes permiso para ver
«Cotizaciones»…»; Marta con 4 pestañas, sin «Nuevo», franja «Solo lectura: no tienes permiso para cambiar permisos…»
(E-10) y botones apagados; `.console-denied` en Integraciones. 08b · Ana con «Crear Cotización», Duplicar y «Cancelada» en
azul; Marta «1 – 8 de 8» sin botón ni ⋮, «Cotización 2» sin «Editar», «Cancelada» en gris y solo «Volver». 08c · Pedro con
«Importar / Exportar» y diálogo Exportar; Ana sin el botón y solo el lápiz; Rosa con papelera; Pedro sin papelera (E-12:
el FAB de 48 px no tapa nada). 08d · láminas «3 de 8» y «5 de 8»; Carlos «1 – 8 de 8», Ana «1 – 3 de 3», «Acceso Denegado ·
Su rol solo le permite…», alcance Equipo guardado, Ana «1 – 5 de 5» con COT 5 y 4. 08e · confirmación y «Éxito · Estado
actualizado correctamente», COT 1 Aprobada; Ana con «Aprobada» en gris; COT 6 con «Convertir a factura»; COT 7 solo
«Versiones e historial / Duplicar». 08f · Socios · Crear concedido en el padre, heredado en el hijo, tachado al excluir;
Carlos «2/37» → «1/37». 08g · Ana «1 – 10 de 25»; Productos · Ver 1/42 → 0/42; Ana sin Inventario (4 iconos) y toast por
dirección; Auditoría de Marta «Rol #77 · Inventario · Productos: ~~Ver~~ → —». 08h · Rosa: Editar, Cambiar contraseña, ⋮
con Eliminar, «Editar equipo» y papelera, credencial con «Rotar secreto» y ⋮; Auditor «Usuarios de Integración 0/4»;
Marta: sin «Nuevo», ⋮ solo «Ver su actividad», barra «1 seleccionada · Limpiar», «Ver permisos» sin «Rotar secreto».

07 cruzó la medianoche de la app (hora RD): el paso 01 agrupa bajo «Hoy · domingo, 27» y los pasos 03–04 bajo «Ayer ·
domingo, 27». Es correcto (la voz no nombra el día); no es un defecto.

### Capítulos (`salida/<guion>/youtube-video.txt`)

- **07-auditoria**: 00:00 La bitácora · 01:05 Los filtros · 02:04 El detalle de un evento · 03:18 El historial de un registro
- **08a-vista**: 00:00 Con permiso: Ana ve Cotizaciones · 00:49 Sin permiso: el menú de Pedro · 01:52 Sin permiso: escribir la dirección · 02:25 Con permiso: Marta ve Seguridad · 03:46 Sin permiso: la pestaña Integraciones
- **08b-crear-editar-anular**: 00:00 Con permiso: crear · 00:52 Con permiso: editar y anular · 01:39 Sin permiso: crear · 02:37 Sin permiso: editar y anular
- **08c-exportar-eliminar**: 00:00 Con permiso: exportar · 00:50 Sin permiso: exportar · 01:45 Con permiso: eliminar · 02:22 Con permiso: la papelera · 02:47 Sin permiso: eliminar · 03:24 Sin permiso: sin papelera
- **08d-alcance**: 00:00 Qué es el alcance · 00:45 Todos: Carlos ve las 8 · 01:17 Propios: Ana ve 3 · 02:09 Propios: una cotización ajena · 02:37 Equipo: Rosa cambia el alcance · 03:13 Equipo: cambiar el alcance · 03:47 Equipo: Ana ve 5
- **08e-aprobar-y-estado**: 00:00 Permiso y estado · 00:38 Con permiso: aprobar · 01:18 Sin permiso: aprobar · 02:19 Estado Aprobada: se puede convertir · 03:15 Estado Borrador: no se puede convertir
- **08f-herencia**: 00:00 Qué es la herencia · 00:45 Conceder en el rol padre · 01:30 Con permiso: le llega por herencia · 02:09 Excluir en el rol hijo · 02:39 Sin permiso: excluido
- **08g-cambio-en-vivo**: 00:00 Antes: Ana ve Productos · 00:32 Rosa quita el permiso · 01:41 Después: el menú de Ana · 02:32 Después: por la dirección · 02:52 El rastro en la Auditoría
- **08h-administrar-la-seguridad**: 00:00 Con permiso: Rosa administra personas · 00:45 Con permiso: Rosa administra equipos · 01:18 Con permiso: Rosa administra credenciales · 01:54 Rosa le da a la auditora solo «Ver» en Integraciones · 02:39 Sin permiso: Marta en la ficha de una persona · 03:41 Sin permiso: Marta en los equipos · 04:07 Sin permiso: Marta en las credenciales

### Cambios en los guiones (copia previa en el scratchpad, `bak-t3/`)

- **07 paso 03 (G-1)**: «lo de antes: en Productos» → «en Inventario, Productos».
- **08g paso 05 (G-1)**: «en Productos: antes» → «en Inventario, Productos: antes» (ancla «Productos: antes»). Paso 03: la
  segunda marca del menú pasa a `aside.sidebar >> nth=0` (G-15).
- **08a paso 04 (E-10)**: la voz nombra la franja «Solo lectura», con una marca `.rpe__readonly` al decir «franja
  amarilla», y dice que los botones se ven más apagados. Paso 02: segunda marca del menú `aside.sidebar >> nth=0` (G-15).
- **08f (G-14)**: «el recurso Socios» marca `.rpe__resource-name` (antes el bloque entero) y «queda tachado» marca la
  acción Crear (`… .rpe__act:has-text('Crear')`) en lugar del recurso.
- **Puentes de login (G-16/G-17)** en 08a-02/04, 08d-03/05/07, 08e-03/04, 08g-02/03/05 y 08h-05: una frase «Mientras entra,
  …» de 4–6 s tras la oración de «Entrando», y una marca SIN cursor sobre `button.auth-primary-btn:has-text('Entrando'),
  aside.sidebar` anclada a ella (señala el botón si aún está entrando, o el menú si ya entró; con la coma nunca falta).
  08a-02 lleva dos puentes (el login de Pedro llegó a 19 s). 08d-05 añade al final «En cuanto entra, su menú trae todos
  los módulos, con Seguridad incluida.», con el puente anclado a «el cambio le llegará».

### Lecciones

- **El login en cámara ya no es de 5–11 s: medimos 13–20 s** (N-4 más la CPU de la grabación). Entre el clic en «Iniciar
  sesión» y la primera acción posterior hace falta ≥ 17 s de voz, más una marca puente a los ~5 s de «Entrando». Sin ella,
  la marca sin ancla del menú espera como mucho 15 s y, si el login pasa de eso, el paso aborta con 50 s de imagen quieta.
- **El veredicto no mira lo que la voz AFIRMA.** Un «Ya estamos en el Inicio» dicho sobre la pantalla de acceso salió
  PUBLICABLE. Comprobación nueva (scratchpad `yadentro.js`): el instante de la marca del menú frente al «Ya…» de la voz en
  cada paso con login. Un adelanto de más de ~1 s es un defecto de guion.
- **R20 también con marcas sin ancla**: si una marca sin `al_decir` y otra con ancla comparten selector en el mismo paso,
  `veredicto.mjs` empareja la anclada con el evento de la primera (−13,6 s). Hay que usar un selector distinto (`>> nth=0`).
- **En PowerShell, `bash` es el de WSL**: `Start-Process` debe llamar a `C:\Program Files\Git\bin\bash.exe`.

## Final · tanda 1 · 00, 01, 02a, 02b, 03, 09 con el build 5 (OPERADOR-GRABACIÓN-FINAL, 2026-09-28)

Build 5 (API `dist` :3001 PID 20760, estático :4200 PID 8352), sin reiniciar. Procedimiento por guion: `revisar.mjs` con y sin
`--audio` (audio regenerado con `tut.py narrar` antes, para que `--audio` mida la voz nueva) + `tut.py verificar` 0 errores →
re-ensayo con `ensayar.py` bajo cerrojo (restaurar antes y después; E2a en 02b): **0 fallos, 0 CORTADO** en los seis
(`germiva/qa-seguridad-final-2026-09-28/_ensayo/<guion>/`) → `grabar-serie.sh` DESACOPLADO (`Start-Process`, Git Bash) →
veredicto → `huecos.mjs` → `tut.py auditar --video` → **revisión visual propia** de cada toma: fotograma a mitad de cada marca,
+0,3 s de cada clic y +1,5 s tras cada navegación (script `fotogramas.mjs` en el scratchpad; `_indice.txt` + hojas 2×2
`_hoja-NN.jpg` en `germiva/qa-seguridad-final-2026-09-28/<guion>/`, tomas previas en `toma1/`, `toma2/`). Corridas: 10:54 (los
seis), 11:55 (los seis), 12:54 (00, 01, 02a, 02b, 03), 13:28 (02b). Cada `video.mp4` es posterior al arranque de su corrida.
Al terminar: **E0** restaurado y verificado, cerrojo libre.

| Guion | Duración | Veredicto | Tomas | Fotogramas revisados (toma final) | Revisión visual | OCR |
|---|---|---|---|---|---|---|
| seguridad-00-introduccion | **3:37** | PUBLICABLE | 3 | 48 | OK | 0 |
| seguridad-01-resumen | **3:46** | PUBLICABLE | 3 | 44 | **BLOQUEADO ERP H-GF-1** (lista «Requiere atención» se desplaza, 1:28–1:38) | 0 |
| seguridad-02a-roles | **3:41** | PUBLICABLE | 3 | 56 | OK | 0 |
| seguridad-02b-editor-permisos | **4:25** | PUBLICABLE | 4 | 61 | **BLOQUEADO ERP H-GF-2** (panel de recursos de ~60 px con la barra; filas cortadas 2:14–2:26, 3:05, 4:18) | 0 |
| seguridad-03-herencia | **4:42** | PUBLICABLE | 3 | 82 | OK (H-GF-2 sorteado en guion) | 0 |
| seguridad-09-lo-que-se-movio | **3:22** | PUBLICABLE | 2 | 48 | OK | 0 |

Todas con `huecos.mjs` 0 tramos > 10 s. Tomas que no valieron: 02b toma 1 y 3 REGRABAR (+0,92 s clic en la pestaña; +1,03 s
marca de Facturas); el resto de regrabaciones fueron por la revisión visual (el veredicto las daba PUBLICABLE).

### Capítulos (`salida/<guion>/youtube-video.txt`)

- **00-introduccion**: 00:00 Bienvenida · 00:41 Los seis conceptos · 01:43 La consola · 02:39 Caso práctico: las cinco pestañas
- **01-resumen**: 00:00 Las cinco cifras · 01:04 Requiere atención · 01:58 Actividad reciente · 03:02 Caso práctico: la revisión semanal
- **02a-roles**: 00:00 La lista de roles · 01:13 Un rol del sistema · 02:02 Duplicar un rol · 02:45 Crear un rol nuevo
- **02b-editor-permisos**: 00:00 Cómo se lee el editor · 01:17 Conceder permisos · 02:14 El alcance · 02:49 Buscar un permiso · 03:25 Guardar y revisar
- **03-herencia**: 00:00 Qué es la herencia · 00:59 Crear un rol hijo · 01:54 Excluir un permiso heredado · 02:39 Eliminar un rol · 03:16 Caso práctico: quién tiene el rol · 03:53 Caso práctico: qué le cambiaron
- **09-lo-que-se-movio**: 00:00 Tu contraseña, en Mi perfil · 00:59 Visibilidad del menú · 01:54 Perfil del Consultorio · 02:24 El enlace viejo del historial · 02:53 Caso práctico: los enlaces viejos

### Puntos «a confirmar» de la corrección 09-28 (confirmados en ensayo y fotograma)

00: el clic en Vendedor abre su editor («5 de 1103», Clientes y Proveedores) y el subrayado cae bajo «Seguridad» y bajo «Vendedor».
01: la cabecera ACCIÓN casa (`.sec-ov__row.gm-sheet-row--head .gm-th:text-is('Acción')`); la ficha de Héctor llega cargada tras
esqueleto (sin «no está en la lista»). 02a: el ⋮ casa con `[aria-label='Más acciones']`; títulos «Crear rol» y «Duplicar rol».
02b: la barra se marca entera sin CORTADO; texto «N cambios sin guardar · nadie tiene este rol todavía»; tras borrar la búsqueda
se ve Clientes y Proveedores. 03: la ficha de Ana llega sin aviso. 09: el filtro fijado dice «Rol · Almacén» (`.sec-audit__pinned`).

### Cambios en los guiones (copia previa en el scratchpad, `bak-final-t1/`)

- **Todos**: `cursor:false` en casi todas las marcas de lectura (el cursor y su tooltip tapaban justo lo que la voz nombraba:
  «Vacío», «Del sistema», «Acceso total», «No se encontraron registros», Ver/Crear/Editar…) y `durante_ms` recortados: **una
  marca vive ≈ durante_ms + 1 s y SOBREVIVE al cambio de pestaña o al cierre de un diálogo**, así que quedaba como caja vacía
  sobre la vista siguiente.
- **00**: «Ahora sí, entro por el candado» (ancla tardía con `--audio`); en Personas la voz dice «La busco por su nombre, y aquí la
  tengo, arriba de todo» y escribe «Ana» en el buscador (antes la tabla se desplazaba por dentro y se iba la cabecera); «la frase»
  subraya el subtítulo.
- **01**: «y lo más viejo, como aquí, con el día y la hora» (la celda dice «Ayer 11:10», no «hace unas horas»); el clic en la fila
  «Cambió permisos» va a su celda CUÁNDO y «el antes y el después» marca la línea de cambio; cartel Cuidado 4,2 s.
- **02b**: «Entro por el candado de la izquierda; arriba, abro Roles y permisos» (+0,92 s); la marca de Facturas pasa al nombre del
  recurso y una marca previa sobre el grupo «Facturación» de los resultados hace el desplazamiento antes (+1,03 s).
- **03**: «Pulso Nuevo, arriba a la derecha; en el menú elijo Rol» (ancla gastada); «Excluido de la herencia» se explica DESPUÉS de
  guardar (H-GF-2); «El filtro Heredados deja solo los recursos que traen algo del padre»; opción del sistema marcada en «Empleado»;
  antes/después del historial subrayados.
- **09**: `al_decir_navegar` en 03 y 04 (la pantalla nueva salía 5–6 s antes de que la voz la anunciara); «a Mi perfil» marca la miga;
  el saludo del Inicio subrayado en lugar de la empresa de la barra (el cursor tapaba el RNC: era el falso positivo del OCR).

### Lecciones

- **El veredicto no ve cabeceras perdidas por desplazamiento interno ni cajas huérfanas**: las seis tomas 1 fueron PUBLICABLE y
  las seis tenían defectos visibles. La revisión por fotograma (marca, +0,3 s de clic, +1,5 s de navegación) es imprescindible.
- **Una marca no se apaga al cambiar de vista**: si la acción siguiente cambia de pestaña o cierra un diálogo antes de `durante_ms`
  + ~1,2 s, la caja queda vacía sobre la pantalla nueva. Comprobador: `arrastre.mjs` (scratchpad).
- **Un `navegar` de paso se ejecuta al empezar la voz**: si la frase que lo anuncia no es la primera, usa `al_decir_navegar`.
- **`revisar.mjs --audio` sólo sirve con el audio nuevo**: corre `tut.py narrar <guion>` antes (no graba, sólo sintetiza).
