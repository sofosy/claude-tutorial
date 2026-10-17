# Germiva ERP · Tutorial: Punto de venta

Un video completo (15:12) que recorre todo el módulo **Punto de venta** en el orden de una jornada
de caja: entrar, abrir el turno, vender, cobrar de todas las formas, poner ventas en espera,
vender a crédito, registrar movimientos de efectivo y cerrar el turno con el arqueo. Grabado en
vivo sobre la empresa de demostración «Ferretería El Progreso» (datos ficticios), con la cajera
Yohanna Peralta y un catálogo de 25 productos con foto.

| Archivo | Qué es |
|---|---|
| [punto-de-venta.mp4](punto-de-venta.mp4) | El video (1920×1080, voz dominicana, −14 LUFS) |
| [punto-de-venta.srt](punto-de-venta.srt) | Subtítulos por frase |
| [punto-de-venta-youtube.txt](punto-de-venta-youtube.txt) | Título, descripción, capítulos, transcripción y créditos de las fotos |
| [punto-de-venta-miniatura.png](punto-de-venta-miniatura.png) | Miniatura |

## Capítulos

| Tiempo | Capítulo | Qué se ve |
|---|---|---|
| 00:00 | Entrar y abrir el turno | Ícono del menú, pantalla completa, aviso «Abre tu turno para vender» |
| 00:51 | La hoja de apertura | Caja preseleccionada, cajero, fondo inicial, notas, conteo del fondo, píldora del turno |
| 01:45 | El catálogo | Tarjetas con foto, código, existencia y precio con ITBIS; categorías; mosaico de iniciales; Agotado; Quedan 3; Exento; atajos F2–F12 |
| 02:53 | Agregar productos al ticket | Tocar tarjetas, contador azul, búsqueda por nombre, búsqueda sin resultados, lector de código de barras |
| 03:48 | El ticket | Líneas, más/menos, papelera, resumen, descuento global, propina legal, nota |
| 04:57 | Cobrar en efectivo | Formas de pago, aviso de crédito a consumidor final, montos rápidos, teclado, cambio, recibo, gaveta, Venta registrada, NCF |
| 06:41 | Producto agotado | El cobro frena la venta antes de cobrar («Revisa la venta») |
| 07:18 | Poner en espera, retomar y anular | Tickets en espera, menú de la cabecera, anular con confirmación |
| 08:11 | Cliente con RNC y crédito fiscal | Selector de cliente, búsqueda, crear cliente, padrón DGII |
| 09:16 | Pago combinado | Tarjeta (tipo, 4 dígitos, autorización) + transferencia en una factura |
| 10:29 | Venta a crédito | Línea de crédito, vencimiento, «Venta a crédito · saldo por cobrar» |
| 11:46 | Devoluciones | Salida al formulario de devoluciones de Ventas (nota de crédito B04) y regreso |
| 12:23 | Caja y turno | Resumen del turno, formas de pago, efectivo esperado, entrada de efectivo, retiro, reporte X |
| 13:45 | Arqueo y cierre del turno | Conteo por denominaciones, otros medios, diferencia, observaciones, conteo ciego, reporte Z |

## Cómo se hizo

- Guion: `claude-tutorial/guiones/pos-punto-de-venta.json`; datos: `claude-tutorial/seeds/pos/`
  (restaurar con `node seeds/pos/restaurar.mjs P0`).
- Puertas: revisar.mjs 0 errores · ensayo 14 pasos / 200 acciones sin fallos · veredicto
  **PUBLICABLE** · auditoría OCR sin datos reales (sus 4 avisos son el RNC ficticio 130555206 leído
  como 130585206) · revisión de contenido con fotogramas.
- Grabado con el ERP ya corregido: ver `HALLAZGOS-POS.md` en la raíz de germiva.
- Fotos de productos: Wikimedia Commons (CC0, dominio público, CC BY, CC BY-SA); créditos en
  `punto-de-venta-youtube.txt` y en `claude-tutorial/seeds/pos/imagenes/CREDITOS.md`.
