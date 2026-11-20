# Germiva ERP · Serie de tutoriales: Productos (Inventario)

Doce videos sobre el catálogo de productos, grabados en vivo sobre la empresa de demostración «Tienda Germiva» (datos ficticios) con las pantallas de noviembre de 2026. Diez son cortos, de dos a tres minutos; las partes 4 y 5 conservan el formato largo de la serie anterior, regrabadas sobre las pantallas actuales.

| # | Video | Duración |
|---|---|---|
| 1 | [El catálogo](01-catalogo.mp4) | 2:14 |
| 2 | [Crear un producto](02-crear-producto.mp4) | 2:35 |
| 3 | [Servicios, fiscal y tienda en línea](03-servicio-fiscal-tienda.mp4) | 2:21 |
| 4 | [Unidades y empaques](04-empaques.mp4) | 6:53 |
| 5 | [Empaques en compras e inventario](05-compras-e-inventario.mp4) | 6:00 |
| 6 | [Vender por empaque](06-vender-por-empaque.mp4) | 2:53 |
| 7 | [Productos por peso y balanza](07-peso-y-balanza.mp4) | 2:26 |
| 8 | [Convertir la unidad base](08-convertir-unidad-base.mp4) | 2:03 |
| 9 | [Crear un producto con variantes](09-variantes-crear.mp4) | 2:40 |
| 10 | [Variantes por dentro, su existencia y su venta](10-variantes-vender.mp4) | 2:30 |
| 11 | [Comercio exterior e insumos](11-exterior-e-insumos.mp4) | 3:07 |
| 12 | [Listas de precios](12-listas-de-precios.mp4) | 2:06 |

Cada video trae su `.srt` (subtítulos), `-youtube.txt` (título, descripción y capítulos) y `-miniatura.png`.
Los guiones cortos (`guiones/productos-NN-*.json`) se generan desde `seeds/productos/_guiones.py`; los de las partes 4 y 5 se editan directamente. Datos de partida: `node seeds/productos/restaurar.mjs A|B|C`.
Sustituye a la serie de siete partes de octubre de 2026 (queda en el historial de git). `v1-2026-09-27/` es la primera versión, anterior a esa.

La fabricación (listas de materiales y órdenes) tiene su propia serie en `entregas/fabricacion/`.

## Capítulos

### 1. El catálogo (2:14)

- 00:00  Leer el catálogo
- 00:36  Buscar y filtrar
- 01:07  Columnas, importar y alta por foto
- 01:34  Duplicar, desactivar y eliminar

Aprenderás:
- Leer el catálogo: producto, código, precio, stock y estado
- Buscar por nombre o código y filtrar por tipo
- Elegir las columnas, importar desde Excel y el alta por foto
- Cuándo duplicar, desactivar o eliminar un producto

### 2. Crear un producto (2:35)

- 00:00  Nombre, categoría y unidad
- 00:49  Precio y cantidad inicial
- 01:29  Mínimo, máximo y guardar
- 01:58  La ficha guardada

Aprenderás:
- Llenar la ficha de un producto de arriba abajo
- Poner el precio con el ITBIS incluido
- Cargar la cantidad inicial con su costo y su lote
- Definir el stock mínimo y máximo
- Qué gana la ficha al guardar: código de barras y etiqueta

### 3. Servicios, fiscal y tienda en línea (2:21)

- 00:00  Crear un servicio
- 01:14  La pestaña Fiscal
- 01:46  Publicar en la tienda en línea

Aprenderás:
- Crear un servicio y en qué se diferencia de un producto
- Para qué sirve la cuenta contable de ingreso
- Dónde van la propina legal y otros impuestos adicionales
- Publicar un producto o servicio en la tienda en línea

### 4. Unidades y empaques (6:53)

- 00:00  La unidad base
- 00:56  Activar los empaques
- 01:37  La caja: contenido, fracciones, compra y venta
- 02:38  Código de barras y precio propio de la caja
- 03:18  El paquete que solo se vende
- 04:15  Mínimo y máximo en cajas
- 05:00  Mínimo y máximo por almacén
- 06:02  Quitar un empaque y resumen

Aprenderás:
- Entender la unidad base y por qué la existencia y el costo siempre se llevan en ella
- Activar los empaques en un producto y agregar una caja con su contenido y sus fracciones
- Decidir dónde se ofrece cada empaque y cuál se propone al comprar y al vender
- Darle a la caja su propio código de barras y su precio propio, o dejar que se derive
- Capturar el mínimo y el máximo en cajas y fijar reglas por almacén

### 5. Empaques en compras e inventario (6:00)

- 00:00  Por reponer sugiere cajas
- 01:05  La orden de compra en cajas
- 02:14  Aprobar y confirmar la orden
- 03:02  Recibir las cajas y procesarlas a inventario
- 04:02  Existencias y kardex con su equivalencia
- 04:59  Un traslado capturado en cajas

Aprenderás:
- Leer «Por reponer»: la sugerencia redondeada a cajas completas y la requisición que crea
- Comprar en cajas: la orden propone la caja y su costo
- Recibir cajas y procesarlas a inventario como unidades
- Leer la existencia y el kardex con su equivalencia en cajas y el costo por unidad
- Registrar un traslado entre almacenes capturado en cajas

### 6. Vender por empaque (2:53)

- 00:00  Facturar por paquete y por caja
- 01:27  La caja en el punto de venta
- 02:09  Las ventas en el kardex

Aprenderás:
- Facturar por paquete y por caja el mismo producto
- Cuándo un empaque usa su precio propio y cuándo se deriva de la unidad
- Vender la caja en el punto de venta escaneando su código
- Leer en el kardex las salidas por empaque

### 7. Productos por peso y balanza (2:26)

- 00:00  Activar la balanza
- 00:44  Preparar el producto
- 01:45  Cobrar con la etiqueta de peso

Aprenderás:
- Activar la balanza etiquetadora y entender su formato
- Agregar el kilo como empaque de un producto que se lleva por libra
- Asignar el código de balanza del producto
- Cobrar en el punto de venta escaneando la etiqueta de peso

### 8. Convertir la unidad base (2:03)

- 00:00  El caso: de cajas a unidades
- 00:32  Ver el impacto y convertir
- 01:25  La ficha después de convertir

Aprenderás:
- Cuándo hace falta convertir la unidad base
- Usar «Ver impacto» antes de convertir
- Qué cambia: existencia, costo, precio, mínimo y máximo
- Cómo queda la caja como empaque después de convertir

### 9. Crear un producto con variantes (2:40)

- 00:00  Un producto con variantes
- 00:55  Opciones y valores
- 01:49  Recargo, matriz y guardar

Aprenderás:
- Cuándo conviene un producto con variantes
- Definir las opciones y sus valores
- Poner un recargo por tamaño
- Leer la matriz y elegir qué combinaciones crear

### 10. Variantes por dentro, su existencia y su venta (2:30)

- 00:00  El padre y sus variantes
- 00:48  Darle existencia a una variante
- 01:45  Vender una variante

Aprenderás:
- Diferenciar el producto padre de sus variantes
- Crear una combinación nueva desde la matriz
- Registrar la entrada de mercancía de una variante
- Vender una variante desde el selector del punto de venta

### 11. Comercio exterior e insumos (3:07)

- 00:00  Comercio exterior
- 00:53  Un producto que se prepara
- 01:46  Cantidades, merma y margen

Aprenderás:
- Registrar la partida arancelaria, el origen y los pesos de un producto importado
- Agregar los insumos que consume un producto preparado
- Poner la cantidad real y la merma de cada insumo
- Leer el costo de insumos y el margen teórico

### 12. Listas de precios (2:06)

- 00:00  Crear una lista calculada
- 00:55  Asignarla a un cliente
- 01:22  El precio en la factura

Aprenderás:
- Dónde se definen las listas de precios
- Crear una lista calculada sobre otra, con redondeo
- Asignar la lista a un cliente
- Ver el precio de la lista en la factura
