# seeds/seguridad — empresa demo, estados E0/E2a/E6c y restauración de la serie «Seguridad»

Empresa demo **50 «Distribuidora Las Palmas SRL»** (comercial «Distribuidora Las Palmas»), RNC ficticio
**130555036**, Calle Duarte 88, Villa Mella · 809-555-0188, DOP, **sin e-CF** (B01/B02), plan **15
«Empresarial»** (suscripción 49, TRIAL), `quote_requires_approval = 1`. Plan de la serie:
`guiones/_SERIE-SEGURIDAD.md`. Todo toca SOLO filas de la empresa 50 (o de sus roles).
Correr desde `claude-tutorial/` con Node ≥ 18 (sin dependencias). API en `:3001`, front estático en `:4200`.

## Uso rápido

```bash
node seeds/seguridad/restaurar.mjs E0     # ≈ 2,8 s: canon de la serie (verifica conteos de 24 tablas)
node seeds/seguridad/restaurar.mjs E2a    # 02b: + «Contador externo» (clon de Contador) y «Cobrador» (vacío)
node seeds/seguridad/restaurar.mjs E6c    # 06b/06c: + credencial «Programa del contador» (sin «Registrar compras»)
```

Recrear desde cero (idempotente; si la empresa no existe la da de alta): `node seeds/seguridad/sembrar.mjs`
→ `fijar.mjs E0` → `preparar.mjs E2a && fijar.mjs E2a` → `preparar.mjs E6c && fijar.mjs E6c` → `restaurar.mjs E0`.

| Archivo | Qué hace |
|---|---|
| `_lib.mjs` | `api(usuario, método, ruta, cuerpo)` con login `auth/dev/login` (clave `Demo2026!`), `sql()` con `sql_log_bin=0`, `empresa()` por RNC, `permisoId(code)` |
| `sembrar.mjs` | Alta `POST auth/dev/register` (Rosa), username, plan 15 (SQL), aprobación de cotizaciones, catálogo POS + fotos + existencias, 4 clientes, 5 roles con permisos por el guardado en lote del editor, 8 personas, equipo, 8 cotizaciones y 3 facturas **con la sesión de su autor**, credencial vieja, fechas retrocedidas, ingresos, R18 y, al final, el «Cambió permisos» de Almacén. Escribe `ids.json` |
| `preparar.mjs E2a\|E6c` | Restaura E0 y arma por API el estado de partida de 02b / 06b-06c. E6c escribe `credencial.json` (clave + secreto) |
| `_estado.mjs` | Tablas medidas y su WHERE (ver abajo) |
| `fijar.mjs E#` / `restaurar.mjs E#` | Volcado por tabla con su WHERE (mysqldump, un `--where` por grupo) → `estados/E#.sql|json`; restauración por diferencias |
| `_medir.mjs` | Foto de conteo/MAX(updated_at)/MAX(id) de las tablas con `company_id` y AUTO_INCREMENT de las demás (`--comparar`) |
| `_ensuciar.mjs` | Repite por API TODO lo que escriben los videos (clonar, crear rol, hijo+exclusión+borrar, alta/edición/rol/desactivar/eliminar persona, equipo, credencial+permisos+login+rotar+pausar+revocar, alcance/herencia/cambio en vivo, aprobar Q1). Sirvió para medir y para probar `restaurar E0` |

`ids.json` y `credencial.json` llevan secretos de demo local: están en `.gitignore`.

## Qué hay en E0 (verificado por API y BD el 2026-09-27)

- **Personas** (correo `<usuario>@germiva.demo`, clave `Demo2026!`): rosa.almanzar 7943 (Admin) · ana.mejia 7944
  (Vendedor, Zona Este) · jose.cabrera 7945 (Vendedor + Almacén, Zona Este) · carlos.pimentel 7946 (Vendedor
  sénior) · pedro.nunez 7947 (Almacén) · marta.guzman 7948 (Auditor) · hector.vargas 7949 (Vendedor, creado hace
  45 días, **nunca entró**) · luisa.feliz 7950 (**sin rol**, entró 1 vez) · sonia.reyes 7951 (Mensajero,
  **inactiva**, entró 1 vez antes de desactivarse).
- **Roles** 77 Vendedor · 78 Vendedor sénior (hijo de 77; «Cotizaciones · Ver» DIRECTO con alcance Todos) · 79
  Almacén · 80 Auditor (solo lectura) · 81 Mensajero (vacío). Equipo **1 «Zona Este»** (Ana, José).
- **Credencial** 7952 «Tienda en línea anterior» (prefijo `gv_live_0e9d2d31`, creada hace 120 días, última
  llamada hace 80 → «Sin uso»).
- **Cotizaciones** 1–8 = Q1…Q8 del plan: 1 Ana Borrador · 2 Ana Borrador · 3 Ana Aprobada · 4 José Borrador ·
  5 José Aceptada · 6 Carlos Aprobada · 7 Carlos Borrador · 8 Rosa Cancelada. Alcance real por API:
  Ana 3 · José 2 · Carlos 8 · Marta 8 · Pedro 403.
- **Facturas** 1000000001 F1 B0100000001 (creada por Carlos; la **emite Rosa**: Carlos no tiene
  `INVOICE_UPDATE` y `change-status` responde 403) · 1000000002 F2 B0200000001 (Rosa, consumidor final) ·
  1000000003 F3 borrador de Carlos.
- **Catálogo**: los 25 productos de `seeds/pos/catalogo.json` (24 con foto), creados por Rosa. Las categorías
  tienen OTRO nombre (Herramientas de trabajo, Material eléctrico, Plomería y agua, Pinturas, Construcción y
  obra, Jardinería) por el defecto D-ENT-1 (abajo).
- **Resumen** (`GET v1/security/overview` como Rosa): 9 personas, 1 administradora, 1 sin rol, 8 activas en 30
  días, 1 credencial / 1 sin uso. «Requiere atención»: Luisa sin rol · Tienda sin uso · Héctor nunca entró ·
  Mensajero sin permisos. La actividad reciente empieza por «Cambió permisos · Roles #79» (Almacén: «Ver, Crear,
  Editar, Importar» → «…, Exportar»). E-3 (2026-09-27): ese lote se rehízo por el API actual → evento **312438**
  (detalle «Inventario · Productos») y su «Creó» sobre role_permissions **12151** (antes 310792/11034), con la hora
  original del sembrado (11:10:22). El evento inicial 310379 (11:03) conserva la etiqueta vieja «Productos · Productos».
- **R18**: `user_company_preferences.incomplete_config_notice_seen_at` marcado para los 9. Comprobado en el
  navegador (1280×720): Rosa y Ana entran por `/authentication/signin` → `/home` en ≈ 7 s, **sin ningún modal ni
  banner** (ni «Configuración incompleta» ni aviso de TRIAL).

## Tablas (medidas con `_medir.mjs` antes/después de `_ensuciar.mjs`)

Cambian: `audit_logs`, `entity_versions`, `profiles`, `quote_approvals`, `quote_versions`, `quotes`, `roles`,
`role_permissions`, `role_permission_exclusions`, `teams`, `team_members`, `user_companies`,
`user_company_roles`, `users`. Se añaden por seguridad `quote_details`, `quote_detail_inventory_allocations`,
`prices`, `price_history`, `products`, `user_company_preferences`, `company_configs` (solo UPDATE),
`subscriptions` (solo UPDATE), `sys_sequences` (UPDATE; trigger anti-DELETE) y (E-4) `user_menu_visibility` (menú de Mi perfil, video 09: `company_id=50` y usuarios de la empresa 50, ANTES que `user_companies`).
`role_permissions` y `role_permission_exclusions` no tienen `company_id`: se acotan con
`role_id IN (SELECT id FROM roles WHERE company_id=50)` y van ANTES que `roles` en la lista.
`user_companies` no tiene `id` (clave compuesta) → modo `reemplazo`.
No se restauran: sesiones de auth, `company_user_activity_daily`, `companies.last_access_at`.

**Bitácora:** `audit_logs` SÍ se restaura por empresa (filas nuevas → DELETE por `company_id` e id; las
temporales se crean con `CREATE … SELECT … LIMIT 0`, sin particiones). Probado: tras `_ensuciar.mjs`
(+184 eventos) `restaurar E0` deja el canon (670 desde el re-canon r2). 01 y 07 se pueden grabar en cualquier orden.

## Trampas

- `users.login_date` nace NULL desde R22 (migración 1810000001031) y lo llena el primer ingreso; el Resumen
  mide los ingresos con los eventos `AUTH/LOGIN_SUCCESS` de `audit_logs`. En E0 Héctor = NULL.
- **D-S13 (re-canon 2026-09-27 r2):** toda petición de la siembra sale con user-agent de Chrome en Windows
  (`NAVEGADOR_UA` en `_lib.mjs`, parchea `fetch`), así «Últimos ingresos» y «Origen» dicen «Chrome · Windows» y no
  «Cliente de API». El paso 16 de `sembrar.mjs` quita los ingresos de preparación POSTERIORES al «Cambió permisos»
  de Almacén (verificaciones por API, re-ejecuciones) → en la toma la fila queda 2.ª (debajo del ingreso de quien
  graba), a y≈500 de 720. **No hacer logins por API entre `sembrar.mjs` y `fijar.mjs E0`**; si se hace, volver a
  correr `sembrar.mjs` (idempotente) antes de fijar.
- Los ids de E2a/E6c (roles 90 «Contador externo», 91 «Cobrador»; credencial 7957 y su rol 92) salen de los
  AUTO_INCREMENT: para re-preparar sin cambiarlos, `ALTER TABLE roles AUTO_INCREMENT=90` antes de `preparar E2a`
  y `roles=92, users=7957` antes de `preparar E6c` (ver HALLAZGOS-SEGURIDAD-VIDEO.md › Verificación ronda 2).
- El API vuelca la auditoría en lotes cada 2 s: `fijar.mjs` espera 2,6 s de quietud y `restaurar.mjs` 2,3 s
  (≈2,8 s en total). Con 0,7 s se fijó una vez E2a sin los 130 eventos del clonado.
- MySQL local 9.7.0-er2: todo UPDATE de `users` o `companies` tarda 2,5–3,5 s («Opening tables»: 690 y 538 FK que
  las referencian). Por eso el login tarda 7–12 s y el alta de usuario 8–10 s en local (D-S12).
- Un `grant` sobre un permiso HEREDADO no hace nada; para volverlo directo con otro alcance hay que mandar
  `rescope` (lo mismo que hace el editor).
- La secuencia QUOTE nace con `initial_value = 1` → la primera cotización de una empresa nueva sale con el
  número **2**. Aquí se dejó `current_value = 0` para que Q1…Q8 sean 1…8 (queda en el canon).
- Cada login revoca la sesión previa del MISMO usuario (R26): no correr `sembrar`, `preparar` ni `_ensuciar`
  mientras se graba.
- El 403 de la credencial dice «…«Productos» (PRODUCT_VIEW). Solicita acceso…»: el código sale en el mensaje.
- `v1/invoices/sales` con la credencial devuelve también el borrador F3, no solo F1 y F2.
