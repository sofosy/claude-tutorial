# Investigación · Multimoneda por API (semillas de los videos 34–39)

Lectura del código de Germiva-api y germiva-website en `master` (2026-10-18), para armar
por el API, con datos ficticios propios, el escenario de los videos del bloque B. Rutas con
el prefijo global `/api`; controladores `v1`. `API:` = `Germiva-api/src/`, `WEB:` =
`germiva-website/src/app/`. Referencia adicional: `Germiva-api/docs/qa-contabilidad/seed/seed-year.cjs`
(arma un año multimoneda con los mismos cuerpos).

## Ids que se consultan, no se fijan

| Qué | GET |
|---|---|
| Tipos de NCF (buscar por `name`: B01, B17…) | `/v1/ncf/types`, `/v1/ncf/types/availability` |
| Impuestos («Exento de ITBIS» deja cifras redondas) | `/v1/taxes?limit=50` |
| Bancos del catálogo | `/v1/banks?limit=50` |
| Monedas habilitadas (USD activa, si no 400) | `/v1/company-currencies` |
| Revaluaciones previas (una posterior al corte bloquea) | `/v1/accounting/exchange-revaluation?currencyId=1` |

## 1. Tasa del día

- `POST /v1/exchange-rates/quick` `{"fromCurrencyCode":"USD","toCurrencyCode":"DOP","rate":58.75,"effectiveDate":"2026-09-24"}`:
  upsert por fecha, idempotente (`exchange-rate.service.ts:430-488`). Sin fecha = hoy (lo que hace la pantalla).
- `POST /v1/exchange-rates` no hace upsert: una segunda tasa del mismo día falla por índice único.
- Qué tasa toma cada documento (`currency-conversion.service.ts:97-199`): la factura, la explícita o
  la última registrada hasta su fecha; el cobro/pago, la explícita, o la de la factura si es del mismo
  día, o la registrada a la fecha del pago.

## 2. Cuentas de diferencia cambiaria

- **Por moneda:** `POST /v1/company/currency-exchange-accounts/upsert`
  `{"items":[{"currencyId":1,"mode":"GROSS","gainAccountId":..,"lossAccountId":..}]}` (reemplaza el set;
  `NET` usa una sola cuenta).
- **Generales:** `POST /v1/company/config/upsert` `{"exchangeGainAccount":..,"exchangeLossAccount":..}`
  (parcial). El alta de la empresa ya las llena desde los roles.
- **Roles del mapeo** (grupo «Multimoneda»): `EXCHANGE_GAIN` «Ganancia por Diferencia Cambiaria»
  (4.02.01.03) y `EXCHANGE_LOSS` «Pérdida por Diferencia Cambiaria» (6.05.02). Son los únicos: la
  diferencia realizada y la no realizada usan los mismos.
- **Orden de resolución** (`exchange-account-resolver.service.ts:55-145`): por moneda › cuenta general
  (aviso suave) › rol del mapeo (aviso) › 400 «Falta configuración de cuenta contable…».

## 3. Cuenta bancaria en USD

1. Cuenta contable nueva (la 1.01.01.02.01 ya la usa otro banco):
   `POST /v1/accounting-chart` `{"code":"1.01.01.02.02","name":"…(USD)","type":"asset","nature":"debit","level":5,"parent":<1.01.01.02>,"allowsMovement":true,"isMonetary":true,"reportSection":"CASH_AND_EQUIVALENTS"}`.
2. `POST /v1/bank-accounts` `{"accountName":..,"accountNumber":..,"accountType":"checking","initialBalance":2000,"openingDate":"2026-09-01","initialBalanceExchangeRate":58.40,"bank":<id>,"currency":1,"glAccount":<id>}`.
   El saldo inicial genera un asiento **en USD** (DR banco / CR 3.06.01) con su contravalor en DOP:
   es el que estrena la columna de moneda del Libro Mayor (M12). En la UI «Saldo Inicial» está
   deshabilitado: solo por API.

## 4–5. Venta en USD

- Producto: `POST /v1/product` `{"category":"SERVICE","name":..,"tax":<Exento>,"managesInventory":false}`.
  En la factura, `unitPriceOverride` llega ya en la moneda del documento.
- Cliente: `POST /v1/partner` (RNC repetido → 409).
- `POST /v1/invoices` `{"issuedDate":"2026-09-24","paymentDueDate":"2026-10-24","partner":..,"ncfType":<B01>,"incomeType":1,"paymentType":2,"currency":1,"exchangeRate":58.75,"details":[{"product":..,"quantity":1,"unitPriceOverride":1000}]}` → borrador.
- Emitir: `PATCH /v1/invoices/change-status/{invoiceNumber}` `{"invoiceStatusCode":"EMITTED"}`: NCF,
  CxC (a crédito) y asiento en DOP (DR CxC 58,750 / CR Ventas 58,750). La serie B no va a la DGII.

## 6. Cobro a otra tasa

`POST /v1/payment` `{"invoiceNumber":..,"amount":"1000.00","currency":1,"exchangeRate":59.5,"transactionDate":"2026-10-15","paymentMethodCode":"TRANSFER","chartOfAccount":<banco USD>}`
(mandar siempre `chartOfAccount`). Asiento: DR Banco USD 59,500 / CR CxC 58,750 / CR Ganancia 750.

## 7. Compra en USD, pago y anticipo

- Compra estándar: solo B11/B13/B17 (E41/E43/E47). Proveedor del exterior → **B17**.
  `POST /v1/invoices` con `"ncfType":<B17>,"currency":1,"exchangeRate":59.00,"goods606Category":"02"`
  y `details[].unitPriceOverride`; emitir igual (crea la CxP). Asiento DR gasto / CR CxP.
- Pago: mismo `POST /v1/payment`; a mayor tasa sale pérdida (DR CxP / DR Pérdida / CR Banco).
- Anticipo a proveedor en USD: `POST /v1/supplier-advances` `{"partner":..,"amount":300,"sourceAccount":..,"advanceDate":..,"currency":1,"exchangeRate":58.9}`;
  aplicar con `POST /v1/supplier-advances/apply`. Los anticipos de clientes solo existen en DOP (DP-127).

## 8. Revaluación de cierre

- `POST /v1/accounting/exchange-revaluation/run` `{"asOfDate":"2026-09-30","currencyId":1,"closingRate":59.20}`.
  Revalúa CxC, CxP y bancos USD con cuenta contable. Sin saldos → 400 sin registrar nada.
- Asiento principal `REVAL-USD-<corte>` al corte; asiento `REVAL-USD-<corte>-POST`, **fechado hoy**,
  solo si hubo cobros/pagos entre el corte y el día en que se corre (retira lo ya liquidado).
- Anular: `POST /v1/accounting/exchange-revaluation/{id}/reverse` `{"reason":..}` (storno de todos los
  asientos de la corrida, incluido el «-POST»).

## 9. Pantallas

| Pantalla | Ruta | Textos estables |
|---|---|---|
| Monedas y tasa del día | `/company/currencies` | «Monedas disponibles», «Tasa del día» «1 USD → DOP», estados «Registrada hoy» / «Pendiente», `.rate-input input`, `.save-rate-btn` «Guardar», «Ver histórico», «Hacer por defecto» |
| Histórico de Tasas | `/company/exchange-rate-history` | «Histórico de tasas de cambio», «Por día» / «Por cambios», tarjetas «Última», «Mínima», «Máxima», «Cambios» (solo lectura) |
| Configuración multimoneda | `/company/multi-currency-settings` | «Cuenta de ganancia cambiaria», «Cuenta de pérdida cambiaria», «Cuentas por moneda (opcional)», «Neta (una cuenta)» / «Separada (ganancia y pérdida)», «Agregar moneda», «Guardar cuentas por moneda», «Guardar configuración» |
| Mapeo | `/accounting/configuracion/mapeos` | grupo `h6.module-group__title` «Multimoneda» |
| Cuentas bancarias | `/accounting/banca/cuentas` | columnas «Moneda», «Saldo» (en la moneda de la cuenta) |
| Factura de venta | `/sales/invoices/create` | chip `button.currency-chip-button` «USD · 1=…», equivalencia `.dgii-equivalence`. Con tasa del día, la tasa no se edita |
| Cobro | `/sales/payments` › «Registrar cobro» | «Tasa del pago» (editable), nota «… ganancia cambiaria de …», «Cuenta de destino». El «Cobrar» de la factura no tiene tasa |
| Pago a proveedor | `/purchases/payments` › «Registrar pago» | «Tasa del pago», «Cuenta de origen» |
| Anticipos a proveedor | `/purchases/supplier-advances` | «Registrar Anticipo», «Aplicar a Factura» |
| Revaluación | `/accounting/banca/revaluacion` | «Ejecutar revaluación al cierre», «Revaluaciones previas», «Anular revaluación» |
| Antigüedad por moneda | `/accounting/cobros/analisis`, `/accounting/pagos/analisis` | una sección por moneda |
| Estado de cuenta | `/sales/account-statements` › `/sales/partner-account/{id}`; proveedor en `/accounting/pagos/analisis` | «Resumen en USD», «Documentos en USD» |
| Diario y Mayor | `/accounting/registro/asientos`, `/accounting/registro/mayor` | `span.document-amount` «USD …» solo en asientos denominados en USD |
| Estados financieros | `/accounting/financial-statements/...` | siempre en moneda local |

## Defectos y límites encontrados (ver el plan: M14, M15)

- **M14:** «Ver asiento» rotula RD$ fijo; un asiento en USD (apertura del banco USD) se ve en dólares
  con el rótulo RD$ (`journal-entry-form.component.html:322,339`).
- **M15:** la tabla «Revaluaciones previas» muestra el número del asiento sin enlace y no hay pantalla
  de detalle.
- Ya en el REU (DP-127/DP-128): tasa con fecha pasada en pantalla, asiento manual en USD, anticipos de
  cliente en USD, transferencias USD↔DOP, rótulos «Ganancia DOP» fijos.
