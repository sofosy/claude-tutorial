"""Genera los guiones CORTOS de la serie Productos (guiones/productos-NN-*.json), nov. 2026.
    python3 seeds/productos/_guiones.py
Editar aquí y regenerar. Las partes «empaques» y «compras» (04 y 05) conservan su guion largo propio."""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "seeds" / "fabricacion"))
from _guiones import COMUN as BASE, campo, clic, marca, teclea  # noqa: E402

COMUN = {**BASE,
         "pronunciacion": {"ITBIS": "itebís", "DGII": "de ge i i", "RNC": "erre ene ce", "POS": "pos"},
         "privacidad": {"perfil": "ninguno",
                        "permitidos": ["germiva", "130555", "Embotelladora", "Agroindustrial", "Cibao", "Galletera", "Colmado", "Esquina"],
                        "mapa_fijo": {"localhost:3001": "api.germiva.com", "localhost:4200": "germiva.com"}}}
LISTA = {**COMUN["sesion"], "navegar": "/inventory/product/list", "esperar": "button:has-text('Nuevo Producto')"}
SNACK = ".mat-mdc-snack-bar-container"
DIALOGO = "mat-dialog-container"
ALERTA = ".custom-alert-dialog-panel mat-dialog-container"
def fila(nombre, col): return f"table tbody tr:has-text('{nombre}') td:nth-child({col})"
def filtro(etiqueta): return f"mat-form-field:has(mat-label:text-is('{etiqueta}'))"
def cartel(titulo, texto, decir, ms=6000): return {"cartel": {"tipo": "consejo", "titulo": titulo, "texto": texto}, "durante_ms": ms, "al_decir": decir}
def tecla(t, decir): return {"presionar": {"tecla": t}, "al_decir": decir}
RESTAURAR = lambda e: {"tipo": "shell", "cmd": f"node seeds/productos/restaurar.mjs {e}"}

VIDEOS = {}

# ───────────────────────── 01 · El catálogo ─────────────────────────
VIDEOS["productos-01-catalogo"] = {
    "titulo": "Productos · Parte 1: el catálogo",
    "descripcion": "Primer video de Productos en Germiva ERP: la pantalla donde vive todo lo que tu empresa compra o vende. Cómo leer cada columna, encontrar un producto en segundos, y qué hacen duplicar, desactivar y eliminar.",
    "_comentario": "Serie Productos corta (nov. 2026), video 1. Estado A (restaurar.mjs A): Tienda Germiva con Refresco Caribe Cola lata (agotado), Galletas soda Crocante (20 cajas), Habichuelas rojas (250 lb) y los productos y servicios sembrados (p. ej. «Barbería y Peluquería»). No crea ni cambia nada: los tres diálogos se cancelan.",
    "sesion": LISTA, "setup": RESTAURAR("A"),
    "aprenderas": ["Leer el catálogo: producto, código, precio, stock y estado", "Buscar por nombre o código y filtrar por tipo", "Elegir las columnas, importar desde Excel y el alta por foto", "Cuándo duplicar, desactivar o eliminar un producto"],
    "errores_comunes": ["Eliminar un producto que ya tuvo movimientos: lo correcto es desactivarlo", "Crear dos veces el mismo producto por no buscarlo antes", "Buscar la existencia de un servicio: un servicio no se almacena"],
    "pasos": [
        {
            "id": "01-columnas", "capitulo": "Leer el catálogo", "rotulo": "El catálogo",
            "ruta": "Inventario › Productos",
            "narracion": "Este es el catálogo de Productos: todo lo que tu empresa compra o vende, mercancía y servicios, y cada fila es uno. Para ganar espacio, recojo el panel. En la primera columna va el nombre. Después el código, que puede ser el de barras. El precio de venta es el de tu lista principal. El stock dice cuánto hay: este refresco está agotado, y un servicio dice no aplica, porque no se almacena. Y al final de la fila están las acciones, que vemos en un momento.",
            "acciones": [
                marca(fila("Habichuelas rojas", 2), "cada fila es uno", 2500),
                clic("button.panel-collapse", "recojo el panel"),
                marca("table thead th:nth-child(2)", "va el nombre", 1200),
                marca(fila("Habichuelas rojas", 3), "Después el código", 3000),
                marca(fila("Habichuelas rojas", 4), "El precio de venta", 3000),
                marca(fila("Habichuelas rojas", 5), "El stock dice", 2000),
                marca(fila("Refresco Caribe Cola lata", 5), "está agotado", 1700),
                marca(fila("Barbería y Peluquería", 5), "dice no aplica", 3500),
                marca(fila("Habichuelas rojas", 7), "están las acciones", 3500),
            ],
        },
        {
            "id": "02-buscar", "capitulo": "Buscar y filtrar", "rotulo": "Buscar y filtrar",
            "ruta": "Inventario › Productos",
            "narracion": "Para encontrar algo rápido, en el campo Buscar escribo parte del nombre o del código. La tabla se filtra sola mientras escribo, sin pulsar nada. Con la equis limpio la búsqueda. El filtro Tipo separa los productos de los servicios: lo abro y elijo Servicio, y quedan solo los servicios, como esta barbería. Para ver todo de nuevo, vuelvo a limpiar. Un consejo: busca siempre antes de crear, para no tener el mismo producto dos veces.",
            "acciones": [
                teclea(filtro("Buscar") + " input", "Refresco", "escribo parte del nombre"),
                marca(fila("Refresco Caribe Cola lata", 2), "se filtra sola", 3000),
                clic("app-dynamic-filters button:has(mat-icon:text-is('clear'))", "Con la equis"),
                clic(filtro("Tipo") + " mat-select", "lo abro"),
                clic("mat-option:has-text('Servicio'):not(:has-text('Productos'))", "elijo Servicio"),
                marca(fila("Barbería y Peluquería", 2), "solo los servicios", 2500),
                clic("app-dynamic-filters button:has(mat-icon:text-is('clear'))", "vuelvo a limpiar"),
                cartel("Consejo", "Busca antes de crear: evita tener el mismo producto dos veces.", "Un consejo", 6000),
            ],
        },
        {
            "id": "03-herramientas", "capitulo": "Columnas, importar y alta por foto", "rotulo": "Herramientas",
            "ruta": "Inventario › Productos",
            "narracion": "Arriba de la tabla hay tres herramientas. El botón de columnas decide qué columnas ves: puedes sumar la marca, la unidad o la categoría. Lo cierro. Importar y exportar carga muchos productos de una vez desde un archivo, y te deja bajar el catálogo completo. Cierro el diálogo. Y alta por foto: subes fotos de tus productos y el sistema prepara las fichas para que tú las revises.",
            "acciones": [
                clic("button:has(mat-icon:text-is('view_column'))", "El botón de columnas"),
                marca(".column-config-menu", "puedes sumar la marca", 3500, cursor=False),
                tecla("Escape", "Lo cierro"),
                clic("button:has-text('Importar / Exportar')", "Importar y exportar"),
                marca(DIALOGO, "desde un archivo", 4500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Cerrar'), {DIALOGO} button[aria-label='Cerrar'], {DIALOGO} button:has(mat-icon:text-is('close'))", "Cierro el diálogo"),
                marca("button:has-text('Alta por foto')", "alta por foto", 6000),
            ],
        },
        {
            "id": "04-acciones", "capitulo": "Duplicar, desactivar y eliminar", "rotulo": "Acciones de la fila",
            "ruta": "Inventario › Productos",
            "narracion": "Ahora las acciones de cada fila, con las galletas. El lápiz abre la ficha. Duplicar crea una copia con toda su configuración, útil para productos casi iguales. Cancelo. La segunda acción es desactivar: el producto se oculta al vender y al comprar, pero conserva su historial: es lo correcto para un producto que ya tuvo movimientos. Cancelo otra vez. Y eliminar lo borra sin vuelta atrás: úsalo solo con algo creado por error. También lo cancelo. En el siguiente video creamos un producto desde cero.",
            "acciones": [
                marca("table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Abrir']", "El lápiz abre", 2000),
                clic("table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Duplicar']", "Duplicar crea"),
                marca(DIALOGO, "toda su configuración", 3500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Cancelar')", "Cancelo. La segunda"),
                clic("table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Desactivar']", "se oculta"),
                marca(DIALOGO, "conserva su historial", 5500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Cancelar')", "Cancelo otra vez"),
                clic("table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Eliminar']", "eliminar lo borra"),
                marca(DIALOGO, "sin vuelta atrás", 4500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Cancelar')", "También lo cancelo"),
            ],
        },
    ],
}

# ───────────────────────── 02 · Crear un producto ─────────────────────────
PRECIOS = "app-inline-product-prices"
def ctl(nombre): return f"input[formcontrolname='{nombre}']"
def ajuste(etiqueta): return f".gm-setting:has(button[aria-label='{etiqueta}'])"
GUARDAR = ".form-layout-footer button:has-text('Guardar')"
VIDEOS["productos-02-crear-producto"] = {
    "titulo": "Productos · Parte 2: crear un producto",
    "descripcion": "Segundo video de Productos en Germiva ERP: dar de alta un producto en una sola hoja. Nombre, categoría y unidad; el precio con ITBIS incluido; la cantidad inicial con su costo y su lote; el mínimo y el máximo; y lo que aparece al guardar: el código de barras y la etiqueta.",
    "_comentario": "Serie Productos corta (nov. 2026), video 2. Estado A. Crea «Chocolate tradicional Cacao Real»: Alimentos, marca Cacao Real, Unidad; RD$165 con ITBIS incluido (neto 139.83); cantidad inicial 24 a costo 95, lote LOT-1101; mínimo 24, máximo 120. La cantidad inicial sustituye a la «primera entrada» del video anterior a nov. 2026: pide costo, y lote si el producto controla lote (viene encendido).",
    "sesion": LISTA, "setup": RESTAURAR("A"),
    "aprenderas": ["Llenar la ficha de un producto de arriba abajo", "Poner el precio con el ITBIS incluido", "Cargar la cantidad inicial con su costo y su lote", "Definir el stock mínimo y máximo", "Qué gana la ficha al guardar: código de barras y etiqueta"],
    "errores_comunes": ["Escribir el precio con ITBIS sin encender «ITBIS incluido»: la factura lo cobra dos veces", "Poner la cantidad inicial sin su costo: el inventario quedaría sin valor", "Cambiar después la unidad de medida a mano: para eso existe «Convertir unidad base»"],
    "pasos": [
        {
            "id": "01-identificacion", "capitulo": "Nombre, categoría y unidad", "rotulo": "Nuevo producto",
            "ruta": "Inventario › Productos › Nuevo",
            "narracion": "Vamos a crear un producto desde cero. Pulso Nuevo Producto. La ficha es una sola hoja que se llena de arriba abajo, y al pie una barra dice qué falta para guardar. Empiezo por el nombre: Chocolate tradicional Cacao Real. Mientras escribo, el sistema revisa que no exista otro igual, y aquí confirma que está disponible. Sigue la categoría, que agrupa productos parecidos. En categoría escribo las primeras letras de alimentos; aparece debajo, entre las que ya existen, y la tomo de la lista. Sigue la unidad de medida, que es la unidad en que se lleva la existencia y el costo: escribo unidad en el campo, espero a que aparezcan las opciones, y de ellas elijo la primera.",
            "acciones": [
                clic("button:has-text('Nuevo Producto')", "Pulso Nuevo Producto"),
                marca(".gm-doc-blocking", "una barra dice", 3000),
                teclea(ctl("name"), "Chocolate tradicional Cacao Real", "Empiezo por el nombre"),
                marca(".name-notice--ok", "está disponible", 2500),
                teclea(campo("Categoría"), "Alimen", "En categoría escribo"),
                clic("mat-option:has-text('Alimentos') >> nth=0", "la tomo de la lista"),
                teclea(campo("Unidad de medida"), "Unidad", "escribo unidad"),
                clic("mat-option:has-text('Unidad (UND)')", "elijo la primera"),
            ],
        },
        {
            "id": "02-precio-existencia", "capitulo": "Precio y cantidad inicial", "rotulo": "Precio y existencia",
            "ruta": "Inventario › Productos › Nuevo",
            "narracion": "Ahora, el precio de venta. En la fila de la lista Precio regular, en monto, escribo ciento sesenta y cinco pesos. Ese precio ya trae adentro el ITBIS, el impuesto sobre la venta, así que enciendo ITBIS incluido, y el total queda en ciento sesenta y cinco: si no lo enciendes, la factura le suma el impuesto encima. Debajo está la cantidad inicial, por si ya tienes mercancía: escribo veinticuatro. Al poner una cantidad, el sistema pide con qué costo entra: noventa y cinco pesos cada uno. Y como el producto controla lote, pide el lote inicial; lo escribo tal como viene en la caja.",
            "acciones": [
                marca(f"{PRECIOS} table tbody tr:first-child td:nth-child(2)", "la lista Precio regular", 2500),
                teclea(f"{PRECIOS} input[type='number']", "165", "escribo ciento sesenta y cinco"),
                clic(f"{PRECIOS} button[aria-label='ITBIS incluido']", "enciendo ITBIS incluido"),
                marca(f"{PRECIOS} table tbody tr:first-child td.col-total, {PRECIOS} table tbody tr:first-child td:nth-child(7)", "el total queda", 6000),
                teclea(ctl("initialQuantity"), "24", "escribo veinticuatro"),
                teclea(ctl("purchasePrice"), "95", "con qué costo entra"),
                teclea(ctl("initialBatchNumber"), "LOT-1101", "pide el lote inicial"),
            ],
        },
        {
            "id": "03-minimo-guardar", "capitulo": "Mínimo, máximo y guardar", "rotulo": "Guardar",
            "ruta": "Inventario › Productos › Nuevo",
            "narracion": "Más abajo, en características, maneja inventario viene encendido: el sistema lleva sus existencias y su costo. En la pestaña Inventario pongo el stock mínimo, veinticuatro: cuando la existencia baje de ahí, el sistema avisa y lo propone en Por reponer. Y el stock máximo, que es hasta dónde reponer: ciento veinte. Con eso es suficiente, así que pulso Guardar. El aviso confirma que el producto se creó, y acepto.",
            "acciones": [
                marca(ajuste("Maneja inventario"), "maneja inventario viene", 4500),
                teclea(ctl("minStock"), "24", "pongo el stock mínimo"),
                teclea(ctl("maxStock"), "120", "el stock máximo"),
                clic(GUARDAR, "pulso Guardar"),
                marca(ALERTA, "El aviso confirma", 2500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "y acepto"),
            ],
        },
        {
            "id": "04-ficha-guardada", "capitulo": "La ficha guardada", "rotulo": "Al guardar",
            "ruta": "Inventario › Productos › Chocolate tradicional Cacao Real",
            "narracion": "La ficha queda abierta y gana partes nuevas. Arriba, junto al nombre, su código y el estado activo. A la derecha, el código de barras que el sistema generó solo, con su candado para que nadie lo cambie por error, y el botón para imprimir la etiqueta. Y abajo aparecen pestañas nuevas, como variantes, insumos e historial. El chocolate ya se puede vender, con veinticuatro unidades en existencia. En el próximo video: los servicios, la parte fiscal y la tienda.",
            "acciones": [
                marca(".page-hero", "su código y el estado", 2800),
                marca(".barcode-section", "el código de barras", 2800),
                marca("button[aria-label='Desbloquear código']", "con su candado", 3000),
                marca("button:has-text('Imprimir etiqueta')", "imprimir la etiqueta", 1800),
                marca("mat-tab-group.product-tabs .mat-mdc-tab-labels", "pestañas nuevas", 2700),
                marca(".page-hero", "ya se puede vender", 4000),
            ],
        },
    ],
}

# ───────────────────────── 03 · Servicios, fiscal y tienda ─────────────────────────
def pestana(nombre): return f"mat-tab-group.product-tabs [role=tab]:has-text('{nombre}')"
VIDEOS["productos-03-servicio-fiscal-tienda"] = {
    "titulo": "Productos · Parte 3: servicios, fiscal y tienda en línea",
    "descripcion": "Tercer video de Productos en Germiva ERP: dar de alta un servicio, que se vende pero no se almacena; la pestaña Fiscal, con la cuenta de ingreso y los impuestos adicionales de la DGII; y cómo publicar un producto o servicio en tu tienda en línea.",
    "_comentario": "Serie Productos corta (nov. 2026), video 3. Estado A. Crea el servicio «Fumigación doméstica» (Servicios de Limpieza, Unidad, RD$2,500 sin ITBIS incluido; al pasar a Servicio el ITBIS queda en Exento y en cámara se elige el 18 % → total 2,950) y lo publica en la tienda. En Fiscal solo se señalan la cuenta de ingreso y los impuestos adicionales (no se agrega ninguno).",
    "sesion": LISTA, "setup": RESTAURAR("A"),
    "aprenderas": ["Crear un servicio y en qué se diferencia de un producto", "Para qué sirve la cuenta contable de ingreso", "Dónde van la propina legal y otros impuestos adicionales", "Publicar un producto o servicio en la tienda en línea"],
    "errores_comunes": ["Dejar el ITBIS en exento en un servicio que sí lo lleva: al cambiar a Servicio viene en exento", "Agregar un impuesto adicional que el producto no lleva", "Dejar «Visible en la tienda» encendido en algo que no quieres mostrar al público"],
    "pasos": [
        {
            "id": "01-servicio", "capitulo": "Crear un servicio", "rotulo": "Un servicio",
            "ruta": "Inventario › Productos › Nuevo",
            "narracion": "No todo lo que vendes se guarda en un almacén. Hoy creamos un servicio. Pulso Nuevo Producto. Se abre la ficha en blanco y, arriba a la derecha, cambio el tipo a servicio. Fíjate en lo que desaparece: la cantidad inicial, las características y el código de barras, porque un servicio no se almacena ni se cuenta. Lo llamo Fumigación doméstica, que es el nombre que verá el cliente en la factura. En categoría escribo servicios de limp, y de la lista que aparece tomo servicios de limpieza. En unidad de medida escribo unidad, porque se cobra por cada visita, y la selecciono cuando aparece. El precio, en monto: dos mil quinientos pesos por cada visita. Ojo con el ITBIS, el impuesto sobre la venta: en un servicio viene en exento. Este sí lo lleva, así que abro la lista y elijo la tasa del dieciocho por ciento. Dejo apagado ITBIS incluido, y mira el total: dos mil novecientos cincuenta, porque la factura le suma el impuesto encima. Pulso Guardar. Aparece un aviso que confirma que el servicio se creó, y lo cierro con aceptar.",
            "acciones": [
                clic("button:has-text('Nuevo Producto')", "Pulso Nuevo Producto"),
                clic("mat-button-toggle:has-text('Servicio') button", "cambio el tipo"),
                marca("mat-tab-group.product-tabs .mat-mdc-tab-labels", "lo que desaparece", 5000),
                teclea(ctl("name"), "Fumigación doméstica", "Lo llamo"),
                teclea(campo("Categoría"), "Servicios de limp", "En categoría escribo"),
                clic("mat-option:has-text('Servicios de Limpieza')", "tomo servicios de limpieza"),
                teclea(campo("Unidad de medida"), "Unidad", "escribo unidad"),
                clic("mat-option:has-text('Unidad (UND)')", "la selecciono"),
                teclea(f"{PRECIOS} input[type='number']", "2500", "dos mil quinientos"),
                marca(f"{PRECIOS} mat-select[aria-label='ITBIS del precio'] >> nth=0", "viene en exento", 2500),
                clic(f"{PRECIOS} mat-select[aria-label='ITBIS del precio'] >> nth=0", "abro la lista"),
                clic("mat-option:has-text('18.00')", "elijo la tasa"),
                marca(f"{PRECIOS} button[aria-label='ITBIS incluido']", "Dejo apagado", 2500),
                marca(f"{PRECIOS} table tbody tr:first-child td:nth-child(7)", "mira el total", 5500),
                clic(GUARDAR, "Pulso Guardar"),
                marca(ALERTA, "Aparece un aviso", 3000, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "con aceptar"),
            ],
        },
        {
            "id": "02-fiscal", "capitulo": "La pestaña Fiscal", "rotulo": "Fiscal",
            "ruta": "Inventario › Productos › Fumigación doméstica",
            "narracion": "Con la ficha guardada, abro la pestaña Fiscal, que sirve igual para productos y servicios. La cuenta contable de ingreso dice a dónde van las ventas de este servicio; si la dejas vacía, se usa la de la empresa. Así puedes separar en tu contabilidad los servicios de la mercancía. Debajo están los impuestos adicionales de la DGII, la Dirección General de Impuestos Internos: aquí se agregan la propina legal o los impuestos selectivos, solo si el producto los lleva. Este servicio no lleva ninguno.",
            "acciones": [
                clic(pestana("Fiscal"), "abro la pestaña Fiscal"),
                marca("app-account-picker[formcontrolname='incomeAccount']", "La cuenta contable de ingreso", 8000),
                marca("app-product-tax-mappings", "los impuestos adicionales", 9000),
            ],
        },
        {
            "id": "03-tienda", "capitulo": "Publicar en la tienda en línea", "rotulo": "Tienda en línea",
            "ruta": "Inventario › Productos › Fumigación doméstica",
            "narracion": "La última pestaña es descripción y tienda. La descripción es lo que lee el cliente en tu catálogo en línea, y admite negritas y listas. Abajo, enciendo visible en la tienda, y el servicio queda publicado. Indexable en buscadores deja que Google lo muestre; apágalo si solo vas a compartir el enlace. Guardo los cambios. El aviso dice que el producto se actualizó, y lo cierro con aceptar. En el próximo video: comprar en cajas y vender por unidad.",
            "acciones": [
                clic(pestana("Descripción y tienda"), "descripción y tienda"),
                marca(".description-editor", "La descripción es", 5000),
                clic("button[aria-label='Visible en la tienda en línea']", "enciendo visible"),
                marca(".gm-setting:has(button[aria-label='Indexable en buscadores'])", "Indexable en buscadores", 5000),
                clic(GUARDAR, "Guardo los cambios"),
                marca(ALERTA, "El aviso dice", 3000, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "con aceptar"),
            ],
        },
    ],
}

# ───────────────────────── 08 · Convertir la unidad base ─────────────────────────
VIDEOS["productos-08-convertir-unidad-base"] = {
    "titulo": "Productos · Parte 8: convertir la unidad base",
    "descripcion": "Octavo video de Productos en Germiva ERP: qué hacer cuando un producto que llevabas por caja ahora quieres venderlo suelto. «Convertir unidad base» pasa la existencia, el costo, los precios y el kardex a la unidad nueva en un solo paso, y deja la caja como empaque.",
    "_comentario": "Serie Productos corta (nov. 2026), video 8. Estado A: «Galletas soda Crocante» con unidad base Caja/Cajón, 20 cajas a costo 180, RD$300 con ITBIS, mínimo 5 / máximo 40. Conversión a Unidad con factor 12: existencia 20 → 240, costo 180 → 15, precio 300 → 25 (exacto: ya no hay aviso de redondeo), mínimo 60 / máximo 480, y la caja queda como empaque ×12 a 300.",
    "sesion": LISTA, "setup": RESTAURAR("A"),
    "aprenderas": ["Cuándo hace falta convertir la unidad base", "Usar «Ver impacto» antes de convertir", "Qué cambia: existencia, costo, precio, mínimo y máximo", "Cómo queda la caja como empaque después de convertir"],
    "errores_comunes": ["Cambiar la unidad de medida a mano: la existencia y el costo quedan en la unidad equivocada", "Convertir sin revisar el impacto", "Olvidar que se puede revertir solo mientras no haya movimientos nuevos"],
    "pasos": [
        {
            "id": "01-abrir", "capitulo": "El caso: de cajas a unidades", "rotulo": "El caso",
            "ruta": "Inventario › Productos",
            "narracion": "Estas galletas se llevan por caja: veinte cajas en existencia, a trescientos pesos cada una. Ahora la tienda quiere venderlas sueltas. Eso no se resuelve cambiando la unidad de medida a mano: hay que convertir la unidad base. Abro la ficha con el lápiz. En características enciendo se compra o se vende en empaques, que se guarda al momento. Y abajo, en la sección unidad base, pulso Convertir unidad base.",
            "acciones": [
                marca(fila("Galletas soda Crocante", 5), "veinte cajas", 1500),
                marca(fila("Galletas soda Crocante", 4), "a trescientos pesos", 2500),
                cartel("Cuidado", "No cambies la unidad de medida a mano: usa «Convertir unidad base».", "Eso no se resuelve", 6000),
                clic("table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Abrir']", "Abro la ficha"),
                clic("button[aria-label='Se compra o se vende en empaques']", "enciendo se compra"),
                clic("button:has-text('Convertir unidad base')", "pulso Convertir"),
            ],
        },
        {
            "id": "02-impacto", "capitulo": "Ver el impacto y convertir", "rotulo": "Ver impacto",
            "ruta": "Inventario › Productos › Galletas soda Crocante",
            "narracion": "El asistente pide dos datos. La unidad nueva: abro la lista y elijo unidad. Y cuántas unidades trae cada caja; aquí son doce. Antes de tocar nada, conviene revisar qué va a pasar: pulso Ver impacto. Arriba, el resumen: la existencia pasa de veinte cajas a doscientas cuarenta unidades, y el valor del inventario no cambia. En la tabla, el costo baja de ciento ochenta por caja a quince por unidad, y el mínimo y el máximo se multiplican por doce. Además, la caja no se pierde: queda como empaque, a sus trescientos pesos, para seguir comprándola igual. Todo cuadra, así que pulso Convertir. El sistema pide una confirmación, porque el cambio toca todo el producto; la doy. El aviso final dice que la caja quedó como empaque; lo cierro.",
            "acciones": [
                marca(DIALOGO, "El asistente pide", 2000, cursor=False),
                clic(f"{DIALOGO} mat-select[formcontrolname='unitMeasureId']", "abro la lista"),
                clic("mat-option:has-text('Unidad') >> nth=0", "elijo unidad"),
                teclea(f"{DIALOGO} input[formcontrolname='factor']", "12", "aquí son doce"),
                clic(f"{DIALOGO} button:has-text('Ver impacto')", "pulso Ver impacto"),
                marca(f"{DIALOGO} .gm-dialog-facts", "Arriba, el resumen", 7000),
                marca(f":nth-match({DIALOGO} .conversion-table, 2) tbody tr:has-text('Costo promedio')", "el costo baja", 4000),
                marca(f":nth-match({DIALOGO} .conversion-table, 2) tbody tr:has-text('Mínimo')", "el mínimo y el máximo", 3000),
                marca(f"{DIALOGO} p.gm-dialog-note:has-text('Se crea el empaque')", "queda como empaque", 5000),
                clic(f"{DIALOGO} button:has-text('Convertir'):not(:has-text('Sí'))", "pulso Convertir"),
                marca(f"{DIALOGO}:has-text('¿Convertir la unidad base?')", "pide una confirmación", 3000, cursor=False),
                clic("button:has-text('Sí, convertir')", "la doy"),
                marca(ALERTA, "El aviso final", 3000, cursor=False),
                clic(f"{DIALOGO} button:has-text('Entendido')", "lo cierro"),
            ],
        },
        {
            "id": "03-resultado", "capitulo": "La ficha después de convertir", "rotulo": "El resultado",
            "ruta": "Inventario › Productos",
            "navegar": "/inventory/product/list",
            "narracion": "Para ver el resultado, vuelvo al catálogo y busco las galletas por su nombre. Ahí está la fila. El stock ya dice doscientas cuarenta, y el precio de venta, veinticinco pesos: trescientos entre doce. Abro la ficha. La unidad de medida ahora es unidad. Y en unidades y empaques está la caja por doce, con su precio de trescientos y la estrella de compra: se sigue comprando por caja, y ahora también se vende suelta. Si te equivocaste, la conversión se puede revertir mientras no haya movimientos nuevos.",
            "acciones": [
                teclea(filtro("Buscar") + " input", "Galletas", "busco las galletas"),
                marca(fila("Galletas soda Crocante", 5), "El stock ya dice", 2000),
                marca(fila("Galletas soda Crocante", 4), "el precio de venta", 3500),
                clic("table tbody tr:has-text('Galletas soda Crocante') button[aria-label='Abrir']", "Abro la ficha"),
                marca("mat-form-field:has(mat-label:has-text('Unidad de medida'))", "La unidad de medida ahora", 2500),
                marca("app-product-units-panel tbody tr:nth-child(1)", "la caja por doce", 7000),
                marca("button:has-text('Convertir unidad base'), button:has-text('Revertir')", "se puede revertir", 4500),
            ],
        },
    ],
}

# ───────────────────────── 07 · Productos por peso y balanza ─────────────────────────
UNIDADES = "app-product-units-panel"
VIDEOS["productos-07-peso-y-balanza"] = {
    "titulo": "Productos · Parte 7: productos por peso y balanza",
    "descripcion": "Séptimo video de Productos en Germiva ERP: vender por peso sin teclear nada. Activar la balanza etiquetadora de la tienda, preparar un producto que se lleva por libra (con su kilo como empaque y su código de balanza) y cobrarlo en el punto de venta escaneando la etiqueta.",
    "_comentario": "Serie Productos corta (nov. 2026), video 7. Estado A: balanza apagada; «Habichuelas rojas» por Libra, RD$85 exento, 250 lb. Formato de balanza por defecto: prefijo 21 + 5 dígitos de producto + 5 de peso con 3 decimales. Etiqueta 21 + 00123 + 02350 + 9 = 2100123023509 → 2.35 lb × 85 = RD$199.75. Tras guardar la configuración la página queda «sucia»: se sale por el panel (navegación interna), no con goto.",
    "setup": RESTAURAR("A"),
    "aprenderas": ["Activar la balanza etiquetadora y entender su formato", "Agregar el kilo como empaque de un producto que se lleva por libra", "Asignar el código de balanza del producto", "Cobrar en el punto de venta escaneando la etiqueta de peso"],
    "errores_comunes": ["Poner en el producto un código de balanza distinto al que tiene programado la balanza", "Cambiar la unidad base a kilo: el kilo se agrega como empaque", "Teclear el peso a mano en el punto de venta teniendo la etiqueta"],
    "pasos": [
        {
            "id": "01-balanza", "capitulo": "Activar la balanza", "rotulo": "La balanza",
            "ruta": "Inventario › Configuración",
            "narracion": "¿Vendes por libra? Con una balanza etiquetadora no hay que teclear el peso. Primero se activa. Entro a Inventario y abro Configuración. Más abajo está la sección balanza etiquetadora. La balanza es de la tienda, no de un producto: imprime una etiqueta con el código del producto y el peso dentro del código de barras. Enciendo uso balanza etiquetadora, y aparece el formato: el prefijo veintiuno, cinco dígitos para el producto y cinco para el peso. Son los valores de las balanzas más comunes; si la tuya usa otros, se ajustan aquí. Pulso Guardar, y cierro el aviso que confirma el cambio.",
            "acciones": [
                clic("nav.module-rail [aria-label='Inventario']", "Entro a Inventario"),
                clic(".panel-item:has-text('Configuración')", "abro Configuración"),
                marca("h3.section-title:has-text('Balanza etiquetadora')", "está la sección", 2500),
                marca(".switch-row:has-text('Uso balanza etiquetadora')", "La balanza es de la tienda", 7000, cursor=False),
                clic(".switch-row:has-text('Uso balanza etiquetadora') mat-slide-toggle button", "Enciendo uso balanza"),
                marca("[formgroupname='scaleLabelFormat']", "aparece el formato", 8000),
                clic(".footer-right button:has-text('Guardar')", "Pulso Guardar"),
                marca(ALERTA, "cierro el aviso", 1500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Entendido')", "confirma el cambio"),
            ],
        },
        {
            "id": "02-producto", "capitulo": "Preparar el producto", "rotulo": "El producto",
            "ruta": "Inventario › Productos › Habichuelas rojas",
            "narracion": "Ahora el producto. Abro Productos, y en el buscador escribo habichuelas. La tabla se filtra y, cuando queda solo esa fila, abro su ficha con el lápiz. Se abre con todos sus datos, y arriba, en la información general, está lo primero que hay que mirar. Su unidad base es la libra: la existencia y el precio, ochenta y cinco pesos, van por libra. Enciendo se compra o se vende en empaques, y agrego un empaque. El aviso rojo de abajo pide su unidad, así que abro la lista de unidades y elijo kilogramo. Fíjate en el contenido: dos punto dos libras, sin escribirlo, porque el sistema conoce la equivalencia entre libra y kilo. Por último, a la derecha, el código de balanza: es el número con que la balanza conoce este producto, y escribo ciento veintitrés, el mismo que tiene programado la balanza. Con eso está listo. Guardo la ficha y, cuando el aviso lo confirma, lo acepto.",
            "acciones": [
                clic(".panel-item:has-text('Productos')", "Abro Productos"),
                teclea(filtro("Buscar") + " input", "Habichuelas", "escribo habichuelas"),
                clic("table tbody tr:has-text('Habichuelas rojas') button[aria-label='Abrir']", "abro su ficha"),
                marca("mat-form-field:has(mat-label:has-text('Unidad de medida'))", "Su unidad base", 3000),
                marca(PRECIOS, "ochenta y cinco pesos", 2500),
                clic("button[aria-label='Se compra o se vende en empaques']", "Enciendo se compra"),
                clic(f"{UNIDADES} button:has-text('Agregar empaque')", "agrego un empaque"),
                marca(f"{UNIDADES} .units-error", "El aviso rojo", 2500, cursor=False),
                clic(f"{UNIDADES} tbody tr:nth-child(1) mat-select[aria-label='Unidad del empaque']", "abro la lista de unidades"),
                clic("mat-option:has-text('Kilogramo')", "elijo kilogramo"),
                marca(f"{UNIDADES} tbody tr:nth-child(1) td[data-label='Contenido']", "en el contenido", 6500),
                marca(ctl("scalePlu"), "el código de balanza", 5000),
                teclea(ctl("scalePlu"), "123", "escribo ciento veintitrés"),
                clic(GUARDAR, "Guardo la ficha"),
                marca(ALERTA, "el aviso lo confirma", 1500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "lo acepto"),
            ],
        },
        {
            "id": "03-pos", "capitulo": "Cobrar con la etiqueta de peso", "rotulo": "Punto de venta",
            "ruta": "Punto de venta",
            "navegar": "/pos",
            "narracion": "Vamos al punto de venta. El cliente pide habichuelas; se pesan, y la balanza imprime su etiqueta. En el buscador escaneo esa etiqueta. Aquí, como no tengo lector, escribo el código completo, los trece dígitos de la etiqueta, y al terminar pulso Enter. El ticket recibe las habichuelas con dos punto treinta y cinco libras: el peso venía dentro del código. El precio es por libra, ochenta y cinco pesos, y la línea suma ciento noventa y nueve con setenta y cinco. Así se vende cualquier producto pesado: sin teclear el peso y sin errores al cobrar.",
            "acciones": [
                teclea("input[aria-label='Buscar producto']", "2100123023509", "escribo el código completo"),
                tecla("Enter", "pulso Enter"),
                marca(".ps-line:has-text('Habichuelas')", "El ticket recibe", 5500),
                marca(".ps-line:has-text('Habichuelas') .ps-line__unit", "El precio es por libra", 3500),
                marca(".ps-line:has-text('Habichuelas') .ps-line__total", "la línea suma", 4000),
            ],
        },
    ],
}

# ───────────────────────── 09 · Variantes: crearlas ─────────────────────────
VIDEOS["productos-09-variantes-crear"] = {
    "titulo": "Productos · Parte 9: crear un producto con variantes",
    "descripcion": "Noveno video de Productos en Germiva ERP: un mismo producto en varias presentaciones y sabores, cada uno con su código, su precio y su existencia. Creamos una gaseosa en lata, grande y jumbo, de naranja, piña y fresa, con el recargo de cada tamaño, en una sola pantalla.",
    "_comentario": "Serie Productos corta (nov. 2026), video 9. Estado A. Crea «Gaseosa Brisa» (RD$35 con ITBIS incluido): opción Presentación con el atajo de colmado sin «Botella 12 oz» (Lata 12 oz, Grande 22 oz, Jumbo 1 L) y opción Sabor (Naranja, Piña, Fresa). Recargo Grande +25 y Jumbo +50 → 35 / 60 / 85. Se desmarca Jumbo + Fresa: se crean 8 variantes. Es el estado de partida del video 10.",
    "sesion": LISTA, "setup": RESTAURAR("A"),
    "aprenderas": ["Cuándo conviene un producto con variantes", "Definir las opciones y sus valores", "Poner un recargo por tamaño", "Leer la matriz y elegir qué combinaciones crear"],
    "errores_comunes": ["Crear un producto aparte por cada sabor: se pierde el resumen y el selector al vender", "Escribir los valores en desorden: ese es el orden en que se ven al vender", "Crear combinaciones que no vendes: se desmarcan en la matriz"],
    "pasos": [
        {
            "id": "01-alta", "capitulo": "Un producto con variantes", "rotulo": "Variantes",
            "ruta": "Inventario › Productos › Nuevo",
            "narracion": "Una gaseosa en lata, grande y jumbo, de naranja, piña y fresa: son nueve productos, pero se crean como uno solo, con variantes. Pulso Nuevo Producto. El nombre: Gaseosa Brisa, que es lo común a todas. Sigue la categoría, igual que en cualquier producto. En categoría escribo las primeras letras de alimentos, espero a que la lista las encuentre, y la tomo de ahí. Luego, en unidad de medida escribo unidad; la lista muestra las que coinciden, y de ellas también la tomo. El precio base va en monto: treinta y cinco pesos, que es lo que cuesta la lata. Ese precio ya trae el impuesto sobre la venta, así que enciendo ITBIS incluido. Estos datos son comunes a todas. Ahora, en características, enciendo tiene variantes.",
            "acciones": [
                cartel("En este video", "Un producto, varias presentaciones y sabores: cada una con su código, precio y existencia.", "son nueve productos", 6000),
                clic("button:has-text('Nuevo Producto')", "Pulso Nuevo Producto"),
                teclea(ctl("name"), "Gaseosa Brisa", "El nombre"),
                teclea(campo("Categoría"), "Alimen", "En categoría escribo"),
                clic("mat-option:has-text('Alimentos') >> nth=0", "la tomo de ahí"),
                teclea(campo("Unidad de medida"), "Unidad", "escribo unidad"),
                clic("mat-option:has-text('Unidad (UND)')", "también la tomo"),
                teclea(f"{PRECIOS} input[type='number']", "35", "treinta y cinco pesos"),
                clic(f"{PRECIOS} button[aria-label='ITBIS incluido']", "enciendo ITBIS incluido"),
                clic("button[aria-label='Tiene variantes']", "enciendo tiene variantes"),
            ],
        },
        {
            "id": "02-opciones", "capitulo": "Opciones y valores", "rotulo": "Opciones",
            "ruta": "Inventario › Productos › Nuevo",
            "narracion": "Aparece la sección opciones y variantes. Una opción es lo que distingue a las variantes, y sus valores son las alternativas. Hay atajos ya escritos para los casos más comunes. Aquí pulso el de presentación, que trae lata, botella, grande y jumbo. La botella no la vendo, así que la quito con su equis. El sabor no tiene atajo: pulso otra, y en el nombre de la opción escribo sabor. Ahora sus valores, uno por uno. Escribo naranja en el campo de valores, y para que quede como etiqueta pulso la tecla Enter. Después escribo piña, de la misma manera, y al terminar vuelvo a pulsar Enter. Y el último valor es fresa: lo escribo completo, y también lo confirmo igual. Fíjate en las etiquetas: el orden en que las escribes es el orden en que se verán al vender.",
            "acciones": [
                marca(".vb-section .section-title", "opciones y variantes", 2500),
                marca(".vb-presets", "Hay atajos", 2500),
                clic(".vb-presets button:has-text('Presentación (cerveza y refresco)')", "pulso el de presentación"),
                clic("button[aria-label='Quitar Botella 12 oz']", "la quito"),
                clic(".vb-presets button:has-text('Otra')", "pulso otra"),
                teclea(".vb-option >> nth=1 >> input >> nth=0", "Sabor", "escribo sabor"),
                teclea(".vb-option >> nth=1 >> .vb-values__input", "Naranja", "Escribo naranja"),
                tecla("Enter", "la tecla Enter"),
                teclea(".vb-option >> nth=1 >> .vb-values__input", "Piña", "escribo piña"),
                tecla("Enter", "vuelvo a pulsar"),
                teclea(".vb-option >> nth=1 >> .vb-values__input", "Fresa", "es fresa"),
                tecla("Enter", "confirmo igual"),
                marca(".vb-option >> nth=1 >> .vb-values", "Fíjate en las etiquetas", 4500),
            ],
        },
        {
            "id": "03-recargo-matriz", "capitulo": "Recargo, matriz y guardar", "rotulo": "La matriz",
            "ruta": "Inventario › Productos › Nuevo",
            "narracion": "El sistema pregunta si alguna opción cambia el precio. La presentación sí, así que la elijo, y aparece un campo por cada tamaño. A la grande le sumo veinticinco pesos sobre el precio base. Y a la jumbo le sumo el doble: cincuenta pesos. Debajo está la matriz: presentaciones en filas, sabores en columnas, y en cada cruce su precio, treinta y cinco, sesenta u ochenta y cinco. La jumbo de fresa todavía no la vendo, así que la desmarco. El botón dice cuántas se van a crear: ocho. Lo pulso. El sistema crea el producto padre y cada combinación como su hija, y el aviso lo confirma; acepto. En el siguiente video las vemos por dentro, les damos existencia y las vendemos.",
            "acciones": [
                marca(".vb-surcharge__q", "El sistema pregunta", 3000),
                clic(".vb-surcharge button:has-text('Presentación')", "la elijo"),
                teclea(".vb-surcharge__field:has(mat-label:text-is('Grande 22 oz')) input", "25", "A la grande"),
                teclea(".vb-surcharge__field:has(mat-label:text-is('Jumbo 1 L')) input", "50", "a la jumbo"),
                marca(".vb-children__title", "Debajo está la matriz", 2500),
                marca(".vb-matrix tbody tr >> nth=1 >> td >> nth=1", "en cada cruce", 5000),
                clic(".vb-matrix tbody tr >> nth=2 >> td >> nth=2 >> .mdc-checkbox", "la desmarco"),
                marca("button:has-text('Guardar producto y')", "El botón dice", 2500),
                clic("button:has-text('Guardar producto y')", "Lo pulso"),
                marca(ALERTA, "el aviso lo confirma", 2000, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "acepto"),
            ],
        },
    ],
}

# ───────────────────────── 10 · Variantes: ficha, existencia y venta ─────────────────────────
VIDEOS["productos-10-variantes-vender"] = {
    "titulo": "Productos · Parte 10: variantes por dentro, su existencia y su venta",
    "descripcion": "Décimo video de Productos en Germiva ERP: qué es el producto padre y qué es cada variante, cómo crear una combinación que faltaba, darle existencia a una variante y venderla en el punto de venta con el selector de presentación y sabor.",
    "_comentario": "Serie Productos corta (nov. 2026), video 10. Parte del resultado del video 9 (el setup lo ensaya sin grabar): «Gaseosa Brisa» con 8 variantes a 35 / 60 / 85. En cámara: se crea Jumbo 1 L + Fresa desde la matriz (85), entrada de 24 latas de naranja a RD$20 a la variante «Lata 12 oz + Naranja», y en el POS se agregan 2 latas (RD$70) desde el selector del padre.",
    "sesion": LISTA,
    "setup": {"tipo": "shell", "cmd": "./.venv/bin/python seeds/_puertas/ensayar.py guiones/productos-09-variantes-crear.json"},
    "aprenderas": ["Diferenciar el producto padre de sus variantes", "Crear una combinación nueva desde la matriz", "Registrar la entrada de mercancía de una variante", "Vender una variante desde el selector del punto de venta"],
    "errores_comunes": ["Buscar la existencia en el padre: el padre no guarda mercancía, la guardan sus variantes", "Registrar la entrada en la variante equivocada", "Cambiar el precio del padre sin saber que arrastra a las variantes que lo heredan"],
    "pasos": [
        {
            "id": "01-padre", "capitulo": "El padre y sus variantes", "rotulo": "El padre",
            "ruta": "Inventario › Productos › Gaseosa Brisa",
            "narracion": "En el video anterior creamos la gaseosa con sus variantes. En el catálogo la busco por su nombre, y cuando aparece abro la ficha del padre. El padre es la plantilla: define lo común, pero no se vende ni guarda existencia. Abro la pestaña variantes. Cada fila es una variante, con su propio código de barras. Las latas dicen del padre: usan su precio y cambian con él. Paso a la vista matriz. La jumbo de fresa, que dejamos fuera, dice crear: la pulso, se abre una ventanita, y en ella escribo su precio, ochenta y cinco pesos, y luego confirmo con el botón crear. El aviso lo confirma, y ya está la combinación que faltaba.",
            "acciones": [
                teclea(filtro("Buscar") + " input", "Gaseosa", "la busco por su nombre"),
                clic("table tbody tr:has-text('Gaseosa Brisa') button[aria-label='Abrir'] >> nth=0", "abro la ficha"),
                marca(".gm-badge:text-is('Producto padre')", "El padre es la plantilla", 4500),
                clic(pestana("Variantes"), "Abro la pestaña"),
                marca(".vp-table tbody tr >> nth=0 >> td >> nth=2", "con su propio código", 3000),
                marca(".vp-inherited >> nth=0", "Las latas dicen", 4000),
                clic(".gm-seg button:has-text('Matriz')", "vista matriz"),
                clic(".vp-cell--new", "la pulso"),
                teclea(".vp-pop input.money-input__control", "85", "escribo su precio"),
                clic(".vp-pop button:has-text('Crear')", "el botón crear"),
                marca(SNACK, "El aviso lo confirma", 2000, cursor=False),
                marca(".vp-matrix tbody tr >> nth=2", "la combinación que faltaba", 3000),
            ],
        },
        {
            "id": "02-entrada", "capitulo": "Darle existencia a una variante", "rotulo": "Entrada",
            "ruta": "Inventario › Productos › Lata 12 oz + Naranja",
            "narracion": "La mercancía entra a cada variante, no al padre. Vuelvo a la lista y abro la lata de naranja. La barra de arriba dice que es un producto hijo, con el enlace a su padre. Arriba pulso el botón de entrada, y se abre su ventana. En el motivo elijo compras de mercancía. En proveedor escribo las primeras letras, espero a que la lista lo encuentre, y elijo la Embotelladora del Caribe. La ubicación: abro la lista y elijo el pasillo A del almacén Sur. El lote lo genera el botón de al lado. En cantidad, veinticuatro latas, que es lo que trae la caja. Y el costo de cada una: veinte pesos, sin el impuesto. Abajo confirmo el registro. El sistema avisa que la compra quedó registrada con su recepción, a la espera de la factura del proveedor; lo acepto. Arriba, la variante ya tiene veinticuatro en existencia.",
            "acciones": [
                clic(".gm-seg button:has-text('Lista')", "Vuelvo a la lista"),
                clic("button[aria-label='Abrir Lata 12 oz + Naranja']", "abro la lata"),
                marca(".child-bar__parent", "es un producto hijo", 3500),
                clic("button:has-text('Registrar Entrada')", "el botón de entrada"),
                marca(DIALOGO, "se abre su ventana", 1500, cursor=False),
                clic(f"{DIALOGO} mat-select[formcontrolname='inventoryMovementTypeId']", "En el motivo"),
                clic("mat-option:has-text('Compras de mercancía')", "compras de mercancía"),
                teclea(f"{DIALOGO} [formcontrolname='partnerId'] input", "Embotell", "escribo las primeras letras"),
                clic("mat-option:has-text('Embotelladora del Caribe')", "elijo la Embotelladora"),
                clic(f"{DIALOGO} [formcontrolname='locationId'] input", "La ubicación"),
                clic("mat-option:has-text('Pasillo A - Estante 1')", "el pasillo A"),
                clic(f"{DIALOGO} button:has(mat-icon:text('auto_awesome'))", "lo genera el botón"),
                teclea(f"{DIALOGO} input[formcontrolname='quantity']", "24", "En cantidad"),
                teclea(f"{DIALOGO} input[formcontrolname='unitPrice']", "20", "el costo de cada una"),
                clic(f"{DIALOGO} button:has-text('Registrar entrada')", "confirmo el registro"),
                marca(f"{SNACK}, {ALERTA}", "El sistema avisa", 4500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "lo acepto"),
                marca(".hero-stock >> nth=0", "ya tiene veinticuatro", 3500),
            ],
        },
        {
            "id": "03-pos", "capitulo": "Vender una variante", "rotulo": "Punto de venta",
            "ruta": "Punto de venta", "navegar": "/pos",
            "narracion": "Y ahora, la venta. En el punto de venta busco gaseosa, escribiendo su nombre. El catálogo se filtra, y aparece una sola tarjeta, la del padre, con todas sus variantes. Al tocarla se abre el selector: presentaciones en filas y sabores en columnas. Solo la lata de naranja tiene existencia; las demás dicen agotado. Le sumo una lata con el botón más, y enseguida otra: son dos latas. Abajo pulso Agregar, y el ticket recibe la línea con el nombre completo de la variante. Y con lector de código de barras ni siquiera hace falta el selector: escaneas la lata y entra directo.",
            "acciones": [
                teclea("input[aria-label='Buscar producto']", "Gaseosa", "busco gaseosa"),
                marca("button.ps-card:has-text('Gaseosa Brisa')", "una sola tarjeta", 3000),
                clic("button.ps-card:has-text('Gaseosa Brisa')", "Al tocarla"),
                marca(DIALOGO, "se abre el selector", 3000, cursor=False),
                clic("button[aria-label^='Sumar una unidad de Lata 12 oz'][aria-label*='Naranja']", "Le sumo una lata"),
                clic("button[aria-label^='Sumar una unidad de Lata 12 oz'][aria-label*='Naranja']", "enseguida otra"),
                clic(f"{DIALOGO} button:has-text('Agregar')", "pulso Agregar"),
                marca(".ps-line:has-text('Naranja')", "el ticket recibe", 5000),
            ],
        },
    ],
}

# ───────────────────────── 11 · Comercio exterior e insumos ─────────────────────────
INSUMOS = "app-product-supplies"
def insumo(nombre, campo_): return f"{INSUMOS} tbody tr:has-text('{nombre}') input[aria-label='{campo_}']"
VIDEOS["productos-11-exterior-e-insumos"] = {
    "titulo": "Productos · Parte 11: comercio exterior e insumos",
    "descripcion": "Undécimo video de Productos en Germiva ERP: los datos de aduana de un producto que se importa (partida arancelaria, país de origen y pesos) y los insumos de un producto que preparas, para conocer su costo real y su margen antes de ponerle precio.",
    "_comentario": "Serie Productos corta (nov. 2026), video 11. Estado A + insumos de cocina (insumos.mjs). Refresco: partida 2202.10.00, origen Estados Unidos, bruto 0.385 kg, neto 0.37 kg. Producto nuevo «Dulce criollo casero» a RD$150 con ITBIS incluido (neto 127.12); insumos: 0.25 lb de habichuela con 10 % de merma (52 × 0.25 × 1.1 = 14.30), 0.25 lata de leche (65 × 0.25 = 16.25) y 0.15 lb de azúcar (38 × 0.15 = 5.70) → costo 36.25, margen 90.87 (71.5 %). La pestaña Insumos enlaza con Fabricación («Abrir fabricación»), que tiene su propia serie.",
    "sesion": LISTA,
    "setup": {"tipo": "shell", "cmd": "node seeds/productos/restaurar.mjs A && node seeds/productos/insumos.mjs"},
    "aprenderas": ["Registrar la partida arancelaria, el origen y los pesos de un producto importado", "Agregar los insumos que consume un producto preparado", "Poner la cantidad real y la merma de cada insumo", "Leer el costo de insumos y el margen teórico"],
    "errores_comunes": ["Dejar los insumos con cantidad uno: el costo sale inflado y el margen en rojo", "Olvidar la merma de lo que se pierde al preparar", "Poner el precio de un producto preparado sin mirar su margen"],
    "pasos": [
        {
            "id": "01-exterior", "capitulo": "Comercio exterior", "rotulo": "Comercio exterior",
            "ruta": "Inventario › Productos › Refresco Caribe Cola lata",
            "narracion": "Si importas o exportas, la aduana pide datos de cada producto. Este refresco lo traemos de fuera. En el catálogo escribo refresco; la tabla se filtra, y cuando queda solo su fila abro la ficha con el lápiz. En características enciendo se importa o se exporta, y abajo aparece la sección comercio exterior. Primero la partida arancelaria, el código con que la aduana clasifica la mercancía; la escribo completa, con sus puntos. Después el país de origen: escribo estados, espero a que la lista lo encuentre entre todos los países, y elijo Estados Unidos. Luego el peso bruto de una lata, con su envase, en kilos. Y por último el peso neto, que es solo el contenido, sin el envase. Guardo la ficha, y acepto el aviso que lo confirma.",
            "acciones": [
                teclea(filtro("Buscar") + " input", "Refresco", "escribo refresco"),
                clic("table tbody tr:has-text('Refresco Caribe Cola lata') button[aria-label='Abrir']", "abro la ficha"),
                clic("button[aria-label='Se importa o se exporta']", "enciendo se importa"),
                marca("h3.section-title:has-text('Comercio exterior')", "abajo aparece", 2500),
                teclea(ctl("tariffCode"), "2202.10.00", "Primero la partida"),
                teclea("[formcontrolname='originCountry'] input", "Estados", "escribo estados"),
                clic("mat-option:has-text('Estados Unidos (US)')", "elijo Estados Unidos"),
                teclea(ctl("grossWeight"), "0.385", "el peso bruto"),
                teclea(ctl("netWeight"), "0.37", "el peso neto"),
                clic(GUARDAR, "Guardo la ficha"),
                marca(ALERTA, "y acepto", 1200, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "que lo confirma"),
            ],
        },
        {
            "id": "02-producto-preparado", "capitulo": "Un producto que se prepara", "rotulo": "Insumos",
            "ruta": "Inventario › Productos › Nuevo", "navegar": "/inventory/product/list",
            "narracion": "Ahora los insumos, que sirven para conocer el costo real de lo que preparas: un plato, un combo o un dulce. Vamos a costear un vaso de habichuelas con dulce. Pulso Nuevo Producto. Lo llamo dulce criollo casero, tal como saldrá en la factura. Sigue la categoría, como en cualquier producto. En categoría escribo las primeras letras de alimentos, espero la lista, y la tomo de ahí. En unidad de medida escribo unidad, porque se vende por vaso; la lista muestra las opciones, y de ellas también la elijo. El precio del vaso va en monto: ciento cincuenta pesos. Ese precio ya trae el impuesto sobre la venta, así que enciendo ITBIS incluido. Pulso Guardar, y acepto el aviso. Con el producto creado se habilita la pestaña insumos, y la abro.",
            "acciones": [
                clic("button:has-text('Nuevo Producto')", "Pulso Nuevo Producto"),
                teclea(ctl("name"), "Dulce criollo casero", "Lo llamo"),
                teclea(campo("Categoría"), "Alimen", "En categoría escribo"),
                clic("mat-option:has-text('Alimentos') >> nth=0", "la tomo de ahí"),
                teclea(campo("Unidad de medida"), "Unidad", "escribo unidad"),
                clic("mat-option:has-text('Unidad (UND)')", "también la elijo"),
                teclea(f"{PRECIOS} input[type='number']", "150", "ciento cincuenta pesos"),
                clic(f"{PRECIOS} button[aria-label='ITBIS incluido']", "enciendo ITBIS incluido"),
                clic(GUARDAR, "Pulso Guardar"),
                marca(ALERTA, "y acepto", 1200, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "el aviso. Con"),
                clic("mat-tab-group.product-tabs .mdc-tab:has-text('Insumos')", "la abro"),
            ],
        },
        {
            "id": "03-receta", "capitulo": "Cantidades, merma y margen", "rotulo": "El margen",
            "ruta": "Inventario › Productos › Dulce criollo casero › Insumos",
            "narracion": "Aquí va lo que consume cada vaso. En agregar insumo escribo habichuela; la lista busca entre los insumos de la empresa, y elijo la habichuela roja para cocinar. Hago lo mismo con la leche: la escribo en el mismo campo, espero un momento, y de la lista tomo la leche evaporada. Y falta el azúcar: lo busco por su nombre, la lista lo encuentra, y entonces elijo el azúcar crema. Antes de seguir, hay que revisar los números de arriba. Mira el margen teórico: sale en rojo, porque cada insumo entró con cantidad uno, como si un vaso llevara una libra entera. Pongo las cantidades reales. De habichuela, un cuarto de libra, que es lo que lleva un vaso. Y su merma, lo que se pierde al cocinar: diez por ciento. De leche, un cuarto de lata por cada vaso que se sirve. Y de azúcar, quince centésimas de libra, un poco más de dos onzas. Salgo del campo, y cada cambio se guarda solo. Ahora sí: el vaso cuesta treinta y seis pesos con veinticinco, y el margen es de noventa pesos, el setenta y uno por ciento del precio. Y si esto lo fabricas por tandas, el botón Abrir fabricación lleva estos insumos a una lista de materiales.",
            "acciones": [
                teclea(f"{INSUMOS} input >> nth=0", "Habichuela", "escribo habichuela"),
                clic("mat-option:has-text('Habichuela roja para cocinar')", "elijo la habichuela roja"),
                teclea(f"{INSUMOS} input >> nth=0", "Leche", "la escribo"),
                clic("mat-option:has-text('Leche evaporada lata')", "tomo la leche evaporada"),
                teclea(f"{INSUMOS} input >> nth=0", "Azúcar", "lo busco"),
                clic("mat-option:has-text('Azúcar crema')", "elijo el azúcar crema"),
                marca(f"{INSUMOS} .gm-stat:has-text('Margen teórico')", "Mira el margen teórico", 6500),
                teclea(insumo("Habichuela", "Cantidad por unidad producida"), "0.25", "un cuarto de libra"),
                teclea(insumo("Habichuela", "Porcentaje de merma"), "10", "Y su merma"),
                teclea(insumo("Leche", "Cantidad por unidad producida"), "0.25", "un cuarto de lata"),
                teclea(insumo("Azúcar", "Cantidad por unidad producida"), "0.15", "quince centésimas"),
                tecla("Tab", "Salgo del campo"),
                marca(f"{INSUMOS} .gm-stat >> nth=0", "el vaso cuesta", 3500),
                marca(f"{INSUMOS} .gm-stat:has-text('Margen teórico')", "el margen es de noventa", 4500),
                marca(f"{INSUMOS} a:has-text('Abrir fabricación')", "el botón Abrir fabricación", 5000),
            ],
        },
    ],
}

# ───────────────────────── 12 · Listas de precios ─────────────────────────
CATALOGO = "app-price-list-catalog"
VIDEOS["productos-12-listas-de-precios"] = {
    "titulo": "Productos · Parte 12: listas de precios",
    "descripcion": "Duodécimo video de Productos en Germiva ERP: precios distintos para distintos clientes sin escribir un precio por producto. Creamos una lista calculada (diez por ciento menos que el precio regular), se la asignamos a un cliente y vemos cómo la factura propone sola su precio.",
    "_comentario": "Serie Productos corta (nov. 2026), video 12. Estado A. Lista «Colmados» = Precio regular −10 %, redondeo a 5. Cliente «Colmado La Esquina» (RNC 130555102; id 240 en el canon armado sobre la instantánea del dev-env: si el canon se rearma y el id cambia, ajustar la ruta del paso 2). Habichuelas rojas: 85 → 76.50 → redondeado 75.",
    "sesion": {**COMUN["sesion"], "navegar": "/inventory/config", "esperar": CATALOGO},
    "setup": RESTAURAR("A"),
    "aprenderas": ["Dónde se definen las listas de precios", "Crear una lista calculada sobre otra, con redondeo", "Asignar la lista a un cliente", "Ver el precio de la lista en la factura"],
    "errores_comunes": ["Crear una lista de precio fijo y escribir cada precio a mano cuando basta un porcentaje", "Olvidar asignar la lista al cliente: seguiría con el precio regular", "Esperar que cambie una factura ya hecha: la lista aplica a los documentos nuevos"],
    "pasos": [
        {
            "id": "01-lista", "capitulo": "Crear una lista calculada", "rotulo": "Nueva lista",
            "ruta": "Inventario › Configuración › Listas de precios",
            "narracion": "A los colmados que te compran para revender les das mejor precio. Eso no se hace producto por producto: se hace con una lista de precios. Están en Inventario, Configuración, al final de la página. La tabla muestra las que ya existen, y la primera es la lista por defecto. Pulso Nueva lista, y se abre su ventana. En tipo elijo porcentaje sobre otra lista. La lista base será el precio regular. En porcentaje escribo menos diez, es decir, diez por ciento menos que la base. En redondeo pongo cinco, para que los precios queden en múltiplos de cinco pesos. Y el nombre de la lista: colmados, que es a quienes se la voy a dar. Con todo lleno, pulso Guardar, y el aviso confirma que se creó. Ahí está, con su cálculo.",
            "acciones": [
                cartel("En este video", "Precios distintos por cliente, sin escribir un precio por producto.", "les das mejor precio", 6000),
                marca(f"{CATALOGO} h3, {CATALOGO}", "al final de la página", 3000),
                marca(f"{CATALOGO} table tbody tr:has-text('Precio regular') td:nth-child(1)", "la primera es", 3000),
                clic(f"{CATALOGO} button:has-text('Nueva lista')", "Pulso Nueva lista"),
                marca(f"{DIALOGO} h2, {DIALOGO} .mat-mdc-dialog-title, {DIALOGO}", "se abre su ventana", 1500, cursor=False),
                clic(f"{DIALOGO} mat-select[formcontrolname='type']", "En tipo"),
                clic("mat-option:has-text('% sobre otra lista')", "porcentaje sobre otra lista"),
                clic(f"{DIALOGO} mat-select[formcontrolname='basePriceListId']", "La lista base"),
                clic("mat-option:has-text('Precio regular')", "será el precio regular"),
                teclea(f"{DIALOGO} app-money-input[formcontrolname='percent'] input", "-10", "escribo menos diez"),
                teclea(f"{DIALOGO} app-money-input[formcontrolname='roundingStep'] input", "5", "En redondeo"),
                teclea(f"{DIALOGO} input[formcontrolname='name']", "Colmados", "el nombre de la lista"),
                clic(f"{DIALOGO} button:has-text('Guardar')", "pulso Guardar"),
                marca(SNACK, "el aviso confirma", 2000, cursor=False),
                marca(f"{CATALOGO} table tbody tr:has-text('Colmados') td:nth-child(1)", "Ahí está", 4000),
            ],
        },
        {
            "id": "02-cliente", "capitulo": "Asignarla a un cliente", "rotulo": "El cliente",
            "ruta": "Ventas › Clientes › Colmado La Esquina", "navegar": "/sales/partners/edit/240",
            "narracion": "La lista se asigna en la ficha de cada cliente. Este es el Colmado La Esquina. En el campo lista de precios escribo las primeras letras, espero a que aparezca, y elijo colmados. Desde ahora, sus documentos usan esos precios; si el campo queda vacío, el cliente usa la lista por defecto. Guardo el cliente. Sale la confirmación de que se actualizó, y la cierro con aceptar.",
            "acciones": [
                marca("app-autocomplete:has-text('Lista de precios')", "En el campo lista", 2500),
                teclea("app-autocomplete:has-text('Lista de precios') input", "Colm", "escribo las primeras letras"),
                clic("mat-option:has-text('Colmados')", "elijo colmados"),
                marca("app-autocomplete:has-text('Lista de precios')", "sus documentos usan", 5500),
                clic(".footer-right button:has-text('Guardar')", "Guardo el cliente"),
                marca(ALERTA, "Sale la confirmación", 2500, cursor=False),
                clic(f"{DIALOGO} button:has-text('Aceptar')", "con aceptar"),
            ],
        },
        {
            "id": "03-factura", "capitulo": "El precio en la factura", "rotulo": "La factura",
            "ruta": "Ventas › Facturas › Nueva", "navegar": "/sales/invoices/create",
            "narracion": "Veámoslo en una factura nueva. Viene con consumidor final, así que primero lo quito con su equis. En cliente escribo esquina; la lista lo busca, y cuando aparece el colmado, lo elijo. Ahora agrego un producto: escribo habichuelas en el buscador de líneas, espero las opciones, y las tomo de la lista. Su precio regular es ochenta y cinco pesos, pero para este cliente la factura propone setenta y cinco: ochenta y cinco menos el diez por ciento, redondeado a cinco. Y si mañana sube el precio regular, el de los colmados sube con él, sin tocar nada. Con esto termina la serie de Productos.",
            "acciones": [
                clic("mat-form-field:has(mat-label:text-is('Cliente')) button:has-text('close')", "lo quito con su equis"),
                teclea("input[placeholder='Busque por nombre o RNC/Cédula']", "Esquina", "escribo esquina"),
                clic("mat-option:has-text('Colmado La Esquina')", "lo elijo"),
                teclea("input[placeholder^='Escriba el código o el nombre']", "Habichuelas", "escribo habichuelas"),
                clic("mat-option:has-text('Habichuelas rojas')", "las tomo de la lista"),
                marca(".products-services-section :text('RD$75.00')", "la factura propone", 7000),
                marca("mat-form-field:has(mat-label:text-is('Cliente'))", "el de los colmados", 4000),
            ],
        },
    ],
}

if __name__ == "__main__":
    for nombre, v in VIDEOS.items():
        guion = {**COMUN, **v}
        (RAIZ / "guiones" / f"{nombre}.json").write_text(json.dumps(guion, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        pal = sum(len(p["narracion"].split()) for p in v["pasos"])
        print(f"{nombre}: {len(v['pasos'])} pasos, {pal} palabras (~{pal/2.9/60:.1f} min)")
