# Revisión semántica · serie «Seguridad» (puerta antes de grabar, 2026-09-27)

Revisor semántico. Leídos: skill `germiva-video` (REVIEWER + «Puerta semántica»), `_CONVENCIONES-SEGURIDAD.md`,
`_SERIE-SEGURIDAD.md`, `_SELECTORES-SEGURIDAD.md`, `seeds/seguridad/README.md` (canon E0), `HALLAZGOS-SEGURIDAD-VIDEO.md`,
los 21 `seguridad-*.json` con sus `_INFORME-AUTOR-*.md` y los 4 diagramas de `marca/diagramas/`.
Contrastado contra los volcados de `exploracion-seguridad/` cuando la voz afirmaba algo que _SELECTORES no cubría.
Sin apps, sin navegador, sin git.

## Resultado

| Guion | BLOQ. | MEJORA | Aplicadas | Puertas tras aplicar |
|---|---|---|---|---|
| 00-introduccion | 0 | 0 | — | sin cambios |
| 01-resumen | 0 | 4 | 4 | revisar 0 ERROR · verificar 0 |
| 02a-roles | 0 | 1 | 0 | sin cambios |
| 02b-editor-permisos | 0 | 0 | — | sin cambios |
| 03-herencia | 0 | 1 | 1 | 0 · 0 |
| 04a-personas | 0 | 5 | 5 | 0 · 0 |
| 04b-alta-y-edicion | 0 | 2 | 1 | 0 · 0 |
| 04c-equipos | 1 | 0 | 1 | 0 · 0 |
| 05-acceso-efectivo | 1 | 0 | 1 | 0 · 0 |
| 06a-credenciales | 0 | 2 | 1 | 0 · 0 |
| 06b-rotar-pausar-revocar | 0 | 0 | — | sin cambios |
| 06c-caso-integracion | 0 | 1 | 1 | 0 · 0 |
| 07-auditoria | 0 | 3 | 2 | 0 · 0 |
| 08a-vista | 1 | 2 | 3 | 0 · 0 |
| 08b-crear-editar-anular | 0 | 3 | 2 | 0 · 0 |
| 08c-exportar-eliminar | 1 | 2 | 3 | 0 · 0 |
| 08d-alcance | 0 | 3 | 3 | 0 · 0 |
| 08e-aprobar-y-estado | 0 | 1 | 1 | 0 · 0 |
| 08f-herencia | 0 | 2 | 1 | 0 · 0 |
| 08g-cambio-en-vivo | 2 | 2 | 4 | 0 · 0 |
| 09-lo-que-se-movio | 0 | 2 | 2 | 0 · 0 |
| **Total** | **6** | **36** | **36** (6 bloqueantes + 30 mejoras) | 17 tocados: `revisar.mjs` 0 ERROR (avisos iguales que antes) · `tut verificar` 0 errores, 0 avisos |

Los avisos de `revisar.mjs` son los mismos que ya traían los guiones, y todos estaban justificados en su `_comentario`: el primer paso sin `panel-collapse` y marcas en la zona del FAB, sobre el paginador o el pie del formulario. Los JSON conservan su formato de fin de línea (CRLF; 08a en LF, como estaba).

## Comprobado y correcto (no se tocó)

- Cifras E0 dichas en voz: Personas 9, Activas 8, Sin rol 1, Nunca entraron 1, Inactivas 1, «Roles y permisos 12» (5 de la empresa + 7 del sistema), 4 asuntos → 3 tras revocar, Ana 5/1160 (Cotizaciones 3/19), Carlos 11 (7/19, Facturación 2), José 10 en 4 módulos, «afectan a 3 / 1 personas», pies 8/3/5, Q1…Q8 por autor, 3 facturas en 06c, credencial 5 → 4 permisos, «ver y aprobar comprobantes» (eCF: Ver, Aprobar).
- Posiciones: el buscador y «Nuevo» están a la derecha (x 820/1128), la Actividad reciente está a la derecha (x 506) y trae 10 filas, «Seguridad» del riel es el candado (icono `lock`), Compras queda justo debajo de Ventas en el riel de Rosa, «Inicio» lleva candado en Visibilidad del menú. El ojo abre en Cotizaciones (`visibility`), el lápiz en Productos (`edit`), y Marta no tiene ⋮ en la lista. El excluido sale tachado (`text-decoration: line-through`). La Solicitud trae número («Solicitud c622…»). Los colores de la bitácora salen de `security-console.shared.ts`: verde creó, azul actualizó, rojo eliminó, ámbar cambió estado, gris acceso. «Ya lo guardé» es el tooltip de la ✕.
- Selector `.console-tabs a` (00-04): existe (volcado fin-01). `:text-is('Crear')` sobre un heredado casa, porque el heredado no lleva icono (03, 08f).
- Diagramas: los cuatro casan con E0 y con la voz. En `conceptos-seguridad` el equipo «No da permisos». En `acceso-efectivo` el equipo no suma y el resultado dice «11 en total; aquí, 4 de ejemplo». En `alcance-propios-todos` salen 8/3/5 con los autores correctos, y en `estado-documento` la COT 1 va de Borrador a Aprobada.
- Verdades del sistema: ningún guion habla de un «filtro por estado del documento». 02b y 08e lo niegan de forma explícita. El equipo nunca suma permisos, y el alcance va por quien creó el registro. «Clientes» se trata como «Socios».
- Temas obligatorios de cartel: mínimo privilegio (06a, 08d), secreto una sola vez (06a), revisar la auditoría (07), no compartir usuarios (04b) y desactivar en vez de borrar (04b). Los 21 guiones tienen de 1 a 2 carteles, un `capitulo` en cada paso y un cierre con caso práctico o resumen.
- Con y sin permiso: 08a–08e y 08g muestran el MISMO punto, primero con permiso y luego sin él. En cada cambio de usuario, la insignia es la de quien entra.

## Correcciones por guion

### 01-resumen
- MEJORA ✔ `01-cifras`: «lo que se modificó esta semana» → «en los últimos siete días». La cifra cuenta 7 días, no la semana del calendario.
- MEJORA ✔ `02-requiere-atencion`: «Hoy hay cuatro asuntos» → «Ahora hay…». Así lo pide R13.
- MEJORA ✔ `03-actividad-reciente`: «la dirección de red **del equipo**» → «de la computadora». En esta serie, «equipo» significa Zona Este, así que la palabra confunde. Se corrigió igual en 04a, 07, 08c y 08g.
- MEJORA ✔ `04-caso-practico`: «en el video de Personas» → «en el video de Personas y en el de alta y edición». Desactivar se enseña en 04b.
- Dependencia (ya declarada): `03` pulsa `.sec-ov__row:has-text('Cambió permisos')`, que exige D-S6 corregido. Hoy la fila dice «Actualizó · Roles #79».

### 02a-roles
- MEJORA ✘ `04-crear-rol` acciones 9–10: la voz habla del error por nombre repetido y del aviso al salir sin guardar, pero las marcas señalan el título y la descripción del rol Cobrador. Se puede aceptar (señalan «el nombre»). Si el autor retoca el paso, conviene quitar esas dos marcas.

### 03-herencia
- MEJORA ✔ `01-rol-hijo`: «le llega solo al hijo» se puede entender como «únicamente al hijo». Se cambió por «le llega al hijo automáticamente».

### 04a-personas
- MEJORA ✔ `01-vistas`: «las que hoy pueden entrar» → «las que pueden entrar» (R13).
- MEJORA ✔ `01-vistas`: «de la una a la nueve, de nueve» sonaba a horas. Se cambió por «del uno al nueve, de nueve».
- MEJORA ✔ `03-ficha`: «el número que identifica **al equipo**» → «a la computadora».
- MEJORA ✔ `05-caso`: «su cuenta podría ver cotizaciones» no era exacto, porque con «Propios» y sin cotizaciones propias Héctor vería 0. Se cambió por «es una puerta abierta a Ventas que nadie está usando».
- MEJORA ✔ `05-caso`: decía «Hazlo cada mes» y el cartel «Revisa cada mes», mientras que 01 habla de una revisión semanal y 07 de revisar cada semana. Se alineó todo a «cada semana»: voz, cartel y ancla `cada semana`.

### 04b-alta-y-edicion
- MEJORA ✔ `01-crear-usuario`: «un vendedor que empieza hoy» → «que acaba de entrar a la empresa» (R13).
- MEJORA ✘ `03-asignar-rol` acción 11: la voz habla de «tu propia ficha», pero la marca cae sobre el título del bloque de Julio. Se deja así: enseñar la ficha propia exigiría navegar.

### 04c-equipos
- **BLOQUEANTE ✔** `04-quitar-editar-eliminar`: decía «Héctor **se queda en el este**», pero Héctor NO es de Zona Este (solo Ana y José). Ahora dice «al final Héctor no va a cubrir el norte, así que marco su casilla».

### 05-acceso-efectivo
- **BLOQUEANTE ✔** `02-herencia-en-la-persona`: decía «ver, crear y editar, **que son de Vendedor**», lo que contradice 03-01 («Ver… es directo: se lo dimos al sénior con alcance Todos») y el canon (Sénior tiene «Cotizaciones · Ver» directo). Ahora dice «ver, crear y editar, como cualquier vendedor, aunque él las ve todas; más aprobar, rechazar, aceptar y convertir, que son solo de su rol».

### 06a-credenciales
- MEJORA ✔ `02-crear-credencial`: «Hoy las dejo vacías» → «Esta vez las dejo vacías».
- MEJORA ✘ `01`: abre con «Seguimos en la consola…» en un video que se ve suelto. Es un detalle menor y se deja.

### 06c-caso-integracion
- MEJORA ✔ `04-conceder`: «la casilla de Productos, **la primera**» afirmaba un orden que nadie verificó. Ahora dice «la casilla de Productos a secas». Se conservó la duración del paso: sin esas palabras, «La marco» chocaba con el ancla anterior.
- A verificar en el ensayo: la voz dice «veinticinco productos» en `05`, pero la lámina pinta `j.total ?? datos.length` y `GET /v1/product` puede venir paginado. Si la cifra no sale 25, cambiar la voz a «los productos del catálogo».

### 07-auditoria
- MEJORA ✔ `01-la-bitacora`: «Estoy en Seguridad, la consola de Rosa…» chocaba con la voz en primera persona que usa toda la serie. Ahora dice «Soy Rosa, la administradora de Distribuidora Las Palmas, y estoy en la consola de Seguridad».
- MEJORA ✔ `01`, `02` y `03`: «dirección / IP **del equipo**» → «de la computadora». En `aprenderas` también: «desde qué computadora».
- MEJORA ✘ `04` acción 7: ya en Personas, se marca la pestaña Auditoría mientras la voz habla de «Cargar eventos anteriores». Se puede aceptar como referencia a la pestaña, y se deja.
- Dependencias (ya declaradas): D-S5 (02 escribe en los filtros de texto), D-S6/D-S7.

### 08a-vista
- **BLOQUEANTE ✔** `02-sin-ventas-menu`: decía «pedro punto **núñez**», pero el usuario tecleado es `pedro.nunez`, y la ñ se oye distinta. Ahora dice «pedro punto nunez, en minúsculas y sin eñe».
- MEJORA ✔ `04-con-seguridad`: «marta punto guzmán» → «guzman». El SRT sale del guion y el usuario no lleva tilde.
- MEJORA ✔ `04-con-seguridad`: «todas las **casillas** de permisos salen en gris» → «todos los botones… los ve, pero no los puede tocar». En el editor son botones, y así los llama 02b.

### 08b-crear-editar-anular
- MEJORA ✔ `03-sin-crear`: «marta punto guzmán» → «guzman».
- MEJORA ✔ `04-sin-editar-anular`: «no hay Guardar ni **Cancelar**» → «no hay Guardar». El botón «Cancelar» no está verificado y se confunde con el paso «Cancelada», que es anular.
- MEJORA ✘ `02`: «el total se recalcula solo» no está verificado. Hay que confirmarlo en el ensayo junto con `input[formcontrolname='quantity']`.

### 08c-exportar-eliminar
- **BLOQUEANTE ✔** `05-entra-pedro`: «pedro punto núñez» → «pedro punto nunez, en minúsculas y sin eñe».
- MEJORA ✔ `01-con-exportar`: «se descarga en su **equipo**» → «en su computadora».
- MEJORA ✔ `02` y `03`: «ana punto mejía» → «mejia» y «rosa punto almánzar» → «almanzar».

### 08d-alcance
- MEJORA ✔ `03` y `07`: «mejía» → «mejia». En `05`: «almánzar» → «almanzar».
- MEJORA ✔ `06-cambiar-a-equipo`: «En la lista de módulos, **a la izquierda**» contradecía 02b («en el centro»): la columna de módulos va en x 336, junto al riel de roles. Ahora dice «En la columna de módulos, junto a la lista de roles».
- MEJORA ✔ `06`: «Hoy está en Propios» → «Ahora está en Propios».
- Dependencia fuerte: `04-ajena-por-numero` afirma el aviso del 403 de alcance. Hoy la UI vuelve muda a la lista (D-S4). `_SERIE` §1 verdad 3 pedía no afirmar nada sobre abrir por número, y `_CONVENCIONES` sí lo afirma. Si la ronda 2 no corrige D-S4, **hay que quitar el paso 04 antes de grabar**.

### 08e-aprobar-y-estado
- MEJORA ✔ `03-sin-aprobar`: «mejía» → «mejia».
- Dependencias (ya declaradas): el modal D-S1, y el clic en «Aprobada», porque `.step-wrapper.chevron-wrapper` intercepta el puntero.

### 08f-herencia
- MEJORA ✔ `01-la-herencia`: «le llega solo» → «le llega automáticamente».
- MEJORA ✘ (diseño): el con/sin se enseña con la cifra «Clientes y Proveedores 2/37 → 1/37» de la ficha de Carlos que ve Rosa. El plan pedía entrar como Carlos y ver «Nuevo Cliente» en `/sales/partners`. Es el mismo punto con las insignias correctas, así que vale, pero la prueba es más débil. Si sobra duración, añadir el login de Carlos en `03` y `05`.

### 08g-cambio-en-vivo
- **BLOQUEANTE ✔** `02-quitar-y-guardar`, acciones 10 y 11: `.rpe__act:text-is('Ver')` no casa con un «Ver» CONCEDIDO, porque lleva el icono dentro («check Ver», volcados a7-02 y fin-05, y la nota del autor de 02b). La marca y el clic habrían fallado. Se cambió a `.rpe__resource:has(.rpe__resource-name:text-is('Productos')) .rpe__act--direct` (Vendedor solo tiene «Ver» concedido en Productos).
- **BLOQUEANTE ✔** `02`: decía «el servidor ya no le entrega productos a **ningún vendedor**», y es falso: José (Vendedor + Almacén) los sigue viendo por Almacén. Ahora dice «…a quien los veía solo gracias a este rol».
- MEJORA ✔ `02`: «En la lista de módulos» → «En la columna de módulos». También «almánzar» → «almanzar».
- MEJORA ✔ `03`: «mejía» → «mejia». En `05`: «guzmán» → «guzman», y «la dirección **del equipo**» → «de la computadora».

### 09-lo-que-se-movio
- MEJORA ✔ `01`: «hoy no la cambio» → «esta vez no la cambio» (R13).
- MEJORA ✔ `pronunciacion`: se añadió `"ERP": "e-erre-pe"`, porque en `03` se dice «ERP» y no tenía fonética.

## Queda para el ensayo (no se puede cerrar sin apps)

1. **Ronda 2**: D-S6 (01-03), D-S5 (07-02), D-S1 (08b y 08e: modal al abrir la cotización), D-S2 (08c y 08g: modal «Impuestos» y fotos rotas), D-S4 (08d-04: si no está corregido, quitar el paso) y D-S7 (etiquetas del registro y actor).
2. **06c**: los selectores de la lámina (`#btn-*`, `#res-*`) no se han probado en navegador, y falta confirmar la cifra «veinticinco productos».
3. **08b-02**: el campo `quantity` (primera línea) y lo que sale al guardar. **08e-02**: el clic sobre el paso «Aprobada».
4. **08f-05**: «Clientes y Proveedores 1/37» después de la exclusión. **08g-02**: el nuevo selector `.rpe__act--direct` en Productos, que debe ser único para Vendedor.
5. Marcas fuera del pliegue que el motor desplaza: «Seguridad» del riel de Rosa (y=716), la fila del cambio en la Actividad reciente (y=790, scroll interno), las casillas de Carlos y Héctor, y la tarjeta «Seguridad» de Mi perfil.
