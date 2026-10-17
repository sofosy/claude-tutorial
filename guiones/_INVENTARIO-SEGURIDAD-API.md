# Inventario API — módulo de Seguridad (serie de videos)

Autor-inventario (API) · 2026-09-27 · Germiva-api `master` @ `24cbb923f` («feat(security): permission
matrix, batch permission saves and security console endpoints (#1336)»).
Método: solo lectura de código + SELECT a la BD local `germiva` (root sin clave, 127.0.0.1:3306).
No se arrancó ninguna app. Rutas relativas a `Germiva-api/src/` salvo que se indique otra cosa.
Prefijo global de rutas: `/api` (`main.ts:132`), puerto local `3001` (`.env` `APP_PORT`).

Documento de QA del propio PR: `Germiva-api/docs/qa/QA-SEGURIDAD.md` (arnés `tests/qa/seguridad/*.mjs`,
42/42 casos API en verde según el PR; no re-ejecutado aquí).

---

## 1. Modelo de datos

### Roles

- **A-001 · Tabla `roles`** (`admin/role/entities/role.entity.ts:13-123`), `@SharedCatalog()`: campos
  `name`, `description`, `can_edit`, `can_delete`, `code`, `is_admin_role`, `is_integration_role`,
  `integration_user_id`, `parent_role_id`; `company_id` viene de `CommonField`.
- **A-002 · Rol de empresa vs rol del sistema**: `company_id IS NULL` = catálogo global del sistema
  (Admin, Cajero, Contador…); `company_id = N` = rol propio de la empresa. `role.service.ts:547-555`
  (`assertRoleWritable`) bloquea toda escritura sobre un rol global desde una empresa cliente con **403**:
  `«<nombre>» es un rol del catálogo del sistema y no se puede modificar. Clónalo para tener una copia propia de tu empresa y ajústala ahí.`
  Solo la empresa principal (`isCurrentCompanyMain`) puede editarlos. En listados se marcan
  `canEdit=false/canDelete=false` (`role.service.ts:299-323`). La matriz expone `isSystemRole` y
  `editable` (`permission-matrix/role-permission-matrix.service.ts:116-120`).
- **A-003 · Visibilidad de roles por empresa**: `findOne` acota a `company_id = actual OR IS NULL`
  (`role.service.ts:495-535`); si no se ve → **404** `El rol con ID <id> no está disponible` (línea 519).
  `findAll` (`role.service.ts:206-291`) oculta: roles de integración, roles clínicos (instancia ERP),
  el rol Referidor, roles cuyos permisos caen 100 % fuera del plan (`findRoleIdsOutOfPlan`, 397-453) y la
  plantilla global cuando la empresa ya tiene un clon con el mismo `code`. Adjunta `permissionCount`
  (336-355) y **`holderCount`** = personas de la empresa con ese rol (362-383, nuevo en #1336).
- **A-004 · Crear / clonar**: el rol creado desde una empresa se guarda con `company_id` de la sesión
  (`role.service.ts:110-139`). Nombre único por empresa sin distinguir mayúsculas → **400**
  `Ya existe un rol con este nombre en la empresa` (línea 105). `POST /role/:id/clone` copia permisos
  DIRECTOS (con alcance), padre y exclusiones; `isAdminRole=false` siempre (146-204).

### Herencia

- **A-005 · Modelo**: un solo padre por rol (`roles.parent_role_id`, cadena simple). Fórmula
  documentada en `admin/role/role-inheritance.helper.ts:9-24`:
  `efectivo(rol) = DIRECT(rol) ∪ (efectivo(padre) − exclusiones(rol))`.
  Se **materializa** en `role_permissions` con `source = INHERITED` (enum
  `common/enum/role-permission-source.enum.ts`), así el guard lee una tabla plana sin recursión.
- **A-006 · Recálculo**: `recomputeInheritedPermissions` (`role-inheritance.helper.ts:144-247`) borra /
  inserta / actualiza las filas INHERITED según el padre, respeta exclusiones, DIRECT propios e
  `isAdminOnly` (un hijo no admin no hereda permisos exclusivos de admin, línea 191), **copia el alcance
  del padre** (192) y baja recursivamente a los hijos (235-246).
- **A-007 · Profundidad y ciclos**: `MAX_INHERITANCE_DEPTH = 10` (línea 27). Mensajes (todos **400**):
  - `Un rol no puede heredar de sí mismo` (79)
  - `El rol padre con ID <id> no está disponible` (87)
  - `No se puede heredar de un rol de integración` (92)
  - `El rol padre debe pertenecer a la misma empresa` (100) — un padre global sí está permitido
  - `No se puede asignar este rol padre: crearía un ciclo de herencia` (108)
  - `La cadena de herencia superaría el máximo de 10 niveles` (113)
  - `La cadena de herencia de roles contiene un ciclo` / `…supera el máximo de 10 niveles` (52, 58; solo con BD corrupta)
- **A-008 · Exclusiones**: tabla `role_permission_exclusions` (`admin/role/entities/role-permission-exclusion.entity.ts`),
  única por (rol, permiso). Solo afecta a lo heredado; nunca a DIRECT. Reglas del editor
  (`permission-matrix/role-permission-changes.service.ts:47-60`): conceder uno excluido = quitar la
  exclusión (vuelve a heredarse con el alcance del padre); quitar uno heredado = crear exclusión; cambiar
  el alcance de uno heredado lo convierte en DIRECT. Estados que ve la UI: `DIRECT · INHERITED · EXCLUDED · NONE`
  (`permission-matrix.interface.ts:10-14`).
- **A-009 · Borrar un rol padre**: **422** `No se puede eliminar el rol porque otros roles heredan de él: <nombres>`
  (`role.service.ts:885-895`).

### Permisos

- **A-010 · Tabla `permission`** (`admin/permission/entities/permission.entity.ts`): `code` único (enum
  `common/enum/permission.enum.ts`), `name` (español), `description`, `isAdminOnly`, `supports_scope`.
  Relación m2m con módulos (`module_permissions`). BD local: **1 420 permisos, 211 con `supports_scope=1`**.
- **A-011 · Recurso / acción NO son columnas**: se derivan del código en el API
  (`permission-matrix/permission-resource.parser.ts`, decisión D2 del QA): sufijo de acción conocido
  (`_VIEW`, `_CREATE`, `_UPDATE`, `_DELETE`…) y recurso = prefijo común; nombre visible del recurso = el del
  permiso «Ver …»; acciones no estándar (p. ej. `INVOICE_CHANGE_STATUS`) usan el nombre del permiso.
- **A-012 · Secciones del editor** (`permission-matrix/permission-matrix-sections.ts`): «Administración y
  control» (GENERAL, COMPANY, USERS, SECURITY, MULTI_COMPANY, API_ACCESS…), «Ventas y facturación» (PARTNERS,
  SALES, INVOICING, ECF, POS, CRM), «Compras e inventario» (PURCHASES, PRODUCTS, INVENTORY, INVENTORY_ADVANCED),
  «Contabilidad», «Nómina y RR. HH.», «Reportes», «Inteligencia artificial», «Salud», «Otros». Submódulo sin
  entrada cae en la sección del padre (SALES_QUOTE → Ventas y facturación).
- **A-013 · Qué se ofrece**: solo módulos contratados (`role-permission-matrix.service.ts:171-226`), sin
  `isAdminOnly` en roles no admin, sin clínicos en ERP (96-101). La empresa principal ve además el
  módulo virtual «Sin módulo».

### Alcance (Propios / Equipo / Todos)

- **A-014 · Dónde se guarda**: `role_permissions.scope` enum `ALL | TEAM | OWN`
  (`admin/role-permission/entities/role-permission.entity.ts:40-45`; enum `common/enum/permission-scope.enum.ts`).
  Etiquetas en la bitácora: `Todos / Equipo / Propios` (`role-permission-changes.service.ts:41-45`).
  Si el permiso no tiene `supportsScope`, el guardado en lote lo fuerza a `ALL` (175-185).
- **A-015 · Cómo se resuelve**: `PermissionGuard` (`admin/auth/guards/permission.guard.ts:61-73`) toma el
  alcance MÁS permisivo entre los permisos que exige el endpoint y que el usuario tiene
  (`getEffectivePermissionScope`, `admin/auth/has-access.ts:175-189`; prioridad ALL > TEAM > OWN, 123-127) y,
  si no es ALL, deja en el contexto `ownershipFilter = { scope, userId }`. Para TEAM,
  `OwnershipFilterInterceptor` (`common/interceptors/ownership-filter.interceptor.ts`) añade los ids de
  quienes comparten equipo (`admin/team/services/team-membership-resolver.service.ts:16-30`, incluye al propio usuario).
- **A-016 · Dónde se APLICA de verdad** (siempre por la columna `created_by_user_id` de `CommonField`,
  `common/entities/common-field.entity.ts:64-68`; **nunca** por vendedor/`sellerId`):
  1. **Listados que usan `paginate()`**: `common/pagination/pagination.ts:220-245` añade
     `created_by_user_id = :userId` (OWN) o `IN (:...teamUserIds)` (TEAM). Excepción explícita con
     `skipOwnershipFilter: true` en form-template, employee (1494) y payroll-record (218).
  2. **Mutaciones con entidad** (`save/remove/softRemove`): `subscribers/ownership-validation.subscriber.ts`.
  3. **Mutaciones por id** (`Repository.update/delete/softDelete` parcheados):
     `common/services/ownership-repository-patcher.service.ts:80-157`. Mensajes **403** exactos (219-257):
     `No tienes permiso para actualizar|eliminar registros creados por otros usuarios.` (OWN) ·
     `No tienes permiso para actualizar|eliminar registros fuera de tu equipo.` (TEAM) ·
     `No tienes permiso para actualizar|eliminar un registro sin propietario asignado.` (propietario NULL).
     Si el criterio no es por id, solo deja un warning y NO filtra (145-150).
- **A-017 · Límite práctico decisivo para el video**: el filtro solo se activa con el alcance del permiso
  que **exige el endpoint**. Los permisos con `supports_scope=1` son casi todos los de «Ver» (`*_VIEW`); los
  de crear/editar/eliminar/aprobar tienen `supports_scope=0` y quedan en ALL. Resultado: **«Propios»
  recorta LISTADOS** (endpoints con `*_VIEW` que usan `paginate`). El **detalle por número/id** no se filtra
  (p. ej. `invoices.service.ts:530-606`, `findOne` por `invoiceNumber + company` sin `created_by`), y las
  ediciones pasan por `*_UPDATE` (ALL). No afirmar en el video que «solo puede abrir/editar lo suyo».

### Filtros por estado del documento

- **A-018 · NO EXISTEN en el API.** No hay columna, tabla, DTO ni lógica que asocie a un rol/permiso un
  conjunto de estados de documento (búsqueda en `admin/role`, `admin/permission`, `admin/role-permission`,
  `admin/team`, migraciones y DTO de la matriz: `permission-matrix.interface.ts:16-24` solo lleva
  `state` de concesión y `scope`). Lo único «de estado» son permisos de ACCIÓN: `INVOICE_CHANGE_STATUS`
  («Estado Facturas Socios»), `QUOTE_APPROVE/REJECT/ACCEPT/SETTLE`, `QUOTE_STATUS_*` (catálogo de estados).
  **El video no puede afirmar «filtros por estado»**.

### Equipos

- **A-019 · Tablas**: `teams` (`admin/team/entities/team.entity.ts`, nombre, descripción ≤500, activo,
  empresa) y `team_members` (`team-member.entity.ts`, único por equipo+usuario, con `company_id`).
- **A-020 · Un equipo NO da permisos.** Solo sirve para el alcance TEAM (A-015) y para filtrar
  personas (`/user?teamId=`). El acceso efectivo no suma nada por equipo.
- **A-021 · Endpoints** `v1/team` (`admin/team/team.controller.ts:23-81`): `POST` TEAM_CREATE · `GET`,
  `GET :id`, `GET :id/members` TEAM_VIEW · `PATCH :id` TEAM_EDIT · `DELETE :id` TEAM_DELETE ·
  `POST|DELETE :id/members` TEAM_MANAGE_MEMBERS. Empresa 43: **0 equipos**.

### Acceso efectivo

- **A-022 · Cálculo en el guard**: `hasAccess` (`admin/auth/has-access.ts:15-45`) = EXISTS sobre
  `user_company_roles` (empresa de la sesión) → `role_permissions` (DIRECT + INHERITED ya materializados)
  → `permission`. Es decir **rol(es) de la persona en esa empresa + herencia**; nada por equipo. Lee la BD
  en cada petición (sin caché) → quitar un permiso corta el acceso al instante.
- **A-023 · Plan**: además, `assertWithinPlan` (`permission.guard.ts:97-123`) rechaza si NINGUNO de los
  permisos exigidos está en un módulo contratado: **403**
  `{ code: 'MODULE_NOT_IN_PLAN', message: 'Su plan no incluye este módulo. Actualice su suscripción para acceder a esta funcionalidad.', permissions: [...] }`.
- **A-024 · Panel de persona**: `GET /v1/security/users/:id/access` (`admin/security-overview/person-access.service.ts:42-84`):
  roles de la empresa (con padre y si es de sistema), equipos, unión de permisos por módulo contratado
  (`granted/total`), total `granted/available` y **últimos 3 ingresos** con IP y user agent (169-191).

### Usuarios / personas e ingresos

- **A-025 · Personas** = `users` con `userType = NORMAL` unidos por `user_companies` a la empresa, sin
  referidores (`security-overview.service.ts:395-416`, mismo criterio que `/user`). Roles por empresa en
  `user_company_roles`.
- **A-026 · Historial de ingresos = bitácora**, no hay tabla de login history. Cada login exitoso deja
  `audit_logs` con `action='AUTH'`, `event='LOGIN_SUCCESS'`, `entity_name='auth'`, `company_id`, `user_id`
  (`admin/auth/auth.service.ts:205-211`, `recordAuthEvent` 119-144, síncrono). Helper y SQL:
  `admin/user/helpers/login-activity.helper.ts:16-62`. `users.login_date` NO es último acceso (es la marca
  de invalidación de tokens; hallazgo H5 del PR). Índice `IDX_audit_logs_company_user (company_id, user_id, created_at)`
  existe en la BD local. Límite: retención de la bitácora (24 meses por defecto).
- **A-027 · Listado de personas** `GET /user` (USER_VIEW, `admin/user/user.controller.ts:42-46`), filtros
  (`admin/user/dto/filter.dto.ts`): `username`, `includeDeleted`, `emailVerified`, **`roleId`** (titulares de
  un rol), `withoutRole`, **`neverLoggedIn`**, **`teamId`** (400 `El campo teamId debe ser un número entero`),
  `active`. Cada fila trae `lastAccessAt` y `teams` (transitorios, `user.service.ts:404-487`).

---

## 2. Endpoints de la consola de Seguridad

Todos usan `@RequirePermissions(...)` = `JwtAuthGuard + EmailVerificationGuard + PermissionGuard + GlobalSubscriptionGuard`
(`admin/auth/decorators/require.permissions.decoractor.ts:10-17`). Sin token → **401**
`{"message":"Unauthorized","statusCode":401}` (passport por defecto). Sin permiso → **403** con el formato
de A-052.

### Resumen

- **A-028 · `GET /api/v1/security/overview`** — USER_VIEW (`admin/security-overview/security-overview.controller.ts:19-32`).
  Respuesta `{ totals, attention, recentActivity }` (`interfaces/security-overview.interface.ts`).
  Cifras (`security-overview.service.ts:90-186`):
  `peopleWithAccess`, `admins` (tienen un rol `is_admin_role`), `withoutRole`, `activePeople`,
  `inactivePeople`, `neverLoggedIn` (sin `AUTH/LOGIN_SUCCESS` en la empresa), `activeLast30Days`,
  `roles` (= total del listado de roles), `apiCredentials` (integraciones activas), `staleApiCredentials`,
  `changesLast7Days` (bitácora sin eventos AUTH) y `securityChangesLast7Days` (de ellos, entidades
  `users, roles, role_permissions, role_permission_exclusions, user_company_roles, user_companies, teams, team_members`, línea 37-46).
- **A-029 · «Requiere atención»** (en serie, 190-301), cada ítem con `kind, count, title, detail, meta, ids(≤20)`:
  | kind | Regla | Título | Meta |
  |---|---|---|---|
  | `USERS_WITHOUT_ROLE` | persona sin fila en `user_company_roles` de la empresa | `N personas sin ningún rol` / `1 persona sin ningún rol` | `Inician sesión pero no ven ningún módulo.` |
  | `STALE_API_CREDENTIAL` | credencial activa sin llamada en 60 días (o nunca llamó y tiene >60 días) (25, 384-386) | `N credenciales de API sin uso` | `Sin llamadas en 60 días. Revócala si ya no se usa.` |
  | `NEVER_LOGGED_IN` | activa, creada hace >30 días, sin ningún login en la empresa (27, 254-282) | `N personas nunca iniciaron sesión` | `Reenvía la invitación o desactiva la cuenta.` |
  | `EMPTY_ROLE` | rol sin ninguna fila en `role_permissions` que alguien de la empresa tiene asignado (307-327) | `N roles sin permisos` | `Asignarlos no da acceso a nada.` |
  `detail` = hasta 3 nombres separados por « · » y `y N más` (469-480).
- **A-030 · Actividad reciente**: últimos 10 eventos de la bitácora de la empresa (incluye los AUTH) con
  `entityLabel` en español (`audit/audit-entity-labels.ts`) (331-358).

### Roles

`admin/role/role.controller.ts` (controlador `role`, **sin `v1`**, `@SkipSubscriptionValidation`):

- **A-031 · CRUD**
  | Método y ruta | Permiso | Línea | Validaciones / errores exactos |
  |---|---|---|---|
  | `POST /api/role` | ROLE_CREATE | 38-42 | `name` obligatorio (`validation.isNotEmpty`, i18n); nombre repetido → 400 `Ya existe un rol con este nombre en la empresa`; padre inválido → mensajes de A-007. Body: `name, description?, isAdminRole?, canDelete?, parentRole?` (`dto/create-role.dto.ts`) |
  | `POST /api/role/:id/clone` | ROLE_CREATE | 44-48 | body `{name, description?}` (`dto/clone-role.dto.ts`) |
  | `GET /api/role` | ROLE_VIEW | 50-54 | filtro `name`, paginado; trae `permissionCount`, `holderCount`, `parentRole` |
  | `GET /api/role/:id` | ROLE_VIEW | 56-60 | 404 `El rol con ID <id> no está disponible` |
  | `PATCH /api/role/:id` | ROLE_EDIT | 62-66 | rol global → 403 (A-002); `canEdit=false` → 422 `No se puede actualizar el rol con ID <id>`; quitar admin → 422 `No se puede remover el estado de rol administrativo` (`role.service.ts:578-654`) |
  | `DELETE /api/role/:id` | ROLE_DELETE | 122-126 | 422 `No se puede eliminar el rol con ID <id>` (canEdit=false) · 422 `Este rol no puede ser eliminado. Puede editar sus permisos pero no eliminarlo.` · 422 herencia (A-009). Soft delete (`role.service.ts:863-899`) |
- **A-032 · `GET /api/role/:id/permission-matrix`** — ROLE_VIEW (68-81). Devuelve `role` (id, name,
  isAdminRole, isSystemRole, parentRole, `editable`, `holders`), `totals` (granted, available, inherited,
  excluded) y `sections → modules (granted/total) → resources → actions {permissionId, code, label, state, scope, supportsScope}`.
  `ParseIntPipe` → id no numérico 400.
- **A-033 · `PATCH /api/role/:id/permissions`** — ROLE_EDIT (83-96). Body (`dto/update-role-permissions.dto.ts`):
  `{ grant?: [{permissionId, scope?}], revoke?: [permissionId], rescope?: [{permissionId, scope}] }`, tope 2 000
  por lista. Una sola transacción, devuelve la matriz actualizada (`role-permission-changes.service.ts:73-104`).
  Errores exactos (400 salvo indicación):
  - `El campo permissionId es requerido` · `El campo permissionId debe ser un número entero` · `El alcance debe ser ALL, TEAM u OWN` · `El campo scope es requerido` · `El campo grant|revoke|rescope debe ser una lista` · `Cada permiso de revoke debe ser un número entero` · `Demasiados cambios en un solo guardado` (DTO)
  - `El permiso <id> no puede concederse y quitarse en el mismo guardado` (119-121)
  - `Los siguientes permisos no existen: <ids>` (150-152)
  - `Este rol no puede recibir los permisos: <nombres>` (admin-only en rol no admin / clínicos en ERP, 162-164)
  - `Los siguientes permisos pertenecen a módulos que su plan no incluye: <códigos>.` (`role.service.ts:756-760`)
  - `El permiso «<nombre>» no admite alcance` (205) · `El permiso «<nombre>» no está concedido a este rol` (210)
  - Rol del sistema → 403 (A-002) · rol de otra empresa → 404.
  - Guardado vacío → 200 sin escribir (92-94).
- **A-034 · Endpoints antiguos conservados** (FE ya no los usa, D7): `PATCH /api/role/add-permission/:role`
  (`{permissions:[ids], scope?}`), `PATCH /api/role/delete-permission/:role`, `PATCH /api/role/update-permission-scope/:role`
  (`{permissionId, scope}`; 404 `El permiso con ID <p> no está asignado al rol con ID <r>`), todos ROLE_EDIT
  (98-120). **No** generan el evento `PERMISSIONS_CHANGED` (ver A-052).
- **A-035 · Titulares del rol**: no hay endpoint propio; se usa `GET /api/user?roleId=<id>` (USER_VIEW) y
  el conteo `holderCount`/`holders`.
- **A-036 · Historial del rol**: no hay endpoint propio; `GET /api/v1/audit-logs/entity/roles/<id>`
  (AUDIT_LOG_READ, coincidencia exacta) o `GET /api/v1/audit-logs?entityName=roles&entityId=<id>` (ojo A-064).
- **A-037 · Catálogo de permisos** `GET /api/permission` — ROLE_VIEW (`admin/permission/permission.controller.ts:15-19`);
  `GET /api/permission/enum` sin guard pero solo en `NODE_ENV=local` (21-30).

### Personas y acciones sobre personas

- **A-038 · Endpoints** (`admin/user/user.controller.ts`): `POST /api/user` USER_CREATE (35-40; body
  `username, email, password?, name, lastName, active?, whatsappPhone?, roles?[]`) · `GET /api/user` USER_VIEW
  (42-46) · `GET /api/user/one/:id` USER_VIEW · `PATCH /api/user/:id` USER_EDIT (78-88; activar/desactivar va
  por aquí con `active`) · `PATCH /api/user/add-role/:user` y `delete-role/:user` USER_EDIT (96-114) ·
  `DELETE /api/user/:id` USER_DELETE · `POST /api/user/:id/restore` USER_CREATE.
  Roles por empresa: `v1/users/:userId/companies/:companyId/roles` y `v1/users/:userId/current-company/roles`
  (GET USER_VIEW; POST/PUT/DELETE USER_EDIT) (`admin/user-company-role/user-company-role.controller.ts`).
- **A-039 · Reglas de asignación de roles** (`admin/user-company-role/role-assignment.policy.ts:33-50`), mensajes exactos:
  `No tienes permiso para asignar roles. Pide a un administrador de Seguridad que lo haga.` ·
  `Uno o más roles no pertenecen a esta empresa.` ·
  `No puedes cambiar tus propios roles. Pide a otro administrador que lo haga.` ·
  `No puedes asignar el rol «<rol>»: incluye permisos que tú no tienes.` ·
  en `user.service.ts`: `No se puede remover el rol administrativo del último administrador de la empresa. Debe haber al menos un administrador por empresa.` (1170) ·
  `No se puede remover el último rol del usuario. El usuario debe mantener al menos un rol en la empresa.` (1214).
- **A-040 · Acciones masivas**: **no hay endpoint masivo** en el API (sin `bulk` en `admin/user`). Si la UI
  ofrece acciones sobre varias personas, las hace una a una. (INFERIDO: no se revisó el FE.)

### Credenciales de API (Integraciones)

`admin/integration-user/integration-user.controller.ts` → `/api/v1/integration-users`:

- **A-041 · Endpoints**
  | Método y ruta | Permiso | Línea |
  |---|---|---|
  | `GET available-permissions` | INTEGRATION_USER_VIEW | 47-62 (no admin-only, recortado al plan) |
  | `POST /` | INTEGRATION_USER_CREATE | 66-87 |
  | `GET /`, `GET :id` | INTEGRATION_USER_VIEW | 89-128 |
  | `PATCH :id` | INTEGRATION_USER_EDIT | 130-160 (no toca credenciales) |
  | `POST :id/regenerate-credentials` | INTEGRATION_USER_EDIT + `@BlockDuringImpersonation` | 162-193 |
  | `PATCH :id/activate` · `PATCH :id/deactivate` | INTEGRATION_USER_EDIT | 195-248 |
  | `DELETE :id` (204, soft delete) | INTEGRATION_USER_DELETE | 250-273 |
  | `GET :id/summary` | INTEGRATION_USER_VIEW | 277-290 (nuevo en #1336) |
  | `GET :id/permissions` | INTEGRATION_USER_VIEW | 292-316 |
  | `POST :id/permissions/:code` · `DELETE :id/permissions/:code` | INTEGRATION_USER_EDIT | 318-382 |
  | `PUT :id/permissions` body `{permissionCodes:[...]}` | INTEGRATION_USER_EDIT | 384-414 |
  Credencial de otra empresa → **404** `Usuario de integración no encontrado` (`integration-user.service.ts:732`).
- **A-042 · Creación y secreto** (`integration-user.service.ts:54-167`, `utils/api-key-generator.util.ts`):
  body `integrationName` (obligatorio, ≤100: `El nombre de la integración es requerido` / `El nombre no puede exceder 100 caracteres`),
  `integrationDescription?` (≤500), `allowedIps?` (IPv4, ≤20: `Cada IP debe ser una dirección IPv4 válida`),
  `allowedEndpoints?` (≤50) (`dto/create-integration-user.dto.ts`).
  API Key `gv_live_<32 hex>`; prefijo visible `gv_live_<8 hex>`; secreto = 48 hex.
  **Se guardan hasheados con SHA-256** (`apiKey`, `apiSecret` = hash; comparación en tiempo constante,
  util 75-93) y además el secreto con **bcrypt** como `password`. La respuesta trae
  `credentials.apiKey`, `credentials.apiSecret`, `apiKeyPrefix` y `message`:
  `IMPORTANTE: Guarde estas credenciales de forma segura. El API Secret NO se puede recuperar después de cerrar esta ventana.` (155-156).
  La credencial es un `users` con `userType=INTEGRATION`, correo `<username>@integration.internal`, y recibe el
  rol global plantilla `INTEGRATOR_DEFAULT` (id 9 en local) en la empresa.
- **A-043 · Permisos por módulo de la credencial**: al PRIMER cambio se crea un rol propio
  `Integración · <nombre>` (`is_integration_role=1`, `integration_user_id`, de la empresa) copiando la
  plantilla recortada al plan y sustituyendo la asignación (`ensureOwnRole`, 553-600; corrige H0 CRÍTICO).
  Validaciones (479-519, 400): `Permisos no encontrados: <códigos>` ·
  `Estos permisos están reservados para administradores: <nombres>` ·
  `Los siguientes permisos pertenecen a módulos que su plan no incluye: <códigos>.`
  La plantilla `INTEGRATOR_DEFAULT` en local concede: `ECF_APPROVAL_RECEIPT, ECF_VIEW, INVOICE_CREATE, INVOICE_VIEW, PURCHASE_INVOICE_CREATE` (**no** `PRODUCT_VIEW`).
- **A-044 · Resumen / actividad 7 días** (`integration-user-summary.service.ts`): `roleId`, `isOwnRole`,
  `permissions` (total), `modules [{name, granted, total, detail «Recurso: Ver, Crear · … y N más»}]` y
  `activity` = 7 días (fecha RD) con el **nº de eventos de la bitácora** hechos por la credencial. El API
  NO guarda llamadas por día (solo `api_call_count` y `last_api_call`): las lecturas no cuentan.
- **A-045 · Rotación y revocación**: `regenerate-credentials` genera key+secret nuevos, invalida los
  anteriores y los JWT (`loginDate = now`); mensaje `Las credenciales anteriores han sido invalidadas. Guarde estas nuevas credenciales de forma segura.` (301-336).
  `deactivate` pone `active=false` e invalida tokens; `activate` lo revierte (338-364). `DELETE` borra la
  asignación de rol, invalida la caché y hace soft delete (366-376).

### Documentación de la API

- **A-046 · Swagger**: UI en `http://localhost:3001/docs` (sin `/api`), JSON en `/api-json`, YAML en `/api-yaml`,
  **solo con `NODE_ENV=local`** (`main.ts:222-260`). Título genérico «API BASE».
- **A-047 · Documentación de producto**: la vista del front `security/api-docs` sirve markdown estático de
  `germiva-website/src/assets/docs/api/endpoints/` (00 códigos y respuestas, 01 autenticación, 02-19 facturas
  emitidas/recibidas, anular, estado de suscripción, reportes IT-1). No hay endpoint de docs en el API.

### Auditoría

- **A-048 · `GET /api/v1/audit-logs`** — AUDIT_LOG_READ (`audit/audit-log.controller.ts:14-21`). Filtros
  (`audit/dto/filter-audit-log.dto.ts`): `entityName` (LIKE por palabras), `entityId`, `action`
  (`CREATE, UPDATE, DELETE, STATUS_CHANGE, ACCESS, AUTH, ACTION, EXPORT, PRINT`), **`actions`** (varias, coma),
  **`ipAddress`**, `userId`, `userName`, `dateFrom`, `dateTo` + paginación. Errores 400:
  `La acción no es válida` · `Una de las acciones no es válida` · `El campo ipAddress debe ser una dirección IP válida` ·
  `El campo entityId debe ser un número entero` · `El campo userId debe ser un número entero`.
  Fechas `YYYY-MM-DD` = día completo en hora RD (UTC-4) (`audit/audit-log.service.ts:15-29, 159-171`).
  Siempre acotado a la empresa de la sesión (113-117). Cada fila añade `entityLabel` en español.
- **A-049 · Historial de un registro**: `GET /api/v1/audit-logs/entity/:entityName/:entityId` — AUDIT_LOG_READ
  (23-43), coincidencia exacta, más reciente primero, acotado a la empresa (`audit-log.service.ts:79-99`).
  Existe además `GET /api/audit`, `/api/audit/detail`, `/api/audit/audit-table` con AUDIT_VIEW (`audit/audit.controller.ts`, sistema anterior).
- **A-050 · Qué guarda cada evento** (`audit/entities/audit-log.entity.ts`): `company_id, entity_name, entity_id,
  action, event, changes {campo: {oldValue, newValue}} (antes/después), user_id, user_name (snapshot), ip_address,
  user_agent, request_id, metadata`. **Origen**: IP y user agent del contexto de la petición
  (`audit-buffer.service.ts:114-117`). **Credencial**: no hay columna propia; la credencial aparece como
  `user_id`/`user_name` del usuario de integración (`integration_gv_live_xxxxxxxx`).
  **Agrupación**: no hay endpoint que agrupe; la correlación es `request_id` («agrupa todos los eventos de
  un mismo request HTTP»). Tabla particionada por mes, append-only.

---

## 3. Autenticación de una credencial de API y respuesta a lo NO permitido

- **A-051 · Dos vías**:
  1. **Cabeceras** `x-api-key: gv_live_…` + `x-api-secret: <48 hex>` — SOLO en endpoints con
     `@RequirePermissionsOrApi` (`admin/auth/decorators/require-permissions-or-api.decorator.ts`,
     `CombinedAuthGuard` jwt→integration). Hoy solo tres controladores:
     `v1/integration/invoices/outbound`, `…/inbound` y `integration-subscription`
     (`modules/integration/controllers/*`). Errores 401 (`admin/auth/strategies/integration.strategy.ts:35-72`):
     `Se requieren los headers x-api-key y x-api-secret para autenticación de integración` ·
     `Credenciales de integración inválidas` · `IP <ip> no autorizada para esta integración` ·
     `Endpoint <ruta> no autorizado para esta integración`.
  2. **Token**: `POST /api/auth/integration/login` body `{apiKey, apiSecret}` (throttle 30/min,
     `admin/auth/auth.controller.ts:231-236`) → `{ token, user, expiresAt }` (JWT de 24 h,
     `auth.service.ts:559-609`). Con `Authorization: Bearer <token>` sirve en **cualquier** endpoint
     `@RequirePermissions` (la `JwtStrategy` acepta `userType=INTEGRATION`, `jwt.strategy.ts:114-121`).
  Con cabeceras en un endpoint solo-JWT (p. ej. `/api/v1/product`) la respuesta es **401**
  `{"message":"Unauthorized","statusCode":401}` — no confundir con «sin permiso».
- **A-052 · Respuesta cuando NO tiene el permiso**: **403**, cuerpo tal cual lo arma
  `admin/auth/exceptions/missing-permission.exception.ts:9-33` (el filtro global lo devuelve sin cambios,
  `common/filters/http-exception.filter.ts`):
  ```json
  {"statusCode":403,"error":"Forbidden",
   "message":"No tienes el permiso requerido para acceder a este recurso: \"Productos\" (PRODUCT_VIEW). Solicita acceso a tu administrador.",
   "missingPermissions":[{"code":"PRODUCT_VIEW","name":"Productos","description":"…"}]}
  ```
  Con varios permisos alternativos: `No tienes los permisos requeridos para acceder a este recurso. Necesitas alguno de los siguientes: "…" (…), "…" (…). Solicita acceso a tu administrador.`
  El nombre sale de `permission.name` en la BD.
- **A-053 · Ejemplo grabable (empresa 43, credencial recién creada con la plantilla)**:
  ```bash
  # 0) Crear la credencial (como admin.progreso) — el secreto sale UNA vez
  curl -s -X POST http://localhost:3001/api/v1/integration-users \
    -H "Authorization: Bearer $TOKEN_ADMIN" -H "Content-Type: application/json" \
    -d '{"integrationName":"Tienda en línea"}'
  # 1) PERMITIDA — listar facturas emitidas por cabeceras (plantilla trae INVOICE_VIEW) → 200
  curl -s http://localhost:3001/api/v1/integration/invoices/outbound \
    -H "x-api-key: gv_live_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" -H "x-api-secret: YYYYYYYY…"
  # 2) Token para endpoints normales
  TOKEN=$(curl -s -X POST http://localhost:3001/api/auth/integration/login \
    -H "Content-Type: application/json" -d '{"apiKey":"gv_live_…","apiSecret":"…"}' | jq -r .token)
  # 3) DENEGADA — listar productos (sin PRODUCT_VIEW) → 403 "Productos" (PRODUCT_VIEW)
  curl -s http://localhost:3001/api/v1/product -H "Authorization: Bearer $TOKEN"
  # 4) Conceder desde Integraciones (o POST …/integration-users/<id>/permissions/PRODUCT_VIEW) y repetir 3) → 200
  ```
  Alternativa «al revés» (facturas denegadas): quitar `INVOICE_VIEW` a la credencial y repetir 1) → 403 con
  el nombre **«Facturas Socios»** (`permission.name` de `INVOICE_VIEW`, id 263): feo para cámara (ver A-072).
  Plan 15 de la 43 incluye INVOICING y PRODUCTS, así que no salta `MODULE_NOT_IN_PLAN`.
  La tabla `integration-users` exige que la credencial sea del mismo `company` que el token del admin.

---

## 4. Permisos de Ventas e Inventario para los ejemplos

- **A-054 · Códigos (BD local)**:
  | Recurso | Ver | Crear | Editar | Eliminar | Anular / estado | Aprobar | Exportar |
  |---|---|---|---|---|---|---|---|
  | Cotizaciones (SALES_QUOTE) | `QUOTE_VIEW` (210, **scope**) | `QUOTE_CREATE` 211 | `QUOTE_UPDATE` 212 (también cancelar/expirar/cambiar estado) | `QUOTE_DELETE` 213 (**sin endpoint** en `modules/quote/quote.controller.ts`) | `QUOTE_UPDATE` (`PATCH /cancel/:n`) | `QUOTE_APPROVE` 221 / `QUOTE_REJECT` 222 / `QUOTE_ACCEPT` | — (no existe) |
  | Facturas de venta (INVOICING) | `INVOICE_VIEW` 263 «Facturas Socios» (**scope**) | `INVOICE_CREATE` 264 | `INVOICE_UPDATE` 265 (borradores; también borrar borrador) | vía `DELETE /v1/invoices/:n` (INVOICE_UPDATE, solo borrador) | `INVOICE_CHANGE_STATUS` 266 (`PATCH /v1/invoices/change-status/:n`) | — | — (no existe) |
  | Productos (PRODUCTS) | `PRODUCT_VIEW` 36 (**scope**) | `PRODUCT_CREATE` 37 | `PRODUCT_UPDATE` 38 | `PRODUCT_DELETE` 39 | activar/inactivar = `PRODUCT_UPDATE` (`PATCH /:id/active`) | — | `PRODUCT_EXPORT` 41 (`GET /v1/product/bulk/export/:format`), `PRODUCT_IMPORT` 40 |
  Rutas: `v1/quotes` (`quote.controller.ts:54-475`), `v1/invoices` (`modules/invoices/invoices.controller.ts:83-1110`;
  listado de ventas `GET /v1/invoices/sales` 242-250), `v1/product` (`modules/product/product.controller.ts:61-1390`),
  existencias `v1/product/:id/inventory*` con `INVENTORY_*`.
- **A-055 · Alcance «Propios» — qué lo respeta DE VERDAD**:
  - `GET /v1/quotes` (QUOTE_VIEW → `quote.service.ts:38-127` usa `paginate`) → **filtra por quien la creó**. ✔
  - `GET /v1/invoices/sales` (INVOICE_VIEW → `invoices.service.ts:224-499` `paginate`) → **filtra por creador**. ✔
  - `GET /v1/product` (PRODUCT_VIEW → `product.service.ts:1249-1560` `paginateWithFuzzyFallback`) → filtra por
    creador (INFERIDO que delega en `paginate`; poco natural para un catálogo). ⚠
  - Detalle `GET /v1/quotes/:n`, `GET /v1/invoices/:n`, `GET /v1/product/one/:id` → **NO filtra**.
  - Editar/aprobar/anular/eliminar → permisos sin `supports_scope` → **NO filtra**.
  - Criterio = `created_by_user_id`, **no** vendedor asignado.
- **A-056 · Filtros de ESTADO**: no existen (A-018). Nada que demostrar.
- **A-057 · Casos con/sin permiso demostrables de verdad en la app** (propuesta):
  1. **Vista** — rol «Vendedor» sin `PRODUCT_VIEW` (o sin `QUOTE_VIEW`): la persona no puede abrir
     Productos; el API responde 403 «Productos» (PRODUCT_VIEW). Efecto inmediato al guardar (A-022).
  2. **Acción** — con `QUOTE_VIEW/CREATE/UPDATE` pero sin `QUOTE_APPROVE`: aprobar
     (`PATCH /v1/quotes/approve/:n`) → 403 «Aprobar Cotizaciones» (QUOTE_APPROVE); al concederlo, aprueba.
     Variante: sin `PRODUCT_DELETE` no puede eliminar un producto.
  3. **Alcance** — `QUOTE_VIEW` en «Propios»: el listado de Cotizaciones muestra solo las que creó esa
     persona; con «Todos», las de toda la empresa. **Requiere sembrar** cotizaciones creadas por al menos dos
     usuarios (la 43 tiene **0 cotizaciones** y **0 facturas** hoy). No abrir la de otro por URL (sí se ve).
  4. **Credencial de API** — A-053: 200 con lo permitido / 403 con lo no permitido, y la bitácora de la
     credencial.
  Descartado: «Estado del documento» (no existe) y «Equipo» sin sembrar equipos (la 43 tiene 0).

---

## 5. Auditoría del cambio de permisos de un rol

- **A-058 · Sí, con antes/después legible**, solo por el guardado en lote `PATCH /role/:id/permissions`:
  `recordAudit` (`role-permission-changes.service.ts:355-400`) compara la matriz antes y después y graba
  UN evento: `entity_name='roles'`, `entity_id=<rol>`, `action='UPDATE'`, `event='PERMISSIONS_CHANGED'`,
  `metadata.roleName`, y `changes` con clave `«Módulo · Recurso»` → `{ oldValue: "Ver, Crear", newValue: "Ver (Propios), Crear, Editar" }`
  (`—` si no había nada). Va por el buffer (flush post-request, `audit-log.service.ts:43-45`).
- **A-059 · Además**: las inserciones en `role_permissions` pasan por el suscriptor de auditoría
  (`audit/audited-entities.config.ts:113-116`: `users` FULL, `roles` FULL, `role_permissions` LIGHT,
  `user_company_roles` FULL), pero los `delete` no (por eso existe el evento). Crear/editar/borrar el rol
  queda como CREATE/UPDATE/DELETE de `roles`. Asignar/quitar roles a personas queda en `user_company_roles`.
- **A-060 · Cómo verlo**: pestaña Auditoría o `GET /api/v1/audit-logs/entity/roles/<id>` (A-049).

---

## 6. Estado de la BD local y cómo sembrar

- **A-061 · #1336 NO trae migraciones** (37 archivos: servicios, DTO, interfaces, arnés; `role.entity.ts` y
  `user.entity.ts` solo añaden propiedades transitorias). El esquema que usa ya existe en la BD local:
  `roles.parent_role_id`, `roles.is_integration_role`, `role_permissions.source`, `permission.supports_scope`,
  `role_permission_exclusions`, índice `IDX_audit_logs_company_user`. **Nada pendiente para Seguridad.**
- **A-062 · Migraciones pendientes en `germiva` local** (tabla `migrations`: 1 249 filas, última
  `ProductMaxStock1810000000999`), comparado con `src/database/migrations/` — **9**, ninguna de Seguridad:
  `1810000000995-ReapplyPremiumErpModulesToEnterprisePlan` (comparte timestamp con `VariantChildCodeIsBarcode`, que sí corrió) ·
  `1810000001000-FractionalStockQuantities` · `1810000001001-ServicesWithoutBatchControl` ·
  `1810000001002-LandedCostCurrency` · `1810000001003-SupplierPaymentSingleCounter` ·
  `1810000001004-DisbursementLocalCurrencyTotal` · `1810000001010-FixDominicanHolidaysLaw13997` ·
  `1810000001011-FixSharedHrCatalogsLegal` · `1810000001012-FixSharedWorkScheduleTexts`.
  Ojo: `dist/database/migrations` llega solo hasta `…0999` → hace falta `nest build` antes de `migration:run`
  (regla: `src/migrations/` es carpeta muerta).
- **A-063 · Alta de empresa y usuarios**:
  - Empresa: `POST /api/auth/dev/register` (solo local/development/test; throttle 1/min; verifica el correo
    y corre `setupInitialCompanyConfiguration`) (`auth.controller.ts:251-275`). Producción: `POST /api/auth/register` (reCAPTCHA).
  - Usuarios: `POST /api/user` (USER_CREATE) con `roles:[ids]`; login de scripts por `POST /api/auth/dev/login`
    (`claude-tutorial/seeds/cajas/_lib.mjs:28-40`, **revoca la sesión previa del mismo usuario**).
  - Plan: la suscripción se cambia por SQL (`UPDATE subscriptions SET plan_id=… WHERE company_id=43`,
    `seeds/cajas/plan-s8.mjs`). Módulos por plan en `plan_module_configs` (no `plan_modules`, que está vacía).
    SECURITY, USERS, GENERAL y COMPANY son **núcleo en todos los planes** (`admin/module/module-visibility.ts:65-70`).
    Plan 2 «Emprendedor»: INVOICING, SALES, PRODUCTS, INVENTORY, POS… **sin SALES_QUOTE ni API_ACCESS**.
    Plan 15 «Empresarial»: todo lo anterior + **SALES_QUOTE**, SALES_ORDER, **API_ACCESS**, CRM, etc.
    → Para la serie hace falta **plan 15**. (Las credenciales usan permisos de SECURITY, así que no las gatea API_ACCESS.)
- **A-064 · Empresa demo 43 hoy**: «Ferretería El Progreso SRL», suscripción 42 **plan 15 TRIAL**;
  usuarios `admin.progreso` (Admin), `yohanna.peralta` (Cajero + «Cajero POS demo»), `luis.batista` (Cajero),
  `carmen.rosario` (Supervisor de Caja), clave `Demo2026!`; 1 rol propio (`Cajero POS demo`, id 75, sin padre);
  0 equipos, 0 credenciales de API, 25 productos, 0 cotizaciones, 0 facturas. Sembrado previo: scripts
  idempotentes por API con los payloads del front + SQL solo para lecturas/plan (`seeds/pos/sembrar.mjs`,
  `seeds/cajas/sembrar-s0.mjs`, estados con `fijar.mjs`/`restaurar.mjs`).
  Para Seguridad habría que sembrar: 1-2 roles propios (uno hijo de otro para la herencia), 1 equipo,
  cotizaciones creadas por dos usuarios distintos, una persona sin rol y opcionalmente una credencial.

---

## Dudas / INFERIDO

- **A-065** · `GET /v1/product` aplica «Propios» vía `paginateWithFuzzyFallback` → se infiere que termina en
  `paginate`; no verificado línea a línea.
- **A-066** · Caché de roles por Redis (`admin/auth/cache/permissions-cache.service.ts`, TTL 30 min, invalida
  por versión en `afterInsert/Update/Remove` de Role/RolePermission/RolePermissionExclusion/UserCompanyRole,
  `permissions-invalidation.subscriber.ts:13-83`). El guardado en lote borra con `delete()`/`update()` por
  QueryBuilder; no se verificó si esos disparan el suscriptor. El **acceso** no depende de la caché
  (A-022), pero el **alcance** sí (sale de `user.companyRoles` en caché): un cambio de «Todos→Propios» podría
  tardar en verse si solo hubo `update`. En el video, tras cambiar el alcance, conviene que la persona
  vuelva a entrar.
- **A-067** · No se revisó el front: si oculta menús/botones por permiso, si ofrece «acciones masivas» y cómo
  muestra el 403. El API no tiene endpoints masivos.
- **A-068** · Cupo de usuarios del plan: el QA del PR (D5) dice que las credenciales cuentan contra el cupo
  y dio 403 en su empresa de prueba; `plan_resource_limits` no tiene filas para el plan 15 en local →
  presumiblemente sin tope. No probado.

## Posibles defectos

- **A-069 (ALTA, a verificar)** · **Borrar un rol no quita el acceso a quienes lo tienen.** `remove` hace soft
  delete del rol (`role.service.ts:863-899`) sin tocar `user_company_roles` ni comprobar titulares, y
  `hasAccess` (`has-access.ts:27-39`) une `user_company_roles → role_permissions` sin mirar
  `roles.deleted_at`. Hoy 0 casos en la BD local, pero no hay nada que lo impida.
- **A-070 (MEDIA)** · **Escalada por `isAdminRole` del cliente**: `CreateRoleDto`/`UpdateRoleDto` aceptan
  `isAdminRole` y el servicio lo guarda tal cual (`role.service.ts:114-131`, 598-599 solo impide pasar de
  true a false). Quien tenga ROLE_CREATE+ROLE_EDIT puede fabricar un rol admin y concederle permisos
  `isAdminOnly`. Además el chequeo «un no-admin no modifica un rol admin» (587-592) es **código muerto**: el
  controlador nunca pasa `userRole` (`role.controller.ts:64`). Y editar permisos de un rol no aplica la regla
  «no dar lo que no se tiene» que sí aplica la asignación (A-039).
- **A-071 (MEDIA)** · «Propios» solo filtra listados (A-017/A-055): el detalle por número/id y las
  ediciones no respetan el alcance. Si la UI lo presenta como «solo ve y toca lo suyo», promete de más.
- **A-072 (BAJA)** · Mensaje de 403 con nombres poco claros: `INVOICE_VIEW` = «Facturas Socios»,
  `INVOICE_CHANGE_STATUS` = «Estado Facturas Socios», `AUDIT_LOG_READ` = «Registro de Auditoría Contable»
  (y es el permiso de TODA la bitácora de Seguridad).
- **A-073 (BAJA)** · `EMPTY_ROLE` cuenta con `LIMIT 20` (`security-overview.service.ts:307-327`): con >20
  roles vacíos en uso anuncia 20 (mismo patrón que el H1 corregido para personas).
- **A-074 (BAJA)** · `GET /v1/audit-logs?entityName=roles` usa LIKE (`audit-log.service.ts:125-127` +
  `common/pagination/filter-by-word.ts`): también trae `user_company_roles`, cuyos `entity_id` son de otra
  tabla → el «historial del rol» por filtro mezcla registros. Usar `/v1/audit-logs/entity/roles/:id`.
- **A-075 (BAJA)** · El evento `PERMISSIONS_CHANGED` solo lo emite el guardado en lote: los endpoints
  antiguos (`add-permission`, `delete-permission`, `update-permission-scope`) y los cambios de permisos de
  credenciales (`POST/DELETE/PUT …/integration-users/:id/permissions`) no dejan antes/después, y los
  quitados con `delete` no dejan rastro. Tampoco se registra en los roles HIJOS cuyo heredado cambió.
- **A-076 (BAJA)** · Borrar una credencial deja huérfano su rol propio `Integración · …`
  (`integration-user.service.ts:366-376`); `resolveTeamUserIds` no excluye equipos borrados
  (`team-membership-resolver.service.ts:19-24`); `/v1/invoices/purchases` exige solo `INVOICE_VIEW`
  (`invoices.controller.ts:252-260`).
- Sin hallazgos de endpoints sin guard en Seguridad (único sin permiso: `GET /api/permission/enum`, bloqueado
  fuera de `local`). Aislamiento multiempresa: roles (404), credenciales (404), persona (404
  `Persona no encontrada en la empresa actual`, `person-access.service.ts:109`), bitácora (filtra por
  `company_id`) — correcto en código.
