import json, copy
base = json.load(open('guiones/productos-04-ventas-pos.json', encoding='utf-8'))
g = {k: copy.deepcopy(v) for k, v in base.items() if k not in ('pasos', 'aprenderas', 'errores_comunes', '_comentario', 'titulo', 'descripcion', 'setup')}
g['titulo'] = "Productos · Parte 5: productos pesados, balanza y cambio de unidad base"
g['descripcion'] = ("Quinta parte de la serie de Productos de Germiva ERP: los productos que se venden por peso y el cambio de unidad base. "
  "Se activa la balanza etiquetadora de la tienda; las habichuelas, que se llevan por libra, reciben el kilo (con su factor automático), "
  "el saco de cien libras para comprar y su código de balanza; en el punto de venta, la etiqueta de peso entra con las libras exactas. "
  "Por último, las galletas que se llevaban por caja pasan a llevarse por unidad con «Convertir unidad base», viendo antes el impacto.")
g['_comentario'] = ("Serie Productos v3, video 5. Estado A (restaurar.mjs A): balanza apagada (scale_label_format NULL); Habichuelas rojas "
  "por Libra, RD$85 exento, 250 lb; Galletas soda Crocante con unidad base Caja/Cajón, 20 cajas a RD$180, RD$300 con ITBIS, mín 5 / máx 40. "
  "Etiqueta: 21 + 00123 + 02350 + 9 = 2100123023509 → 2.35 lb = RD$199.75. Tras guardar la configuración, la página sigue «sucia» "
  "y un goto dispararía beforeunload: el paso 2 sale por el panel (navegación interna). Tras convertir, la ficha no refresca el precio: "
  "el paso 5 la reabre desde el catálogo (precio 25.00, costo 15, 240 unidades).")
g['setup'] = {"tipo": "shell", "cmd": "node seeds/productos/restaurar.mjs A"}
g['aprenderas'] = [
  "Activar la balanza etiquetadora de la tienda y leer su formato",
  "Agregar el kilo a un producto por libra: el factor sale solo",
  "Dar código de balanza a un producto y venderlo escaneando la etiqueta de peso",
  "Convertir la unidad base de caja a unidad, revisando antes el impacto en existencia, costo, precios y límites"]
g['errores_comunes'] = [
  "Usar el prefijo 20 para la balanza: es el de los códigos internos del sistema",
  "Cambiar la unidad de medida a mano en la ficha en vez de convertir: la existencia y el costo quedarían en la unidad vieja",
  "Convertir sin leer el impacto: los precios que no se dividen exacto se redondean"]
F = False
DLG = ".custom-alert-dialog-panel mat-dialog-container"
UP = "app-product-units-panel"
CONV = "mat-dialog-container"
g['pasos'] = [
{"id": "01-balanza", "capitulo": "Activar la balanza", "rotulo": "Balanza etiquetadora", "ruta": "Inventario › Configuración",
 "texto_pantalla": "Configuración · la balanza etiquetadora y el formato de su etiqueta",
 "narracion": "En esta parte vemos los productos que se venden por peso, y cómo cambiar la unidad base de un producto. Empezamos por la balanza. Entro a Inventario y abro Configuración. Bajo hasta balanza etiquetadora. La balanza es de la tienda, no de un producto: imprime una etiqueta con el código del producto y el peso dentro del código de barras. Enciendo uso balanza etiquetadora. Aparece el formato: el prefijo veintiuno, cinco dígitos para el código del producto, cinco para el peso, y tres decimales. Son los valores de las balanzas más comunes; se ajustan a la de tu tienda. Debajo, un ejemplo: veintiuno, el producto ciento veintitrés, y dos mil trescientos cincuenta, que con tres decimales son dos punto treinta y cinco. Pulso guardar, y el aviso confirma; lo cierro.",
 "acciones": [
  {"click": "nav.module-rail [aria-label='Inventario']", "al_decir": "Entro a Inventario"},
  {"click": ".panel-item:has-text('Configuración')", "al_decir": "abro Configuración"},
  {"resaltar": "h3.section-title:has-text('Balanza etiquetadora')", "durante_ms": 3000, "al_decir": "Bajo hasta"},
  {"resaltar": ".switch-row:has-text('Uso balanza etiquetadora')", "durante_ms": 7000, "cursor": F, "al_decir": "La balanza es de la tienda"},
  {"click": ".switch-row:has-text('Uso balanza etiquetadora') mat-slide-toggle button", "al_decir": "Enciendo uso balanza"},
  {"resaltar": "[formgroupname='scaleLabelFormat']", "durante_ms": 9000, "al_decir": "Aparece el formato"},
  {"resaltar": "p.field-note:has-text('Ejemplo')", "durante_ms": 8000, "al_decir": "Debajo, un ejemplo"},
  {"click": ".footer-right button:has-text('Guardar')", "al_decir": "Pulso guardar"},
  {"resaltar": DLG, "durante_ms": 2000, "cursor": F, "al_decir": "el aviso confirma"},
  {"click": "mat-dialog-container button:has-text('Entendido')", "al_decir": "lo cierro"}]},
{"id": "02-habichuelas", "capitulo": "Un producto por libra: kilo, saco y código de balanza", "rotulo": "Habichuelas por libra", "ruta": "Inventario › Productos › Habichuelas rojas",
 "texto_pantalla": "Ficha · el kilo con su factor automático, el saco para comprar y el código de balanza",
 "narracion": "Ahora un producto que se vende por peso: las habichuelas. Abro Productos, la lista de todo el catálogo. En el buscador escribo habichuelas, y abro su ficha con el lápiz. Su unidad base es la libra: la existencia y el precio, ochenta y cinco pesos, están por libra. Enciendo se compra o se vende en empaques, y agrego el primero. Debajo, en rojo, el panel avisa que falta elegir la unidad. Abro la lista de unidades y elijo kilogramo. Fíjate en el contenido: dos punto dos libras, y no hay que escribirlo, porque libra y kilo son de la misma familia de peso y el sistema conoce la equivalencia. En fracciones elijo dos decimales, para vender un kilo y medio. Agrego otro empaque: el saco, en que lo trae el proveedor. Abro la lista y elijo saco. El aviso rojo cambia y pide cuántas libras trae: cien libras. Este solo se compra: le quito el casillero de venta y le pongo la estrella de compra. Por último, a la derecha, el código de balanza: escribo ciento veintitrés, el mismo del ejemplo. Guardo la ficha, y acepto el aviso.",
 "acciones": [
  {"click": ".panel-item:has-text('Productos')", "al_decir": "Abro Productos"},
  {"resaltar": "table tbody", "durante_ms": 2000, "cursor": F, "al_decir": "la lista de todo"},
  {"escribir": {"sel": "mat-form-field:has(mat-label:text-is('Buscar')) input", "texto": "Habichuelas"}, "al_decir": "escribo habichuelas"},
  {"click": "table tbody tr:has-text('Habichuelas rojas') button[aria-label='Abrir']", "al_decir": "con el lápiz"},
  {"resaltar": "mat-form-field:has(mat-label:has-text('Unidad de medida'))", "durante_ms": 3500, "al_decir": "Su unidad base"},
  {"resaltar": "app-inline-product-prices mat-form-field:has(mat-label:has-text('Precio de venta'))", "durante_ms": 3000, "al_decir": "ochenta y cinco pesos"},
  {"click": "button[aria-label='Se compra o se vende en empaques']", "al_decir": "Enciendo se compra"},
  {"click": f"{UP} button:has-text('Agregar empaque')", "al_decir": "agrego el primero"},
  {"resaltar": f"{UP} .units-error", "durante_ms": 3000, "cursor": F, "al_decir": "en rojo"},
  {"click": f"{UP} tbody tr:nth-child(1) mat-select[aria-label='Unidad del empaque']", "al_decir": "Abro la lista de unidades"},
  {"click": "mat-option:has-text('Kilogramo')", "al_decir": "elijo kilogramo"},
  {"resaltar": f"{UP} tbody tr:nth-child(1) td[data-label='Contenido']", "durante_ms": 8000, "al_decir": "en el contenido"},
  {"click": f"{UP} tbody tr:nth-child(1) mat-select[aria-label='Fracciones permitidas']", "al_decir": "En fracciones"},
  {"click": "mat-option:has-text('2 decimales')", "al_decir": "dos decimales"},
  {"click": f"{UP} button:has-text('Agregar empaque')", "al_decir": "Agrego otro empaque"},
  {"click": f"{UP} tbody tr:nth-child(3) mat-select[aria-label='Unidad del empaque']", "al_decir": "Abro la lista y elijo"},
  {"click": "mat-option:has-text('Saco')", "al_decir": "elijo saco"},
  {"resaltar": f"{UP} .units-error", "durante_ms": 2500, "cursor": F, "al_decir": "El aviso rojo cambia"},
  {"escribir": {"sel": f"{UP} tbody tr:nth-child(3) input[aria-label='Contenido en unidades base']", "texto": "100"}, "al_decir": "cien libras"},
  {"click": f"{UP} tbody tr:nth-child(3) td[data-label='Venta'] mat-checkbox", "al_decir": "le quito el casillero"},
  {"click": f"{UP} tbody tr:nth-child(3) button[aria-label='Proponer al comprar']", "al_decir": "la estrella de compra"},
  {"escribir": {"sel": "input[formcontrolname='scalePlu']", "texto": "123"}, "al_decir": "escribo ciento veintitrés"},
  {"click": ".form-layout-footer button:has-text('Guardar')", "al_decir": "Guardo la ficha"},
  {"resaltar": DLG, "durante_ms": 1500, "cursor": F, "al_decir": "y acepto"},
  {"click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "el aviso"}]},
{"id": "03-pos-etiqueta", "capitulo": "Vender con la etiqueta de peso", "rotulo": "Etiqueta de balanza", "ruta": "Punto de venta",
 "texto_pantalla": "Punto de venta · la etiqueta de peso entra con las libras exactas",
 "navegar": "/pos",
 "narracion": "Vamos al punto de venta. El cliente pide habichuelas; se pesan en la balanza, y la balanza imprime una etiqueta. En el buscador escaneo esa etiqueta; aquí escribo su código y pulso Enter, como hace el lector. El ticket recibe las habichuelas con dos punto treinta y cinco libras: el peso venía dentro del código. El precio es por libra, ochenta y cinco, exento de ITBIS, y la línea suma ciento noventa y nueve con setenta y cinco. Abajo, artículos lo dice en libras. Así se vende cualquier producto pesado: sin teclear el peso, y sin errores al cobrar.",
 "acciones": [
  {"escribir": {"sel": "input[aria-label='Buscar producto']", "texto": "2100123023509"}, "al_decir": "escaneo esa etiqueta"},
  {"presionar": {"tecla": "Enter"}, "al_decir": "pulso Enter"},
  {"resaltar": ".ps-line:has-text('Habichuelas')", "durante_ms": 6000, "al_decir": "El ticket recibe"},
  {"resaltar": ".ps-line:has-text('Habichuelas') .ps-line__unit", "durante_ms": 5000, "al_decir": "El precio es por libra"},
  {"resaltar": ".ps-line:has-text('Habichuelas') .ps-line__total", "durante_ms": 4000, "al_decir": "la línea suma"},
  {"resaltar": ".ps-summary__row:has-text('Artículos')", "durante_ms": 4000, "al_decir": "Abajo, artículos"}]},
{"id": "04-convertir", "capitulo": "Convertir la unidad base", "rotulo": "Convertir unidad base", "ruta": "Inventario › Productos › Galletas soda Crocante",
 "texto_pantalla": "Convertir unidad base · de caja a unidad, viendo antes el impacto",
 "navegar": "/inventory/product/list",
 "narracion": "Último caso: las galletas. Hasta hoy se llevaban por caja, y ahora la tienda quiere venderlas sueltas. Eso no se resuelve cambiando la unidad de medida a mano: hay que convertir la unidad base. En el catálogo busco galletas y abro su ficha. Enciendo empaques, que se guarda al momento, y abajo, en unidad base, pulso convertir unidad base. Elijo la unidad nueva: unidad. Cuántas trae cada caja: doce. Pulso ver impacto. Arriba, el resumen: una caja son doce unidades, la existencia pasa de veinte a doscientas cuarenta, y el valor del inventario no cambia. El aviso amarillo dice que el precio no se divide exacto y se redondea; lo acepto. En la tabla, el costo pasa de ciento ochenta por caja a quince por unidad, y el mínimo y el máximo se multiplican por doce. Y la caja queda como empaque, a trescientos pesos, para seguir comprándola igual. Pulso convertir, confirmo, y el aviso dice que la caja quedó como empaque por doce.",
 "acciones": [
  {"escribir": {"sel": "mat-form-field:has(mat-label:text-is('Buscar')) input", "texto": "Galletas"}, "al_decir": "busco galletas"},
  {"click": "table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Abrir']", "al_decir": "abro su ficha"},
  {"click": "button[aria-label='Se compra o se vende en empaques']", "al_decir": "Enciendo empaques"},
  {"click": "button:has-text('Convertir unidad base')", "al_decir": "pulso convertir"},
  {"click": f"{CONV} mat-select[formcontrolname='unitMeasureId']", "al_decir": "Elijo la unidad nueva"},
  {"click": "mat-option:has-text('Unidad') >> nth=0", "al_decir": "unidad. Cuántas"},
  {"escribir": {"sel": f"{CONV} input[formcontrolname='factor']", "texto": "12"}, "al_decir": "doce"},
  {"click": f"{CONV} button:has-text('Ver impacto')", "al_decir": "Pulso ver impacto"},
  {"resaltar": f"{CONV} .gm-dialog-facts", "durante_ms": 9000, "al_decir": "Arriba, el resumen"},
  {"resaltar": f"{CONV} .gm-dialog-alert--warning", "durante_ms": 3500, "al_decir": "El aviso amarillo"},
  {"click": f"{CONV} mat-checkbox:has-text('Acepto los redondeos')", "al_decir": "lo acepto"},
  {"resaltar": f":nth-match({CONV} .conversion-table, 2) tbody tr:has-text('Costo promedio')", "durante_ms": 5000, "al_decir": "el costo pasa"},
  {"resaltar": f":nth-match({CONV} .conversion-table, 2) tbody tr:has-text('Mínimo')", "durante_ms": 3500, "al_decir": "el mínimo y el máximo"},
  {"resaltar": f"{CONV} p.gm-dialog-note:has-text('Se crea el empaque')", "durante_ms": 5000, "al_decir": "la caja queda como empaque"},
  {"click": f"{CONV} button:has-text('Convertir'):not(:has-text('Sí'))", "al_decir": "Pulso convertir"},
  {"click": "button:has-text('Sí, convertir')", "al_decir": "confirmo"},
  {"resaltar": DLG, "durante_ms": 3000, "cursor": F, "al_decir": "el aviso dice"},
  {"click": "mat-dialog-container button:has-text('Entendido')", "al_decir": "por doce"}]},
{"id": "05-galletas-resultado", "capitulo": "La ficha después de convertir", "rotulo": "Galletas por unidad", "ruta": "Inventario › Productos › Galletas soda Crocante",
 "texto_pantalla": "Ficha · unidad base Unidad, precio y costo por unidad, la caja como empaque",
 "navegar": "/inventory/product/list",
 "narracion": "Para ver la ficha con todos sus datos nuevos, vuelvo a abrir las galletas desde el catálogo. Arriba, el stock: doscientas cuarenta, y el costo promedio, quince pesos. La unidad de medida ahora es unidad. El precio de venta, veinticinco pesos con ITBIS, que es trescientos entre doce. Y en unidades y empaques, la caja por doce con su precio de trescientos y la estrella de compra: se sigue comprando por caja, y ahora se vende también suelta. Si te equivocaste, la conversión se puede revertir mientras el producto no tenga movimientos nuevos. En la próxima parte vemos las variantes: tallas, colores y sabores de un mismo producto.",
 "acciones": [
  {"escribir": {"sel": "mat-form-field:has(mat-label:text-is('Buscar')) input", "texto": "Galletas"}, "al_decir": "vuelvo a abrir"},
  {"click": "table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Abrir']", "al_decir": "desde el catálogo"},
  {"resaltar": ":nth-match(.hero-stock, 1)", "durante_ms": 2500, "al_decir": "Arriba, el stock"},
  {"resaltar": ":nth-match(.hero-stock, 2)", "durante_ms": 2500, "al_decir": "el costo promedio"},
  {"resaltar": "mat-form-field:has(mat-label:has-text('Unidad de medida'))", "durante_ms": 3000, "al_decir": "La unidad de medida"},
  {"resaltar": "app-inline-product-prices mat-form-field:has(mat-label:has-text('Precio de venta'))", "durante_ms": 5000, "al_decir": "El precio de venta"},
  {"resaltar": f"{UP} tbody tr:nth-child(1)", "durante_ms": 9000, "al_decir": "en unidades y empaques"},
  {"resaltar": "button:has-text('Convertir unidad base')", "durante_ms": 5000, "al_decir": "se puede revertir"}]},
]
json.dump(g, open('guiones/productos-05-pesados-conversion.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok')
