# seeds/cajas — datos, estados y exploración de la serie «Cajas»

Empresa demo **43 «Ferretería El Progreso»** (SRL, RNC 130555021, DOP). Todo lo de aquí toca SOLO
filas `company_id = 43`; la empresa 29 y el catálogo global de denominaciones no se tocan.
Correr desde `claude-tutorial/seeds/cajas` (Node ≥ 18, sin dependencias) o con ruta.

| Archivo | Qué hace |
|---|---|
| `_lib.mjs` | `api(usuario, método, ruta, cuerpo)` con login `auth/dev/login` (clave `Demo2026!`), `sql()` con `sql_log_bin=0`, constantes (empresa 43, cuentas 116/167, Efectivo=1) |
| `sembrar-s0.mjs` | Siembra S0 UNA vez sobre la empresa recién creada (política, 3 cajas, 6 turnos de D-3…D-1 con cuadres confirmados por carmen, bloqueo de Santiago, turno abierto de luis). Se niega si ya hay sesiones (`--forzar`) |
| `_estado.mjs` | Lista MEDIDA de tablas que escribe el flujo (ver abajo) y su modo de restauración |
| `fijar.mjs <S#>` | Vuelca con mysqldump las filas `company_id=43` de esas tablas a `estados/<S#>.sql` (+ `.json` con conteos y hora). Espera a que la auditoría asíncrona del API se quede quieta |
| `restaurar.mjs <S#>` | Devuelve la empresa 43 al canon: borra filas nuevas, UPDATE de las cambiadas, re-INSERT de las borradas; `sys_sequences` por UPDATE (trigger anti-DELETE); desplaza en el tiempo las sesiones ABIERTAS para que «Abierta hace 2 h» no envejezca (`--sin-desplazar` lo evita). Verifica conteos al terminar. **≈ 0,6 s** |
| `preparar.mjs S1|S2i` | Arma por API S1 (S0 + umbrales 1,000/60,000) o S2i (S0 + sesión del admin en Caja Principal, para la impresora) |
| `explorar.py [v1…v7 impresora verificar todo]` + `escenarios_cajas.py` | Exploración del DOM vivo (Playwright headless 1280×720, dsf 1.5, login real). Salida en `guiones/exploracion-cajas/`. Cerrojo `seeds/_puertas/NAVEGADOR.lock` («EXPLORANDO datos-cajas»). Al final restaura S0 (`--sin-restaurar` lo evita). v3…v6 FIJAN S3…S6 con el resultado real de la UI |

## Estados fijados (`estados/`)

| Estado | Contenido | Cómo se obtuvo |
|---|---|---|
| S0 | 3 cajas (Principal cerrada, Mostrador 2 abierta por luis.batista con 6,050, Santiago bloqueada), 6 turnos previos cuadrados, política 5,000/50/3/720/5,000/10,000 | `sembrar-s0.mjs` |
| S1 | S0 + umbrales de alerta 1,000 / 60,000 | `preparar.mjs S1` |
| S2i | S0 + sesión del admin en Caja Principal (paso de impresora) | `preparar.mjs S2i` |
| S3 | S1 + sesión de yohanna en Principal (fondo 5,000), entrada 2,000 (MOV-00009), salida 6,500 con ITBIS 991.53 **por aprobar** (MOV-00010) | `explorar.py v3` (UI real) |
| S4 | S3 + MOV-00010 aprobado por carmen + TRF-2026-00001 3,000 Mostrador 2 → Principal recibida (esperado Principal 3,500; alerta de saldo bajo creada y resuelta) | `explorar.py v4` |
| S5 | S4 + conteo de cierre de yohanna REC-2026-00007 (3,480, −20 «Faltan 20 pesos en monedas») pendiente; sesión cerrada | `explorar.py v5` |
| S6 | S5 + REC-00007 aprobado por carmen (con asiento del faltante) + arqueo sorpresa REC-00008 sobre la sesión de luis (3,050, pendiente) + Santiago desbloqueada | `explorar.py v6` |

Uso entre tomas: `node seeds/cajas/restaurar.mjs S3` (el estado de PARTIDA del video, ver
`guiones/_DATOS-CAJAS.md`). Probado: S0→S0, S0→S1→S1→S0→S0, S3/S4/S5/S6 tras modificar por UI.

## Tablas (medidas con auto_increment/update_time de las 622 tablas antes/después)

`cashiers` (incluye bloqueo, isOpen y los campos de **impresora**) · `cashier_sessions` ·
`cash_movements` · `cash_transfers` · `cashier_reconciliations` · `cashier_reconciliation_details`
· `cash_counts` · `cash_count_details` · `cashier_alerts` · `cashier_config` · `cash_denominations`
(solo las de la empresa) · `cashier_device_requests` · `journal_entries` · `journal_entry_details`
· `general_ledger` · `auto_posting_logs` · `accounting_periods` · `account_period_balances` ·
`user_company_preferences` (a dónde aterriza cada usuario) · `company_configs` (solo UPDATE) ·
`sys_sequences` (MOV/REC/TRF/ALT/ASI: solo UPDATE) · `audit_logs` (filas de la empresa; tabla
particionada → las tablas temporales se crean con `CREATE … SELECT … LIMIT 0`).
No se restauran (no afectan a la UI de Cajas): `auth_session`, `users.login_date`,
`company_user_activity_daily`, `companies.last_access_at`.

## Trampas medidas

- La auditoría del API se escribe DESPUÉS de responder: `fijar` espera conteos quietos y
  `restaurar` espera a que `MAX(id)` de audit_logs deje de crecer.
- `sys_sequences` tiene `tg_protect_sys_sequences` (DELETE prohibido): una secuencia nacida después
  del canon (p. ej. TRF) queda con `current_value = initial_value` → TRF-2026-00001 otra vez.
- Zona horaria: el API lee los `timestamp` como instantes de la sesión MySQL (UTC-5) y los entrega
  en RD (UTC-4): un literal escrito con `NOW()` de MySQL se ve bien; las horas retrocedidas a mano
  (p. ej. 08:05) se ven +1 h en la UI (09:05).
- Cada login revoca la sesión previa del MISMO usuario: no usar `_lib.api()` con el usuario que está
  grabando. `preparar.mjs S1/S2i` usa `admin.progreso`.
