# Serie «Seguridad» — plan (consola unificada, master 09-27)

Autor: AUTOR-PLAN · 2026-09-27. Fuentes: `_INVENTARIO-SEGURIDAD-FE.md` (F-###, front `7b4cbf3eb`),
`_INVENTARIO-SEGURIDAD-API.md` (A-###, API `24cbb923f`), skill `germiva-video` (R0–R30).
Cobertura punto por punto: `_COBERTURA-SEGURIDAD.md`. Solo documentos: nada de esto se ha ensayado.

## 1. Criterio

- **Público:** el ADMINISTRADOR de una empresa, no técnico. Cada pantalla se abre diciendo qué es,
  qué representa una fila y para qué sirve (regla de apertura del skill). No se dicen nombres de tabla,
  códigos de permiso, ni «endpoint» (salvo en 06c, y explicado en una línea).
- **Todo el módulo, sin repetir:** cada pantalla, diálogo y aviso de la consola es la tarea principal de UN
  video. En los demás solo se nombra. Los puntos que no se enseñan llevan su motivo en la cobertura.
- **Cada tipo de permiso se enseña CON y SIN sobre el MISMO punto.** Primero entra quien lo tiene
  (insignia verde «Con permiso · …»). Después entra quien no lo tiene (insignia roja «Sin permiso · …»).
  Cada lado va en su propio paso. Los siete tipos del pedido y su video son:

  | Tipo | Punto de la app | Con | Sin | Video |
  |---|---|---|---|---|
  | VISTA | menú Ventas › Cotizaciones + URL directa `/sales/quotes`; pestaña Integraciones + URL | Ana; Marta ve Seguridad | Pedro; Marta sin Integraciones | 08a |
  | ACCIÓN · crear, editar, anular | «Crear Cotización», formulario de una cotización en borrador, paso «Cancelada» | Ana | Marta | 08b |
  | ACCIÓN · exportar, eliminar | «Importar / Exportar» y «Eliminar» en Productos | Pedro (exportar) · Rosa (eliminar) | Ana (exportar) · Pedro (eliminar) | 08c |
  | ACCIÓN · aprobar | paso «Aprobada» del stepper de la cotización | Carlos | Ana | 08e |
  | ALCANCE | el MISMO listado de Cotizaciones | Carlos «Todos» (8) | Ana «Propios» (3) → «Equipo» (5) | 08d |
  | ESTADO | «Más acciones › Convertir a factura» | Carlos, cotización Aprobada | Carlos, cotización en Borrador | 08e |
  | HERENCIA Y EQUIPOS | «Nuevo Cliente» en Clientes, concedido en el rol PADRE | Carlos (lo hereda) | Carlos (excluido en el hijo) | 08f (+05) |
  | CAMBIO EN VIVO | menú Inventario › Productos | Ana antes | Ana después + Auditoría antes/después | 08g |
  | INTEGRACIÓN | la credencial consulta facturas (200) y productos (403) | — | — | 06c |

- **Verdades del sistema (lo contrario NO se dice en voz ni en cartel):**
  1. No hay «filtros por estado del documento» en permisos (A-018). Los filtros del editor —Todos,
     Concedidos, Heredados y Sin conceder— son el estado del PERMISO dentro del rol (F-139). El caso ESTADO
     se enseña con reglas reales de la cotización: el paso «Aprobada» exige `QUOTE_APPROVE` cuando la
     empresa exige aprobación. «Convertir a factura» exige `QUOTE_CONVERT_DIRECTLY_TO_INVOICE` y además que
     la cotización esté Aprobada o Aceptada (F-255, F-256). Frase guía: «el permiso dice qué puedes hacer;
     el estado del documento dice cuándo».
  2. Un **equipo NO da permisos**: solo sirve para el alcance «Equipo» (A-020). La herencia es solo por
     ROL PADRE (A-005). Acceso efectivo = la suma de los roles de la persona en esa empresa más lo que
     heredan (A-022). El sistema comprueba los permisos en cada operación (A-022).
  3. El **alcance** (Propios · Equipo · Todos) solo existe en los permisos de «Ver» y recorta LISTADOS según
     **quién creó el registro**, no según el vendedor asignado (A-016, A-017). Se está corrigiendo que valga
     también al abrir un registro por su número. El video NO afirma nada sobre abrir por número: ni que
     se puede ni que no se puede.
  4. Las credenciales con `x-api-key`/`x-api-secret` solo sirven en los endpoints de integración. Con el
     token de `/api/auth/integration/login`, un endpoint no permitido responde 403 «No tienes el permiso
     requerido…» (A-051, A-052).
- **Pasos de 40–90 s = UNA tarea.** Cada video dura de 2:40 a 4:10. Cuando un tema no cabe, se parte
  (02a/02b, 04a/04b/04c, 06a/06b/06c, 08a…08g).
- **Recursos por guion:** `marca_video` (entrada 3 s y cierre 3 s, con logo), voz
  `es-DO-RamonaNeural +15%`, subtítulos (SRT), un `capitulo` y un `rotulo` por paso, y música
  `marca/musica/elevator-music-mcculloch.mp3` a −32 dB con ducking. Capa de seguridad del motor:
  - `"insignia": {"tipo":"con|sin|info","texto":"…"}` en cada paso con/sin, y en los pasos de concepto con
    `info`.
  - `{"cartel":{"tipo":"consejo|cuidado",…},"durante_ms":N,"al_decir":"…"}`: como máximo un cartel por paso.
    Siempre sobre algo que está en pantalla, para no romper R0.
  - `{"diagrama":"…"}`, `{"diagrama_fase":n}` y `{"diagrama_cerrar":true}`, con una fase por cada idea dicha.
- **Cambiar de usuario dentro del video:** la sesión del guion (`sesion`) solo entra una vez, fuera de cámara
  (`capturar.py:_sesion`). Los cambios de usuario van EN CÁMARA, al principio del paso que lleva la insignia
  de la nueva persona, siempre con la misma receta y en voz: «Ahora salgo y entro como Pedro, el encargado
  de almacén».
  ```
  {"click": "button.topbar-user", "al_decir": "salgo"}
  {"click": ".user-item-list:has-text('Cerrar sesión')", "al_decir": "cierro sesión"}
  {"escribir": {"sel": "input[formcontrolname='username']", "texto": "pedro.nunez"}, "al_decir": "entro como"}
  {"escribir": {"sel": "input[formcontrolname='password']", "texto": "Demo2026!"}, "al_decir": "su clave"}
  {"click": "button.auth-primary-btn", "al_decir": "Entrar"}
  ```
  El cambio cuesta unos 15 s de voz. Hay que dejar 2–3 s de habla entre el tecleo y la palabra siguiente
  (R2). La clave se ve enmascarada. `privacidad.permitidos` lleva todos los usuarios demo. R26: mientras se
  graba, nadie más entra con estos usuarios, y los scripts `dev/login` del sembrado revocan la sesión.
- **R13:** la voz nunca dice la fecha ni el día («hoy», «ayer» solo cuando los lee de la pantalla).

## 2. Empresa demo — DECISIÓN

**Se crea una empresa NUEVA y limpia: «Distribuidora Las Palmas SRL»** (comercial «Distribuidora Las
Palmas»), RNC ficticio **130555036** (tiene el dígito verificador DGII bien calculado, está en el rango demo
`1305550xx` y no lo usa ninguna serie: las usadas son 001, 002, 012, 021, 079 y 206). Dirección: Calle
Duarte 88, Villa Mella, Santo Domingo Norte · 809-555-0188. Moneda DOP y **sin e-CF** (B01/B02).

Motivos de la decisión:
1. Es lo que pidió el usuario («crear una empresa de demo desde cero con datos ficticios»).
2. La 43 «Ferretería El Progreso» es el canon de las series Cajas (S0–S8) y POS (P0). Meterle roles,
   equipos, credenciales, cotizaciones y `quote_requires_approval` rompería sus restauraciones. Además
   arrastra un rol «Cajero POS demo», cajas abiertas y bitácora ajena que ensuciarían Resumen y Auditoría.
3. Con una empresa limpia, cada cifra del Resumen está planeada: personas sin rol, personas que nunca
   entraron, credenciales sin uso y roles vacíos.

**Se reutiliza** el catálogo del sembrado POS: `seeds/pos/catalogo.json` (6 categorías y 25 productos) y las
fotos de `seeds/pos/imagenes/`. El giro «distribuidora de ferretería» casa con esos productos.

Alta y preparación (script nuevo `seeds/seguridad/sembrar.mjs`, idempotente, por API con los payloads del
front y SQL solo donde se indica):
1. `POST /api/auth/dev/register`: empresa + administradora `rosa.almanzar` (A-063). Throttle 1/min.
2. Plan **15 «Empresarial»** por SQL en `subscriptions`, como en `seeds/cajas/plan-s8.mjs`. Trae
   SALES_QUOTE, INVOICING, PRODUCTS y API_ACCESS (A-063).
3. `company_configs.quote_requires_approval = 1` (por el toggle de Preferencias › Facturación o por API).
   Sin esto, «Aprobada» exige `QUOTE_UPDATE` y el caso ESTADO no se puede enseñar (F-256).
4. Catálogo, fotos y existencias (adaptar `seeds/pos/sembrar.mjs` + `imagenes.mjs` al `company_id` nuevo).
   Clientes ficticios: «Constructora Mirador» (RNC 130555044), «Ferretería Doña Luz» (130555052),
   «Inversiones Barahona» (130555087) y «Colmado La Esquina» (130555095). Todos con la regla POS: dígito
   válido y ausentes de `taxpayers`.
5. Roles, usuarios, equipo y credenciales (§3–§5). La secuencia NCF B01/B02 va como en P0.
6. Documentos (§6), creados **con la sesión de quien figura como autor** (`dev/login` de cada uno), porque el
   alcance filtra por `created_by_user_id`.
7. Retroceder por SQL: `users.created_at` de Héctor (hace 45 días, para NEVER_LOGGED_IN) y la credencial
   «Tienda en línea anterior» (creada hace 120 días, `last_api_call` hace 80 días, para STALE).
8. Un guardado en lote real de permisos, como Rosa sobre «Almacén» (concede «Productos · Exportar»), para
   que la bitácora ya traiga un «Cambió permisos» con antes/después (lo usan 01 y 07).
9. `user_company_preferences.incomplete_config_notice_seen_at` para TODOS los usuarios (R18).
10. `fijar.mjs E0` → canon. Restaurador `seeds/seguridad/restaurar.mjs E#` hecho con el patrón de
    `seeds/pos/_estado.mjs`: marca de agua + tablas medidas con `_medir.mjs --comparar`, e incluye
    `audit_logs` de la empresa (ver Preguntas abiertas 1). Las sesiones van con `sql_log_bin=0` (R14).

## 3. Usuarios demo (clave de todos `Demo2026!`, correos `@germiva.demo`, una sola empresa)

| Persona (ficticia) | Usuario | Rol(es) en la empresa | Equipo | Estado | Qué demuestra |
|---|---|---|---|---|---|
| Rosa Almánzar | `rosa.almanzar` | Admin (sistema) | — | Activa | La administradora: graba la consola (00–07, 09) y hace los cambios en vivo. Cuenta como «Administradores 1». Tiene «Productos · Eliminar» (08c, lado CON) |
| Ana Mejía | `ana.mejia` | **Vendedor** | Zona Este | Activa | Vendedora común: alcance «Propios» (3 cotizaciones), no aprueba y no exporta. Es la persona del cambio en vivo (08g) |
| José Cabrera | `jose.cabrera` | **Vendedor** + **Almacén** | Zona Este | Activa | Suma de dos roles en el acceso efectivo (05). Sus cotizaciones aparecen con alcance «Equipo» (08d) |
| Carlos Pimentel | `carlos.pimentel` | **Vendedor sénior** (hijo de Vendedor) | — | Activa | Herencia: aprueba, convierte y ve «Todos» (08d, 08e, 08f) |
| Pedro Núñez | `pedro.nunez` | **Almacén** | — | Activa | No ve Ventas (VISTA, 08a). Exporta pero no elimina productos (08c) |
| Marta Guzmán | `marta.guzman` | **Auditor (solo lectura)** | — | Activa | Ve todo y no cambia nada. Ve Seguridad pero no Integraciones (08a). Revisa la bitácora en 08g |
| Héctor Vargas | `hector.vargas` | Vendedor | — | Activa, **nunca entró** (creado hace 45 días) | Asunto «nunca inició sesión», vista «Nunca entraron» y estado «Pendiente» |
| Luisa Féliz | `luisa.feliz` | **ninguno** | — | Activa (entró 1 vez) | Asunto «persona sin ningún rol», vista «Sin rol» y «Sin ningún rol» en rojo |
| Sonia Reyes | `sonia.reyes` | **Mensajero** (rol vacío) | — | **Inactiva** | Vista «Inactivas» y asunto «rol sin permisos» |

Se crea EN CÁMARA y se borra al restaurar: **Julio Santana** `julio.santana` (Vendedor), en 04b.

## 4. Roles de la empresa

Todos los roles son de la empresa (sin `code`). Los códigos se confirman en la exploración con el editor
real: se ve el tooltip «{estado} · {CODIGO}» (F-145).

| Rol | Padre | Permisos (alcance) | Titulares |
|---|---|---|---|
| **Vendedor** | — | Cotizaciones: Ver (**Propios**), Crear, Editar (`QUOTE_UPDATE`) · Clientes: Ver (Todos) · Productos: Ver (Todos) | Ana, José, Héctor |
| **Vendedor sénior** | **Vendedor** | Hereda todo lo anterior. DIRECTOS: Cotizaciones Ver (**Todos**, porque cambiar el alcance lo vuelve directo, A-008), Aprobar, Rechazar, Aceptar, Convertir a factura · Facturas: Ver, Crear | Carlos |
| **Almacén** | — | Productos: Ver, Crear, Editar, Exportar, Importar · Inventario: Ver. **Sin** Eliminar y sin nada de Ventas | Pedro, José |
| **Auditor (solo lectura)** | — | Ver (Todos) de Cotizaciones, Facturas, Productos y Clientes · Seguridad: `USER_VIEW`, `TEAM_VIEW`, `ROLE_VIEW`, `AUDIT_LOG_READ`. **Sin** `INTEGRATION_USER_VIEW` y sin ningún crear/editar/eliminar | Marta |
| **Mensajero** | — | **ninguno** (rol vacío a propósito) | Sonia |

Roles del sistema visibles en el rail «Del sistema»: Admin, Cajero, Supervisor de Caja, Contador, Compras,
Recursos Humanos y Empleado. Referidor queda oculto (A-003).
Se crean en cámara (y el restaurador los quita): «Cobrador» y «Contador externo» (02a, que parte de E0 y deja
E2a), «Vendedor en práctica» (03, lo borra en el mismo video) y el equipo «Zona Norte» (04c).

## 5. Equipos y credenciales

- **Equipo «Zona Este»**: «Vendedores del este: Villa Mella y Los Alcarrizos». Miembros Ana y José. Sirve al
  alcance «Equipo» de 08d y demuestra que no suma permisos (05).
- **Credencial «Tienda en línea anterior»**: plantilla por defecto. Creada hace 120 días y sin llamadas
  desde hace 80 → estado «Sin uso» y asunto STALE del Resumen. Se revoca en 06b.
- **Credencial «Programa del contador»**: la crea Rosa EN CÁMARA en 06a. Para 06c la trae ya creada el
  estado **E6c** (el sembrado la crea por API y guarda el secreto en `seeds/seguridad/credencial.json`,
  fuera de git y nunca en cámara). Sus permisos son los de la plantilla `INTEGRATOR_DEFAULT` (A-043):
  facturas Ver/Crear y e-CF. **NO** trae `PRODUCT_VIEW`. En 06a se le quita «Registrar compras»
  (`PURCHASE_INVOICE_CREATE`), por mínimo privilegio.

## 6. Documentos sembrados (E0)

`quote_requires_approval = 1`. Las cotizaciones las crea cada autor con su propia sesión. Las aprobaciones
las hace Carlos.

| # | Creada por | Cliente | Estado en E0 | Para qué |
|---|---|---|---|---|
| Q1 | Ana | Constructora Mirador | Borrador | 08e: Carlos la aprueba (CON) |
| Q2 | Ana | Colmado La Esquina | Borrador | 08b: Ana la edita y Marta no · 08e: Ana no puede aprobarla (SIN) |
| Q3 | Ana | Ferretería Doña Luz | Aprobada (por Carlos) | variedad de estados en «Propios» |
| Q4 | José | Inversiones Barahona | Borrador | alcance «Equipo» |
| Q5 | José | Constructora Mirador | Aceptada | alcance «Equipo» |
| Q6 | Carlos | Ferretería Doña Luz | Aprobada | 08e ESTADO: «Convertir a factura» sí aparece |
| Q7 | Carlos | Inversiones Barahona | Borrador | 08e ESTADO: «Convertir a factura» no aparece |
| Q8 | Rosa | Colmado La Esquina | Cancelada | variedad («Todos» = 8) |

Recuentos: Ana «Propios» = **3** · «Equipo» (Ana + José) = **5** · «Todos» = **8**.
Facturas: **F1** B01 emitida por Carlos (Constructora Mirador), **F2** B02 emitida por Rosa (consumidor
final) y **F3** borrador de Carlos. Las lee la credencial en 06c.
Productos: los 25 del catálogo POS, creados por Rosa.

## 7. Estados y restauración (R7)

| Estado | Contenido | Lo usan |
|---|---|---|
| **E0** | §2–§6 | todos salvo 02b y 06c |
| **E2a** | E0 + roles «Cobrador» (vacío) y «Contador externo» (clon de Contador) | 02b |
| **E6c** | E0 + credencial «Programa del contador» con su rol propio (plantilla sin «Registrar compras») | 06c |

Cada toma escribe; tras cada toma y cada ensayo va `restaurar.mjs <estado de partida>`. `fijar.mjs E2a`
y `fijar.mjs E6c` se ejecutan una vez, después de preparar esos estados por script.

---

## 8. Videos

Convenciones de la tabla: **I** = insignia del paso · **C** = cartel · **D** = diagrama. Todas las rutas son
del ERP (`http://localhost:4200`). Cada guion lleva `sesion` = el primer usuario que aparece.
«Contraer panel» = `click_opcional: button.panel-collapse`, que se hace después de presentar la primera
pantalla de módulo (R5). En `/home` no existe.

### 00 — «Seguridad: qué es y cómo se organiza» (≈2:50) · entra `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: nada.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-bienvenida | Para quién es la serie y qué resuelve el módulo: quién entra, qué puede hacer y qué cambió. Presentar la empresa demo. En `/home` se señala el riel del menú | `/home` | 40 s | I info «Módulo de Seguridad» |
| 02-seis-conceptos | Persona, rol, permiso (recurso + acción), alcance, equipo y credencial de API, uno por fase | lámina | 75 s | D `conceptos-seguridad` fases 2–6 · C consejo «Da permisos a roles, nunca persona por persona» |
| 03-la-consola | Menú «Seguridad» (F-001; aparece con cualquier permiso de Seguridad, F-002) → consola `/security/resumen`: título y subtítulo, las cinco pestañas con sus conteos, el buscador «Buscar persona, rol o permiso» (solo se usa para personas, D-11) y el botón «Nuevo» con sus 4 ítems, solo señalado. Contraer panel | `/security/resumen` | 60 s | C cuidado «Cada pestaña exige su permiso: sin él, desaparece» |

**BLOQUEANTE (motor):** los diagramas actuales afirman lo contrario de la verdad 2. La tarjeta 05 de
`conceptos-seguridad` dice «Un grupo de personas que suma permisos a todos sus miembros». Hay que
cambiarla por «Agrupa personas. No da permisos: sirve para el alcance «Equipo».».
En `acceso-efectivo`, la fase 3 suma «Reportes · Ver del equipo». Hay que quitar la capa de equipo o
convertirla en «Equipo Zona Este → no suma permisos» (tachado). También hay que cambiar el subtítulo, «Sus
permisos se suman: los de su rol, los que el rol hereda y los de su equipo», por «…los de sus roles y los que
esos roles heredan».
Además hay que alinear los nombres con esta serie: Ana, Vendedor, Vendedor sénior, Zona Este. En
`alcance-propios-todos` hay que usar «Cotizaciones · Ver» con los autores Ana, José y Carlos (Marta es la
auditora de esta serie). En `estado-documento` hay que usar la cotización: Borrador → Aprobada, con
«Convertir a factura» bloqueado en Borrador y permitido en Aprobada. Sin estos cambios, 00, 05, 08d y 08e
no se graban.

### 01 — «Seguridad: el Resumen» (≈3:10) · `rosa.almanzar`
Estado de partida: E0, restaurado JUSTO antes, porque la actividad reciente se ve en cámara.
Qué escribe en BD: nada (solo los eventos de sesión).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-cifras | Las cinco cifras: Personas con acceso («N activas en 30 días»), Administradores, Sin ningún rol (punto ámbar), Credenciales de API («1 sin uso en 60 días») y Cambios en 7 días. Se dice a dónde lleva cada una y se pulsa «Sin ningún rol» → Personas › Sin rol (Luisa) → vuelta | resumen → personas → resumen | 75 s | — |
| 02-requiere-atencion | Los cuatro asuntos, cada uno con su marca: 1 persona sin ningún rol, 1 credencial sin uso, 1 persona nunca inició sesión y 1 rol sin permisos. Se explica su CTA. Se pulsa «Configurar» del rol vacío → Roles › Mensajero («Vacío») → vuelta. Estado «Nada pendiente» en voz | resumen → roles → resumen | 75 s | C cuidado «Un rol vacío no da acceso a nada: asignarlo no sirve» |
| 03-actividad-reciente | La tabla Cuándo · Quién · Acción · Registro · IP, el formato «Hace N min / Hoy HH:MM» y las etiquetas de acción. Se pulsa la fila «Cambió permisos» (la del sembrado) → Auditoría con el evento abierto (solo se anuncia; se explica en 07). «Ver bitácora →» señalado | resumen → auditoría | 55 s | — |

### 02a — «Seguridad: roles del sistema y roles de tu empresa» (≈3:40) · `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: roles «Contador externo» (clon) y «Cobrador» (vacío) → **E2a**.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-lista-de-roles | Pestaña «Roles y permisos». Qué es un rol. Rail «De la empresa» (Vendedor y, debajo con ↳, Vendedor sénior; insignia «Vacío» en Mensajero; conteo de titulares con tooltip) y «Del sistema» (candado). El buscador «Buscar rol…» se usa con «vend». Contraer panel | `/security/roles` | 60 s | — |
| 02-rol-del-sistema | Abrir «Contador» (sistema): insignia «Del sistema», aviso de solo lectura, acciones en gris; no hay «Editar» ni ⋮. Por qué: los mantiene Germiva y valen para todas las empresas (A-002) | roles | 50 s | C consejo «Para ajustar un rol del sistema, duplícalo» |
| 03-duplicar | «Duplicar» → diálogo «Clonar Rol» (la voz aclara que duplicar y clonar son lo mismo, D-07): aviso de qué se copia, Nombre «Contador externo» (arranca vacío), la descripción ya copiada → «Clonar» → diálogo «Operación completada» → Aceptar → el rol nuevo aparece en «De la empresa» | roles → diálogo → roles | 60 s | — |
| 04-crear-rol | «Nuevo › Rol» → «Crear Rol»: Nombre «Cobrador», Descripción «Cobra facturas a domicilio»; el interruptor «Heredar permisos de otro rol» solo se señala (se usa en 03) → «Crear» → éxito → Aceptar → «Cobrador» con «Vacío». La voz menciona que un nombre repetido da error (A-004) y que salir con cambios pregunta antes (F-168) | roles → diálogo → roles | 55 s | — |

### 02b — «Seguridad: el editor de permisos» (≈3:55) · `rosa.almanzar`
Estado de partida: **E2a**. Qué escribe en BD: permisos del rol «Cobrador».

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-modulos-y-leyenda | Abrir «Vendedor» para leer el editor: rail «Módulos» agrupado por sección (A-012), solo con lo contratado (A-013); barras «n/total»; título «Módulo Ventas» y «n de total permisos»; leyenda Concedido · Alcance. Recurso = qué cosa; acción = qué se hace con ella | roles › Vendedor | 60 s | I info «Permiso = recurso + acción» |
| 02-conceder | Abrir «Cobrador» → módulo de Clientes/Socios → recurso Clientes → pulsar «Ver» (✓ Concedido), pulsar otra vez para ver el ciclo y dejarlo concedido. En Cobros, «Conceder todo». El fondo crema marca lo cambiado. La barra de guardado dice «N cambios sin guardar · afectan a 0 personas» | roles › Cobrador | 60 s | — |
| 03-alcance | En «Clientes · Ver» concedido, el segmentado Propios · Equipo · Todos → «Propios». Qué filtra: los LISTADOS, por quien creó el registro. Solo existe en los permisos de ver | roles › Cobrador | 50 s | C consejo «El alcance recorta lo que se lista según quién lo creó, no el vendedor asignado» |
| 04-buscar-permiso | «Buscar permiso…» con «factur» → «Resultados de «factur»» en todos los módulos, agrupados; se concede «Facturas · Ver» desde ahí. El tope de 60 va en voz | roles › Cobrador | 45 s | — |
| 05-guardar-o-descartar | Pulsar «Contador externo» con cambios pendientes → «Cambios sin guardar» → «Seguir editando» → «Guardar cambios» → toast «Permisos del rol actualizados exitosamente» → filtro «Concedidos» para revisar lo guardado. «Descartar» en voz | roles | 55 s | C cuidado «Nada se aplica hasta pulsar Guardar cambios» |

### 03 — «Seguridad: herencia, titulares e historial de un rol» (≈4:00) · `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: crea «Vendedor en práctica» (hijo de Vendedor), le pone una
exclusión y lo elimina. Queda como E0, más la bitácora.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-rol-hijo | Abrir «Vendedor sénior»: chip «Hereda de Vendedor» (al pulsarlo abre el padre, y se vuelve), la meta «· N heredados de Vendedor», el filtro «Heredados» y la diferencia en pantalla entre heredado (color del padre) y concedido directo (✓). La leyenda «Heredado de…» y «Excluido de la herencia». Lo que se añada al padre llega solo al hijo | roles › Vendedor sénior | 65 s | I info «Hereda de Vendedor» |
| 02-crear-hijo | «Nuevo › Rol» «Vendedor en práctica», con el interruptor «Heredar permisos de otro rol» encendido y Rol padre «Vendedor»; se lee el aviso de sincronización. En voz: no se puede heredar de uno mismo ni hacer un ciclo, porque la lista excluye los descendientes (A-007) → «Crear» → Aceptar | roles → diálogo → roles | 60 s | — |
| 03-excluir | En «Vendedor en práctica», «Cotizaciones · Crear» (heredado) → pulsar → «Excluido de la herencia» → «Guardar cambios» → toast. Qué es una exclusión (A-008). El aviso de «al cambiar el padre se recalcula» (F-165) en voz | roles › Vendedor en práctica | 50 s | C consejo «Excluir quita un heredado solo en este rol; el padre no cambia» |
| 04-titulares-e-historial | Abrir «Vendedor»: el enlace «3 personas tienen este rol» → subvista «Personas» (tabla y clic en Ana → panel, luego vuelta). Subvista «Historial»: la entrada «Cambió permisos» con el antes tachado y el después en verde. Sin permiso de auditoría, «Historial» no aparece | roles › Vendedor | 60 s | — |
| 05-eliminar-rol | «Vendedor en práctica» › ⋮ «Eliminar rol» → confirmación → «Eliminar» → toast «Rol eliminado exitosamente». Un rol del que otros heredan no se puede eliminar (A-009), y en los del sistema no existe el ⋮ | roles → diálogo → roles | 45 s | C cuidado «Un rol padre no se elimina mientras otro herede de él» |

### 04a — «Seguridad: las personas y su ficha» (≈3:20) · `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: nada.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-vistas | Pestaña «Personas». Una fila es alguien que entra a ESTA empresa. Rail «Vistas»: Todas, Activas, Sin rol (Luisa), Nunca entraron (Héctor) e Inactivas (Sonia), con sus conteos. Columnas Persona · Roles · Último ingreso · Estado (Activa, Pendiente e Inactiva, cada una con su marca). El pie «Mostrando 1–9 de 9» | personas | 70 s | — |
| 02-buscar-y-filtrar | Buscar «pimentel» → Carlos. Filtro «Rol» → «Almacén» (Pedro y José). La voz explica el vacío «No se encontraron resultados…». Volver a «Todos los roles» | personas | 45 s | — |
| 03-ficha-de-la-persona | Clic en «Ana Mejía» → panel: estado, equipo «Zona Este» y «Último ingreso». Roles («Vendedor · De la empresa»; el botón lleva al rol). «Permisos efectivos n/total» por módulo y «Ver los N módulos». «Últimos ingresos» con navegador, sistema e IP (salen de la bitácora, A-026). Botones «Editar», «Cambiar contraseña» y ⋮ señalados (se usan en 04b) | personas?usuario= | 75 s | — |
| 04-su-actividad | ⋮ › «Ver su actividad» → Auditoría filtrada por Ana (sus ingresos). Vuelta con el navegador | personas → auditoría | 35 s | — |

### 04b — «Seguridad: dar de alta, editar y desactivar personas» (≈3:50) · `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: el usuario Julio Santana (creado, editado, desactivado y
eliminado).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-crear-usuario | «Nuevo › Usuario» → «Crear Usuario»: Nombre(s) «Julio», Apellido(s) «Santana», Correo (se ve «Verificando correo…»), Usuario «julio.santana», WhatsApp (el hint), Contraseña y confirmación (regla: 6 o más, mayúscula y número), «Roles del Usuario» → Vendedor, Estado Activo → «Guardar» → «Operación completada» → Aceptar. Los avisos de correo ya registrado o eliminado van en voz. No existe «invitar» (F-115) | personas → diálogo → personas | 90 s | C consejo «El rol se elige al crear: sin rol, la persona entra y no ve ningún módulo» |
| 02-editar-y-contrasena | Panel de Julio › «Cambiar contraseña» → «Editar Usuario» con la casilla «Cambiar la contraseña de este usuario» marcada → se escribe la clave nueva → «Actualizar» → éxito | panel → diálogo → panel | 50 s | — |
| 03-asignar-rol | Panel de Julio › «+ Asignar rol» → se añade «Almacén» → guardar → el bloque «Roles» muestra dos. **Depende del arreglo de D-01** (ver Preguntas abiertas). En voz: nadie cambia sus propios roles, no se puede dar un rol con permisos que tú no tienes, y el último administrador no se puede quitar (A-039) | panel → diálogo → panel | 50 s | C cuidado «Nadie puede cambiarse sus propios roles» |
| 04-desactivar-activar | ⋮ › «Desactivar» → confirmación («No podrá iniciar sesión…») → toast → estado «Inactiva» → ⋮ «Activar» → toast | panel | 45 s | — |
| 05-eliminar | ⋮ › «Eliminar» → confirmación («no se puede deshacer») → «Eliminar» → toast → el panel se cierra | panel → personas | 35 s | C consejo «Si puede volver, desactívala en vez de eliminarla» |

### 04c — «Seguridad: equipos» (≈3:20) · `rosa.almanzar`
Estado de partida: E0 («Zona Este» con Ana y José). Qué escribe en BD: el equipo «Zona Norte» (se crea,
recibe miembros, se edita y se elimina).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-que-es-un-equipo | Rail «Equipos»: «Zona Este · 2». Clic → lista filtrada. Un equipo agrupa personas para que un permiso con alcance «Equipo» deje ver lo que crean sus compañeros. **No da permisos** | personas?equipo= | 45 s | C cuidado «Un equipo no da permisos: solo decide qué ven con alcance Equipo» |
| 02-crear-equipo | «+» Nuevo equipo → «Nuevo Equipo»: Nombre «Zona Norte», Descripción «Vendedores de Santiago y Puerto Plata» → «Guardar» → «Operación completada» → Aceptar. En voz: el diálogo no gestiona miembros (F-097) | personas → diálogo → personas | 50 s | — |
| 03-agregar-miembros | Vista «Todas» → marcar Carlos y Héctor → barra «2 seleccionadas» → «Agregar a equipo» › «Zona Norte» → toast «Personas agregadas…» → rail «Zona Norte · 2». «Limpiar» señalado | personas | 55 s | — |
| 04-quitar-editar-eliminar | Abrir «Zona Norte» → marcar Héctor → «Quitar del equipo» (sin confirmación) → toast. «Editar equipo» → cambiar la descripción → «Actualizar» → éxito. Papelera «Eliminar equipo» → confirmación → toast → vuelve a «Todas» | personas?equipo= | 65 s | — |

### 05 — «Seguridad: el acceso efectivo de una persona» (≈3:20) · `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: nada.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-como-se-calcula | Diagrama corregido: rol → lo que hereda de su padre → suma = acceso efectivo. El equipo aparece sin sumar | lámina | 60 s | D `acceso-efectivo` fases 2–4 · I info «Acceso efectivo = roles + herencia» |
| 02-herencia-en-la-persona | Personas › Carlos: «Vendedor sénior · Hereda de Vendedor», y sus permisos efectivos por módulo (Ventas y Facturación más altos que los de Ana) | personas?usuario= | 50 s | I info «Carlos · Vendedor sénior» |
| 03-dos-roles-suman | Personas › José: roles Vendedor + Almacén. Sus permisos efectivos suman los dos (Productos más alto que el de Ana) | personas?usuario= | 50 s | I info «José · dos roles» |
| 04-equipo-no-suma | Ana y José comparten «Zona Este» y su acceso efectivo no cambia por eso. Un cambio de permisos vale desde la siguiente operación (A-022). Lo que no está en el plan contratado no se puede usar aunque esté concedido (A-023). Cierre con Luisa: «Sin ningún rol…» y «Ningún permiso concedido.» | personas?usuario= | 55 s | C consejo «¿Por qué alguien puede o no puede algo? Mira aquí su acceso efectivo» |

### 06a — «Seguridad: credenciales de API para otros programas» (≈3:50) · `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: la credencial «Programa del contador» y su rol propio (sin
«Registrar compras»).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-que-es-una-credencial | Pestaña «Integraciones». Una credencial deja que OTRO programa (la tienda en línea, el sistema del contador) consulte o registre datos sin que entre una persona. La tabla tiene Credencial, Prefijo, Último uso y Estado («Sin uso» en rojo en «Tienda en línea anterior»). Notas al pie | integraciones | 45 s | — |
| 02-crear-credencial | «Nueva credencial» → «Nueva integración»: la nota del secreto; Nombre «Programa del contador», Descripción «Consulta las facturas emitidas para la contabilidad». «Restricciones · Opcional» (IP y endpoint permitidos) se explica y no se llena → «Generar credenciales» | integraciones → diálogo | 65 s | C consejo «Limitar IP y rutas reduce el daño si la clave se filtra» |
| 03-guardar-el-secreto | La franja «Credencial «Programa del contador» lista. Copia el secreto ahora…»: API Key y «Copiar»; el secreto enmascarado con «Mostrar» y «Copiar secreto» → toast «Secreto copiado» → cerrar («Ya lo guardé») | integraciones | 45 s | C cuidado «El secreto se ve una sola vez: si se pierde, hay que rotarlo» |
| 04-panel | Clic en la fila → panel: estado, «N llamadas en total», «Sin restricción de IP», bloque «Permisos» (usa la plantilla) y «Operaciones en 7 días» (cuenta solo lo que crea, modifica o elimina; las consultas no, A-044) | integraciones?credencial= | 45 s | — |
| 05-sus-permisos | «Editar permisos» → página «Permisos de Integración»: tarjeta de datos, buscador y acordeón por módulo. Se desmarca «Registrar compras»: cada casilla guarda al instante, sin botón (F-191). En voz: al primer cambio la credencial recibe permisos propios (A-043) → «Volver a Integraciones» | página de permisos → integraciones | 60 s | C consejo «Da a cada programa solo lo que necesita» |

### 06b — «Seguridad: rotar, pausar y revocar credenciales · documentación de la API» (≈3:10) · `rosa.almanzar`
Estado de partida: **E6c** (ya existe «Programa del contador»). Qué escribe en BD: rota el secreto de
«Programa del contador», la desactiva y la activa, y revoca «Tienda en línea anterior». Se restaura a E6c.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-rotar-secreto | Panel de «Programa del contador» › «Rotar secreto» → confirmación («el actual deja de funcionar de inmediato…») → «Rotar secreto» → reaparece la franja del secreto (F-176) | integraciones | 55 s | C cuidado «Rotar corta la integración hasta que el otro programa use el secreto nuevo» |
| 02-desactivar-activar | ⋮ › «Desactivar» → toast → estado «Inactiva» → ⋮ «Activar» → toast. Sirve para pausar sin perder la configuración | integraciones | 40 s | — |
| 03-revocar | «Tienda en línea anterior» › ⋮ «Revocar y eliminar» → «Revocar credencial» → «Eliminar» → toast. En voz: el asunto «credencial sin uso» del Resumen desaparece | integraciones | 45 s | — |
| 04-documentacion | «Documentación de la API» → barra lateral (Inicio, Autenticación, Facturas emitidas y recibidas, Reportes DGII, Cuenta) y un documento abierto (Login). Es para el técnico que conecta el otro programa | `/security/api-docs/…` | 50 s | — |

### 06c — «Seguridad: caso práctico — lo que una credencial puede y no puede consultar» (≈3:30) · `rosa.almanzar`
Estado de partida: **E6c**. Qué escribe en BD: concede «Productos · Ver» a la credencial (y 1 login de
integración).
**Herramienta de demo declarada en voz:** lámina HTML local `seeds/seguridad/lamina-contador/`
(`http://localhost:4390`, servida con `seeds/_puertas/servir-estatico.mjs` + un proxy Node, para no depender
del CORS del API). Se titula «Programa del contador (prueba)» y tiene dos botones: «Consultar facturas
emitidas» (`GET /api/v1/invoices/sales`) y «Consultar productos» (`GET /api/v1/product`). Ambos usan el
token de `/api/auth/integration/login`, obtenido con la clave y el secreto de `credencial.json`, y muestran
el código (200/403) y el cuerpo legible. La API Key se ve enmascarada (`privacidad.mapa_fijo`). La voz lo
dice así: «esta página hace de programa del contador: pide datos al ERP con la credencial, como lo haría el
programa real».

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-el-programa | Abrir la lámina. Qué es: el otro programa, que se identifica con su clave y su secreto, no con un usuario. Se pulsa «Conectar» → «Conectado» | lámina | 45 s | I info «Credencial · Programa del contador» |
| 02-consulta-permitida | «Consultar facturas emitidas» → **200** y la lista F1 y F2 | lámina | 45 s | I con «Con permiso · Facturas · Ver» |
| 03-consulta-no-permitida | «Consultar productos» → **403** con el mensaje «No tienes el permiso requerido para acceder a este recurso: «Productos»… Solicita acceso a tu administrador.» (A-052) | lámina | 50 s | I sin «Sin permiso · Productos · Ver» · C cuidado «Sin permiso, el ERP responde 403 y no entrega nada» |
| 04-conceder-y-repetir | Al ERP: Integraciones › panel › «Editar permisos» → marcar «Productos · Ver» → volver a la lámina → «Consultar productos» → **200**. Cierre: el cambio vale al instante | ERP → lámina | 70 s | I con «Con permiso · Productos · Ver» |

### 07 — «Seguridad: la auditoría» (≈3:40) · `rosa.almanzar`
Estado de partida: E0 (trae el «Cambió permisos» del sembrado sobre «Almacén»). Qué escribe en BD: nada.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-la-bitacora | Pestaña «Auditoría». Qué es: cada cambio y cada ingreso, con quién, cuándo y desde dónde. Total «N eventos», grupos por día («Hoy · …»), columnas Hora · Quién · Acción · Registro («Rol #id», «Sesión»…) · IP y las insignias de acción | auditoría | 60 s | — |
| 02-filtros | Período → «Últimos 30 días»; Persona «ana»; Acción → marcar «Creó» y «Cambió estado» (el menú no se cierra); Registro «roles»; IP en voz; «Limpiar». Se nombra el vacío «No se encontraron resultados…» | auditoría | 60 s | — |
| 03-detalle-del-evento | Clic en «Cambió permisos» (Rol Almacén) → panel: insignia, fecha y hora, «Rol #id por Rosa Almánzar», «Qué cambió» con «Inventario · Productos: Ver, Crear… → Ver, Crear…, Exportar» (antes tachado, después resaltado) y «Solicitud» (IP, origen, evento) | auditoría?evento= | 60 s | C consejo «Todo cambio de permisos queda aquí con su antes y su después» |
| 04-historial-y-persona | «Historial del registro →» (todo lo que le pasó a ese rol, período «Todo el historial») → «Ver a Rosa Almánzar →» (Personas). «Cargar eventos anteriores» y «El evento no está entre los resultados…» en voz | auditoría → personas | 50 s | — |

### 08a — «Con y sin permiso: VER una pantalla» (≈3:50) · entra `ana.mejia`
Estado de partida: E0. Qué escribe en BD: nada (solo eventos de sesión).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-con-ventas | Ana: el menú «Ventas › Cotizaciones» existe y abre su lista. Qué permiso lo da: Cotizaciones · Ver | `/home` → `/sales/quotes` | 45 s | I con «Con permiso · Ana (Vendedor)» |
| 02-sin-ventas-menu | «Ahora salgo y entro como Pedro, el encargado de almacén» → su menú no tiene «Ventas»: sin el permiso de ver, la opción no existe | login → `/home` | 50 s | I sin «Sin permiso · Pedro (Almacén)» |
| 03-sin-ventas-url | Pedro escribe `/sales/quotes` en la barra → vuelve al inicio sin aviso (F-251). Contraste: `/my-company` → vuelve al inicio CON el toast «No tienes acceso a esa sección…» (F-252) | URL → `/home` | 45 s | I sin «Sin permiso · Pedro (Almacén)» · C consejo «Escribir la dirección no salta el permiso» |
| 04-con-seguridad | «Entro como Marta, la auditora» → menú «Seguridad» visible (F-002), con Resumen, Personas, Roles y Auditoría. Todo en solo lectura: no tiene «Nuevo»; en Roles, «Duplicar» y «Editar» no existen y las acciones del editor salen en gris; en una persona, no hay «Editar» ni «Cambiar contraseña»; en Personas, no hay «+» de equipo (F-227…F-235) | login → `/security/resumen` | 60 s | I con «Con permiso · Marta (Auditor)» |
| 05-sin-integraciones | Marta no tiene la pestaña «Integraciones»; escribe `/security/integraciones` → franja con candado «No tiene permiso para ver «Integraciones». Solicite el acceso…» y debajo su primera pestaña (F-243). En voz: quien no tiene ninguna pestaña ve solo ese aviso (F-245) | URL → consola | 40 s | I sin «Sin permiso · Marta · Integraciones» |

### 08b — «Con y sin permiso: CREAR, EDITAR y ANULAR» (≈3:40) · entra `ana.mejia`
Estado de partida: E0. Qué escribe en BD: la cantidad de una línea de Q2 (se restaura). Q2 NO se cancela:
tiene que seguir en borrador para 04 y para 08e.

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-con-crear | Ana: el botón «Crear Cotización» arriba y «Más acciones › Duplicar» en la fila. Se abre el formulario nuevo y se cancela | `/sales/quotes` | 40 s | I con «Con permiso · Ana · Crear» |
| 02-con-editar-anular | Ana abre Q2 (su borrador): cambia la cantidad de una línea y guarda (CON editar). En el stepper, el paso «Cancelada» está disponible: se señala y NO se pulsa. La voz explica que en cotizaciones anular se llama «Cancelar» y que ella podría hacerlo | `/sales/quotes/:n` | 65 s | I con «Con permiso · Ana · Editar y cancelar» |
| 03-sin-crear | «Entro como Marta» → la MISMA lista, sin «Crear Cotización» ni «Duplicar» (desaparecen, no se ponen en gris, F-253). `/sales/quotes/create` por URL → inicio | login → lista | 55 s | I sin «Sin permiso · Marta · Crear» |
| 04-sin-editar-anular | Marta abre la MISMA Q2 → la ve, pero no puede guardar cambios y el paso «Cancelada» no se puede pulsar | detalle | 45 s | I sin «Sin permiso · Marta · Editar y cancelar» · C consejo «Solo lectura = Ver sin Crear ni Editar» |


### 08c — «Con y sin permiso: EXPORTAR y ELIMINAR» (≈3:40) · entra `pedro.nunez`
Estado de partida: E0. Qué escribe en BD: nada (la exportación descarga un archivo y no se elimina nada).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-con-exportar | Pedro: Inventario › Productos → «Importar / Exportar» → menú → exportar a Excel (la descarga se ve en voz). Contraer panel | `/inventory/product/list` | 50 s | I con «Con permiso · Pedro · Exportar» |
| 02-sin-exportar | «Entro como Ana» → la MISMA lista, sin «Importar / Exportar» y sin «Nuevo Producto» | login → lista | 50 s | I sin «Sin permiso · Ana · Exportar» |
| 03-con-eliminar | «Entro como Rosa» → ⋮ de la fila «Machete de 22"» → «Eliminar» existe (se señala y NO se pulsa) | login → lista | 45 s | I con «Con permiso · Rosa · Eliminar» |
| 04-sin-eliminar | «Entro como Pedro» → mismo ⋮ de la misma fila: tiene Abrir, Duplicar y Desactivar, pero no «Eliminar». Pedro edita, pero no borra | login → lista | 50 s | I sin «Sin permiso · Pedro · Eliminar» · C consejo «Separa crear y eliminar: el que carga datos no tiene por qué borrarlos» |

### 08d — «Con y sin permiso: el ALCANCE (propios, equipo, todos)» (≈3:50) · entra `carlos.pimentel`
Estado de partida: E0. Qué escribe en BD: cambia el alcance de «Cotizaciones · Ver» del rol Vendedor a
Equipo (se restaura).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-que-es-el-alcance | Diagrama: la misma lista de cotizaciones con «Todos» y con «Solo los propios» | lámina | 40 s | D `alcance-propios-todos` (corregido) · I info «Alcance · Cotizaciones · Ver» |
| 02-todos | Carlos (Vendedor sénior, alcance Todos): Cotizaciones → **8**, de Ana, José, Carlos y Rosa (se marca la columna del creador si existe, o el total) | `/sales/quotes` | 45 s | I con «Alcance Todos · Carlos» |
| 03-propios | «Entro como Ana» → la MISMA lista con **3**, solo las que creó ella. Sin rótulo en pantalla: se nota en el total (F-258) | login → lista | 45 s | I sin «Alcance Propios · Ana» · C consejo «Propios = lo que la persona creó, no lo que tiene asignado» |
| 04-equipo | «Entro como Rosa» → Roles › Vendedor › «Cotizaciones · Ver» → «Equipo» → «Guardar cambios». «Entro como Ana» → **5**: las suyas y las de José, su compañero de «Zona Este». Aquí se ve para qué sirve un equipo | login ×2 → roles → lista | 80 s | I info «Alcance Equipo · Ana (Zona Este)» |

### 08e — «Con y sin permiso: APROBAR y el ESTADO del documento» (≈4:05) · entra `carlos.pimentel`
Estado de partida: E0. Qué escribe en BD: Q1 queda Aprobada (se restaura).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-permiso-y-estado | Diagrama: el permiso dice QUÉ acción existe y el estado dice CUÁNDO se puede usar | lámina | 40 s | D `estado-documento` (versión cotización) · I info «Permiso + estado» |
| 02-con-aprobar | Carlos abre Q1 (borrador de Ana) → stepper «Aprobada» → confirmar → estado Aprobada | `/sales/quotes/:n` | 50 s | I con «Con permiso · Carlos · Aprobar» |
| 03-sin-aprobar | «Entro como Ana» → abre Q2 (su borrador): el paso «Aprobada» no se puede pulsar; lo aprueba otra persona | login → detalle | 50 s | I sin «Sin permiso · Ana · Aprobar» |
| 04-con-estado-aprobada | «Entro como Carlos» → Q6 (Aprobada) → «Más acciones» › «Convertir a factura» aparece (se señala; no se convierte) | login → detalle | 50 s | I con «Estado Aprobada · Convertir a factura» |
| 05-sin-estado-borrador | Carlos, con el MISMO permiso, abre Q7 (Borrador) → «Más acciones» sin «Convertir a factura». Tener el permiso no basta. Esto no es un filtro del rol: es la regla del documento | detalle | 45 s | I sin «Estado Borrador · Convertir a factura» · C cuidado «Tener el permiso no basta si el documento no está en el estado correcto» |

### 08f — «Con y sin permiso: HERENCIA (y por qué el equipo no cuenta)» (≈3:50) · entra `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: concede «Clientes · Crear» a Vendedor y excluye ese permiso en
Vendedor sénior (se restaura).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-conceder-en-el-padre | Rosa: Roles › Vendedor → «Clientes · Crear» → Guardar (la barra dice «afectan a 4 personas»: Ana, José y Héctor como titulares, más Carlos por herencia; verificar el número) | roles › Vendedor | 50 s | — |
| 02-llega-al-hijo | Roles › Vendedor sénior → ese permiso aparece «Heredado de Vendedor». Personas › Carlos → sus permisos efectivos de Clientes suben | roles → personas | 45 s | I info «Herencia · Vendedor → Vendedor sénior» |
| 03-con-heredado | «Entro como Carlos» → Clientes: «Nuevo Cliente» existe, aunque nadie se lo dio a su rol directamente | login → clientes | 45 s | I con «Con permiso (heredado) · Carlos» |
| 04-excluir-en-el-hijo | «Entro como Rosa» → Vendedor sénior → «Clientes · Crear» heredado → Excluido → Guardar | login → roles | 45 s | — |
| 05-sin-excluido | «Entro como Carlos» → la MISMA pantalla sin «Nuevo Cliente». Ana (rol padre) lo conserva: solo se dice en voz, porque se vio en 01 | login → clientes | 45 s | I sin «Sin permiso (excluido) · Carlos» · C cuidado «Meter a alguien en un equipo no le da permisos: eso lo hacen sus roles» |

### 08g — «Con y sin permiso: un CAMBIO EN VIVO y su rastro en Auditoría» (≈3:50) · entra `ana.mejia`
Estado de partida: E0. Qué escribe en BD: quita «Productos · Ver» del rol Vendedor (se restaura).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-antes | Ana: Inventario › Productos existe y lista los 25 productos | `/inventory/product/list` | 40 s | I con «Con permiso · Ana · Productos» |
| 02-quitar-y-guardar | «Entro como Rosa» → Roles › Vendedor → Productos › «Ver» → Sin conceder → la barra «1 cambio sin guardar · afectan a N personas» (la voz dice la cifra que salga, P-11) → «Guardar cambios» → toast | login → roles | 60 s | C cuidado «Guardar aplica el cambio a todos los que tienen el rol, desde su siguiente operación» |
| 03-despues | «Entro como Ana» → «Productos» ya no está en su menú; `/inventory/product/list` por URL → inicio | login → `/home` | 50 s | I sin «Sin permiso · Ana · Productos» |
| 04-el-rastro | «Entro como Marta, la auditora» → Auditoría → la fila «Cambió permisos · Rol #… · Rosa Almánzar» → detalle: «Inventario · Productos: Ver → —». Se dice quién, cuándo, desde qué IP, y el antes y el después | login → auditoría | 60 s | I info «Auditoría · Marta» |

### 09 — «Seguridad: dónde quedó lo que se movió» (≈2:40) · `rosa.almanzar`
Estado de partida: E0. Qué escribe en BD: la visibilidad del menú de Rosa (se oculta y luego se
restablece; el guion la deja como estaba).

| id | Tarea | Pantallas | Dur. | Capa |
|---|---|---|---|---|
| 01-contrasena-en-mi-perfil | Arriba a la derecha, menú del usuario → «Mi perfil» → tarjeta «Seguridad»: Contraseña actual, nueva y confirmación, cada una con su ojo, y «Actualizar contraseña» (se llena y NO se pulsa: la voz dice que sale «Contraseña actualizada exitosamente»). Una cuenta con la clave bloqueada ve un aviso en su lugar (F-218) | `/profile` | 55 s | I info «Antes: Seguridad › Configuración» |
| 02-visibilidad-del-menu | Tarjeta «Preferencias» › «Visibilidad del menú» → desplegar → apagar «Compras» → «Guardar Cambios» → «Cambios Guardados» → Aceptar → el menú ya no lo muestra → «Restablecer Todo» → confirmación → «Menús Restablecidos». Hay menús con candado que no se pueden ocultar (Seguridad, F-001) | `/profile` | 70 s | C cuidado «Ocultar un menú NO quita el permiso: es solo tu preferencia de pantalla» |
| 03-enlaces-viejos | Se escribe `/security/settings` en la barra → llega a Mi perfil: los enlaces guardados siguen funcionando (F-008). Tarjeta de marca (no pantalla): «Perfil del Consultorio» se mudó a Configuración › Perfil del Consultorio, pero solo existe en **RegiSalud**; en el ERP no aparece | URL → `/profile` + tarjeta | 35 s | I info «Solo en RegiSalud» |

**Decisión Perfil del Consultorio:** en el ERP la ruta manda a `/home` sin aviso (F-222, F-224). No se
muestra ninguna pantalla ERP inexistente. Va como `tarjeta` del motor con el texto «Perfil del Consultorio
→ RegiSalud › Configuración › Perfil del Consultorio» y la voz lo explica. No se graba RegiSalud en esta
serie.

---

## 9. Resumen de la serie

| # | Video | Graba | Parte de | Duración |
|---|---|---|---|---|
| 00 | Qué es y cómo se organiza | Rosa | E0 | 2:50 |
| 01 | El Resumen | Rosa | E0 | 3:10 |
| 02a | Roles del sistema y de tu empresa | Rosa | E0 → E2a | 3:40 |
| 02b | El editor de permisos | Rosa | E2a | 3:55 |
| 03 | Herencia, titulares e historial | Rosa | E0 | 4:00 |
| 04a | Las personas y su ficha | Rosa | E0 | 3:20 |
| 04b | Alta, edición y desactivación | Rosa | E0 | 3:50 |
| 04c | Equipos | Rosa | E0 | 3:20 |
| 05 | Acceso efectivo | Rosa | E0 | 3:20 |
| 06a | Credenciales de API | Rosa | E0 | 3:50 |
| 06b | Rotar, pausar, revocar · documentación | Rosa | E6c | 3:10 |
| 06c | Caso INTEGRACIÓN (200 / 403) | Rosa + lámina | E6c | 3:30 |
| 07 | La auditoría | Rosa | E0 | 3:40 |
| 08a | Caso VISTA | Ana → Pedro → Marta | E0 | 3:50 |
| 08b | Caso ACCIÓN: crear, editar, anular | Ana → Marta | E0 | 3:40 |
| 08c | Caso ACCIÓN: exportar, eliminar | Pedro → Ana → Rosa → Pedro | E0 | 3:40 |
| 08d | Caso ALCANCE | Carlos → Ana → Rosa → Ana | E0 | 3:50 |
| 08e | Caso ACCIÓN aprobar + ESTADO | Carlos → Ana → Carlos | E0 | 4:05 |
| 08f | Caso HERENCIA y equipos | Rosa → Carlos → Rosa → Carlos | E0 | 3:50 |
| 08g | Caso CAMBIO EN VIVO + Auditoría | Ana → Rosa → Ana → Marta | E0 | 3:50 |
| 09 | Dónde quedó lo que se movió | Rosa | E0 | 2:40 |
| | **21 videos** | | | **≈ 75 min** |

Orden de grabación sugerido: 01 primero, tras restaurar, porque su actividad reciente es la del sembrado.
Luego 00, 02a (+`fijar E2a`), 02b, 03, 04a–c, 05, 07, 06a, 06b y 06c, después 08a–g y al final 09.

## 10. Requisitos previos a guionizar

1. Rama `fix/security-video-findings` MERGEADA en master (los dos repos) y `git pull` + rebuild con la
   tanda parada (regla de videos; R22 y R23f). Después hay que volver a leer los puntos que cambiaron:
   D-01, D-05, D-07, D-08, D-09, D-11, D-12 y el alcance por id.
2. Diagramas corregidos (bloqueante de §8/00).
3. `seeds/seguridad/` completo: sembrar, fijar, restaurar y la lámina con su proxy. Además, R18 marcado
   para los 9 usuarios.
4. Exploración del DOM vivo por usuario (Rosa, Ana, Pedro, Marta, Carlos) y confirmación de los códigos y
   etiquetas reales del editor. Los selectores salen de F-263…F-274.

## 11. Preguntas abiertas (requieren la app o la BD vivas)

1. **Restaurar la bitácora:** ¿`audit_logs` admite `DELETE` por `company_id` y marca de agua? Es append-only,
   está particionada por mes y puede tener un trigger. Sin eso, la «Actividad reciente» de 01 y la
   bitácora de 07 cambian de toma en toma. Si no se puede borrar, 01 y 07 se graban primero y una sola
   vez, o se filtra por período.
2. **El menú tras un cambio de permisos:** el front lee `session.permissionCodes` del login (F-249). ¿Una
   sesión ya abierta oculta la entrada al recargar, o solo al volver a entrar? En la serie siempre se vuelve
   a entrar, y la voz dice «desde su siguiente operación» y «al volver a entrar ya no lo ve». Hay que
   confirmar que ninguna frase prometa más de lo que se ve.
3. **D-01 (asignar rol a una persona existente):** ¿quedó arreglado en `fix/security-video-findings`? Si no,
   04b-03 se sustituye por una voz sobre asignar roles al crear y queda como hallazgo.
4. **El login en cámara:** que el formulario local entre sin reCAPTCHA visible con `button.auth-primary-btn`;
   a qué pantalla lleva (¿`/home`?); que no salgan el modal «Configuración incompleta» (R18) ni el aviso de
   suscripción TRIAL en una empresa nueva con plan 15, y cuánto tarda (para calibrar los 15 s).
5. **El motor y otro origen:** ¿`navegar` acepta una URL absoluta de otro origen (`http://localhost:4390`)
   a mitad del video y luego vuelve al ERP con `navegar` relativo, conservando la sesión? Si no, la lámina se
   sirve bajo el mismo origen del front estático o se graba 06c en dos guiones montados.
6. **El stepper de la cotización para Ana y Marta:** con `quote_requires_approval=1`, ¿el paso «Aprobada» se
   ve deshabilitado o desaparece? ¿«Cancelada» se llama así? ¿Marta ve el formulario de solo lectura, o con
   campos editables y un error al guardar?
7. **«Convertir a factura»:** en Q7 (Borrador), ¿el ítem desaparece o sale deshabilitado? En Q6 (Aprobada),
   ¿Carlos necesita además `INVOICE_CREATE`? (Se le da igual).
8. **Cifras del Resumen:** ¿NEVER_LOGGED_IN toma a Héctor con `created_at` retrocedido 45 días? ¿EMPTY_ROLE
   cuenta a «Mensajero», cuya titular está inactiva? ¿STALE toma a la credencial retrocedida?
9. **Alta de Luisa sin rol:** ¿`POST /api/user` acepta `roles: []`? Si no, se quita el rol por SQL, porque la
   regla de A-039 impide quitar el último rol por la UI.
10. **Alcance tras el cambio:** en 08d-04, ¿Ana ve 5 al volver a entrar? A-066 dice que el alcance sale de la
    caché de roles. Y en 08d-02, ¿la lista de Cotizaciones tiene una columna de creador o de vendedor que se
    pueda marcar sin mentir (el creador no es el vendedor)?
11. **La barra de guardado:** en 08f-01 y 08g-02, ¿«afectan a N personas» cuenta a los titulares por herencia
    (Carlos)? La voz dice el número que salga.
12. **`/my-company` para Pedro (08a-03):** ¿su rol carece de `COMPANY_VIEW` y se ve el toast de F-252?
13. **Etiquetas reales del editor** para Clientes · Crear (¿`PARTNER_CREATE`?), Inventario · Ver y
    Cotizaciones · Aceptar/Convertir. Las mira el guionista con el tooltip.
14. **La exportación de productos (08c-01):** ¿la descarga abre un diálogo nativo que tape la toma? Si es así,
    solo se señala el menú.
