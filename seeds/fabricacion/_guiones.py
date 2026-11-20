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

if __name__ == "__main__":
    for nombre, v in VIDEOS.items():
        guion = {**COMUN, **v}
        (RAIZ / "guiones" / f"{nombre}.json").write_text(json.dumps(guion, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        pal = sum(len(p["narracion"].split()) for p in v["pasos"])
        print(f"{nombre}: {len(v['pasos'])} pasos, {pal} palabras (~{pal/2.9/60:.1f} min)")
