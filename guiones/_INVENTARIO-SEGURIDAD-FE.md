# Inventario FRONT — Consola de Seguridad (Germiva ERP)

- **Fuente:** `germiva-website`, rama `master`, commit `7b4cbf3eb` «feat(security): unified security console redesign (#1237)» (27-09-2026).
- **Método:** SOLO lectura de código. No se arrancó la app, así que todo lo visual es lo que dice la plantilla; lo que depende del API o no se pudo confirmar va marcado **INFERIDO**.
- **Uso:** cada punto `F-nnn` es una línea de cobertura. Hay que completar la columna «Video / minuto» cuando se grabe.
- **Rutas de archivo:** son relativas a `germiva-website/src/app/`. `SEC` = `modules/security/`. `CON` = `modules/security/consola/`.
- **Convención de avisos:** **toast** = `MatSnackBar` (se cierra solo; su botón es «OK» o «Cerrar»). **Diálogo Aceptar** = `CustomAlertDialogComponent`, que es modal con un botón. **Confirmación** = `ConfirmDialogComponent`, con dos botones.

> Nota de nomenclatura: el encargo decía «pestaña Roles», pero la etiqueta REAL de la pestaña es **«Roles y permisos»** (id `roles`). El orden REAL de las pestañas es **Resumen · Personas · Roles y permisos · Integraciones · Auditoría** (`CON/security-console.component.ts:200-228`).

---

## 1. Entrada al módulo y rutas

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-001 | Entrada del menú lateral | Grupo «Seguridad» (clave i18n `MENUITEMS.SECURITY.TEXT` = «Seguridad», icono `lock`). Tiene UNA subentrada, «Seguridad» (icono `shield`), que lleva a `/security/resumen`. El grupo lleva `configurable: false`, así que no se puede ocultar desde «Visibilidad del menú». | `layout/sidebar/sidebar-items.ts:1523-1565` | |
| F-002 | Permiso para ver la entrada del menú | `hasFn(['USER_VIEW','ROLE_VIEW','TEAM_VIEW','PERMISSION_VIEW','AUDIT_VIEW','INTEGRATION_USER_VIEW'])` en OR. Basta con uno, y sin ninguno **la entrada desaparece**. No exige correo verificado ni módulo del plan. | `sidebar-items.ts:1530` y `:1561` | |
| F-003 | Ruta raíz | `/security` → redirige a `/security/resumen` | `SEC/security.routes.ts:44-48` | |
| F-004 | Ruta de la consola | `/security/:tab` → `SecurityConsoleComponent`. Hay cinco ids válidos: `resumen`, `personas`, `roles`, `integraciones` y `auditoria`. Un id desconocido cae en la primera pestaña visible. | `security.routes.ts:117-120`; `shared/components/console-shell/console-shell.component.ts:285-295` | |
| F-005 | Rutas heredadas (redirigen) | `/security/user` y `user/:id` → `personas`. `team` y `team/:id` → `personas?vista=equipos`. `role` y `role/:id` → `roles` (**se pierde el id**). `permission` → `roles`. `audit` → `auditoria`. `integration-user` → `integraciones`. `integration-user/docs[/:slug]` → `api-docs[/:slug]`. | `security.routes.ts:52-65, 89-92` | |
| F-006 | Alias de pestaña en la URL | `user`, `users`, `team`, `teams` → personas. `role`, `permission`, `permissions` → roles. `audit` → auditoria. `integration-user` → integraciones. | `CON/security-console.component.ts:234-245` | |
| F-007 | Historial de un registro (ruta vieja) | `/security/audit/entity-name/:name/entity-id/:id` → `/security/auditoria?registro=:name&registroId=:id&periodo=todo` | `security.routes.ts:20-27, 93-97` | |
| F-008 | Rutas que salieron del módulo | `/security/settings` → `/profile`. `/security/menu-visibility` → `/profile`. `/security/medical-profile` → `/my-company/perfil-consultorio`. Detalle en §8. | `security.routes.ts:66-82` | |
| F-009 | Rutas con página propia | `/security/integration-user/:id/permissions` (permisos de una credencial) y `/security/api-docs/:slug` (documentación). También quedan redirecciones globales: `/api-docs[/:slug]` → `/security/api-docs[/:slug]`. | `security.routes.ts:98-114`; `app.routes.ts:84-95` | |
| F-010 | Sin guard de ruta | La ruta `security` de `app.routes.ts` NO tiene `canActivate` de permiso ni de módulo. Solo pasa por los guards del tronco autenticado (correo verificado y `data.permissions`, que aquí no se declara). El control es **dentro de la consola**, por pestaña (F-014). | `app.routes.ts:281-285` | |

## 2. La consola (cáscara común a las cinco pestañas)

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-011 | Hoja única | La cabecera, las pestañas y el contenido van en una sola superficie (`.gm-sheet`, `[sheet]="true"`). Título `h1` «Seguridad» y subtítulo «Quién entra, qué puede hacer y qué cambió.» El breadcrumb solo muestra «Seguridad» › pestaña activa. | `CON/security-console.component.ts:84-92, 247`; `console-shell.component.ts:79-118` | |
| F-012 | Barra de pestañas | `nav[mat-tab-nav-bar]` con `a[mat-tab-link]`. Solo aparece si hay más de una pestaña visible. Selector: `.gm-sheet__tabs a[mat-tab-link]` con el texto de la pestaña. | `shared/components/console-tabs/console-tabs.component.ts:50-66` | |
| F-013 | Conteos en las pestañas | Personas = `peopleWithAccess`. Roles y permisos = `roles`. Integraciones = `apiCredentials`. Salen de `GET /v1/security/overview`, que **solo se pide con USER_VIEW**. Sin ese permiso las pestañas salen sin número. Un conteo de 0 no se muestra (`@if (tab.count)`). | `security-console.component.ts:200-228, 249-253`; `console-tabs.component.ts:60` | |
| F-014 | Permiso de cada pestaña | Resumen = `USER_VIEW`. Personas = `USER_VIEW` **o** `TEAM_VIEW`. Roles y permisos = `ROLE_VIEW`. Integraciones = `INTEGRATION_USER_VIEW`. Auditoría = `AUDIT_LOG_READ`. Sin el permiso la pestaña **desaparece** de la barra. | `security-console.component.ts:200-228`; `console-shell.component.ts:272-276` | |
| F-015 | Aviso de pestaña denegada por URL | Si la URL pide una pestaña que existe pero no está concedida, se ve un aviso con candado: «No tiene permiso para ver «{Etiqueta}». Solicite el acceso al administrador de la empresa.» Debajo se muestra la PRIMERA pestaña visible. No es toast: es una franja fija dentro de la hoja. Selector: `.console-denied`. | `console-shell.component.ts:105-113, 302-308` | |
| F-016 | Buscador global de la cabecera | `mat-form-field` con icono `search` y placeholder «Buscar persona, rol o permiso». Con Enter lleva a `/security/roles?q=…` si la pestaña activa es Roles, o a `/security/personas?q=…` en cualquier otro caso. Selector: `.security-console__search input`. | `security-console.component.ts:97-109, 264-271` | |
| F-017 | Botón «Nuevo» (menú) | `mat-flat-button` con el icono `add` y el texto «Nuevo». Solo existe si hay al menos uno de `USER_CREATE`, `ROLE_CREATE`, `TEAM_CREATE` o `INTEGRATION_USER_CREATE`; si no, **desaparece**. | `security-console.component.ts:111-143, 184-194` | |
| F-018 | Nuevo › Usuario | Ítem «Usuario» (icono `person_add`), con `USER_CREATE`. Navega a `/security/personas?nuevo=1` y abre el diálogo de alta de usuario (F-078). | `security-console.component.ts:118-123`; `CON/personas/security-people.component.ts:251-256` | |
| F-019 | Nuevo › Rol | Ítem «Rol» (icono `admin_panel_settings`), con `ROLE_CREATE`. Navega a `/security/roles?nuevo=1` y abre el diálogo «Crear Rol» (F-148). | `security-console.component.ts:124-129`; `CON/roles/security-roles.component.ts:485-494` | |
| F-020 | Nuevo › Equipo | Ítem «Equipo» (icono `groups`), con `TEAM_CREATE`. Navega a `/security/personas?nuevo=equipo` y abre el diálogo «Nuevo Equipo» (F-092). | `security-console.component.ts:130-135` | |
| F-021 | Nuevo › Integración de API | Ítem «Integración de API» (icono `api`), con `INTEGRATION_USER_CREATE`. Navega a `/security/integraciones?nuevo=1` y abre el diálogo «Nueva integración» (F-170). | `security-console.component.ts:136-141`; `CON/integraciones/security-integrations.component.ts:114-117` | |
| F-022 | Estado compartido | `SecurityConsoleStore`: una sola petición `/v1/security/overview` alimenta el Resumen, los conteos de las pestañas y los de las vistas de Personas. Las acciones que cambian algo llaman a `refresh()`. | `CON/security-console.store.ts:1-48` | |
| F-023 | Etiquetas de acción (compartidas) | Creó (verde) · Actualizó (azul) · Eliminó (rojo) · Cambió estado (ámbar) · Acceso · Consultó · Acción · Exportó (acento) · Imprimió. En Roles y Auditoría, un evento `PERMISSIONS_CHANGED` se muestra como «Cambió permisos». | `CON/security-console.shared.ts:11-21`; `CON/auditoria/security-audit.component.ts:277-279` | |
| F-024 | Formato de tiempo relativo | «Hace un momento» · «Hace N min» · «Hace N h» · «Hoy HH:MM» · «Ayer HH:MM» · «vie 12 sep, 09:03» (el año solo si no es el actual). Todo en hora de RD. | `security-console.shared.ts:38-54` | |
| F-025 | Origen legible del user-agent | Muestra «Edge / Opera / Chrome / Firefox / Safari / Cliente de API / Navegador · Windows / Android / iOS / macOS / Linux». Sin user-agent: «Origen desconocido». | `security-console.shared.ts:93-111` | |

## 3. Pestaña RESUMEN — `/security/resumen`

Es el componente `app-security-overview` (`CON/resumen/security-overview.component.ts`). Permiso: `USER_VIEW`, el mismo que exige el API (`@RequirePermissions(USER_VIEW)` en el controlador del overview).

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-026 | Estado de carga | Dos esqueletos: una línea de 64 px y una tarjeta de 320 px (`.sec-ov__loading`, `aria-busy="true"`). | `security-overview.component.ts:55-59` | |
| F-027 | Estado de error | Icono `error_outline`, el texto «Error al cargar los datos. Intenta nuevamente.» y el botón «Reintentar» (icono `refresh`). | `:60-68` | |
| F-028 | Cifra «Personas con acceso» | Muestra el valor `peopleWithAccess` y el subtexto «N activas en 30 días» (o «1 activa en 30 días»). Al pulsarla va a `/security/personas?vista=todas`. Selector: `.gm-sheet-fig` con el texto «Personas con acceso». | `:71-75, 330-336` | |
| F-029 | Cifra «Administradores» | Muestra el valor `admins` y el subtexto «Acceso total a la empresa». Al pulsarla va a `/security/roles`. | `:76-80` | |
| F-030 | Cifra «Sin ningún rol» | Muestra el valor `withoutRole` y el subtexto «Entran y no ven ningún módulo». Si es mayor que 0 lleva un punto ámbar y la clase `gm-sheet-fig--warn`. Al pulsarla va a `personas?vista=sin-rol`. | `:81-94` | |
| F-031 | Cifra «Credenciales de API» | Muestra el valor `apiCredentials`. El subtexto dice «Ninguna emitida», «Todas en uso» o «N sin uso en 60 días». Al pulsarla va a `integraciones`. | `:95-99, 338-344` | |
| F-032 | Cifra «Cambios en 7 días» | Muestra el valor `changesLast7Days` y el subtexto «N de seguridad» (`securityChangesLast7Days`). Al pulsarla va a `auditoria`. | `:100-104` | |
| F-033 | Bloque «Requiere atención» | Título `h2#sec-ov-attention` y contador «N asunto(s)». Cada asunto es un `button.sec-ov__issue` con un punto de color, el título, `meta`, `detail` (nombres) y un CTA con «→». | `:108-128` | |
| F-034 | Asunto USERS_WITHOUT_ROLE | Título del API: «1 persona sin ningún rol» / «N personas sin ningún rol». Meta: «Inician sesión pero no ven ningún módulo.» CTA «Asignar rol», que va a `personas?vista=sin-rol`. Tono ámbar. | Front `:18-22`; API `admin/security-overview/security-overview.service.ts:216-226` | |
| F-035 | Asunto STALE_API_CREDENTIAL | «1 credencial de API sin uso» / «N credenciales de API sin uso». Meta: «Sin llamadas en 60 días. Revócala si ya no se usa.» CTA «Revisar», que va a `integraciones?credencial={id}`. Tono rojo. | Front `:23-27`; API `:236-251` | |
| F-036 | Asunto NEVER_LOGGED_IN | «1 persona nunca inició sesión» / «N personas nunca iniciaron sesión» (solo personas activas creadas hace más de 30 días). Meta: «Reenvía la invitación o desactiva la cuenta.» CTA «Ver», que va a `personas?vista=nunca`. Tono neutro. | Front `:28-32`; API `:255-282` | |
| F-037 | Asunto EMPTY_ROLE | «1 rol sin permisos» / «N roles sin permisos». Meta: «Asignarlos no da acceso a nada.» CTA «Configurar», que va a `roles?rol={id}`. Tono neutro. | Front `:33-37`; API `:284-300` | |
| F-038 | Atención vacía | Icono `check_circle` en verde y el texto «Nada pendiente: todos tienen rol y las credenciales están en uso.» | `:129-134` | |
| F-039 | Bloque «Actividad reciente» | Título `h2#sec-ov-activity`, la meta «Actualizado hace …» y el enlace «Ver bitácora →», que va a `auditoria`. La tabla tiene las columnas Cuándo · Quién · Acción · Registro · IP. El API trae hasta 10 filas. | `:137-163`; API `RECENT_ACTIVITY_LIMIT = 10` | |
| F-040 | Fila de actividad | Al pulsarla va a `/security/auditoria?evento={id}` y abre ese evento. En 767 px o menos se ocultan las columnas Registro e IP. | `:153-163, 313-322, 378-380` | |
| F-041 | Actividad vacía | Icono `inbox` y el texto «No se encontraron registros». | `:164-169` | |

## 4. Pestaña PERSONAS — `/security/personas`

Es el componente `app-security-people` (`CON/personas/security-people.component.{html,ts}`). Permiso de la pestaña: `USER_VIEW` o `TEAM_VIEW`. Query params: `vista`, `equipo`, `rol`, `q`, `usuario` y `nuevo`.

### 4.1 Rail de vistas y equipos

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-042 | Rótulo «Vistas» | `aside.gm-sheet-rail` con `aria-label="Vistas de personas"` | `html:3-4` | |
| F-043 | Vista «Todas» | URL sin `vista`. El conteo es `peopleWithAccess`. | `ts:42-48, 172-187` | |
| F-044 | Vista «Activas» | `?vista=activas` (filtro `active=true`). El conteo es `activePeople`. | idem | |
| F-045 | Vista «Sin rol» | `?vista=sin-rol` (filtro `withoutRole=true`). Si el conteo es mayor que 0 lleva un punto ámbar. | `html:11-13` | |
| F-046 | Vista «Nunca entraron» | `?vista=nunca` (filtro `neverLoggedIn=true`). El conteo es `neverLoggedIn`. | `ts:46` | |
| F-047 | Vista «Inactivas» | `?vista=inactivas` (filtro `active=false`). El conteo es `inactivePeople`. | `ts:47` | |
| F-048 | Conteos del rail | Salen del overview (F-022). Sin `USER_VIEW` quedan vacíos. | `ts:172-187` | |
| F-049 | Rótulo «Equipos» | Solo aparece si hay equipos o si hay `TEAM_CREATE`. | `html:19-27` | |
| F-050 | Botón «+» Nuevo equipo | `mat-icon-button` con `aria-label="Nuevo equipo"` y tooltip «Nuevo equipo». Exige `TEAM_CREATE`; sin él **desaparece**. Abre el diálogo de F-092. | `html:22-26` | |
| F-051 | Lista de equipos | Cada equipo es un botón con el nombre y el número de miembros. Al pulsarlo va a `?equipo={id}`. Los equipos solo se cargan con `TEAM_VIEW`. Máximo 100. | `html:28-32`; `ts:295-300` | |
| F-052 | Sin equipos | El texto «Sin equipos todavía.» | `html:33-35` | |

### 4.2 Lista de personas

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-053 | Título de la lista | Es el nombre de la vista (o del equipo) seguido de «· {total}». | `html:42-44`; `ts:127-131` | |
| F-054 | Buscador | Campo con placeholder «Nombre, usuario o correo» y `aria-label="Buscar persona"`. Espera 300 ms y busca por el parámetro `username`. También se rellena con `?q=`. | `html:45-53`; `ts:158-162, 229` | |
| F-055 | Filtro «Rol» | `mat-stroked-button` con el icono `filter_list`. Su texto es el nombre del rol elegido, o «Rol» si no hay ninguno. El menú ofrece «Todos los roles» y luego cada rol (hasta 200). Pone `?rol={id}`. | `html:54-63`; `ts:199-201` | |
| F-056 | Botón «Editar equipo» | Solo aparece con un equipo abierto y `TEAM_EDIT` (icono `edit`). Abre el diálogo de F-093. | `html:64-70` | |
| F-057 | Botón eliminar equipo | Icono `delete`, `aria-label` y tooltip «Eliminar equipo». Solo aparece con un equipo abierto y `TEAM_DELETE`. | `html:71-75` | |
| F-058 | Confirmación de eliminar equipo | Título «Eliminar equipo». Mensaje: «¿Está seguro de que desea eliminar el equipo "{nombre}"? Esta acción no se puede deshacer.» Botones «Cancelar» y «Eliminar» (rojo). | `ts:434-451, 528-536` | |
| F-059 | Éxito / error al eliminar equipo | Toast «Equipo eliminado exitosamente» [OK, 2,5 s]; después vuelve a «Todas». Error: toast «Error al eliminar el equipo» (o el mensaje del API) [Cerrar, 5 s]. | `ts:444-448, 538-540` | |
| F-060 | Columnas | Una casilla, Persona (avatar con iniciales, nombre, correo · equipos), Roles (separados por coma, o «Sin ningún rol» en rojo), Último ingreso («Nunca» si no ha entrado) y Estado. | `html:107-161` | |
| F-061 | Estado de la persona | «Eliminada» (rojo), «Inactiva» (neutro), «Pendiente» (ámbar: activa pero sin ningún ingreso) o «Activa» (verde). | `ts:357-362` | |
| F-062 | Casilla «Seleccionar todas» | `input[type=checkbox].sec-people__check` con `aria-label="Seleccionar todas"`. Marca solo la página actual. | `html:108-113` | |
| F-063 | Casilla por fila | `aria-label="Seleccionar {nombre}"` | `html:141-146` | |
| F-064 | Carga | Seis esqueletos de 36 px. | `html:120-125` | |
| F-065 | Error | «Error al cargar los datos. Intenta nuevamente.» y el botón «Reintentar». | `html:126-134` | |
| F-066 | Vacío | Sin filtros: icono `inbox` y «No se encontraron registros». Con búsqueda o rol: icono `search_off` y «No se encontraron resultados para los filtros seleccionados». | `html:162-169` | |
| F-067 | Paginación | «Mostrando {a}–{b} de {total}» y los botones «Página anterior» / «Página siguiente» (`aria-label`). Muestra 20 por página. | `html:173-182`; `ts:50, 133-141` | |

### 4.3 Acciones masivas

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-068 | Barra de selección | `.sec-people__bulk` con `role="status"`. Dice «**N** seleccionada(s)». | `html:79-81` | |
| F-069 | «Agregar a equipo» | Botón con el icono `group_add` y un menú con los equipos. Exige `TEAM_MANAGE_MEMBERS` y que exista al menos un equipo; si no, **desaparece**. | `html:82-91` | |
| F-070 | Éxito / error al agregar | Toast «Persona agregada a «{equipo}» exitosamente» o «Personas agregadas a «{equipo}» exitosamente» [OK]. Error: «Error al agregar al equipo» [Cerrar]. | `ts:399-409` | |
| F-071 | «Quitar del equipo» | Icono `group_remove`. Solo aparece con un equipo abierto y `TEAM_MANAGE_MEMBERS`. No pide confirmación. | `html:92-97`; `ts:411-423` | |
| F-072 | Éxito / error al quitar | Toast «Persona quitada de «{equipo}» exitosamente» o «Personas quitadas de «{equipo}» exitosamente». Error: «Error al quitar del equipo». | `ts:417-421` | |
| F-073 | «Limpiar» | Un `mat-button` con el icono `close` que borra la selección. | `html:99-102` | |

### 4.4 Panel de la persona (`?usuario={id}`)

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-074 | Abrir el panel | Se pulsa el nombre (`button.sec-people__who`) y la URL queda en `?usuario={id}`. El panel `aside` lleva `aria-label="Detalle de la persona"`. También se abre por enlace directo, aunque la persona no esté en la página actual. | `html:147, 186-187`; `ts:213-215, 302-319` | |
| F-075 | Cabecera del panel | Avatar grande, nombre, correo y el botón cerrar (`aria-label="Cerrar panel"`, tooltip «Cerrar»). Debajo: estado, equipos y «Último ingreso: {hace …/nunca}». | `html:189-206` | |
| F-076 | Botón «Editar» | `mat-flat-button` con el icono `edit`. Exige `USER_EDIT`. Abre el diálogo «Editar Usuario» (F-085). | `html:209-213` | |
| F-077 | Botón «Cambiar contraseña» | `mat-stroked-button` con el icono `key`. Exige `USER_EDIT`. Abre «Editar Usuario» con la casilla «Cambiar la contraseña de este usuario» ya marcada. | `html:214-217`; `SEC/user/components/user-form/user-form.component.ts:151-153` | |
| F-078 | Menú «Más acciones» | `mat-icon-button more_vert` con `aria-label` y tooltip «Más acciones». Solo existe si hay `USER_EDIT` o `USER_DELETE`. | `html:207, 219-241` | |
| F-079 | Más acciones › Desactivar / Activar | Con `USER_EDIT`. Icono `person_off` o `person`. Desactivar pide confirmación: título «Desactivar usuario». Mensaje: «¿Desactivar a "{nombre}"? No podrá iniciar sesión hasta que se active de nuevo.» Botón «Desactivar». Activar no pide confirmación. | `html:223-228`; `ts:466-486` | |
| F-080 | Éxito / error de activar | Toast «Usuario desactivado exitosamente» o «Usuario activado exitosamente» [OK]. Error: «Error al actualizar el usuario». | `ts:471-474` | |
| F-081 | Más acciones › Ver su actividad | Con `AUDIT_LOG_READ`. Icono `history`. Va a `/security/auditoria?persona={username}`. | `html:229-234`; `ts:509-511` | |
| F-082 | Más acciones › Eliminar | Con `USER_DELETE`. Icono `delete`, en rojo. Confirmación: título «Eliminar usuario». Mensaje: «¿Está seguro de que desea eliminar el usuario "{nombre}"? Esta acción no se puede deshacer.» Botón «Eliminar». | `html:235-240`; `ts:488-503` | |
| F-083 | Éxito / error al eliminar | Toast «Usuario eliminado exitosamente» [OK]; el panel se cierra. Error: «Error al eliminar el usuario» [Cerrar]. | `ts:496-500` | |
| F-084 | Bloque «Roles» | Lista los roles como botones (`button.sec-people__role`) que llevan a `/security/roles?rol={id}`. El subtexto de cada uno es «Administrador», «Hereda de {padre}», «Del sistema» o «De la empresa». Sin roles: «Sin ningún rol: inicia sesión pero no ve ningún módulo.» | `html:250-261`; `ts:505-507` | |
| F-085 | Enlace «+ Asignar rol» | Exige `USER_EDIT` y abre el diálogo «Editar Usuario». **OJO: ese diálogo en edición NO trae selector de roles.** Ver el defecto D-01. | `html:262-264` | |
| F-086 | Bloque «Permisos efectivos» | Muestra «{granted} / {available}» y la ayuda «La unión de sus roles, por módulo contratado.» Cada módulo lleva una barra `gm-coverage` y «n/total». Enseña hasta 8 módulos con algo concedido. | `html:267-283`; `ts:52, 147-154` | |
| F-087 | «Ver los N módulos» | Enlace que despliega todos los módulos, también los que están en 0. Sin permisos: «Ningún permiso concedido.» | `html:281-288` | |
| F-088 | Bloque «Últimos ingresos» | Cada línea dice «{cuándo} · {navegador · sistema}» y la IP. Si no hay: «Sin ingresos registrados en esta empresa.» Los datos vienen de `GET /v1/security/users/:id/access`. | `html:291-301`; `CON/resumen/security-overview.service.ts:17` | |
| F-089 | Carga del panel | Dos esqueletos de línea. | `html:247-248` | |
| F-090 | Persona no encontrada | Icono `person_search` y «Esta persona no está en la lista actual.», con el botón «Cerrar». | `html:304-310` | |
| F-091 | Error al abrir para editar | Toast «Error al cargar los datos» [Cerrar]. | `ts:459-464` | |

### 4.5 Diálogo de equipo (crear / editar)

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-092 | «Nuevo Equipo» | Lo arman `app-form-dialog-layout`, `entityLabel="Equipo"` y `gender="m"`. Campos: «Nombre» (`formcontrolname="name"`, obligatorio, 255 como máximo) y «Descripción» (`textarea formcontrolname="description"`, 500 como máximo). Botones «Cancelar» y «Guardar». | `SEC/team/components/team-form/team-form.component.ts:27-72, 89-93`; `shared/components/form-layout/form-dialog-layout.component.ts:329-338` | |
| F-093 | «Editar Equipo» | El mismo diálogo, con el botón «Actualizar». | idem | |
| F-094 | Éxito del equipo | Diálogo Aceptar de tipo success: título «Operación completada». Mensaje «El equipo ha sido creado correctamente.» o «El equipo ha sido actualizado correctamente.», botón «Aceptar». | `team-form.component.ts:147-162` | |
| F-095 | Error del equipo | Diálogo Aceptar de tipo error, título «Error», con el mensaje del API y el botón «Entendido». | `:164-176` | |
| F-096 | Salir con cambios (equipo) | Diálogo de aviso con el título «Guardar Cambios». Mensaje: «¿Estás seguro que deseas salir sin guardar los cambios?» Botones «Sí, salir» y «Cancelar». | `:111-134` | |
| F-097 | Miembros | El diálogo NO gestiona miembros. Se agregan o quitan desde la lista con la acción masiva (F-069 y F-071). | — | |

### 4.6 Diálogo de usuario (crear / editar)

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-098 | Título | «Crear Usuario» o «Editar Usuario». En alta el botón dice «Guardar»; en edición, «Actualizar». Ancho 640 px, `disableClose`. | `SEC/user/components/user-form/user-form.component.html:1-9` | |
| F-099 | Nombre(s) | `formcontrolname="name"`, obligatorio, placeholder «Ej: Juan Carlos». | `html:14-23` | |
| F-100 | Apellido(s) | `formcontrolname="lastName"`, obligatorio, placeholder «Ej: Pérez García». | `html:24-33` | |
| F-101 | Correo Electrónico | `formcontrolname="email"`, obligatorio y con formato de correo. En alta verifica el correo tras 500 ms y muestra el hint «Verificando correo...». | `html:37-54`; `ts:166-196` | |
| F-102 | Aviso de correo existente | Franja azul: «Este correo ya está registrado. Se vinculará el usuario existente a esta empresa sin modificar su contraseña.» En ese caso se ocultan las contraseñas. | `html:81-86` | |
| F-103 | Aviso de correo eliminado | Franja ámbar: «Este correo pertenece a un usuario eliminado. Se restaurará con los datos proporcionados.» | `html:87-92` | |
| F-104 | Nombre de Usuario | `formcontrolname="username"`, obligatorio, placeholder «Ej: jperez». | `html:55-64` | |
| F-105 | WhatsApp | `formcontrolname="whatsappPhone"`. Hint: «Con código de país. Habilita a esta persona a consultar la empresa por WhatsApp.» | `html:67-78` | |
| F-106 | Contraseña (alta) | «Contraseña» (`formcontrolname="password"`) con el hint «Mínimo 6 caracteres, mayúscula y número», y «Confirmar Contraseña» (`confirmPassword`). El ojo alterna `visibility` / `visibility_off`. | `html:107-139` | |
| F-107 | Cambiar contraseña (edición) | Casilla «Cambiar la contraseña de este usuario». Si la cuenta tiene la clave bloqueada, solo la ve un admin de la empresa principal. | `html:94-105`; `ts:112-120` | |
| F-108 | Bloqueo de contraseña | Casilla «Bloquear el cambio de contraseña de esta cuenta» (`formcontrolname="passwordChangeLocked"`). Solo sale en edición y solo para la empresa principal. | `html:143-156` | |
| F-109 | Roles (solo en alta) | `app-role-multi-select`: `label="Roles del Usuario"`, `hint="Seleccione los roles que tendrá en esta empresa"`. **En edición no aparece** (`@if (!isEditMode)`), y el TS borra `roles` del envío (`ts:317-319`). | `html:158-179` | |
| F-110 | Aviso de médicos (solo en clínica) | Según el rol: «Elija los roles para saber a qué médicos verá esta persona.» / «Con estos roles verá la agenda de TODOS los médicos activos del centro.» / «Como personal médico verá su propia agenda y sus propios pacientes.» / «Verá solo a los médicos de los que sea asistente. Se asigna en la ficha del médico, pestaña «Asistentes».» | `ts:256-276` | |
| F-111 | Estado | «Estado:» con los radios «Activo» e «Inactivo» (`formcontrolname="active"`). | `html:181-191` | |
| F-112 | Éxito del usuario | Diálogo Aceptar success, título «Operación completada». Mensaje «El usuario ha sido creado correctamente.» o «El usuario ha sido actualizado correctamente.» | `ts:326-339` | |
| F-113 | Error del usuario | Diálogo Aceptar error, título «Error», con el mensaje del API y el botón «Entendido». | `ts:341-356` | |
| F-114 | Salir con cambios (usuario) | «Guardar Cambios» / «¿Estás seguro que deseas salir sin guardar los cambios?» [Sí, salir / Cancelar] | `ts:278-301` | |
| F-115 | No hay botón «Nuevo usuario» en la pestaña | El alta solo se abre desde Nuevo › Usuario de la cabecera (F-018) o con `?nuevo=1`. No existe «invitar» ni «reenviar invitación». | `security-people.component.html` (ausencia) | |

## 5. Pestaña ROLES Y PERMISOS — `/security/roles`

Es el componente `app-security-roles` (`CON/roles/security-roles.component.ts`). Permiso de la pestaña: `ROLE_VIEW`. Query params: `rol={id}` y `nuevo=1`.

### 5.1 Rail de roles

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-116 | Buscador de roles | Placeholder «Buscar rol…», `aria-label="Buscar rol"`. Filtra en el cliente por nombre o descripción. Selector: `.sec-roles__search input`. | `:73-81, 440-447` | |
| F-117 | Grupo «De la empresa» | Roles sin `code`. Cada **hijo va justo debajo de su padre**, con sangría y «↳» (`.sec-roles__child`, `.sec-roles__branch`). | `:86-105, 453-461` | |
| F-118 | Insignia «Vacío» | `gm-badge--warning` «Vacío» cuando `permissionCount` es 0. | `:99-101` | |
| F-119 | Conteo de titulares | `.gm-rail-count` con el tooltip «1 persona» o «N personas». | `:102, 498-501` | |
| F-120 | Grupo «Del sistema» | Roles con `code` y candado (`mat-icon lock`, `.sec-roles__lock`). | `:106-119` | |
| F-121 | Rail vacío | «No se encontraron resultados para los filtros seleccionados» | `:120-122` | |
| F-122 | Carga del rail | Tres esqueletos de línea. Pide hasta 200 roles. | `:83-84, 605-627` | |
| F-123 | Selección inicial | Abre el primer rol de la empresa (o el primero de todos). `?rol={id}` abre un rol concreto. | `:482-484, 629-632` | |
| F-124 | Sin rol elegido | Icono `admin_panel_settings` y «Elige un rol en la lista para ver y ajustar sus permisos.» | `:214-219` | |

### 5.2 Cabecera del rol abierto

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-125 | Nombre | `h2.sec-roles__h2`. | `:131` | |
| F-126 | Chip «Hereda de {padre}» | `button.gm-badge--info.sec-roles__chip`. Al pulsarlo **abre el rol padre**. | `:132-136` | |
| F-127 | Insignias | «Del sistema» (neutra) y «Administrador» (acento). | `:137-142` | |
| F-128 | Descripción y titulares | «{descripción} · » seguido del enlace «1 persona tiene este rol» o «N personas tienen este rol», que lleva a la subvista Personas. | `:144-149, 474-477` | |
| F-129 | Botón «Duplicar» | `mat-stroked-button` con el icono `content_copy`. Exige `ROLE_CREATE`; sin él **desaparece**. Sirve también para los roles del sistema. | `:152-157` | |
| F-130 | Botón «Editar» | Icono `edit`. Exige `ROLE_EDIT` y que el rol sea editable (`matrix.role.editable`). En un rol del sistema **desaparece**. | `:158-163, 469` | |
| F-131 | «Más acciones» › «Eliminar rol» | `mat-icon-button more_vert` con `aria-label` y tooltip «Más acciones». Su único ítem es «Eliminar rol» (icono `delete`, rojo). Exige `ROLE_DELETE`, que el rol sea editable y que `canDelete !== false`. Si no se cumple, **el botón de tres puntos desaparece**. | `:164-174, 470-472` | |
| F-132 | Confirmación de eliminar rol | Título «Eliminar rol». Mensaje: «¿Está seguro de que desea eliminar el rol "{nombre}"? Esta acción no se puede deshacer.» Botones «Cancelar» y «Eliminar» (rojo). | `:557-571` | |
| F-133 | Éxito / error al eliminar rol | Toast «Rol eliminado exitosamente» [OK, 2,5 s]. Error: «Error al eliminar el rol» (o el mensaje del API) [Cerrar, 5 s]. | `:572-584` | |
| F-134 | Subvistas | `nav.sec-roles__views` con `aria-label="Vistas del rol"` y los botones «Permisos», «Personas {n}» y «Historial». El activo lleva la clase `.is-on`. «Historial» exige `AUDIT_LOG_READ`; sin él **desaparece**. | `:178-186, 426` | |
| F-135 | Cambios sin guardar | Al cambiar de rol o de subvista con cambios pendientes sale una confirmación: título «Cambios sin guardar». Mensaje «Hay 1 cambio de permisos sin guardar. Si continúas, se descarta.» o «Hay N cambios de permisos sin guardar. Si continúas, se descartan.» Botones «Seguir editando» y «Descartar cambios» (rojo). | `:634-651` | |

### 5.3 Editor de permisos (subvista «Permisos»)

Es el componente `app-role-permission-editor` (`CON/roles/role-permission-editor.component.ts`). Carga `GET /role/:id/permission-matrix` y guarda con `PATCH /role/:id/permissions`.

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-136 | Rail «Módulos» | Muestra el total «{concedidos} de {disponibles}». Los módulos van **agrupados por sección** (`.rpe__section`). Cada módulo lleva una barra de cobertura y «n/total». Selector: `.rpe__module`, filtrado por el nombre. | `:117-138` | |
| F-137 | Módulo inicial | El primero donde el rol ya concede algo. | `:775-781` | |
| F-138 | Título del módulo | «Módulo {nombre}». La meta dice «{n} de {total} permisos» y, si hay padre, « · {n} heredados de {padre}». | `:147-155` | |
| F-139 | Filtros por estado del PERMISO | Grupo segmentado (`aria-label="Filtrar por estado"`) con cuatro botones: «Todos», «Concedidos», «Heredados» (incluye los excluidos) y «Sin conceder». **Son estados del permiso dentro del rol, no del documento.** | `:157-163, 577-582, 806-817` | |
| F-140 | Búsqueda en todo el catálogo | Placeholder «Buscar permiso…», `aria-label="Buscar permiso en todos los módulos"`. Con 2 letras o más busca en TODOS los módulos: por recurso, por módulo, por etiqueta de acción o por código (sin acentos). El título pasa a «Resultados de «{texto}»» y la meta a «{n} permisos en todo el catálogo». Los resultados se agrupan por módulo (`.gm-sheet-group`). | `:164-172, 144-146, 623-646` | |
| F-141 | Tope de la búsqueda | Pinta como máximo 60 recursos y avisa: «Se muestran los primeros 60 recursos: afina la búsqueda para ver el resto.» | `:78, 256-258` | |
| F-142 | Leyenda | «Concedido». Si hay padre, también «Heredado de {padre}» y «Excluido de la herencia». Cierra con «**Alcance** Propios · Equipo · Todos, en los listados que lo admiten». | `:175-182` | |
| F-143 | Aviso de rol del sistema (solo lectura) | Icono `lock` y el texto: «“{nombre}” es un rol del sistema: se ve aquí para saber qué concede. Duplícalo para tener una copia de tu empresa y ajustarla.» Todas las acciones quedan **deshabilitadas** (`[disabled]`). | `:184-192` | |
| F-144 | Recurso | `.rpe__resource` muestra el nombre del recurso, «{concedidas}/{acciones}» y el botón «Conceder todo» o «Quitar todo» (solo si se puede editar). Un recurso con cambios lleva `.rpe__resource--changed` (fondo crema). | `:199-211` | |
| F-145 | Acciones del recurso | Cada acción es un botón `.rpe__act` con la etiqueta real (Ver, Crear, Emitir, Anular, Reversar…). El estado va en la clase: `--direct` (con ✓), `--inherited`, `--excluded` o `--none`. `aria-pressed` indica si está concedida y el tooltip (400 ms) dice «{estado} · {CODIGO}». Estados: «Concedido», «Heredado del rol padre», «Excluido de la herencia» y «Sin conceder». Sin `ROLE_EDIT` o en un rol del sistema están **deshabilitadas**. Selector: `.rpe__resource` con el recurso → `getByRole('button', {name:'Ver', exact:true})`. | `:212-229, 64-69` | |
| F-146 | Ciclo al pulsar | Sin conceder → Concedido → Sin conceder. En los heredados: Heredado → Excluido → Heredado. | `permission-edits.ts:33-44` | |
| F-147 | Alcance | Solo en las acciones concedidas que lo admiten (`supportsScope`). Muestra «{acción}» y un segmentado **«Propios» / «Equipo» / «Todos»** (`.rpe__scope-seg`, `aria-label="Alcance de {acción} en {recurso}"`). Sin ROLE_EDIT está deshabilitado. Por defecto: `ALL`. | `:230-246, 71-75`; `permission-edits.ts:51-60` | |
| F-148 | Barra de guardado por lote | `.gm-sheet-savebar` (`role="status"`) dice «**N cambio(s) sin guardar** · afectan a N persona(s)». Botones «Descartar» (icono `close`) y «Guardar cambios» (icono `save`; muestra «Guardando…» mientras guarda). Todo va en una sola petición. | `:261-276, 669-672, 749-769` | |
| F-149 | Éxito / error al guardar permisos | Toast «Permisos del rol actualizados exitosamente» [OK, 2,5 s]. Error: «Error al guardar los permisos» (o el mensaje del API) [Cerrar, 5 s]. | `:759, 764` | |
| F-150 | Vacío / error / carga del editor | Vacío: icono `inbox` o `search_off` y «No se encontraron resultados para los filtros seleccionados». Error: «Error al cargar los datos. Intenta nuevamente.» con el botón «Reintentar». Carga: dos líneas y una tarjeta de 360 px. | `:100-114, 250-255` | |
| F-151 | Pantalla estrecha | En 991 px o menos el rail de módulos se apila con un alto máximo de 220 px (el de roles, 240 px). | `:542-557`; `security-roles.component.ts:401-409` | |

### 5.4 Subvista «Personas» del rol

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-152 | Tabla de titulares | Columnas Persona (avatar, nombre, correo) · Último ingreso · Estado («Activa» o «Inactiva»). Muestra hasta 50. Pide `GET /user?roleId=`. | `CON/roles/role-holders.component.ts:23-45, 96-108` | |
| F-153 | Abrir una persona | Al pulsar la fila va a `/security/personas?usuario={id}`. | `:129-131` | |
| F-154 | Más de 50 | «Se muestran {n} de {total}.» y el enlace «Ver todas en Personas →», que va a `/security/personas?rol={id}`. | `:52-57, 133-135` | |
| F-155 | Vacío | «Nadie tiene este rol todavía.» | `:46-51` | |

### 5.5 Subvista «Historial» del rol

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-156 | Entradas | Cada entrada lleva una insignia de acción («Cambió permisos» si es `PERMISSIONS_CHANGED`), quién y cuándo. Debajo, líneas «campo  antes → después»: el antes tachado en rojo y el después en verde. Hasta 30 entradas, de `GET /v1/audit-logs/entity/roles/{id}`. | `CON/roles/role-history.component.ts:30-50, 98-127` | |
| F-157 | Vacío | Icono `inbox` y «No se encontraron registros». | `:50-55` | |

### 5.6 Diálogo de rol (crear / editar / duplicar)

Es el componente `app-rol-form` (`SEC/rol/components/rol-form/`). Ancho 640 px, `disableClose`.

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-158 | Títulos y botón | «Crear Rol» con [Crear] · «Editar Rol» con [Actualizar] · **«Clonar Rol»** con [Clonar] (se abre desde el botón «Duplicar»). A la izquierda siempre va «Cancelar». | `rol-form.component.ts:111-121` | |
| F-159 | Aviso de clonado | «Se creará un nuevo rol copiando los permisos, la herencia y las exclusiones de **{rol}**.» | `rol-form.component.html:14-26` | |
| F-160 | Nombre | `formcontrolname="name"`, obligatorio. Al clonar arranca vacío y copia la descripción. | `html:28-37`; `ts:139-141` | |
| F-161 | Descripción | `textarea formcontrolname="description"` | `html:39-47` | |
| F-162 | Herencia: interruptor | `mat-slide-toggle` «Heredar permisos de otro rol». No aparece al clonar. | `html:50-62` | |
| F-163 | Herencia: elegir el padre | `mat-select formcontrolname="parentRole"`, `mat-label` «Rol padre», placeholder «Selecciona el rol del cual heredar», icono `account_tree`. Ofrece todos los roles (hasta 500); a los del sistema les pone la etiqueta «Sistema». **Excluye el propio rol y a todos sus descendientes** para evitar ciclos. Con el interruptor encendido, el padre es obligatorio. | `html:64-82`; `ts:51-57, 147-158, 177-198` | |
| F-164 | Aviso de herencia | «Este rol heredará automáticamente los permisos de **{padre}** y se mantendrá sincronizado con sus cambios. Podrás excluir permisos individuales desde el detalle del rol.» | `html:84-94` | |
| F-165 | Aviso al cambiar el padre (edición) | Icono `sync`: «Al guardar se recalcularán los permisos heredados de este rol. Los permisos asignados directamente no se modifican.» | `html:98-106` | |
| F-166 | Éxito del rol | Diálogo Aceptar success «Operación completada». Mensaje «El rol ha sido creado correctamente.», «El rol ha sido actualizado correctamente.» o «El rol ha sido clonado correctamente con sus permisos, herencia y exclusiones.» Botón «Aceptar». | `ts:233-251, 295-299` | |
| F-167 | Error del rol | Diálogo Aceptar error «Error» con el mensaje del API y el botón «Entendido». | `ts:252-264` | |
| F-168 | Salir con cambios (rol) | «Guardar Cambios» / «¿Estás seguro que deseas salir sin guardar los cambios?» [Sí, salir / Cancelar] | `ts:200-223` | |

## 6. Pestaña INTEGRACIONES — `/security/integraciones`

Es el componente `app-security-integrations` (`CON/integraciones/security-integrations.component.{html,ts}`). Permiso de la pestaña: `INTEGRATION_USER_VIEW`. Query params: `credencial={id}` y `nuevo=1`.

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-169 | Barra superior | Título «Credenciales de API», el botón «Documentación de la API» (icono `menu_book`, sin permiso, lleva a `/security/api-docs`) y el botón «Nueva credencial» (icono `add`), que exige `INTEGRATION_USER_CREATE`; sin él **desaparece**. | `html:35-47`; `ts:191-193` | |
| F-170 | Diálogo «Nueva integración» | Ancho 760 px. Nota inicial: «Al guardar se generan una clave y un secreto. El **secreto se enseña una sola vez**: Germiva no lo guarda en claro y, si se pierde, hay que regenerarlo.» | `SEC/integration-user/components/integration-user-form/integration-user-form.component.ts:53-60` | |
| F-171 | Campos del alta | «Nombre de la Integración» (`formcontrolname="integrationName"`, obligatorio, 3 como mínimo; placeholder «Portal de Clientes, Tienda en línea...»; errores «El nombre es obligatorio» y «Mínimo 3 caracteres») y «Descripción» (`integrationDescription`, placeholder «Qué hace esta integración»). | `:62-85, 207-210` | |
| F-172 | Restricciones (opcional) | Sección «Restricciones · Opcional» con el texto: «Sin restricciones, la credencial funciona desde cualquier origen y contra cualquier ruta. Acotarla es lo que limita el daño si se filtra.» | `:87-96` | |
| F-173 | IP permitida | Campo «IP permitida» (placeholder «192.168.1.1»). Se añade con Enter o con el botón «Agregar IP» y queda como chip, que se quita con «Quitar». Admite `*`. Error: «Escribe una IP válida, por ejemplo 192.168.1.1». | `:99-129, 218-236` | |
| F-174 | Endpoint permitido | Campo «Endpoint permitido» (placeholder «/api/v1/invoice») y el botón «Agregar endpoint». Cada endpoint queda como chip. | `:131-158` | |
| F-175 | Botones del alta | «Cancelar» (icono `close`) y «Generar credenciales» (icono `vpn_key`, deshabilitado si el formulario no es válido). Si falla, se ve una franja roja dentro del diálogo con «Error al crear la integración» o el mensaje del API. | `:161-188, 274-277` | |
| F-176 | Franja del secreto (una sola vez) | `.sec-api__secret` (`role="status"`, icono `key`). Dice: «**Credencial «{nombre}» lista.** Copia el secreto ahora: no se vuelve a mostrar.» Muestra la API Key completa con el botón «API Key» (copiar). El secreto va enmascarado (12 primeros caracteres + 18 puntos + 4 últimos) con los botones «Mostrar»/«Ocultar» y «Copiar secreto». El botón cerrar tiene `aria-label="Cerrar aviso"` y el tooltip «Ya lo guardé». Es una franja, NO un diálogo. | `html:1-31`; `ts:177-179, 199-217` | |
| F-177 | Aviso al copiar | Toast «API Key copiado», «Secreto copiado» o «No se pudo copiar el …» [OK, 2 s]. | `ts:269-272` | |
| F-178 | Tabla de credenciales | Columnas Credencial (nombre y «Creada el {d mes} · {descripción}») · Prefijo de la API Key · Último uso («Nunca» si no hay; en rojo si lleva más de 60 días) · Estado («Activa», «Sin uso» en rojo, «Inactiva»). Selector: `.sec-api__row` con el nombre. | `html:50-87`; `ts:158-175` | |
| F-179 | Carga, error y vacío de la lista | Carga: dos esqueletos de 48 px. Error: «Error al cargar los datos. Intenta nuevamente.» y «Reintentar». Vacío: icono `inbox` y «No se encontraron registros». | `html:56-93` | |
| F-180 | Notas al pie | «Cada credencial tiene sus propios permisos: cambiar los de una no toca los de otra.» y «Rotar un secreto invalida el anterior de inmediato.» | `html:95-98` | |
| F-181 | Panel de la credencial | Se abre al pulsar la fila (`?credencial={id}`). Muestra nombre, prefijo y cerrar («Cerrar panel»). Datos: estado · «{n} llamadas en total» · «{n} IP permitidas» o «Sin restricción de IP». | `html:102-119` | |
| F-182 | Botón «Editar permisos» | `mat-flat-button` con el icono `shield`. Va a `/security/integration-user/{id}/permissions`. **No tiene control de permiso en el front** (ver D-05). | `html:121-124`; `ts:195-197` | |
| F-183 | Botón «Rotar secreto» | Icono `autorenew`. Exige `INTEGRATION_USER_EDIT`. Confirmación: título «Rotar secreto». Mensaje: «¿Rotar el secreto de "{nombre}"? El actual deja de funcionar de inmediato y la integración se cae hasta que se actualice en su lado.» Botones «Cancelar» y «Rotar secreto». Si sale bien, reaparece la franja del secreto (F-176). Error: toast «Error al rotar el secreto». | `html:125-130`; `ts:219-234` | |
| F-184 | «Más acciones» › Desactivar / Activar | Exige `INTEGRATION_USER_EDIT`. Iconos `pause_circle` / `play_circle`. No pide confirmación. Toast «Integración desactivada exitosamente» o «Integración activada exitosamente» [OK]. Error: «Error al actualizar la integración». | `html:131-141`; `ts:236-245` | |
| F-185 | «Más acciones» › Revocar y eliminar | Exige `INTEGRATION_USER_DELETE` (en rojo). Confirmación: título «Revocar credencial». Mensaje: «¿Está seguro de que desea eliminar la integración "{nombre}"? Sus credenciales dejarán de funcionar. Esta acción no se puede deshacer.» Botón «Eliminar». Toast «Integración eliminada exitosamente». Error: «Error al eliminar la integración». | `html:142-147`; `ts:247-263` | |
| F-186 | Bloque «Permisos» del panel | «Permisos {n}». Si la credencial aún usa la plantilla compartida: «Usa los permisos de la plantilla de integraciones. Al editarlos recibe los suyos propios.» Por módulo: nombre, «n/total» y un detalle en palabras. Sin permisos: «Ningún permiso concedido.» Los datos vienen de `GET /v1/integration-users/:id/summary`. | `html:157-176` | |
| F-187 | Bloque «Operaciones en 7 días» | Total y siete barras con tooltip «N operación(es)». La de hoy va resaltada y los rótulos son «lun…hoy». Texto: «Lo que la credencial creó, modificó o eliminó, según la bitácora.» | `html:178-196`; `ts:86-99` | |
| F-188 | Credencial inexistente | Icono `search_off` y «La credencial no existe o fue eliminada.», con el botón «Cerrar». | `html:199-205` | |

### 6.1 Página de permisos de una credencial — `/security/integration-user/:id/permissions`

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-189 | Cabecera | El breadcrumb tiene el título «Permisos de Integración» y las migas «Seguridad › Integraciones API › {nombre} › Permisos». Diseño viejo con `mat-card`. | `SEC/integration-user/pages/integration-user-permissions/integration-user-permissions.component.ts:61-65` | |
| F-190 | Tarjeta de datos | Nombre (icono `integration_instructions`), «API Key Prefix:», «Descripción:» («Sin descripción» si no hay), «Estado:» («Activo» o «Inactivo») y «Permisos activos:» «n de total». | `:73-104` | |
| F-191 | Permisos por módulo | Tarjeta «Permisos Disponibles por Módulo», buscador «Buscar permisos» (placeholder «Nombre o código...») y el total «n de total permisos activos». Hay un acordeón por módulo con submódulos, cada uno con código y «n / total». Dentro, una casilla por permiso con nombre y código. **Cada casilla guarda al instante**, sin botón de guardar y sin toast de éxito. | `:107-270` | |
| F-192 | Mensajes de la página | «Cargando permisos...» · «No hay permisos disponibles en el sistema» · «No se encontraron permisos» · toast «Error al cargar datos» / «Error al actualizar permiso» [Cerrar]. Si falla la carga: «No se pudo cargar la información de la integración». | `:68-69, 115-124, 262-266, 281-287; 800-841` | |
| F-193 | Volver | Botón «Volver a Integraciones» (icono `arrow_back`). Va a `/security/integration-user`, que redirige a `integraciones` (**se pierde la credencial abierta**). | `:273-277, 850-852` | |

### 6.2 Documentación de la API — `/security/api-docs` → `/security/api-docs/referencia-endpoints`

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-194 | Dónde está | Se abre con el botón «Documentación de la API» de Integraciones (F-169). La URL es `/security/api-docs`, que redirige a `/security/api-docs/referencia-endpoints`. Tiene layout propio (NO es una pestaña). | `security.routes.ts:108-114` | |
| F-195 | Barra lateral | Encabezado «Documentación API» (icono `menu_book`). En móvil hay un botón «Menu». Secciones plegables: Inicio (Referencia de Endpoints, Codigos y Respuestas, Registro de Cambios) · Autenticacion (Login POST) · Facturas Emitidas (Crear, Listar, Consultar, Estado Fiscal, Reintentar Envio DGII, Enviar al Comprador, Descargar PDF, Obtener QR, Actualizar, Anular) · Facturas Recibidas (Listar, Consultar, Aprobacion Comercial) · Reportes DGII (IT-1 datos, Excel y TXT) · Cuenta (Estado de Suscripción). Son 21 documentos, con una insignia de método HTTP. | `modules/api-docs/pages/api-docs-layout/api-docs-layout.component.html:1-44`; `modules/api-docs/data/api-docs-nav.data.ts` | |
| F-196 | Contenido | Markdown servido desde `assets/docs/api/endpoints/*.md` con `ngx-markdown`. Un slug que no existe muestra «Documento no encontrado.» | `api-docs-viewer.component.ts:27-31`; `.html:1-5` | |

## 7. Pestaña AUDITORÍA — `/security/auditoria`

Es el componente `app-security-audit` (`CON/auditoria/security-audit.component.{html,ts}`). Permiso de la pestaña: `AUDIT_LOG_READ`. Datos: `GET /v1/audit-logs`. Query params: `periodo`, `persona` (o el alias `userName`), `acciones`, `registro`, `registroId`, `ip` y `evento`.

| ID | Qué | Detalle exacto | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-197 | Filtro Período | `mat-stroked-button` con el icono `calendar_today` y la etiqueta del período. Menú con radios: «Hoy», «Últimos 7 días» (el de siempre), «Últimos 30 días», «Este mes» y «Todo el historial». Pone `?periodo=hoy/30d/mes/todo`; 7d no se escribe en la URL. | `html:2-13`; `ts:25-33, 229-231` | |
| F-198 | Filtro Persona | Campo con el icono `person`, placeholder «Persona» y `aria-label="Filtrar por persona"`. Espera 400 ms y pone `?persona=`. | `html:15-18`; `ts:240-245` | |
| F-199 | Filtro Acciones | Botón con el icono `filter_list` y el texto «Acción» o «Acción: Creó, Eliminó…». Menú de casillas **de selección múltiple** que no se cierra al marcar: Creó, Actualizó, Eliminó, Cambió estado, Acceso, Consultó, Acción, Exportó, Imprimió. Pone `?acciones=CREATE,DELETE`. | `html:20-31`; `ts:94-98, 233-238` | |
| F-200 | Filtro Registro | Campo con el icono `description`, placeholder «Registro» y `aria-label="Filtrar por registro"`. Filtra por el nombre de la tabla (p. ej. `roles`) y pone `?registro=`; al escribir borra `registroId`. | `html:33-36`; `ts:244` | |
| F-201 | Filtro IP | Campo con el icono `lan`, placeholder «IP» y `aria-label="Filtrar por IP"`. Pone `?ip=`. | `html:38-41` | |
| F-202 | «Limpiar» | Botón con el icono `filter_alt_off`. Solo aparece si hay algún filtro o un período distinto de 7 días. | `html:43-48`; `ts:99-101, 247-249` | |
| F-203 | Total | «{n} evento(s)» | `html:50` | |
| F-204 | Agrupación por día | Encabezados `.gm-sheet-group`: «Hoy · sábado 27 de septiembre», «Ayer · …» o «Viernes 25 de septiembre». | `html:80-81`; `ts:103-112`; `security-console.shared.ts:68-76` | |
| F-205 | Fila de evento | Columnas Hora (HH:MM, hora RD) · Quién · Acción (insignia) · Registro («{etiqueta} #id») · IP. Selector: `.sec-audit__row` con el texto (p. ej. «Cambió permisos»). | `html:56-95` | |
| F-206 | Nombre legible del registro | auth → «Sesión», users → «Usuario», profiles → «Perfil», roles → «Rol», role_permissions → «Permisos del rol», role_permission_exclusions → «Permisos excluidos del rol», user_company_roles → «Rol asignado», user_companies → «Acceso a la empresa», teams → «Equipo», team_members → «Miembro de equipo», permission → «Permiso», companies → «Empresa», user_menu_visibility → «Visibilidad del menú». El resto se muestra capitalizado. | `SEC/audit/interface/audit.interface.ts:48-72` | |
| F-207 | Carga, error y vacío | Carga: seis esqueletos de 30 px. Error: «Error al cargar los datos. Intenta nuevamente.» y «Reintentar». Vacío: «No se encontraron registros», o «No se encontraron resultados para los filtros seleccionados» si hay filtros. | `html:64-102` | |
| F-208 | «Cargar eventos anteriores» | Botón con el icono `expand_more` que carga 50 más; muestra «Cargando…» mientras tanto. | `html:103-110`; `ts:35, 181-193` | |
| F-209 | Detalle del evento | Se abre al pulsar la fila (`?evento={id}`). Panel `aside` con `aria-label="Detalle del evento"`: insignia, fecha y hora completas, cerrar («Cerrar detalle»), «{registro} #id» y «por **{persona}**» («el sistema» si no hay persona). | `html:115-130` | |
| F-210 | «Qué cambió» (antes → después) | Una línea por campo: el antes tachado y el después resaltado. Sin cambios: «Este evento no registra cambios de campos.» | `html:132-146` | |
| F-211 | «Solicitud» (origen) | Muestra IP, Origen (navegador · sistema), Evento (código, si lo hay) y Solicitud (`requestId`). | `html:147-162` | |
| F-212 | «Historial del registro →» | Filtra la bitácora por ese registro exacto: `registro`, `registroId`, `periodo=todo`. | `html:164`; `ts:259-261` | |
| F-213 | «Ver a {persona} →» | Va a `/security/personas?q={userName}`. | `html:165-167`; `ts:263-265` | |
| F-214 | Evento fuera del filtro | Icono `search_off` y «El evento no está entre los resultados de los filtros actuales.», con el botón «Cerrar». | `html:171-177` | |
| F-215 | Llegadas ya filtradas | Desde el Resumen (`?evento=`), desde Personas «Ver su actividad» (`?persona=`) y desde la ruta vieja de historial (F-007). | varios | |

## 8. Lo que se mudó de Seguridad

| ID | Qué | Detalle exacto | Archivo:línea | Commit | Video / min |
|---|---|---|---|---|---|
| F-216 | Cómo llegar a Mi perfil | Se abre el menú del usuario (arriba a la derecha, `button.topbar-user`) y se elige «Mi perfil» (icono `account_circle`). La ruta es **`/profile`**, con `canActivateAutorizedRoute` (solo sesión, sin permiso). El breadcrumb dice «Mi Perfil» con las migas «Perfil › Mi Perfil». | `layout/header/header.component.html:74-112`; `modules/profile/profile.routes.ts`; `profile-view.component.html:3` | | |
| F-217 | Cambio de contraseña | Tarjeta **«Seguridad»** con el subtítulo «Cambie su contraseña de acceso». Campos: «Contraseña actual» (`formcontrolname="password"`), «Contraseña nueva» (`new_password`) y «Confirmar contraseña nueva» (`confirm_new_password`). Cada uno tiene un ojo con el tooltip «Mostrar contraseña» / «Ocultar contraseña». Botón «Actualizar contraseña» (icono `lock_reset`), que dice «Guardando...» mientras guarda. Éxito: **diálogo Aceptar** «Éxito» con «Contraseña actualizada exitosamente». Error: diálogo «Error» [Aceptar]. | `modules/profile/pages/profile-view/profile-view.component.html:447-547`; `.ts:430, 734-760` | `5d93c9e28` (#749, 20-07-2026): «Password change consolidated into the profile; /security/settings now…» | |
| F-218 | Cuenta con la clave bloqueada | En lugar del formulario sale el aviso: «Esta cuenta tiene el **cambio de contraseña bloqueado**: la contraseña no puede modificarse.» | `profile-view.component.html:456-463` | | |
| F-219 | Visibilidad del menú | En Mi perfil, tarjeta **«Preferencias»** («Personalice su experiencia en el sistema»), que también trae Idioma y Tema (Claro/Oscuro). La sección plegable **«Visibilidad del menú»** dice: «Elige qué módulos y opciones ves en tu menú lateral. Aplica solo para tu usuario en esta empresa.» Se despliega con un botón que tiene `aria-label` «Desplegar» / «Contraer». | `profile-view.component.html:388-445` | `66a47f0c7` (#1031, 29-08-2026) | |
| F-220 | Contenido de Visibilidad del menú | `app-menu-visibility-config [embedded]`. Botones «Restablecer Todo» (rojo, icono `restart_alt`) y «Guardar Cambios» (icono `save`, deshabilitado si no hay cambios). Hay un árbol de menús con `mat-slide-toggle`; los que no se pueden ocultar muestran un candado con el tooltip «Este menú no puede ser ocultado». | `SEC/menu-visibility/pages/menu-visibility-config.component.html:13-90` | | |
| F-221 | Mensajes de Visibilidad del menú | Guardar: diálogo Aceptar «Cambios Guardados» con «La configuración de visibilidad del menú se ha guardado correctamente.» Error: «Error al Guardar» [Entendido]. Restablecer pide confirmación: «¿Restablecer Todo?» con «Se mostrarán todos los menús ocultos. ¿Desea continuar?» [Sí, restablecer / Cancelar], y luego «Menús Restablecidos» con «Todos los menús han sido restablecidos y son visibles nuevamente.» [Aceptar]. Error: «Error al Restablecer». | `menu-visibility-config.component.ts:150-240` | | |
| F-222 | Perfil del Consultorio | Ruta nueva **`/my-company/perfil-consultorio`**. En el menú está en «Configuración › Perfil del Consultorio» (icono `medical_information`). **Solo en modo clínica (RegiSalud)** y con `COMPANY_UPDATE`. Guard `canActivateClinicOnlyFn(['COMPANY_UPDATE'])`: en el ERP o sin el permiso redirige a `/home` **sin aviso**. | `modules/my-company/my-company.routes.ts:19-33`; `sidebar-items.ts:2003-2019`; `core/guard/can-activate.guard.ts:301-319` | `66a47f0c7` (#1031) | |
| F-223 | Textos del Perfil del Consultorio | Breadcrumb «Configuración › Perfil del Consultorio». Texto: «Elige el perfil de tu operación para mostrar solo los módulos que necesitas. Puedes ajustar cada módulo o mostrar todo cuando quieras.» Tarjetas «Médico Independiente» y «Centro Médico». Debajo, «Módulos visibles» con «N oculto(s)» y los botones «Aplicar sugeridos», «Mostrar todo» y «Guardar». Éxito: diálogo Aceptar «Cambios Guardados» con «El perfil del consultorio se ha guardado correctamente.» Error: «Error al Guardar» [Entendido]. | `SEC/medical-profile/pages/medical-profile-config.component.html:1-80`; `.ts:270-285` | | |
| F-224 | Relevancia para una serie del ERP | Perfil del Consultorio **no aplica al ERP Germiva**: el guard lo manda a `/home`. En los videos del ERP basta con mencionar que «ya no está en Seguridad». | — | | |

## 9. Permisos y comportamiento sin permiso (resumen)

### 9.1 Tabla de permisos → elemento

| ID | Permiso | Qué controla en el front | Cómo se oculta | Video / min |
|---|---|---|---|---|
| F-225 | `USER_VIEW` | Pestaña Resumen, carga del overview (conteos), lista de Personas | Pestaña desaparece. Sin él la lista de Personas no carga (queda vacía). Sin él no hay conteos. | |
| F-226 | `TEAM_VIEW` | Entrada a Personas (junto con USER_VIEW), lista de equipos del rail | Desaparece | |
| F-227 | `USER_CREATE` | Nuevo › Usuario; `?nuevo=1` | Desaparece; el parámetro se ignora en silencio | |
| F-228 | `USER_EDIT` | Botones Editar y Cambiar contraseña, Desactivar/Activar, «+ Asignar rol» | Desaparecen | |
| F-229 | `USER_DELETE` | Más acciones › Eliminar | Desaparece | |
| F-230 | `TEAM_CREATE` / `TEAM_EDIT` / `TEAM_DELETE` | «+» Nuevo equipo y Nuevo › Equipo / «Editar equipo» / papelera del equipo | Desaparecen | |
| F-231 | `TEAM_MANAGE_MEMBERS` | «Agregar a equipo» y «Quitar del equipo» | Desaparecen (la barra deja solo «Limpiar») | |
| F-232 | `ROLE_VIEW` | Pestaña «Roles y permisos» | Desaparece | |
| F-233 | `ROLE_CREATE` | Nuevo › Rol, «Duplicar» | Desaparecen | |
| F-234 | `ROLE_EDIT` | «Editar» del rol, casillas de acción, alcance, Conceder/Quitar todo | «Editar» y «Conceder todo» desaparecen; las acciones y el alcance se **deshabilitan** (se ven grises) | |
| F-235 | `ROLE_DELETE` | Más acciones › Eliminar rol | El botón de tres puntos desaparece | |
| F-236 | `AUDIT_LOG_READ` | Pestaña Auditoría, subvista «Historial» del rol, «Ver su actividad» | Desaparecen | |
| F-237 | `INTEGRATION_USER_VIEW` | Pestaña Integraciones | Desaparece | |
| F-238 | `INTEGRATION_USER_CREATE` | «Nueva credencial», Nuevo › Integración de API | Desaparecen | |
| F-239 | `INTEGRATION_USER_EDIT` | «Rotar secreto», Desactivar/Activar | Desaparecen | |
| F-240 | `INTEGRATION_USER_DELETE` | «Revocar y eliminar» | Desaparece | |
| F-241 | Sin permiso de front | «Editar permisos» de la credencial y su página; «Documentación de la API» | Siempre visibles (ver D-05) | |
| F-242 | `PERMISSION_VIEW`, `AUDIT_VIEW` | SOLO la visibilidad de la entrada del menú (F-002). Ninguna pestaña los usa. | — (ver D-03) | |

### 9.2 Qué ve un usuario sin permiso que entra por URL directa

| ID | Caso | Resultado en el front | Video / min |
|---|---|---|---|
| F-243 | Tiene alguna pestaña pero no la pedida (p. ej. `/security/auditoria` sin AUDIT_LOG_READ) | No hay redirección. La URL se queda igual, se ve la franja con candado «No tiene permiso para ver «Auditoría». Solicite el acceso al administrador de la empresa.» y debajo el contenido de la primera pestaña visible. En el breadcrumb queda marcada esa primera pestaña. | |
| F-244 | Entra por el menú («Seguridad» → `/security/resumen`) sin USER_VIEW | Ve la franja «No tiene permiso para ver «Resumen»…» **aunque entró por el menú**, y debajo su primera pestaña visible (ver D-02). | |
| F-245 | No tiene ninguno de los permisos de pestaña | Ve la cabecera «Seguridad» sin pestañas, la franja «No tiene permiso para ver «{pestaña}»» y el cuerpo vacío. Si tiene algún `*_CREATE`, el botón «Nuevo» sigue apareciendo. | |
| F-246 | Pide `?nuevo=1` sin el permiso de alta | El parámetro se borra y no se abre ningún diálogo. No hay aviso. | |
| F-247 | Pide `/security/integration-user/:id/permissions` sin permisos | La página se abre (no tiene guard). El API decidirá: si responde 403, sale el toast «Error al cargar datos» y «No se pudo cargar la información de la integración». **INFERIDO**. | |
| F-248 | Pide `/my-company/perfil-consultorio` sin COMPANY_UPDATE o en el ERP | Redirige a `/home` sin aviso. | |

## 10. Permisos en el FRONT de otros módulos (para los ejemplos con y sin permiso)

| ID | Mecanismo | Detalle | Archivo:línea | Video / min |
|---|---|---|---|---|
| F-249 | Servicio de permisos | `PermissionService.has(code | code[], strict=false)`: una lista funciona como OR y con `strict` como AND. `hasFn()` es la versión con señal. Lee `session.permissionCodes` (lista plana que calcula el API; **no trae el alcance**). | `core/service/permission.service.ts:54-83, 89-102` | |
| F-250 | Menú lateral | Cada entrada tiene `visible: this.requireEmailVerifiedAndPermission([...])` (correo verificado + OR de permisos) o `this.permission.hasFn([...])`, más `module: ModuleCode` (el plan contratado). Si no se cumple, la entrada **desaparece**. Ejemplo: grupo «Ventas» (`QUOTE_VIEW`, `SALES_ORDER_VIEW`, …) y la subentrada «Cotizaciones» (`QUOTE_VIEW`, módulo `SALES_QUOTE`). | `layout/sidebar/sidebar-items.ts:52-54, 264-324` | |
| F-251 | Guard por `data.permissions` (URL directa) | El tronco autenticado aplica `canActivateByRouteDataPermissionsFn` en OR. Sin permiso: `RedirectCommand('/home')` **sin aviso**. Ejemplos: `/sales/quotes` (QUOTE_VIEW), `/sales/quotes/create` (QUOTE_CREATE), `/sales/quotes/edit/:n` (QUOTE_UPDATE), `/inventory/product/list` (PRODUCT_VIEW) y `/inventory/product/create` (PRODUCT_CREATE). | `core/guard/can-activate.guard.ts:117-140`; `app.routes.ts:~174-181`; `modules/sales/sales.routes.ts:60-105`; `modules/inventory/inventory.routes.ts:90-114` | |
| F-252 | Guard `canActivateRouteByPermissionsFn` (otras rutas) | Redirige a `/home` **con un toast de aviso**: «No tienes acceso a esa sección. Pide a un administrador que te asigne el permiso.» [Cerrar] (clase `snackbar-warning`). Lo usa, p. ej., `/my-company` (COMPANY_VIEW). | `can-activate.guard.ts:25-73`; `my-company.routes.ts:12` | |
| F-253 | Botones de listas dinámicas | `DynamicViewConfig.actions[].permission`. `dynamic-table` pinta la acción solo si `hasPermission(action.permission)`; si no, **desaparece** (no se deshabilita). | `shared/components/dynamic-table/dynamic-table.component.ts:46, 109, 360, 2365` | |
| F-254 | Cotizaciones: lista | Botón de cabecera «Crear Cotización» (QUOTE_CREATE). En la fila: «Abrir» (sin permiso propio) y «Más acciones» › «Duplicar» (QUOTE_CREATE). | `modules/sales/quotes/pages/quote-list/quote-list.component.ts:565-611` | |
| F-255 | Cotizaciones: formulario | «Más acciones» › «Convertir a factura» (`QUOTE_CONVERT_DIRECTLY_TO_INVOICE`), «Convertir a orden de venta» (`QUOTE_CONVERT_TO_ORDER`) y «Duplicar» (QUOTE_CREATE). Las conversiones además **dependen del estado**: APPROVED o ACCEPTED, o DRAFT si la empresa no exige aprobación (`canConvertToDocument`). | `quote-form.component.html:147-188`; `.ts:243-246, 910-925` | |
| F-256 | Cotizaciones: estados (stepper) | Cada paso del stepper exige su permiso: ACCEPTED → `QUOTE_ACCEPT`; REJECTED → `QUOTE_REJECT` (solo si la cotización requiere aprobación); APPROVED → `QUOTE_APPROVE` si requiere aprobación, o `QUOTE_UPDATE` si no; CANCELLED y EXPIRED → `QUOTE_UPDATE`; CONVERTED → `QUOTE_CONVERT_TO_ORDER`; INVOICED → `QUOTE_CONVERT_DIRECTLY_TO_INVOICE`. Sin el permiso, el paso no queda disponible (no se puede pulsar). | `quote-form.component.ts:4270, 4373-4388` | |
| F-257 | Productos: lista | Cabecera: «Nuevo Producto» (PRODUCT_CREATE), «Alta por foto» (PRODUCT_VIEW) e «Importar / Exportar» (PRODUCT_EXPORT). Fila: «Abrir» (PRODUCT_VIEW), «Duplicar» (PRODUCT_CREATE), «Desactivar»/«Activar» (PRODUCT_UPDATE) y «Eliminar» (PRODUCT_DELETE). | `modules/inventory/product/pages/product-list/product-list.component.ts:350-446` | |
| F-258 | Alcance en el front | **El front no muestra nada del alcance** (Propios / Equipo / Todos). La sesión solo trae códigos, sin alcance. El efecto se ve en el número de filas que devuelve el API. `QUOTE_VIEW`, `SALES_ORDER_VIEW`, `INVOICE_VIEW`, `PRODUCT_VIEW`, `PARTNER_VIEW`, `CASHIER_SESSION_VIEW` y otras admiten alcance (`supportsScope: true`, 210 permisos). | API `admin/permission/default.permission.ts` (p. ej. `:1702` QUOTE_VIEW) | |

### 10.1 Candidatos para demostrar en video (con usuario A = con permiso / usuario B = sin permiso)

| ID | Tipo | Pantalla + elemento + permiso | Qué se ve CON | Qué se ve SIN |
|---|---|---|---|---|
| F-259 | **VISTA** | Menú «Ventas › Cotizaciones» y URL `/sales/quotes`, con **`QUOTE_VIEW`** (módulo SALES_QUOTE contratado). Se quita en Roles y permisos › Ventas › recurso Cotizaciones › acción «Ver». | La entrada del menú y la lista | La entrada desaparece del menú. Si teclea la URL, vuelve a `/home` **sin aviso** (guard por `data.permissions`). Ideal para mostrarlo junto al contraste de F-252. |
| F-260 | **ACCIÓN** | En `/sales/quotes`, el botón de cabecera **«Crear Cotización»** (`QUOTE_CREATE`) y «Más acciones › Duplicar». Alternativa: `/inventory/product/list`, fila › **«Eliminar»** (`PRODUCT_DELETE`). | Los botones | Los botones desaparecen. `/sales/quotes/create` por URL vuelve a `/home`. |
| F-261 | **ALCANCE** | `QUOTE_VIEW` con alcance **«Propios»** frente a «Todos» (segmentado de F-147) para un vendedor. Se ve en `/sales/quotes`. | Todas las cotizaciones de la empresa | Solo las que creó él. La pantalla no muestra ningún rótulo: el contraste está en el número de filas y el total. **INFERIDO**: que «propio» signifique «creado por él» lo aplica el API y hay que confirmarlo con el autor del API. |
| F-262 | **ESTADO** | Formulario de cotización: stepper **«Aprobada»** con `QUOTE_APPROVE` (empresa que exige aprobación) y «Más acciones › Convertir a factura», que exige `QUOTE_CONVERT_DIRECTLY_TO_INVOICE` **y** un estado APPROVED o ACCEPTED. | Paso pulsable y conversión disponible cuando el estado lo permite | Sin el permiso, el paso no se puede pulsar. Con el permiso pero en borrador (y con aprobación exigida), «Convertir a factura» no aparece: **el estado del documento manda además del permiso**. |

## 11. Selectores estables sugeridos (resumen)

| ID | Elemento | Selector |
|---|---|---|
| F-263 | Pestañas de la consola | `.gm-sheet__tabs a[mat-tab-link]` + `hasText: 'Personas'` / `'Roles y permisos'` / `'Integraciones'` / `'Auditoría'` / `'Resumen'` |
| F-264 | Aviso de pestaña denegada | `.console-denied` |
| F-265 | Buscador global | `.security-console__search input` (placeholder «Buscar persona, rol o permiso») |
| F-266 | Menú Nuevo | `getByRole('button', {name: 'Nuevo'})` → `.mat-mdc-menu-item` + texto |
| F-267 | Cifras del Resumen | `.gm-sheet-fig` + texto del rótulo; asuntos `.sec-ov__issue`; enlace `.sec-ov__link` «Ver bitácora» |
| F-268 | Personas | rail `.gm-rail-btn` + texto de vista; filas `.sec-people__row` + usuario; nombre `.sec-people__who`; panel `.sec-people__buttons`; bloque roles `.sec-people__role`; masivas `.sec-people__bulk` |
| F-269 | Roles | rail `.gm-rail-btn` + nombre del rol; cabecera `.sec-roles__h2`, `.sec-roles__actions`, `.sec-roles__chip`; subvistas `.sec-roles__views button` |
| F-270 | Editor | módulos `.rpe__module`; recurso `.rpe__resource` + nombre; acción `getByRole('button',{name:'Ver',exact:true})`; alcance `.rpe__scope-seg` → `'Propios'`/`'Todos'`; buscador `.rpe__search input`; barra de guardado `.gm-sheet-savebar`; aviso de solo lectura `.rpe__readonly` |
| F-271 | Integraciones | filas `.sec-api__row`; franja del secreto `.sec-api__secret`; panel `.sec-api__buttons` |
| F-272 | Auditoría | filtros `input[aria-label="Filtrar por persona"]`, `…por registro`, `…por IP`; filas `.sec-audit__row`; cambios `.sec-audit__change`; enlaces `.sec-audit__link` |
| F-273 | Diálogos | `mat-dialog-container` + `getByRole('button',{name:'Eliminar'|'Descartar cambios'|'Seguir editando'|'Rotar secreto'|'Desactivar'|'Aceptar'})`. Los campos de los diálogos se toman por `formcontrolname` (`name`, `lastName`, `email`, `username`, `password`, `confirmPassword`, `description`, `parentRole`, `integrationName`). |
| F-274 | Nota | Esta consola NO usa `app-dynamic-filters`: sus filtros son `input` nativos con `aria-label` o placeholder. Los de listas como Cotizaciones y Productos (`app-dynamic-filters`) no tienen `formcontrolname` y se toman por `mat-label`. |

---

## Dudas / INFERIDO

1. **Semántica de «Propios» y «Equipo»**: el front solo envía `scope` y no muestra nada. Que «Propios» filtre por `createdBy` (y «Equipo» por los miembros de los equipos del usuario) es INFERIDO; hay que confirmarlo en el API (`common/enum/permission-scope.enum.ts` y los servicios de cotizaciones).
2. **Filtro «Persona» de Auditoría**: se envía como `userName`, y «Ver su actividad» manda el `username`. No se confirmó si el API compara con el username o con el nombre visible que aparece en «Quién».
3. **`?q=` en la pestaña Roles**: el buscador global navega a `/security/roles?q=…`, pero `SecurityRolesComponent` no lee `q` (solo `rol` y `nuevo`). Se deduce que no filtra nada; hay que comprobarlo en vivo.
4. **Subvista «Personas» del rol sin USER_VIEW**: llama a `GET /user?roleId=`. Si el API responde 403, el componente muestra «Nadie tiene este rol todavía.» (el error se traga). INFERIDO que el API exige USER_VIEW.
5. **Página de permisos de credencial**: se desconoce qué permiso exige el API para `POST/DELETE /v1/integration-users/:id/permissions/:code` (supuestamente INTEGRATION_USER_EDIT).
6. **`routerLinkActive` de la documentación**: los enlaces apuntan a `/security/integration-user/docs/:slug` (redirección), así que probablemente el ítem activo nunca se resalta. Hay que verlo en pantalla.
7. **Cifras «Administradores» y «Cambios en 7 días»**: las calcula el API; no se revisó qué cuenta exactamente como «de seguridad» (`SECURITY_ENTITIES` en `security-overview.service.ts:37`).
8. **Tiempo de vida del secreto en pantalla**: la franja vive en memoria del componente; al cambiar de pestaña o recargar, desaparece para siempre. Se deduce de la señal `fresh`, no se probó.

## Posibles defectos

- **D-01 (grave): no se puede asignar ni quitar roles a una persona existente.** «+ Asignar rol» y «Editar» abren `UserFormComponent` en modo edición, que no muestra el selector de roles (`user-form.component.html:158` `@if (!isEditMode)`) y además borra `roles` del envío (`user-form.component.ts:317-319`). `UserService.addRole/deleteRole` existen (`user.service.ts:77-82`) pero, tras borrar `user-detail`, **no los llama nadie** (`grep` sin resultados). Solo se asignan roles al crear el usuario. Esto bloquea el video «asignar rol a una persona».
- **D-02: el menú lleva siempre a `/security/resumen`.** Un usuario con ROLE_VIEW o AUDIT_LOG_READ pero sin USER_VIEW entra por el menú y ve «No tiene permiso para ver «Resumen»» sin haber pedido nada.
- **D-03: el menú y las pestañas no están alineados.** La entrada del menú acepta `PERMISSION_VIEW` y `AUDIT_VIEW`, pero ninguna pestaña los usa (Roles pide ROLE_VIEW y Auditoría AUDIT_LOG_READ). Quien solo tiene esos permisos ve la entrada y llega a una consola sin pestañas.
- **D-04: Personas solo con TEAM_VIEW.** La pestaña se ofrece, pero la lista no carga (`loadUsers` sale si no hay USER_VIEW) y muestra «No se encontraron registros», que es engañoso.
- **D-05: «Editar permisos» de la credencial sin guard.** El botón está siempre visible y la página `/security/integration-user/:id/permissions` no tiene guard ni deshabilita las casillas sin INTEGRATION_USER_EDIT.
- **D-06: «Más acciones» de la persona.** Solo aparece con USER_EDIT o USER_DELETE, así que «Ver su actividad» (AUDIT_LOG_READ) queda inaccesible para un auditor sin permisos de edición.
- **D-07: el botón dice «Duplicar» y el diálogo «Clonar Rol»** (botón «Clonar»). El mensaje de éxito dice «clonado». Terminología inconsistente.
- **D-08: el asunto «nunca inició sesión» sugiere una acción que no existe.** Su texto dice «Reenvía la invitación o desactiva la cuenta.», pero no hay función de reenviar invitación en el front.
- **D-09: textos sin acento en la documentación de la API.** «Autenticacion», «Codigos y Respuestas», «Reintentar Envio DGII», «Aprobacion Comercial» y el botón móvil «Menu» (`api-docs-nav.data.ts:14, 26, 66, 120`; `api-docs-layout.component.html:5`).
- **D-10: mezcla de inglés y diseño viejo en la página de permisos de credencial.** Aparece «API Key Prefix:», el breadcrumb dice «Integraciones API» (la pestaña se llama «Integraciones») y usa tarjetas `mat-card` fuera del sistema `.gm-sheet`. «Volver a Integraciones» pierde la credencial abierta.
- **D-11: el buscador global promete «permiso» pero no busca permisos.** El placeholder dice «Buscar persona, rol o permiso», pero solo navega a Personas o a Roles, y Roles ignora `q` (duda 3).
- **D-12: `/security/role/:id` redirige a `roles` sin el id.** El comentario dice que la bitácora la enlaza; el rol no queda seleccionado (debería ser `roles?rol=:id`).
- **D-13: tres formas de avisar el éxito en la misma consola.** Los diálogos de alta y edición (usuario, equipo, rol) usan un diálogo con «Aceptar»; las acciones de la consola usan toasts «… exitosamente»; y la página de permisos de credencial no avisa nada al guardar.
- **D-14: errores sin detalle.** En la subvista Personas del rol y en el Historial el error de carga se traga y se ve el estado vacío («Nadie tiene este rol todavía.» / «No se encontraron registros»).
