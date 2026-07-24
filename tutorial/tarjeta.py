"""Tarjetas de título y cierre: los únicos frames que no salen del navegador.

Un tutorial que termina cortando la última captura se siente inacabado. La tarjeta
de cierre resume lo logrado y engancha con lo que sigue.
"""
from PIL import Image, ImageDraw

from .anotar import COLORES, _fuente


def _fondo(tam):
    """Degradado vertical oscuro, dibujado por filas."""
    ancho, alto = tam
    img = Image.new("RGB", tam)
    dib = ImageDraw.Draw(img)
    ini, fin = (17, 24, 39), (31, 41, 55)
    for y in range(alto):
        t = y / alto
        dib.line([(0, y), (ancho, y)],
                 fill=tuple(int(a + (b - a) * t) for a, b in zip(ini, fin)))
    return img


def _envolver(dib, texto, fuente, ancho_max):
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if dib.textlength(prueba, font=fuente) <= ancho_max:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


SEPARADOR = 190  # ancho de la línea que separa el cierre del gancho


def _cargar_logo(ruta, ancho_max):
    """Logo escalado y con el fondo blanco convertido en transparencia.

    El archivo de marca viene sobre blanco; pegarlo tal cual sobre el degradado
    oscuro dejaría un recuadro blanco alrededor.
    """
    from pathlib import Path

    p = Path(ruta)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent / p
    if not p.exists():
        return None
    logo = Image.open(p).convert("RGBA")
    logo = logo.resize((ancho_max, int(logo.height * ancho_max / logo.width)))
    logo.putdata([(r, g, b, 0 if min(r, g, b) > 232 else a)
                  for r, g, b, a in logo.getdata()])
    return logo


def render(tarjeta, destino, tam):
    ancho, alto = tam
    img = _fondo(tam).convert("RGBA")
    dib = ImageDraw.Draw(img)
    centro = ancho // 2
    max_texto = int(ancho * 0.76)

    # (fuente, color, líneas, aire por encima del grupo)
    grupos = []
    if tarjeta.get("encabezado"):
        f = _fuente(44)
        grupos.append((f, COLORES["ambar"], [tarjeta["encabezado"].upper()], 0))
    f = _fuente(122)
    grupos.append((f, (255, 255, 255),
                   _envolver(dib, tarjeta["titulo"], f, max_texto), 46))
    if tarjeta.get("subtitulo"):
        f = _fuente(56)
        grupos.append((f, (203, 213, 225),
                       _envolver(dib, tarjeta["subtitulo"], f, max_texto), 40))
    if tarjeta.get("pie"):
        f = _fuente(52)
        grupos.append((None, None, None, 86))  # separador
        grupos.append((f, COLORES["ambar"],
                       _envolver(dib, tarjeta["pie"], f, max_texto), 46))

    # el eslogan solo se escribe si no hay logo: el arte de marca ya lo incluye
    if tarjeta.get("slogan") and not tarjeta.get("logo"):
        f = _fuente(46)
        grupos.append((f, (148, 163, 184),
                       _envolver(dib, tarjeta["slogan"], f, max_texto), 70))

    def alto_grupo(f, lineas):
        return 6 if f is None else int(f.size * 1.24) * len(lineas)

    total = sum(aire + alto_grupo(f, lineas) for f, _, lineas, aire in grupos)
    # el logo de marca ya trae el eslogan impreso: se dimensiona para que se lea
    logo = _cargar_logo(tarjeta["logo"], int(ancho * 0.23)) if tarjeta.get("logo") else None
    if logo:
        total += logo.height + 64

    y = (alto - total) // 2
    if logo:
        img.alpha_composite(logo, ((ancho - logo.width) // 2, y))
        y += logo.height + 64

    for f, color, lineas, aire in grupos:
        y += aire
        if f is None:
            dib.rounded_rectangle([centro - SEPARADOR // 2, y,
                                   centro + SEPARADOR // 2, y + 6],
                                  radius=3, fill=COLORES["ambar"])
            y += 6
            continue
        for linea in lineas:
            dib.text((centro, y), linea, font=f, fill=color, anchor="ma")
            y += int(f.size * 1.24)

    img.save(destino)
