# Ensayo · serie «Seguridad» · tanda 3 (OPERADOR-ENSAYO, 2026-09-27)

Guiones: 07, 08a, 08b, 08c, 08d, 08e, 08f, 08g y 08h. Apps: API `dist` :3001 y front estático :4200, sin reiniciar. Un solo
navegador headless 1280×720 (dsf 1.5). Cada ensayo y cada sonda corrieron bajo `seeds/_puertas/NAVEGADOR.lock`
(«ENSAYANDO <guion> <pid>»), tomado con `wx` desde el proceso node vivo que lanzaba el ensayo y borrado solo si seguía siendo
suyo. Antes y después de cada corrida se restauró E0 (`restaurar.mjs E0`; también tras las dos sondas que escribieron por SQL).
Al terminar quedó **E0**. Logs con líneas `──` de paso (R28) y capturas en
`germiva/qa-seguridad-ensayos-2026-09-27/<guion>/`.

## Resultado

| Guion | Pasos | Acciones | Fallos 1.ª → final | revisar | verificar | Duración estimada |
|---|---|---|---|---|---|---|
| 07-auditoria | 4 | 53 | 41 (1 raíz) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:59 + 6 s ≈ **4:05** |
| 08a-vista | 5 | 47 | 0 (2 afirmaciones falsas) → **0** | 0 · 3 | 0 · 0 | 3:42 + 6 s ≈ **3:48** |
| 08b-crear-editar-anular | 4 | 42 | 0 (FAB, afirmación) → **0** | 0 · 5 | 0 · 0 | 2:51 + 6 s ≈ **2:57** |
| 08c-exportar-eliminar | 6 | 49 | 2 → **0** | 0 · 3 | 0 · 0 | 3:23 + 6 s ≈ **3:29** |
| 08d-alcance | 7 | 66 | 0 → **0** | 0 · 9 | 0 · 0 | 4:01 + 6 s ≈ **4:07** (al borde) |
| 08e-aprobar-y-estado | 5 | 59 | 2 → **0** | 0 · 3 | 0 · 0 | 3:15 + 6 s ≈ **3:21** |
| 08f-herencia | 5 | 39 | 0 (cifra bajo el FAB) → **0** | 0 · 1 | 0 · 0 | 2:51 + 6 s ≈ **2:57** |
| 08g-cambio-en-vivo | 5 | 59 | 0 → **0** | 0 · 5 | 0 · 0 | 3:33 + 6 s ≈ **3:39** |
| 08h-administrar-la-seguridad | 7 | 79 | 10 (1 raíz) → **0** | 0 · 2 | 0 · 0 | 3:55 + 6 s ≈ **4:01** |

Avisos que quedan, todos justificados en el `_comentario` de cada guion:

- Primer paso sin `button.panel-collapse`: no existe en `/security/*`, en `/home` ni en la lámina.
- «dos marcas a la vez» entre `…:has-text('Entrando')` y `aside.sidebar`: artefacto de la predicción. La marca del menú no
  lleva ancla y el motor la pinta cuando termina el login, 5–11 s después, no a los 0,4 s.
- Marcas sobre el paginador o el pie del formulario: el rango queda a la izquierda del FAB, y «Guardar» / «Volver» caen en
  x≈1140, fuera de él.

## Receta común: cambio de usuario EN CÁMARA (a)

Hubo que corregir la voz de los ocho guiones 08:

- **El botón no dice «Entrar»**: dice «Iniciar sesión». Mientras entra, muestra un spinner y «Entrando…». La voz ahora dice
  «pulso Iniciar sesión; el botón dice Entrando…».
- **Marcas del login**:
  - una marca anclada a «Entrando» sobre `button.auth-primary-btn:has-text('Entrando')`, a +2 s del clic, con 3000 ms y
    `cursor: false`;
  - después, la marca sin ancla sobre `aside.sidebar`, que sale cuando el login termina.
- **Relleno de voz**: entre «Entrando» y la primera acción de la pantalla nueva hay 10–12 s de voz («Ya dentro, abro…»). Así
  la voz nunca describe el menú mientras la pantalla todavía es la de acceso, y ningún tramo pasa de 10 s sin cambios en
  pantalla. En 08g-03, donde la voz se alarga, se añadieron dos marcas: una sobre el riel y otra sobre el saludo del Inicio.
- **Login medido en esta tanda**: 5,1–10,8 s del clic al menú. Carlos tardó 10,8 s una vez y Marta 8,2–10,8 s.
- **La insignia sobrevive al cierre de sesión**. `logout()` solo borra claves propias de sessionStorage, y la captura de cada
  paso tras el login la muestra: 08a-02, 08a-04, 08b-03, etc.
- **El panel del menú sigue contraído** tras cerrar sesión (localStorage). Si el paso entra con `navegar` (08c-04 y 08c-06),
  `button.panel-collapse` no existe: se quitó el clic y la voz lo dice. Si el paso entra pulsando «Ventas» en el riel, el
  panel se vuelve a abrir y el clic sí funciona.

## Fallos y correcciones por guion

### 07-auditoria (d)

- **41 fallos, 1 sola raíz.** El clic en la pestaña «Auditoría» cayó en «Integraciones», porque las pestañas se ensanchan
  cuando llegan los contadores (E-13). Se añadió una marca previa sobre `.gm-sheet__tabs`, anclada a «consola de Seguridad».
- **Filtros de texto**: recargan al escribir (D-S5 corregido).
  - Persona `ana.mejia`: 75 eventos.
  - Acción «Creó»: 54.
  - Registro `quotes`: 3 (Cotización #206–#208).
  - IP 10.9.9.9: 0, con «No se encontraron resultados para los filtros seleccionados».
  - «Limpiar»: vuelve a 671.
- **Voz del filtro Persona**: decía «sus entradas al sistema y las cotizaciones que creó». Arriba de la lista salen precios,
  historial de precios y versiones, y los accesos de Ana quedan abajo. Ahora dice «sus cotizaciones, con sus líneas, precios
  y versiones».
- **Detalle del evento** (`s-03-detalle.png`): «Cambió permisos · Rol #79 · por Rosa Almánzar · Inventario · Productos: Ver,
  Crear, Editar, Importar → …, Exportar», con Origen «**Chrome · Windows**».
  - La voz decía «el de Almacén». Ahora dice «el setenta y nueve, que es Almacén».
  - Del Origen ahora dice «aquí, Chrome en Windows».
- **Celda #12151**: «Creó · Permiso de rol #12151», justo debajo de «Cambió permisos» (y 479 frente a 433), a la misma hora.
- **Historial del registro**: 3 eventos. «Ver a Rosa Almánzar →» lleva a Personas `?q=rosa.almanzar`.

### 08a-vista

- **«salen en gris» era falso** (E-10): los botones deshabilitados de Marta se ven igual que los editables. Ahora la voz dice
  «se ven, pero están bloqueados: si pulsa uno, no cambia nada». El guion pulsa uno y el recurso sigue en 0/4, sin barra de
  guardado.
- **Última marca de 01**: `h4.page-title` estaba pegado arriba y llegaba 1,5 s tarde (R5b). Pasa a
  `table thead th:nth-child(2)`.
- **Contrastes vistos**:
  - Ana: Ventas › Cotizaciones y «1 – 3 de 3».
  - Pedro: sin Ventas; por dirección, toast «No tienes permiso para ver «Cotizaciones»…».
  - Marta: 4 pestañas, sin «Nuevo», rol sin Duplicar/Editar; por dirección, `.console-denied`.

### 08b-crear-editar-anular

- **D-S1 corregido**: la cotización se abre sin modal.
  - La 1.ª línea es «Bombillo LED 9 W», 12 → 15, y el total de la línea se recalcula al teclear (RD$1,681.50).
  - El guardado muestra el diálogo «Éxito · Cotización actualizada exitosamente».
  - Marta ve el 15.
- **El ojo de COT 2 cae sobre el FAB** en la lista de 8 filas de Marta (E-12). La marca pasa al ojo de COT 7 y el paso 04
  entra con `navegar /sales/quotes/2`.
- **«el puntero indica que no está permitido» no se ve en el video**: el cursor es el del motor, no el CSS de la página.
  Ahora la voz dice «sale en gris, apagado; para Ana estaba en azul», que es lo que se ve.
- **«ya no está» (Crear Cotización)**: la marca pasa a `.table-only-header`.

### 08c-exportar-eliminar

- **2 fallos**: `button.panel-collapse` no existe en 04 ni en 06 (panel ya contraído).
- **D-S2 corregido**: sin modal y con fotos.
- **Ana**: ahora tampoco ve «Alta por foto»; solo tiene el lápiz «Abrir».
- **Contrastes**: Rosa tiene la papelera; Pedro, no.

### 08d-alcance (e)

- **D-S4 corregido**: Ana abre COT 4 por dirección y sale «Acceso Denegado · Su rol solo le permite ver y trabajar las
  cotizaciones que usted creó…». Al pulsar «Entendido», vuelve a su lista 1–3 de 3. La voz ahora nombra y pulsa «Entendido»,
  en vez de un `click_opcional` mudo.
- **Recuentos**: Carlos 1–8, Ana 1–3 y, tras cambiar a Equipo, 1–5 (COT 5 y 4 de José).
- **Lámina `alcance-propios-todos`**:
  - fase 2: «Solo los propios 3 de 8» (`seguridad-08e-aprobar-y-estado/lam-alcance-f2.png`);
  - fase 3: «Equipo · Zona Este 5 de 8».
- **Duración**: se recortó la voz para no pasar de 4:10 (queda ≈4:07). Si el login real tarda más de 11 s, el paso se alarga:
  es el guion más justo de la tanda.

### 08e-aprobar-y-estado (e)

- **2 fallos, ensayo más rápido que la toma**: tras `navegar /sales/quotes`, el clic inmediato en el ojo de COT 7 no abrió la
  cotización, y «Más acciones» cayó en el menú de una fila. Se añadió una marca previa sobre la celda Estado de COT 7 («Aquí
  está la número siete, que sigue en Borrador; la abro…»).
- **Verificado**:
  - el clic crudo en el paso «Aprobada» abre la confirmación y después «Éxito · Estado actualizado correctamente»;
  - para Ana, «Aprobada» sale en gris (antes la voz hablaba del puntero);
  - Más acciones de Q6: «Convertir a factura»;
  - Más acciones de Q7: solo «Versiones e historial» y «Duplicar».
- **Lámina `estado-documento`**: fase 1 Borrador/Bloqueado, fase 2 Aprobada/Permitido, fase 3 la frase final
  (`lam-estado-f1..f3.png`).

### 08f-herencia

- **La cifra del contraste quedaba bajo el FAB** (E-12): «Clientes y Proveedores 2/37» y «1/37» caían en x≈1233, y≈641. La
  marca de «Permisos efectivos» pasa a `.sec-people__block:has(.sec-people__module)`. El motor centra el bloque entero y la
  fila sube a y≈560. En 05 se añade la misma marca antes de «volvió a uno».
- **Verificado**:
  - el editor abre Vendedor en «Clientes y Proveedores»;
  - Socios · Crear queda concedido;
  - en Sénior sale tachado en rojo;
  - Carlos pasa de 12/1160 y 2/37 a 11/1160 y 1/37.

### 08g-cambio-en-vivo (c)

- **D-S9 confirmado** con una sonda aparte (`ds9-*.png`). Con la sesión de Ana abierta, tras quitar `PRODUCT_VIEW`:
  - a los +3 s, la navegación sigue mostrando «Inventario» (caché de 30 s);
  - a los +35 s, al volver el foco, el riel lo pierde sin volver a entrar;
  - por dirección, `/home` con toast.
- **Voz**: como hay un solo navegador, Ana sigue volviendo a entrar, pero la voz ya no dice que «el menú se arma al entrar».
  Ahora dice que se habría puesto al día solo, a más tardar en medio minuto. El resumen de 05 va igual.
- **Auditoría (Marta)**: «Cambió permisos · Rol #77 · por Rosa Almánzar · Inventario · Productos: ~~Ver~~ → —», Origen
  «Chrome · Windows». La voz dice ahora «el setenta y siete, que es Vendedor».

### 08h-administrar-la-seguridad (f)

- **10 fallos en cascada** por E-11: el módulo «Acceso API» solo trae «Integraciones Avanzadas». Los permisos de las
  credenciales son Seguridad › «Usuarios de Integración».
  - El paso 04 se reescribió: módulo Seguridad, recurso «Usuarios de Integración» 0/4, «Ver».
  - La voz ya no dice que Acceso API guarda los permisos de las integraciones.
- **Contraste de Marta**, confirmado con una sonda que le dio el mismo permiso por SQL, y E0 restaurado después:
  - consola sin «Nuevo»;
  - ficha de Ana sin Editar, Cambiar contraseña ni «+ Asignar rol», y ⋮ solo con «Ver su actividad»;
  - Zona Este sin «+», sin «Editar equipo» y sin papelera;
  - barra de selección «1 seleccionada · Limpiar»;
  - Integraciones solo con «Documentación de la API»;
  - credencial con «Ver permisos», sin «Rotar secreto» y sin ⋮.
- **E0**: tras cada ensayo quedó restaurado, sin el permiso del Auditor.

## Defectos del ERP anotados (HALLAZGOS-SEGURIDAD-VIDEO.md › Ensayos › Tanda 3)

- **E-10**: el editor en solo lectura no se distingue del editable.
- **E-11**: «Acceso API» no contiene los permisos de las credenciales.
- **E-12**: el FAB tapa la cifra del 2.º módulo en «Permisos efectivos» y el ojo de la 7.ª fila de Cotizaciones.
- **E-13**: las pestañas de la consola se ensanchan al llegar los contadores.

## Herramientas (scratchpad, fuera del repo)

- `ens.mjs`, `sonda.mjs` y `sonda.py`: los de T2.
- `ds9.py` + `quitar_pv.mjs`: prueba de D-S9 con la sesión abierta. Van bajo el cerrojo, y E0 se restauró antes y después.
- `_CONVENCIONES-SEGURIDAD.md`: se añadió la receta del login en cámara («Iniciar sesión», «Entrando…», 5–11 s, panel
  contraído).

## Pendiente para el orquestador

- **08d (≈4:07) y 07 (≈4:05)**: si la voz real sale por debajo de 2,9 palabras/s o el login pasa de 11 s, recortar en 08d-07 la
  frase «y el rol de Ana ahora tiene alcance Equipo en cotizaciones».
- **Grabación**: el login de MySQL local (N-4) es lo que más varía. Si una toma pasa de 12 s, la voz «Ya dentro…» puede caer
  sobre la pantalla de acceso durante 1–2 s.
