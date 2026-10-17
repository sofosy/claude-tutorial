# Serie «Cajas» — propuesta (vista única, master 09-23)

Autor: AUTOR-INVENTARIO · 2026-09-23. Selectores y textos: `_INVENTARIO-CAJAS.md` (§ entre
corchetes). Datos: `_DATOS-CAJAS.md` (estados S0…S6).

## Criterio
- Cubre el módulo COMPLETO sin repetir: cada pantalla y diálogo aparece en UN video como tarea
  principal; en los demás solo se nombra.
- **Rol según permiso real** (BD, 09-23): la configuración la graba el **Admin**; la operación, una
  **Cajera** (rol 2, que solo ve «Cajas» y «Mi caja»); aprobaciones, cuadre oficial, desbloqueo,
  historial y análisis, una **Supervisora de Caja** (rol 3). Por la regla de **cuatro ojos** la
  supervisora nunca aprueba lo que ella misma hizo.
- Los videos encadenan una historia de un día: la cajera abre, opera, pide aprobación; la
  supervisora aprueba y mueve efectivo; la cajera cierra; la supervisora cuadra. El estado final de un
  video es el inicial del siguiente (S0…S6 en `_DATOS-CAJAS.md`); entre tomas se restaura el estado
  de partida del video.
- Pasos de 40–80 s = UNA tarea. 7 videos, 3–4 pasos, 3:00–4:00 cada uno. Total ≈ 23 min.
- Siempre `navegar` con `?section=` (el aterrizaje sin él depende de si hay sesión abierta,
  [0.1]). Contraer el panel del menú al presentar la pantalla (R5, `click_opcional:
  button.panel-collapse`).
- Todos los éxitos del módulo son **toast** de 3,5 s (`.mat-mdc-snack-bar-container`), no diálogo:
  marcar al instante, nada que pulsar [0.4]. Las confirmaciones sí son diálogo
  (`.custom-alert-dialog-style button.confirm-button`).

Usuarios demo (a crear, ver `_DATOS-CAJAS.md` §3): `admin`/`admin` (existe) · **yohanna.peralta**
(Cajera) · **luis.batista** (Cajero, opera la Caja Mostrador 2 de fondo) · **carmen.rosario**
(Supervisora de Caja).

---

## Video 1 — «Cajas: el tablero y tus cajas» (≈3:10) · graba `admin`
Estado de partida: **S0**. Qué escribe: 1 caja nueva (`CAJA-03 «Caja Mostrador 3»`).
Restaurar: borrar/archivar CAJA-03 (o volver a S0).

| id | Tarea | Parte de → llega a | Duración |
|---|---|---|---|
| 01-tablero | Qué es una caja y qué es una sesión; recorrer el tablero: tarjeta de «Caja Mostrador 2» (Abierta, «La opera luis.batista», «Efectivo en caja»), «Caja Sucursal Santiago» (Bloqueada, motivo), «Caja Principal» (Cerrada, «Abrir sesión»); filtro «Abiertas N» y vuelta a «Todas»; el ⋮ de la tarjeta (Movimientos · Sesiones · Cuadres · Configurar caja) solo señalado; pestañas de sección señaladas una vez. | `/cashier?section=cajas` → mismo | 60 s |
| 02-nueva-caja | «Nueva caja» → Nombre «Caja Mostrador 3», Código «CAJA-03», Ubicación «Área de ventas — piso 2»; métodos Efectivo+Tarjeta+Transferencia; explicar (sin activar) «Control por denominaciones (modo estricto)»; Límite mínimo 1,000 y máximo 60,000 (umbrales de alerta); «Crear caja» → toast «Caja creada exitosamente» → la tarjeta nueva aparece Cerrada. [1.1.a, 2] | tablero → diálogo → tablero | 75 s |
| 03-panel-configuracion | Botón «Configuración» → panel «Configuración de cajas» › Cajas: cifras Total/Abiertas/Cerradas/Bloqueadas, búsqueda y filtros, «Operativas / Archivadas»; ⋮ de la fila de Caja Mostrador 3 → señalar «Ver detalles», «Bloquear», «Archivar» (archivar = sacarla de uso sin borrar su historia; se restaura desde Archivadas); cerrar el panel. [1, 1.1] | tablero → panel → tablero | 55 s |

Notas: el diálogo de caja NO tiene campo Tipo (no inventarlo). «Abrir sesión» de Caja Principal
solo se señala: la abre la cajera en el video 3.

## Video 2 — «Cajas: denominaciones y políticas de operación» (≈3:20) · graba `admin`
Estado de partida: **S0**. Qué escribe: denominación «Veinte» (RD$20, Billete) propia de la empresa;
`cashier_config.id=1` (umbrales de alerta 1,000 / 60,000). Restaurar: soft-delete de la
denominación nueva (SOLO la de `company_id=29`) y `cashier_config` de S0.

| id | Tarea | Parte de → llega a | Duración |
|---|---|---|---|
| 01-denominaciones | `/cashier?config=denominaciones`: qué es una denominación y para qué sirve (conteo del fondo, conteo de cierre, modo estricto); grupos Billetes/Monedas; «Nueva denominación» → Nombre «Veinte», Valor 20, Divisa DOP, Tipo «Billete», Orden 7 → «Crear denominación» → toast → aparece en Billetes. [1.2] | panel → diálogo → panel | 60 s |
| 02-politicas-fondo-tolerancia | Sub-pestaña «Políticas»: «Estaciones de trabajo» (apagado = modo Flexible, se nombra y no se toca); «Fondos y límites» (fondo inicial por defecto 5,000; mínimo y máximo vacíos); «Tolerancias de diferencia»: modo Monto fijo, RD$50 por método de pago, 3 diferencias consecutivas antes de bloquear; «Control de sesiones» 720 min y feriados. [1.3] | panel → panel | 75 s |
| 03-politicas-aprobaciones-cuadre | «Aprobaciones»: retiros > 5,000 y depósitos > 10,000 esperan a un supervisor; notas obligatorias en retiros. «Umbrales de alerta»: escribir 1,000 (saldo bajo) y 60,000 (exceso). «Cuadre de caja»: requerir cuadre para cerrar ✓, justificación ✓, conteo ciego (explicar, NO activar), ventana de 24 h para reabrir. «Guardar configuración» → toast «Configuración de cajas guardada exitosamente». | panel → panel | 75 s |

⚠ No editar ni eliminar las 10 denominaciones existentes: son catálogo GLOBAL y el API no lo impide
(ver riesgos). Activar «Conteo ciego» cambiaría los videos 5 y 6.

## Video 3 — «Cajas: abre tu caja y registra entradas y salidas» (≈3:40) · graba `yohanna.peralta` (Cajera)
Estado de partida: **S1** (= S0 + umbrales de alerta del video 2). Qué escribe: sesión de
yohanna en Caja Principal (fondo 5,000), entrada 2,000, salida 6,500 PENDIENTE.
Restaurar: volver a S1.

| id | Tarea | Parte de → llega a | Duración |
|---|---|---|---|
| 01-abrir-sesion | Entra a `/cashier?section=cajas`: la cajera solo ve «Cajas» y «Mi caja». Tarjeta «Caja Principal» → «Abrir sesión» → panel «Abrir mi caja»: la caja viene elegida, el cajero es ella, «Fondo inicial» prellenado en 5,000 (política), el recuadro «Conteo del fondo» explica que esta caja no exige conteo por denominaciones; nota «Turno de la mañana»; «Abrir caja» → toast «Caja abierta exitosamente» → aterriza en «Mi caja». [2, 3.1] | tablero → panel → Mi caja | 70 s |
| 02-entrada | «Mi caja»: barra «Caja abierta», «Desglose del efectivo» (fondo = esperado 5,000). «Entrada» → Monto 2,000, Contrapartida «Cuenta contable» (la empresa no tiene bancos: se explica), buscar «Otros ingresos» → «Otros ingresos diversos», nota «Cambio en monedas traído del banco» → «Crear movimiento» → toast «Movimiento MOV-… registrado exitosamente» → la fila en «Movimientos» y el desglose sube a 7,000. [3.2, 3.3] | Mi caja → panel → Mi caja | 75 s |
| 03-salida-pendiente | «Salida» → Monto 6,500, botón «%» calcula el ITBIS incluido (991.53), Contrapartida «Otros gastos generales», nota «Pago del mantenimiento del aire acondicionado» (obligatoria en salidas) → «Resumen del movimiento» → «Crear movimiento» → toast de ADVERTENCIA «…Requiere aprobación de un supervisor antes de afectar el saldo.» → la fila con estado «Por aprobar» (`FE/enums/movement-status.enum.ts:11`) y el saldo sigue en 7,000. Explicar el umbral de 5,000. | Mi caja → panel → Mi caja | 75 s |
| 04-resumen | Pestaña «Resumen» (flujo neto del turno) y «Movimientos» (acciones «Ver detalle» y «Anular movimiento» señaladas: anular pide motivo y solo en la sesión abierta). Mencionar que los cobros en efectivo de facturas (Ventas) suman aquí solos. | Mi caja → Mi caja | 45 s |

## Video 4 — «Cajas: aprueba movimientos y mueve efectivo entre cajas» (≈3:30) · graba `carmen.rosario` (Supervisora)
Estado de partida: **S3** (fin del video 3). Qué escribe: aprobación del MOV de 6,500; transferencia
TRF de 3,000 Caja Mostrador 2 → Caja Principal, recibida. Restaurar: volver a S3.

| id | Tarea | Parte de → llega a | Duración |
|---|---|---|---|
| 01-por-aprobar | `/cashier?section=aprobaciones`: qué es «Por aprobar» y el contador de la pestaña; cifras (Movimientos por aprobar 1, Cuadres por confirmar 0, Cajas bloqueadas 1…); cola «Movimientos pendientes de aprobación» con la salida de 6,500 de yohanna.peralta y su nota → «Aprobar» → diálogo «Aprobar movimiento» («…saldrá del saldo de la sesión y se generará su asiento contable») → «Aprobar» → toast. Explicar «Rechazar» (pide motivo, no toca saldo) y los cuatro ojos. [4.1, 4.2] | Por aprobar → Por aprobar | 75 s |
| 02-nueva-transferencia | Pestaña «Historial» › «Transferencias»: qué es una transferencia entre cajas. «Nueva transferencia» → Caja origen «Caja Mostrador 2» (muestra «Saldo disponible en sesión»), Caja destino «Caja Principal», Monto 3,000, Notas «Reposición de cambio para la caja principal» → «Crear transferencia» → toast «…La caja destino ya puede recibirla.» (bajo 5,000 no pide aprobación). [5] | Historial › Transferencias → diálogo → misma lista | 75 s |
| 03-recibir | Fila de la transferencia, estado «Por recibir» → «Recibir» → diálogo «Recibir transferencia» (N°, monto, origen, destino, la nota de qué hacer si el efectivo no coincide) → «Confirmar recepción» → toast «Transferencia recibida exitosamente» → estado «Recibida». | lista → diálogo → lista | 55 s |

Nota: la cajera NO puede crear ni recibir transferencias desde la UI (no ve «Historial»; ver
riesgos) — por eso lo hace la supervisora.

## Video 5 — «Cajas: cierra tu caja con el conteo de cierre» (≈3:30) · graba `yohanna.peralta`
Estado de partida: **S4** (fin del video 4: esperado en Caja Principal = 5,000 + 2,000 − 6,500 +
3,000 = **3,500**; la alerta de saldo bajo que disparó la salida aprobada puede haberse resuelto
al recibir la transferencia — verificar). Qué escribe: cuadre
REC-… PENDIENTE de yohanna (contado 3,480, −20 dentro de tolerancia) y la sesión CERRADA.
Restaurar: volver a S4.

| id | Tarea | Parte de → llega a | Duración |
|---|---|---|---|
| 01-cerrar-caja | `/cashier?section=caja`: el desglose ahora trae la salida aprobada y la transferencia recibida (explicar cada término hasta «esperado» 3,500). «Cerrar caja» → diálogo «Conteo de cierre requerido» («Para cerrar la caja debes registrar el conteo de cierre…») → «Iniciar conteo» → página «Conteo de cierre (previo al cuadre)» ya en el paso «Ingresar montos». Qué es un arqueo y por qué el cajero declara y el supervisor cuadra. [3.5, 3.6] | Mi caja → diálogo → página de conteo | 65 s |
| 02-ingresar-montos | «Resumen de la sesión» (Fondo inicial · Cobros del turno · Total esperado en caja) y «Ver cálculo»; «Detalles por método de pago»: en «Efectivo» escribir 3,480 → Diferencia −20 «Dentro de ±RD$50.00» → justificación de la línea «Faltan 20 pesos en monedas» (la pide solo si hay diferencia) → «Siguiente». | paso 2 → paso 3 | 80 s |
| 03-registrar-conteo | Paso «Confirmar cuadre»: Total esperado / Total recibido / Diferencia total, aviso «Todos los métodos de pago están dentro de la tolerancia»; «Justificación global» opcional; «Registrar conteo» → toast «Conteo de cierre registrado exitosamente. Un supervisor hará el cuadre oficial.» → vuelve a Mi caja «Sin sesión activa». Explicar que fuera de tolerancia la justificación es obligatoria. | paso 3 → Mi caja | 60 s |

Alternativa didáctica (si se quiere ver el bloqueo previo): antes de 01, con la salida aún pendiente
(estado S3), «Cerrar caja» muestra «Aún no puedes cerrar la caja». Solo si cabe en el tiempo.

## Video 6 — «Cajas: cuadre oficial, arqueo sorpresa y desbloqueo» (≈3:40) · graba `carmen.rosario`
Estado de partida: **S5** (fin del video 5). Qué escribe: confirmación del cuadre de yohanna;
arqueo sorpresa PENDIENTE sobre la sesión de luis.batista (Caja Mostrador 2, sigue abierta);
desbloqueo de «Caja Sucursal Santiago». Restaurar: volver a S5.

| id | Tarea | Parte de → llega a | Duración |
|---|---|---|---|
| 01-aprobar-cuadre | `/cashier?section=aprobaciones` › «Cuadres pendientes de confirmación»: la fila de Caja Principal (Esperado 3,500 · Contado 3,480 · Diferencia −20) → «Ver detalle del cuadre» → diálogo «Detalle del cuadre de caja»: el detalle por método, la justificación, «Reconteo de supervisión» con «Corregir el conteo» (explicar, sin usar) → «Aprobar cuadre» → toast. Explicar «Rechazar cuadre» (vuelve al cajero para recontar) y el bloqueo automático a los 3 cuadres seguidos fuera de tolerancia. [4.2, 4.3] | Por aprobar → diálogo → Por aprobar | 85 s |
| 02-arqueo-sorpresa | «Historial» › «Cuadres» › «Nuevo cuadre» → página «Generar cuadre de caja»: Sesión de caja «Caja Mostrador 2 · … abierta …», Tipo «Arqueo sorpresa» (la nota del tipo dice que no cierra) → «Continuar» → monto contado de Efectivo = esperado (Cuadre exacto) → «Siguiente» → «Generar cuadre» → toast «Arqueo sorpresa registrado exitosamente. La sesión sigue abierta.» | Historial › Cuadres → página → Historial › Cuadres | 75 s |
| 03-desbloquear | Pestaña «Cajas» con filtro «Bloqueadas» → tarjeta «Caja Sucursal Santiago» («Bloqueada: …») → «Desbloquear» → diálogo «Desbloquear caja»: notas, «Resetear contador de diferencias consecutivas», marcar «Confirmo que he verificado…» → «Desbloquear caja» → toast «Caja «Caja Sucursal Santiago» desbloqueada exitosamente» → la tarjeta pasa a Cerrada. Mencionar que bloquear se hace desde Configuración › Cajas (⋮ «Bloquear»). [2, 4.4] | tablero → diálogo → tablero | 60 s |

## Video 7 — «Cajas: historial y análisis» (≈3:10) · graba `carmen.rosario`
Estado de partida: **S6** (fin del video 6). Qué escribe: nada (solo lectura; «Reconocer» una alerta
es opcional y escribe). Restaurar: no hace falta (salvo si se reconoce la alerta).

| id | Tarea | Parte de → llega a | Duración |
|---|---|---|---|
| 01-historial-de-una-caja | Tablero › ⋮ de «Caja Principal» › «Sesiones» → Historial filtrado por esa caja: la sesión de yohanna.peralta cerrada; acciones «Ver detalles», «Reabrir» (auditada, 24 h, solo sin cuadre: señalar, no usar). Sub-pestañas «Movimientos» (entrada, salida aprobada, transferencia recibida; «Exportar» en el ⋮) y «Cuadres» (el REC confirmado; «Recontar la sesión» y «Anular cuadre» explicados). [2, 5] | tablero → Historial | 75 s |
| 02-analisis | «Análisis»: cifras en vivo (Sesiones activas, Cajas abiertas, Bloqueadas, Cuadres pendientes, Efectivo en cajas, Alertas activas); «Reporte diario» con Período «Hoy»; «Cuadres y análisis» (% dentro de tolerancia, diferencia promedio); «Rendimiento» por cajero. [6] | Análisis › Reporte diario → Rendimiento | 75 s |
| 03-alertas-auditoria | «Alertas»: la alerta de saldo bajo que disparó la salida aprobada (umbral de 1,000 del video 2; saldo 500). **Verificar en el ensayo su estado**: `refreshBalanceAlerts` corre también al recibir la transferencia (`API/cashiers/cash-transfer.service.ts:462`) y al cerrar, así que puede figurar ya resuelta: la voz debe decir lo que muestre la pantalla. Acciones «Reconocer / Resolver / Descartar»; «Auditoría»: quién abrió, aprobó y cuadró, con fecha. | Análisis › Alertas → Auditoría | 50 s |

---

## Cobertura (qué queda y dónde)
| Pantalla / diálogo | Video |
|---|---|
| Tablero, filtros, tarjeta, ⋮, «Nueva caja», «Configurar caja» (señalado) | 1 |
| Panel Configuración › Cajas (cifras, filtros, archivadas, ⋮ fila) | 1 |
| Denominaciones (alta) | 2 |
| Políticas (todas) | 2 |
| Abrir mi caja, Mi caja, Entrada, Salida (ITBIS, pendiente), Resumen, Anular/Ver detalle (señalados) | 3 |
| Por aprobar (movimientos), aprobar/rechazar, cuatro ojos | 4 |
| Transferencias: nueva, recibir | 4 |
| Cerrar caja guiado, página de conteo (3 pasos), tolerancia, justificación | 5 |
| Cuadres por confirmar, Detalle del cuadre (reconteo), aprobar/rechazar, auto-bloqueo | 6 |
| Generar cuadre (supervisor), arqueo sorpresa | 6 |
| Desbloquear (tablero + diálogo) | 6 |
| Historial (sesiones, movimientos, cuadres; reabrir, recontar, anular, exportar) | 7 |
| Análisis (5 pestañas, período) | 7 |
| Fuera de la serie mínima (decisión): modo Estaciones/vinculación de dispositivos, impresora, apertura a nombre de otro cajero (`/cashier/sessions/create`), caja en modo estricto con conteo por denominaciones, conteo ciego, rechazo+reconteo, cobro de factura (vive en Ventas). Candidatos a un video 8 «Casos especiales» si el usuario lo pide. |

## Checklist para el guionista (antes de escribir los JSON)
1. Validar en el ensayo el selector del ítem «Cajas» del riel; si no, `navegar`.
2. `article.board-card[aria-label='Caja <nombre>']`: el aria-label antepone «Caja » (con «Caja
   Principal» queda `'Caja Caja Principal'`).
3. `matTooltip` no es atributo fiable: preferir `aria-label` (Por aprobar lo tiene) o
   `button:has(mat-icon:text-is('…'))`.
4. Toast de 3,5 s → `resaltar` inmediato; el toast de advertencia (pendiente) igual.
5. Autocompletar: teclear ≥2 letras y elegir `mat-option:has-text('…')`; dejar 2–3 s de voz tras el
   tecleo (R2).
6. Los diálogos laterales de Cajas se cierran solos al guardar; con «Cancelar» y datos sucios
   preguntan «descartar cambios».
7. El título de la página de conteo cambia con el rol: Cajera «Conteo de cierre (previo al cuadre)»
   / Supervisora «Generar cuadre de caja»; el botón final «Registrar conteo» / «Generar cuadre».
