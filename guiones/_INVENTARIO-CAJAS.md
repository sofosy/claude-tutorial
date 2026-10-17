# Inventario de Cajas para la serie de videos (vista única, master 09-23)

Autor: AUTOR-INVENTARIO · 2026-09-23 · SOLO LECTURA sobre los repos, sin apps levantadas.
Fuente: código de `germiva-website` (master con el front PR #1171) y `Germiva-api` (PR #1261),
más la BD local (empresa 29). **Todo selector sale del código y lleva archivo:línea.** Aun así,
cada selector se valida con `ensayar.mjs` antes de grabar (R28: el ensayo solo vale si trae
líneas `──` de paso).

Rutas cortas usadas abajo:
- `FE/` = `germiva-website/src/app/modules/cashier/`
- `SH/` = `germiva-website/src/app/shared/`
- `API/` = `Germiva-api/src/modules/`

Marca **[DIN]** = el selector depende de contenido dinámico (nombre de caja, usuario, número de
movimiento, cantidad de filas…): se ajusta a los datos demo de `_DATOS-CAJAS.md`.

---

## 0. Piezas transversales (valen para todos los videos)

### 0.1 Entrada al módulo
- Menú: una sola entrada **«Cajas»** (icono `point_of_sale`) → `/cashier`.
  `germiva-website/src/app/layout/sidebar/sidebar-items.ts:809-831` (se ve con CUALQUIERA de
  `CASHIER_VIEW, CASHIER_SESSION_VIEW, CASH_MOVEMENT_APPROVE, CASH_TRANSFER_APPROVE,
  CASHIER_RECONCILIATION_CONFIRM, CASHIER_ALERT_MANAGE, CASHIER_SESSION_REOPEN,
  CASHIER_CONFIG_VIEW, CASHIER_CREATE, CASH_DENOMINATION_CREATE, CASH_DEVICE_SETTING`).
  El selector del ítem en el riel no está en el código de Cajas (lo pinta el layout): **validar en
  el ensayo**; alternativa segura: `"navegar": "/cashier"`.
- Aterrizaje sin `?section=`: si el usuario tiene sesión abierta propia → «Mi caja»; si no →
  tablero «Cajas» (`FE/pages/cashier-hub/cashier-hub.component.ts:302-316`). Mientras decide
  pinta «Cargando cajas...» (`:136-137`). **Para que el video sea determinista, navegar SIEMPRE con
  `?section=`**.

### 0.2 Cabecera de la vista única (`FE/pages/cashier-hub/cashier-hub.component.ts`)
| Elemento | Texto exacto | Selector propuesto | Línea |
|---|---|---|---|
| Título | «Cajas» | `h1.page-hero-title` | :87 |
| Subtítulo (cambia por sección) | ver tabla 0.3 | `p.page-hero-subtitle` | :88, textos en `cashier-hub.sections.ts:31-69` |
| Botón panel de configuración | «Configuración» (icono `tune`) | `.page-hero-actions button:has-text('Configuración')` | :91-97 (solo si `canConfigure`) |
| Conmutador de secciones | una pestaña por sección | `#cashier-hub-tab-cajas`, `#cashier-hub-tab-caja`, `#cashier-hub-tab-aprobaciones`, `#cashier-hub-tab-historial`, `#cashier-hub-tab-analisis` | :102-129 (id en :110). **No se pinta si el usuario solo tiene UNA sección** (:101) |
| Contador «Por aprobar» | número | `#cashier-hub-tab-aprobaciones .gm-badge--warning` **[DIN]** | :121-126 |
| Perfil que solo configura | «Tu perfil administra la configuración de cajas» + botón «Abrir configuración» | `.gm-state button:has-text('Abrir configuración')` | :157-170 |

### 0.3 Secciones y quién las ve (`FE/pages/cashier-hub/cashier-hub.sections.ts:23-77`)
| `?section=` | Pestaña | Permisos (basta uno) | Subtítulo exacto |
|---|---|---|---|
| `cajas` | Cajas | `CASHIER_VIEW` | «Estado de cada caja: ábrela, continúa tu turno o revisa quién la opera.» |
| `caja` | Mi caja | `CASHIER_SESSION_VIEW` | «Abre tu sesión, registra entradas y salidas de efectivo y ciérrala con su cuadre.» |
| `aprobaciones` | Por aprobar | `CASH_MOVEMENT_APPROVE`, `CASH_TRANSFER_APPROVE`, `CASHIER_RECONCILIATION_CONFIRM`, `CASHIER_ALERT_MANAGE` | «Movimientos, transferencias y cuadres que esperan una decisión del supervisor.» |
| `historial` | Historial | `CASH_MOVEMENT_APPROVE`, `CASHIER_RECONCILIATION_CONFIRM`, `CASHIER_SESSION_REOPEN`, `CASHIER_CONFIG_VIEW` | «Sesiones, movimientos, transferencias y cuadres de todas las cajas de la empresa.» |
| `analisis` | Análisis | `CASH_MOVEMENT_APPROVE`, `CASHIER_RECONCILIATION_CONFIRM`, `CASHIER_ALERT_MANAGE`, `CASHIER_CONFIG_VIEW` | «Estado en vivo, reportes del período, alertas y auditoría del módulo.» |
| panel `?config=` | (botón Configuración) | `CASHIER_CREATE`, `CASH_DENOMINATION_CREATE`, `CASH_DEVICE_SETTING`, `CASHIER_CONFIG_VIEW` (`:84-89`) | — |

**Matriz real de roles (BD local, `role_permissions`, 09-23):**
| Rol | Secciones que ve | Configuración |
|---|---|---|
| Admin (1) | las 5 | Sí: Cajas · Denominaciones · Políticas |
| Supervisor de Caja (3) | Cajas · Mi caja · Por aprobar · Historial · Análisis | Sí, por `CASH_DEVICE_SETTING`, pero solo **Cajas** y **Denominaciones** (sin `CASHIER_CONFIG_VIEW` no ve Políticas; sin `CASHIER_CREATE/UPDATE` no crea ni edita cajas; sí **Bloquear/Desbloquear**) |
| Cajero (2) | **Cajas · Mi caja** (sin Historial ni Análisis) | No |

Permisos de Cajero (2): `CASHIER_VIEW, CASHIER_SESSION_VIEW/CREATE/UPDATE, CASH_MOVEMENT_VIEW/CREATE/VOID,
CASH_TRANSFER_VIEW/CREATE, CASHIER_RECONCILIATION_VIEW/CREATE, CASH_COUNT_VIEW/CREATE,
CASH_DENOMINATION_VIEW, ACCOUNTING_CHART_READ, BANK_ACCOUNT_READ`.
Supervisor (3) añade: `CASH_MOVEMENT_APPROVE, CASH_TRANSFER_APPROVE, CASHIER_RECONCILIATION_CONFIRM,
CASHIER_SESSION_DELETE/REOPEN, CASHIER_ALERT_VIEW/MANAGE, CASHIER_BLOCK/UNBLOCK,
CASHIER_SURPRISE_AUDIT, CASH_DEVICE_SETTING, CASH_COUNT_UPDATE/DELETE`.

### 0.4 Avisos: ¿toast o diálogo? (R3 de la skill)
- **Éxito = toast** (snackbar) en TODO el módulo: `CrudFeedbackService.success/saved/warning`
  (`SH/services/crud-feedback.service.ts:119-129`), acción «Cerrar», dura **3,5 s**
  (`:67`). Selector: `.mat-mdc-snack-bar-container`. No hay que pulsar nada. Texto típico:
  «Caja creada exitosamente» (`saved('Caja','creada')` → `:120`).
  Los que quedan pendientes salen como **toast de advertencia** (`feedback.warning`).
  ⇒ Marcar el toast con `resaltar` **enseguida** (vive 3,5 s; el de error 6 s).
- **Confirmaciones y errores = diálogo** `CustomAlertDialogComponent`
  (`SH/services/custom-alert.service.ts:35-60`; plantilla
  `SH/components/custom-alert-dialog/custom-alert-dialog.component.html`):
  contenedor `.custom-alert-dialog-style` (:1), botón de confirmar
  `.custom-alert-dialog-style button.confirm-button` (:34; su texto = `confirmButtonText`,
  por defecto «Confirmar»; en `alerts.error/warning` sin texto dice «Aceptar»), cancelar
  `button.cancel-button` (:25). Con dos diálogos abiertos marcar por panel (R20).
- Los diálogos propios de Cajas llevan cabecera `.cashier-dialog-header h2` y la X
  `button.cashier-sheet-close` (tooltip «Cerrar»).
- Los «paneles laterales» (Configuración, Abrir mi caja, Nuevo movimiento, Anular movimiento)
  son `MatDialog` a la derecha, alto 100 vh, con clase `.cashier-operation-sheet`
  (`FE/services/operation-sheet.service.ts:24-40`); los anchos usan además
  `.cashier-operation-sheet--wide`.

### 0.5 Atajos de teclado de Mi caja (`FE/pages/cashier-workspace/cashier-workspace.component.ts:1318-1361`)
`1` = Entrada · `2` = Salida · `R` = Actualizar · `Ctrl+Shift+C` = Cerrar caja (solo sin diálogo abierto).
No usarlos en cámara (el espectador no ve la tecla); se pueden mencionar.

---

## 1. CONFIGURACIÓN — panel lateral «Configuración de cajas»

**Qué es (novato):** los ajustes que se hacen una vez: qué cajas (puntos de cobro) tiene la
empresa, qué billetes y monedas se cuentan, y las reglas que aplican a todas las cajas.
**Ruta:** `/cashier?config=cajas|denominaciones|politicas` (alias viejos `registers`, `devices`,
`denominations`, `policies`, `general`: `cashier-hub.sections.ts:104-120`). Rutas heredadas
`/cashier/config` y `/cashier/config/:section` redirigen (`FE/cashier.routes.ts:69-80`).
**Rol:** Admin (las 3 secciones); Supervisor (Cajas sin crear/editar + Denominaciones sin crear).
**Abrir:** botón «Configuración» de la cabecera (0.2) o `navegar` con `?config=`.

Panel (`FE/components/cashier-settings-sheet/cashier-settings-sheet.component.ts`):
- Título «Configuración de cajas» `#cashier-settings-sheet-title` (:37); subtítulo «Cajas,
  denominaciones y políticas de operación» (:38); cerrar `.settings-sheet__header button.cashier-sheet-close` (:40-47).
- Sub-pestañas `nav.segmented--sub button.segmented__option:has-text('Cajas'|'Denominaciones'|'Políticas')`
  (`FE/pages/config-center/config-center.component.ts:102-118`, rótulos :691-693). Cambiar de
  pestaña con Políticas sin guardar pregunta «descartar cambios» (:725-734).
- Cerrar con cambios sin guardar en Políticas → confirmación (`cashier-settings-sheet:128-132`).
- Al cerrar el panel se recargan tablero, Mi caja, Por aprobar y Análisis (`cashier-hub:455-460`).

### 1.1 Sección «Cajas» (`?config=cajas`) — `FE/pages/config-center/config-center.component.ts`
| Elemento | Texto exacto | Selector | Línea |
|---|---|---|---|
| Título de sección | «Cajas» + nota «Puntos de cobro de la empresa: crea, edita, bloquea y gestiona sus dispositivos.» | `.config-section h3.section-title` · `.config-section > p.gm-dialog-note` | :123-139 |
| Exportar | «Exportar» (Excel) | `.section-title__tail button:has-text('Exportar')` | :127-130 |
| Alta | «Nueva caja» (solo `CASHIER_CREATE`) | `.section-title__tail button:has-text('Nueva caja')` | :131-136 |
| Cifras | «Total de cajas» · «Abiertas» · «Cerradas» · «Bloqueadas» (del API `GET v1/cashiers/summary`) | `.config-kpis .gm-fig` | :146-166 |
| Bandeja de solicitudes de vínculo | solo modo Estaciones | `app-device-requests-inbox` | :170 |
| Buscar | «Buscar» (placeholder «Nombre, código, ubicación...») | `.table-toolbar input[placeholder^='Nombre, código']` | :175-184 |
| Filtros | «Tipo» · «Estado» (Todos/Activa/Inactiva/Bloqueada) · «Bloqueada» (Todas/Sí/No) | `mat-form-field:has(mat-label:text-is('Estado')) mat-select` (R4) | :186-213 |
| Operativas / Archivadas | segmentado | `.toolbar-archived button:has-text('Archivadas')` | :222-227 |
| Tabla | columnas Caja · Ubicación · Tipo · Estado · Balance · Métodos · Dispositivo | `table.data-table tbody tr` **[DIN]** | :261-373 |
| Editar fila | icono lápiz, tooltip «Editar» (solo `CASHIER_UPDATE`) | `tr:has-text('Caja Mostrador 2') button[mattooltip='Editar']` **[DIN]** — ojo: Angular NO refleja `matTooltip` como atributo en todos los casos; preferir `tr:has-text('…') button:has(mat-icon:text-is('edit'))` | :358-362 |
| Menú ⋮ de fila | «Más acciones» | `tr:has-text('…') button:has(mat-icon:text-is('more_vert'))` **[DIN]** | :363-365 |
| Ítems del ⋮ | «Ver detalles» · «Bloquear» (si no está bloqueada, `CASHIER_BLOCK`) · «Desbloquear» (bloqueada, `CASHIER_UNBLOCK`) · «Desvincular dispositivo» · «Archivar» (`CASHIER_DELETE`) | `.gm-menu button[mat-menu-item]:has-text('Bloquear')` (R21: pulsar su `mat-icon`) | :385-416 |
| Archivadas: fila | «Ver detalles» / «Restaurar» | `button:has(mat-icon:text-is('restore'))` | :348-356 |
| Vacío | «Aún no hay cajas» / «Sin resultados» / «No hay cajas archivadas» | `.gm-state__t` | :235-258 |

Diálogos que abre:
- **Nueva / Editar caja** → 1.1.a.
- **Bloquear caja** / **Desbloquear caja** → 4.4 (diálogo común). Éxito: toast «Caja «X» bloqueada
  exitosamente» / «…desbloqueada exitosamente» (:889, :905).
- **Archivar**: confirmación «Archivar caja» — «La caja "X" se archivará: dejará de aparecer en el
  listado y no podrá operar. Podrás restaurarla desde "Ver archivadas".» — botón «Archivar»
  (:912-926) → toast «Caja «X» archivada exitosamente». El API lo rechaza si la caja tiene sesión
  abierta («La caja X tiene una sesión abierta; ciérrala antes de archivarla.»). Es **soft delete**.
- **Restaurar**: «Restaurar caja» / botón «Restaurar» (:929-942).
- **Ver detalles**: `CashierDetailDialogComponent` (600 px) (:962-969).

#### 1.1.a Diálogo «Nueva caja» / «Editar caja» — `FE/components/cashier-form/cashier-form.component.ts`
Título `.cashier-dialog-header h2` = «Nueva caja» | «Editar caja» (:37).
| Sección | Campo (etiqueta exacta) | formControlName | Línea | Regla |
|---|---|---|---|---|
| Información general | Nombre (placeholder «Ej: Caja principal») | `name` | :52 | requerido, 1-100 |
| | Código («Ej: CAJA-001») | `code` | :60 | requerido, 1-50, único por empresa (API «Ya existe una caja con el código …») |
| | Ubicación («Ej: Sucursal Centro») | `location` | :68 | **requerido** (:279) |
| Métodos de pago aceptados | Efectivo · Tarjeta · Transferencia | `acceptCash` · `acceptCard` · `acceptTransfer` | :81-83 | por defecto ✓ ✓ ✗ |
| Modo de operación | «Control por denominaciones (modo estricto)» | `requireDenominationControl` | :91 | nota :95-100; se revierte solo si no hay denominaciones (:315-323) |
| Montos y límites | Fondo fijo (RD$) — «Monto base que permanece en la caja (opcional)» | `fixedFund` | :124 | ≥0 |
| | Límite mínimo de efectivo — «Umbral de alerta por saldo bajo (opcional)» | `minCashLimit` | :134 | ≤ máximo (:330-345) |
| | Límite máximo de efectivo — «Umbral de alerta por exceso de efectivo (opcional)» | `maxCashLimit` | :148 | |
| Dispositivo asignado (solo edición) | «Sin asignar» / «Vinculado» | — | :158-187 | |
Botones: «Cancelar» (:205-207) · **«Crear caja»** | **«Guardar»** (:208-213; deshabilitado si inválido).
Selector confirmar: `.cashier-form-dialog [mat-dialog-actions] button:has-text('Crear caja')`.
Éxito: **toast** «Caja creada exitosamente» / «Caja actualizada exitosamente» (:400). Error: banda
roja dentro del diálogo `.gm-dialog-alert--danger` (:190-195).
Selectores de campo: `.cashier-form-dialog input[formcontrolname='name']` (formControlName
estático sí se refleja como atributo `formcontrolname`).
**No hay campo «Tipo»**: el tipo (Física…) lo pone el API (todas las cajas de la BD son `PHYSICAL`).

### 1.2 Sección «Denominaciones» (`?config=denominaciones`) — `config-center.component.ts:420-498`
**Qué es:** el catálogo de billetes y monedas con que se cuenta el efectivo (conteo del fondo al
abrir, conteo de cierre en cajas estrictas, desglose de cobros estrictos).
| Elemento | Texto | Selector | Línea |
|---|---|---|---|
| Alta | «Nueva denominación» (`CASH_DENOMINATION_CREATE`: solo Admin) | `button:has-text('Nueva denominación')` | :426-433 |
| Nota | «Billetes y monedas disponibles para los conteos y cuadres de caja.» | | :435 |
| Grupos | «Billetes» / «Monedas» con contador | `.gm-grp:has-text('Billetes')` | :465-470, :684-687 |
| Fila | «RD$ 2,000» + nombre («Dos Mil») | `.gm-mini:has-text('Dos Mil')` **[DIN]** | :471-490 |
| Editar / Eliminar | iconos `edit` / `delete` | `.gm-mini:has-text('…') button:has(mat-icon:text-is('edit'))` | :478-489 |
| Vacío | «Aún no hay denominaciones» + aviso de modo estricto | | :442-462 |

Diálogo **Nueva / Editar denominación** (`FE/components/denomination-form/denomination-form.component.ts`):
título «Nueva denominación» | «Editar denominación» (:38).
| Campo | formControlName | Línea |
|---|---|---|
| Nombre de la denominación («Ej: Billete de cien») | `nameCount` | :52 |
| Valor («Ej: 100», sufijo = divisa) | `valueCount` | :65 |
| Divisa (`mat-select`, opción «DOP — …») | `currency` | :76-80 |
| Tipo de denominación: segmentado **«Moneda» / «Billete»** (no es formControl en el DOM; botones `.type-seg button`) | `type` (vía `setType`) | :94-107 |
| Orden de visualización | `sort` | :113 |
Botones «Cancelar» · **«Crear denominación»** | «Guardar» (:136-146). Éxito: toast «Denominación creada
exitosamente» (:331). Eliminar: confirmación «Eliminar denominación» — «¿Está seguro que desea
eliminar la denominación "X"?» — botón «Eliminar» (`config-center:1062-1077`) → toast
«Denominación eliminada exitosamente».

⚠ **Las 10 denominaciones de la BD son del CATÁLOGO GLOBAL (`company_id IS NULL`)**: 2000, 1000,
500, 200, 100, 50 (billetes) y 25, 10, 5, 1 (monedas), todas DOP, `sort` NULL. La entidad es
`@SharedCatalog` pero `updateDenomination`/`removeDenomination`
(`API/cashiers/cashiers.service.ts:1487-1523`) **no llaman a `assertSharedCatalogEditable`**: si en
cámara se edita o elimina una de ellas desde la empresa 29 (que NO es principal,
`isCompanyMain=0`), se cambia el catálogo de TODAS las empresas. **En el video solo se CREA una
denominación nueva (propia de la empresa). Nunca editar ni eliminar las globales.** Además falta el
billete de **RD$20** en el catálogo: es el candidato natural para «Nueva denominación».

### 1.3 Sección «Políticas» (`?config=politicas`) — `FE/pages/global-config/global-config.component.ts`
**Qué es:** reglas globales que aplican a todas las cajas. Solo `CASHIER_CONFIG_VIEW` (Admin). Sin
`CASHIER_CONFIG_EDIT` el formulario sale deshabilitado (:506-512).
Título «Políticas de operación» + nota «Reglas globales que aplican a todas las cajas: fondos,
tolerancias, sesiones, aprobaciones y cuadres.» (`config-center:500-510`).
| Bloque (h4) | Campo (etiqueta exacta) | formControlName | Línea | Valor actual empresa 29 |
|---|---|---|---|---|
| Estaciones de trabajo (solo `COMPANY_CONFIG_CREATE`) | «Operar con estaciones vinculadas» (checkbox SIN formControlName) | — (`mat-checkbox:has-text('Operar con estaciones')`) | :58-86 | **OFF** (Flexible) |
| Fondos y límites | Fondo inicial por defecto | `defaultInitialCash` | :101 | 5,000.00 |
| | Fondo inicial mínimo | `minInitialCash` | :110 | vacío |
| | Fondo inicial máximo | `maxInitialCash` | :123 | vacío |
| Tolerancias de diferencia | Modo de tolerancia (Monto fijo / Porcentaje / Ambos) | `toleranceMode` | :146 | Monto fijo |
| | Tolerancia (monto fijo) | `toleranceAmount` | :158 | 50.00 |
| | Tolerancia (porcentaje) | `tolerancePercentage` | :168 | 1.00 (deshabilitado en modo Monto) |
| | Diferencias consecutivas máximas («Antes de bloquear automáticamente») | `maxConsecutiveDifferences` | :179 | 3 |
| Control de sesiones | Duración máxima de sesión (min) | `maxSessionDurationMinutes` | :198 | 720 |
| | Permitir operación en días feriados | `allowOperationOnHolidays` | :204 | apagado |
| Aprobaciones | Retiros sin aprobación (máximo) | `maxWithdrawalWithoutApproval` | :229 | 5,000.00 |
| | Depósitos sin aprobación (máximo) | `maxDepositWithoutApproval` | :236 | 10,000.00 |
| | Requerir notas para retiros | `requireNotesForWithdrawal` | :241 | ✓ |
| Umbrales de alerta | Alerta por saldo bajo | `alertThresholdLow` | :262 | vacío |
| | Alerta por exceso de efectivo | `alertThresholdHigh` | :275 | vacío |
| Cuadre de caja | Requerir cuadre para cerrar sesión | `requireReconciliationForClose` | :297 | ✓ |
| | Requerir justificación para diferencias | `requireJustificationForDifference` | :303 | ✓ |
| | Conteo ciego en el cuadre | `blindCount` | :309 | apagado |
| | Ventana para reabrir sesión (hrs) | `reconciliationConfirmationHours` | :322 | 24 |
Hints de modo (:499-503): «Se acepta una diferencia hasta el monto fijo» / «…hasta ese porcentaje del
total esperado» / «Se acepta la mayor de las dos: el monto fijo funciona como piso del porcentaje».
Botón **«Guardar configuración»** (`form-actions`, :331-345; «Guardando…» mientras guarda) →
toast «Configuración de cajas guardada exitosamente» (:767). Error → diálogo «Error al guardar».
Selector: `button[type=submit]:has-text('Guardar configuración')`. La fila de BD es
`cashier_config.id=1` (compartida por toda la empresa 29): **restaurar entre tomas**.

---

## 2. DATOS MAESTROS — tablero «Cajas» (`?section=cajas`)

**Qué es:** la puerta de entrada: una tarjeta por caja con su estado y UNA acción principal.
**Ruta:** `/cashier?section=cajas`, filtro enlazable `&estado=abiertas|cerradas|bloqueadas`
(`FE/pages/cashier-board/cashier-board.component.ts:37-40, :627-635`).
**Rol:** `CASHIER_VIEW` (Admin, Supervisor, Cajero).

| Elemento | Texto exacto | Selector | Línea |
|---|---|---|---|
| Buscar | «Buscar» («Nombre, código, ubicación...») | `.board-toolbar__search input` | :110-120 |
| Filtro por estado con totales | «Todas N» · «Abiertas N» · «Cerradas N» · «Bloqueadas N» | `.board-toolbar nav button.segmented__option:has-text('Abiertas')` **[DIN: el número]** | :122-134, :564-572 |
| Alta | «Nueva caja» (solo `CASHIER_CREATE`) | `button.board-toolbar__new` | :136-141 |
| Tarjeta | `article.board-card` con `aria-label="Caja <nombre>"` | `article.board-card[aria-label='Caja Caja Mostrador 2']` **[DIN]** (el aria-label antepone «Caja »: con nombres que ya empiezan por «Caja» queda «Caja Caja …») | :194 |
| Distintivos | «Tu caja» · «Bloqueada» · «Abierta» · «Cerrada» | `.board-card__badges .gm-badge` | :200-218 |
| Datos | «Ubicación» · «La opera» (usuario o «Tú») + «Abierta hace …» · «Efectivo en caja» · o «Última actividad» | `.board-card__facts` | :228-262 |
| Acción principal | **«Continuar»** (su caja) · **«Abrir sesión»** (cerrada y libre) · **«Ver sesión»** (abierta por otro, solo supervisión) · **«Desbloquear»** (bloqueada, `CASHIER_UNBLOCK`) | `article.board-card[aria-label='Caja …'] .board-card__foot button` **[DIN]** | :264-282, lógica :769-789 |
| Sin acción | «En uso» · «Ya tienes una caja abierta» · «Bloqueada: <motivo>» · «Bloqueada por supervisión» · «Disponible» · «Se abre desde su estación vinculada» | `.board-card__note` | :280, :792-800 |
| Menú ⋮ de tarjeta | «Más acciones» → «Movimientos» · «Sesiones» · «Cuadres» (van a Historial filtrado `?cashier=<id>`) · «Configurar caja» (`CASHIER_UPDATE`) | `article.board-card[…] button.board-card__menu` → `.gm-menu button:has-text('Movimientos')` | :219-225, :304-319, :524-532, :887-891 |
| Cargar más | «Cargar más (N de M)» (50 por página) | `.board-more button` | :294-301 |
| Estados | carga (esqueletos) · «Error al cargar los datos. Intente nuevamente.» + «Reintentar» · «No hay cajas configuradas» | | :144-190 |

Orden de tarjetas: la del usuario, abiertas, bloqueadas, cerradas; alfabético dentro (:579-595).
«Abrir sesión» abre el MISMO panel «Abrir mi caja» con la caja preseleccionada (:816-832) → 3.1.
«Ver sesión» abre **«Detalle de sesión»** (`FE/components/session-detail/session-detail.component.ts:48`;
datos Caja · Cajero · Estado · Apertura · Cierre · Duración · Fondo inicial · Modo, sección «Efectivo
de la sesión»; botón «Cerrar» :130).
«Desbloquear» → diálogo 4.4, toast «Caja «X» desbloqueada exitosamente» (:853).
«Configurar caja» → diálogo 1.1.a en modo edición (:860-875).
Con estaciones OFF (empresa 29) «Abrir sesión» aparece en toda caja cerrada si el usuario puede
abrir y no tiene otra sesión (:782-789).

---

## 3. OPERACIÓN DIARIA DEL CAJERO — «Mi caja» (`?section=caja`)

**Qué es:** la sesión propia: abrir la caja con su fondo, registrar entradas y salidas de efectivo,
ver el desglose y cerrarla con el conteo. Ruta heredada `/cashier/workspace` redirige
(`FE/cashier.routes.ts:36-40`). **Rol:** `CASHIER_SESSION_VIEW`.
Componente: `FE/pages/cashier-workspace/cashier-workspace.component.ts`.

### 3.0 Estado sin sesión
«Sin sesión activa» + «Abre tu caja para empezar a operar.» (:171-177); estado vacío «No tienes una
sesión activa» + **«Abrir mi caja»** (`.gm-state button:has-text('Abrir mi caja')`, :370-378) +
«Ver todas las cajas» (vuelve al tablero, :389-392).

### 3.1 Panel «Abrir mi caja» — `FE/components/session-form/session-form.component.ts`
Se abre desde «Abrir mi caja» o desde «Abrir sesión» del tablero (caja preseleccionada).
Título «Abrir mi caja» + «Confirma el fondo inicial y el conteo para empezar a operar» (:58-59).
| Campo | Detalle | Selector / formControlName | Línea |
|---|---|---|---|
| Caja | desde el tablero: solo lectura, hint «Caja elegida en el tablero de Cajas»; desde Mi caja (Flexible): autocompletar «Caja» con solo cajas abribles | `app-autocomplete:has(mat-label:text-is('Caja')) input` **[DIN]** | :159-191 |
| Cajero | solo lectura, «La sesión se abrirá a tu nombre» | — | :194-201 |
| Fondo inicial (RD$) | prellenado con la política (5,000); con fondo fijo de la caja queda bloqueado («Fondo fijo definido por el supervisor para esta caja») | `initialCash` | :204-224 |
| Notas | «Observaciones o notas adicionales...» | `notes` | :226-235 |
| Conteo del fondo | caja normal: «Esta caja no requiere conteo por denominaciones al abrir…»; caja estricta: banda «Esta caja opera en modo estricto…» + tarjetas por denominación y distintivo «Contado: RD$…» | `app-denominations-input input.denoms__qty[aria-label='Cantidad de Mil']` **[DIN]** | :311-365; tarjetas `FE/components/denominations-input/denominations-input.component.ts:49-64` |
Botones: «Cancelar» · **«Abrir caja»** (icono `point_of_sale`; «Procesando...» mientras abre;
deshabilitado en estricta mientras el conteo no cuadre, con la pista «Cuenta el fondo: RD$x de RD$y»)
(:440-463). Selector: `mat-dialog-actions button:has-text('Abrir caja')`.
Éxito: **toast «Caja abierta exitosamente»** (:1292) y, desde el tablero, salta a «Mi caja» (`cashier-board:823-829`).
Errores posibles del API (diálogo/banda): fondo fuera de mínimo/máximo, caja bloqueada, feriado,
«Ya existe una sesión abierta para la caja X», «El usuario X ya tiene una sesión abierta…».

### 3.2 Barra de sesión y acciones rápidas (sesión abierta)
| Elemento | Texto | Selector | Línea |
|---|---|---|---|
| Estado | «Caja abierta» + nombre de caja + saldo + usuario + «abierta hace …» | `header.session-bar` | :143-170 |
| Actualizar | «Actualizar» | `.session-bar__actions button:has-text('Actualizar')` | :185-188 |
| Cerrar caja | «Cerrar caja» (rojo; `CASHIER_SESSION_UPDATE` + dueño o gestor) | `.session-bar__actions button:has-text('Cerrar caja')` | :191-196 |
| Ajustes del equipo | ⋮ → «Configurar impresora» | `button[aria-label='Ajustes de este equipo']` | :205-216 |
| Sesión ajena | «Esta caja está siendo operada por …» | `.foreign-session-banner` | :223-233 |
| Entrada | «Entrada» / «Ingresar dinero» | `button.quick-action--in` | :240-248 |
| Salida | «Salida» / «Retirar dinero» | `button.quick-action--out` | :250-258 |
| Conteo | Cajero: «Conteo de cierre» / «Declara y cierra tu turno»; con `CONFIRM`: «Cuadre» / «Conteo & cierre» | `button.quick-action--reconcile` | :261-273 |
| Desglose del efectivo | ecuación fondo + cobros + entradas − salidas… = esperado (cifras del API) | `section.breakdown-panel` | :277-286 |
| Pestañas | «Movimientos» · «Alertas» (solo `CASHIER_ALERT_VIEW`: el **Cajero NO la ve**) · «Resumen» | `.workspace-tabs .mat-mdc-tab:has-text('Resumen')` | :289-367 |
| Lista de movimientos | por fila: «Anular movimiento» / «Ver detalle» | `app-simple-movement-list button[aria-label='Anular movimiento']` **[DIN]** | `FE/components/simple-movement-list/simple-movement-list.component.ts:147-152` |

### 3.3 Panel «Nuevo movimiento de caja» — `FE/components/create-movement-dialog/create-movement-dialog.component.ts`
Título «Nuevo movimiento de caja» (:86). Desde Mi caja la sesión viene dada y se muestran «Caja» y
«Cajero» (:119-130).
| Campo | formControlName | Línea | Regla |
|---|---|---|---|
| Tipo de movimiento: «Entrada de efectivo» / «Salida de efectivo» (preseleccionado por el botón) | `type` | :133-152, opciones :591-594 | |
| Monto (RD$) — hint «Saldo disponible: …» | `amount` | :165-191 | >0; en salida no puede exceder el saldo («El monto excede el saldo disponible») |
| ITBIS incluido (opcional) + botón `%` «Calcular ITBIS 18% incluido en el monto» | `taxAmount` | :194-225 | tope = 18/118 del monto |
| Contrapartida: «Cuenta bancaria» / «Cuenta contable» | `counterpartKind` | :230-262 | **Empresa 29 NO tiene cuentas bancarias** → la opción banco sale deshabilitada y el hint «Esta empresa no tiene cuentas bancarias activas…» |
| Cuenta contable (autocompletar, mín. 2 letras, «Buscar cuenta del catálogo...») | `counterpartAccount` (vía autocompletar) | :285-300 | selector `app-autocomplete:has(mat-label:text-is('Cuenta contable')) input` + `mat-option:has-text('Otros ingresos diversos')` **[DIN]** |
| Notas / Justificación (500) | `notes` | :322-339 | **obligatoria en salidas** («La salida de efectivo requiere una nota…») |
| Resumen del movimiento | Tipo · Base · ITBIS incluido · Monto | `.movement-summary` | :342-371 |
Botones: «Cancelar» · **«Crear movimiento»** (:383-399).
Éxito: **toast** «Movimiento MOV-2026-000NN registrado exitosamente» (:1113-1117 del workspace) **[DIN]**;
si supera el umbral (salida > RD$5,000 o entrada > RD$10,000 en la empresa 29) → **toast de
advertencia** «Movimiento MOV-… registrado. Requiere aprobación de un supervisor antes de afectar el
saldo.» y el movimiento queda con estado «Por aprobar» (`FE/enums/movement-status.enum.ts:11`)
fuera del saldo. Transferencias: «Por recibir» (PENDING) · «Pendiente de aprobación» · «Recibida»
(`FE/enums/transfer-status.enum.ts:20-26`).
Cuentas contables que ya usa la BD como contrapartida (catálogo global): **6.03.21 «Otros gastos
generales»** (salidas) y **4.02.01.02 «Otros ingresos diversos»** (entradas).

### 3.4 Anular un movimiento — `FE/components/void-movement-dialog/void-movement-dialog.component.ts`
Título «Anular movimiento» (:46); «Razón de la anulación» `reason` (:112-115); botones «Cancelar» ·
confirmar rojo (:140-150). Éxito: toast «Movimiento anulado exitosamente» (workspace :1301). No se
ofrece en sesiones cerradas; los movimientos de transferencia no se anulan sueltos (API).
«Ver detalle» → «Detalle del movimiento» (`movement-detail-dialog.component.ts:39`, botón «Cerrar» :127).

### 3.5 Cerrar la caja: conteo de cierre (flujo guiado)
1. «Cerrar caja» → primero comprueba pendientes: si hay movimientos por aprobar o transferencias
   salientes sin recibir → diálogo **«Aún no puedes cerrar la caja»** («La sesión tiene N movimiento
   pendiente de aprobación…») botón «Entendido» (:1238-1257).
2. Con la política «Requerir cuadre para cerrar sesión» ✓ (empresa 29) → diálogo **«Conteo de
   cierre requerido»** — «Para cerrar la caja debes registrar el conteo de cierre. ¿Iniciar el conteo
   ahora?» — botón **«Iniciar conteo»** (:1172-1189). Sin la política: «Cerrar caja» / «¿Está seguro
   de que desea cerrar la sesión #N de X?» / botón «Cerrar caja» → toast «Caja cerrada exitosamente».
3. Navega a `/cashier/reconciliation/new?session=<id>&returnUrl=/cashier?section=caja` (:1284-1291)
   → sección 3.6. El botón «Conteo de cierre» hace lo mismo sin pasar por «Cerrar caja» (:1219-1229).

### 3.6 Página «Conteo de cierre (previo al cuadre)» / «Generar cuadre de caja»
Ruta `/cashier/reconciliation/new` (`FE/cashier.routes.ts:83-90`, `CASHIER_RECONCILIATION_CREATE`).
Componente `FE/pages/cashier-reconciliation-form-page/cashier-reconciliation-form-page.component.ts`.
Título según permiso (:1093-1099): Cajero → **«Conteo de cierre (previo al cuadre)»**; con
`CASHIER_RECONCILIATION_CONFIRM` → **«Generar cuadre de caja»**. Botón «Volver» (:91-94).
Stepper lineal de 3 pasos (`mat-stepper`, :116) con rótulos «Seleccionar sesión» · «Ingresar
montos» · «Confirmar cuadre» (`.step-label`, :122, :219, :508).
**Paso 1** (con `?session=` se precarga y el paso se salta):
- «Sesión de caja» (autocompletar, :133-142) **[DIN]**; «Tipo de cuadre» `reconciliationType`
  (:147) con «Cierre normal» · «Arqueo sorpresa» · «Cambio de turno» · «Supervisión» · «Emergencia»
  (`FE/enums/reconciliation-type.enum.ts`); ficha Caja · Cajero · Apertura · Fondo inicial (:161-180).
- **«Continuar»** (:202-212).
**Paso 2 «Ingresar montos»**:
- Sin conteo ciego: «Resumen de la sesión» con «Fondo inicial» · «Cobros del turno» · «Total
  esperado en caja» (+ Copagos/Descuentos/Recargos/«Vueltos entregados» si existen) (:235-291);
  «Desglose del efectivo esperado» con «Ver cálculo» / «Ocultar cálculo» (:296-315).
- Con conteo ciego: nota «Conteo ciego activo: declara los montos contados…» (:226-233).
- Caja estricta: «Conteo de efectivo por denominaciones» (tarjetas) + «No hay efectivo: confirmar
  conteo en RD$0.00» (:320-343).
- «Detalles por método de pago»: por fila Método · Monto esperado · Monto recibido
  (`actualAmount`, :405) · Diferencia · Justificación (`justification`, :444, aparece solo si hay
  diferencia) · botón «Volver al monto esperado» (:411-416); texto «Dentro/Fuera de ±RD$50.00»
  (:430-435). Filas del sistema por cada método con transacciones; «Agregar método de pago»
  (:474-482; agrega fila con `paymentMethod`, :379).
- Selector del monto de efectivo: `.detail-row:has(.method-label:has-text('Efectivo')) input[formcontrolname='actualAmount']` **[DIN]**.
- «Atrás» · **«Siguiente»** (:486-500).
**Paso 3 «Confirmar cuadre»**:
- «Resumen de totales»: «Total esperado» · «Total recibido» (o «Total declarado») · «Diferencia total» (:512-538).
- Un aviso: «Cuadre exacto: los montos recibidos coinciden con lo esperado.» (verde) · «Todos los
  métodos de pago están dentro de la tolerancia.» · «N método de pago queda fuera de tolerancia…»
  (ámbar) (:543-569). Selector `.gm-dialog-alert--success` / `--warning`.
- «Revisa las diferencias» (solo si hay) (:573-595).
- «Justificación global» `globalJustification` (5-250; obligatoria si hay una línea fuera de
  tolerancia sin justificar) (:597-618).
- «Atrás» · **«Registrar conteo»** (Cajero) | **«Generar cuadre»** (Supervisor) (:623-640).
Éxito: **toast** y vuelve a `returnUrl` (:1698-1705). Textos (:1722-1734): Cajero cierre →
«Conteo de cierre registrado exitosamente. Un supervisor hará el cuadre oficial.»; Supervisor →
«Cuadre de caja generado exitosamente. La sesión quedó cerrada.»; arqueo sorpresa →
«Arqueo sorpresa registrado exitosamente. La sesión sigue abierta.»; reconteo → «Reconteo registrado
exitosamente. Queda pendiente de confirmación.» Error → diálogo «No se pudo registrar el conteo» /
«No se pudo generar el cuadre».
**Regla API** (`API/cashier-reconciliation/cashier-reconciliation.service.ts:395-489`): el cuadre nace
`PENDING_CONFIRMATION` y **cierra la sesión en la misma transacción** (salvo arqueo sorpresa); con
pendientes de aprobación responde 400; el control de diferencias consecutivas y el auto-bloqueo se
aplican al CONFIRMAR (:487-489, :898-925).
Ruta extra `/cashier/reconciliation` = lista de cuadres del cajero (`FE/cashier.routes.ts:91-104`).

---

## 4. SUPERVISIÓN / APROBACIÓN — «Por aprobar» (`?section=aprobaciones`)

**Qué es:** lo que espera una decisión del supervisor, en un solo lugar. Ruta heredada
`/cashier/supervision`. **Rol:** Supervisor de Caja / Admin.
Componente `FE/pages/supervision-center/supervision-center.component.ts`.

### 4.1 Cifras (botones que saltan a su lista) — :83-96, definición :442-481
«Movimientos por aprobar» (→ esta sección) · «Transferencias por aprobar» (→ Historial ›
Transferencias) · «Cuadres por confirmar» (→ Historial › Cuadres) · «Alertas activas» (→ Análisis ›
Alertas) · «Cajas bloqueadas» (→ tablero `?estado=bloqueadas`). Selector
`.sup-figs button.gm-fig:has-text('Cuadres por confirmar')`.

### 4.2 Colas (una superficie, tres bloques)
| Cola | Columnas | Acciones (tooltip/aria-label) | Línea |
|---|---|---|---|
| «Movimientos pendientes de aprobación» + «Actualizar» | N° · Tipo · Monto · Caja / Sesión · Solicitado por · Fecha · Nota | `button[aria-label='Aprobar']` · `button[aria-label='Rechazar']` | :102-174 |
| «Transferencias pendientes de aprobación» + «Ver todas» (solo `CASH_TRANSFER_APPROVE`) | N° · Monto · Origen → destino · Solicitado por · Fecha · Nota | `button[aria-label='Aprobar transferencia']` · `…'Rechazar transferencia'` | :178-243 |
| «Cuadres pendientes de confirmación» + «Ver todos» (paginada) | N° · Caja · Cajero · Esperado · Contado · Diferencia · Fecha | `button[aria-label='Ver detalle del cuadre']` · `…'Aprobar cuadre'` · `…'Rechazar cuadre'` | :248-326 |
Fila concreta: `tr:has-text('MOV-2026-00…') button[aria-label='Aprobar']` **[DIN]**.
Vacíos: «No hay movimientos esperando aprobación» / «No hay transferencias…» / «No hay cuadres…».
**⚠ Hoy la cola de cuadres tiene 73 pendientes de QA** (ver `_DATOS-CAJAS.md`).

Diálogos:
- **Aprobar movimiento**: confirmación «Aprobar movimiento» — «¿Está seguro de que desea aprobar MOV-…
  por RD$…? El monto saldrá del saldo de la sesión y se generará su asiento contable.» — botón
  «Aprobar» (:524-549) → toast «Movimiento MOV-… aprobado exitosamente».
- **Rechazar** (movimiento / transferencia / cuadre): `ReasonPromptDialogComponent`
  (`FE/components/reason-prompt-dialog/reason-prompt-dialog.component.ts`): título «Rechazar
  movimiento MOV-…» (:49), banda explicativa (:58-63), «Motivo del rechazo» (textarea con
  `[formControl]`, sin formcontrolname: selector `app-reason-prompt-dialog textarea`, :64-76),
  botones «Cancelar» · «Rechazar» (:80-84) → toast «… rechazado exitosamente».
- **Aprobar transferencia**: «Aprobar transferencia» — «…Después la caja destino podrá recibirla.» —
  «Aprobar» (:581-605).
- **Aprobar cuadre** (desde la fila): «Aprobar cuadre» — «¿Está seguro de que desea aprobar el cuadre
  REC-…? El cuadre es exacto. | Tiene una diferencia de RD$… ya justificada por el cajero. La decisión
  queda firmada a su nombre.» — «Aprobar» (:637-661) → toast «Cuadre REC-… aprobado exitosamente».

### 4.3 Diálogo «Detalle del cuadre de caja» (reconteo del supervisor)
`FE/components/cashier-reconciliation-view-dialog/cashier-reconciliation-view-dialog.component.ts`
(80 % × 81 %). Título «Detalle del cuadre de caja» (:53); detalle `app-cashier-reconciliation-details` (:61).
- «Reconteo de supervisión» + casilla **«Corregir el conteo»** (:66-80): por método «Esperado: … ·
  Cajero declaró: …» y campo «Contado oficial» (`[formControl]`, :92-99); «Justificación de
  supervisión (si hay diferencia)» (:104-108).
- Pie: «Anular cuadre» (izquierda, solo cuadres confirmados) (:128-134) · «Cerrar» · **«Rechazar
  cuadre»** · **«Aprobar cuadre»** (:141-152). Éxito: toast «Cuadre aprobado exitosamente» (:362).
**Cuatro ojos** (`API/…`, QA D-04b): nadie aprueba su propio movimiento/transferencia ni confirma el
cuadre de su propia sesión si en la empresa hay OTRO usuario activo con ese permiso → 403 «No puedes
…: otro supervisor de la empresa debe hacerlo.» ⇒ en el video, quien aprueba NO puede ser quien
creó/operó.
**Auto-bloqueo**: al confirmar el 3.er cuadre consecutivo fuera de tolerancia la caja se bloquea
(«<prefijo> 3 cuadres consecutivos con diferencias fuera de tolerancia»).

### 4.4 Diálogo «Bloquear caja» / «Desbloquear caja» — `FE/components/cashier-block-dialog/cashier-block-dialog.component.ts`
Configs :47-61. Bloquear: «Tipo de bloqueo» `reasonType` (:171-178: «Auditoría pendiente»,
«Diferencias consecutivas», «Actividad sospechosa», «Mantenimiento», «Incidente de seguridad», «Otra
razón») + «Detalle de la razón» `reasonDetail` (mín. 20 caracteres, :186-200). Desbloquear: «Notas de
desbloqueo (opcional)» `notes` (:204-209), «Resetear contador de diferencias consecutivas»
`resetDifferences` (:216), **«Confirmo que he verificado las condiciones de la caja y es seguro
desbloquearla»** `confirmed` (:223, obligatoria). Botones «Cancelar» · «Bloquear caja» |
«Desbloquear caja» (:240-253). Desde: ⋮ de Configuración › Cajas y botón «Desbloquear» del tablero.

---

## 5. CONSULTAS — «Historial» (`?section=historial`)

**Qué es:** lo ya ocurrido en todas las cajas. Rutas heredadas `/cashier/operations?tab=`.
**Rol:** Supervisor / Admin (el Cajero NO lo ve). Pestaña interna `?tab=sesiones|movimientos|
transferencias|cuadres`, filtro de caja `?cashier=<id>` (desde el ⋮ del tablero).
Sub-pestañas `nav[aria-label='Listados del historial'] button:has-text('Sesiones')`
(`FE/pages/operations-center/operations-center.component.ts:55-66, :102-105`).

| Pestaña | Columnas | Acciones de barra | Acciones de fila | Archivo:línea |
|---|---|---|---|---|
| Sesiones | Caja · Cajero · Estado · Modo · Apertura · Cierre · Notas | ⋮ → «Abrir sesión para un cajero» (`CASHIER_SESSION_DELETE`, → `/cashier/sessions/create`) | «Ver detalles» · «Editar» · «Reabrir» | `FE/pages/session-list/session-list.component.ts:79-90, :117-126, :159-170` |
| Movimientos | Número · Fecha · Tipo · Estado · Monto · Caja · Cajero · Autorizado por | «Nuevo movimiento» · ⋮ «Exportar movimientos a Excel» | «Ver detalle» · «Anular» | `FE/pages/cash-movement-list/cash-movement-list.component.ts:128-142, :172-180, :224-236` |
| Transferencias | N° de transferencia · Monto · Caja origen · Caja destino · Estado · Solicitante · Fecha | **«Nueva transferencia»** · ⋮ «Exportar transferencias a Excel» | «Aprobar» · «Rechazar» · **«Recibir»** · «Cancelar» | `FE/pages/cash-transfer-list/cash-transfer-list.component.ts:160-172, :204-211, :237-253` |
| Cuadres | N° de cuadre · Caja · Esperado · Contado · Diferencia · Estado · Tolerancia · Supervisor · Fecha | «Nuevo cuadre» (→ 3.6) · ⋮ «Exportar cuadres a Excel» | «Ver» · «Recontar la sesión» (rechazado/anulado) · «Anular cuadre» (confirmado) | `FE/pages/cashier-reconciliation-list/cashier-reconciliation-list.component.ts:115-129, :159-168, :214-233` |

Diálogos:
- **Nueva transferencia entre cajas** (`FE/components/cash-transfer-form/cash-transfer-form.component.ts`):
  título (:39); «Caja origen» `sourceCashier` (:56) · «Caja destino» `targetCashier` (:77) · «Monto
  a transferir» `amount` (:96, hint «Saldo disponible en sesión: …») · «Notas (opcional)» `notes`
  (:116); «Cancelar» · **«Crear transferencia»** (:122-138). Reglas API: origen y destino distintos,
  ambas activas y no bloqueadas, origen con sesión abierta y saldo; sobre RD$5,000 (umbral de retiros)
  → «Pendiente de aprobación». Toasts (`cash-transfer-list:425-427`): «Transferencia creada
  exitosamente. La caja destino ya puede recibirla.» | advertencia «Transferencia creada. Supera el
  monto permitido sin aprobación: un supervisor debe aprobarla antes de recibirla.»
- **Recibir transferencia** (`FE/components/receive-transfer-dialog/receive-transfer-dialog.component.ts`):
  ficha N° · Monto a recibir · Origen · Destino (:47-64); nota (:66-70); error si el destino no tiene
  sesión abierta (:73-78); «Cancelar» · **«Confirmar recepción»** (:82-93) → toast «Transferencia
  recibida exitosamente». Solo el cajero de la sesión destino o un supervisor (API).
- **Reabrir sesión**: `ReasonPromptDialogComponent` «Reabrir sesión #N», «Motivo de la reapertura»,
  «Reabrir sesión» (`session-list:293-312`) → toast «Sesión #N reabierta exitosamente». API: solo la
  última sesión de la caja, dentro de 24 h, sin cuadre/conteo.
- «Ver» cuadre → 4.3.

---

## 6. CONSULTAS — «Análisis» (`?section=analisis`)

**Qué es:** estado en vivo, reportes del período, alertas y auditoría. Rutas heredadas
`/cashier/dashboard`, `/cashier/reports`, `/cashier/monitoring` (→ `tab=alertas`).
Componente `FE/pages/analytics-center/analytics-center.component.ts`.
- Sub-pestañas (:140-150, :400-407): «Reporte diario» · «Cuadres y análisis» · «Rendimiento» ·
  «Alertas» · «Auditoría» (`?tab=diario|cuadres|rendimiento|alertas|auditoria`).
- Botón actualizar (icono `refresh`, tooltip «Actualizar ahora · Última actualización: …») (:153-160).
- Cifras en vivo (:186-217, :449-485): «Sesiones activas» · «Cajas abiertas» (x/y) · «Bloqueadas» ·
  «Cuadres pendientes» · «Efectivo en cajas» · «Alertas activas» (las que tienen destino son botones).
- Filtro del período (Reporte diario / Cuadres / Rendimiento) (:220-268): «Período» (Hoy · Últimos 7
  días · Este mes · Mes anterior · Últimos 90 días · Este año · Personalizado), «Fecha desde», «Fecha
  hasta», autocompletar «Caja». Selector `mat-form-field:has(mat-label:text-is('Período')) mat-select`.
- Contenido: `app-analytics-daily-section` · `app-analytics-reconciliations-section` ·
  `app-analytics-performance-section` · `app-cashier-alert-list` (acciones «Reconocer» · «Resolver» ·
  «Descartar», `FE/pages/cashier-alert-list/cashier-alert-list.component.ts:212-222`; diálogo
  «Resolver alerta», `resolve-alert-dialog.component.ts:30`) · `app-audit-log` (filtros acción,
  entidad, usuario, fechas).

---

## 7. Fuera de la vista única (mencionar, no grabar salvo decisión)
- `/cashier/sessions/create` y `/cashier/sessions/:id/edit` (`FE/cashier.routes.ts:105-117`):
  apertura de sesión a nombre de otro cajero (gestión).
- Modo **Estaciones** (vincular navegador ↔ caja, «Solicitar vinculación», bandeja de aprobación,
  «Desvincular dispositivo»): la empresa 29 está en Flexible (`company_configs.cashier_station_mode=OFF`);
  exige cambiar la política. No entra en la serie mínima.
- **Cobro de facturas en caja**: no se hace en Cajas. El diálogo de cobro de Ventas/CxC resuelve la
  sesión abierta del usuario (`germiva-website/src/app/modules/accounting/shared/payments/portfolio-payment-dialog.component.ts:296-330`)
  y el cobro en efectivo suma a «Cobros del turno» del desglose. **Moneda extranjera**: la gaveta suma
  el equivalente en moneda local (QA D-03/D-23).
- Impresora/gaveta (`printer-config-dialog`), detalle de caja, audit entry dialog.

---

## 8. Glosario que el video debe explicar
| Término | Explicación para un novato |
|---|---|
| Caja | Un punto de cobro físico (una gaveta con su efectivo): «Caja Principal», «Caja Mostrador 2». |
| Sesión (turno) | El período en que UN cajero opera una caja: se abre con un fondo y se cierra con un conteo. Una caja solo tiene una sesión abierta a la vez y un cajero solo una caja. |
| Fondo de caja / fondo inicial | El efectivo con que arranca la gaveta (el «cambio»). Política: 5,000 por defecto. **Fondo fijo**: monto que el supervisor fija para una caja y el cajero no puede cambiar. |
| Entrada / Salida | Dinero que entra o sale de la gaveta sin ser un cobro (cambio que trae el dueño, pago de un mensajero). Cada una lleva contrapartida contable (de dónde viene / a dónde va). |
| Contrapartida | La cuenta bancaria o contable del otro lado del asiento. |
| Umbral de aprobación | Montos por encima de los cuales el movimiento queda «Pendiente» y no toca el saldo hasta que un supervisor lo apruebe (retiros > 5,000; depósitos > 10,000). |
| Transferencia entre cajas | Mover efectivo de una caja a otra: sale del origen al crearla y entra al destino cuando la caja destino confirma la recepción. |
| Desglose del efectivo / efectivo esperado | Fondo + cobros en efectivo + entradas − salidas ± transferencias = lo que DEBE haber. |
| Arqueo | Contar el dinero físico de la gaveta. **Arqueo sorpresa**: conteo sin aviso durante el turno; no cierra la sesión. |
| Conteo de cierre | El arqueo que declara el cajero al terminar: es un PREVIO; cierra su sesión. |
| Cuadre | Comparar lo contado con lo esperado, método por método; el cuadre OFICIAL lo aprueba (o rechaza) el supervisor. |
| Diferencia / sobrante / faltante | Contado − esperado: positivo = sobrante, negativo = faltante. |
| Tolerancia | Diferencia aceptable por método de pago (empresa 29: RD$50 en monto fijo); fuera de ella hay que justificar. |
| Justificación | Explicación escrita de una diferencia fuera de tolerancia (por línea o global, 5-250 caracteres). |
| Denominación | Cada billete o moneda (RD$2,000 … RD$1) con que se cuenta billete por billete. |
| Modo estricto (control por denominaciones) | La caja exige contar por denominaciones al abrir y al cerrar, y el conteo debe cuadrar con el fondo. |
| Conteo ciego | El cajero declara lo contado sin ver el esperado ni la diferencia; el supervisor lo ve al confirmar. |
| Cuatro ojos | Quien hace una operación no puede aprobarla: la aprueba otro supervisor. |
| Bloqueo | Una caja bloqueada no puede abrir sesión: manual (supervisor) o automático tras 3 cuadres seguidos fuera de tolerancia. Desbloquear exige confirmar y puede resetear el contador. |
| Reapertura | Volver a abrir una sesión cerrada (solo la última de la caja, 24 h, sin cuadre): evento auditado con motivo. |
| Reconteo | Nuevo cuadre de una sesión cuyo cuadre fue rechazado o anulado. |
