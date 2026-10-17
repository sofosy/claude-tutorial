import json, copy
base = json.load(open('guiones/productos-03-compras-inventario.json', encoding='utf-8'))
g = {k: copy.deepcopy(v) for k, v in base.items() if k not in ('pasos', 'aprenderas', 'errores_comunes', '_comentario', 'titulo', 'descripcion', 'setup')}
g['titulo'] = "Productos · Parte 4: empaques en ventas y punto de venta"
g['descripcion'] = ("Cuarta parte de la serie de Productos de Germiva ERP: vender un mismo producto por paquete, por caja y por unidad. "
  "La factura propone el empaque marcado para la venta, calcula su precio (propio o base por factor) y resume las líneas por empaque; "
  "el punto de venta agrega la caja al escanear su código de barras y la unidad al tocar la tarjeta; "
  "y Existencias y el Kardex descuentan todo en unidades, con cada salida leída en su empaque.")
g['_comentario'] = ("Serie Productos v3, video 4. Estado C (restaurar.mjs C): Refresco con Caja ×24 (compra ★, precio propio 780, código 7460001000243) "
  "y Paquete ×6 (venta ★, sin precio propio → 6 × 35 = 210), 240 unidades en el Almacén Sur, lote LOT-EMB-0925. "
  "Factura: 2 paquetes (420) + 1 caja (780) = 1,200, «Guardar y Cobrar» cobra en efectivo sin preguntar. POS: escanear la caja (780) "
  "+ tarjeta = unidad (35 c/u) ×3 → 885; el paquete no tiene código de barras, así que en el POS no entra (por diseño: el empaque "
  "solo llega al ticket por su código). Cobro sin turno; se desmarca «Imprimir recibo» para que no salga el diálogo de impresión. "
  "Saldo final: 240 − 36 − 27 = 177 = 7 cajas y 9 unidades.")
g['setup'] = {"tipo": "shell", "cmd": "node seeds/productos/restaurar.mjs C"}
g['aprenderas'] = [
  "Facturar por paquete: el empaque marcado para la venta llega solo, con su precio",
  "Cambiar la línea a caja y ver su precio propio",
  "Vender en el punto de venta: la caja por su código de barras y la unidad tocando la tarjeta",
  "Leer las ventas en Existencias y en el Kardex: todo baja en unidades, cada salida con su empaque"]
g['errores_comunes'] = [
  "Escribir en la cantidad las unidades sueltas con la línea en caja: dos cajas son cuarenta y ocho unidades, no dos",
  "Esperar que el punto de venta ofrezca el paquete sin código de barras: la tarjeta siempre agrega la unidad",
  "Dejar el empaque sin precio propio cuando la caja lleva descuento: sin él, la caja vale el precio de la unidad por el factor"]
F = False
DLG = ".custom-alert-dialog-panel mat-dialog-container"
LIN1 = ":nth-match(.products-services-section .table-row, 1)"
LIN2 = ":nth-match(.products-services-section .table-row, 2)"
BUSCA_LINEA = "input[placeholder^='Escriba el código o el nombre']"
BUSCA_POS = "input[aria-label='Buscar producto']"
g['pasos'] = [
{"id": "01-factura-paquete", "capitulo": "Facturar por paquete", "rotulo": "Factura por paquete", "ruta": "Ventas › Facturas › Nueva",
 "texto_pantalla": "Factura · el paquete llega solo, a seis veces el precio de la unidad",
 "narracion": "En la parte anterior compramos diez cajas de refresco. Hoy las vendemos de tres formas: por paquete, por caja y por unidad. Desde el inicio pulso nueva factura, y recojo el panel para ver la línea completa. El cliente queda como consumidor final, que basta para este ejemplo. En las líneas busco el refresco escribiendo su nombre; la lista muestra que hay doscientas cuarenta disponibles, y lo agrego. Fíjate en la unidad: vino sola en paquete por seis, porque el paquete es el que tiene la estrella de venta. El total a pagar es doscientos diez pesos: el paquete no tiene precio propio, así que vale seis veces la unidad, treinta y cinco pesos con ITBIS. En cantidad escribo dos, dos paquetes, y el total sube a cuatrocientos veinte.",
 "acciones": [
  {"click": "button:has-text('Nueva factura')", "al_decir": "pulso nueva factura"},
  {"click": "button.panel-collapse", "al_decir": "recojo el panel"},
  {"resaltar": "mat-form-field:has(mat-label:has-text('Cliente'))", "durante_ms": 3500, "al_decir": "El cliente queda"},
  {"escribir": {"sel": BUSCA_LINEA, "texto": "Refresco"}, "al_decir": "busco el refresco"},
  {"resaltar": "mat-option:has-text('Refresco Caribe Cola lata')", "durante_ms": 3000, "cursor": F, "al_decir": "la lista muestra"},
  {"click": "mat-option:has-text('Refresco Caribe Cola lata')", "al_decir": "y lo agrego"},
  {"resaltar": f"{LIN1} app-line-unit-select", "durante_ms": 6000, "al_decir": "Fíjate en la unidad"},
  {"resaltar": ".cost-row--total", "durante_ms": 9000, "al_decir": "El total a pagar"},
  {"escribir": {"sel": f"{LIN1} input[formcontrolname='quantity']", "texto": "2"}, "al_decir": "En cantidad escribo dos"},
  {"presionar": {"tecla": "Tab"}, "al_decir": "dos paquetes"},
  {"resaltar": ".cost-row--total", "durante_ms": 3000, "al_decir": "el total sube"}]},
{"id": "02-factura-caja", "capitulo": "La caja con su precio propio", "rotulo": "Factura por caja", "ruta": "Ventas › Facturas › Nueva",
 "texto_pantalla": "Factura · la caja con su precio propio, y el cobro",
 "narracion": "Ahora el mismo cliente se lleva también una caja entera. Agrego otra línea con el refresco; otra vez llega en paquete. Abro el selector de unidad: ofrece unidad, caja y paquete, los tres empaques que se venden. Elijo caja por veinticuatro. Esta línea suma setecientos ochenta: la caja tiene precio propio, más barato que veinticuatro unidades sueltas, que serían ochocientos cuarenta. Debajo de las líneas, el resumen las cuenta por empaque: dos paquetes y una caja. El total a pagar es mil doscientos pesos. Pulso guardar y cobrar; la venta es de contado y en efectivo, así que el cobro se registra en el mismo paso. El aviso lo confirma, y acepto. La factura queda emitida y pagada, con sus dos líneas en paquete y en caja.",
 "acciones": [
  {"escribir": {"sel": BUSCA_LINEA, "texto": "Refresco"}, "al_decir": "Agrego otra línea"},
  {"click": "mat-option:has-text('Refresco Caribe Cola lata')", "al_decir": "otra vez llega"},
  {"click": f"{LIN2} app-line-unit-select mat-select", "al_decir": "Abro el selector"},
  {"resaltar": ".cdk-overlay-pane mat-option:has-text('Caja')", "durante_ms": 4000, "cursor": F, "al_decir": "ofrece unidad"},
  {"click": ".cdk-overlay-pane mat-option:has-text('Caja ×24')", "al_decir": "Elijo caja por veinticuatro"},
  {"resaltar": f"{LIN2} app-line-unit-select", "durante_ms": 9000, "al_decir": "Esta línea suma"},
  {"resaltar": ".gm-doc-linecount", "durante_ms": 4500, "al_decir": "Debajo de las líneas"},
  {"resaltar": ".cost-row--total", "durante_ms": 3000, "cursor": F, "al_decir": "El total a pagar"},
  {"click": "button:has-text('Guardar y Cobrar')", "al_decir": "Pulso guardar y cobrar"},
  {"resaltar": DLG, "durante_ms": 2500, "cursor": F, "al_decir": "El aviso lo confirma"},
  {"click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "y acepto"},
  {"resaltar": ".page-hero", "durante_ms": 4000, "cursor": F, "al_decir": "La factura queda emitida"}]},
{"id": "03-pos-caja-unidad", "capitulo": "Punto de venta: la caja por su código", "rotulo": "Punto de venta", "ruta": "Punto de venta",
 "texto_pantalla": "Punto de venta · la caja entra por su código de barras, la unidad tocando la tarjeta",
 "navegar": "/pos",
 "narracion": "Pasemos al punto de venta, la pantalla del mostrador. En el buscador escaneo el código de barras de la caja; aquí lo escribo y pulso Enter, como hace el lector. El ticket recibe una caja por veinticuatro, a setecientos ochenta: el código dice qué empaque es. Ahora busco el refresco por nombre. La tarjeta muestra lo que queda, doscientas cuatro unidades, y su precio por unidad. Al tocarla entra una unidad, a treinta y cinco cada una. Con el más subo a tres. El paquete no tiene código de barras, así que en el mostrador no entra; si lo quieres vender aquí, dale un código en la ficha del producto. Abajo, artículos resume el ticket por empaque: una caja y tres unidades.",
 "acciones": [
  {"escribir": {"sel": BUSCA_POS, "texto": "7460001000243"}, "al_decir": "escaneo el código"},
  {"presionar": {"tecla": "Enter"}, "al_decir": "pulso Enter"},
  {"resaltar": ".ps-line:has-text('Caja ×24')", "durante_ms": 6000, "al_decir": "El ticket recibe"},
  {"escribir": {"sel": BUSCA_POS, "texto": "Refresco"}, "al_decir": "Ahora busco el refresco"},
  {"resaltar": "button.ps-card:has-text('Refresco Caribe Cola lata')", "durante_ms": 5000, "al_decir": "La tarjeta muestra"},
  {"click": "button.ps-card:has-text('Refresco Caribe Cola lata')", "al_decir": "Al tocarla"},
  {"click": ".ps-line:has-text('c/u') button[aria-label='Agregar una unidad']", "al_decir": "Con el más"},
  {"click": ".ps-line:has-text('c/u') button[aria-label='Agregar una unidad']", "al_decir": "subo a tres"},
  {"resaltar": ".ps-line:has-text('c/u')", "durante_ms": 2000, "cursor": F, "al_decir": "El paquete no tiene"},
  {"resaltar": ".ps-summary__row:has-text('Artículos')", "durante_ms": 5000, "al_decir": "Abajo, artículos"}]},
{"id": "04-pos-cobrar", "capitulo": "Cobrar en el punto de venta", "rotulo": "Cobrar", "ruta": "Punto de venta › Cobrar",
 "texto_pantalla": "Punto de venta · cobro en efectivo con cambio",
 "narracion": "El total es ochocientos ochenta y cinco pesos. Pulso cobrar, y se abre la ventana de cobro. La forma de pago ya está en efectivo. El cliente me paga con mil, y lo marco con el botón rápido. A la derecha, el cambio a devolver: ciento quince pesos. En esta demostración no imprimo el recibo, así que desmarco esa casilla. Confirmo el cobro. La venta queda registrada con su factura y su comprobante, y pulso nueva venta. Fíjate en la tarjeta del refresco: ahora quedan ciento setenta y siete unidades.",
 "acciones": [
  {"resaltar": "button.ps-charge", "durante_ms": 3000, "al_decir": "El total es"},
  {"click": "button.ps-charge", "al_decir": "Pulso cobrar"},
  {"resaltar": ".pos-payment-panel", "durante_ms": 2000, "cursor": F, "al_decir": "se abre la ventana"},
  {"resaltar": "button.pd-method:has-text('Efectivo')", "durante_ms": 2500, "cursor": F, "al_decir": "La forma de pago"},
  {"click": "button.pd-key--quick:has-text('1,000')", "al_decir": "lo marco"},
  {"resaltar": ".cdk-overlay-pane :text('Cambio a devolver')", "durante_ms": 4000, "cursor": F, "al_decir": "el cambio a devolver"},
  {"click": "label:has-text('Imprimir recibo')", "al_decir": "desmarco esa casilla"},
  {"click": "button.pd-btn-confirm", "al_decir": "Confirmo el cobro"},
  {"resaltar": ".cdk-overlay-pane", "durante_ms": 4000, "cursor": F, "al_decir": "La venta queda registrada"},
  {"click": ".cdk-overlay-pane button:has-text('Nueva venta')", "al_decir": "pulso nueva venta"},
  {"resaltar": "button.ps-card:has-text('Refresco Caribe Cola lata')", "durante_ms": 5000, "al_decir": "Fíjate en la tarjeta"}]},
{"id": "05-existencias-kardex", "capitulo": "Las ventas en el kardex", "rotulo": "Existencias y kardex", "ruta": "Inventario › Existencias",
 "texto_pantalla": "Kardex · cada salida en su empaque, el saldo en unidades",
 "navegar": "/inventory/existencias",
 "narracion": "Veamos cómo quedó el inventario. En Existencias escribo refresco en el buscador y pulso filtrar. Disponible: ciento setenta y siete unidades, que son siete cajas por veinticuatro y nueve unidades sueltas. Abro el detalle con el ojo, y pulso ver su kardex. Cada venta dejó su salida, en el empaque en que se vendió. La factura sacó dos paquetes por seis, doce unidades, y una caja de veinticuatro. El punto de venta sacó otra caja y tres unidades. Todas salen del mismo lote y al mismo costo por unidad, veintidós pesos. El saldo final se lee igual que en Existencias. En la próxima parte vemos los productos pesados, la balanza y el cambio de unidad base.",
 "acciones": [
  {"escribir": {"sel": "mat-form-field:has(mat-label:text-is('Buscar')) input", "texto": "Refresco"}, "al_decir": "escribo refresco"},
  {"click": "button:has(mat-icon:text-is('filter_list'))", "al_decir": "pulso filtrar"},
  {"resaltar": "table tbody tr:has-text('Refresco') td:nth-child(2)", "durante_ms": 7000, "al_decir": "Disponible"},
  {"click": "table tbody tr:has-text('Refresco') button:has(mat-icon:text-is('visibility'))", "al_decir": "con el ojo"},
  {"click": ".gm-console-split__aside :text('Ver su kardex')", "al_decir": "pulso ver su kardex"},
  {"resaltar": "table thead th:nth-child(6)", "durante_ms": 4000, "al_decir": "Cada venta dejó"},
  {"resaltar": ":nth-match(table tbody tr:has-text('Salida'), 1) td:nth-child(6)", "durante_ms": 3500, "al_decir": "La factura sacó"},
  {"resaltar": ":nth-match(table tbody tr:has-text('Salida'), 2) td:nth-child(6)", "durante_ms": 3000, "al_decir": "y una caja"},
  {"resaltar": ":nth-match(table tbody tr:has-text('Salida'), 3) td:nth-child(6)", "durante_ms": 2500, "al_decir": "El punto de venta"},
  {"resaltar": ":nth-match(table tbody tr:has-text('Salida'), 4) td:nth-child(6)", "durante_ms": 2500, "al_decir": "y tres unidades"},
  {"resaltar": ":nth-match(table tbody tr:has-text('Salida'), 1) td:nth-child(8)", "durante_ms": 5000, "al_decir": "Todas salen"},
  {"resaltar": "table tbody tr:has-text('Saldo final') td:has-text('7 Cajas')", "durante_ms": 4000, "al_decir": "El saldo final"}]},
]
json.dump(g, open('guiones/productos-04-ventas-pos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok')
