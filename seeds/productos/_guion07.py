import json, copy
base = json.load(open('guiones/productos-06-variantes.json', encoding='utf-8'))
g = {k: copy.deepcopy(v) for k, v in base.items() if k not in ('pasos', 'aprenderas', 'errores_comunes', '_comentario', 'titulo', 'descripcion', 'setup')}
g['titulo'] = "Productos · Parte 7: comercio exterior, insumos y listas de precios"
g['descripcion'] = ("Séptima y última parte de la serie de Productos de Germiva ERP: los datos de comercio exterior de un producto importado "
  "(partida arancelaria, país de origen, pesos y volumen), la receta de costo con insumos y merma para conocer el margen teórico, "
  "y una lista de precios calculada sobre otra, con descuento y redondeo, asignada a un cliente y aplicada en su factura.")
for w in ('Dulce', 'criollo', 'Colmados', 'Esquina', 'Estados Unidos', '2202.10.00'):
    if w not in g['privacidad']['permitidos']:
        g['privacidad']['permitidos'].append(w)
g['_comentario'] = ("Serie Productos v3, video 7. Estado A + insumos de cocina (seeds/productos/insumos.mjs: habichuela para cocinar, leche "
  "evaporada, azúcar crema, batata). Partida 2202.10.00 = gaseosas/refrescos con azúcar o aromatizados (SA); no se citan tasas. "
  "Producto nuevo «Dulce criollo casero» (nombre sin palabras de otros productos) RD$150 con ITBIS; receta 0.25 lb habichuela +10 % merma, "
  "0.25 lata de leche, 0.15 lb azúcar → costo 36.25, margen 90.87 (71.5 %). Lista «Colmados» = Precio regular −10 %, redondeo 5. "
  "Cliente Colmado La Esquina (id 8187 del canon). En la factura se busca «Esquina» (con «Colmado» salen personas reales del padrón). "
  "El refresco no tiene existencia en A (no se puede facturar): el ejemplo de la lista son las habichuelas, 85 → 75.")
g['setup'] = {"tipo": "shell", "cmd": "node seeds/productos/restaurar.mjs A && node seeds/productos/insumos.mjs"}
g['aprenderas'] = [
  "Registrar partida arancelaria, país de origen, pesos y volumen de un producto importado",
  "Armar la receta de un producto con insumos, cantidades y merma",
  "Leer el costo de insumos, el margen teórico y el costo porcentual",
  "Crear una lista de precios como porcentaje de otra, con redondeo",
  "Asignar la lista a un cliente y verla aplicada en su factura"]
g['errores_comunes'] = [
  "Confundir el peso neto con el bruto: el neto es solo el contenido, el bruto incluye el envase",
  "Olvidar la merma en la receta: el costo real sale más bajo de lo que es",
  "Crear la lista y no asignarla a ningún cliente: sin cliente, la factura usa la lista por defecto"]
F = False
DLG = ".custom-alert-dialog-panel mat-dialog-container"
SUP = "app-product-supplies"
LST = "app-price-list-catalog"
g['pasos'] = [
{"id": "01-exterior", "capitulo": "Comercio exterior", "rotulo": "Comercio exterior", "ruta": "Inventario › Productos › Refresco Caribe Cola lata",
 "texto_pantalla": "Ficha · partida arancelaria, país de origen, pesos y volumen",
 "navegar": "/inventory/product/list",
 "narracion": "Esta es la última parte de la serie de Productos. Empezamos con comercio exterior: los datos que pide la aduana cuando un producto se importa o se exporta. El refresco lo traemos de fuera. En el catálogo escribo refresco y abro su ficha. En características enciendo se importa o se exporta, y abajo aparece comercio exterior. La partida arancelaria es el código con que la aduana clasifica la mercancía en el Sistema Armonizado: los refrescos y gaseosas van en la veintidós cero dos punto diez. El país de origen: escribo estados, y elijo Estados Unidos. Luego los pesos de una lata en kilos: el bruto, con el envase, cero punto tres ocho cinco; el neto, solo el contenido, cero punto treinta y siete; y el volumen, en metros cúbicos. Guardo, y acepto.",
 "acciones": [
  {"resaltar": "table tbody", "durante_ms": 2000, "cursor": F, "al_decir": "Empezamos con comercio"},
  {"escribir": {"sel": "mat-form-field:has(mat-label:text-is('Buscar')) input", "texto": "Refresco"}, "al_decir": "escribo refresco"},
  {"click": "table tbody tr:has-text('Refresco Caribe Cola lata') button[aria-label='Abrir']", "al_decir": "abro su ficha"},
  {"click": "button[aria-label='Se importa o se exporta']", "al_decir": "enciendo se importa"},
  {"resaltar": "h3.section-title:has-text('Comercio exterior')", "durante_ms": 2500, "al_decir": "abajo aparece"},
  {"escribir": {"sel": "input[formcontrolname='tariffCode']", "texto": "2202.10.00"}, "al_decir": "La partida arancelaria"},
  {"resaltar": "mat-form-field:has(input[formcontrolname='tariffCode'])", "durante_ms": 4000, "al_decir": "van en la veintidós"},
  {"escribir": {"sel": "[formcontrolname='originCountry'] input", "texto": "Estados"}, "al_decir": "escribo estados"},
  {"resaltar": "mat-option:has-text('Estados Unidos (US)')", "durante_ms": 1200, "cursor": F, "al_decir": "y elijo"},
  {"click": "mat-option:has-text('Estados Unidos (US)')", "al_decir": "Estados Unidos. Luego"},
  {"escribir": {"sel": "input[formcontrolname='grossWeight']", "texto": "0.385"}, "al_decir": "el bruto"},
  {"escribir": {"sel": "input[formcontrolname='netWeight']", "texto": "0.37"}, "al_decir": "el neto"},
  {"escribir": {"sel": "input[formcontrolname='volume']", "texto": "0.0004"}, "al_decir": "y el volumen"},
  {"click": ".form-layout-footer button:has-text('Guardar')", "al_decir": "Guardo"},
  {"resaltar": DLG, "durante_ms": 1500, "cursor": F, "al_decir": "y acepto"},
  {"click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "acepto"}]},
{"id": "02-receta-alta", "capitulo": "Un producto con receta", "rotulo": "Producto con receta", "ruta": "Inventario › Productos › Nuevo",
 "texto_pantalla": "Alta · el dulce de la casa, para armar su receta",
 "navegar": "/inventory/product/list",
 "narracion": "Ahora los insumos. Sirven para conocer el costo real de lo que preparas: un plato, un combo o un dulce. Muchos colmados venden su habichuela con dulce; vamos a costearla. Pulso nuevo producto y lo llamo dulce criollo casero. En categoría escribo alimentos, y la elijo. En unidad de medida escribo unidad, y también la elijo. El precio: ciento cincuenta pesos el vaso, con el ITBIS incluido. Pulso guardar, y acepto. Las secciones que necesitan el producto ya creado se abren solas, entre ellas la pestaña insumos, que abro.",
 "acciones": [
  {"click": "button:has-text('Nuevo Producto')", "al_decir": "Pulso nuevo producto"},
  {"escribir": {"sel": "input[formcontrolname='name']", "texto": "Dulce criollo casero"}, "al_decir": "lo llamo"},
  {"escribir": {"sel": "mat-form-field:has(mat-label:has-text('Categoría')) input", "texto": "Alimen"}, "al_decir": "En categoría escribo"},
  {"click": "mat-option:has-text('Alimentos') >> nth=0", "al_decir": "y la elijo"},
  {"escribir": {"sel": "mat-form-field:has(mat-label:has-text('Unidad de medida')) input", "texto": "Unidad"}, "al_decir": "En unidad de medida"},
  {"click": "mat-option:has-text('Unidad (UND)')", "al_decir": "también la elijo"},
  {"escribir": {"sel": "app-inline-product-prices mat-form-field:has(mat-label:has-text('Precio de venta')) input", "texto": "150"}, "al_decir": "El precio"},
  {"click": "mat-checkbox:has-text('ITBIS incluido') input", "al_decir": "con el ITBIS incluido"},
  {"click": ".form-layout-footer button:has-text('Guardar')", "al_decir": "Pulso guardar"},
  {"resaltar": DLG, "durante_ms": 1500, "cursor": F, "al_decir": "y acepto"},
  {"click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "acepto. Las secciones"},
  {"click": "mat-tab-group.product-tabs .mdc-tab:has-text('Insumos')", "al_decir": "que abro"}]},
{"id": "03-receta", "capitulo": "Insumos, merma y margen", "rotulo": "Insumos", "ruta": "Inventario › Productos › Dulce criollo casero › Insumos",
 "texto_pantalla": "Insumos · lo que consume cada vaso, con su merma, y el margen teórico",
 "narracion": "Aquí va lo que consume cada vaso. En agregar insumo escribo habichuela, y elijo la habichuela roja para cocinar. Luego leche: la leche evaporada. Y azúcar: el azúcar crema. Arriba aparecen el costo de los insumos, el precio sin ITBIS, el margen teórico y el costo en porcentaje. Ahora mismo el margen sale en rojo: cada insumo entró con cantidad uno, como si un vaso llevara una libra de habichuelas. Ajusto las cantidades reales: un cuarto de libra de habichuela, con diez por ciento de merma, que es lo que se pierde al cocinar; un cuarto de lata de leche; y quince centésimas de libra de azúcar. Cada cambio se guarda solo. Ahora el vaso cuesta treinta y seis pesos con veinticinco en insumos, y el margen teórico es de noventa pesos, el setenta y uno por ciento del precio.",
 "acciones": [
  {"escribir": {"sel": f"{SUP} input >> nth=0", "texto": "Habichuela"}, "al_decir": "escribo habichuela"},
  {"resaltar": "mat-option:has-text('Habichuela roja para cocinar')", "durante_ms": 1200, "cursor": F, "al_decir": "y elijo"},
  {"click": "mat-option:has-text('Habichuela roja para cocinar')", "al_decir": "la habichuela roja"},
  {"escribir": {"sel": f"{SUP} input >> nth=0", "texto": "Leche"}, "al_decir": "Luego leche"},
  {"resaltar": "mat-option:has-text('Leche evaporada lata')", "durante_ms": 1000, "cursor": F, "al_decir": "la leche evaporada"},
  {"click": "mat-option:has-text('Leche evaporada lata')", "al_decir": "evaporada. Y"},
  {"escribir": {"sel": f"{SUP} input >> nth=0", "texto": "Azúcar"}, "al_decir": "Y azúcar"},
  {"resaltar": "mat-option:has-text('Azúcar crema')", "durante_ms": 1000, "cursor": F, "al_decir": "el azúcar crema"},
  {"click": "mat-option:has-text('Azúcar crema')", "al_decir": "crema. Arriba"},
  {"resaltar": f"{SUP} .gm-stat >> nth=0", "durante_ms": 2500, "al_decir": "el costo de los insumos"},
  {"resaltar": f"{SUP} .gm-stat:has-text('Margen teórico')", "durante_ms": 6000, "al_decir": "el margen sale en rojo"},
  {"escribir": {"sel": f"{SUP} tbody tr:has-text('Habichuela') input[aria-label='Cantidad por unidad producida']", "texto": "0.25"}, "al_decir": "un cuarto de libra"},
  {"escribir": {"sel": f"{SUP} tbody tr:has-text('Habichuela') input[aria-label='Porcentaje de merma']", "texto": "10"}, "al_decir": "diez por ciento de merma"},
  {"escribir": {"sel": f"{SUP} tbody tr:has-text('Leche') input[aria-label='Cantidad por unidad producida']", "texto": "0.25"}, "al_decir": "un cuarto de lata"},
  {"escribir": {"sel": f"{SUP} tbody tr:has-text('Azúcar') input[aria-label='Cantidad por unidad producida']", "texto": "0.15"}, "al_decir": "quince centésimas"},
  {"presionar": {"tecla": "Tab"}, "al_decir": "Cada cambio se guarda"},
  {"resaltar": f"{SUP} .gm-stat >> nth=0", "durante_ms": 3500, "al_decir": "Ahora el vaso cuesta"},
  {"resaltar": f"{SUP} .gm-stat:has-text('Margen teórico')", "durante_ms": 4500, "al_decir": "y el margen teórico"}]},
{"id": "04-lista", "capitulo": "Una lista de precios calculada", "rotulo": "Lista de precios", "ruta": "Inventario › Configuración › Listas de precios",
 "texto_pantalla": "Listas de precios · Colmados = Precio regular menos diez por ciento, redondeado",
 "navegar": "/inventory/config",
 "narracion": "Por último, las listas de precios: los precios distintos para distintos clientes. Se definen en Inventario, configuración, al final de la página. Hoy hay tres: el precio regular, que es la lista por defecto, la mayorista y la VIP, las tres de precio fijo. Vamos a crear una para los colmados que nos compran para revender, sin tener que escribir un precio por producto. Pulso nueva lista. En tipo elijo porcentaje sobre otra lista. La lista base, el precio regular. El porcentaje, menos diez: diez por ciento menos. Y redondeo a múltiplos de cinco pesos, para que los precios queden redondos. El nombre: colmados, con su descripción. Guardo, y la lista aparece con su cálculo.",
 "acciones": [
  {"resaltar": f"{LST}", "durante_ms": 3500, "al_decir": "Se definen en Inventario"},
  {"resaltar": f"{LST} table tbody", "durante_ms": 5000, "al_decir": "Hoy hay tres"},
  {"click": f"{LST} button:has-text('Nueva lista')", "al_decir": "Pulso nueva lista"},
  {"click": "mat-dialog-container mat-select[formcontrolname='type']", "al_decir": "En tipo"},
  {"click": "mat-option:has-text('% sobre otra lista')", "al_decir": "porcentaje sobre otra lista"},
  {"click": "mat-dialog-container mat-select[formcontrolname='basePriceListId']", "al_decir": "La lista base"},
  {"click": "mat-option:has-text('Precio regular')", "al_decir": "el precio regular"},
  {"escribir": {"sel": "mat-dialog-container app-money-input[formcontrolname='percent'] input", "texto": "-10"}, "al_decir": "El porcentaje"},
  {"escribir": {"sel": "mat-dialog-container app-money-input[formcontrolname='roundingStep'] input", "texto": "5"}, "al_decir": "Y redondeo"},
  {"escribir": {"sel": "mat-dialog-container input[formcontrolname='name']", "texto": "Colmados"}, "al_decir": "El nombre"},
  {"escribir": {"sel": "mat-dialog-container input[formcontrolname='description']", "texto": "Colmados que compran para revender"}, "al_decir": "con su descripción"},
  {"click": "mat-dialog-container button:has-text('Guardar')", "al_decir": "Guardo"},
  {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 1500, "cursor": F, "al_decir": "y la lista aparece"},
  {"resaltar": f"{LST} table tbody tr:has-text('Colmados')", "durante_ms": 4000, "al_decir": "con su cálculo"}]},
{"id": "05-cliente", "capitulo": "La lista en el cliente", "rotulo": "Lista del cliente", "ruta": "Ventas › Clientes › Colmado La Esquina",
 "texto_pantalla": "Cliente · la lista de precios que se aplica en sus documentos",
 "navegar": "/sales/partners/edit/8187",
 "narracion": "La lista se le asigna a cada cliente, en su ficha. Este es el Colmado La Esquina. En lista de precios escribo colm, y elijo colmados. Debajo, la pista lo explica: son los precios que se aplican en sus documentos, y si queda vacía, usa la lista por defecto. Guardo el cliente, y acepto.",
 "acciones": [
  {"resaltar": "app-autocomplete:has-text('Lista de precios')", "durante_ms": 3000, "al_decir": "La lista se le asigna"},
  {"escribir": {"sel": "app-autocomplete:has-text('Lista de precios') input", "texto": "Colm"}, "al_decir": "escribo colm"},
  {"resaltar": "mat-option:has-text('Colmados')", "durante_ms": 1000, "cursor": F, "al_decir": "y elijo"},
  {"click": "mat-option:has-text('Colmados')", "al_decir": "elijo colmados"},
  {"resaltar": "app-autocomplete:has-text('Lista de precios')", "durante_ms": 5000, "al_decir": "Debajo, la pista"},
  {"click": ".footer-right button:has-text('Guardar')", "al_decir": "Guardo el cliente"},
  {"resaltar": DLG, "durante_ms": 1500, "cursor": F, "al_decir": "y acepto"},
  {"click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "acepto"}]},
{"id": "06-factura", "capitulo": "El precio de la lista en la factura", "rotulo": "Factura con lista", "ruta": "Ventas › Facturas › Nueva",
 "texto_pantalla": "Factura · el cliente con lista Colmados paga 75 en vez de 85",
 "navegar": "/sales/invoices/create",
 "narracion": "Ahora una factura nueva para él. Quito el consumidor final, y en cliente escribo esquina y lo elijo. Agrego las habichuelas: su precio regular es ochenta y cinco, pero para este cliente la factura propone setenta y cinco: ochenta y cinco menos diez por ciento, redondeado a cinco pesos. Si el regular cambia, el de los colmados cambia con él. Así termina la serie de Productos: la ficha, los empaques, las compras y las ventas en cajas, los pesados, las variantes, y hoy, comercio exterior, insumos y listas de precios.",
 "acciones": [
  {"click": "mat-form-field:has(mat-label:text-is('Cliente')) button:has-text('close')", "al_decir": "Quito el consumidor final"},
  {"escribir": {"sel": "input[placeholder='Busque por nombre o RNC/Cédula']", "texto": "Esquina"}, "al_decir": "en cliente escribo"},
  {"resaltar": "mat-option:has-text('Colmado La Esquina')", "durante_ms": 1000, "cursor": F, "al_decir": "esquina y"},
  {"click": "mat-option:has-text('Colmado La Esquina')", "al_decir": "lo elijo"},
  {"escribir": {"sel": "input[placeholder^='Escriba el código o el nombre']", "texto": "Habichuelas"}, "al_decir": "Agrego las habichuelas"},
  {"click": "mat-option:has-text('Habichuelas rojas')", "al_decir": "su precio regular"},
  {"resaltar": ":nth-match(.products-services-section .table-row, 1) .table-cell:has-text('RD$75')", "durante_ms": 8000, "al_decir": "la factura propone"},
  {"resaltar": "mat-form-field:has(mat-label:text-is('Cliente'))", "durante_ms": 4000, "al_decir": "Si el regular cambia"},
  {"resaltar": ".products-services-section", "durante_ms": 6000, "cursor": F, "al_decir": "Así termina la serie"}]},
]
json.dump(g, open('guiones/productos-07-exterior-insumos-listas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok')
