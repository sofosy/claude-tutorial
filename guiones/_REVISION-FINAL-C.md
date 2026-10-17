# Revisión final C · serie «Seguridad» · 05, 06a, 06b, 06c, 07, 08a, 08b (2026-09-28)

REVISOR-FINAL, solo lectura. Fotogramas en `qa-seguridad-revision-final-2026-09-28/<guion>/`, contrastados con
`salida/<guion>/video.srt` y el guion. Se descartaron los falsos positivos conocidos (SKILL › «Falsos positivos del
informe»). Todo lo que sigue sale de un fotograma concreto.

**Contexto del motor:** los siete `video.mp4` son de antes de `e1810d6` (27/09 19:37 a 28/09 00:27; el commit es del
28/09 00:44). Por eso, donde una lista o un panel con scroll propio se desplazó y dejó una cabecera o una fila cortada,
el tipo es **motor** y hay que regrabar ese paso con el motor ya corregido.

| Video | Veredicto | Qué hay que hacer |
|---|---|---|
| 05 acceso efectivo | **CORREGIR** | regrabar 02 y 04 (motor) y cambiar una marca de 04 |
| 06a credenciales | **CORREGIR** | regrabar 04 (motor) |
| 06b rotar/pausar/revocar | **CORREGIR** | cambiar la voz y una marca en 02/03 y regrabar |
| 06c caso integración | **OK** | nada bloquea; hay 2 mejoras opcionales |
| 07 auditoría | **CORREGIR** | regrabar sin cruzar la medianoche y corregir voz/pantalla en 04 |
| 08a vista | **CORREGIR** | cambiar una marca de 01 (y hay un texto del ERP que conviene arreglar) |
| 08b crear/editar/anular | **OK** | detalles menores |

Datos: en los siete solo aparecen datos ficticios de la demo (Distribuidora Las Palmas, RNC 130555036, @germiva.demo,
las personas del canon, IP 192.168.1.25). No se ve ningún secreto completo: en la franja se enseñan 12 caracteres +
`•••` + 4, y en la página del contador todo son puntos. Las insignias de contraste son correctas en 06c, 08a y 08b.

---

## 05 · seguridad-05-acceso-efectivo — CORREGIR

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| 05-1 | 0:56–1:31 | 02-herencia-en-la-persona | `013-00m56.62s`, `014`…`021` | motor | Al pulsar a Carlos (fila 9), la lista de Personas se desplaza por dentro y **la cabecera de la tabla (PERSONA · ROLES · ÚLTIMO INGRESO · ESTADO) queda cortada por la mitad** (y≈455) durante todo el paso. Es el patrón que corrigió `e1810d6`. | Regrabar el paso 02 con `e1810d6`. |
| 05-2 | 2:20 | 04-equipo-no-suma | `039-02m20.03s` | motor | Al marcar la cabecera del bloque de Ana, el panel de la ficha se desplaza y la etiqueta **«ROLES» queda cortada** bajo la cabecera del panel (y≈615). | Regrabar el paso 04 con `e1810d6`. |
| 05-3 | 2:23–2:32 | 04-equipo-no-suma | `041-02m27.08s` | guion | Mientras la voz dice «Un cambio en un rol vale desde la siguiente operación… y solo cuenta lo que la empresa tiene contratado», la marca cae 5 s sobre **«Cotizaciones 3/19»** de Ana. La voz no nombra esa fila, así que la marca no explica nada. | Marcar el subtítulo «La unión de sus roles, por módulo contratado.» (`.sec-people__block-head + *` o equivalente), o quitar esta marca. |
| 05-4 | 0:56–2:12 | 02/03 | `013`, `025` | ERP (baja) | En la lista, «Sin ningún r…», «Vendedor s…» y «Vendedor, A…» salen truncados. La voz no los lee. | Nota para el ERP; no bloquea. |

Lo demás está bien: la lámina tiene el contenido correcto y no la tapa ninguna insignia en sus fases, y todas las marcas
del panel caen donde toca (Hereda de Vendedor, 11/1160, 7/19, 2/79, 1/37, José 5/42 e Inventario 1/47, Luisa y
«+ Asignar rol»). El cartel «Consejo» tapa la lista, no la ficha.

## 06a · seguridad-06a-credenciales — CORREGIR

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| 06a-1 | 3:15–3:22 | 04-panel | `059-03m17.06s` | motor | Al marcar «Operaciones en 7 días», el panel de la credencial se desplaza por dentro y **la fila «Compras 1/38» queda cortada** bajo la cabecera fija del panel (se ven medio título y la cifra). | Regrabar el paso 04 con `e1810d6`. |
| 06a-2 | 1:34–1:40 | 02-crear-credencial | `032-01m37.77s` | guion (baja) | La marca de «Endpoint permitido» es **más alta que el campo**: incluye el hueco de la ayuda que hay debajo (y 660–760 con el campo en 668–720). | Marcar el `input` o `.mat-mdc-text-field-wrapper` del campo, no el `mat-form-field`. |
| 06a-3 | 3:17 | 04-panel | `059` | ERP (baja) | Al posarse el cursor sobre la gráfica sale el tooltip «0 operaciones», que tapa las etiquetas «mié/jue». | Marca sin cursor (`"cursor": false`). |
| 06a-4 | 2:02–2:40 | 03-guardar-el-secreto | `037`, `041`, `042` | — | Comprobado: el secreto va tapado (`0427c0db1ad3•••…•••1cd8`) y la API Key se enseña truncada. Son datos de prueba. | Nada que hacer. |

Nota ERP (no bloquea): la etiqueta «Endpoint permitido» está en inglés; la voz la explica («las rutas del sistema»).

## 06b · seguridad-06b-rotar-pausar-revocar — CORREGIR

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| 06b-1 | 2:16–2:26 (con 1:23–1:50) | 03-revocar | `052-02m19.98s`, `029`, `030`, `036` | guion (+ERP) | La voz dice que el número de la pestaña Integraciones «dice **cuántas credenciales tiene la empresa**». Pero entre 1:23 y 1:50, con Programa del contador desactivada, la pestaña marcaba **«1» teniendo dos credenciales en la lista**. El contador cuenta las activas. Un novato ve que el número baja al desactivar y no entiende por qué. | Voz: «su número dice cuántas credenciales **activas** hay». Opcional: que en 02 la voz señale que el número baja a 1 al desactivar. ERP: aclararlo en la etiqueta o en un tooltip. |
| 06b-2 | 1:16–1:21 | 02-desactivar-activar | `027-01m19.50s` | guion | «Fíjate arriba, junto al nombre: ahí va a cambiar el estado»: la marca `.sec-api__card-top` rodea el nombre y el prefijo, pero **deja fuera «Activa»**, que es lo que cambia (y≈486). | Marcar `.sec-api__facts`, como en 1:25. |
| 06b-3 | 2:46–2:55 | 04-documentacion | `063-02m52.34s`, `066` | motor (baja) | Al marcar el índice lateral, la página se desplaza y **las migas «Seguridad / Integraciones / Documentación de la API» quedan cortadas** bajo la barra superior (y≈88). | Se resuelve al regrabar con `e1810d6` (el paso ya hay que regrabarlo por 06b-1 y 06b-2). |
| 06b-4 | 2:30–2:38 | 03-revocar | `058-02m37.37s` | guion (baja) | «Ahora hay tres asuntos pendientes»: en pantalla solo se ven dos. El tercero queda bajo el pliegue de «Requiere atención». | «…ahora son tres asuntos» y marcar solo la cifra, o desplazar la lista para que se vea el tercero. |
| 06b-5 | 2:37 | 03-revocar | `058` | ERP (baja) | La tarjeta del Resumen dice «Credenciales de API 1 · **Todas en uso**», pero la única que queda tiene «Último uso: **Nunca**». | ERP: «Sin uso todavía» cuando la credencial nunca se usó. |
| 06b-6 | 0:25–0:35 · 2:05–2:12 | 01 · 03 | `009`, `048` | ERP (baja) | Los diálogos «Rotar secreto» y «Revocar credencial» usan comillas rectas ("Programa del contador") y el segundo trata de **usted** («¿Está seguro de que desea…»), mientras la consola trata de tú. Además el título dice «Revocar credencial», el texto dice «eliminar la integración» y el botón dice «Eliminar». | ERP: comillas «», tuteo y un solo verbo. La voz ya lo cubre («Confirmo con Eliminar»). |

Lo demás está bien: el cartel «Cuidado» sale mientras rota, el toast «Secreto copiado» se ve y se explica, el estado
«Inactiva» se ve en el panel y en la fila, «412 llamadas en total» concuerda en número, y la documentación sale dentro
del shell (E-7).

## 06c · seguridad-06c-caso-integracion — OK

La página de demostración se presenta como «Página de prueba». La clave sale truncada (`gv_live_4bc32ae5••••`) y el
secreto todo con puntos: **no se puede leer ningún secreto**. Las insignias van bien («Con permiso · Facturas · Ver»,
«Sin permiso · Productos · Ver», «Con permiso · Productos · Ver»), y el contraste 403 → conceder → 200 con 25
productos se ve completo. «1 llamada en total» concuerda (G-7).

Mejoras opcionales (no bloquean):

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| 06c-1 | 1:22–1:47 | 03-consulta-no-permitida | `020-01m28.70s`, `021` | guion (lámina) | La lámina enseña «Código técnico del permiso: **PRODUCT_VIEW**». La voz no lo lee, pero un novato lo ve. | Quitar esa línea de `demo-integracion/index.html` o dejarla solo para el técnico, y regrabar 03 cuando toque. |
| 06c-2 | serie | 06a → 06b/06c | `06a/037` vs `06b/003`, `06c/006` | guion (canon) | En 06a se crea la credencial con prefijo `gv_live_3f3d43b7`, y 06b/06c arrancan con `gv_live_4bc32ae5` (canon E6c). La voz de 06c dice «la credencial que creamos». | Aceptable. Si se regraba 06a, fijar E6c con la misma clave o no mencionar el prefijo. |

## 07 · seguridad-07-auditoria — CORREGIR

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| 07-1 | 0:20 → 1:25 | 01 → 02 | `007-00m20.47s` vs `022-01m25.08s`, `037`, `057` | guion / toma (R13) | **La toma cruzó la medianoche.** A los 0:20 el encabezado del día dice «**Hoy** · domingo, 27 de septiembre»; desde 1:25 el mismo grupo dice «**Ayer** · domingo, 27 de septiembre». En el grupo aparece además el acceso de la toma a las 23:59. Un espectador atento ve el salto. | Regrabar fuera de la franja 23:30–00:30, o bien recolocar los eventos del canon con `hoy.mjs`. |
| 07-2 | 3:48–4:04 | 04-historial-y-persona | `063-03m55.01s`, `064` | guion | La voz describe elementos de **Auditoría** («al pie aparece **Cargar eventos anteriores**…», «verás el aviso **El evento no está entre los resultados**»), pero la pantalla sigue en **Personas** (Rosa filtrada) y la marca cae sobre la pestaña «Auditoría». Ninguno de los dos elementos se ve. | Volver antes a Auditoría (con «Todo el historial») y marcar el botón «Cargar eventos anteriores» del pie, o bien reducir la frase a un consejo sin afirmar lo que se ve. |
| 07-3 | 3:21 | 04-historial-y-persona | `052-03m21.31s` | motor | En el panel de detalle, al marcar los atajos, la zona «Qué cambió» se desplaza y **una línea queda cortada** bajo la cabecera fija del panel (y≈423). | Regrabar con `e1810d6`. |
| 07-4 | 0:44–0:52 | 01-la-bitacora | `013-00m46.47s` | guion (baja) | La voz recorre los colores empezando por «verde… azul… rojo… ámbar… y gris», y la marca se queda 7 s sobre la insignia **gris** «Acceso». En pantalla no hay ninguna fila roja ni ámbar. | Marcar la columna «Acción» (`.gm-th:has-text('Acción')`) o anclar la marca a «gris». |
| 07-5 | 3:08 | 03-detalle-del-evento | `050-03m08.57s` | ERP (baja) | «Evento **PERMISSIONS_CHANGED**» es un código en inglés. La voz lo llama «el código del evento». | ERP: enseñar la etiqueta («Cambió permisos») y dejar el código en un tooltip. |
| 07-6 | 1:38–1:46 · 3:29 | 02 · 04 | `029`, `057` | ERP (media) | El filtro «Registro» exige el nombre interno en inglés («quotes», «roles»). La voz lo avisa y funciona, pero obliga a saberlo. | ERP: aceptar el nombre en español o ofrecer un selector. |

Lo demás está bien: los filtros recargan la lista (D-S5): 75 → 3 → 0 eventos, y «Limpiar» deja 671. El detalle se lee
correctamente: «Inventario · Productos», antes tachado y después resaltado, «Chrome · Windows» e IP 192.168.1.25.
El Historial del registro enseña 3 eventos del rol 79.

## 08a · seguridad-08a-vista — CORREGIR

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| 08a-1 | 0:39–0:51 | 01-con-ventas | `013-00m45.78s` | guion | «Ana llega hasta aquí porque su rol, Vendedor, tiene el permiso Cotizaciones, Ver»: la marca cae 6 s sobre la cabecera de columna **«CLIENTE»**, que no tiene nada que ver con lo que se explica. | Marcar las migas «Ventas / Cotizaciones» o el título «Gestión de Cotizaciones y Presupuestos» (la pantalla que el permiso deja ver). |
| 08a-2 | 2:01 vs 3:59 | 03 vs 05 | `036-02m01.70s`, `069-03m59.67s` | ERP (media) | Dentro del mismo video el aviso de URL directa trata de **tú** («No tienes permiso… Solicita el acceso al administrador de tu empresa») y la franja de la consola de **usted** («No tiene permiso para ver «Integraciones». Solicite el acceso al administrador de la empresa»). La voz lee los dos tal cual. | ERP: pasar `.console-denied` a tuteo. La voz de 05 se adapta sola si se regraba. |
| 08a-3 | 0:30–0:50 | 01-con-ventas | `012`, `013` | ERP (baja) | En la lista de Cotizaciones, el título «Cotizaciones» va pegado a las migas en la misma línea («Cotizaciones 🏠 / Ventas / Cotizaciones»). Es el patrón E-8, que aquí no se corrigió. | ERP; no bloquea. |

Lo demás está bien: las insignias de contraste son correctas («Con permiso · Ana (Vendedor)», «Sin permiso · Pedro
(Almacén)», «Con permiso · Marta (Auditor)», «Sin permiso · Marta · Integraciones»). En el menú de Pedro no aparece
Ventas y el toast de URL directa se ve y se explica. Marta tiene cuatro pestañas y no tiene «Nuevo», y se ven la
franja «Solo lectura» y el tooltip «Concedido · Socios · Ver», sin código (E-2 y E-10 correctos). No queda tiempo
muerto de login con desfase (G-16/G-17 resueltos).

## 08b · seguridad-08b-crear-editar-anular — OK

El contraste se ve entero. Ana tiene «Crear Cotización», «Duplicar», «Editar Cotización 2», «Cancelada» en azul y
«Guardar», y el diálogo «Éxito — Cotización actualizada exitosamente» se explica. Marta tiene 8 cotizaciones, sin
botón Crear ni tres puntos, «Cotización 2» sin «Editar», «Cancelada» en gris y solo «Volver». Las insignias van bien.
El total recalculado es coherente: COT 2 pasa a RD$2,385.00 en la lista de Marta.

Detalles menores (no bloquean):

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| 08b-1 | 2:21–2:34 | 03-sin-crear | `046`, `047` | motor (baja) | La página se desplaza para centrar la tabla: las etiquetas de los filtros quedan contra la barra superior y la insignia «Sin permiso · Marta · Crear» tapa la etiqueta «Estado». No afecta a lo que se explica. | Se corrige solo si algún día se regraba con `e1810d6`. |
| 08b-2 | 2:43–2:50 | 04-sin-editar-anular | `052-02m46.18s` | motor (baja) | Las migas del detalle quedan cortadas arriba y la marca de `.page-hero-title` se extiende hasta x≈970, más ancha que «Cotización 2». | Marcar `h1` / el texto del título. |

---

## Transversal (ERP, no bloquea ningún video)

- **Totales distintos según la pantalla**: en la ficha de una persona «11 / **1160**» (05), en el editor de roles
  «5 de **1103** permisos» (08a) y en los permisos de una credencial «5 de **1336**» (06a/06c). Un novato que compara
  los números no sabe cuál es «el total del sistema». Conviene unificar el denominador o no enseñarlo.
- Mezcla de trato **tú / usted** en los mensajes de acceso (08a-2, 06b-6).

## Orden sugerido de regrabación

1. 07 (entero, fuera de la medianoche; 07-2 y 07-4 corregidos antes).
2. 05 pasos 02 y 04, con 05-3 corregido.
3. 06b pasos 02, 03 y 04 (06b-1, 06b-2 y 06b-4), restaurando E6c antes.
4. 06a paso 04.
5. 08a paso 01 (08a-1).

Todo con el motor en `e1810d6` o posterior. Primero la puerta 1 y el ensayo, después `restaurar`.
