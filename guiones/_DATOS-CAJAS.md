# Datos de Cajas — empresa demo 43 (VIGENTE) y plan original sobre la empresa 29 (OBSOLETO)

## 0. VIGENTE (carril DATOS+EXPLORACIÓN, 2026-09-23) — la serie se graba en la EMPRESA 43

La empresa 29 **ya no se usa ni se toca** (sus cajas QA-*, sesiones 43/77, cuadres y usuarios qa.*
quedan como estaban; verificado: sin escrituras nuevas). Todo lo de §1–§5 más abajo es el plan
viejo y queda solo como referencia histórica.

### 0.1 Empresa
| Dato | Valor |
|---|---|
| id | **43** |
| Razón social / comercial | «Ferretería El Progreso SRL» / «Ferretería El Progreso» |
| RNC | **130555021** (rango demo `1305550…`) |
| Dirección / teléfono | Av. Duarte 214, Ensanche La Fe, Santo Domingo · 809-555-0142 |
| Alta | `POST /api/auth/dev/register` (flujo real + verificación automática; `setup_status=COMPLETED`, plantilla de catálogo 1) |
| Plan | 2 «Emprendedor» (TRIAL; incluye el módulo `POS` que gatea «Cajas»). El `selectedPlanId:15` se ignoró |
| Moneda | DOP |
| Modo de estaciones | `company_configs.cashier_station_mode = OFF` (Flexible) |
| Bancos | ninguno → contrapartida siempre «Cuenta contable» |
| Cuentas de contrapartida (catálogo global) | id 116 **4.02.01.02 «Otros ingresos diversos»** · id 167 **6.03.21 «Otros gastos generales»** (en el autocompletar: «4.02.01.02 - Otros ingresos diversos», «6.03.21 - Otros gastos generales») |
| Denominaciones | las 10 globales (no se editan); la del video 2 nace con `company_id=43` |

### 0.2 Usuarios (clave de todos: `Demo2026!`, correos `@germiva.demo`, `current_company_id=43`)
| id | username (login) | Nombre en pantalla | Rol en la 43 | Graba |
|---|---|---|---|---|
| 7645 | `admin.progreso` | Ramón Almonte | Admin (1) — dueño de la empresa | videos 1, 2 (+ impresora) |
| 7646 | `yohanna.peralta` | Yohanna Peralta | Cajero (2) | videos 3, 5 |
| 7647 | `luis.batista` | Luis Batista | Cajero (2) | fondo: opera Caja Mostrador 2 |
| 7648 | `carmen.rosario` | Carmen Rosario | Supervisor de Caja (3) | videos 4, 6, 7 |
`user_company_preferences.incomplete_config_notice_seen_at` marcado para los 4; ningún modal al
entrar (verificado por la UI). Cuatro ojos: además de carmen, admin.progreso también puede aprobar,
así que carmen nunca aprueba lo suyo (su arqueo sorpresa lo confirmaría el admin).
OJO: el panel «Abrir mi caja» muestra el CORREO como cajero («yohanna.peralta@germiva.demo»); el
tablero y las listas muestran el username.

### 0.3 Cajas (ids 49/50/51)
| id | Código | Nombre | Ubicación | S0 |
|---|---|---|---|---|
| 49 | CAJA-01 | Caja Principal | Mostrador de entrada — frente a la puerta | Cerrada (acepta efectivo, tarjeta y transferencia) |
| 50 | CAJA-02 | Caja Mostrador 2 | Área de pinturas y herramientas | **Abierta** por luis.batista hace 2 h: fondo 5,000 + entrada 1,500 («Cambio para la gaveta») − salida 450 con ITBIS 68.64 («Compra de agua y café para clientes») = **6,050** |
| 51 | CAJA-SAN | Caja Sucursal Santiago | Sucursal Santiago — Av. Estrella Sadhalá | **Bloqueada** por carmen.rosario: «[Auditoría pendiente] Faltante de efectivo en el último arqueo; pendiente de revisión con la gerencia» (alerta ALT-2026-00001 activa) |

Historia (fechas retrocedidas por SQL solo en filas de la 43; la UI las muestra +1 h):
D-3 yohanna/Principal +1,500 → cuadre exacto 6,500 · luis/Mostrador 2 −800 → exacto 4,200 ·
D-2 yohanna −1,180 (ITBIS 180) → 3,790 (−30 «Faltan 30 pesos: vuelto mal entregado a un cliente») ·
luis +2,500 → exacto 7,500 · D-1 yohanna +3,000 −650 → exacto 7,350 · luis sin movimientos → 5,010
(+10 «Sobran 10 pesos en monedas»). Todos confirmados por carmen (REC-2026-00001…00006, con sus
asientos; los de diferencia generan «Faltante/Sobrante de caja en cuadre»).
Numeración de la 43 en S0: MOV hasta 00008, REC hasta 00006, ALT 00001, ASI hasta 000010.

### 0.4 Estados y restauración (R7)
`node seeds/cajas/restaurar.mjs <S#>` (≈ 0,6 s, verifica conteos) · `fijar.mjs <S#>` ·
detalle en `seeds/cajas/README.md`.
| Estado | Parte de | Qué contiene (medido en BD) |
|---|---|---|
| S0 | Videos 1 y 2 | §0.3 |
| S1 | Video 3 | S0 + umbrales de alerta 1,000 / 60,000 |
| S2i | Paso «Impresora» (propuesto en Video 2, admin) | S0 + sesión de admin.progreso en Caja Principal |
| S3 | Video 4 | S1 + yohanna abrió Principal (5,000, «Turno de la mañana»), MOV-2026-00009 entrada 2,000 (116), MOV-2026-00010 salida 6,500 / ITBIS 991.53 (167) **PENDING_APPROVAL**; saldo 7,000 |
| S4 | Video 5 | S3 + MOV-00010 APPROVED por carmen (asiento) + TRF-2026-00001 3,000 Mostrador 2 → Principal RECEIVED (MOV-00011/00012). Esperado Principal **3,500**, Mostrador 2 **3,050**. ALT-2026-00002 saldo bajo (500 < 1,000) creada al aprobar y **Resuelta** al recibir |
| S5 | Video 6 | S4 + REC-2026-00007 CLOSING 3,480 (−20, dentro de ±50, «Faltan 20 pesos en monedas») PENDING_CONFIRMATION; sesión de yohanna cerrada |
| S6 | Video 7 | S5 + REC-00007 CONFIRMED por carmen (asiento del faltante) + REC-2026-00008 SURPRISE_AUDIT 3,050 exacto sobre la sesión de luis (Pendiente) + Santiago desbloqueada (ALT-00001 Resuelta) |
| S8 | Video 8 (cobro de factura, pago combinado) | S1 + **plan 15** en la suscripción de la 43 + factura 1000000001 de CONTADO en BORRADOR (B01, «Constructora Los Pinos», 7,500 + ITBIS 1,350 = 8,850) + sesión de **admin.progreso** en Caja Principal (fondo 5,000). Maestros persistentes (no se restauran): cliente «Constructora Los Pinos» (RNC ficticio 130555079). Preparar: `seeds/cajas/preparar-s8.mjs`; después de ensayar/grabar el video 8: `seeds/cajas/plan-s8.mjs off` (S0…S6 no guardan el plan). Detalle: `_INVENTARIO-COBRO-FACTURA.md` |

Diferencias con el plan original: la historia usa Principal y Mostrador 2 (no hay «Caja Eventos»);
la alerta de saldo bajo del video 7 aparece **Resuelta** (no activa); el arqueo del video 6 es por
**3,050** (no 6,050: la transferencia salió de Mostrador 2).

---

# HISTÓRICO — plan original sobre la empresa 29 (NO EJECUTADO, NO USAR)

Autor: AUTOR-INVENTARIO · 2026-09-23. Consultas **solo SELECT** a la BD local `germiva`
(MySQL 9.7, 127.0.0.1:3306). **Nada de este archivo se ha ejecutado**: el plan (§3–§5) es una
propuesta para la sesión que prepare los datos.

---

## 1. Estado ACTUAL (09-23, BD local)

### 1.1 Cajas de la empresa 29 (`cashiers`)
44 filas; 42 operativas + 2 archivadas (8 `QA-A2-03`, 13 `QA-R2-02`). **Solo 2 tienen nombre
presentable**; el resto son de QA y saldrían en cámara:

| id | code | name | ubicación | estado | sesión abierta |
|---|---|---|---|---|---|
| 4 | CAJA-01 | **Caja Principal** | Recepción — oficina Sofosy | isOpen=1 | **sesión 43 de `john.delibua@sofosy.demo` abierta desde el 09-09** (nunca cerrada) |
| 5 | CAJA-02 | **Caja Secundaria** | Área de ventas — piso 1 | cerrada, `consecutive_differences=1` | — (7 sesiones de admin/qa.a2.*) |
| 6 | QA-A2-01 | QA-A2 Caja 1 | NULL | abierta | sesión 77 `qa.a2.cajero1` (evidencia CONC-01) |
| 7, 10–12, 14–17 | QA-A2-02, QA-A1-01/02, QA-R2-01/03/04/05/06 | «QA-A1 Caja 1», «QA R2 Caja 3 (conc)»… | NULL | cerradas | — |
| 19 | QA-R3-01 | QA-R3 Caja 1 | Estación R3-1 | abierta | sesión 112 `qa.r3.cajero` |
| 20 | QA-R3-02 | QA-R3 Caja 2 | Estación R3-2 | cerrada, **modo estricto**, fondo fijo 5,000 | — |
| 21–30 | QA-VF-01…06, QA-VFN1-05…08 | «QA-Final Caja n», «QA-FinalL1 Caja n» | NULL | 25 abierta | sesión 504 `qa.a2.cajero2` en 25 |
| 31–48 | QA-CALC-01…20 | «QA-CALC Caja n» / «QA-CALC-nn» | «QA» | cerradas (42 y 48 con dispositivo vinculado) | — |

Todas `PHYSICAL`, `ACTIVE`, ninguna bloqueada. **5 sesiones abiertas** (43, 77, 112, 504 y la 382
ya soft-deleted en la caja 33).

### 1.2 Volumen operativo de la empresa 29
| Tabla | Estado |
|---|---|
| `cashier_sessions` | 459 (454 cerradas) |
| `cash_movements` | COMPLETED 320 · APPROVED 26 · REJECTED 49 · VOIDED 17 · **0 por aprobar** |
| `cash_transfers` | CANCELLED 52 · RECEIVED 41 · REJECTED 4 · **PENDING 1** (TRF-2026-00004, 150, QA-A2 1→2) · **APPROVED 1** (TRF-2026-00026, 11,000, QA-R3 1→2, sin recibir) |
| `cashier_reconciliations` | CONFIRMED 390 · **PENDING_CONFIRMATION 73** · REJECTED 15 · VOIDED 8. Los 73 pendientes: QA R2 Caja 4 (17), QA R2 Caja 3 (13), QA-A1 Caja 1 (13), QA R2 Caja 6 (10), QA R2 Caja 5 (5), **Caja Secundaria (3)**, y 1–3 en otras QA |
| `cashier_alerts` | **ACTIVE 9** (5 WARNING, 4 CRITICAL: Caja Principal 1, QA-A1 Caja 1 3, QA-CALC Caja 3 2, QA-Final Caja 1, QA-A2 Caja 1, QA-R3 Caja 1) · RESOLVED 20 |
| `cashier_device_requests` | 0 |

⇒ Hoy «Por aprobar» mostraría **73 cuadres** con nombres QA, el tablero 44 tarjetas «QA-*», y
Análisis/Historial filas de `qa.*@sofosy.demo` (correos sin la marca «germiva»: el auditor de
privacidad de `claude-tutorial` los trataría como fuga).

### 1.3 `cashier_config` (id=1, company 29)
`default_initial_cash` 5,000 · `min/max_initial_cash` NULL · `tolerance_mode` AMOUNT ·
`tolerance_amount` 50 · `tolerance_percentage` 1 · `max_consecutive_differences` 3 ·
`max_session_duration_minutes` 720 · `max_withdrawal_without_approval` **5,000** ·
`max_deposit_without_approval` **10,000** · `require_notes_for_withdrawal` 1 ·
`require_reconciliation_for_close` **1** · `require_justification_for_difference` 1 ·
`reconciliation_confirmation_hours` 24 · `allow_operation_on_holidays` 0 · `blind_count` **0** ·
`alert_threshold_low/high` NULL.
`company_configs.cashier_station_mode` (29) = **OFF** (modo Flexible: se abre cualquier caja).

### 1.4 Denominaciones (`cash_denominations`)
La empresa 29 **no tiene propias**. Se ven las 10 del **catálogo global** (`company_id IS NULL`,
`@SharedCatalog`), todas DOP, `sort` NULL: billetes 2000 «Dos Mil», 1000 «Mil», 500 «Quinientos»,
200 «Doscientos», 100 «Cien», 50 «Cincuenta»; monedas 25 «Veinticinco», 10 «Diez», 5 «Cinco»,
1 «Uno». **Falta el billete de RD$20.** La empresa 29 NO es principal (`isCompanyMain=0`).

### 1.5 Usuarios con roles de caja en la empresa 29 (`user_company_roles`)
Todos son de QA (correo `@sofosy.demo`, perfil «QA-…»). Ninguno sirve para cámara.
- **Cajero (2):** 7620 qa.a2.cajero1 · 7621 qa.a2.cajero2 · 7626 qa.a1.cajero · 7629 qa.r3.cajero ·
  7631 qa.vfin.cajero1 · 7632 qa.vfin.cajero2 · 7634 qa.vfin2.cajero · 7636 qa.vfin4.cajero ·
  7638 qa.vfin3.cajero1 (clave `QaCajas2026!`, `QA_CREDENTIALS.md`).
- **Supervisor de Caja (3):** 7622 qa.a2.supervisor · 7627 qa.a1.supervisor · 7630 qa.r3.supervisor ·
  7633 qa.vfin.supervisor · 7635 qa.vfin2.supervisor · 7637 qa.vfin4.supervisor · 7640 qa.vfin3.supervisor.
- **Admin (1):** 1 `admin` (perfil «Sistema Administrador») · 261 john.delibua · 265 franklin.cuevas ·
  7611, 7628, 7639, 7641 (QA).
Como hay 7 supervisores activos, la regla de cuatro ojos SIEMPRE aplica (nadie aprueba lo suyo).

### 1.6 Otros datos que condicionan el guion
- **0 cuentas bancarias** en la empresa 29 → la contrapartida de Entrada/Salida es siempre «Cuenta
  contable». El plan de cuentas es global (`accounting_chart.company_id` NULL). Las que ya usó la BD:
  id 167 **6.03.21 «Otros gastos generales»** (86 usos) e id 116 **4.02.01.02 «Otros ingresos
  diversos»** (63).
- Métodos de pago (`payment_methods`): 1 Efectivo (CASH), 2 Transferencia, 3 Cheque, 4 Depósito,
  5 Tarjeta, 6 Venta a crédito…
- MySQL local va en UTC-5 y el API en RD (memoria `reference_mysql_local_utc5_vs_app_rd`): las horas
  leídas por SQL salen 1 h corridas; «Abierta hace…» lo calcula el front.

---

## 2. Principio del plan
1. **No borrar historia**: todo lo de QA se oculta con **soft delete** (`deleted_at`) usando un
   **sello de tiempo marcador** único, `2026-09-23 00:00:07`, para poder revertir con un solo
   `UPDATE … SET deleted_at = NULL WHERE deleted_at = '2026-09-23 00:00:07'`. Antes, respaldo
   completo de las tablas tocadas.
2. Los datos demo se crean **por el API** (misma lógica, numeración, asientos y alertas que en
   producción) con usuarios demo; SQL solo para lo que el API no ofrece (usuarios, retro-fechar,
   contador de diferencias).
3. Nombres dominicanos ficticios; **usernames SIN «@»** (el visor pinta `user.username`: «La opera
   yohanna.peralta») y correos con la marca `germiva` (permitida por el auditor de privacidad,
   `claude-tutorial/config.json › privacidad.permitidos`).
4. Tras montar S0 se fija el canon (`recanon.mjs`); cada estado S1…S6 se reconstruye con un script
   de API desde S0 (determinista) o se vuelca como canon propio.

---

## 3. Paso A — Respaldo y ocultar lo de QA (SQL, NO ejecutado)

```bash
# A.0 respaldo (Git Bash; MYSQL_PWD desde Germiva-api/.env)
"/c/Program Files/MySQL/MySQL Server 9.7/bin/mysqldump.exe" -h 127.0.0.1 -u root germiva \
  cashiers cashier_sessions cash_movements cash_transfers cashier_reconciliations \
  cashier_reconciliation_details cash_counts cash_count_details cashier_alerts cashier_config \
  cash_denominations users profiles user_companies user_company_roles \
  > "<scratchpad>/respaldo-cajas-2026-09-23.sql"
```

```sql
-- A.1 marcador
SET @t := '2026-09-23 00:00:07.000000';

-- A.2 operación de la empresa 29: se oculta TODA (QA + la sesión 43 de john.delibua + los 3 cuadres
--     pendientes de Caja Secundaria). Las cajas 4 y 5 quedan limpias para la demo.
UPDATE cash_movements          SET deleted_at=@t WHERE company_id=29 AND deleted_at IS NULL;
UPDATE cash_transfers          SET deleted_at=@t WHERE company_id=29 AND deleted_at IS NULL;
UPDATE cashier_reconciliations SET deleted_at=@t WHERE company_id=29 AND deleted_at IS NULL;
UPDATE cash_counts             SET deleted_at=@t WHERE company_id=29 AND deleted_at IS NULL;
UPDATE cashier_alerts          SET deleted_at=@t WHERE company_id=29 AND deleted_at IS NULL;
UPDATE cashier_sessions        SET deleted_at=@t WHERE company_id=29 AND deleted_at IS NULL;

-- A.3 cajas QA fuera (equivale a «Archivar»; el API lo impediría por las sesiones abiertas 77/112/504)
UPDATE cashiers SET deleted_at=@t
 WHERE company_id=29 AND deleted_at IS NULL AND id NOT IN (4,5);

-- A.4 las dos cajas que se conservan, sin sesión viva ni contador heredado
--     (valores previos para revertir: 4 → isOpen=1; 5 → consecutive_differences=1)
UPDATE cashiers SET isOpen=0, consecutive_differences=0, is_blocked=0, block_reason=NULL
 WHERE id IN (4,5);
```

Revertir (tras la serie):
```sql
SET @t := '2026-09-23 00:00:07.000000';
UPDATE cash_movements SET deleted_at=NULL WHERE deleted_at=@t;   -- y las otras 6 tablas igual
UPDATE cashiers SET deleted_at=NULL WHERE deleted_at=@t;
UPDATE cashiers SET isOpen=1 WHERE id=4;  UPDATE cashiers SET consecutive_differences=1 WHERE id=5;
-- y soft-delete de lo demo (usuarios demo, cajas CAJA-SAN/CAJA-EVT/CAJA-03, sus sesiones…)
```
Notas:
- Lo que NO se oculta: `audit_logs` (Análisis › Auditoría mostrará entradas viejas de `qa.*`; en el
  video 7 filtrar por fecha de hoy o por usuario demo). Los asientos contables de los movimientos QA
  quedan intactos (no se ven en Cajas).
- **Decisión para el usuario** (QA_CREDENTIALS dice «no tocar» la sesión 43 y la 77): ocultarlas
  es reversible y solo en la BD local (memoria `feedback_local_db_libre…`). Si no se aprueba, la
  alternativa es crear cajas demo NUEVAS y dejar las QA… pero el tablero mostraría igual 44 tarjetas
  QA: no hay forma limpia sin ocultarlas.
- Verificar tras A: `GET /api/v1/cashiers/summary` → total 2, abiertas 0; «Por aprobar» en 0.

---

## 4. Paso B — Usuarios demo (SQL, mismo patrón que `QA_CREDENTIALS.md`: `profiles` + `users` +
`user_companies` + `user_company_roles`; NO ejecutado)

| Usuario (login) | Correo | Perfil (nombre / apellido) | Rol | Uso |
|---|---|---|---|---|
| `yohanna.peralta` | yohanna.peralta@germiva.demo | Yohanna / Peralta | Cajero (2) | cajera de los videos 3 y 5 |
| `luis.batista` | luis.batista@germiva.demo | Luis / Batista | Cajero (2) | opera «Caja Mostrador 2» de fondo (tarjeta «La opera», origen de la transferencia, arqueo sorpresa) |
| `carmen.rosario` | carmen.rosario@germiva.demo | Carmen / Rosario | Supervisor de Caja (3) | videos 4, 6, 7 |
| `admin` (existe, id 1) | — | Sistema Administrador | Admin | videos 1 y 2 (clave `admin`, como el guion de RR.HH.) |

```sql
-- hash bcrypt reutilizado de QA = 'QaCajas2026!'
SET @h := '$2b$10$/Y8XXCnxzZE3CDq05OJD1Ofj8FlU/z35pnV1aWiVPX2dRr93iArT.';
INSERT INTO profiles (created_at, updated_at, is_internal, name, first_name, active)
VALUES (NOW(), NOW(), 0, 'Peralta', 'Yohanna', 1);  SET @p1 := LAST_INSERT_ID();
INSERT INTO users (created_at, updated_at, is_internal, username, email, password, active,
                   emailVerified, current_company_id, profile_id, userType, is_default_password,
                   termsAccepted)
VALUES (NOW(), NOW(), 0, 'yohanna.peralta', 'yohanna.peralta@germiva.demo', @h, 1, 1, 29, @p1,
        'NORMAL', 0, 1);  SET @u1 := LAST_INSERT_ID();
INSERT INTO user_companies (user_id, company_id, is_internal) VALUES (@u1, 29, 0);
INSERT INTO user_company_roles (user_id, company_id, role_id, created_at, is_internal, active)
VALUES (@u1, 29, 2, NOW(), 0, 1);
-- ídem luis.batista (rol 2) y carmen.rosario (rol 3)
-- R18: marcar el aviso «Configuración incompleta» como visto para los 3
INSERT INTO user_company_preferences (user_id, company_id, incomplete_config_notice_seen_at,
                                      created_at, updated_at, is_internal, active)
VALUES (@u1, 29, NOW(), NOW(), NOW(), 0, 1);  -- ídem @u2, @u3
```
Comprobar con la columna `name`/`first_name` de `profiles` cuál es nombre y cuál apellido en la UI
(en QA: `name='QA-R3'`, `first_name='Cajero'`). Login de prueba:
`POST http://localhost:3001/api/auth/dev/login {"username":"yohanna.peralta","password":"QaCajas2026!","recaptchaToken":"dev-bypass"}`.
Cada login revoca la sesión anterior del mismo usuario (R26): **no** hacer login por API con el
usuario que está grabando.

---

## 5. Paso C — Cajas y operación demo por API (estado S0; NO ejecutado)

Base `http://localhost:3001/api`, token de `auth/dev/login` de cada actor.

| # | Actor | Llamada | Resultado |
|---|---|---|---|
| C1 | admin | `PATCH v1/cashiers/5` `{"name":"Caja Mostrador 2","location":"Área de ventas — piso 1"}` | renombra «Caja Secundaria» |
| C2 | admin | `PATCH v1/cashiers/4` `{"location":"Recepción — oficina principal"}` | «Oficina Sofosy» fuera de cámara (opcional) |
| C3 | admin | `POST v1/cashiers` `{"code":"CAJA-SAN","name":"Caja Sucursal Santiago","location":"Sucursal Santiago — Av. 27 de Febrero","acceptCash":true,"acceptCard":true,"acceptTransfer":false}` | para el desbloqueo (video 6) |
| C4 | admin | `POST v1/cashiers` `{"code":"CAJA-EVT","name":"Caja Eventos","location":"Salón de capacitación","acceptCash":true,"acceptCard":false,"acceptTransfer":false}` | cerrada, con historial |
| C5 | luis.batista | `POST v1/cashiers/sessions/open` `{"cashier":<id CAJA-EVT>,"initialCash":5000,"notes":"Turno de ayer"}` → `POST v1/cashiers/movements` IN 1,200 (`counterpartAccount`:116) → `POST v1/cashier-reconciliation` `{"cashierSession":…,"reconciliationType":"CLOSING","details":[{"paymentMethod":1,"actualAmount":"6200"}]}` | historial de días previos (cuadre exacto) |
| C6 | carmen.rosario | `PATCH v1/cashier-reconciliation/<id>/confirm` `{"accepted":true}` | REC confirmado |
| C7 | (repetir C5–C6 dos veces con yohanna en «Caja Mostrador 2»: uno exacto y uno con −30 justificado) | | Análisis «Últimos 7 días» con datos |
| C8 | SQL | retro-fechar esas sesiones/movimientos/cuadres a D-1, D-2, D-3 (`openedAt`, `closedAt`, `created_at`) | curvas del Reporte diario/Rendimiento |
| C9 | carmen.rosario | `POST v1/cashiers/<id CAJA-SAN>/block` `{"reason":"Diferencias consecutivas: tres cuadres seguidos con faltantes en efectivo, pendiente de auditoría"}` + SQL `UPDATE cashiers SET consecutive_differences=3 WHERE code='CAJA-SAN' AND company_id=29` | tarjeta «Bloqueada: …» |
| C10 | luis.batista | `POST v1/cashiers/sessions/open` `{"cashier":5,"initialCash":5000,"notes":"Turno de la mañana"}` → IN 1,500 (116, «Cambio para la gaveta») → OUT 450 (167, «Compra de agua y café para clientes», `taxAmount` 68.64) + SQL `openedAt = NOW() - INTERVAL 2 HOUR` | «Caja Mostrador 2» abierta: saldo 6,050, «Abierta hace 2 h» |

**S0** = A + B + C1…C10 (cajas: Caja Principal cerrada y libre · Caja Mostrador 2 abierta por
luis.batista · Caja Eventos cerrada · Caja Sucursal Santiago bloqueada; `cashier_config` = §1.3;
«Por aprobar» en 0; sin alertas activas).

Estados encadenados (cada uno = S0 + las acciones de los videos previos, reproducibles por API):
| Estado | Punto de partida de | Se obtiene con |
|---|---|---|
| S0 | Videos 1 y 2 | §3–§5 |
| S1 | Video 3 | S0 + `PATCH v1/cashier-config` umbrales `alertThresholdLow` 1000 / `alertThresholdHigh` 60000 (lo que guarda el video 2; la denominación y CAJA-03 NO se arrastran) |
| S3 | Video 4 | S1 + yohanna: `sessions/open` caja 4 fondo 5000 → IN 2000 (116) → OUT 6500 (167, taxAmount 991.53) ⇒ OUT queda `PENDING_APPROVAL` |
| S4 | Video 5 | S3 + carmen: `movements/<id>/approve` → `POST v1/cash-transfers` `{"sourceCashier":5,"targetCashier":4,"amount":3000,"reason":"Reposición de cambio para la caja principal"}` → `cash-transfers/<id>/receive` ⇒ esperado caja 4 = 3,500; la alerta de saldo bajo nace al aprobar (500 < 1,000) y puede resolverse sola al recibir (`refreshBalanceAlerts`) |
| S5 | Video 6 | S4 + yohanna: `cashier-reconciliation` CLOSING `details:[{paymentMethod:1, actualAmount:"3480", justification:"Faltan 20 pesos en monedas"}]` ⇒ REC PENDIENTE, sesión cerrada |
| S6 | Video 7 | S5 + carmen: confirmar REC · arqueo sorpresa sobre la sesión de luis (`reconciliationType":"SURPRISE_AUDIT"`, efectivo = esperado) · `POST v1/cashiers/<CAJA-SAN>/unblock` `{"reason":"Auditoría completada","notes":"…"}` |

Lo que escribe cada video (para restaurar entre tomas) está en `_SERIE-CAJAS.md`. Sugerencia: un
`seeds/cajas/preparar.mjs --estado=S3` que haga §5 + las llamadas de la tabla, y `recanon` por
estado; así una toma fallida se repite desde su estado exacto.

**Opcional (recomendado): un cobro de factura en efectivo** en la sesión de yohanna (S3), hecho desde
Ventas con su usuario (el cobro toma la sesión abierta, `portfolio-payment-dialog.component.ts:324-330`),
para que «Cobros del turno» del video 5 no sea 0. Si se agrega, recalcular: esperado = 3,500 + cobro.

---

## 6. Riesgos de datos detectados
1. **Denominaciones globales editables por cualquier empresa** (`API/cashiers/cashiers.service.ts:1487-1523`
   sin `assertSharedCatalogEditable`): en el video 2 solo crear, nunca editar/eliminar. Además
   `createDenomination` busca duplicados por `nameCount` sin filtrar por empresa (:1454-1461):
   «Veinte» no existe hoy, pero verificar en el ensayo que la nueva quede con `company_id=29`.
2. Ocultar por soft delete deja filas con relaciones a cajas/sesiones borradas; si alguna vista
   (Análisis › Auditoría, exportaciones) lista algo con «—», revisar en el ensayo.
3. Los 7 supervisores QA siguen activos: la regla de cuatro ojos funciona igual (conviene que sigan
   para que el «aprobador único» no se active).
4. La sesión 504 (`qa.a2.cajero2`, 09-22) y la 77 son evidencia de QA: quedan ocultas, no cerradas;
   revertir con el marcador.
