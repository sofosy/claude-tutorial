"""Paquete para YouTube: título, descripción y capítulos con timestamps.

No genera texto nuevo: la narración ya está escrita en el guion y las duraciones
salen del montaje, así que los tiempos son exactos y sin costo.
"""
MIN_CAPITULO = 10  # YouTube ignora los capítulos de menos de 10 segundos


def _mmss(s):
    return f"{int(s) // 60:02d}:{int(s) % 60:02d}"


def _capitulos(guion, duraciones, transicion):
    """Agrupa pasos consecutivos que comparten `capitulo`.

    Un capítulo por paso produciría entradas de 8 segundos que YouTube descarta
    en silencio: se pega el texto, se ve bien, y los capítulos no aparecen.
    """
    caps, t = [], 0.0
    for i, (paso, dur) in enumerate(zip(guion["pasos"], duraciones)):
        titulo = paso.get("capitulo") or guion["titulo"]
        if not caps or caps[-1][0] != titulo:
            caps.append([titulo, t])
        t += dur - (transicion if i else 0)

    # fusiona los que quedaron cortos con el anterior
    fusionados = []
    for i, (titulo, ini) in enumerate(caps):
        fin = caps[i + 1][1] if i + 1 < len(caps) else t
        if fusionados and fin - ini < MIN_CAPITULO:
            continue
        fusionados.append((titulo, ini))
    return fusionados, t


def _miniatura(guion, salida):
    """Frame representativo, oscurecido, con el título encima."""
    from PIL import Image, ImageDraw

    from .anotar import COLORES, _fuente
    from .tarjeta import _envolver

    portada = next((p["id"] for p in guion["pasos"] if p.get("portada")), None)
    frames = sorted((salida / "anotados").glob("*.png"))
    if not frames:
        return None
    ruta = next((f for f in frames if f.stem == portada), frames[0])

    img = Image.open(ruta).convert("RGB").resize((1280, 720))
    velo = Image.new("RGBA", img.size, (10, 14, 24, 165))
    img = Image.alpha_composite(img.convert("RGBA"), velo)
    dib = ImageDraw.Draw(img)

    f = _fuente(74)
    lineas = _envolver(dib, guion["titulo"], f, 1120)
    y = (720 - len(lineas) * 88) // 2
    for linea in lineas:
        dib.text((640, y), linea, font=f, fill=(255, 255, 255), anchor="ma")
        y += 88
    dib.rounded_rectangle([565, y + 22, 715, y + 30], radius=4,
                          fill=COLORES["ambar"])

    destino = salida / "miniatura.png"
    img.convert("RGB").save(destino)
    return destino


def publicar(guion, salida, duraciones, transicion, mapa=None):
    from .privacidad import aplicar_a_texto
    lim = lambda s: aplicar_a_texto(s, mapa or {})
    caps, total = _capitulos(guion, duraciones, transicion)
    partes = [
        "TÍTULO", "=" * 60, guion["titulo"], "",
        "DESCRIPCIÓN", "=" * 60,
    ]
    if guion.get("descripcion"):
        partes += [lim(guion["descripcion"]), ""]

    partes.append("⏱️ CAPÍTULOS")
    for titulo, ini in caps:
        partes.append(f"{_mmss(ini)}  {titulo}")

    if guion.get("aprenderas"):
        partes += ["", "📋 EN ESTE VIDEO APRENDERÁS"]
        partes += [f"• {x}" for x in guion["aprenderas"]]

    if guion.get("errores_comunes"):
        partes += ["", "⚠️ ERRORES COMUNES"]
        partes += [f"• {x}" for x in guion["errores_comunes"]]

    if guion.get("tags"):
        partes += ["", "🏷️ ETIQUETAS", ", ".join(guion["tags"])]

    partes += ["", "—", f"Duración: {_mmss(total)}", "",
               "TRANSCRIPCIÓN", "=" * 60]
    partes += [lim(p["narracion"]) for p in guion["pasos"]]

    destino = salida / "youtube.txt"
    destino.write_text("\n".join(partes) + "\n", encoding="utf-8")
    if len(caps) < 3:
        print(f"  aviso: solo {len(caps)} capítulos; YouTube pide mínimo 3")
    print(f"  → {destino}")
    mini = _miniatura(guion, salida)
    if mini:
        print(f"  → {mini}")
