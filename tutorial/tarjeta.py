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


# ── Entrada y cierre de marca (`marca_video`) ─────────────────────────────
# Paleta de la identidad 2026 (Logos/Germiva-logo-eslogan): azul marino del
# nombre, verde y teal de la hoja, azul de la hoja inferior.
MARINO = (11, 53, 82)       # #0B3552 — títulos
VERDE_MARCA = (91, 211, 78)  # #5BD34E — línea de acento, punto del rótulo
AZUL_MARCA = (18, 115, 184)  # #1273B8 — antetítulo
TEAL = (4, 177, 158)         # #04B19E
TINTA = MARINO
GRIS = (71, 85, 105)
RAIZ_MARCA = "marca"


def _inter_bold(tam):
    """Inter Bold (marca/fuentes) para las líneas secundarias; el título va en
    ExtraBold vía `_fuente`. Sin el archivo, cae a `_fuente`."""
    from pathlib import Path

    from PIL import ImageFont
    ruta = Path(__file__).resolve().parent.parent / "marca" / "fuentes" / "Inter-Bold.ttf"
    try:
        return ImageFont.truetype(str(ruta), tam)
    except OSError:
        return _fuente(tam)


def _fondo_claro(tam):
    ancho, alto = tam
    img = Image.new("RGB", tam)
    dib = ImageDraw.Draw(img)
    ini, fin = (255, 255, 255), (241, 245, 249)
    for y in range(alto):
        t = y / alto
        dib.line([(0, y), (ancho, y)],
                 fill=tuple(int(a + (b - a) * t) for a, b in zip(ini, fin)))
    return img


def cargar_marca(ruta, alto=None, ancho=None):
    """Arte de marca (logo o símbolo) escalado, con transparencia.

    Los PNG de `marca/` ya vienen con el fondo transparente y sin halo
    (generados desde Logos/ des-mezclando el blanco). Si llega uno opaco, se
    le aplica el mismo des-mezclado aquí, para no pegar un recuadro blanco.
    """
    from pathlib import Path

    p = Path(ruta)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent / p
    if not p.exists():
        return None
    arte = Image.open(p)
    if arte.mode != "RGBA" or arte.getchannel("A").getextrema()[0] == 255:
        rgb = arte.convert("RGB")
        fuera = []
        for r, g, b in rgb.getdata():
            a = max(0.0, min(1.0, (248 - min(r, g, b)) / 128))
            fuera.append((255, 255, 255, 0) if a <= 0 else
                         tuple(max(0, min(255, round(255 - (255 - c) / a))) for c in (r, g, b))
                         + (round(a * 255),))
        arte = Image.new("RGBA", rgb.size)
        arte.putdata(fuera)
    caja = arte.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if caja:
        arte = arte.crop(caja)
    if alto:
        escala = alto / arte.height
    else:
        escala = ancho / arte.width
    return arte.resize((round(arte.width * escala), round(arte.height * escala)), Image.LANCZOS)


def _envolver_parejo(dib, texto, fuente, ancho_max):
    """Como `_envolver`, pero con líneas de largo parejo: estrecha el ancho
    mientras no aparezca una línea más, para no dejar una palabra huérfana."""
    lineas = _envolver(dib, texto, fuente, ancho_max)
    ancho = ancho_max
    while len(lineas) > 1 and ancho > ancho_max // 3:
        prueba = _envolver(dib, texto, fuente, ancho - 20)
        if len(prueba) > len(lineas):
            break
        lineas, ancho = prueba, ancho - 20
    return lineas


def render_marca(tipo, datos, destino, tam=(1920, 1080)):
    """`tipo` = "entrada" (símbolo · antetítulo · título · «Germiva ERP ·
    Tutorial») o "cierre" (logo horizontal —ya trae el eslogan— · url).
    Sobrio: fondo claro, un arte de marca, pocas líneas de Inter centradas."""
    ancho, alto = tam
    img = _fondo_claro(tam)
    dib = ImageDraw.Draw(img)
    centro = ancho // 2

    # (fuente, color, líneas, aire por encima); None = línea de acento
    grupos = []
    if tipo == "entrada":
        arte = cargar_marca(datos.get("simbolo") or f"{RAIZ_MARCA}/simbolo.png", alto=210)
        # «Módulo · Tema»: el módulo sube como antetítulo y el tema queda de título
        titulo = datos["titulo"]
        antetitulo = None
        if " · " in titulo:
            antetitulo, titulo = titulo.split(" · ", 1)
        if antetitulo:
            grupos.append((_inter_bold(32), AZUL_MARCA, [antetitulo.upper()], 60))
        f = _fuente(80)
        grupos.append((f, MARINO, _envolver_parejo(dib, titulo, f, int(ancho * 0.82)),
                       18 if antetitulo else 60))
        grupos.append((None, None, None, 40))
        grupos.append((_inter_bold(36), TEAL, [datos.get("linea") or "Germiva ERP · Tutorial"], 34))
    else:
        # el logo horizontal ya lleva «ERP | Siembra control, cosecha
        # resultados»: el eslogan NO se repite en texto
        arte = cargar_marca(datos.get("logo") or f"{RAIZ_MARCA}/logo.png", ancho=int(ancho * 0.52))
        grupos.append((None, None, None, 64))
        if datos.get("url"):
            grupos.append((_inter_bold(46), AZUL_MARCA, [datos["url"].replace("https://", "")], 34))

    def alto_grupo(f, lineas):
        return 6 if f is None else int(f.size * 1.22) * len(lineas)

    total = sum(aire + alto_grupo(f, l) for f, _, l, aire in grupos)
    if arte:
        total += arte.height
    y = (alto - total) // 2
    if arte:
        img.paste(arte, ((ancho - arte.width) // 2, y), arte)
        y += arte.height
    for f, color, lineas, aire in grupos:
        y += aire
        if f is None:
            dib.rounded_rectangle([centro - 60, y, centro + 60, y + 6], radius=3, fill=VERDE_MARCA)
            y += 6
            continue
        for linea in lineas:
            dib.text((centro, y), linea, font=f, fill=color, anchor="ma")
            y += int(f.size * 1.22)
    img.save(destino)


def render_rotulo(texto, destino, alto_frame=1080, ancho_frame=1920):
    """Rótulo del paso: una píldora oscura semitransparente con el título en
    Inter, del tamaño justo del texto (~5 % del alto del cuadro). Se guarda
    del tamaño del rótulo; el montaje lo coloca abajo a la izquierda."""
    alto = round(alto_frame * 0.05)          # 54 px en 1080p
    f = _inter_bold(round(alto * 0.46))
    medir = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    ancho_max = int(ancho_frame * 0.40)
    punto, relleno = 10, round(alto * 0.42)
    disponible = ancho_max - 2 * relleno - punto - 14
    if medir.textlength(texto, font=f) > disponible:
        while texto and medir.textlength(texto + "…", font=f) > disponible:
            texto = texto[:-1]
        texto = texto.rstrip(" ·,") + "…"
    ancho = int(2 * relleno + punto + 14 + medir.textlength(texto, font=f))
    img = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    dib = ImageDraw.Draw(img)
    dib.rounded_rectangle([0, 0, ancho - 1, alto - 1], radius=alto // 2, fill=(7, 33, 52, 212))
    cy = alto // 2
    dib.ellipse([relleno, cy - punto // 2, relleno + punto, cy + punto // 2], fill=VERDE_MARCA)
    dib.text((relleno + punto + 14, cy), texto, font=f, fill=(255, 255, 255), anchor="lm")
    img.save(destino)
    return img.size
