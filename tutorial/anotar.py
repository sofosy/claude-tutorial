"""C2 — Anotación con Pillow.

Dibuja sobre el frame usando las cajas que reportó el navegador en C1.
Paleta de un solo acento para no competir con los colores propios del ERP.
"""
import json

from PIL import Image, ImageDraw, ImageFont

COLORES = {
    "ambar": (245, 166, 35),
    "rojo": (220, 38, 38),
    "verde": (5, 150, 105),
}
GROSOR = 7
MARGEN = 10          # aire entre el elemento y el recuadro
OSCURECER = 165      # alpha del velo en estilo "foco"
SALIDA_ANCHO, SALIDA_ALTO = 1920, 1080  # tamaño del video, para la capa de barra

_FUENTES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def _fuente(tam):
    for f in _FUENTES:
        try:
            return ImageFont.truetype(f, tam)
        except OSError:
            continue
    return ImageFont.load_default()


def _expandir(caja, img):
    x, y, w, h = caja
    return [max(0, x - MARGEN), max(0, y - MARGEN),
            min(img.width, x + w + MARGEN), min(img.height, y + h + MARGEN)]


def _cursor(img, caja):
    """Puntero dibujado sobre el elemento indicado.

    El screenshot del navegador no incluye el cursor del sistema, así que se
    dibuja. Marcar el elemento dice *cuál* es; el puntero dice *que ahí vas a
    hacer algo*, que es lo que el usuario imita.
    """
    x, y, w, h = caja
    forma = [(0, 0), (0, 17), (4.2, 13), (7.3, 20), (10.2, 18.7), (7.2, 12), (12, 12)]
    s = 3.4
    # en elementos anchos (un input, una fila) el puntero se pega al inicio del
    # contenido, no al borde derecho, donde quedaría flotando lejos de todo
    tx = min(x + min(w * 0.5, h * 2.2), img.width - 60)
    ty = y + h * 0.78
    pts = [(tx + px * s, ty + py * s) for px, py in forma]

    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.polygon([(px + 5, py + 7) for px, py in pts], fill=(0, 0, 0, 80))
    d.polygon(pts, fill=(255, 255, 255, 255))
    d.line(pts + [pts[0]], fill=(23, 30, 45, 255), width=5, joint="curve")
    return Image.alpha_composite(img, capa)


def _velo(img, cajas):
    """Oscurece todo menos las zonas marcadas."""
    velo = Image.new("RGBA", img.size, (10, 14, 24, OSCURECER))
    for c in cajas:
        x0, y0, x1, y1 = _expandir(c, img)
        velo.paste((0, 0, 0, 0), (int(x0), int(y0), int(x1), int(y1)))
    return Image.alpha_composite(img, velo)


def _etiqueta(dib, x, y, texto, color, img):
    r = 26
    x = min(max(x, r), img.width - r)   # las entradas de menú tocan el borde
    y = min(max(y, r), img.height - r)
    dib.ellipse([x - r, y - r, x + r, y + r], fill=color)
    dib.text((x, y), str(texto), fill=(255, 255, 255), font=_fuente(30),
             anchor="mm")


def _chip(dib, x, y, texto):
    """Ruta de navegación fija: ubica al que cayó al video por la mitad."""
    f = _fuente(26)
    x0, y0, x1, y1 = dib.textbbox((x, y), texto, font=f, anchor="lm")
    dib.rounded_rectangle([x0 - 18, y0 - 12, x1 + 18, y1 + 12], radius=8,
                          fill=(16, 22, 34, 225))
    dib.text((x, y), texto, fill=COLORES["ambar"], font=f, anchor="lm")


def _capa(texto, ruta, destino, arriba):
    """Barra y chip de ruta, en una capa aparte del tamaño final del video.

    Si se pintaran sobre el frame, el zoom de C4 se los comería (y taparían el
    elemento resaltado antes de hacerlo). Se superponen después del zoom.

    `arriba` manda la barra al tope: los botones de acción de un ERP viven al
    fondo del formulario, y ahí el encuadre no puede centrarlos porque ya toca el
    borde de la página. En esos pasos la barra abajo siempre les roza.
    """
    capa = Image.new("RGBA", (SALIDA_ANCHO, SALIDA_ALTO), (0, 0, 0, 0))
    dib = ImageDraw.Draw(capa)
    alto = 78

    if texto:
        y0 = 0 if arriba else SALIDA_ALTO - alto
        dib.rectangle([0, y0, SALIDA_ANCHO, y0 + alto], fill=(16, 22, 34, 228))
        borde = y0 + alto - 3 if arriba else y0
        dib.rectangle([0, borde, SALIDA_ANCHO, borde + 3], fill=COLORES["ambar"])
        dib.text((45, y0 + alto // 2), texto, fill=(255, 255, 255),
                 font=_fuente(29), anchor="lm")

    if ruta:
        # pegada a la barra, nunca en la esquina superior: ahí vive el logo y el
        # encabezado de cualquier ERP, y el chip terminaría tapándolos
        y = alto + 42 if arriba else SALIDA_ALTO - alto - 42
        _chip(dib, 45, y, ruta)

    capa.save(destino)


def anotar(pasos, salida):
    frames = salida / "frames"
    dest = salida / "anotados"
    barras = salida / "barras"
    dest.mkdir(parents=True, exist_ok=True)
    barras.mkdir(parents=True, exist_ok=True)

    for paso in pasos:
        pid = paso["id"]
        print(f"  · {pid}")
        meta = json.loads((frames / f"{pid}.json").read_text(encoding="utf-8"))
        img = Image.open(frames / f"{pid}.png").convert("RGBA")

        marcas = meta["resaltar"]
        enfocadas = [m["caja"] for m in marcas if m.get("estilo") == "foco"]
        if enfocadas:
            img = _velo(img, enfocadas)

        dib = ImageDraw.Draw(img)
        for m in marcas:
            color = COLORES.get(m.get("color", "ambar"), COLORES["ambar"])
            x0, y0, x1, y1 = _expandir(m["caja"], img)
            if m.get("estilo") == "subrayado":
                # en menús y enlaces, un recuadro compite con el resaltado propio
                # de la navegación; la línea señala sin discutirle al diseño
                dib.rounded_rectangle([x0, y1 - GROSOR, x1, y1 + 2], radius=4,
                                      fill=color)
            else:
                dib.rounded_rectangle([x0, y0, x1, y1], radius=10,
                                      outline=color, width=GROSOR)
            if m.get("etiqueta"):
                _etiqueta(dib, x0, y0, m["etiqueta"], color, img)

        if meta.get("cursor"):
            img = _cursor(img, meta["cursor"])

        img.convert("RGB").save(dest / f"{pid}.png")

        if meta.get("texto_pantalla") or meta.get("ruta"):
            al_fondo = any(m["caja"][1] + m["caja"][3] > img.height * 0.80
                           for m in marcas)
            _capa(meta.get("texto_pantalla"), meta.get("ruta"),
                  barras / f"{pid}.png", arriba=al_fondo)
