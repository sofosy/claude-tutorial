"""Rutas y carga del guion."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


ZOOM_CAMPO = 1.22  # más cerrado que esto y el campo pierde su entorno


def _expandir_campos(paso):
    """Un paso con `campos` se convierte en una captura por campo.

    Marcar cinco campos en un mismo frame reparte la atención y el usuario no
    sabe cuál mira mientras escucha. Una marca por captura elimina la duda, y
    escribirlo así evita tener que repetir navegar/setup/ruta campo por campo.

    El bloque `vista` antepone una toma de la pantalla completa, sin zoom: ir
    directo al primer campo ampliado deja al usuario sin saber dónde está parado
    dentro de la pantalla. Primero el mapa, después el detalle.
    """
    if "campos" not in paso:
        return [paso]

    base = {k: v for k, v in paso.items()
            if k not in ("campos", "id", "acciones", "vista")}
    entradas = []
    if "vista" in paso:
        entradas.append(("0", paso["vista"], None))
    entradas += [(str(i + 1), c, c["sel"]) for i, c in enumerate(paso["campos"])]

    pasos = []
    for n, (sufijo, dato, sel) in enumerate(entradas):
        p = dict(base)
        p["id"] = f"{paso['id']}-{sufijo}"
        p["acciones"] = (paso.get("acciones", []) if n == 0 else []) \
            + dato.get("acciones", [])
        p["narracion"] = dato["narracion"]
        p["texto_pantalla"] = dato.get("texto_pantalla")
        if sel:
            p["resaltar"] = [{"sel": sel, "estilo": dato.get("estilo", "caja"),
                              "color": dato.get("color", "ambar")}]
            p["kenburns"] = {"hacia": sel,
                             "zoom": paso.get("kenburns", {}).get("zoom", ZOOM_CAMPO)}
        else:
            p["resaltar"] = []
            p.pop("kenburns", None)
        if n > 0:  # ya estamos en la pantalla: no re-navegar ni re-sembrar datos
            p.pop("navegar", None)
            p.pop("setup", None)
        pasos.append(p)
    return pasos


def _leer(nombre):
    ruta = RAIZ / nombre
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def cargar_guion(nombre):
    """Guion = config.json + config.local.json + el guion, en ese orden.

    Lo compartido (marca, voz, dominio público, privacidad) vive en la config
    para que todos los tutoriales salgan iguales sin repetirlo guion por guion.
    Lo que depende de esta máquina va en config.local.json, que no se versiona.
    """
    ruta = RAIZ / "guiones" / f"{nombre}.json"
    if not ruta.exists():
        raise SystemExit(f"No existe el guion: {ruta}")

    guion = {}
    for capa in (_leer("config.json"), _leer("config.local.json"),
                 json.loads(ruta.read_text(encoding="utf-8"))):
        guion.update({k: v for k, v in capa.items() if not k.startswith("_")})

    if "{RAIZ}" in guion.get("base_url", ""):
        guion["base_url"] = guion["base_url"].replace("{RAIZ}", str(RAIZ))

    guion["pasos"] = [p for base in guion["pasos"] for p in _expandir_campos(base)]
    return guion


def dir_salida(nombre):
    d = RAIZ / "salida" / nombre
    d.mkdir(parents=True, exist_ok=True)
    return d


def pasos_filtrados(guion, solo=None):
    """Todos los pasos, o solo el que empieza con el prefijo dado (--paso 03)."""
    if not solo:
        return guion["pasos"]
    sel = [p for p in guion["pasos"] if p["id"].startswith(solo)]
    if not sel:
        raise SystemExit(f"Ningún paso coincide con '{solo}'")
    return sel
