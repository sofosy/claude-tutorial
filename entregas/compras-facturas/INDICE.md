# Germiva ERP · Serie de tutoriales: Compras — entrada de facturas

Once videos cortos sobre todas las formas de dar entrada a una factura de compra, grabados en vivo sobre la empresa de demostración «Ferretería Germiva» (datos ficticios, RNC del rango 130555) con las pantallas de noviembre de 2026 y la misma voz de la serie de Productos.

La regla que ordena la serie: ¿el comprobante lo emitió el proveedor? Va al buzón de **Facturas Recibidas** (videos 2 a 6). ¿Ya recibiste la mercancía con su orden? Desde la **recepción** (videos 7 y 8). ¿Lo emite tu empresa? **Nueva Factura** (videos 9 a 11).

| # | Video | Duración |
|---|---|---|
| 1 | [Por dónde entra cada factura](01-por-donde-entra.mp4) | 2:00 |
| 2 | [Registrar a mano, por totales](02-manual-por-totales.mp4) | 2:44 |
| 3 | [Por líneas y al contado](03-manual-por-lineas.mp4) | 2:02 |
| 4 | [Importar con IA](04-importar-con-ia.mp4) | 2:07 |
| 5 | [Plantilla de Excel y entrada por lote](05-plantilla-y-lote.mp4) | 1:37 |
| 6 | [El reporte de e-CF recibidos de la DGII](06-reporte-dgii.mp4) | 1:43 |
| 7 | [La factura de una mercancía ya recibida](07-cotejar-recepcion.mp4) | 1:37 |
| 8 | [La factura llega antes que la mercancía](08-mercancia-por-recibir.mp4) | 1:29 |
| 9 | [Comprar a un proveedor informal](09-proveedor-informal.mp4) | 2:03 |
| 10 | [Gastos menores](10-gastos-menores.mp4) | 1:42 |
| 11 | [Pagos al exterior](11-pagos-al-exterior.mp4) | 2:03 |

Cada video trae su `.srt` (subtítulos), `-youtube.txt` (título, descripción y capítulos) y `-miniatura.png`.
Los guiones (`guiones/compras-facturas-NN-*.json`) se generan desde `seeds/compras-facturas/_guiones.py`. Datos de partida: `node seeds/compras-facturas/preparar.mjs A|B` (el video 4 lee la factura con IA: exporta `OPENAI_API_KEY` antes; la clave solo se guarda en la base local). Los archivos que se suben salen de `seeds/compras-facturas/archivos.py` y `factura-ferremateriales.html`.

## Capítulos

### 1. Por dónde entra cada factura (2:00)

- 00:00  Quién emitió el comprobante
- 00:31  Las puertas del buzón
- 01:04  Comprobantes que emite tu empresa
- 01:31  Mercancía ya recibida

Aprenderás:
- La pregunta que decide la pantalla: ¿quién emitió el comprobante?
- Las cuatro formas de que una factura llegue al buzón
- Qué significa «Pendiente» y «Con entrada»
- Cuándo se usa «Nueva Factura» y el listado único de Facturas

### 2. Registrar a mano, por totales (2:44)

- 00:00  La captura manual
- 00:27  Proveedor y comprobante
- 01:03  Condiciones de pago
- 01:21  Montos por totales
- 01:58  Asiento, 606 y dar entrada

Aprenderás:
- Abrir la captura manual y sus tres partes
- Elegir el proveedor y aprovechar su ficha: categoría 606, plazo y cuenta
- Copiar el pie de la factura por totales
- Leer el asiento y el 606 antes de dar entrada
- Guardar borradores para registrar varias facturas

### 3. Por líneas y al contado (2:02)

- 00:00  Proveedor y contado
- 00:40  Por líneas
- 01:24  Resumen y dar entrada

Aprenderás:
- Registrar al contado y elegir el método de pago
- Cambiar a la captura por líneas
- Poner la tasa de ITBIS de cada línea, incluida una exenta
- Por qué la compra al contado nace pagada y sin cuenta por pagar

### 4. Importar con IA (2:07)

- 00:00  Subir la foto
- 00:39  Revisar contra el original
- 01:24  Líneas y dar entrada

Aprenderás:
- Subir fotos o PDF de facturas con «Importar con IA»
- Revisar lo leído al lado del documento original
- Qué pasa cuando el proveedor no está registrado
- Dar entrada a la factura revisada

### 5. Plantilla de Excel y entrada por lote (1:37)

- 00:00  La plantilla
- 00:31  Importar el archivo
- 00:54  Dar entrada en lote

Aprenderás:
- Descargar la plantilla del buzón y cómo se llena
- Importar el archivo: las facturas quedan pendientes
- Dar entrada a varias facturas en lote
- Cuándo una factura no entra por lote

### 6. El reporte de e-CF recibidos de la DGII (1:43)

- 00:00  Subir el reporte
- 00:32  Lo que queda fijo
- 01:09  Dar entrada

Aprenderás:
- Qué es el reporte de e-CF recibidos y dónde se sube
- Qué hace el sistema con cada comprobante del reporte
- Qué datos quedan fijos y cuáles completas tú
- Dar entrada a un comprobante del reporte

### 7. La factura de una mercancía ya recibida (1:37)

- 00:00  La recepción sin facturar
- 00:37  Cotejar la factura
- 01:06  Registrar la factura cotejada

Aprenderás:
- Encontrar la recepción procesada y sin facturar
- Generar la factura de compra desde la recepción
- Qué se coteja: cantidades aceptadas y precio de la orden
- Registrar la factura cotejada y cerrar la recepción

### 8. La factura llega antes que la mercancía (1:29)

- 00:00  La factura que llega primero
- 00:37  Marcar la línea
- 01:00  La recepción en borrador

Aprenderás:
- Registrar una factura de mercancía que todavía no llega
- Marcar las líneas como «Mercancía por recibir»
- La recepción en borrador que abre el sistema
- Quién completa esa recepción y cuándo se mueve el inventario

### 9. Comprar a un proveedor informal (2:03)

- 00:00  Proveedor informal y comprobante
- 00:49  La línea y las retenciones
- 01:22  Pagar desde la caja

Aprenderás:
- Cuándo corresponde el Comprobante de Compras (B11/E41)
- Registrar la compra en «Nueva Factura» con un servicio del catálogo
- Proponer las retenciones del proveedor informal
- Pagar el neto desde la caja

### 10. Gastos menores (1:42)

- 00:00  Formulario libre y tipo
- 00:36  Los conceptos
- 01:06  Pagar desde la caja

Aprenderás:
- Cuándo se usa el comprobante de Gastos Menores (B13/E43)
- Cambiar al formulario libre y escribir conceptos sin catálogo
- Por qué las líneas van exentas
- Pagar el gasto desde la caja

### 11. Pagos al exterior (2:03)

- 00:00  Proveedor del exterior y moneda
- 00:43  La línea y la retención del ISR
- 01:27  A crédito y emitir

Aprenderás:
- Cuándo se usa el comprobante de Pagos al Exterior (B17/E47)
- Registrar la compra en dólares con la tasa del día
- Aplicar la retención del ISR obligatoria
- Emitir la compra a crédito
