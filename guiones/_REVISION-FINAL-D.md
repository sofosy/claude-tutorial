# Revisión final D · serie «Seguridad» · 08c–08h y 09 (2026-09-28)

REVISOR-FINAL, solo lectura: no grabé, no abrí el navegador ni el ERP y no edité guiones. Leí los fotogramas de
`qa-seguridad-revision-final-2026-09-28/<guion>/` (unos 170 de 533, con prioridad en cada marca de contraste, cada
insignia, cada cartel y cada diálogo) y los comparé con `video.srt`, con `_indice.tsv` y con los `veredicto.log` /
`auditoria-video.txt`. Extraje con ffmpeg unos fotogramas más como evidencia, y dejé cada uno en la carpeta de su
video con el prefijo `rev-*.jpg`.

Qué significa cada tipo: **guion** = se arregla en el JSON; **motor** = lo produce `grabar.py` o la capa `#__tut_ui`
(desplazamiento, marca, SRT); **ERP** = texto o comportamiento de la aplicación.

## Resumen

| Video | Veredicto | Por qué |
|---|---|---|
| 08c-exportar-eliminar | **OK** (con observaciones) | Todos los contrastes se ven: el botón Importar/Exportar está con Pedro y falta con Ana; la papelera está con Rosa y falta con Pedro. Los defectos son menores. |
| 08d-alcance | **CORREGIR** | En 3:29–3:47 queda oculta la cabecera del recurso «Cotizaciones» (Ver/Crear/Editar): es el patrón de desplazamiento del motor y obliga a regrabar el paso 06. |
| 08e-aprobar-y-estado | **OK** (con observaciones) | Los contrastes se ven. Hay una incoherencia menor en la voz: nombra la cotización uno y luego abre la seis. |
| 08f-herencia | **CORREGIR** | El caso conocido de 2:02 está confirmado: en esta toma lo que se corta es la cabecera de la tabla Personas, entre 1:54 y 2:10. |
| 08g-cambio-en-vivo | **CORREGIR** | En 3:58–4:14 el detalle del evento se desplaza y oculta «QUÉ CAMBIÓ», y la marca resalta los códigos `PERMISSIONS_CHANGED` y el UUID de la solicitud. |
| 08h-administrar-la-seguridad | **CORREGIR** | En 2:14–2:40 el editor corta filas bajo la leyenda fija. En 2:17 la voz dice que Marta no ve «Integraciones» mientras se resalta una barra de pestañas donde sí aparece. |
| 09-lo-que-se-movio | **OK** (con observaciones) | Nada bloquea. El OCR de la auditoría marcó un RNC que es un falso positivo causado por el cursor. |

### Patrón que se repite en toda la serie (no bloquea por sí solo; corregirlo si se regraba)

**La insignia del contraste siguiente aparece antes de cambiar de persona.** Durante 8–12 s la pantalla contradice a
la insignia:
- 08c 0:51 «Sin permiso · Ana · Exportar» sobre la lista de Pedro, que todavía tiene Importar/Exportar (`017`, `018`).
- 08c 1:46 «Con permiso · Rosa · Eliminar» sobre la lista de Ana, sin papelera (`034`).
- 08c 2:48 «Sin permiso · Pedro · Eliminar» sobre la lista de Rosa, **con la papelera a la vista** (`052`).
- 08e 1:19 «Sin permiso · Ana · Aprobar» sobre la cotización que Carlos acaba de aprobar (`027`).
- Lo mismo en 08d 1:18 y 2:38, 08g 0:33 y 1:42, y 08h 2:40.

Tipo **guion**. Propuesta: que el paso ponga primero una insignia neutra («Cambio de persona → Ana») y que la
insignia del contraste se ancle a «Ya dentro» (o a la marca `aside.sidebar` posterior al login).

**El cursor se queda encima de la cifra o de la etiqueta que se lee.** Pasa con «1 – 8 de 8», «1 – 3 de 3», «1 – 5 de
5» y «1 – 10 de 25», con el paso «Aprobada» de la barra de estados (su ayuda emergente lo tapa) y con «Ver» en el
detalle de auditoría. Tipo **guion**. Propuesta: `"cursor": false` en las marcas que solo leen un texto.

---

## 08c-exportar-eliminar — OK

| mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|
| 0:34 | 01-con-exportar | `010-00m34.01s` | motor | La insignia tapa el final del título del diálogo («Importar / Exportar ~~productos~~») mientras la marca señala el diálogo. | Al abrirse un `mat-dialog-container`, la insignia se aparta o se oculta (el mismo criterio que usa el cartel en `df2bdf8`). |
| 2:15 | 03-entra-rosa | `045-02m15.00s`, `rev-132`, `extra-136.2s` | motor | La marca «Entrando» sigue unos 0,5–1 s después de que el login cambia a Inicio: queda una caja naranja huérfana sobre «Clientes / Proveedores». | Apagar la marca cuando cambia la ruta, o que la marca puente `…'Entrando'), aside.sidebar` reemplace a la anterior. |
| 2:15 | 03-entra-rosa | `extra-136.2s` | ERP (baja) | Durante unos segundos la barra superior dice «Rosa.Almanzar» con el avatar «R» (el usuario) antes de mostrar «Rosa Almánzar / RA». | Pintar el nombre completo desde la respuesta del login, o mostrar un esqueleto mientras llega el perfil. |
| 3:34 | 06-sin-eliminar | `067-03m34.38s` | guion | Con «pero no la papelera: Eliminar no aparece», la marca cae sobre el interruptor rojo de **Desactivar**. Un novato puede tomar ese botón rojo por la papelera. | Marcar la celda completa de acciones (`tr:has-text('Machete de 22') td:last-child`) o decir «la fila termina en Desactivar». |
| 0:47, 3:46 | 01 · 06 | SRT | motor (baja) | Hay cues de una sola palabra («computadora.») y tres solapes de hasta 0,19 s. | Revisar el partidor del SRT para que no deje una palabra sola en una cue. |

Revisado sin defecto: la insignia y el cartel «Con/Sin permiso: …»; el diálogo (pestañas Importar/Exportar y los
botones Exportar Excel y CSV); Ana solo tiene el lápiz «Abrir»; Rosa tiene 4 acciones y Pedro 3; el cartel «Consejo»
no tapa la fila explicada.

## 08d-alcance — CORREGIR

| mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|
| **3:29–3:47** | **06-cambiar-a-equipo** | `066-03m29.16s`, `068`, `069`, `072`, `074` | **motor** | Al marcar `.rpe__scope-seg[aria-label='Alcance de Ver en Cotizaciones']`, el panel interior se desplaza y la cabecera del recurso **Cotizaciones** (✓Ver ✓Crear ✓Editar, visible en `065` a las 3:25) queda debajo de la leyenda fija. La voz dice «En el recurso Cotizaciones, el permiso Ver trae su alcance», pero en pantalla solo se ven «Aceptar/Liquidar Cotización» y un «Ver · Propios · Equipo · Todos» suelto. «Detalles Cotizaciones» también queda cortado abajo. Es el mismo patrón que G-14/G-19. | **Regrabar el paso 06** con el motor corregido (`e1810d6`). Si no, marcar primero `.rpe__resource-name:text-is('Cotizaciones')` y pulsar el segmento sin que la marca centre el bloque. |
| 1:17 | 02-todos | `021-01m17.52s` | guion | Con «su permiso de ver tiene alcance Todos», la marca resalta la cabecera «N°» de la tabla. No se relaciona con la frase, y se alarga hasta «Ahora la misma lista con Ana». | Marcar el paginador «1 – 8 de 8» con `"cursor": false`. |
| 2:14 | 04-ajena-por-numero | `043-02m14.58s` | guion / motor | La dirección que «Ana escribe en el navegador» no aparece en ninguna parte: el diálogo «Acceso Denegado» sale sin transición. Además, su marca automática llega desplazada unos 20 px durante la animación. | Mostrar un cartel breve con la dirección (`/sales/quotes/4`) antes de navegar; lo mismo vale para 08g-04. |
| 4:31 | 07-equipo | `091-04m31.11s` | guion (baja) | El cartel «Consejo» tapa la fila COT 1, que forma parte de «sus tres». | Poner el cartel después de la frase, o elegir otra esquina. |
| 1:50 | 03-propios | `035` | — | «Buenos días, Ana» aquí frente a «Buenas noches» en el resto de la serie: la toma cruzó la medianoche. La voz no lo menciona, así que no es un defecto (R13). | — |

Revisado sin defecto: la lámina de alcance y sus 3 fases (8 de 8, 3 de 8, Equipo 5 de 8); los tres contrastes del
paginador (1–8, 1–3 y 1–5 de 5 con COT 5 y 4); el diálogo «Su rol solo le permite ver y trabajar las cotizaciones que
usted creó…» con «Entendido»; la barra «1 cambio sin guardar · afectan a 3 personas» y el aviso de éxito.

## 08e-aprobar-y-estado — OK

| mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|
| 2:43–3:04 | 04-con-estado-aprobada | `061`, `067` | guion | La voz dice «recuerda que la cotización uno ya quedó aprobada hace un momento» y enseguida abre **la seis**, sin decir por qué. Un novato espera ver la uno. | Abrir COT 1 (está Aprobada, como se ve en la lista a las 3:22) o decir «abro otra aprobada, la seis». |
| 1:16, 3:04 | 02 · 04 | `026`, `069` | guion | La marca sobre el paso «Aprobada» queda tapada por el cursor y por su ayuda emergente: la palabra no se lee. Solo la salva la insignia «Aprobada» del título. | `"cursor": false`, o marcar la insignia del título `.page-hero-title`. |
| 0:52–3:44 | 02–05 | `017`, `069`, `078` | ERP (baja) | Aparece un ⚠ naranja en la primera línea de cada cotización y nadie lo explica. Es un aviso de existencias. | Ninguna en el video, o una frase breve si se regraba. |
| 1:16 | 02 | `026` | ERP (baja) | Con la cotización ya aprobada y de solo lectura, siguen visibles «Cancelar» y un «Guardar» apagado. | Que el formulario de solo lectura muestre solo «Volver». |

Revisado sin defecto: la lámina estado-documento (Bloqueado → Permitido); el diálogo «Aprobar cotización» y el aviso
«Éxito · Estado actualizado correctamente»; con Ana, el paso Aprobada gris y el Borrador que no cambia; el contraste
de «Más acciones» (con Convertir a factura / solo Versiones e historial y Duplicar); el cartel «Cuidado».

## 08f-herencia — CORREGIR

| mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|
| **1:54–2:10** (el «2:02» conocido) | **03-llega-al-hijo** | `029`, `030`, `031`, `rev-122.5` | **motor / ERP** | La lista de Personas se desplaza para enseñar a Carlos y su cabecera (PERSONA · ROLES · ÚLTIMO INGRESO · ESTADO) queda cortada por la mitad bajo «Todas · 9». En esta toma, «Permisos efectivos» sí se lee entero (Productos 1/42, Clientes y Proveedores 2/37). | **Regrabar el paso 03** con el motor de `e1810d6`, o abrir a Carlos filtrando antes por nombre para que la lista no se desplace. |
| 2:53 | 05-sin-excluido | `044-02m53.49s` | ERP / motor (baja) | En la segunda visita la lista vuelve arriba y la fila de Carlos, la abierta, queda cortada abajo («Carlos Pime…»). | La misma corrección que en el paso 03. |
| 1:12, 2:32 | 02 · 04 | `016`, `036` | ERP (baja, texto) | La barra de guardado dice «1 cambio sin guardar · **afectan** a 1 persona» (y «afectan a 3 personas»): el verbo concuerda con las personas y no con «cambio». La voz dice bien «afecta». | Cambiar la barra a «· afecta a N persona(s)». |
| 1:59 | 03 | `030` | ERP (baja) | El editor cuenta «de 1103 permisos» y la ficha «12 / 1160»: dos totales distintos para lo mismo. | Unificar el denominador, o no mostrar el total en la ficha. |

Revisado sin defecto: la lámina acceso-efectivo y sus 4 fases; «Crear» concedido en el padre, el chip «Hereda de
Vendedor» y el Crear heredado en el hijo; la exclusión tachada; 2/37 → 1/37 y 12 → 11 en la ficha; el cartel
«Cuidado»; los avisos de éxito.

## 08g-cambio-en-vivo — CORREGIR

| mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|
| **3:58–4:14** | **05-el-rastro** | `079-03m58.04s`, `080-04m05.27s` | **motor** | La marca `.sec-audit__facts` desplaza el panel del detalle: el título **QUÉ CAMBIÓ** desaparece (en `078` estaba en y=451) y «Inventario · Productos / Ver → –» queda sin su título durante 16 s, incluido todo el resumen. | **Regrabar el paso 05**: marcar solo `.sec-audit__facts` con el motor corregido, o cerrar el resumen con el panel en su posición inicial. |
| 3:58 | 05-el-rastro | `079` | ERP + guion | La marca resalta el bloque entero de Solicitud, con «Evento **PERMISSIONS_CHANGED**» y «Solicitud 83d7e5dc-…» (código interno y UUID en inglés), pero la voz solo nombra «la dirección de la computadora y el navegador». | ERP: ocultar Evento y Solicitud o traducir el evento («Cambió permisos»). Guion: marcar solo las filas IP y Origen. |
| 2:36 | 04-por-direccion | `054` | guion | Igual que en 08d-04: la dirección escrita no se ve. El aviso naranja «No tienes permiso para ver «Productos»…» sí se ve bien. El botón «Cerrar» del aviso tiene poco contraste (naranja sobre naranja), un detalle del ERP. | Cartel con la dirección. |
| 0:20 | 01-antes | `007` | guion (baja) | El cursor tapa «1 – 10 de 25». | `"cursor": false`. |

Revisado sin defecto: el contraste del menú (Inventario presente y luego ausente, con Inicio, Ventas, Calendario y
Configuración), «Ver» concedido y luego sin conceder, «afectan a 3 personas», los avisos, «Cambió permisos · Rol
#77», IP 192.168.1.25 y Chrome · Windows, y «Inventario · Productos».

## 08h-administrar-la-seguridad — CORREGIR

| mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|
| **2:14–2:40** | **04-dar-solo-ver** | `037`, `040`, `041`, `042`, `045` | **motor** | Al centrar «Usuarios de Integración», el panel interior se desplaza: queda un fragmento «0/1 Conceder todo» sin nombre debajo de la leyenda fija y «Visibilidad de Menú» sale cortado abajo. En 2:28 la barra de guardado queda cortada (solo se ve su texto) y en 2:31 la marca de la barra se queda en un hueco vacío bajo «Guardando…» (`042`). | **Regrabar el paso 04** con el motor de `e1810d6`, o buscar «Integración» en «Buscar permiso…» para que el recurso quede solo. |
| 2:17 | 04-dar-solo-ver | `038-02m17.68s` | guion | La voz dice «Por eso Marta ni siquiera ve la pestaña Integraciones» mientras se resalta la barra de pestañas **de Rosa**, donde «Integraciones 1» sí aparece. Pantalla y voz se contradicen. | Quitar la marca, o decir «en la sesión de Marta, esta pestaña no le aparece» y marcar solo `a[mat-tab-link]:has-text('Integraciones')`. |
| 0:22–0:43 · 3:22–3:38 | 01 · 05 | `005`, `007`, `010`, `067`, `070` | ERP / motor (baja) | La lista Personas está desplazada para enseñar a Ana: no se ve la cabecera de columnas y la primera fila («pedro.nunez@…») queda cortada. | Lo mismo que en 08f-03. |
| 3:50–3:57 | 06-sin-equipos | `074`, `075` | guion | Las marcas llegan una frase tarde. Con «junto al título Equipos no está el botón de sumar» se marca «Zona Este»; con «arriba de la lista no hay Editar equipo ni la papelera» se marca la etiqueta EQUIPOS, y la esquina superior derecha, donde faltan esos botones, no recibe ninguna marca. | Anclar `.sec-people__teams-label` a «junto» y marcar `.sec-people__title`/la barra superior en «arriba de la lista». |
| 1:01 | 02-con-equipos | `016` | guion (baja) | La marca de la papelera llega cuando la voz ya dice «Y para mover personas…». | Anclarla a «papelera». |
| 1:54, 3:46 | 03 · 06 | SRT | motor (baja) | Hay cues de una palabra («Germiva.», «credenciales.») y solapes de 0,19 s. | La misma corrección que en 08c. |

Revisado sin defecto: los contrastes de Rosa y Marta (Editar/Cambiar contraseña/Asignar rol presentes y luego
ausentes; «Más acciones» con 3 opciones y luego solo «Ver su actividad»; «+» de equipos, Editar equipo y papelera
presentes y luego ausentes; barra con Agregar/Quitar y luego solo Limpiar; Nueva credencial; «Editar permisos» →
«Ver permisos»; Rotar secreto y los tres puntos ausentes), las insignias y el cartel «Consejo».

## 09-lo-que-se-movio — OK

| mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|
| 2:40 | 03b-historial-viejo | `049-02m40.60s` | ERP + guion | La voz dice «ya viene filtrada por ese registro… el del rol Almacén», pero el filtro Registro solo muestra **«roles»** (el nombre interno de la tabla, sin número) y la lista dice «Rol #79». En pantalla no aparece «Almacén» en ningún sitio. | ERP: que el filtro muestre «Rol #79» o «Almacén». Guion: decir «el rol número setenta y nueve, Almacén». |
| 2:18 | 03-perfil-consultorio | `045-02m18.59s` | guion (baja) | El cartel «En RegiSalud» tapa la ayuda emergente «Configuración» del elemento marcado. | Mover el cartel o marcar antes de mostrarlo. |
| 2:12–2:16 | 03-perfil-consultorio | `auditoria-video/00066-68.png` | — (falso positivo) | La auditoría OCR lee el RNC «130955036». El fotograma muestra el RNC ficticio **130555036** con el cursor encima de una cifra. No hay dato real. | Ninguna (justificar en el informe de auditoría). |
| 0:22, 2:55 | 01 · 04 | `005`, `054` | ERP (baja, texto) | Mi perfil mezcla tratamientos: «Cambie su contraseña», «Actualice su nombre», «Personalice su experiencia» frente a «Elige qué módulos…». Además, la miga de pan repite «Mi Perfil / Perfil / Mi Perfil». | Unificar en tú y dejar la miga «Mi perfil». |
| 0:04 | 01 | `001` | — (canon) | El Inicio dice «domingo, 27 de septiembre» y los videos 08 dicen «lunes, 28». La voz no lo nombra, así que no es un defecto. | — |

Revisado sin defecto: la tarjeta Seguridad y el formulario de contraseña (sin pulsar Actualizar); Visibilidad del
menú (Inicio con candado; Compras apagado y luego ausente del riel; «Cambios Guardados»; «¿Restablecer Todo?» con
«Sí, restablecer»; «Menús Restablecidos»; Compras de vuelta); la redirección del historial viejo a Auditoría con 3
eventos; `/security/settings` → Mi perfil; el candado de Seguridad.

---

## Datos y privacidad (los 7 videos)

Solo aparecen datos ficticios: Distribuidora Las Palmas, RNC 130555036, las cuentas @germiva.demo, Rosa, Ana, José,
Carlos, Pedro, Marta, Héctor, Luisa y Sonia, e IP 192.168.1.25. `auditoria-video.txt` da «Sin hallazgos» en 08c–08h;
el único aviso de 09 es el falso positivo de arriba. No encontré inglés en la voz ni en los subtítulos. En pantalla hay
inglés o códigos técnicos solo en 08g (PERMISSIONS_CHANGED y el UUID) y en 09 («roles» en el filtro).

## Orden de regrabación sugerido

1. **08d paso 06**, **08g paso 05**, **08h paso 04** y **08f paso 03**, todos con el motor corregido en `e1810d6`.
2. Si se regraban, aprovechar para corregir en esos guiones la insignia adelantada y `"cursor": false` en las
   lecturas.
3. Las entradas marcadas «ERP» van a la cola del ERP y no bloquean los videos.
