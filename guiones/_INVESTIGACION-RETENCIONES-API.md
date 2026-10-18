# Investigación · Retenciones de ISR e ITBIS y carta de retención por API (videos 40–49)

Lectura del código de Germiva-api y germiva-website en `master` (2026-10-18) para armar por el
API, con datos ficticios propios, el escenario de los videos del bloque C. Rutas con el prefijo
`/api`; controladores `v1`. El `ValidationPipe` usa `whitelist`: un campo mal escrito se descarta
sin avisar. La empresa sale siempre de la sesión.

## Reglas que mandan sobre los datos

- **Ley 30-26:** ISR honorarios/alquileres de persona física **15 %**; servicios técnicos **3 %**. Manda
  la **fecha del comprobante**; una tasa distinta a la del tipo da 400 «Inconsistencia de retención…».
- **Matriz de retenciones** (modo `warn` en local): clasifica al proveedor solo por la **longitud** del
  documento (11 dígitos = persona física, 9 = sociedad).
  - Comprobante de Compras (B11/E41) → ITBIS `itbis-comprobante-compras-100` y, si es servicio, ISR
    `isr-honorarios-pf-10` (sugeridos).
  - B01/E31 + persona física + servicio → `itbis-pf-to-pj-100` + `isr-honorarios-pf-10`.
  - El 30 % de sociedades (`itbis-sociedades-servicios-30`) solo con B01/E31 y RNC; no se sugiere.
- **Comprobante contra contribuyente:** B11/E41 **solo** a un informal con cédula; B01/E31 nunca a un
  informal. Hacen falta dos personas físicas: una informal (B11) y una formal (B01).
- Cédula y RNC: solo se mide la longitud (sin dígito verificador obligatorio); no hay consulta en
  línea a la DGII (padrón local). Enviar siempre `isInformalTaxpayer`.
- Período contable abierto en octubre 2026 (sin período, el asiento queda pendiente y el pago falla).
- La compra estándar/libre solo ofrece B11/B13/B17 (E41/E43/E47); el B01 de un proveedor entra por
  el Buzón (registro manual). E41 exige certificado: en local se usa **B11**.

## Proveedores y cliente — `POST /v1/partner`

Campos: `name`, `tin`, `partnerType` (`SUPPLIER`/`CUSTOMER`), `partnerCategory` (`PERSON`/`BUSINESS`),
`documentType` (`RNC`/`CEDULA`), `isInformalTaxpayer`, `isRetentionAgent` (cliente), `customerType`
(si es cliente), `addresses[]`, `contacts[]`. RNC repetido como proveedor → 409.

## Tipos de retención

`GET /v1/tax-retention-types/by-dgii-code/<slug>?asOf=2026-10-15`; lista `GET /v1/tax-retention-types`;
historial `GET /v1/tax-retention-types/:id/rates` (no registrar tasas nuevas en la base del video).
`GET /v1/tax-retention-types/active?ncfTypeCode=B11&supplierTaxId=..&isService=true` trae el
veredicto de la matriz (`ALLOWED|WARNING|BLOCKED`) y lo sugerido: es lo que usa «Proponer retenciones»
(se calcula en el frontend, no hay endpoint propio).

## Compra con retención

- Libre: `POST /v1/invoices/inline`; estándar: `POST /v1/invoices` (exige producto y `rnc`+`legalName`).
  Nacen en borrador; emitir con `PATCH /v1/invoices/change-status/:invoiceNumber {"invoiceStatusCode":"EMITTED"}`.
- Por línea: `retentionAgentIndicator: 1`, `itbisWithholdingRate` (30/100, % del ITBIS),
  `isrWithholdingRate` (15/3, % del neto). En cabecera: `itbisTaxRetentionType`, `isrTaxRetentionType`
  (enviarlos siempre). `goods606Category: "02"`.
- B01 del proveedor: `POST /v1/supplier-document-inbox/manual {"invoice": CreateRawInvoiceDto}` con
  `ncf`, `ncfTypeCode:"01"`, `paymentTypeCode:"2"`, `buyerRnc`/`buyerLegalName` (= el proveedor),
  `recordAsPurchase:true`, `details[]` y `totals{… totalItbisWithheld, totalIsrWithheld}`. Nace emitida.
- Efectos al emitir: filas `purchase_tax_withholdings` (`RET-<id>-ITBIS|ISR`, «Aplicada»); asiento con
  CR CxP por el **neto** y una línea CR por tipo («Retención ITBIS/ISR por Pagar» o el rol granular del
  tipo); CxP neta.

## Corregir retenciones

`PATCH /v1/invoices/purchase-retentions/:invoiceNumber {"itbisWithheldAmount","isrWithheldAmount","itbisTaxRetentionType","isrTaxRetentionType"}`.
Solo compras emitidas; cambiar montos exige la CxP sin pagos (solo el tipo se permite aunque esté
pagada). Bloqueado si la compra está en una carta vigente. Para compras pagadas: «Corregir compra»
(`PATCH /v1/purchase-correction/:invoiceNumber`, con vista previa).

## Pago al neto

`POST /v1/payment {"invoiceNumber","amount","paymentMethodCode":"TRANSFER","transactionDate","chartOfAccount"}`.
El tope es el neto. La retención no cambia de estado; la fecha del pago la toman el 606 (columna 7) y
la carta. Con la carta emitida ya no se puede cambiar la fecha del pago.

## Retenciones que te hacen tus clientes

- **Al cobrar:** `POST /v1/payment` con `itbisRetenido` / `isrRetenido`. Asiento DR «Retención de
  ITBIS/ISR a Favor» / CR CxC; va al 607 del período del cobro. No crea fila en «Retenciones recibidas».
- **En la factura de venta:** mismas columnas por línea; la factura queda neta y crea `TW-<factura>-ITBIS`
  («Retenciones recibidas»).
- **Manual:** `POST /v1/tax-withholdings` (sin asiento).

## Carta de retención

- «Firma y destinatario»: `PUT /v1/withholding-certificates/settings`
  `{"signerName","signerTitle","city","addressee":"dgii|supplier|whom_it_may_concern","includeSeal","includeSignature","closingNote"}`.
- Firma, sello y membrete: `POST /v1/media/upload` (multipart, solo imagen) y `POST /v1/company-media`
  `{"company":1,"media":<id>,"type":"signature|seal|letterhead|logo"}`. El PDF solo imprime PNG/JPG.
- Emisión (`withholding-certificate.controller.ts`):

| Acción | Endpoint |
|---|---|
| Estados por proveedor del período (por fecha de **pago**) | `GET /v1/withholding-certificates/candidates?startDate&endDate` |
| Vista previa | `GET /v1/withholding-certificates/preview?partner&startDate&endDate` |
| Emitir una / reemitir | `POST /v1/withholding-certificates {"partner","startDate","endDate"[,"replaceExisting":true]}` |
| Emitir pendientes | `POST /v1/withholding-certificates/bulk {"startDate","endDate"}` |
| PDF | `GET /v1/withholding-certificates/:id/pdf` |
| Enviar por correo | `POST /v1/withholding-certificates/:id/send {"email"}` (usa Novu: sin Novu en local responde 503) |
| Anular | `POST /v1/withholding-certificates/:id/cancel {"reason"}` |

- Número `CR-2026-000001` por empresa y año. «Desactualizada» si cambia lo certificado; la forma de
  provocarlo sin tocar una compra certificada es pagar otra compra con retención del mismo proveedor
  dentro del mismo rango.
- Estados: Borrador, Emitida, Enviada, Entregada, Recibida, Vencida, Anulada.

## Reportes

606 (`/v1/dgii-reports/606?period=202610`, mes de emisión; columna 7 = fecha de pago), IR-17 (mes de
la factura; secciones II ISR y III ITBIS), IT-1 sección A (casillas 39 PF→PJ 100 %, 43 sociedades 30 %,
47 Comprobante de Compras). La carta va por mes de pago: para el video, factura y pago en octubre.

## Pantallas

| Pantalla | Ruta | Textos estables |
|---|---|---|
| Consola | `/accounting/fiscal/:tab` | pestañas «Retenciones recibidas», «Retenciones practicadas», «Cartas de retención», «Tipos de Retención» |
| Tipos de Retención | `…/tipos-retencion` | «Tipos de Retención DGII»; el diálogo trae «Historial de tasas» |
| Mapeo | `/accounting/configuracion/mapeos` | roles «Retención ITBIS por Pagar», «Retención ISR por Pagar», «Retención de ITBIS a Favor», «Retención de ISR a Favor» y los granulares |
| Compra | `/purchases/invoices/create` (`?form=standard|libre`) | columna «Ret./Perc.», `.add-retention-perception-btn`, modal «Configurar Retención», `.voucher-retention-notice button` «Proponer retenciones», «TOTAL A PAGAR» |
| Corregir retenciones | vista de la compra | `.retention-correction button`, diálogo «Corregir retenciones» |
| B01 del proveedor | `/purchases/received-invoices` › «Registrar manual» | sección «Retenciones», «Dar entrada» |
| Cobro | `/sales/payments` › «Registrar cobro» | «Retenciones del cliente (opcional)» |
| Cartas | `…/cartas-retencion` | «Cartas de retención a proveedores», `.wc__intro button` «Firma y destinatario», filtros «Mes» (por defecto el anterior) y «Año», `.wc__bulk` «Emitir pendientes (N)», badges «Por emitir», «Sin pagos», «… · desactualizada», historial «Cartas emitidas» |
| Mi Empresa | `/my-company` › «Logo y Archivos» › «Subir imágenes» | casillas Logo / Sello / Firma / Membrete |
| Reportes | `/dgii-reports/606`, `/ir-17`, `/it-1` | «Generar» |

## Cifras propuestas (octubre 2026, ITBIS 18 %)

- A — B11 a persona física informal: 20,000 + 3,600 → retiene ITBIS 3,600 + ISR 3,000 → neto 17,000.
- B — B01 de persona física formal (honorarios): 50,000 + 9,000 → ITBIS 9,000 + ISR 7,500 → neto 42,500.
- C — B01 de sociedad (servicios): 100,000 + 18,000 → ITBIS 30 % = 5,400 → neto 112,600.
- Venta a un cliente agente de retención: 118,000; retiene 5,400 → se cobran 112,600.
