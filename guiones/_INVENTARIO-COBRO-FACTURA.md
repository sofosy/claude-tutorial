# Inventario — cobrar una factura en la caja con pago combinado (video 8, 2026-09-23)

Autor video 8. Lectura de código (solo lectura) de `Germiva-api` y `germiva-website` en master local del
23/09/2026 + comprobación en la BD local y en el DOM vivo (empresa demo 43). Rutas relativas a cada repo.

## 1. Dónde se cobra una factura (front)

| Regla | Evidencia |
|---|---|
| El cobro de una factura YA emitida se hace en la propia factura: Ventas › Facturas › abrir la factura → sección **«Cobro»** al pie del formulario + botón **«Cobrar»** en la barra fija | `src/app/modules/sales/invoices/pages/invoice-form/invoice-form.component.html:2305-2326` (panel), `:489-503` y `:553-563` (botón «Cobrar» / «Guardar y Cobrar») |
| El panel sale en una factura emitida mientras quede saldo (también a crédito); NO sale en modo «Ver» (`viewMode`), ni en proformas, ni con total 0 | `invoice-form.component.ts:1256-1275` (`shouldShowInlinePayment`) |
| El panel dice a qué caja entra el cobro: chip «<caja> · Sesión #<id>»; sin sesión y en modo flexible, chip «Pago directo (sin caja)» | `invoice-form.component.ts:3302-3306` (`cashierSessionLabel`); `src/app/modules/invoicing/payment/components/inline-payment-panel/inline-payment-panel.component.html:14-27` |
| Métodos: control segmentado (Efectivo, Tarjeta, Transferencia…); **«Pago combinado (varios métodos)»** es una casilla en la misma fila | `inline-payment-panel.component.html:109-143` |
| Pago combinado: se llena método + monto y se pulsa **«Agregar al recibo»**; cada método queda como chip en una tira con «Asignado» y «Falta» | `inline-payment-panel.component.html:60-100` (tira), `:310-325` (botón) ; `inline-payment-panel.component.ts:328-345` (`splitRemaining`, `canSplit`) |
| Efectivo pide «Monto recibido» (botón «Exacto») y muestra la devuelta; Tarjeta pide «Últimos 4 dígitos», «Tipo de tarjeta» y «Cód. autorización» | `inline-payment-panel.component.html:170-247`, `:275-283` |
| La línea de estado al pie del panel dice en qué queda la factura antes de pulsar | `inline-payment-panel.component.html:402-409` (`paymentOutcome`) |
| La pestaña **«Pagos»** de la factura lista cada recibo con Recibo/referencia · Fecha · Método · Estado · Notas · Monto | `invoice-form.component.html:409-455` |
| El front envía `tenders[]` (un elemento por método) a `POST /v1/payment` | `src/app/modules/invoicing/payment/components/register-payment-dialog/register-payment-dialog.component.ts:394-413`; `inline-payment-panel` → `invoice-form` |

## 2. Cómo el API conecta el cobro con la caja

| Regla | Evidencia |
|---|---|
| Un cobro con `tenders[]` va al canal multi-método: UN recibo (Payment, `RCP-2026-…`) con UNA línea (PaymentDetail) por método | `src/modules/payment/payment.service.ts:1440-1447` (enrutado), `:2251-2460` (`createMultiTenderInternal`) |
| La caja del cobro se resuelve así: 1) si el cliente declara la sesión, debe ser de la empresa, estar abierta y ser del usuario (o de un gestor de sesiones); 2) si no, **la única sesión abierta del usuario que cobra**; 3) sin sesión: modo ESTRICTO rechaza («Esta empresa requiere una sesión de caja abierta para procesar pagos. Abre tu caja…»), FLEXIBLE/NONE cobra **sin caja** (`paymentContext = DIRECT_INVOICE`) | `src/modules/cashiers/cashier-session-access.service.ts:150-192` (`resolveCashFlowSession`); `payment.service.ts:2353-2365`, `:4135-4158` |
| Modo de la empresa: ESTRICTO si `requireCashierSessionForSale` o `paymentCashierMode=STRICT`; por defecto FLEXIBLE. La 43 es FLEXIBLE | `cashier-session-access.service.ts:126-137` |
| La factura queda **PAGADA** si Σ cobros ≥ adeudado; si no, **PAGADA PARCIALMENTE**; la CxC se liquida una vez con el total (método representativo: OTHER si hay mezcla) | `payment.service.ts:2439-2481`, `:2509-2520` |
| En la sesión: el efectivo va a `cash_counts.cashAmount` y lo demás a `cardAmount` (acumulados auxiliares) | `payment.service.ts:2483-2505` |
| **Efectivo esperado** = fondo + cobros en EFECTIVO + entradas + transf. recibidas − salidas − transf. enviadas. **La tarjeta NO entra al efectivo esperado** | `src/modules/cashiers/cashier-session-balance.service.ts:855-885` (`buildBreakdown`), `:887-898` (`cashTotalOf`: solo `CASH`) |
| Totales por método de la sesión (la fuente del cuadre): pagos válidos agrupados por método; tarjeta y cheque → cubeta «tarjeta», transferencia y depósito → «transferencia» | `cashier-session-balance.service.ts:913-946` (`getSessionPaymentTotals`), `:948-981` (`toDrawerBuckets`), `:1091-1107` (pagos anulados/fallidos no cuentan) |
| Los cobros NO crean movimientos de caja (`cash_movements`): no salen en la lista «Movimientos» de Mi caja ni en el flujo neto de «Resumen»; se ven en el término «Cobros en efectivo» del desglose | `germiva-website/src/app/modules/cashier/utils/cash-equation.util.ts:36-57`; `payment.service.ts` no usa `CashMovement` |
| El conteo/cuadre de cierre muestra «Cobros del turno» (todos los métodos) y una fila por método con su esperado | `germiva-website/.../cashier-reconciliation-form-page.component.ts:240-260` y filas `.detail-row` por método |
| Tras cada cobro con caja se recalculan las alertas de saldo | `payment.service.ts:2536-2548` |

## 3. Caminos de UI hasta el cobro (DOM vivo, 23/09) y quién graba

| Hecho | Evidencia |
|---|---|
| Cajero (rol 2) tiene `INVOICE_VIEW`, `INVOICE_CREATE`, `INVOICE_UPDATE`, `PAYMENT_CREATE`, `PAYMENT_VIEW`; NO el permiso de historial de versiones ni `PAYMENT_RECEIPT` | BD `role_permissions` (consulta del 23/09) |
| Con el plan 2 de la demo el riel de la cajera NO trae Ventas (Inicio · RR.HH. · Cajas · Calendario · Inventario · Contabilidad · Configuración); con el plan 15 sí | `exploracion-cajas/v8-02-riel.json` (plan 2), `v8cajera-01-riel.json` (plan 15) |
| La cajera, al abrir una factura: diálogo **«Acceso Denegado — … "Ver Historial de Versiones de Facturas"»** (403 `GET /v1/invoices/versions/…`) → **H-16** | `v8cajera-03-factura-abierta.png/.json` |
| Plan 2 «Emprendedor» (y los ERP 2–5: ninguno trae `SALES_CREDIT`): abrir CUALQUIER factura guardada lanza **«Módulo No Disponible»** (403 `MODULE_NOT_IN_PLAN` de `GET /v1/accounts-receivable/payment-history`, permiso `ACCOUNTS_RECEIVABLE_READ` del módulo `SALES_CREDIT`; la petición no lleva `SKIP_PLAN_ALERT`) → **H-17** | `invoice-form.component.ts:2464-2477`, `:2994`; `core/interceptor/error.interceptor.ts:370-381`; `Germiva-api/src/admin/auth/guards/permission.guard.ts:93-120`; `v8h17-03-factura-abierta.png/.json` (también 403 en `POST /v1/discounts/evaluate-for-invoice` en un borrador) |
| Factura EMITIDA con saldo: en el listado su única acción es «Ver Detalles» → `/view` (solo lectura, sin panel de cobro; el ⋮ trae Ver asiento · Nota de crédito/débito · Generar conduce · Duplicar). El cobro inline solo se alcanza escribiendo la URL sin `/view` → **H-20** | `invoice-list.component.ts:306-327`, `:604-609`; `invoice-form.component.ts:173-175`, `:1257`; `v8-20-ver-detalles.json`, `v8-21-mas-acciones-factura.json` |
| Ventas › Cobros › «Registrar cobro»: el panel dice **«Pago directo (sin caja)»** aunque el usuario tiene su caja abierta (el diálogo no pasa `sessionLabel`), y el API igual asigna el cobro a esa sesión (paso 2 de `resolveCashFlowSession`) → **H-21** | `register-payment-dialog.component.ts:180-196`; `inline-payment-panel.component.html:14-27`; `v8-25-factura-elegida.json` |
| Factura en BORRADOR de contado: el listado ofrece el lápiz «Editar» → formulario con **«Guardar y Cobrar»** y el panel de cobro con el chip «Caja Principal · Sesión #…»; al cobrar se asigna el NCF y la factura pasa a PAGADA; diálogo **«Cobro procesado — La factura se guardó y el pago se registró correctamente.»** (≈ 6 s) → Aceptar → la página se recarga en «Ver Factura … Pagada» | `v8-31…v8-40`; `payment.service.ts:1486-1494` (DRAFT = «emite NCF al cobrar») |
| **Decisión**: graba **`admin.progreso`** con SU PROPIA sesión en Caja Principal, sobre una factura de contado en borrador preparada por ventas (el camino real sin defectos: lápiz «Editar» → «Guardar y Cobrar»), con la empresa 43 en el **plan 15** solo mientras dura S8 (`seeds/cajas/plan-s8.mjs`; es el plan que se pidió al crear la demo, `_DATOS-CAJAS.md` §0.1). Coherente con la regla que enseña el video (el cobro entra a la caja abierta de quien cobra) y sin enseñar ningún defecto como correcto | — |

## 4. Datos (estado S8)

S8 = S1 + plan 15 + factura **1000000001** de CONTADO en BORRADOR, tipo B01, cliente «Constructora Los Pinos»
(RNC ficticio 130555079), 10 × «Cemento gris Portland 42.5 kg» a 450 + 20 × «Varilla corrugada 3/8" x 20 pies»
a 150 = subtotal 7,500 + ITBIS 18 % 1,350 = **RD$8,850.00**, + sesión de `admin.progreso` en Caja Principal
con fondo 5,000. Preparación: `seeds/cajas/preparar-s8.mjs`; restauración: `restaurar.mjs S8` (tablas nuevas
en `_estado.mjs`). Cobro del video: **5,000 en efectivo + 3,850 con tarjeta** (Visa ••••4821, autorización
738214, ficticios) → recibo RCP-2026-000001 con 2 líneas, NCF B0100000001, efectivo esperado 10,000,
«Cobros del turno» 8,850, cuadre: Efectivo 10,000 · Tarjeta 3,850. Entrar al cuadre y «Volver» no escribe
(`cashier_reconciliations` sin cambios, medido).
