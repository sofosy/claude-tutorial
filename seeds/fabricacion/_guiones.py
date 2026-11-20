"""Genera guiones/fabricacion-NN-*.json (cabecera común + pasos de cada video).
    python3 seeds/fabricacion/_guiones.py
Editar aquí y regenerar: los .json son el producto, este archivo es la fuente."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
COMUN = {
    "base_url": "http://localhost:4200",
    "zona_horaria": "America/Santo_Domingo",
    "sesion": {"tipo": "api", "url": "http://localhost:3001/api/auth/dev/login",
               "cuerpo": {"username": "admin", "password": "admin"}, "clave": "aut",
               "extra": {"__v": 2}, "navegar": "/home"},
    "voz": {"id": "es-DO-RamonaNeural", "velocidad": "+12%"},
    "musica": {"archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -32, "ducking": True, "fade_s": 2},
    "loudnorm": {"lufs": -14, "tp": -1.5},
    "marca_video": {"entrada_s": 3, "cierre_s": 3},
    "rotulo_paso": {"segundos": 3.5},
    "css_global": ["app-chatbot-widget{display:none!important}", ".chatbot-fab{display:none!important}"],
    "pronunciacion": {"OF-1": "o efe uno", "OF-2": "o efe dos", "OF-3": "o efe tres", "ITBIS": "itebís"},
    "privacidad": {"perfil": "ninguno", "permitidos": ["germiva", "130555"],
                   "mapa_fijo": {"localhost:3001": "api.germiva.com", "localhost:4200": "germiva.com"}},
}
PANEL = "section.gm-console-panel"
def campo(etiqueta): return f"mat-form-field:has(mat-label:has-text('{etiqueta}')) input"
def clic(sel, decir, **k): return {"click": sel, "al_decir": decir, **k}
def marca(sel, decir, ms=3500, **k): return {"resaltar": sel, "durante_ms": ms, "al_decir": decir, **k}
def teclea(sel, texto, decir): return {"escribir": {"sel": sel, "texto": texto}, "al_decir": decir}
def fila(texto): return f"table.mfg-recipe-table tbody tr:has-text('{texto}')"

VIDEOS = {}

# ───────────────────────── 01 · La lista de materiales ─────────────────────────
VIDEOS["fabricacion-01-lista-de-materiales"] = {
    "titulo": "Fabricación · Parte 1: la lista de materiales",
    "descripcion": "Primer video de Fabricación en Germiva ERP. La lista de materiales es la receta del producto que fabricas: qué componentes lleva, cuánto trabajo y cuánto cuesta cada unidad. La armamos con una panadería y su bizcocho de vainilla, en menos de tres minutos.",
    "_comentario": "Serie Fabricación (nov. 2026), video 1. Estado A (seeds/fabricacion/preparar.mjs A): Panadería Germiva con Harina de trigo 60 lb a 30, Azúcar crema 40 lb a 38, Huevos 150 a 9.50, Mantequilla 10 lb a 140, y «Bizcocho de vainilla» sin lista. Lista: produce 12, tolerancia 5 %, 8 lb harina + 5 lb azúcar + 30 huevos + 3 lb mantequilla = 1,135.00; 90 min × 400/h + 120 = 720.00; costo por unidad 154.5833.",
    "setup": {"tipo": "shell", "cmd": "node seeds/fabricacion/preparar.mjs A"},
    "aprenderas": ["Dónde está Fabricación y qué trae cada pestaña", "Crear la lista de materiales de un producto", "Agregar la mano de obra y los gastos indirectos", "Leer el costo por unidad antes de fabricar", "Publicar la lista y entender sus versiones"],
    "errores_comunes": ["Poner las cantidades de una sola unidad cuando la corrida produce varias", "Dejar fuera la mano de obra: el costo sale más bajo que el real", "Creer que editar la lista cambia las órdenes ya creadas: cada orden conserva su versión"],
    "pasos": [
        {
            "id": "01-consola", "capitulo": "Dónde está Fabricación", "rotulo": "Fabricación",
            "ruta": "Inventario › Fabricación",
            "narracion": "¿Fabricas lo que vendes? Germiva ya lleva la fabricación completa: qué lleva cada producto, cuánto cuesta hacerlo y qué sale del almacén. Lo vemos con una panadería y su bizcocho de vainilla. Entro a Inventario y abro Fabricación, la primera opción. Para ver mejor, recojo el panel. Arriba hay cuatro pestañas: el tablero, las órdenes, las listas de materiales y la trazabilidad. Todo empieza por la lista de materiales, que es la receta: qué componentes lleva el producto y en qué cantidad. Pulso Nueva lista.",
            "acciones": [
                {"cartel": {"tipo": "consejo", "titulo": "En este video", "texto": "La lista de materiales: la receta y el costo de lo que fabricas."}, "durante_ms": 7000, "al_decir": "Germiva ya lleva"},
                clic("nav.module-rail [aria-label='Inventario']", "Entro a Inventario"),
                clic(".panel-item:has-text('Fabricación')", "abro Fabricación"),
                clic("button.panel-collapse", "recojo el panel"),
                marca("nav.mat-mdc-tab-nav-bar, .mat-mdc-tab-links", "cuatro pestañas", 4000),
                marca("a.mat-mdc-tab-link:has-text('Listas de materiales')", "Todo empieza", 5500),
                clic("button:has-text('Nueva lista')", "Pulso Nueva lista"),
            ],
        },
        {
            "id": "02-componentes", "capitulo": "El producto y sus componentes", "rotulo": "Lista de materiales",
            "ruta": "Fabricación › Listas de materiales › Nueva",
            "narracion": "Primero, el producto terminado: escribo bizcocho en el buscador y, cuando aparece debajo, lo elijo. En cantidad que produce pongo doce, porque una corrida de esta receta saca doce bizcochos. En tolerancia de consumo, cinco por ciento: si un día se gasta más material que eso, el sistema pide una explicación antes de registrar. Ahora, los componentes de una corrida. Busco harina, y fíjate que el buscador dice cuánta hay libre y a qué costo; la elijo. En cantidad van ocho libras, que es lo que llevan los doce bizcochos, no uno solo. Agrego otro componente y busco el azúcar. Aparece el azúcar crema, con sus cuarenta libras de existencia, y la selecciono. De azúcar, esta receta lleva por corrida cinco libras, ni más ni menos. Seguimos. Agrego uno más, y ahora busco los huevos. Hay ciento cincuenta en la despensa; con el nombre completo los marco en el buscador. La receta lleva en total treinta unidades, un cartón completo. Ya casi. Para terminar, agrego el último componente y escribo las primeras letras de la mantequilla. Con eso basta para encontrarla, así que la tomo del buscador. Y de mantequilla van tres libras. Listo. Ahora mira a la derecha: cada línea ya muestra su costo, calculado con lo que te costó la compra.",
            "acciones": [
                teclea(campo("Producto terminado"), "bizcocho", "escribo bizcocho"),
                clic("mat-option:has-text('Bizcocho de vainilla')", "lo elijo"),
                teclea(campo("Cantidad que produce"), "12", "pongo doce"),
                teclea(campo("Tolerancia de consumo"), "5", "cinco por ciento"),
                teclea(campo("Componente 1"), "harina", "Busco harina"),
                marca("mat-option:has-text('Harina de trigo')", "cuánta hay libre", 2500, cursor=False),
                clic("mat-option:has-text('Harina de trigo')", "la elijo"),
                teclea("input[aria-label='Cantidad del componente 1']", "8", "ocho libras"),
                clic("button:has-text('Agregar componente')", "Agrego otro componente"),
                teclea(campo("Componente 2"), "azúcar", "busco el azúcar"),
                clic("mat-option:has-text('Azúcar crema')", "la selecciono"),
                teclea("input[aria-label='Cantidad del componente 2']", "5", "cinco libras"),
                clic("button:has-text('Agregar componente')", "Agrego uno más"),
                teclea(campo("Componente 3"), "huevos", "busco los huevos"),
                clic("mat-option:has-text('Huevos')", "los marco"),
                teclea("input[aria-label='Cantidad del componente 3']", "30", "treinta unidades"),
                clic("button:has-text('Agregar componente')", "agrego el último componente"),
                teclea(campo("Componente 4"), "mante", "la mantequilla"),
                clic("mat-option:has-text('Mantequilla')", "la tomo"),
                teclea("input[aria-label='Cantidad del componente 4']", "3", "tres libras"),
                marca("table.mfg-recipe-table tbody tr:nth-child(1) td:nth-child(5)", "cada línea ya muestra", 2500),
            ],
        },
        {
            "id": "03-costo-publicar", "capitulo": "Mano de obra, costo y publicar", "rotulo": "Costo y publicar",
            "ruta": "Fabricación › Listas de materiales › Nueva",
            "narracion": "Falta el trabajo. En mano de obra pongo noventa minutos, que es lo que tarda una corrida. La tarifa por hora del panadero: cuatrocientos pesos. Y en gastos indirectos, lo que no es material ni trabajo, como la luz del horno y el empaque: ciento veinte pesos. Ahora mira abajo. Los materiales de la corrida cuestan mil ciento treinta y cinco pesos; la mano de obra y los indirectos, setecientos veinte; y cada bizcocho sale en ciento cincuenta y cuatro con cincuenta y ocho. Ese es tu costo real para poner el precio. Pulso Publicar lista, y el aviso confirma que se publicó. Queda como versión uno: si mañana cambias la receta se publica la versión dos, y las órdenes ya creadas conservan la suya. Con la lista publicada ya podemos fabricar. Eso, en el siguiente video.",
            "acciones": [
                teclea(campo("Mano de obra por corrida"), "90", "noventa minutos"),
                teclea(campo("Tarifa por hora"), "400", "La tarifa por hora"),
                teclea(campo("Gastos indirectos por corrida"), "120", "en gastos indirectos"),
                marca("table.mfg-recipe-table tfoot tr:nth-child(1) td:nth-child(2)", "Los materiales de la corrida", 4000),
                marca("table.mfg-recipe-table tfoot tr:nth-child(2) td:nth-child(2)", "la mano de obra y los indirectos", 3000),
                marca("table.mfg-recipe-table tfoot tr:nth-child(3) td:nth-child(2)", "cada bizcocho sale", 7000),
                clic("button:has-text('Publicar lista')", "Pulso Publicar lista"),
                marca(".mat-mdc-snack-bar-container", "el aviso confirma", 2500, cursor=False),
                marca("ul.mfg-recipe-list li.is-active, ul.mfg-recipe-list li", "Queda como versión uno", 8000),
                marca("button:has-text('Fabricar')", "ya podemos fabricar", 4000),
            ],
        },
    ],
}

# ───────────────────────── 02 · La orden de fabricación ─────────────────────────
def sel(etiqueta): return f"mat-form-field:has(mat-label:has-text('{etiqueta}')) mat-select"
RUN = "article.mfg-run"
VIDEOS["fabricacion-02-orden-de-fabricacion"] = {
    "titulo": "Fabricación · Parte 2: la orden de fabricación",
    "descripcion": "Segundo video de Fabricación en Germiva ERP. Con la lista de materiales publicada, fabricar son tres pasos: crear la orden, reservar el material y registrar lo que salió. Vemos cómo el sistema descuenta la materia prima, da entrada al producto terminado con su costo real y hace el asiento contable solo.",
    "_comentario": "Serie Fabricación (nov. 2026), video 2. Estado B (preparar.mjs B): la lista del bizcocho publicada (v1). Orden OF-1 por 24 UND: requiere 16 lb harina, 10 lb azúcar, 60 huevos, 6 lb mantequilla; materiales 2,270.00 + conversión 1,440.00 = 3,710.00 → 154.5833 por unidad. Origen Almacén Sur · Despensa, destino Almacén Sur · Vitrina. La contabilización automática de producción viene activa en la empresa sembrada (asiento ASI-…).",
    "sesion": {**COMUN["sesion"], "navegar": "/inventory/fabricacion", "esperar": "button:has-text('Nueva orden')"},
    "setup": {"tipo": "shell", "cmd": "node seeds/fabricacion/preparar.mjs B"},
    "aprenderas": ["Crear una orden de fabricación y leer su plan de materiales", "Qué significa reservar el material", "Registrar la producción y cerrar la orden", "Ver la salida de materia prima y la entrada del producto terminado", "Dónde queda el costo real y el asiento contable"],
    "errores_comunes": ["Dejar el producto terminado en el mismo almacén de la materia prima sin querer", "Creer que reservar descuenta la existencia: solo la aparta; se descuenta al registrar la producción", "Registrar sin revisar la columna «Usado» cuando se gastó más material del previsto"],
    "pasos": [
        {
            "id": "01-nueva-orden", "capitulo": "Crear la orden y leer el plan", "rotulo": "Nueva orden",
            "ruta": "Fabricación › Órdenes › Nueva",
            "narracion": "En el video anterior publicamos la receta del bizcocho. Hoy lo fabricamos, y son tres pasos: crear la orden, reservar el material y registrar lo que salió. Pulso Nueva orden. La lista de materiales ya viene elegida. En cantidad a fabricar escribo veinticuatro, que son dos corridas. El almacén de los componentes es la despensa, de donde sale la materia prima. El del producto terminado lo abro y lo cambio a la vitrina, que es donde entran los bizcochos. Abajo, el sistema ya hizo la cuenta: lo requerido de cada componente, lo disponible, y la columna por comprar vacía, porque hay de todo. Costo estimado de la orden: tres mil setecientos diez pesos. Si faltara material, aquí mismo dice cuánto hay que comprar, y la orden se guarda en borrador hasta que llegue. Pulso Guardar y reservar.",
            "acciones": [
                {"cartel": {"tipo": "consejo", "titulo": "Tres pasos", "texto": "Crear la orden · reservar el material · registrar lo que salió."}, "durante_ms": 6000, "al_decir": "son tres pasos"},
                clic("button:has-text('Nueva orden')", "Pulso Nueva orden"),
                marca(sel("Lista de materiales"), "ya viene elegida", 2500),
                teclea(campo("Cantidad a fabricar"), "24", "escribo veinticuatro"),
                marca(sel("Almacén de los componentes"), "es la despensa", 3500),
                clic(sel("Almacén del producto terminado"), "lo abro"),
                clic("mat-option:has-text('Vitrina')", "a la vitrina"),
                marca("table.gm-table thead th:nth-child(2)", "lo requerido", 1500),
                marca("table.gm-table thead th:nth-child(3)", "lo disponible", 800),
                marca("table.gm-table thead th:nth-child(4)", "la columna por comprar", 2800),
                marca("table.gm-table tfoot tr:last-child td:last-child", "Costo estimado de la orden", 3000),
                marca(".mfg-note", "Si faltara material", 6000),
                clic("button:has-text('Guardar y reservar')", "Pulso Guardar y reservar"),
            ],
        },
        {
            "id": "02-reservada", "capitulo": "Material reservado", "rotulo": "Material reservado",
            "ruta": "Fabricación › Órdenes › OF-1",
            "narracion": "El aviso confirma que la orden se creó y el material quedó reservado. Arriba está su número, y la línea de avance marca material reservado. Reservar no descuenta nada todavía: la harina y los huevos siguen en la despensa, pero apartados, y nadie más puede venderlos ni usarlos en otra orden. A la izquierda está el consumo previsto, con el lote de donde va a salir cada componente. Y en la columna usado puedes corregir la cantidad si al final se gastó más o menos.",
            "acciones": [
                marca(".mat-mdc-snack-bar-container", "El aviso confirma", 3000, cursor=False),
                marca(".mfg-title", "su número", 1200),
                marca("ol.mfg-steps", "la línea de avance", 4000),
                marca("tr.mfg-row--sub:has-text('HAR-1101') td:nth-child(2)", "pero apartados", 4000),
                marca("tr.mfg-row--sub:has-text('HAR-1101') td:nth-child(1)", "con el lote", 3500),
                marca("input[aria-label^='Usado de Harina']", "en la columna usado", 5000),
            ],
        },
        {
            "id": "03-registrar", "capitulo": "Registrar la producción", "rotulo": "Registrar producción",
            "ruta": "Fabricación › Órdenes › OF-1",
            "narracion": "Los bizcochos ya salieron del horno. A la derecha registro la producción. Unidades buenas: veinticuatro, que ya viene propuesto. Si alguno se hubiera dañado, iría en unidades descartadas; eso lo vemos en el próximo video. El lote del producto terminado lo propone el sistema, y el costo de conversión, mil cuatrocientos cuarenta, sale de la mano de obra de la lista. Debajo está el costo de este registro: cada bizcocho entra al almacén en ciento cincuenta y cuatro con cincuenta y ocho. Dejo marcado cerrar la orden, y pulso Registrar y cerrar la orden. El aviso lo confirma: producción registrada y orden cerrada.",
            "acciones": [
                marca(campo("Unidades buenas"), "Unidades buenas", 3000),
                marca(campo("Unidades descartadas"), "unidades descartadas", 3000),
                marca(campo("Lote del producto terminado"), "El lote del producto terminado", 3000),
                marca(campo("Costo de conversión"), "el costo de conversión", 4500),
                marca("dl.mfg-cost .mfg-cost__total", "cada bizcocho entra", 4500),
                marca("mat-checkbox:has-text('Cerrar la orden')", "Dejo marcado", 2500),
                clic("button:has-text('Registrar y cerrar la orden')", "pulso Registrar"),
                marca(".mat-mdc-snack-bar-container", "El aviso lo confirma", 3500, cursor=False),
            ],
        },
        {
            "id": "04-resultado", "capitulo": "Kardex, costo y asiento", "rotulo": "El resultado",
            "ruta": "Fabricación › Órdenes › OF-1",
            "narracion": "¿Y qué hizo el sistema con un solo clic? Está todo abajo, en producción registrada. Primero, los movimientos de inventario: cuatro salidas de materia prima, cada una de su lote y a su costo, y una entrada de veinticuatro bizcochos a la vitrina, a ciento cincuenta y cuatro con cincuenta y ocho cada uno. Segundo, el asiento contable, hecho solo: sale el material del inventario, entra el producto terminado. Y tercero, el resultado: materiales, conversión y costo total. Arriba, la orden quedó cerrada. Ya tienes bizcochos para vender, y sabes exactamente cuánto te costó cada uno.",
            "acciones": [
                marca(f"{RUN} .mfg-run__head", "en producción registrada", 2500),
                marca(f"{RUN} table.gm-table >> nth=0 >> tbody tr:nth-child(1) td:nth-child(1)", "cuatro salidas", 4500),
                marca(f"{RUN} table.gm-table >> nth=0 >> tbody tr:nth-child(5) td:nth-child(1)", "una entrada", 6500),
                marca(f"{RUN} .gm-badge--success >> nth=0", "el asiento contable", 5000),
                marca(f"{RUN} dl.mfg-cost >> nth=-1", "el resultado", 3000),
                marca(".mfg-title .gm-badge", "quedó cerrada", 6000),
            ],
        },
    ],
}

# ───────────────────────── 03 · Merma, faltantes y trazabilidad ─────────────────────────
def tab(nombre): return f"a.mat-mdc-tab-link:has-text('{nombre}')"
def tablero(titulo): return f"section.mfg-panel:has(h3:has-text('{titulo}'))"
VIDEOS["fabricacion-03-merma-faltantes-trazabilidad"] = {
    "titulo": "Fabricación · Parte 3: merma, faltantes y trazabilidad",
    "descripcion": "Tercer video de Fabricación en Germiva ERP: lo que pasa cuando no todo sale perfecto. Registrar una merma y decidir si la absorbe el producto o va al gasto, corregir un registro, guardar una orden en borrador cuando falta material, leer el tablero y rastrear un lote de materia prima hasta las órdenes que lo usaron.",
    "_comentario": "Serie Fabricación (nov. 2026), video 3. Estado C (preparar.mjs C): OF-1 cerrada (24 UND, lote OF-1-1) y OF-2 reservada (12 UND). En cámara: OF-2 con 11 buenas + 1 descartada, merma normal → 1,855.00 / 11 = 168.64 por unidad (anormal sería 154.58 y 154.58 al gasto). Queda 1 lb de mantequilla: una orden nueva de 12 pide 3 lb → «Por comprar 2 LB», se guarda en borrador (OF-3). Trazabilidad del lote HAR-1101: entrada de 60 lb y salidas a OF-1 (16) y OF-2 (8). «Corregir este registro» solo se señala (no se pulsa).",
    "sesion": {**COMUN["sesion"], "navegar": "/inventory/fabricacion", "esperar": "button:has-text('Nueva orden')"},
    "setup": {"tipo": "shell", "cmd": "node seeds/fabricacion/preparar.mjs C"},
    "aprenderas": ["Registrar unidades descartadas y elegir el tratamiento de la merma", "Cómo se corrige un registro de producción", "Guardar una orden en borrador cuando falta material y ver qué comprar", "Leer el tablero de fabricación", "Rastrear un lote hasta las órdenes que lo consumieron"],
    "errores_comunes": ["Marcar como pérdida anormal la merma de todos los días: el costo del producto queda más bajo que el real", "Borrar o ajustar a mano la existencia en vez de usar «Corregir este registro»", "Dejar órdenes en borrador sin revisar en el tablero qué material hay que comprar"],
    "pasos": [
        {
            "id": "01-merma", "capitulo": "Registrar una merma", "rotulo": "Merma",
            "ruta": "Fabricación › Órdenes › OF-2",
            "narracion": "En fabricación no todo sale perfecto. Hoy vemos qué hacer con la merma, con el material que falta, y cómo rastrear un lote. Abro la pestaña Órdenes: cada fila es una orden, con su avance y su estado. Entro a la segunda, de doce bizcochos, que ya tiene el material reservado. Resulta que uno se quemó. En unidades buenas escribo once, que son los que sí sirven para vender. Y el que se perdió va al lado, en unidades descartadas: uno. Aparece una decisión nueva, el tratamiento de la merma. La abro. Merma normal es la de todos los días, y la absorbe el producto: los once buenos cargan con el costo del que se perdió. Pérdida anormal es un accidente, y va directo al gasto sin encarecer el producto. Elijo la normal. El motivo es obligatorio; escribo que se quemó en el horno. Y mira el costo: cada bizcocho sube a ciento sesenta y ocho con sesenta y cuatro. Pulso Registrar y cerrar la orden.",
            "acciones": [
                {"cartel": {"tipo": "consejo", "titulo": "En este video", "texto": "Merma · material que falta · trazabilidad de un lote."}, "durante_ms": 5500, "al_decir": "qué hacer con la merma"},
                clic(tab("Órdenes"), "Abro la pestaña"),
                marca("table.gm-table tbody tr:has-text('OF-1') td:nth-child(3)", "con su avance", 2500),
                clic("table.gm-table tbody tr:has-text('OF-2') td:nth-child(1)", "Entro a la segunda"),
                marca(".mfg-title", "ya tiene el material reservado", 2500),
                teclea(campo("Unidades buenas"), "11", "escribo once"),
                teclea(campo("Unidades descartadas"), "1", "en unidades descartadas"),
                clic(sel("Tratamiento de la merma"), "La abro"),
                marca("mat-option:has-text('Merma normal')", "Merma normal es", 7000, cursor=False),
                marca("mat-option:has-text('Pérdida anormal')", "Pérdida anormal es", 6000, cursor=False),
                clic("mat-option:has-text('Merma normal')", "Elijo la normal"),
                teclea(campo("Motivo de la merma"), "Se quemó en el horno", "escribo que se quemó"),
                marca("dl.mfg-cost .mfg-cost__total", "cada bizcocho sube", 4500),
                clic("button:has-text('Registrar y cerrar la orden')", "Pulso Registrar"),
            ],
        },
        {
            "id": "02-corregir", "capitulo": "Corregir un registro", "rotulo": "Corregir",
            "ruta": "Fabricación › Órdenes › OF-2",
            "narracion": "El aviso confirma el registro, y la orden quedó cerrada con su merma anotada. ¿Y si te equivocaste al registrar? Aquí no se borra nada. Abajo, en el registro, está Corregir este registro: pides la corrección, escribes el motivo, y el sistema solo devuelve el material al almacén, retira los bizcochos y reversa el asiento contable.",
            "acciones": [
                marca(".mat-mdc-snack-bar-container", "El aviso confirma", 2500, cursor=False),
                marca("app-summary-strip, .mfg-title .gm-badge", "con su merma anotada", 4000),
                marca("button:has-text('Corregir este registro')", "está Corregir este registro", 9000),
            ],
        },
        {
            "id": "03-falta-material", "capitulo": "Cuando falta material", "rotulo": "Falta material",
            "ruta": "Fabricación › Órdenes › Nueva",
            "narracion": "Ahora, cuando el material no alcanza. Pulso Nueva orden y pido doce bizcochos más. Enseguida se recalcula, y el plan lo marca en rojo: de mantequilla hay que comprar dos libras. El aviso de abajo lo explica, y el botón de reservar queda apagado. Pero la orden no se pierde: pulso Guardar borrador. El sistema confirma que se creó, y la orden queda esperando la compra. Ahora voy al Tablero. Abajo, material para las órdenes en borrador es tu lista de compras de fabricación: lo necesario, lo libre y lo que falta comprar. Y arriba, el resumen del período: la producción buena, el porcentaje de merma, el costo de producción y el costo por unidad.",
            "acciones": [
                clic("button:has-text('Nueva orden')", "Pulso Nueva orden"),
                teclea(campo("Cantidad a fabricar"), "12", "pido doce"),
                marca("td.mfg-short", "lo marca en rojo", 3500),
                marca(".mfg-note--warn", "El aviso de abajo", 2000),
                marca("button:has-text('Guardar y reservar')", "el botón de reservar", 2500),
                clic("button:has-text('Guardar borrador')", "pulso Guardar borrador"),
                marca(".mat-mdc-snack-bar-container", "El sistema confirma", 2500, cursor=False),
                clic(tab("Tablero"), "voy al Tablero"),
                marca(tablero("Material para las órdenes en borrador"), "material para las órdenes", 8000),
                marca("app-summary-strip", "el resumen del período", 8000),
            ],
        },
        {
            "id": "04-trazabilidad", "capitulo": "Rastrear un lote", "rotulo": "Trazabilidad",
            "ruta": "Fabricación › Trazabilidad",
            "narracion": "Por último, la trazabilidad. Imagina que el proveedor avisa que un lote de harina salió malo. Abro Trazabilidad y, en el buscador, escribo el número del lote, que viene en la etiqueta del saco. Con el lote escrito, pulso Buscar. Ahí está su historia completa: la entrada por la compra, y cada orden de fabricación que lo usó, con el saldo que fue quedando. Con un clic en el documento llegas a la orden, y de ahí a los bizcochos que salieron de ella. Lista de materiales, orden y control: eso es fabricar con Germiva.",
            "acciones": [
                clic(tab("Trazabilidad"), "Abro Trazabilidad"),
                teclea("input[placeholder^='Lote de un componente']", "HAR-1101", "escribo el número"),
                clic("app-mfg-trace button:has-text('Buscar')", "pulso Buscar"),
                marca("app-mfg-trace table tbody tr:last-child td:nth-child(5)", "la entrada por la compra", 2000),
                marca("app-mfg-trace table tbody tr:nth-child(1) td:nth-child(5)", "cada orden de fabricación", 2000),
                marca("app-mfg-trace table thead th:nth-child(4)", "con el saldo", 2500),
                clic("app-mfg-trace button.mfg-link:has-text('OF-1')", "Con un clic"),
                marca(".mfg-title", "llegas a la orden", 6000),
            ],
        },
    ],
}

# ───────────────────────── 04 · Del pedido a la fábrica y sub-ensambles ─────────────────────────
VIDEOS["fabricacion-04-pedido-y-subensambles"] = {
    "titulo": "Fabricación · Parte 4: fabricar para un pedido y sub-ensambles",
    "descripcion": "Cuarto video de Fabricación en Germiva ERP. Un cliente pide un producto que todavía no está hecho: desde el pedido de venta se planifica la fabricación con un clic. Y cuando el producto lleva adentro otro que también fabricas (un sub-ensamble), el sistema crea su orden sola y arrastra el costo completo.",
    "_comentario": "Serie Fabricación (nov. 2026), video 4. Estado D (preparar.mjs D): lista del bizcocho de vainilla (v1) y «Bizcocho de cumpleaños» (1 bizcocho de vainilla + 0.5 lb azúcar + 2 huevos; 20 min × 400/h + 25 indirectos, produce 1) con un pedido de venta confirmado VEN-…-000001 de 6 UND para el Colmado Germiva La Esquina. En cámara: OF-1 (cumpleaños, 6) en borrador → «Planificar sub-ensambles» crea OF-2 (vainilla, 6) → se reserva y se registra OF-2 (927.50 → 154.5833 c/u) → vuelta a OF-1, reservar y registrar: 927.50 + 114 + 114 + 950 = 2,105.50 → 350.9167 por unidad. «Planificar fabricación» solo sale con el pedido Confirmado o Parcialmente despachado y con permiso de editar inventario.",
    "sesion": {**COMUN["sesion"], "navegar": "/sales/sales-orders/1", "esperar": "button:has-text('Planificar fabricación')"},
    "setup": {"tipo": "shell", "cmd": "node seeds/fabricacion/preparar.mjs D"},
    "aprenderas": ["Planificar la fabricación desde un pedido de venta confirmado", "Qué es un sub-ensamble y cómo lo reconoce el sistema", "Crear las órdenes de los sub-ensambles con un clic", "En qué orden se fabrica: primero lo de adentro", "Cómo el costo del sub-ensamble llega al producto final"],
    "errores_comunes": ["Buscar «Planificar fabricación» en un pedido en borrador: solo aparece cuando está confirmado", "Intentar reservar la orden principal antes de fabricar el sub-ensamble", "Comprar un componente que tú mismo fabricas: si tiene lista de materiales, se planifica como sub-ensamble"],
    "pasos": [
        {
            "id": "01-pedido", "capitulo": "Del pedido de venta a la orden", "rotulo": "Desde el pedido",
            "ruta": "Ventas › Órdenes de Venta",
            "narracion": "Un colmado pidió seis bizcochos de cumpleaños, y no hay ninguno hecho. Este es su pedido de venta, ya confirmado. Para verlo mejor, recojo el panel de la izquierda. En la línea del producto hay un botón nuevo: Planificar fabricación. Lo pulso, y Germiva me lleva a una orden de fabricación con el producto y la cantidad del pedido ya puestos. Mira el plan: el bizcocho de cumpleaños lleva adentro un bizcocho de vainilla, que también se fabrica aquí. Por eso tiene la etiqueta sub-ensamble, y dice que faltan seis. No hay que comprarlos, hay que hacerlos. Pulso Guardar borrador.",
            "acciones": [
                marca(":text-is('Confirmada') >> nth=0", "ya confirmado", 1500),
                clic("button.panel-collapse", "recojo el panel"),
                marca("button:has-text('Planificar fabricación')", "hay un botón nuevo", 3000),
                clic("button:has-text('Planificar fabricación')", "Lo pulso"),
                marca(campo("Cantidad a fabricar"), "la cantidad del pedido", 3500),
                marca("table.gm-table tbody tr:has-text('Bizcocho de vainilla') td:nth-child(1)", "lleva adentro", 4500),
                marca("table.gm-table tbody tr:has-text('Bizcocho de vainilla') .gm-badge", "la etiqueta sub-ensamble", 1800),
                marca("td.mfg-short", "faltan seis", 4500),
                clic("button:has-text('Guardar borrador')", "Pulso Guardar borrador"),
            ],
        },
        {
            "id": "02-subensamble", "capitulo": "Planificar y fabricar el sub-ensamble", "rotulo": "Sub-ensamble",
            "ruta": "Fabricación › Órdenes",
            "narracion": "La orden quedó en borrador, como confirma el aviso, y arriba aparece otro botón: Planificar sub-ensambles. Lo pulso, y el aviso dice que las órdenes de los sub-ensambles se crearon en borrador. Aquí está: el sistema crea sola la orden del bizcocho de vainilla, por los seis que faltan, enlazada a esta. La regla es sencilla: primero se fabrica lo de adentro. Entro a la orden hija. Arriba, pulso Reservar material; el aviso confirma la reserva. Y como ya vimos en el segundo video, registro la producción: las seis unidades buenas vienen propuestas, así que pulso Registrar y cerrar la orden.",
            "acciones": [
                marca(".mat-mdc-snack-bar-container", "como confirma el aviso", 1800, cursor=False),
                marca("button:has-text('Planificar sub-ensambles')", "aparece otro botón", 2500),
                clic("button:has-text('Planificar sub-ensambles')", "Lo pulso"),
                marca(".mat-mdc-snack-bar-container", "el aviso dice", 3500, cursor=False),
                marca("section.mfg-panel:has(h3:has-text('Órdenes de los sub-ensambles'))", "crea sola la orden", 6000),
                clic("tr.mfg-row--link:has-text('Bizcocho de vainilla') td:nth-child(1) .gm-cell-title", "Entro a la orden hija"),
                clic("button:has-text('Reservar material')", "pulso Reservar material"),
                marca(".mat-mdc-snack-bar-container", "el aviso confirma", 2500, cursor=False),
                marca(campo("Unidades buenas"), "las seis unidades buenas", 3000),
                clic("button:has-text('Registrar y cerrar la orden')", "pulso Registrar"),
            ],
        },
        {
            "id": "03-principal", "capitulo": "Terminar la orden principal", "rotulo": "Orden principal",
            "ruta": "Fabricación › Órdenes",
            "narracion": "Listo el sub-ensamble. En sus datos, el enlace sub-ensamble de me devuelve a la orden principal. Ahora sí hay bizcochos de vainilla en el almacén, así que pulso Reservar material, y el aviso confirma que quedó reservado. Ahora registro la producción de los seis bizcochos de cumpleaños, y la orden se cierra con su aviso. Fíjate en el costo por unidad: unos trescientos cincuenta y un pesos. Ahí va todo: el bizcocho de vainilla con su propia mano de obra, el azúcar, los huevos y el trabajo de decorarlo. Los seis ya están en el almacén, listos para despachar el pedido del colmado. Del pedido a la fábrica, sin salir de Germiva.",
            "acciones": [
                marca(".mat-mdc-snack-bar-container", "Listo el sub-ensamble", 2000, cursor=False),
                clic("dl.mfg-facts button.mfg-link", "me devuelve"),
                clic("button:has-text('Reservar material')", "pulso Reservar material"),
                marca(".mat-mdc-snack-bar-container", "el aviso confirma", 2200, cursor=False),
                clic("button:has-text('Registrar y cerrar la orden')", "registro la producción"),
                marca(".mat-mdc-snack-bar-container", "con su aviso", 1000, cursor=False),
                marca("app-summary-strip, .mfg-title", "Fíjate en el costo", 5000),
                marca("article.mfg-run table.gm-table >> nth=0 >> tbody tr:has-text('Bizcocho de vainilla') td:nth-child(1)", "el bizcocho de vainilla", 6000),
                marca("article.mfg-run table.gm-table >> nth=0 >> tbody tr:last-child td:nth-child(1)", "Los seis ya están", 6000),
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
