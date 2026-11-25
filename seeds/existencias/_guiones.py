"""Genera los guiones de la serie «Existencias» (cargas masivas de existencias, Repuestos Germiva).

    python3 seeds/existencias/_guiones.py            # escribe guiones/existencias-*.json

Cabecera común (voz, música, marca, privacidad); cada video declara su estado de restaurar.mjs.
"""
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
D = "mat-dialog-container"

CABECERA = {
    "base_url": "http://localhost:4200",
    "zona_horaria": "America/Santo_Domingo",
    "sesion": {"tipo": "api", "url": "http://localhost:3001/api/auth/dev/login",
               "cuerpo": {"username": "admin", "password": "admin"}, "clave": "aut", "extra": {"__v": 2},
               "navegar": "/home"},
    "voz": {"id": "es-DO-RamonaNeural", "velocidad": "+12%"},
    "musica": {"archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -32, "ducking": True, "fade_s": 2},
    "loudnorm": {"lufs": -14, "tp": -1.5},
    "marca_video": {"entrada_s": 3, "cierre_s": 3},
    "rotulo_paso": {"segundos": 3.5},
    "css_global": ["app-chatbot-widget{display:none!important}", ".chatbot-fab{display:none!important}"],
    "pronunciacion": {"ITBIS": "itebís", "RNC": "erre ene ce", "606": "seiscientos seis", "SRL": "ese erre ele",
                      "DOT 4": "dot cuatro"},
    "privacidad": {
        "perfil": "ninguno",
        "permitidos": ["germiva", "130555", "Almacén", "Sucursal", "Santiago", "Inventario", "Conteo", "Complemento",
                       "Sobrante", "Corrige", "Contenedor", "Kit de embrague", "Filtro", "Pastillas", "Bujía", "Correa",
                       "Amortiguador", "Líquido", "Radiador", "Repuestos", "Autopartes", "Caribe", "Cibao", "Cajas"],
        "mapa_fijo": {"localhost:3001": "api.germiva.com", "localhost:4200": "germiva.com"},
    },
    "portada_s": 6,
}


def r(sel, al_decir, ms=4000, cursor=False):
    return {"resaltar": sel, "durante_ms": ms, "al_decir": al_decir, "cursor": cursor}


def c(sel, al_decir):
    return {"click": sel, "al_decir": al_decir}


def cartel(tipo, titulo, texto, al_decir, ms=7000):
    return {"cartel": {"tipo": tipo, "titulo": titulo, "texto": texto}, "durante_ms": ms, "al_decir": al_decir}


def subir(archivo, al_decir):
    return {"subir": {"sel": f"{D} input[type='file']", "archivo": f"seeds/existencias/archivos/{archivo}",
                      "ancla": f"{D} button:has-text('Elegir archivo y revisar')"}, "al_decir": al_decir}


def campo(etiqueta):
    return f"{D} mat-form-field:has-text('{etiqueta}')"


def seg(texto):
    return f"{D} .gm-seg button:has-text('{texto}')"


def fila(producto, col):
    """Celda de la tabla de la vista previa (2 producto · 4 hoy · 5 queda en · 6 movimiento · 8 valor · 9 estado)."""
    return f"{D} .sbu-table--plan tbody tr:has-text('{producto}') td:nth-child({col})"


ABRIR_EXISTENCIAS = [
    c("nav.module-rail [aria-label='Inventario']", "Entro a Inventario"),
    c(".panel-item:has-text('Existencias')", "abro Existencias"),
]

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
V1 = {
    "titulo": "Existencias · Parte 1: inventario inicial",
    "descripcion": "Primera parte de la serie de cargas masivas de existencias de Germiva ERP. Repuestos Germiva, una "
                   "importadora que empieza a usar el sistema, carga de una vez la existencia de su Almacén Central: "
                   "descarga la plantilla, la llena en Excel, elige el motivo Inventario inicial y la referencia, revisa "
                   "la vista previa con el asiento contra el patrimonio de apertura y la aplica.",
    "_comentario": "Serie Existencias, video 1. Estado A: siete repuestos sin existencia, inventario inicial abierto. "
                   "El archivo inicial-central.xlsx lo genera restaurar.mjs A desde la plantilla real.",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs A"},
    "aprenderas": [
        "Descargar la plantilla de existencias de un almacén",
        "Llenar la cantidad a ingresar y el costo sin ITBIS",
        "Elegir el motivo Inventario inicial y escribir la referencia",
        "Leer la vista previa y el asiento antes de aplicar",
        "Saber dónde queda el proveedor: no en la carga, sino en la ficha y en la recepción",
    ],
    "errores_comunes": [
        "Registrar el mismo inventario también en el Balance Inicial: quedaría duplicado",
        "Cargar como inventario inicial una compra a un proveedor: las compras entran por la recepción",
        "Escribir el costo con ITBIS: el costo de la plantilla va sin ITBIS",
    ],
    "pasos": [
        {
            "id": "01-existencias", "capitulo": "La pantalla de Existencias", "rotulo": "Existencias",
            "ruta": "Inventario › Existencias",
            "texto_pantalla": "Existencias · los repuestos, todos en cero",
            "narracion": "Esta es Repuestos Germiva, una importadora de repuestos que empieza a usar Germiva. Entro a "
                         "Inventario y abro Existencias. Cada fila es un repuesto, con lo disponible y lo reservado. "
                         "Recojo el panel. Hoy todos están sin stock: la mercancía está en los almacenes, pero todavía "
                         "no en el sistema. Solo en el Almacén Central hay mil doscientos filtros de aceite, cuatrocientos "
                         "juegos de pastillas de freno y dos mil quinientas bujías. Escribirlos uno por uno sería lento y "
                         "fácil de equivocar. Para eso está Actualizar existencias: una plantilla de Excel que se llena y "
                         "se sube de una vez.",
            "acciones": ABRIR_EXISTENCIAS + [
                r("table tbody tr:has-text('Filtro de aceite') td:nth-child(1)", "Cada fila es un repuesto", 3500),
                c("button.panel-collapse", "Recojo el panel"),
                r("table tbody tr:has-text('Filtro de aceite') td:nth-child(4)", "sin stock", 4000),
                r("table tbody tr:has-text('Filtro de aceite') td:nth-child(1)", "mil doscientos filtros", 1700),
                r("table tbody tr:has-text('Pastillas de freno') td:nth-child(1)", "cuatrocientos", 2200),
                r("table tbody tr:has-text('Bujía de iridio') td:nth-child(1)", "dos mil quinientas", 2200),
                r("button:has-text('Actualizar existencias')", "Para eso está", 5000),
            ],
        },
        {
            "id": "02-plantilla", "capitulo": "Descargar la plantilla", "rotulo": "Paso 1 · la plantilla",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Descarga la plantilla · un almacén, todos los productos",
            "narracion": "Para empezar, pulso Actualizar existencias. El diálogo tiene dos pasos, y el primero es descargar la "
                         "plantilla. Elijo qué voy a hacer: Entrada, que suma lo que escriba a lo que ya hay. El conteo "
                         "físico lo vemos en otro video. Como la empresa tiene dos almacenes, cargo uno a la vez: elijo Un "
                         "almacén, y en la lista, el Almacén Central. En productos dejo Todos: los que tienen existencia y los que no. Ahora descargo la plantilla. El "
                         "Excel trae cada repuesto con su código, su nombre y la existencia de hoy. Yo lleno dos columnas: "
                         "la cantidad a ingresar y el costo unitario, sin ITBIS, es decir, sin el impuesto. Las filas que dejo vacías no se tocan. "
                         "Fíjate que no hay columna de proveedor: el inventario con el que empiezas no es una compra. Lo "
                         "que se le compre a Autopartes del Caribe entra por la recepción, con su factura.",
            "acciones": [
                c("button:has-text('Actualizar existencias')", "Pulso Actualizar existencias"),
                r(f"{D} section.sbu-panel:has(#sbu-step-1)", "el primero es descargar", 3500),
                r(seg("Entrada (sumar)"), "Entrada, que suma", 4000),
                c(seg("Un almacén"), "elijo Un almacén"),
                c(f"{campo('Almacén a exportar')} mat-select", "en la lista"),
                c("mat-option:has-text('Almacén Central')", "el Almacén Central"),
                c(f"{D} .gm-seg button:text-is('Todos')", "dejo Todos"),
                c(f"{D} button:has-text('Descargar plantilla')", "descargo la plantilla"),
                cartel("consejo", "Lo que llenas en el Excel",
                       "cantidad_a_ingresar y costo_unitario, sin ITBIS. Una fila vacía no se toca.",
                       "Yo lleno dos columnas", 8000),
                cartel("cuidado", "¿Y el proveedor?",
                       "La carga no lo pide: no es una compra. Lo que se le compra a un proveedor entra por la "
                       "recepción, con su factura y su 606.", "no hay columna de proveedor", 9000),
            ],
        },
        {
            "id": "03-motivo", "capitulo": "Motivo, referencia y asiento", "rotulo": "Paso 2 · motivo y referencia",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Sube el archivo · motivo Inventario inicial",
            "narracion": "Ya llené el Excel. Voy al segundo paso: subir el archivo. Primero, el motivo de la carga. "
                         "Elijo Inventario inicial. Debajo dice lo que significa: son las existencias con las que la "
                         "empresa empieza, y se asientan contra el patrimonio de apertura, solo mientras el inventario "
                         "inicial esté abierto. Escribo la referencia: Inventario inicial Almacén Central. Motivo y "
                         "referencia son obligatorios y quedan en cada movimiento y en el asiento. En el asiento contable "
                         "dejo Un solo asiento, que es lo recomendado: una línea por cuenta para toda la carga. Elijo el "
                         "archivo y pido revisarlo. Todavía no se aplica nada.",
            "acciones": [
                r(f"{D} section.sbu-panel:has(#sbu-step-2)", "subir el archivo", 3000),
                c(f"{campo('Motivo de la carga')} mat-select", "el motivo de la carga"),
                c("mat-option:has-text('Inventario inicial')", "Elijo Inventario inicial"),
                r(f"{campo('Motivo de la carga')} + p", "Debajo dice", 7000),
                {"escribir": {"sel": f"{campo('Referencia o detalle')} input", "texto": "Inventario inicial Almacén Central"},
                 "al_decir": "Escribo la referencia"},
                r(f"{D} .gm-seg:has(button:has-text('Un solo asiento'))", "Un solo asiento", 5000),
                subir("inicial-central.xlsx", "Elijo el archivo"),
                r(f"{D} .sbu-context", "Todavía no se aplica nada", 2500),
            ],
        },
        {
            "id": "04-vista-previa", "capitulo": "La vista previa y el asiento", "rotulo": "Vista previa",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Vista previa · lo que cambia y el asiento, antes de aplicar",
            "narracion": "Esta es la vista previa: lo que va a pasar con cada fila, antes de aplicar. Arriba, el "
                         "resumen: entran tres productos, por setecientos diecinueve mil quinientos pesos. Las otras "
                         "cuatro filas no se tocan, porque las dejé vacías, y no hay errores. Debajo está el asiento que "
                         "se generará: débito a Inventario de mercancías y crédito a la cuenta de apertura del inventario, "
                         "por el mismo importe. Si algo impidiera registrarlo, lo diría aquí y la carga no se podría "
                         "aplicar. Más abajo, el detalle. Filtro las que se aplican. Cada fila dice cuánto hay hoy, en "
                         "cuánto queda y el valor que entra. Todo cuadra: aplico los tres cambios. La carga corre en segundo "
                         "plano, con su barra de progreso.",
            "acciones": [
                r(f"{D} .sbu-context", "Esta es la vista previa", 2500),
                r(f"{D} .sbu-stats .gm-stat:has-text('Entran')", "entran tres productos", 3800),
                r(f"{D} .sbu-stats .gm-stat:has-text('No se tocan')", "no se tocan", 4000),
                r(f"{D} .sbu-posting", "el asiento que se generará", 9000),
                c(f"{D} .sbu-toolbar button:has-text('Se aplican')", "Filtro las que se aplican"),
                r(fila("Bujía de iridio", 5), "en cuánto queda", 1200),
                r(fila("Bujía de iridio", 8), "el valor que entra", 1800),
                c(f"{D} button:has-text('Aplicar 3 cambios')", "aplico los tres cambios"),
                r(D, "segundo plano", 2500),
            ],
        },
        {
            "id": "05-resultado", "capitulo": "Resultado e inventario inicial abierto", "rotulo": "Resultado",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Resultado · asiento registrado e inventario inicial abierto",
            "narracion": "Existencias actualizadas: tres productos. Con pocos productos termina enseguida; con miles, "
                         "puedes cerrar la ventana y volver luego. El asiento quedó "
                         "registrado por setecientos diecinueve mil quinientos pesos, con el motivo y la referencia, y "
                         "desde aquí puedes abrirlo. La Sucursal Santiago se carga igual, con su propia plantilla. Pulso "
                         "Nueva actualización. Abajo queda el historial de cargas, y el aviso de inventario inicial "
                         "abierto. Mientras esté abierto, puedes seguir cargando como inventario inicial. Cuando termines "
                         "de cargar todo lo que traes, lo cierras con este botón. Eso, y qué hacer si te quedó mercancía "
                         "fuera, lo vemos en el próximo video.",
            "acciones": [
                r(f"{D} .gm-dialog-alert--success:has-text('Existencias actualizadas')", "Existencias actualizadas", 4000),
                r(f"{D} .gm-dialog-alert--success:has-text('Asiento')", "El asiento quedó registrado", 6000),
                r(f"{D} button:has-text('Ver asiento')", "puedes abrirlo", 3000),
                c(f"{D} button:has-text('Nueva actualización')", "Pulso Nueva actualización"),
                r(f"{D} .sbu-history", "el historial de cargas", 2500),
                r(f"{D} .sbu-phase", "inventario inicial abierto", 7000),
                r(f"{D} .sbu-phase button:has-text('Cerrar inventario inicial')", "con este botón", 4000),
            ],
        },
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
V2 = {
    "titulo": "Existencias · Parte 2: mercancía que quedó fuera de la carga inicial",
    "descripcion": "Segunda parte de la serie de cargas masivas de existencias de Germiva ERP. A Repuestos Germiva se le "
                   "quedó un estante por contar en la carga inicial. Con la plantilla «Sin existencia» descarga solo lo "
                   "que está en cero, lo carga como inventario inicial porque la fase sigue abierta, y al terminar cierra "
                   "el inventario inicial. Qué hacer si ya estaba cerrado.",
    "_comentario": "Serie Existencias, video 2. Estado B: Central con filtros, pastillas y bujías; Santiago cargado; "
                   "faltan la correa y el amortiguador en el Central. Archivo complemento-central.xlsx (plantilla "
                   "«Sin existencia» del Central).",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs B"},
    "aprenderas": [
        "Descargar la plantilla solo con los productos sin existencia",
        "Cargar lo que faltó como inventario inicial mientras la fase está abierta",
        "Cerrar el inventario inicial cuando ya cargaste todo",
        "Qué motivo usar si la fase ya está cerrada",
    ],
    "errores_comunes": [
        "Buscar entre miles de filas lo que faltó en vez de usar «Sin existencia»",
        "Olvidar que un producto que ya tiene existencia no sale en «Sin existencia»: va con la plantilla «Todos»",
        "Cerrar el inventario inicial antes de terminar de cargar: no se reabre desde la pantalla",
    ],
    "pasos": [
        {
            "id": "01-el-caso", "capitulo": "El estante que no se contó", "rotulo": "El caso",
            "ruta": "Inventario › Existencias",
            "texto_pantalla": "Existencias · faltan la correa y el amortiguador",
            "narracion": "Seguimos con Repuestos Germiva. Entro a Inventario y abro Existencias. En el video anterior "
                         "cargamos el inventario inicial del Almacén Central, y la Sucursal Santiago se cargó igual. "
                         "Recojo el panel. Pero al revisar, el encargado del Central se dio cuenta de que el estante de "
                         "correas y amortiguadores no se contó. El amortiguador está sin stock, y la correa de distribución "
                         "solo tiene lo de Santiago. Como el inventario inicial sigue abierto, esa mercancía todavía puede "
                         "entrar como inventario inicial, contra el patrimonio de apertura. Abro Actualizar existencias.",
            "acciones": ABRIR_EXISTENCIAS + [
                c("button.panel-collapse", "Recojo el panel"),
                r("table tbody tr:has-text('Amortiguador delantero') td:nth-child(4)", "El amortiguador está sin stock", 2500),
                r("table tbody tr:has-text('Correa de distribución') td:nth-child(2)", "solo tiene lo de", 4000),
                c("button:has-text('Actualizar existencias')", "Abro Actualizar existencias"),
            ],
        },
        {
            "id": "02-sin-existencia", "capitulo": "La plantilla «Sin existencia»", "rotulo": "Productos sin existencia",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Descarga la plantilla · solo los productos sin existencia",
            "narracion": "Como en el video anterior, dejo Entrada, para sumar. Elijo Un almacén, y en la lista de "
                         "almacenes, el Almacén Central. Ahora viene lo nuevo. En Productos elijo Sin existencia: la "
                         "plantilla trae solo lo que en ese almacén está en cero o en negativo. Con miles de productos, así "
                         "no tienes que buscar entre todas las filas lo que faltó. Descargo la plantilla y lleno solo la "
                         "correa y el amortiguador, con su costo. Ojo con un caso: si a un producto que ya tiene existencia "
                         "le faltaron unidades, ese no sale en esta plantilla. Para él descargas la de Todos y escribes "
                         "solo las unidades que faltan.",
            "acciones": [
                r(seg("Entrada (sumar)"), "dejo Entrada", 3000),
                c(seg("Un almacén"), "Elijo Un almacén"),
                c(f"{campo('Almacén a exportar')} mat-select", "en la lista"),
                c("mat-option:has-text('Almacén Central')", "el Almacén Central"),
                c(seg("Sin existencia"), "elijo Sin existencia"),
                r(f"{D} .gm-seg:has(button:has-text('Sin existencia')) + p", "solo lo que en ese almacén", 6000),
                c(f"{D} button:has-text('Descargar plantilla')", "Descargo la plantilla"),
                cartel("consejo", "¿Ya tenía existencia?",
                       "No sale en «Sin existencia». Descarga la plantilla «Todos» y escribe solo las unidades que faltaron.",
                       "Ojo con un caso", 9000),
            ],
        },
        {
            "id": "03-cargar", "capitulo": "Cargar lo que faltó", "rotulo": "Motivo y vista previa",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Inventario inicial · la correa y el amortiguador",
            "narracion": "Ya llené el Excel. Ahora, el segundo paso. Abro el motivo de la carga: sigue siendo "
                         "Inventario inicial, porque es mercancía que la empresa ya tenía al empezar. En la referencia "
                         "escribo: Complemento del inventario inicial, estante de correas. Esa referencia queda en el "
                         "asiento y en cada movimiento. Subo el archivo. En la vista previa entran dos productos por ciento "
                         "sesenta y siete mil pesos, y las otras dos filas de la plantilla no se tocan. El asiento es el "
                         "mismo del inventario inicial: débito a Inventario y crédito a la cuenta de apertura. Filtro las "
                         "que se aplican: sesenta correas y cuarenta amortiguadores, con su costo. Todo cuadra, así que "
                         "aplico los dos cambios. Corre en segundo plano, con su barra de progreso.",
            "acciones": [
                c(f"{campo('Motivo de la carga')} mat-select", "Abro el motivo"),
                c("mat-option:has-text('Inventario inicial')", "Inventario inicial, porque"),
                {"escribir": {"sel": f"{campo('Referencia o detalle')} input",
                              "texto": "Complemento del inventario inicial: estante de correas"},
                 "al_decir": "En la referencia"},
                subir("complemento-central.xlsx", "Subo el archivo"),
                r(f"{D} .sbu-stats .gm-stat:has-text('Entran')", "entran dos productos", 4000),
                r(f"{D} .sbu-posting", "El asiento es el mismo", 7000),
                c(f"{D} .sbu-toolbar button:has-text('Se aplican')", "Filtro las"),
                r(fila("Correa de distribución", 6), "sesenta correas", 1300),
                r(fila("Amortiguador delantero", 6), "cuarenta amortiguadores", 2000),
                c(f"{D} button:has-text('Aplicar 2 cambios')", "aplico los dos cambios"),
                r(D, "segundo plano", 2500),
            ],
        },
        {
            "id": "04-cerrar", "capitulo": "Cerrar el inventario inicial", "rotulo": "Cerrar inventario inicial",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Cerrar inventario inicial · desde aquí, toda carga es un ajuste",
            "narracion": "Listo: el asiento quedó registrado. Ya está todo lo que la empresa traía, así que es momento "
                         "de cerrar el inventario inicial. Pulso Nueva actualización y, abajo, Cerrar inventario "
                         "inicial. El aviso explica lo que pasa: desde ahora toda carga se registra como ajuste, ganancia "
                         "o pérdida, nunca más como inventario inicial, y no se reabre desde aquí. Confirmo. El aviso "
                         "ahora dice cerrado, con la fecha y quién lo cerró. Si abro el motivo, Inventario inicial ya no "
                         "se puede elegir. Si más adelante aparece mercancía que debió entrar al empezar, usa Corrección "
                         "de error de registro: entra como ajuste y llega a los resultados del período, así que, si el "
                         "monto es importante, coordínalo antes con tu contador.",
            "acciones": [
                r(f"{D} .gm-dialog-alert--success:has-text('Asiento')", "el asiento quedó registrado", 3500),
                c(f"{D} button:has-text('Nueva actualización')", "Pulso Nueva actualización"),
                c(f"{D} .sbu-phase button:has-text('Cerrar inventario inicial')", "abajo, Cerrar inventario"),
                r("mat-dialog-container:has-text('Sí, cerrar')", "El aviso explica", 9000),
                c("mat-dialog-container button:has-text('Sí, cerrar')", "Confirmo"),
                r(f"{D} .sbu-phase", "ahora dice cerrado", 4500),
                c(f"{campo('Motivo de la carga')} mat-select", "Si abro el motivo"),
                r("mat-option:has-text('Inventario inicial')", "ya no se puede elegir", 3500),
                r("mat-option:has-text('Corrección de error de registro')", "usa Corrección", 3500),
                {"presionar": {"tecla": "Escape"}, "al_decir": "entra como ajuste"},
                cartel("cuidado", "Fase cerrada", "Lo que aparezca después entra como ajuste y va a resultados. "
                       "Si el monto es importante, coordínalo con tu contador.", "llega a los resultados", 8000),
            ],
        },
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
V3 = {
    "titulo": "Existencias · Parte 3: conteo físico",
    "descripcion": "Tercera parte de la serie de cargas masivas de existencias de Germiva ERP. Repuestos Germiva cuenta la "
                   "Sucursal Santiago y deja el sistema igual a lo contado: plantilla de conteo con los productos con "
                   "existencia, sobrantes y faltantes en la vista previa, la confirmación de lo que queda en cero y un "
                   "solo asiento con la ganancia y la pérdida por ajuste.",
    "_comentario": "Serie Existencias, video 3. Estado C (fase cerrada). Archivo conteo-santiago.xlsx exportado de la "
                   "plantilla de conteo de Santiago: correa 60→62, bujía 500→488, filtro 40→0, pastillas 150 sin cambio.",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs C"},
    "aprenderas": [
        "Descargar la plantilla de conteo justo al empezar a contar",
        "Leer sobrantes, faltantes y filas que no cambian",
        "Confirmar los productos que quedan en cero",
        "Entender el asiento: ganancia y pérdida por ajuste en un solo asiento",
    ],
    "errores_comunes": [
        "Exportar la plantilla días antes del conteo: lo vendido en medio se marca como movido",
        "Escribir cero en lo que no se contó: la fila vacía no se toca, el cero sí",
        "Contar menos de lo reservado por pedidos pendientes: primero despáchalos o libéralos",
    ],
    "pasos": [
        {
            "id": "01-plantilla-conteo", "capitulo": "La plantilla de conteo", "rotulo": "Plantilla de conteo",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Conteo físico · Sucursal Santiago, productos con existencia",
            "narracion": "Hoy toca el conteo anual de la tienda de Santiago. Entro a Inventario y abro Existencias. "
                         "Primero recojo el panel, para ver mejor. La idea es que el sistema quede igual a lo que se contó. Pulso "
                         "Actualizar existencias y elijo Conteo físico: aquí no escribes lo que entra, sino lo que "
                         "contaste, y la existencia queda en esa cantidad. Un conteo se hace por almacén. Elijo Un almacén, "
                         "y en la lista de almacenes, la Sucursal Santiago. Fíjate que Productos cambió solo a Con "
                         "existencia, que es lo normal para contar. Descargo la plantilla justo al empezar a contar: guarda "
                         "la existencia de este momento. En el Excel escribes lo contado en existencia contada, y dejas "
                         "vacío lo que no contaste.",
            "acciones": ABRIR_EXISTENCIAS + [
                c("button.panel-collapse", "recojo el panel"),
                c("button:has-text('Actualizar existencias')", "Pulso"),
                c(seg("Conteo físico (fijar)"), "elijo Conteo físico"),
                c(seg("Un almacén"), "Elijo Un almacén"),
                c(f"{campo('Almacén a exportar')} mat-select", "en la lista"),
                c("mat-option:has-text('Sucursal Santiago')", "la Sucursal Santiago"),
                r(f"{D} .gm-seg:has(button:has-text('Sin existencia'))", "Productos cambió solo", 5000),
                c(f"{D} button:has-text('Descargar plantilla')", "Descargo la"),
                cartel("consejo", "Vacía no es cero",
                       "Escribe lo contado en existencia_contada. Una fila vacía no se toca; un cero deja el producto en cero.",
                       "En el Excel escribes", 8000),
            ],
        },
        {
            "id": "02-subir-conteo", "capitulo": "Motivo y archivo", "rotulo": "Motivo Conteo físico",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Motivo Conteo físico · referencia del conteo",
            "narracion": "Ya terminamos de contar y llenamos el Excel. Abro el motivo de la carga, y de la lista elijo "
                         "Conteo físico: los sobrantes se registran como ganancia y los faltantes como pérdida por ajuste. "
                         "En la referencia escribo: Conteo anual 2026, Sucursal Santiago. Así, quien vea el asiento sabe "
                         "de dónde salió. Subo el archivo con lo contado.",
            "acciones": [
                c(f"{campo('Motivo de la carga')} mat-select", "Abro el motivo"),
                c("mat-option:has-text('Conteo físico')", "elijo Conteo físico"),
                {"escribir": {"sel": f"{campo('Referencia o detalle')} input", "texto": "Conteo anual 2026, Sucursal Santiago"},
                 "al_decir": "En la referencia escribo"},
                subir("conteo-santiago.xlsx", "Subo el archivo"),
            ],
        },
        {
            "id": "03-vista-previa-conteo", "capitulo": "Sobrantes, faltantes y ceros", "rotulo": "Vista previa del conteo",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Vista previa · sobrantes, faltantes y lo que queda en cero",
            "narracion": "La vista previa compara lo contado con lo que había al exportar. Entra un producto: sobraron "
                         "dos correas. Salen dos: faltan doce bujías, y los cuarenta filtros no aparecieron. Las pastillas "
                         "se contaron iguales, así que no se tocan. Debajo, un solo asiento con las dos patas: la ganancia "
                         "por ajuste de lo que sobró, y la pérdida por ajuste de lo que faltó. Las salidas se ven al costo "
                         "promedio de hoy; al aplicar se usa el costo exacto de cada lote. Dejar un producto en cero pide "
                         "confirmarlo. Filtro Con aviso: el filtro de aceite quedará en cero, tenía cuarenta. Lo "
                         "verificamos en el almacén, así que lo confirmo. Si un producto se vendiera después de exportar, "
                         "el sistema lo marcaría y, por omisión, no lo tocaría. Aplico los tres cambios. Corre en segundo "
                         "plano, con su barra de progreso.",
            "acciones": [
                r(f"{D} .sbu-stats .gm-stat:has-text('Entran')", "Entra un producto", 1400),
                r(f"{D} .sbu-stats .gm-stat:has-text('Salen')", "Salen dos", 3500),
                r(f"{D} .sbu-stats .gm-stat:has-text('No se tocan')", "no se tocan", 1100),
                r(f"{D} .sbu-posting", "un solo asiento con las dos patas", 11000),
                c(f"{D} .sbu-toolbar button:has-text('Con aviso')", "Filtro Con aviso"),
                r(fila("Filtro de aceite", 9), "quedará en cero", 4000),
                c(f"{D} mat-checkbox:has-text('Confirmo que deben quedar en cero')", "lo confirmo"),
                cartel("consejo", "Movidos después de exportar",
                       "Si un producto se vende o se compra después de bajar la plantilla, se marca y por omisión no se toca.",
                       "Si un producto se vendiera", 7000),
                c(f"{D} button:has-text('Aplicar 3 cambios')", "Aplico los tres cambios"),
                r(D, "segundo plano", 2500),
            ],
        },
        {
            "id": "04-resultado-conteo", "capitulo": "Resultado y asiento", "rotulo": "Resultado del conteo",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Resultado · el conteo aplicado y su asiento",
            "narracion": "Existencias actualizadas: tres productos. Salidas por ocho mil quinientos cuarenta pesos y "
                         "entradas por dos mil quinientos. El asiento quedó registrado con el motivo y la referencia del "
                         "conteo. Pulso Ver asiento. Aquí está, en Contabilidad, con sus cuatro líneas: la ganancia y la "
                         "pérdida por ajuste contra la cuenta de inventario. Ahora la Sucursal Santiago tiene en el "
                         "sistema exactamente lo que se contó.",
            "acciones": [
                r(f"{D} .gm-dialog-alert--success:has-text('Existencias actualizadas')", "Existencias actualizadas", 1200),
                r(f"{D} .sbu-stats .gm-stat:has-text('Salidas')", "Salidas por", 3500),
                r(f"{D} .gm-dialog-alert--success:has-text('Asiento')", "El asiento quedó registrado", 4000),
                c(f"{D} button:has-text('Ver asiento')", "Pulso Ver asiento"),
                r("table tbody tr:first-child td:nth-child(1)", "con sus cuatro líneas", 6000),
            ],
        },
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
V4 = {
    "titulo": "Existencias · Parte 4: sobrante encontrado",
    "descripcion": "Cuarta parte de la serie de cargas masivas de existencias de Germiva ERP. Al reorganizar el Almacén "
                   "Central aparecen cajas de bujías y filtros que no estaban registrados. Se cargan con el motivo "
                   "Sobrante encontrado, que se asienta como ganancia por ajuste. Cuándo no es un sobrante sino una "
                   "compra a un proveedor, y cómo quedan los movimientos.",
    "_comentario": "Serie Existencias, video 4. Estado C. Archivo sobrante-central.xlsx: bujías +36, filtros +10.",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs C"},
    "aprenderas": [
        "Elegir entre los cuatro motivos de carga",
        "Cargar un sobrante con el motivo Sobrante encontrado",
        "Leer el asiento de ganancia por ajuste",
        "Distinguir un sobrante de una compra a un proveedor",
    ],
    "errores_comunes": [
        "Cargar como sobrante mercancía de un proveedor que no se ha recibido: es una compra",
        "Usar Sobrante encontrado en un conteo: ahí los sobrantes ya van con el motivo Conteo físico",
    ],
    "pasos": [
        {
            "id": "01-sobrante", "capitulo": "Apareció mercancía", "rotulo": "El sobrante",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Entrada · Almacén Central, todos los productos",
            "narracion": "Seguimos con Repuestos Germiva. Entro a Inventario y abro Existencias. Ahora recojo el panel. Al reorganizar el pasillo B del Almacén "
                         "Central aparecieron tres cajas de bujías, treinta y seis unidades, y diez filtros de aceite que "
                         "no estaban registrados. Antes de cargarlos, una pregunta: ¿vienen de un proveedor? Si son de un "
                         "pedido que todavía no se ha recibido, no son un sobrante, son una compra, y van por la recepción, "
                         "a nombre de ese proveedor. Aquí no: llevan tiempo en el almacén. Pulso Actualizar existencias. "
                         "Dejo Entrada, para sumar. Elijo Un almacén, y en la lista de almacenes, el Almacén Central. Ahora "
                         "descargo la plantilla con todos los productos, y en el Excel escribo solo lo que apareció.",
            "acciones": ABRIR_EXISTENCIAS + [
                c("button.panel-collapse", "recojo el panel"),
                r("table tbody tr:has-text('Bujía de iridio') td:nth-child(1)", "tres cajas de bujías", 2500),
                r("table tbody tr:has-text('Filtro de aceite') td:nth-child(1)", "diez filtros", 2500),
                cartel("cuidado", "¿Viene de un proveedor?",
                       "Si es de un pedido que no se ha recibido, es una compra: va por la recepción, con su factura y su 606.",
                       "vienen de un proveedor", 9000),
                c("button:has-text('Actualizar existencias')", "Pulso Actualizar existencias"),
                r(seg("Entrada (sumar)"), "Dejo Entrada", 2500),
                c(seg("Un almacén"), "Elijo Un almacén"),
                c(f"{campo('Almacén a exportar')} mat-select", "en la lista"),
                c("mat-option:has-text('Almacén Central')", "el Almacén Central"),
                c(f"{D} button:has-text('Descargar plantilla')", "descargo la plantilla"),
            ],
        },
        {
            "id": "02-motivo-sobrante", "capitulo": "Los cuatro motivos", "rotulo": "Motivo Sobrante encontrado",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Los motivos de una carga · Sobrante encontrado",
            "narracion": "Ya llené el Excel. Abro el motivo de la carga para verlos todos. Inventario inicial está "
                         "deshabilitado, porque ya se cerró. Conteo físico es para las diferencias al contar. Corrección "
                         "de error de registro, para cantidades mal registradas antes. Y Sobrante encontrado, para "
                         "mercancía que apareció sin estar registrada: solo existe para archivos de entrada. Lo elijo. En "
                         "la referencia escribo: Cajas encontradas al reorganizar el pasillo B. Así queda explicado en el "
                         "asiento y en cada movimiento. Subo el archivo.",
            "acciones": [
                c(f"{campo('Motivo de la carga')} mat-select", "Abro el motivo"),
                r("mat-option:has-text('Inventario inicial')", "Inventario inicial está deshabilitado", 2500),
                r("mat-option:has-text('Conteo físico')", "Conteo físico es para", 2500),
                r("mat-option:has-text('Corrección de error de registro')", "Corrección de error", 2500),
                r("mat-option:has-text('Sobrante encontrado')", "Y Sobrante encontrado", 3500),
                c("mat-option:has-text('Sobrante encontrado')", "Lo elijo"),
                {"escribir": {"sel": f"{campo('Referencia o detalle')} input",
                              "texto": "Cajas encontradas al reorganizar el pasillo B"}, "al_decir": "la referencia escribo"},
                subir("sobrante-central.xlsx", "Subo el archivo"),
            ],
        },
        {
            "id": "03-aplicar-sobrante", "capitulo": "Vista previa y resultado", "rotulo": "Ganancia por ajuste",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Vista previa · ganancia por ajuste de inventario",
            "narracion": "Entran dos productos por cinco mil doscientos setenta pesos: treinta y seis bujías a noventa y "
                         "cinco, y diez filtros a ciento ochenta y cinco, su costo de siempre. Las demás filas no se tocan. "
                         "En el asiento, débito a Inventario y crédito a otros ingresos por ajuste de inventario. Es una "
                         "ganancia, porque la empresa tiene más de lo que creía. Aplico los dos cambios. El asiento quedó "
                         "registrado, con su motivo y su referencia.",
            "acciones": [
                r(f"{D} .sbu-stats .gm-stat:has-text('Entran')", "Entran dos productos", 5000),
                r(f"{D} .sbu-stats .gm-stat:has-text('No se tocan')", "Las demás filas", 1500),
                r(f"{D} .sbu-posting", "En el asiento", 8000),
                c(f"{D} button:has-text('Aplicar 2 cambios')", "Aplico los dos cambios"),
                r(f"{D} .gm-dialog-alert--success:has-text('Asiento')", "quedó registrado", 5000),
            ],
        },
        {
            "id": "04-movimientos", "capitulo": "Los movimientos, sin proveedor", "rotulo": "Movimientos",
            "ruta": "Inventario › Movimientos",
            "texto_pantalla": "Movimientos · la nota de la carga y sin proveedor",
            "narracion": "Desde el resultado también puedes ir a los movimientos. Pulso Ver movimientos. Cada producto dejó su movimiento de entrada, y la nota dice de qué carga "
                         "salió, en qué fila del archivo, el motivo y la referencia. Fíjate que no tiene proveedor: un "
                         "sobrante no se le compró a nadie. Por eso tampoco genera cuenta por pagar ni entra al 606. La "
                         "entrada recalcula el costo promedio, pero no cambia el último precio de compra del producto: ese "
                         "solo lo mueve una compra.",
            "acciones": [
                c(f"{D} button:has-text('Ver movimientos')", "Pulso Ver movimientos"),
                r("table tbody tr:first-child td:nth-child(2)", "Cada producto dejó", 3000),
                r("table tbody tr:first-child td:nth-child(3)", "la nota dice", 5000),
                cartel("consejo", "¿Dónde queda el proveedor?",
                       "En las compras: la recepción y la factura lo llevan, con su cuenta por pagar y su 606.",
                       "no tiene proveedor", 8000),
            ],
        },
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
V5 = {
    "titulo": "Existencias · Parte 5: corregir una cantidad mal registrada",
    "descripcion": "Quinta parte de la serie de cargas masivas de existencias de Germiva ERP. En el complemento del "
                   "inventario inicial se digitaron 140 amortiguadores en vez de 40. Con la plantilla de conteo se fija "
                   "la cantidad correcta y el motivo Corrección de error de registro; el faltante se asienta como pérdida "
                   "por ajuste y el asiento lleva la explicación.",
    "_comentario": "Serie Existencias, video 5. Estado D: Central con 140 amortiguadores (error), fase cerrada. "
                   "Archivo correccion-central.xlsx: amortiguador contado 40.",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs D"},
    "aprenderas": [
        "Corregir una cantidad con la plantilla de conteo",
        "Usar el motivo Corrección de error de registro y explicar el error en la referencia",
        "Entender por qué un faltante siempre es pérdida por ajuste",
    ],
    "errores_comunes": [
        "Corregir con una carga un error que está en un documento: va con su devolución o nota de crédito",
        "No anotar en la referencia qué se corrige: después nadie entiende el asiento",
    ],
    "pasos": [
        {
            "id": "01-el-error", "capitulo": "Un cero de más", "rotulo": "El error",
            "ruta": "Inventario › Existencias",
            "texto_pantalla": "Existencias · 140 amortiguadores en lugar de 40",
            "narracion": "En el complemento del inventario inicial alguien escribió ciento cuarenta amortiguadores, y en "
                         "el almacén hay cuarenta: un cero de más. Entro a Inventario y abro Existencias. Ahora recojo el "
                         "panel, para ver la lista completa. El amortiguador dice ciento cuarenta. Para dejarlo en "
                         "cuarenta uso la plantilla de conteo, porque fija la cantidad exacta. Si el error hubiera estado "
                         "en un documento, como una compra o una factura, se corregiría en ese documento, con su "
                         "devolución o su nota de crédito. Abro Actualizar existencias.",
            "acciones": ABRIR_EXISTENCIAS + [
                c("button.panel-collapse", "recojo el"),
                r("table tbody tr:has-text('Amortiguador delantero') td:nth-child(2)", "dice ciento cuarenta", 4500),
                cartel("consejo", "¿El error está en un documento?",
                       "Corrígelo en ese documento, con su devolución o nota de crédito, no con una carga.",
                       "Si el error hubiera estado", 8000),
                c("button:has-text('Actualizar existencias')", "Abro Actualizar"),
            ],
        },
        {
            "id": "02-corregir", "capitulo": "Fijar la cantidad correcta", "rotulo": "Corrección",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Conteo físico · motivo Corrección de error de registro",
            "narracion": "En el primer paso del diálogo, elijo Conteo físico. Luego Un almacén, y en la lista de "
                         "almacenes, el Almacén Central. Dejo Con existencia. Descargo la plantilla, y en el Excel escribo "
                         "cuarenta solo en el amortiguador; las demás filas, vacías, para que no se toquen. El motivo es "
                         "Corrección de error de registro: sirve para cantidades mal registradas antes. Y en la "
                         "referencia explico qué se corrige: Se digitó 140 en lugar de 40 en el complemento. Cualquiera "
                         "que vea el asiento entenderá por qué se hizo. Subo el archivo.",
            "acciones": [
                c(seg("Conteo físico (fijar)"), "elijo Conteo físico"),
                c(seg("Un almacén"), "Luego Un almacén"),
                c(f"{campo('Almacén a exportar')} mat-select", "en la lista"),
                c("mat-option:has-text('Almacén Central')", "el Almacén Central"),
                c(f"{D} button:has-text('Descargar plantilla')", "Descargo la plantilla"),
                c(f"{campo('Motivo de la carga')} mat-select", "El motivo es"),
                c("mat-option:has-text('Corrección de error de registro')", "Corrección de error de registro:"),
                {"escribir": {"sel": f"{campo('Referencia o detalle')} input",
                              "texto": "Se digitó 140 en lugar de 40 en el complemento"}, "al_decir": "explico qué se corrige"},
                subir("correccion-central.xlsx", "Subo el archivo"),
            ],
        },
        {
            "id": "03-vista-previa-correccion", "capitulo": "La pérdida por ajuste", "rotulo": "Pérdida por ajuste",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Vista previa · sale lo que se digitó de más",
            "narracion": "Sale un producto: cien amortiguadores, por doscientos treinta mil pesos al costo. Lo demás no "
                         "se toca. En el asiento, débito a la pérdida por ajuste de inventario y crédito a Inventario. Un "
                         "faltante siempre se registra como pérdida por ajuste, aunque el error venga del inventario "
                         "inicial; si el monto es importante, coordínalo con tu contador. Aplico el cambio. El "
                         "amortiguador queda en cuarenta, y el asiento lleva la referencia que explica el error. Pulso Ver "
                         "asiento: ahí está, con la pérdida y el crédito a inventario.",
            "acciones": [
                r(f"{D} .sbu-stats .gm-stat:has-text('Salen')", "Sale un producto", 5000),
                r(f"{D} .sbu-posting", "En el asiento", 7000),
                cartel("cuidado", "Un faltante es pérdida",
                       "Aunque el error venga del inventario inicial. Si el monto es grande, coordínalo con tu contador.",
                       "Un faltante siempre", 8000),
                c(f"{D} button:has-text('Aplicar 1 cambio')", "Aplico el cambio"),
                r(f"{D} .gm-dialog-alert--success:has-text('Asiento')", "el asiento lleva la referencia", 3500),
                c(f"{D} button:has-text('Ver asiento')", "Pulso Ver"),
                r("table tbody tr:first-child td:nth-child(1)", "con la pérdida", 5000),
            ],
        },
    ],
}

PIS = "app-product-import-stock-step"

V6 = {
    "titulo": "Existencias · Parte 6: productos nuevos con su existencia",
    "descripcion": "Sexta parte de la serie de cargas masivas de existencias de Germiva ERP. Repuestos Germiva crea con la "
                   "importación de productos dos kits de embrague que ya tiene en el almacén: la plantilla lleva la "
                   "existencia, el costo, el almacén y el proveedor habitual (RNC y nombre). Al subirla elige el motivo y "
                   "la referencia, revisa el asiento y la importa.",
    "_comentario": "Serie Existencias, video 6. Estado E (inventario inicial abierto). Archivo productos-nuevos.xlsx: "
                   "KE-500 30 × 4,800 y KE-520 20 × 5,350, proveedor Repuestos del Cibao Germiva (130555302).",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs E"},
    "aprenderas": [
        "Crear productos con su existencia desde la plantilla de productos",
        "Dejar el proveedor habitual con las columnas RNC y nombre del proveedor",
        "Elegir el motivo y revisar el asiento antes de importar",
    ],
    "errores_comunes": [
        "Llenar la columna existencia en un producto que ya existe: se ignora; usa Actualizar existencias",
        "Escribir un tipo de entrada distinto al del motivo: la fila sale con error",
        "Crear con existencia productos que vienen de una compra: créalos sin existencia y recíbelos",
    ],
    "pasos": [
        {
            "id": "01-catalogo", "capitulo": "Productos que no existen", "rotulo": "Productos",
            "ruta": "Inventario › Productos",
            "texto_pantalla": "Productos · el catálogo de Repuestos Germiva",
            "narracion": "Repuestos Germiva trae una línea nueva: kits de embrague, para sedán y para camioneta. Entro a "
                         "Inventario y abro Productos. Ahora recojo el panel. Este es el catálogo, con un repuesto por "
                         "fila. Los kits todavía no están, y ya hay treinta y veinte en el Almacén Central. Para crear "
                         "muchos productos de una vez, con su existencia, se usa Importar o Exportar.",
            "acciones": [
                c("nav.module-rail [aria-label='Inventario']", "Entro a"),
                c(".panel-item:has-text('Productos')", "abro Productos"),
                c("button.panel-collapse", "recojo el panel"),
                r("table tbody tr:has-text('Filtro de aceite') td:nth-child(2)", "un repuesto por", 3500),
                r("button:has-text('Importar / Exportar')", "se usa Importar", 4000),
            ],
        },
        {
            "id": "02-plantilla-productos", "capitulo": "La plantilla, con el proveedor", "rotulo": "Plantilla de productos",
            "ruta": "Inventario › Productos › Importar / Exportar",
            "texto_pantalla": "Plantilla de productos · existencia, costo, almacén y proveedor",
            "narracion": "Desde aquí, abro Importar o Exportar. Primero, la plantilla de Excel: trae una fila por producto, con "
                         "código, nombre, marca, unidad y precio. Este aviso lo dice: para los productos que manejan "
                         "inventario puedes cargar la existencia inicial, y solo se aplica al crear el producto. En cada "
                         "kit lleno la existencia, el costo de compra sin ITBIS, el impuesto, y el almacén. Y aquí sí va el proveedor: "
                         "las columnas RNC del proveedor, su registro de contribuyente, y nombre del proveedor dejan a Repuestos del Cibao como proveedor "
                         "habitual de cada kit; si no existiera, se crearía. La columna tipo de entrada se deja vacía: la "
                         "decide el motivo. Ya llené los dos kits. Selecciono el archivo.",
            "acciones": [
                c("button:has-text('Importar / Exportar')", "abro Importar"),
                r(f"{D} button:has-text('Plantilla Excel')", "la plantilla de Excel", 4000),
                r(f"{D} .callout:has-text('existencia inicial')", "Este aviso lo dice", 7000),
                cartel("consejo", "Existencia, costo y almacén",
                       "Columnas existencia, precio_compra (sin ITBIS) y almacen. Solo cuentan al crear el producto.",
                       "En cada kit lleno", 7000),
                cartel("consejo", "El proveedor habitual",
                       "rnc_proveedor 130555302 y nombre_proveedor Repuestos del Cibao Germiva, SRL. Si no existe, se crea.",
                       "aquí sí va el proveedor", 9000),
                {"subir": {"sel": f"{D} input[type='file']", "archivo": "seeds/existencias/archivos/productos-nuevos.xlsx",
                           "ancla": f"{D} button:has-text('Seleccionar archivo e importar')"}, "al_decir": "Selecciono el archivo"},
            ],
        },
        {
            "id": "03-motivo-asiento", "capitulo": "Motivo y asiento", "rotulo": "Este archivo carga existencia",
            "ruta": "Inventario › Productos › Importar / Exportar",
            "texto_pantalla": "Este archivo carga existencia · motivo, referencia y asiento",
            "narracion": "Como el archivo trae existencia, el diálogo se detiene: este archivo carga existencia. Crea dos "
                         "productos por doscientos cincuenta y un mil pesos, y toda carga de existencia lleva su motivo y "
                         "su asiento. Abro el motivo de la carga y elijo Inventario inicial, porque la empresa todavía está "
                         "cargando lo que trae al empezar. En la referencia escribo: Nueva línea de kits de embrague. Esa referencia queda en el asiento. "
                         "Dejo Un solo asiento. Pulso Revisar el asiento: débito a Inventario y crédito a la cuenta de "
                         "apertura, por el mismo importe. Pulso Importar.",
            "acciones": [
                r(f"{D} {PIS} .pis__lead", "este archivo carga existencia", 6000),
                c(f"{D} {PIS} mat-form-field:has-text('Motivo de la carga') mat-select", "Abro el motivo"),
                c("mat-option:has-text('Inventario inicial')", "elijo Inventario inicial"),
                {"escribir": {"sel": f"{D} {PIS} mat-form-field:has-text('Referencia o detalle') input",
                              "texto": "Nueva línea de kits de embrague"}, "al_decir": "En la referencia escribo"},
                r(f"{D} {PIS} .gm-seg", "Dejo Un solo asiento", 1800),
                c(f"{D} {PIS} button:has-text('Revisar el asiento')", "Pulso Revisar"),
                r(f"{D} {PIS} .pis__table-wrap", "débito a Inventario", 6000),
                c(f"{D} {PIS} button:has-text('Importar')", "Pulso Importar"),
            ],
        },
        {
            "id": "04-resultado-importacion", "capitulo": "Resultado", "rotulo": "Productos creados",
            "ruta": "Inventario › Productos",
            "texto_pantalla": "Resultado · dos productos creados con su existencia y su asiento",
            "narracion": "La importación corre en sus etapas: subir, validar, registrar y finalizar. Listo: dos productos "
                         "creados. Y la existencia quedó registrada con su asiento, que desde aquí puedes abrir. Cierro el "
                         "diálogo. Los dos kits ya están en el catálogo, con su existencia en el Almacén Central y su "
                         "proveedor habitual. Si estos kits vinieran de una compra, lo correcto sería crearlos sin "
                         "existencia y recibirlos con la recepción, a nombre del proveedor.",
            "acciones": [
                r(D, "corre en sus etapas", 2500),
                r(f"{D} .chip.created", "dos productos", 1200),
                r(f"{D} .banner.success", "la existencia quedó registrada", 5000),
                c(f"{D} button:text-is('Cerrar')", "Cierro el"),
                r("table tbody tr:has-text('Kit de embrague sedán') td:nth-child(2)", "Los dos kits", 4000),
                cartel("cuidado", "¿Vienen de una compra?",
                       "Créalos sin existencia y recíbelos con la recepción, a nombre del proveedor.",
                       "Si estos kits vinieran", 8000),
            ],
        },
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
V7 = {
    "titulo": "Existencias · Parte 7: cuando el asiento no se puede registrar",
    "descripcion": "Séptima parte de la serie de cargas masivas de existencias de Germiva ERP. La vista previa avisa que el "
                   "asiento no se puede registrar porque una cuenta del mapeo es agrupadora: la carga no se aplica. Se "
                   "corrige la cuenta en el Mapeo de Cuentas, se vuelve a subir el mismo archivo y se aplica. Qué hacer si "
                   "el asiento queda pendiente después de aplicar.",
    "_comentario": "Serie Existencias, video 7. Estado F: el mapeo «Otros Ingresos por Ajuste de Inventario» apunta a la "
                   "agrupadora 4.02.01.02. Archivo sobrante-central.xlsx.",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs F"},
    "aprenderas": [
        "Leer el aviso de asiento que no se puede registrar",
        "Corregir la cuenta en el Mapeo de Cuentas",
        "Volver a subir el mismo archivo y aplicar",
        "Qué hacer si el asiento queda pendiente después de aplicar",
    ],
    "errores_comunes": [
        "Repetir una carga cuyo asiento quedó pendiente: la existencia ya entró; se usa Reintentar asiento",
        "Asignar una cuenta agrupadora en el mapeo: solo las de detalle admiten movimientos",
    ],
    "pasos": [
        {
            "id": "01-intentar", "capitulo": "La carga del sobrante", "rotulo": "El sobrante",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Actualizar existencias · el sobrante del Almacén Central",
            "narracion": "Vamos a cargar el sobrante del Almacén Central, el mismo del video del sobrante. Entro a "
                         "Inventario y abro Existencias. Primero recojo el panel. Pulso Actualizar existencias. Ya tengo "
                         "el Excel lleno. Abro el motivo de la carga y elijo Sobrante encontrado. En la referencia "
                         "escribo: Cajas encontradas en el pasillo B. Así queda explicada la carga. Elijo el archivo y pido revisarlo.",
            "acciones": ABRIR_EXISTENCIAS + [
                c("button.panel-collapse", "recojo el panel"),
                c("button:has-text('Actualizar existencias')", "Pulso Actualizar"),
                c(f"{campo('Motivo de la carga')} mat-select", "Abro el motivo"),
                c("mat-option:has-text('Sobrante encontrado')", "elijo Sobrante encontrado"),
                {"escribir": {"sel": f"{campo('Referencia o detalle')} input", "texto": "Cajas encontradas en el pasillo B"},
                 "al_decir": "En la referencia"},
                subir("sobrante-central.xlsx", "Elijo el archivo"),
            ],
        },
        {
            "id": "02-bloqueo", "capitulo": "El aviso", "rotulo": "Asiento que no se puede registrar",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "No se puede registrar el asiento · la carga no se aplica",
            "narracion": "Las filas están bien: entran dos productos por cinco mil doscientos setenta pesos. Pero en el "
                         "asiento aparece un aviso en rojo: no se puede registrar el asiento, así que la carga no se puede "
                         "aplicar. Y dice por qué: la cuenta de otros ingresos que tiene el mapeo es agrupadora y no admite "
                         "movimientos; hay que asignar una cuenta de detalle en la configuración contable. Por eso el botón "
                         "de aplicar está deshabilitado: no se movió nada. Las causas pueden ser una cuenta agrupadora o "
                         "inactiva, una configuración que falta o un período cerrado. Cierro el diálogo y voy a "
                         "corregirlo.",
            "acciones": [
                r(f"{D} .sbu-stats .gm-stat:has-text('Entran')", "entran dos productos", 3500),
                r(f"{D} .sbu-posting .gm-dialog-alert--danger", "aparece un aviso en rojo", 12000),
                r(f"{D} button:has-text('Aplicar 2 cambios')", "el botón", 4000),
                cartel("consejo", "Causas posibles",
                       "Cuenta agrupadora o inactiva, configuración contable que falta o período cerrado.",
                       "Las causas pueden ser", 7000),
                c(f"{D} button:has-text('Cancelar')", "Cierro el diálogo"),
            ],
        },
        {
            "id": "03-mapeo", "capitulo": "Corregir la cuenta", "rotulo": "Mapeo de Cuentas",
            "ruta": "Contabilidad › Configuración Contable › Mapeo de Cuentas",
            "texto_pantalla": "Mapeo de Cuentas · Otros Ingresos por Ajuste de Inventario",
            "navegar": "/accounting/configuracion/mapeos", "al_decir_navegar": "Voy al Mapeo",
            "narracion": "Esto lo hace quien lleva la contabilidad. Voy al Mapeo de Cuentas, en la configuración contable: "
                         "aquí cada operación del sistema tiene su cuenta. Busco ajuste de inventario, y la lista se filtra sola. Este rol, otros "
                         "ingresos por ajuste de inventario, apunta a la cuenta agrupadora. Abro su selector, que solo "
                         "ofrece cuentas de detalle, y elijo Otros ingresos diversos, general. Se guarda al instante, y el "
                         "aviso lo confirma.",
            "acciones": [
                {"escribir": {"sel": ".mapping-filters input", "texto": "Ajuste de Inventario"}, "al_decir": "Busco ajuste"},
                r("li.role-row:has(.role-row__label:text-is('Otros Ingresos por Ajuste de Inventario'))",
                  "Este rol", 5000),
                c("li.role-row:has(.role-row__label:text-is('Otros Ingresos por Ajuste de Inventario')) mat-select",
                  "Abro su selector"),
                c("mat-option:has-text('4.02.01.02.01')", "elijo Otros ingresos diversos"),
                r(".mat-mdc-snack-bar-container", "el aviso lo confirma", 3500),
            ],
        },
        {
            "id": "04-reintentar", "capitulo": "El mismo archivo, otra vez", "rotulo": "Volver a subir",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "El mismo archivo · ahora el asiento sí se registra",
            "navegar": "/inventory/existencias", "al_decir_navegar": "Vuelvo a Existencias",
            "narracion": "Ya está corregido. Vuelvo a Existencias y pulso otra vez Actualizar existencias. No hace falta descargar otra "
                         "plantilla: subo el mismo archivo. Abro el motivo y elijo Sobrante encontrado. Escribo la misma "
                         "referencia, para que quede igual que la primera vez en el asiento. Y ahora sí, elijo el archivo. En la vista previa, el asiento sale completo: débito a Inventario y crédito a "
                         "otros ingresos diversos. Aplico los dos cambios, y la carga corre en segundo plano.",
            "acciones": [
                c("button:has-text('Actualizar existencias')", "pulso otra vez"),
                c(f"{campo('Motivo de la carga')} mat-select", "Abro el motivo"),
                c("mat-option:has-text('Sobrante encontrado')", "elijo Sobrante encontrado"),
                {"escribir": {"sel": f"{campo('Referencia o detalle')} input", "texto": "Cajas encontradas en el pasillo B"},
                 "al_decir": "Escribo la misma"},
                subir("sobrante-central.xlsx", "Y ahora sí, elijo el archivo"),
                r(f"{D} .sbu-posting", "el asiento sale completo", 6000),
                c(f"{D} button:has-text('Aplicar 2 cambios')", "Aplico los dos cambios"),
                r(D, "segundo plano", 2500),
            ],
        },
        {
            "id": "05-pendiente", "capitulo": "Si queda pendiente después de aplicar", "rotulo": "Reintentar asiento",
            "ruta": "Inventario › Existencias › Actualizar existencias",
            "texto_pantalla": "Resultado · y qué hacer si el asiento queda pendiente",
            "narracion": "Asiento registrado. Hay un segundo caso, menos común: que algo cambie mientras la carga corre, "
                         "por ejemplo, que alguien cierre el período. Entonces la existencia sí entra, pero el asiento queda "
                         "pendiente, y el resultado lo dice con el botón Reintentar asiento. No repitas la carga: corrige la "
                         "causa y reintenta. Mientras siga pendiente, el diálogo lo avisa arriba y no deja aplicar otra "
                         "carga. Así ninguna carga queda sin su asiento.",
            "acciones": [
                r(f"{D} .gm-dialog-alert--success:has-text('Asiento')", "Asiento registrado", 4000),
                cartel("cuidado", "Asiento pendiente",
                       "La existencia ya entró: no repitas la carga. Corrige la causa y pulsa Reintentar asiento.",
                       "No repitas la carga", 9000),
                r(f"{D} .sbu-stats", "ninguna carga queda", 4000),
            ],
        },
    ],
}

# ═══════════════════════════════════════════════════════════════════════════════════════════════════
V8 = {
    "titulo": "Existencias · Parte 8: recibir un contenedor desde Excel",
    "descripcion": "Octava parte de la serie de cargas masivas de existencias de Germiva ERP. Llega un contenedor de "
                   "Autopartes del Caribe Germiva: la compra entra por una recepción sin orden de compra, con el proveedor "
                   "y el almacén, y las líneas se importan desde Excel. Se guarda, se aprueba y se procesa a inventario; "
                   "la compra queda en el historial del producto a nombre del proveedor.",
    "_comentario": "Serie Existencias, video 8. Estado C. Archivo recepcion-contenedor.xlsx: FA-210 1,800 × 172 y "
                   "PF-88 600 × 610 (675,600 sin ITBIS). Flujo: Guardar → Aprobar Recepción → Procesar a Inventario.",
    "setup": {"tipo": "shell", "cmd": "node seeds/existencias/restaurar.mjs C"},
    "aprenderas": [
        "Por qué una compra entra por la recepción y no por Actualizar existencias",
        "Crear una recepción sin orden de compra con su proveedor y almacén",
        "Importar las líneas de la recepción desde Excel",
        "Aprobar y procesar la recepción a inventario",
        "Ver la compra a nombre del proveedor en el historial del producto",
    ],
    "errores_comunes": [
        "Cargar una compra con Actualizar existencias: se pierden el proveedor, la cuenta por pagar y el 606",
        "Cambiar el almacén después de importar las líneas: pierden la ubicación",
        "Dejar la recepción guardada sin procesarla: la mercancía no entra hasta procesarla a inventario",
    ],
    "pasos": [
        {
            "id": "01-recepcion", "capitulo": "La recepción, con su proveedor", "rotulo": "Recepción sin orden",
            "ruta": "Compras › Recepciones › Crear recepción",
            "texto_pantalla": "Recepción sin orden de compra · proveedor y almacén",
            "navegar": "/purchases/receipts/create", "al_decir_navegar": "abro una recepción",
            "narracion": "En Compras, abro una recepción nueva. Llegó un contenedor de Autopartes del Caribe con filtros y pastillas de freno. Esto sí es una "
                         "compra: tiene proveedor, factura y cuenta por pagar, así que no va por Actualizar existencias "
                         "sino por la recepción. Elijo el origen: Sin orden de compra. "
                         "Primero el proveedor: escribo Autopartes, espero un momento a que aparezca, y lo elijo de la lista. Luego el almacén destino: "
                         "escribo Central; espero a que aparezca en la lista, y elijo el Almacén Central. Conviene elegirlo antes de importar las líneas, "
                         "porque las líneas toman su ubicación.",
            "acciones": [
                {"click_opcional": "button.panel-collapse", "al_decir": "Llegó un contenedor"},
                cartel("cuidado", "Una compra, no una carga",
                       "Tiene proveedor, factura y cuenta por pagar: entra por la recepción, no por Actualizar existencias.",
                       "Esto sí es una compra", 8000),
                c("button:has-text('Sin orden de compra')", "Sin orden de compra"),
                {"escribir": {"sel": "app-partner-document-select input", "texto": "Autopartes"}, "al_decir": "escribo Autopartes"},
                c("mat-option:has-text('Autopartes del Caribe Germiva')", "lo elijo de la lista"),
                {"escribir": {"sel": "app-autocomplete:has-text('Almacén destino') input", "texto": "Central"},
                 "al_decir": "escribo Central"},
                c("mat-option:has-text('Almacén Central')", "elijo el Almacén Central"),
                cartel("consejo", "Almacén primero",
                       "Si cambias el almacén después de importar las líneas, pierden su ubicación.",
                       "Conviene elegirlo", 7000),
            ],
        },
        {
            "id": "02-importar-lineas", "capitulo": "Las líneas desde Excel", "rotulo": "Importar líneas",
            "ruta": "Compras › Recepciones › Crear recepción",
            "texto_pantalla": "Importar líneas desde Excel · código, cantidad y costo",
            "narracion": "Con cientos de líneas no se escriben a mano. Pulso Importar líneas desde Excel. La plantilla "
                         "trae el código del producto, la cantidad, el costo unitario sin ITBIS, el impuesto, y, si hace falta, el lote "
                         "y el vencimiento. Ya llené la del contenedor: mil ochocientos filtros a ciento setenta y dos, y "
                         "seiscientos juegos de pastillas a seiscientos diez. Elijo el archivo. Dos líneas listas, por "
                         "seiscientos setenta y cinco mil seiscientos pesos sin ITBIS, y ninguna con error. Agrego las dos "
                         "líneas.",
            "acciones": [
                c("button:has-text('Importar líneas desde Excel')", "Pulso Importar líneas"),
                r(f"{D} button:has-text('Descargar plantilla')", "La plantilla", 6000),
                {"subir": {"sel": f"{D} input[type='file']", "archivo": "seeds/existencias/archivos/recepcion-contenedor.xlsx",
                           "ancla": f"{D} button:has-text('Elegir archivo')"}, "al_decir": "Elijo el archivo"},
                r(D, "Dos líneas listas", 6000),
                c(f"{D} button:has-text('Agregar 2 líneas')", "Agrego las dos"),
            ],
        },
        {
            "id": "03-procesar", "capitulo": "Guardar, aprobar y procesar", "rotulo": "Procesar a inventario",
            "ruta": "Compras › Recepciones",
            "texto_pantalla": "Recepción · guardar, aprobar y procesar a inventario",
            "narracion": "Las líneas quedan en la recepción con su cantidad, su costo y su ubicación. Pulso guardar; el "
                         "aviso dice que la recepción se creó, y acepto. En el menú acciones pulso aprobar recepción; me pide confirmar, y "
                         "apruebo. El aviso dice que ya se puede procesar a inventario; acepto. Y en el mismo menú, "
                         "procesar a inventario. Pulso procesar las dos líneas. La mercancía entró al almacén: el asiento "
                         "va a inventario contra mercancía por recibir, y cuando llegue la factura del proveedor se coteja "
                         "con esta recepción, con su ITBIS, su cuenta por pagar y su 606.",
            "acciones": [
                r("mat-card:has-text('Líneas') mat-card-title", "Las líneas quedan", 3500),
                c(".form-layout-footer button:has-text('Guardar')", "Pulso guardar"),
                r(".custom-alert-dialog-panel mat-dialog-container", "la recepción se creó", 2500),
                c("mat-dialog-container button:has-text('Aceptar')", "y acepto. En"),
                c(".page-hero button:has-text('Acciones')", "el menú acciones"),
                c(".mat-mdc-menu-panel button:has-text('Aprobar Recepción')", "pulso aprobar recepción"),
                c("mat-dialog-container button:has-text('Aprobar')", "y apruebo"),
                r(".custom-alert-dialog-panel mat-dialog-container", "ya se puede procesar", 2500),
                c("mat-dialog-container button:has-text('Aceptar')", "acepto. Y en"),
                c(".page-hero button:has-text('Acciones')", "el mismo menú"),
                c(".mat-mdc-menu-panel button:has-text('Procesar a Inventario')", "procesar a inventario. Pulso"),
                c("mat-dialog-container button:has-text('Procesar 2 líneas')", "procesar las dos líneas"),
                r(".custom-alert-dialog-panel mat-dialog-container", "La mercancía entró", 3500),
                c("mat-dialog-container button:has-text('Aceptar')", "el asiento va"),
                cartel("consejo", "Después, la factura",
                       "Se coteja con esta recepción: ITBIS, cuenta por pagar a nombre del proveedor y 606.",
                       "cuando llegue la factura", 8000),
            ],
        },
        {
            "id": "04-historial", "capitulo": "La compra a nombre del proveedor", "rotulo": "Historial del producto",
            "ruta": "Inventario › Productos › Historial",
            "texto_pantalla": "Historial del producto · la recepción con su proveedor",
            "navegar": "/inventory/product/list", "al_decir_navegar": "abro el catálogo",
            "narracion": "Ahora veamos dónde queda el proveedor. En Inventario abro el catálogo de productos, y entro al "
                         "filtro de aceite. En la pestaña Historial están los documentos del producto. Aquí está la "
                         "recepción del contenedor, a nombre de Autopartes del Caribe, con su cantidad y su costo. Esa es "
                         "la diferencia con las cargas de existencias: el inventario inicial, los conteos y los sobrantes "
                         "no tienen proveedor; las compras sí, y quedan a su nombre.",
            "acciones": [
                c("table tbody tr:has-text('Filtro de aceite') td:nth-child(2)", "entro al"),
                c("div[role='tab']:has-text('Historial')", "En la pestaña Historial"),
                r("table tbody tr:has-text('Autopartes') td:nth-child(1)", "Aquí está la", 2000),
                r("table tbody tr:has-text('Autopartes') td:has-text('Autopartes')", "a nombre de Autopartes", 5000),
                cartel("consejo", "¿Dónde queda el proveedor?",
                       "En las compras: recepción, factura, cuenta por pagar y 606. Las cargas de existencias no lo llevan.",
                       "Esa es la diferencia", 9000),
            ],
        },
    ],
}

VIDEOS = {
    "existencias-01-inventario-inicial": V1,
    "existencias-02-mercancia-que-quedo-fuera": V2,
    "existencias-03-conteo-fisico": V3,
    "existencias-04-sobrante": V4,
    "existencias-05-correccion": V5,
    "existencias-06-productos-nuevos": V6,
    "existencias-07-asiento-no-se-registra": V7,
    "existencias-08-recepcion-contenedor": V8,
}

if __name__ == "__main__":
    for nombre, cuerpo in VIDEOS.items():
        guion = {**CABECERA, **{k: v for k, v in cuerpo.items() if k != "pasos"}, "pasos": cuerpo["pasos"]}
        destino = RAIZ / "guiones" / f"{nombre}.json"
        destino.write_text(json.dumps(guion, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("escrito", destino.relative_to(RAIZ))
