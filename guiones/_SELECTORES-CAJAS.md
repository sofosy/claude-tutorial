# Selectores VERIFICADOS de la serie «Cajas» (DOM vivo, empresa demo 43)

Carril DATOS+EXPLORACIÓN · 2026-09-23. Medido con `seeds/cajas/explorar.py` (Playwright headless,
1280×720, dsf 1.5, login real por la UI con el ROL que graba cada video). Cada selector de esta
tabla se usó de verdad en el recorrido o se contó en vivo (`n/m` = visibles/total; `1/1` = único).
Evidencia por pantalla: `guiones/exploracion-cajas/<video>-<pantalla>.png/.json`
(+ `verificacion-selectores.json`). Datos y estados: `_DATOS-CAJAS.md`. Hallazgos: `_HALLAZGOS-CAJAS.md`.

**Reglas transversales comprobadas**
- Login: `input[formcontrolname='username']`, `input[formcontrolname='password']`,
  `button.auth-primary-btn`. Ningún modal al entrar para los 4 usuarios demo (R18 sembrado).
  Navegar SIEMPRE por `http://localhost:4200`.
- Ítem del riel «Cajas»: `a[href='/cashier']` (1/1). **No existe `button.panel-collapse`** en esta
  versión (0/0): el menú es un riel de iconos fijo, no hay panel que contraer → quitar ese
  `click_opcional` de la receta R5 para Cajas.
- Pestañas de la vista única: `#cashier-hub-tab-cajas|caja|aprobaciones|historial|analisis` (1/1).
  La cajera solo tiene `#cashier-hub-tab-cajas` y `#cashier-hub-tab-caja`.
- **Toasts** (`.mat-mdc-snack-bar-container`, abajo-centro, ≈ x 460-800 · y 660-706, botón
  «Cerrar»): el texto capturado va sin «Cerrar». Duran 3,5 s → `resaltar` inmediato.
- Confirmaciones: `.custom-alert-dialog-style button.confirm-button` (funcionó en Aprobar
  movimiento, Conteo de cierre requerido y la «Confirmación» del detalle del cuadre).
- Diálogos propios: `mat-dialog-container` + `button:has-text('…')`; cerrar con la X
  `button[aria-label='Cerrar']` o `button.cashier-sheet-close` (paneles).
- **Chatbot** `.chatbot-fab` = [1200, 640, 56, 56] (verificado). Solo estorba sin overlay;
  ver «choca con FAB» en cada video.
- Campos: `formcontrolname` se refleja siempre (verificado en todos los formularios). `matTooltip`
  estático SÍ se refleja como `mattooltip` (p. ej. `button[mattooltip='Recibir']`).
- Escribir en inputs: `click` + teclear. En el campo «Orden de visualización» el `mat-label`
  intercepta el clic → hacer clic en el input con `force` o enfocar (el motor usa `click`; si
  falla, marcar en el guion `teclear` sobre `mat-form-field:has(mat-label:text-is('Orden de visualización')) input`).

---

## Video 1 — tablero y tus cajas · `admin.progreso` · S0

| Paso | Acción | Selector verificado | Texto exacto observado |
|---|---|---|---|
| 01 | navegar | `/cashier?section=cajas` | Título «Cajas»; subtítulo «Estado de cada caja: ábrela, continúa tu turno o revisa quién la opera.» |
| 01 | tarjetas | `article.board-card[aria-label='Caja Caja Mostrador 2']` · `…'Caja Caja Sucursal Santiago'` · `…'Caja Caja Principal'` (1/1 c/u) | Orden: Mostrador 2 (Abierta) · Santiago (Bloqueada) · Principal (Cerrada). Mostrador 2: «La opera luis.batista · Abierta hace 2 h · Efectivo en caja RD$6,050.00» + botón «Ver sesión». Santiago: «Última actividad 22/09/2026 17:40» + «Desbloquear». Principal: «Última actividad 22/09/2026 14:05» + «Abrir sesión». |
| 01 | filtros | `.board-toolbar nav button.segmented__option:has-text('Abiertas')` / `…('Todas')` | «Todas 3 · Abiertas 1 · Cerradas 2 · Bloqueadas 1»; URL pasa a `&estado=abiertas` |
| 01 | ⋮ tarjeta | `article.board-card[aria-label='Caja Caja Mostrador 2'] button.board-card__menu` (aria «Más acciones») | Menú admin: «Movimientos · Sesiones · Cuadres · Configurar caja» (`.mat-mdc-menu-panel button:has-text('…')`) |
| 02 | Nueva caja | `button.board-toolbar__new` | Diálogo «Nueva caja» [360,63,560,594], secciones INFORMACIÓN GENERAL · MÉTODOS DE PAGO ACEPTADOS · MODO DE OPERACIÓN · MONTOS Y LÍMITES |
| 02 | campos | `.cashier-form-dialog input[formcontrolname='name'|'code'|'location'|'fixedFund'|'minCashLimit'|'maxCashLimit']`; casillas `mat-checkbox:has-text('Transferencia')` (por defecto ✓Efectivo ✓Tarjeta ✗Transferencia) | Hints: «Monto base que permanece en la caja (opcional)», «Umbral de alerta por saldo bajo (opcional)», «Umbral de alerta por exceso de efectivo (opcional)» |
| 02 | crear | `.cashier-form-dialog button:has-text('Crear caja')` (deshabilitado hasta llenar Nombre, Código y Ubicación) | Toast **«Caja creada exitosamente»**; la tarjeta «Caja Mostrador 3» entra 3.ª (Cerrada) y la de Principal pasa a x 970 |
| 03 | panel | `.page-hero-actions button:has-text('Configuración')` | Panel «Configuración de cajas» [320,0,960,720]; cifras TOTAL DE CAJAS · ABIERTAS · CERRADAS · BLOQUEADAS; filtros Tipo/Estado/Bloqueada; tabla CAJA · UBICACIÓN · TIPO · ESTADO · BALANCE · MÉTODOS · DISPOSITIVO |
| 03 | ⋮ fila | `tr:has-text('Caja Mostrador 3') button:has(mat-icon:text-is('more_vert'))` | Menú «Ver detalles · Bloquear · Archivar» |
| 03 | archivadas | `.toolbar-archived button:has-text('Archivadas')` / `…('Operativas')` | vacío «No hay cajas archivadas» |
| 03 | cerrar | `.settings-sheet__header button.cashier-sheet-close` | vuelve al tablero |

No cabe / choca: el diálogo «Nueva caja» hace scroll interno (Límite mín./máx. en y 663 → fuera
hasta teclear o desplazar). En el panel la 4.ª fila de la tabla queda bajo el pliegue (y 749) y la
paginación en y 836. Sin choque con el FAB (el panel lo tapa).

## Video 2 — denominaciones y políticas · `admin.progreso` · S0

| Paso | Acción | Selector verificado | Texto exacto observado |
|---|---|---|---|
| 01 | navegar | `/cashier?section=cajas&config=denominaciones` | Nota «Billetes y monedas disponibles para los conteos y cuadres de caja.»; grupos BILLETES / MONEDAS |
| 01 | Nueva | `button:has-text('Nueva denominación')` | Diálogo «Nueva denominación» [340,180,600,360] |
| 01 | campos | `mat-dialog-container input[formcontrolname='nameCount'|'valueCount'|'sort']`, divisa `mat-select[formcontrolname='currency']` (ya «DOP — Peso dominicano»), tipo `mat-dialog-container .type-seg button:has-text('Billete')` | — |
| 01 | crear | `mat-dialog-container button:has-text('Crear denominación')` | Toast **«Denominación creada exitosamente»**. Verificado en BD: nace con `company_id=43` (no toca el catálogo global) |
| 02 | Políticas | `nav.segmented--sub button.segmented__option:has-text('Políticas')` | «Políticas de operación» — «Reglas globales que aplican a todas las cajas: fondos, tolerancias, sesiones, aprobaciones y cuadres.» |
| 02 | campos | `input[formcontrolname='defaultInitialCash'|'minInitialCash'|'maxInitialCash'|'toleranceAmount'|'tolerancePercentage'|'maxConsecutiveDifferences'|'maxSessionDurationMinutes'|'maxWithdrawalWithoutApproval'|'maxDepositWithoutApproval'|'alertThresholdLow'|'alertThresholdHigh'|'reconciliationConfirmationHours']`; `mat-select[formcontrolname='toleranceMode']` | Valores S0: 5000.00 · vacío · vacío · Monto fijo · 50.00 · 1.00 (deshabilitado) · 3 · 720 («720 = 12 horas») · 5000.00 · 10000.00 · vacío · vacío · 24. Casillas: «Operar con estaciones vinculadas» ✗ (sin formcontrolname) · «Permitir operación en días feriados» ✗ · «Requerir notas para retiros» ✓ · «Requerir cuadre para cerrar sesión» ✓ · «Requerir justificación para diferencias» ✓ · «Conteo ciego en el cuadre» ✗ |
| 03 | guardar | `button[type=submit]:has-text('Guardar configuración')` (pie fijo del panel, [1032,668]) | Toast **«Configuración de cajas guardada exitosamente»** |

Scroll: el formulario de Políticas mide ≈ 1 650 px; 4 pasos de rueda de 600 px llegan al final.
Los umbrales de alerta quedan a y 680 tras el 1.er scroll. El FAB queda bajo el panel (no estorba).

## Video 3 — abre tu caja y registra · `yohanna.peralta` (Cajera) · S1 → S3

| Paso | Acción | Selector verificado | Texto exacto observado |
|---|---|---|---|
| 01 | navegar | `/cashier?section=cajas` (sin `section` también cae en el tablero: no tiene sesión) | Solo pestañas «Cajas · Mi caja». Mostrador 2 dice **«En uso»**; Santiago **«Bloqueada: [Auditoría pendiente] Faltante de efectivo en el último arqueo; pendiente de revisión con la gerencia»** (`.board-card__note`) |
| 01 | abrir | `article.board-card[aria-label='Caja Caja Principal'] .board-card__foot button:has-text('Abrir sesión')` | Panel «Abrir mi caja» — «Confirma el fondo inicial y el conteo para empezar a operar». Caja «Caja Principal» (hint «Caja elegida en el tablero de Cajas»), Cajero **«yohanna.peralta@germiva.demo»** («La sesión se abrirá a tu nombre»), Fondo inicial 5000 («Efectivo inicial en caja al abrir la sesión»), Conteo del fondo: «Esta caja no requiere conteo por denominaciones al abrir. Un supervisor puede exigirlo activando el control por denominaciones en la configuración de la caja.» |
| 01 | notas | `mat-dialog-container textarea[formcontrolname='notes']` | — |
| 01 | confirmar | `mat-dialog-container button:has-text('Abrir caja')` ([1145,676]) | Toast **«Caja abierta exitosamente»** → salta a `?section=caja`: barra «Caja abierta · Caja Principal · RD$5,000.00 · yohanna.peralta · abierta hace unos segundos» |
| 02 | Entrada | `button.quick-action--in` | Panel «Nuevo movimiento de caja» [760,0,520,720]; «CAJA Caja Principal · CAJERO yohanna.peralta»; Tipo «Entrada de efectivo» — «Ingreso de efectivo a la caja (ventas, depósitos, etc.)» |
| 02 | monto | `mat-dialog-container input[formcontrolname='amount']` | — |
| 02 | cuenta | `mat-dialog-container app-autocomplete:has(mat-label:text-is('Cuenta contable')) input` → teclear «Otros ingresos» → `mat-option:has-text('Otros ingresos diversos')` | Queda «4.02.01.02 - Otros ingresos diversos». Contrapartida fija «Cuenta contable» con el aviso «Esta empresa no tiene cuentas bancarias activas: la contrapartida se registra en una cuenta contable.» (ver H-03: pisa la etiqueta) |
| 02 | nota | `mat-dialog-container textarea[formcontrolname='notes']` (contador «34/500») | — |
| 02 | crear | `mat-dialog-container button:has-text('Crear movimiento')` | Toast **«Movimiento MOV-2026-00009 registrado exitosamente»**; desglose: ENTRADAS (1) RD$2,000.00 · EFECTIVO ESPERADO RD$7,000.00 |
| 03 | Salida | `button.quick-action--out` | Tipo «Salida de efectivo» — «Retiro de efectivo de la caja (pagos, gastos, etc.)»; hint «Saldo disponible: RD$7,000.00» |
| 03 | ITBIS | `mat-dialog-container button:has(mat-icon:text-is('percent'))` (deshabilitado sin monto) | 6,500 → **991.53** |
| 03 | cuenta | igual que 02 con «Otros gastos» → `mat-option:has-text('Otros gastos generales')` | «6.03.21 - Otros gastos generales»; la nota es obligatoria: «La salida de efectivo requiere una nota que justifique el retiro» |
| 03 | resumen | `mat-dialog-container .movement-summary` (requiere scroll interno) | — |
| 03 | crear | `mat-dialog-container button:has-text('Crear movimiento')` | Toast de advertencia **«Movimiento MOV-2026-00010 registrado. Requiere aprobación de un supervisor antes de afectar el saldo.»** Saldo sigue 7,000 |
| 04 | pestañas | `.workspace-tabs .mat-mdc-tab:has-text('Resumen')` / `…('Movimientos')` | La cajera NO ve «Alertas». Bajo Movimientos: chips «Sesión · Hoy · Ayer · Semana» |
| 04 | fila | `app-simple-movement-list button[aria-label='Ver detalle']` / `[aria-label='Anular movimiento']` (1 por fila; la fila nueva es la 1.ª) | «Detalle del movimiento» (N° MOVIMIENTO, TIPO, MONTO, ESTADO «Por aprobar», …) botón `button:has-text('Cerrar')`; «Anular movimiento» con «Atención: Esta acción es irreversible…» y «Razón de la anulación» `textarea[formcontrolname='reason']`, botón deshabilitado hasta escribir |
| alt | cerrar con pendiente | `.session-bar__actions button:has-text('Cerrar caja')` | Diálogo **«Aún no puedes cerrar la caja» — «La sesión tiene 1 movimiento pendiente de aprobación. Un supervisor debe aprobarlos o rechazarlos (o cancela la transferencia) antes del cuadre y el cierre.»** botón «Entendido» |

No cabe / choca: en Mi caja la lista de movimientos empieza en y ≈ 692 (las filas y sus botones
en y 774/865 → desplazar antes de señalarlas). La barra de pestañas Movimientos|Resumen llega a
x 1252 y el FAB tapa su extremo derecho (clic en el texto, x ≈ 968, está libre). El toast cae
sobre la zona de pestañas.

## Video 4 — aprobar y transferir · `carmen.rosario` (Supervisora) · S3 → S4

| Paso | Acción | Selector verificado | Texto exacto observado |
|---|---|---|---|
| 01 | navegar | `/cashier?section=aprobaciones` | Subtítulo «Movimientos, transferencias y cuadres que esperan una decisión del supervisor.»; pestaña «Por aprobar 1» (`#cashier-hub-tab-aprobaciones`); cifras `.sup-figs button.gm-fig`: «0 Transferencias por aprobar · 0 Cuadres por confirmar · 1 Alertas activas · 1 Cajas bloqueadas» (la de movimientos no sale como botón aparte en la medición) |
| 01 | cola | tabla N° · TIPO · MONTO · CAJA / SESIÓN · SOLICITADO POR · FECHA · NOTA · DECISIÓN | fila «MOV-2026-00010 · Salida · RD$6,500.00 · Caja Principal · #513 · yohanna.peralta · … · Pago del mantenimiento del aire acondicionado». Botones `tr:has-text('MOV-2026-00010') button[aria-label='Aprobar']` / `[aria-label='Rechazar']` [1168/1202, 421] |
| 01 | aprobar | `…button[aria-label='Aprobar']` → `.custom-alert-dialog-style button.confirm-button` | Diálogo **«Aprobar movimiento» — «¿Está seguro de que desea aprobar MOV-2026-00010 por RD$6,500.00? El monto saldrá del saldo de la sesión y se generará su asiento contable.»** → toast **«Movimiento MOV-2026-00010 aprobado exitosamente»**. «Alertas activas» pasa a 2 (nace ALT-2026-00002 saldo bajo: 500 < 1,000) |
| 02 | navegar | `/cashier?section=historial&tab=transferencias` | sub-pestañas `nav[aria-label='Listados del historial'] button:has-text('Sesiones'|'Movimientos'|'Transferencias'|'Cuadres')` (1/1) |
| 02 | nueva | `button:has-text('Nueva transferencia')` | Diálogo «Nueva transferencia entre cajas» [340,110,600,500]; nota «La caja origen debe tener una sesión abierta. El monto se valida contra su saldo disponible.» |
| 02 | campos | `mat-dialog-container mat-select[formcontrolname='sourceCashier']` → `mat-option:has-text('Caja Mostrador 2')`; `…[formcontrolname='targetCashier']` → `mat-option:has-text('Caja Principal')`; `input[formcontrolname='amount']`; `textarea[formcontrolname='notes']` | Opciones: «Caja Mostrador 2 (CAJA-02)», «Caja Principal (CAJA-01)»; hint **«Saldo disponible en sesión: RD$6,050.00»** |
| 02 | crear | `mat-dialog-container button:has-text('Crear transferencia')` | Toast **«Transferencia creada exitosamente. La caja destino ya puede recibirla.»**; fila «TRF-2026-00001 · RD$3,000.00 · Caja Mostrador 2 · Caja Principal · Por recibir · carmen.rosario» |
| 03 | recibir | `tr:has-text('TRF-2026-00001') button[mattooltip='Recibir']` (icono `inventory`, SIN aria-label) | Diálogo «Recibir transferencia»: «N° TRANSFERENCIA TRF-2026-00001 · MONTO A RECIBIR RD$3,000.00 · ORIGEN Caja Mostrador 2 · DESTINO Caja Principal — Al confirmar, la caja destino registra una entrada por el monto enviado. Si el efectivo recibido no coincide, no confirmes: pide que se cancele la transferencia y que se registre de nuevo por el monto correcto.» |
| 03 | confirmar | `mat-dialog-container button:has-text('Confirmar recepción')` | Toast **«Transferencia recibida exitosamente»**; estado «Recibida». La alerta de saldo bajo se RESUELVE sola («Resuelta automáticamente: el saldo de la caja volvió al rango configurado.») |

Choca: la paginación de la tabla (y 633-643) roza el FAB; la acción «Recibir» (y 579) está libre.
Explicar «Rechazar» sin pulsarlo.

## Video 5 — cierre con conteo · `yohanna.peralta` · S4 → S5

| Paso | Acción | Selector verificado | Texto exacto observado |
|---|---|---|---|
| 01 | navegar | `/cashier?section=caja` | Desglose: FONDO 5,000 + COBROS 0 + ENTRADAS 5,000 (entrada + transf. recibida) − SALIDAS 6,500 … = ESPERADO 3,500 (`section.breakdown-panel`) |
| 01 | cerrar | `.session-bar__actions button:has-text('Cerrar caja')` | Diálogo **«Conteo de cierre requerido» — «Para cerrar la caja debes registrar el conteo de cierre. ¿Iniciar el conteo ahora?»** botones «Cancelar» · «Iniciar conteo» |
| 01 | iniciar | `.custom-alert-dialog-style button.confirm-button` | Página `/cashier/reconciliation/new?session=<id>&returnUrl=…` — **«Conteo de cierre (previo al cuadre)»** / «Cuenta el dinero de tu sesión y declara los montos. Un supervisor hará el cuadre oficial con tu conteo (puede recontar).»; ya en el paso «Ingresar montos» (`mat-step-header:has-text('Ingresar montos')`) |
| 02 | cálculo | `button:has-text('Ver cálculo')` → «Ocultar cálculo» | Desglose del efectivo esperado RD$3,500.00 |
| 02 | monto | `.detail-row:has(.method-label:has-text('Efectivo')) input[formcontrolname='actualAmount']` (1/1; también `[aria-label='Monto recibido']`) | Prellenado 3500; con 3480 → **«−RD$20.00 · Dentro de ±RD$50.00»**; aparece `input[formcontrolname='justification']` (placeholder «¿Por qué la diferencia?»). Ver H-04: dice «0 transacciones» |
| 02 | siguiente | `button:has-text('Siguiente')` (y 781 sin scroll → FUERA de 720; tras abrir cálculo y 928) | — |
| 03 | confirmar | página paso 3 | «Resumen de totales», «Revisa las diferencias 1», aviso **«Todos los métodos de pago están dentro de la tolerancia. Tolerancia por método: ±RD$50.00.»**, «Justificación global» `textarea[formcontrolname='globalJustification']` (label «Justificación del cuadre (opcional)», hint «Opcional. Mínimo 5 caracteres») |
| 03 | registrar | `button:has-text('Registrar conteo')` (y 785 → desplazar) | Toast **«Conteo de cierre registrado exitosamente. Un supervisor hará el cuadre oficial.»** → vuelve a Mi caja: «No tienes una sesión activa» + `button:has-text('Abrir mi caja')` / `button:has-text('Ver todas las cajas')` |

No cabe: la página de conteo mide ≈ 1 000 px; «Siguiente» y «Registrar conteo» están bajo el
pliegue → `desplazar` antes. La justificación global del paso 3 cruza la zona del FAB.

## Video 6 — cuadre oficial, arqueo, desbloqueo · `carmen.rosario` · S5 → S6

| Paso | Acción | Selector verificado | Texto exacto observado |
|---|---|---|---|
| 01 | navegar | `/cashier?section=aprobaciones` | «Cuadres pendientes de confirmación 1»: fila «REC-2026-00007 · Caja Principal · yohanna.peralta · RD$3,500.00 · RD$3,480.00 · −RD$20.00». La cola está en y ≈ 889 → desplazar |
| 01 | detalle | `button[aria-label='Ver detalle del cuadre']` (también `'Aprobar cuadre'`, `'Rechazar cuadre'`) | Diálogo «Detalle del cuadre de caja» [128,68,1024,583]: RESULTADO, DESGLOSE DEL EFECTIVO ESPERADO, TOTALES POR MÉTODO DE PAGO (con la justificación «Faltan 20 pesos en monedas»), RECONTEO DE SUPERVISIÓN |
| 01 | reconteo | `mat-dialog-container mat-checkbox:has-text('Corregir el conteo')` | Muestra «Contado oficial» (3480) y «Justificación de supervisión (si hay diferencia)»; se desmarca |
| 01 | aprobar | `mat-dialog-container button:has-text('Aprobar cuadre')` → segunda confirmación `.custom-alert-dialog-style button.confirm-button` | **«Confirmación» — «¿Estás seguro que deseas APROBAR este cuadre de caja?»** (H-06) → toast **«Cuadre aprobado exitosamente»**. Genera el asiento del faltante (ASI de REC-2026-00007) |
| 02 | navegar | `/cashier?section=historial&tab=cuadres` → `button:has-text('Nuevo cuadre')` | Página **«Generar cuadre de caja»** / «Cuenta el dinero de la sesión, compara contra lo esperado y confirma el cuadre.» |
| 02 | sesión | `app-autocomplete:has(mat-label:text-is('Sesión de caja')) input` → teclear «Mostrador» → `mat-option:has-text('Caja Mostrador 2')` | Opción «Caja Mostrador 2 · Área de pinturas y herramientas · abierta 23/09/2026 hh:mm»; hint «Sesiones abiertas, o cerradas con un cuadre rechazado o anulado (reconteo)» |
| 02 | tipo | `mat-select[formcontrolname='reconciliationType']` → `mat-option:has-text('Arqueo sorpresa')` | Nota «Arqueo sorpresa. Verificación no programada del efectivo en caja. No cierra la sesión: la caja sigue operando.» |
| 02 | continuar | `button:has-text('Continuar')` **[1102,671] TAPADO por el FAB** → desplazar antes | — |
| 02 | monto | `.detail-row:has(.method-label:has-text('Efectivo')) input[formcontrolname='actualAmount']` = **3050** (esperado de luis tras enviar 3,000) | paso 3: **«Cuadre exacto: los montos recibidos coinciden con lo esperado.»**; con otro monto sale «1 método de pago queda fuera de tolerancia…» y «Generar cuadre» se deshabilita |
| 02 | generar | `button:has-text('Generar cuadre')` | Toast **«Arqueo sorpresa registrado exitosamente. La sesión sigue abierta.»**; REC-2026-00008 queda «Pendiente» (H-11) |
| 03 | navegar | `/cashier?section=cajas&estado=bloqueadas` | una tarjeta; `article.board-card[aria-label='Caja Caja Sucursal Santiago'] .board-card__foot button:has-text('Desbloquear')` |
| 03 | diálogo | — | «Desbloquear caja»: CAJA Caja Sucursal Santiago · CÓDIGO CAJA-SAN · SALDO ACTUAL RD$0.00 · RAZÓN … · FECHA DE BLOQUEO 22/09/2026 17:40 · **BLOQUEADO POR Sistema** (H-13); `textarea[formcontrolname='notes']`; `mat-checkbox[formcontrolname='resetDifferences']` (marcada, «Actual: 0 diferencias»); `mat-dialog-container mat-checkbox:has-text('Confirmo')` |
| 03 | desbloquear | `mat-dialog-container button:has-text('Desbloquear caja')` (deshabilitado hasta marcar «Confirmo…») | Toast **«Caja «Caja Sucursal Santiago» desbloqueada exitosamente»**. Con el filtro Bloqueadas la lista queda VACÍA («Limpiar filtros») → para mostrarla «Cerrada» volver a «Todas». La alerta ALT-2026-00001 pasa a Resuelta |

## Video 7 — historial y análisis · `carmen.rosario` · S6 (solo lectura)

| Paso | Acción | Selector verificado | Texto exacto observado |
|---|---|---|---|
| 01 | ⋮ tarjeta | `article.board-card[aria-label='Caja Caja Principal'] button.board-card__menu` → `.mat-mdc-menu-panel button:has-text('Sesiones')` | La supervisora ve «Movimientos · Sesiones · Cuadres» (sin «Configurar caja»). URL `?section=historial&tab=sesiones&cashier=49` |
| 01 | sesiones | fila: `button:has(mat-icon:text-is('visibility'|'edit'|'lock_open'))` (tooltips «Ver detalles», «Editar», «Reabrir»; sin aria-label) | 4 sesiones de Principal: hoy (yohanna, Cerrada, 05:10→05:12 del recorrido) y D-1…D-3 |
| 01 | pestañas | `nav[aria-label='Listados del historial'] button:has-text('Movimientos'|'Transferencias'|'Cuadres')` | Movimientos (7): «MOV-2026-00012 Transferencia TRF-2026-00001 de Caja Mostrador 2 · Transferencia recibida · Completado»; «MOV-2026-00010 … · Salida · Aprobado · RD$6,500.00 ITBIS RD$991.53 · Autorizado por yohanna.peralta» (H-02). Transferencias con filtro «Caja origen = Caja Principal» sale VACÍA (el ⋮ filtra por origen). Cuadres (4) REC-00007 Confirmado · Supervisor carmen.rosario |
| 02 | análisis | `/cashier?section=analisis`; sub-pestañas `button:has-text('Cuadres y análisis'|'Rendimiento'|'Alertas'|'Auditoría')` | Cifras: «1 Sesiones activas · 1/3 Cajas abiertas · 0 Bloqueadas · 1 Cuadres pendientes · RD$3,050.00 Efectivo en cajas · 0 Alertas activas · 0 críticas · 0 advertencias». Período por defecto **«Este mes»** (01/09 → 23/09) (H-10); «Sesiones y flujo del 1 sept 2026 al 23 sept 2026»: 8 sesiones, 7/7 cerradas cuadradas, fondo total RD$40,000, flujo neto RD$920 |
| 02 | rendimiento | tabla # · CAJA · CAJERO · SESIONES · CUADRES · CONFIRMADOS · % DENTRO DE TOLERANCIA · DIF. PROMEDIO (ABSOLUTA) · ÚLTIMA ACTIVIDAD | «Caja Principal · yohanna.peralta · 4 · 4 · 4 · 100.0 % · RD$12.50»; «Caja Mostrador 2 · luis.batista · 4 · 4 · 3 · 100.0 % · RD$3.33» |
| 03 | alertas | tabla N° DE ALERTA · SEVERIDAD · TIPO · ALERTA · CAJA · ESTADO · FECHA | ALT-2026-00002 «Saldo bajo en caja … (RD$500.00) … (RD$1,000.00). Resolución: Resuelta automáticamente…» · Resuelta; ALT-2026-00001 «Caja bloqueada …» · Resuelta al desbloquear. **Ninguna activa**: la voz debe decir «resuelta» (confirma el aviso del plan) y «Reconocer/Resolver/Descartar» no se ven en filas resueltas |
| 03 | auditoría | tabla FECHA Y HORA · ACCIÓN · ENTIDAD · DESCRIPCIÓN · USUARIO · IP | 1.ª fila «Cambio de estado · Alerta de caja · Alerta de caja #85 — Estado: Activa → Resuelta · carmen.rosario · ::1»; filtros Acción / Tipo de entidad / Usuario / fechas. La IP «::1» sale en cámara |

Choca: en Historial y Auditoría la 3.ª fila de acciones queda bajo el FAB (y ≈ 607-630).

---

## Impresora de la estación (pedido del usuario)

**Permisos reales (BD `role_permissions`, 09-23):** `CASHIER_UPDATE` solo lo tiene **Admin (1)**;
Cajero (2) ✗, Supervisor de Caja (3) ✗ (tienen `CASH_DEVICE_SETTING`, que no abre este PATCH).
**UI:** el ⋮ `button[aria-label='Ajustes de este equipo']` ([1198,248]) aparece a CUALQUIERA con
sesión propia abierta en modo Flexible; ítem `.mat-mdc-menu-panel button:has-text('Configurar impresora')`
(o su `mat-icon` `print`, R21).

| Paso | Selector verificado | Observado |
|---|---|---|
| menú | `button[aria-label='Ajustes de este equipo']` → `.mat-mdc-menu-panel button:has(mat-icon:text-is('print'))` | Menú con un solo ítem «Configurar impresora» |
| diálogo | `app-printer-config-dialog` en `mat-dialog-container` [128,113,1024,495] | «Configurar impresora — Caja Principal · esta estación — La configuración se guarda en la caja y se aplica en el equipo vinculado a ella. Conecta la impresora a esta estación y usa Detectar, o digita los datos manualmente.»; casillas `mat-checkbox[formcontrolname='autoPrintReceipt']` «Imprimir recibo al facturar» (✓) y `…'autoOpenDrawer'` «Abrir gaveta al facturar» (✗); `button:has-text('Detectar')` (NO pulsar: abre el selector WebUSB nativo); `input[formcontrolname='printerVendorId']` / `…'printerProductId'` (placeholder «Ej: 0483» / «Ej: 070b»); `mat-select[formcontrolname='printerConnectionType']` = «USB Directo (WebUSB)». **En Chromium headless NO sale «Este navegador no soporta WebUSB»** (navigator.usb existe) |
| guardar (admin) | `mat-dialog-container button:has-text('Guardar')` | Diálogo se cierra, toast **«Impresora configurada exitosamente»** (PATCH aceptado; la fila de `cashiers` no se leyó antes de restaurar), `localStorage.HARDWARE_CONFIG_STG_KEY = {"cashierId":49,"printerVendorId":"0483","printerProductId":"070b","printerConnectionType":"USB","autoOpenDrawer":false,"autoPrintReceipt":true}`. Restaurado después (S0 → campos NULL; el contexto del navegador se descarta) |
| guardar (cajera) | ídem | **«Acceso Denegado — No tiene el permiso requerido para acceder a este recurso: "Editar Cajas". Solicite acceso a su administrador.»** + «No se pudo guardar la configuración de impresora» (H-01) |

**Propuesta para la serie:** mientras H-01 siga abierto, la impresora la graba **`admin.progreso`**
como **paso 04 del Video 2** («Impresora de esta estación», ≈ 45 s → el video queda ≈ 4:05),
partiendo del estado **S2i** (= S0 + sesión del admin abierta en Caja Principal; `node
seeds/cajas/restaurar.mjs S2i`): `navegar /cashier?section=caja` → ⋮ → «Configurar impresora» →
explicar casillas y «Detectar» (sin pulsarlo) → teclear 0483 / 070b → «Guardar» → toast. Encaja
con el tema del video (ajustes que se hacen una vez) y con el rol que realmente puede guardar.
Si se corrige H-01 (permitir a la cajera guardar la impresora de SU estación), el sitio natural
sería el Video 3 tras abrir la caja (cajera, S3). Restaurar después: `restaurar.mjs S2i` (vuelve
los campos de impresora de `cashiers`; el localStorage muere con el contexto de grabación).
