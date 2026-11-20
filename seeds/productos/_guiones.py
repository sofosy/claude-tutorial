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

if __name__ == "__main__":
    for nombre, v in VIDEOS.items():
        guion = {**COMUN, **v}
        (RAIZ / "guiones" / f"{nombre}.json").write_text(json.dumps(guion, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        pal = sum(len(p["narracion"].split()) for p in v["pasos"])
        print(f"{nombre}: {len(v['pasos'])} pasos, {pal} palabras (~{pal/2.9/60:.1f} min)")
