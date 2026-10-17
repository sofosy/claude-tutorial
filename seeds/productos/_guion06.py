import json, copy
base = json.load(open('guiones/productos-05-pesados-conversion.json', encoding='utf-8'))
g = {k: copy.deepcopy(v) for k, v in base.items() if k not in ('pasos', 'aprenderas', 'errores_comunes', '_comentario', 'titulo', 'descripcion', 'setup')}
g['titulo'] = "Productos · Parte 6: variantes"
g['descripcion'] = ("Sexta parte de la serie de Productos de Germiva ERP: un producto con variantes. Una gaseosa que se vende en tres "
  "presentaciones y tres sabores: las opciones con el atajo para colmados, el recargo que sube el precio de las presentaciones "
  "grandes, la matriz de combinaciones, la ficha del producto padre, crear una combinación que faltaba, la ficha de una variante "
  "con su entrada de mercancía y la venta en el punto de venta eligiendo presentación y sabor.")
g['privacidad'] = copy.deepcopy(base['privacidad'])
for w in ('Gaseosa', 'Brisa'):
    if w not in g['privacidad']['permitidos']:
        g['privacidad']['permitidos'].append(w)
g['_comentario'] = ("Serie Productos v3, video 6. Estado A (restaurar.mjs A). Se crea «Gaseosa Brisa» (nombre sin palabras de otros productos; "
  "«Uva» choca con otro producto, por eso los sabores son Naranja, Piña y Fresa). Precio RD$35 con ITBIS, costo 20. Presentación (atajo de colmado) "
  "sin Botella 12 oz; recargo Grande +25, Jumbo +50 → 35/60/85. Se desmarca Jumbo+Fresa (8 variantes) y luego se crea desde la celda «Crear» de la "
  "matriz con precio 85. Entrada de 24 latas de naranja a RD$20 a la variante. En el POS la tarjeta del padre abre el selector de presentación × sabor.")
g['setup'] = {"tipo": "shell", "cmd": "node seeds/productos/restaurar.mjs A"}
g['aprenderas'] = [
  "Activar variantes y definir sus opciones con los atajos o escribiéndolas",
  "Hacer que una opción cambie el precio con un recargo",
  "Elegir en la matriz qué combinaciones se crean",
  "Leer la ficha del padre: precios propios y heredados",
  "Crear después una combinación que faltaba",
  "Darle existencia a una variante y venderla en el punto de venta"]
g['errores_comunes'] = [
  "Crear todas las combinaciones aunque no se vendan: desmarca las que no tienes, se crean después",
  "Registrar la entrada en el padre: la mercancía entra siempre a una variante",
  "Escribir un precio en una variante sin querer: deja de seguir al padre; la flecha lo devuelve"]
F = False
DLG = ".custom-alert-dialog-panel mat-dialog-container"
OPT2 = ".vb-option >> nth=1"
g['pasos'] = [
{"id": "01-alta", "capitulo": "Un producto con variantes", "rotulo": "Nuevo producto", "ruta": "Inventario › Productos › Nuevo",
 "texto_pantalla": "Alta · los datos comunes y «Tiene variantes»",
 "navegar": "/inventory/product/list",
 "narracion": "En esta parte vemos las variantes: un mismo producto que se vende en varias presentaciones o sabores, cada uno con su código, su precio y su existencia. El ejemplo es una gaseosa en lata, grande y jumbo, de naranja, piña y fresa. Pulso nuevo producto. El nombre: Gaseosa Brisa, y el sistema confirma que está disponible. En categoría escribo alimentos, y la elijo de la lista. En unidad de medida escribo unidad, y también la elijo. El precio de venta, treinta y cinco pesos con el ITBIS incluido, y el costo, veinte. Estos datos son comunes a todas las variantes. Ahora, en características, enciendo tiene variantes.",
 "acciones": [
  {"click": "button:has-text('Nuevo Producto')", "al_decir": "Pulso nuevo producto"},
  {"escribir": {"sel": "input[formcontrolname='name']", "texto": "Gaseosa Brisa"}, "al_decir": "El nombre"},
  {"resaltar": ".name-notice--ok", "durante_ms": 2500, "al_decir": "está disponible"},
  {"escribir": {"sel": "mat-form-field:has(mat-label:has-text('Categoría')) input", "texto": "Alimen"}, "al_decir": "En categoría escribo"},
  {"click": "mat-option:has-text('Alimentos') >> nth=0", "al_decir": "la elijo de la lista"},
  {"escribir": {"sel": "mat-form-field:has(mat-label:has-text('Unidad de medida')) input", "texto": "Unidad"}, "al_decir": "En unidad de medida"},
  {"click": "mat-option:has-text('Unidad (UND)')", "al_decir": "también la elijo"},
  {"escribir": {"sel": "app-inline-product-prices mat-form-field:has(mat-label:has-text('Precio de venta')) input", "texto": "35"}, "al_decir": "treinta y cinco pesos"},
  {"click": "mat-checkbox:has-text('ITBIS incluido') input", "al_decir": "con el ITBIS incluido"},
  {"escribir": {"sel": "input[formcontrolname='purchasePrice']", "texto": "20"}, "al_decir": "el costo, veinte"},
  {"resaltar": ".gm-setting:has(button[aria-label='Tiene variantes'])", "durante_ms": 2500, "al_decir": "en características"},
  {"click": "button[aria-label='Tiene variantes']", "al_decir": "enciendo tiene variantes"}]},
{"id": "02-opciones", "capitulo": "Opciones y valores", "rotulo": "Opciones", "ruta": "Inventario › Productos › Nuevo",
 "texto_pantalla": "Opciones y variantes · presentación con el atajo, sabor escrito a mano",
 "narracion": "Aparece opciones y variantes. Una opción es lo que distingue a las variantes, como la presentación, y sus valores son las alternativas. Hay atajos con valores ya escritos; el de cerveza y refresco es el del colmado. Lo pulso, y trae lata, botella, grande y jumbo. La botella no la vendo: la quito con su equis. El sabor no está entre los atajos, así que pulso otra, y en el nombre de la opción escribo sabor. Ahora sus valores: escribo naranja y lo confirmo con Enter; luego piña, Enter; y fresa, Enter. Cada valor queda como una etiqueta, y el orden en que los escribes es el orden en que se ven al vender.",
 "acciones": [
  {"resaltar": ".vb-section .section-title", "durante_ms": 2500, "al_decir": "Aparece opciones"},
  {"resaltar": ".vb-lead >> nth=0", "durante_ms": 5000, "al_decir": "Una opción es"},
  {"resaltar": ".vb-presets", "durante_ms": 3000, "al_decir": "Hay atajos"},
  {"click": ".vb-presets button:has-text('Presentación (cerveza y refresco)')", "al_decir": "Lo pulso"},
  {"click": "button[aria-label='Quitar Botella 12 oz']", "al_decir": "la quito con su equis"},
  {"click": ".vb-presets button:has-text('Otra')", "al_decir": "pulso otra"},
  {"escribir": {"sel": f"{OPT2} >> input >> nth=0", "texto": "Sabor"}, "al_decir": "escribo sabor"},
  {"escribir": {"sel": f"{OPT2} >> .vb-values__input", "texto": "Naranja"}, "al_decir": "escribo naranja"},
  {"presionar": {"tecla": "Enter"}, "al_decir": "con Enter"},
  {"escribir": {"sel": f"{OPT2} >> .vb-values__input", "texto": "Piña"}, "al_decir": "luego piña"},
  {"presionar": {"tecla": "Enter"}, "al_decir": "piña, Enter"},
  {"escribir": {"sel": f"{OPT2} >> .vb-values__input", "texto": "Fresa"}, "al_decir": "y fresa"},
  {"presionar": {"tecla": "Enter"}, "al_decir": "fresa, Enter"},
  {"resaltar": f"{OPT2} >> .vb-values", "durante_ms": 5000, "al_decir": "Cada valor queda"}]},
{"id": "03-recargo-matriz", "capitulo": "El recargo y la matriz", "rotulo": "Recargo y matriz", "ruta": "Inventario › Productos › Nuevo",
 "texto_pantalla": "Recargo por presentación y las combinaciones que se van a crear",
 "narracion": "Ahora el sistema pregunta si alguna opción cambia el precio. La presentación sí: la grande y la jumbo cuestan más. Elijo presentación, y aparece un campo por cada valor. A la grande le sumo veinticinco pesos, y a la jumbo, cincuenta. Debajo está la matriz de variantes que se van a crear: presentaciones en filas, sabores en columnas, y en cada cruce el precio: treinta y cinco, sesenta y ochenta y cinco. La jumbo de fresa todavía no la vendo, así que la desmarco; se puede crear más adelante. El botón dice cuántas se van a crear: ocho. Pulso guardar producto. El sistema crea el padre y cada combinación como un producto hijo, y lo confirma; acepto.",
 "acciones": [
  {"resaltar": ".vb-surcharge__q", "durante_ms": 3000, "al_decir": "Ahora el sistema pregunta"},
  {"click": ".vb-surcharge button:has-text('Presentación')", "al_decir": "Elijo presentación"},
  {"escribir": {"sel": ".vb-surcharge__field:has(mat-label:text-is('Grande 22 oz')) input", "texto": "25"}, "al_decir": "A la grande"},
  {"escribir": {"sel": ".vb-surcharge__field:has(mat-label:text-is('Jumbo 1 L')) input", "texto": "50"}, "al_decir": "a la jumbo, cincuenta"},
  {"resaltar": ".vb-children__title", "durante_ms": 3500, "al_decir": "Debajo está la matriz"},
  {"resaltar": ".vb-matrix tbody", "durante_ms": 6000, "al_decir": "presentaciones en filas"},
  {"click": ".vb-matrix tbody tr >> nth=2 >> td >> nth=2 >> .mdc-checkbox", "al_decir": "la desmarco"},
  {"resaltar": "button:has-text('Guardar producto y')", "durante_ms": 3000, "al_decir": "El botón dice"},
  {"click": "button:has-text('Guardar producto y')", "al_decir": "Pulso guardar producto"},
  {"resaltar": DLG, "durante_ms": 2500, "cursor": F, "al_decir": "y lo confirma"},
  {"click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "acepto"}]},
{"id": "04-padre", "capitulo": "La ficha del padre", "rotulo": "Producto padre", "ruta": "Inventario › Productos › Gaseosa Brisa",
 "texto_pantalla": "Producto padre · las variantes con su código, precio y existencia",
 "narracion": "Se abre la ficha del producto padre, en la pestaña variantes. El padre es la plantilla: define lo común, pero no se vende ni guarda existencia. Por eso sus cifras resumen a los hijos: el precio va de treinta y cinco a ochenta y cinco, y ocho están a la venta. En la tabla, cada fila es una variante, con su propio código de barras que el sistema generó. Las latas dicen del padre: usan su precio, y si lo cambias en el padre, cambian con él. Las grandes y las jumbo tienen el suyo, y esta flecha lo devuelve al del padre. Paso a la vista matriz. La jumbo de fresa dice crear: la pulso, escribo su precio, ochenta y cinco, y pulso crear. El aviso de arriba confirma, y ya está la combinación que faltaba.",
 "acciones": [
  {"resaltar": ".gm-badge:text-is('Producto padre')", "durante_ms": 3000, "al_decir": "Se abre la ficha"},
  {"resaltar": ".hero-stock >> nth=1", "durante_ms": 3500, "al_decir": "el precio va"},
  {"resaltar": ".hero-stock >> nth=2", "durante_ms": 2500, "al_decir": "ocho están a la venta"},
  {"resaltar": ".vp-table tbody tr >> nth=0 >> td >> nth=2", "durante_ms": 4000, "al_decir": "cada fila es una variante"},
  {"resaltar": ".vp-inherited >> nth=0", "durante_ms": 5000, "al_decir": "Las latas dicen"},
  {"resaltar": ".vp-table tbody tr:has-text('Grande 22 oz + Naranja') td.vp-col-price", "durante_ms": 2500, "al_decir": "Las grandes"},
  {"resaltar": ".vp-table tbody tr:has-text('Grande 22 oz + Naranja') .vp-revert", "durante_ms": 3000, "al_decir": "esta flecha"},
  {"click": ".gm-seg button:has-text('Matriz')", "al_decir": "vista matriz"},
  {"click": ".vp-cell--new", "al_decir": "la pulso"},
  {"escribir": {"sel": ".vp-pop input.money-input__control", "texto": "85"}, "al_decir": "escribo su precio"},
  {"click": ".vp-pop button:has-text('Crear')", "al_decir": "y pulso crear"},
  {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2000, "cursor": F, "al_decir": "El aviso de arriba"},
  {"resaltar": ".vp-matrix tbody tr >> nth=2", "durante_ms": 3500, "al_decir": "ya está la combinación"}]},
{"id": "05-variante", "capitulo": "La ficha de una variante y su entrada", "rotulo": "Una variante", "ruta": "Inventario › Productos › Gaseosa Brisa › Lata 12 oz + Naranja",
 "texto_pantalla": "Variante · producto hijo con su código y su existencia",
 "narracion": "Vuelvo a la lista y abro una variante: la lata de naranja. Es un producto hijo: la barra de arriba lo dice, con el enlace al padre y sus hermanas, para saltar de una a otra. El nombre se arma solo y está bloqueado. A diferencia del padre, la variante sí recibe mercancía: pulso registrar entrada, y se abre su ventana. El motivo, compras de mercancía. El proveedor: escribo embotell, espero a que la lista lo encuentre, y elijo la Embotelladora del Caribe. La ubicación, el pasillo A del almacén Sur, y el lote lo genera el botón de al lado. Entran veinticuatro latas, a veinte pesos cada una. Registro la entrada, y acepto. Arriba, la variante ya tiene veinticuatro en existencia.",
 "acciones": [
  {"click": ".gm-seg button:has-text('Lista')", "al_decir": "Vuelvo a la lista"},
  {"click": "button[aria-label='Abrir Lata 12 oz + Naranja']", "al_decir": "abro una variante"},
  {"resaltar": ".child-bar__parent", "durante_ms": 3000, "al_decir": "Es un producto hijo"},
  {"resaltar": ".child-bar__siblings", "durante_ms": 3000, "al_decir": "sus hermanas"},
  {"resaltar": "mat-form-field:has([formcontrolname='name'])", "durante_ms": 3000, "al_decir": "El nombre se arma"},
  {"click": "button:has-text('Registrar Entrada')", "al_decir": "pulso registrar entrada"},
  {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": F, "al_decir": "se abre su ventana"},
  {"click": "mat-dialog-container mat-select[formcontrolname='inventoryMovementTypeId']", "al_decir": "El motivo"},
  {"click": "mat-option:has-text('Compras de mercancía')", "al_decir": "compras de mercancía"},
  {"escribir": {"sel": "mat-dialog-container [formcontrolname='partnerId'] input", "texto": "Embotell"}, "al_decir": "escribo embotell"},
  {"resaltar": "mat-option:has-text('Embotelladora del Caribe')", "durante_ms": 1500, "cursor": F, "al_decir": "la lista lo encuentre"},
  {"click": "mat-option:has-text('Embotelladora del Caribe')", "al_decir": "elijo la Embotelladora"},
  {"resaltar": "mat-dialog-container [formcontrolname='partnerId']", "durante_ms": 1500, "al_decir": "del Caribe"},
  {"click": "mat-dialog-container [formcontrolname='locationId'] input", "al_decir": "La ubicación"},
  {"click": "mat-option:has-text('Pasillo A - Estante 1')", "al_decir": "el pasillo A"},
  {"click": "mat-dialog-container button:has(mat-icon:text('auto_awesome'))", "al_decir": "lo genera el botón"},
  {"escribir": {"sel": "mat-dialog-container input[formcontrolname='quantity']", "texto": "24"}, "al_decir": "Entran veinticuatro"},
  {"escribir": {"sel": "mat-dialog-container input[formcontrolname='unitPrice']", "texto": "20"}, "al_decir": "a veinte pesos"},
  {"click": "mat-dialog-container button:has-text('Registrar entrada')", "al_decir": "Registro la entrada"},
  {"resaltar": DLG, "durante_ms": 1500, "cursor": F, "al_decir": "y acepto"},
  {"click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "Arriba, la variante"},
  {"resaltar": ".hero-stock >> nth=0", "durante_ms": 3500, "al_decir": "ya tiene veinticuatro"}]},
{"id": "06-pos", "capitulo": "Vender una variante", "rotulo": "Punto de venta", "ruta": "Punto de venta",
 "texto_pantalla": "Punto de venta · el padre abre el selector de presentación y sabor",
 "navegar": "/pos",
 "narracion": "Por último, la venta. En el punto de venta busco gaseosa. Aparece una sola tarjeta, la del padre, con sus nueve variantes y lo que hay en existencia. Al tocarla se abre el selector: presentaciones en filas y sabores en columnas. Solo la lata de naranja tiene existencia, veinticuatro; las demás dicen agotado. Sumo dos latas con el más. Abajo resume: dos unidades, setenta pesos. Pulso agregar, y el ticket recibe la línea con el nombre completo de la variante. Con lector de código de barras no hace falta el selector: escaneas la lata y entra directo. En la próxima parte vemos comercio exterior, insumos y listas de precios.",
 "acciones": [
  {"escribir": {"sel": "input[aria-label='Buscar producto']", "texto": "Gaseosa"}, "al_decir": "busco gaseosa"},
  {"resaltar": "button.ps-card:has-text('Gaseosa Brisa')", "durante_ms": 4500, "al_decir": "Aparece una sola tarjeta"},
  {"click": "button.ps-card:has-text('Gaseosa Brisa')", "al_decir": "Al tocarla"},
  {"resaltar": "mat-dialog-container", "durante_ms": 3500, "cursor": F, "al_decir": "se abre el selector"},
  {"click": "button[aria-label='Sumar una unidad de Lata 12 oz Naranja']", "al_decir": "Sumo dos latas"},
  {"click": "button[aria-label='Sumar una unidad de Lata 12 oz Naranja']", "al_decir": "con el más"},
  {"resaltar": "mat-dialog-container .mat-mdc-dialog-actions, mat-dialog-container :text('unidades en')", "durante_ms": 3500, "al_decir": "Abajo resume"},
  {"click": "mat-dialog-container button:has-text('Agregar')", "al_decir": "Pulso agregar"},
  {"resaltar": ".ps-line:has-text('Lata 12 oz + Naranja')", "durante_ms": 5000, "al_decir": "el ticket recibe"}]},
]
json.dump(g, open('guiones/productos-06-variantes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok')
