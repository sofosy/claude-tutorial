# Germiva ERP · Serie de tutoriales: Fabricación (Inventario)

Cuatro videos cortos, de dos a tres minutos, que enseñan a fabricar con Germiva en el orden en que se aprende: la receta, la orden, los imprevistos y la conexión con ventas. Grabados en vivo sobre la empresa de demostración «Panadería Germiva» (datos ficticios), con el bizcocho de vainilla como ejemplo de principio a fin.

| # | Video | Duración | Estado de partida |
|---|---|---|---|
| 1 | [La lista de materiales](01-lista-de-materiales.mp4) | 3:07 | `node seeds/fabricacion/preparar.mjs A` |
| 2 | [La orden de fabricación](02-orden-de-fabricacion.mp4) | 2:55 | `node seeds/fabricacion/preparar.mjs B` |
| 3 | [Merma, faltantes y trazabilidad](03-merma-faltantes-trazabilidad.mp4) | 2:56 | `node seeds/fabricacion/preparar.mjs C` |
| 4 | [Fabricar para un pedido y sub-ensambles](04-pedido-y-subensambles.mp4) | 2:11 | `node seeds/fabricacion/preparar.mjs D` |

Cada video trae su `.srt` (subtítulos), `-youtube.txt` (título, descripción y capítulos) y `-miniatura.png`.
Los guiones (`guiones/fabricacion-NN-*.json`) se generan desde `seeds/fabricacion/_guiones.py`: se edita ahí y se regenera.

Complementa a la serie «Productos» (`entregas/productos/`), que cubre el catálogo, los empaques, las variantes y las listas de precios.

## Capítulos

### 1. La lista de materiales (3:07)

- 00:00  Dónde está Fabricación
- 00:39  El producto y sus componentes
- 02:09  Mano de obra, costo y publicar

Aprenderás:
- Dónde está Fabricación y qué trae cada pestaña
- Crear la lista de materiales de un producto
- Agregar la mano de obra y los gastos indirectos
- Leer el costo por unidad antes de fabricar
- Publicar la lista y entender sus versiones

Errores comunes que evita:
- Poner las cantidades de una sola unidad cuando la corrida produce varias
- Dejar fuera la mano de obra: el costo sale más bajo que el real
- Creer que editar la lista cambia las órdenes ya creadas: cada orden conserva su versión

### 2. La orden de fabricación (2:55)

- 00:00  Crear la orden y leer el plan
- 00:58  Material reservado
- 01:28  Registrar la producción
- 02:11  Kardex, costo y asiento

Aprenderás:
- Crear una orden de fabricación y leer su plan de materiales
- Qué significa reservar el material
- Registrar la producción y cerrar la orden
- Ver la salida de materia prima y la entrada del producto terminado
- Dónde queda el costo real y el asiento contable

Errores comunes que evita:
- Dejar el producto terminado en el mismo almacén de la materia prima sin querer
- Creer que reservar descuenta la existencia: solo la aparta; se descuenta al registrar la producción
- Registrar sin revisar la columna «Usado» cuando se gastó más material del previsto

### 3. Merma, faltantes y trazabilidad (2:56)

- 00:00  Registrar una merma
- 01:07  Corregir un registro
- 01:31  Cuando falta material
- 02:17  Rastrear un lote

Aprenderás:
- Registrar unidades descartadas y elegir el tratamiento de la merma
- Cómo se corrige un registro de producción
- Guardar una orden en borrador cuando falta material y ver qué comprar
- Leer el tablero de fabricación
- Rastrear un lote hasta las órdenes que lo consumieron

Errores comunes que evita:
- Marcar como pérdida anormal la merma de todos los días: el costo del producto queda más bajo que el real
- Borrar o ajustar a mano la existencia en vez de usar «Corregir este registro»
- Dejar órdenes en borrador sin revisar en el tablero qué material hay que comprar

### 4. Fabricar para un pedido y sub-ensambles (2:11)

- 00:00  Del pedido de venta a la orden
- 00:43  Planificar y fabricar el sub-ensamble
- 01:25  Terminar la orden principal

Aprenderás:
- Planificar la fabricación desde un pedido de venta confirmado
- Qué es un sub-ensamble y cómo lo reconoce el sistema
- Crear las órdenes de los sub-ensambles con un clic
- En qué orden se fabrica: primero lo de adentro
- Cómo el costo del sub-ensamble llega al producto final

Errores comunes que evita:
- Buscar «Planificar fabricación» en un pedido en borrador: solo aparece cuando está confirmado
- Intentar reservar la orden principal antes de fabricar el sub-ensamble
- Comprar un componente que tú mismo fabricas: si tiene lista de materiales, se planifica como sub-ensamble
