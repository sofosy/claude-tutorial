"""Verificación del guion ANTES de grabar, y del resultado DESPUÉS de montar.

El guion lo escribe un modelo (Opus/Sonnet) y otro lo rectifica. Para que esa
rectificación no sea «ver el video entero», hay dos herramientas:

- `revisar_guion(guion)`: reglas que un guion de grabación tiene que cumplir
  para que el video se explique solo. La regla madre es «cada clic y cada
  vista se explican»: todo clic/tecleo lleva `al_decir` con una palabra que
  la narración de ese paso dice de verdad; toda vista tiene narración,
  rótulo y ruta.
- `informe(guion, salida)`: tras montar, escribe `informe-video.md` con la
  línea de tiempo real de cada paso (qué palabra sonaba en el instante de
  cada clic, cuánto se desfasó, qué paso duró más que su voz) y una hoja de
  contactos con el fotograma exacto de cada clic, para revisarlos de un
  vistazo.
"""
import json
import subprocess
from collections import Counter

from . import narrar, privacidad

MIN_PALABRAS = 6          # una narración más corta que esto no explica nada
DESFASE_MAX = 0.9         # segundos entre la palabra y el clic que se toleran
ACCIONES_VISIBLES = ("click", "escribir", "seleccionar", "marcar", "presionar", "subir")


def _hallazgo(lista, nivel, paso, texto):
    lista.append((nivel, paso, texto))


def _normal(palabra):
    return "".join(c for c in palabra.lower() if c.isalnum())


def _posicion(narracion, clave, desde=0):
    """Índice de palabra donde la narración dice `clave`, buscando desde `desde`."""
    tokens = [_normal(w) for w in narracion.split()]
    buscadas = [_normal(w) for w in str(clave).split()]
    for i in range(desde, len(tokens) - len(buscadas) + 1):
        if tokens[i:i + len(buscadas)] == buscadas:
            return i
    return None


def _instante_cercano(palabras, clave, t_evento):
    """De todas las veces que la voz dice `clave`, la más cercana al evento."""
    buscadas = [_normal(w) for w in str(clave).split()]
    dichas = [_normal(p["texto"]) for p in palabras]
    candidatos = [palabras[i]["t"] for i in range(len(dichas) - len(buscadas) + 1)
                  if dichas[i:i + len(buscadas)] == buscadas]
    return min(candidatos, key=lambda t: abs(t - t_evento)) if candidatos else None


def revisar_guion(guion):
    """Devuelve [(nivel, paso, texto)]; nivel ∈ {'ERROR', 'AVISO'}."""
    h = []
    for donde, tipo, valor in privacidad.revisar_guion(guion):
        _hallazgo(h, "ERROR", donde, f"dato que parece real sin declarar ({tipo}): {valor}")

    selectores = Counter()
    for p in guion["pasos"]:
        pid = p["id"]
        narr = (p.get("narracion") or "").strip()
        if len(narr.split()) < MIN_PALABRAS:
            _hallazgo(h, "ERROR", pid, "narración ausente o demasiado corta: la vista no se explica")
        if p.get("tarjeta"):
            continue
        if not p.get("texto_pantalla"):
            _hallazgo(h, "AVISO", pid, "sin `texto_pantalla`: la barra inferior saldrá vacía")
        if not p.get("ruta"):
            _hallazgo(h, "AVISO", pid, "sin `ruta`: quien caiga al video por la mitad no sabrá dónde está")
        if not p.get("resaltar") and not p.get("acciones") and not p.get("navegar"):
            _hallazgo(h, "AVISO", pid, "paso sin marca, sin acciones y sin navegación: ¿qué mira el usuario?")

        # cada clic se explica: lleva palabra de sincronía y la narración la dice
        from .grabar import instante
        palabras_narr = [{"t": i, "texto": w} for i, w in enumerate(narr.split())]
        espera_previa = 0
        clics = []
        ultimo = -1  # las palabras se consumen en orden: una acción no puede ir «hacia atrás»
        for acc in p.get("acciones", []):
            if "esperar_ms" in acc:
                espera_previa += acc["esperar_ms"]
                continue
            clave = next((k for k in ACCIONES_VISIBLES + ("resaltar", "plano_general", "quitar_marca")
                          if k in acc), None)
            if not clave:
                continue
            que = acc[clave] if isinstance(acc[clave], str) else (
                acc[clave].get("sel") if isinstance(acc[clave], dict) else clave)
            if clave in ACCIONES_VISIBLES:
                clics.append(que)
            if acc.get("al_decir") is None:
                if clave in ACCIONES_VISIBLES:
                    _hallazgo(h, "ERROR", pid, f"{clave} «{que}» sin `al_decir`: el clic no está anclado a la narración")
            elif isinstance(acc["al_decir"], str):
                pos = _posicion(narr, acc["al_decir"], desde=ultimo + 1)
                if pos is None:
                    if instante(palabras_narr, acc["al_decir"]) is None:
                        _hallazgo(h, "ERROR", pid, f"la narración no dice «{acc['al_decir']}» ({clave} «{que}»)")
                    else:
                        _hallazgo(h, "ERROR", pid, f"«{acc['al_decir']}» ({clave} «{que}») aparece en la"
                                  " narración ANTES que la palabra de la acción anterior: las acciones"
                                  " deben ir en el orden en que la voz las nombra")
                else:
                    ultimo = pos
            if acc.get("al_decir") is not None and clave in ACCIONES_VISIBLES and espera_previa >= 1000:
                # la espera corre ANTES de mirar la palabra: si suma más que el
                # instante de la palabra, el clic llega tarde sin remedio
                _hallazgo(h, "AVISO", pid, f"{espera_previa} ms de `esperar_ms` antes de «{que}» con"
                          " `al_decir`: retrasan el clic. El motor ya espera a que el elemento"
                          " sea visible; quita la espera o usa `esperar` (selector).")
            espera_previa = 0
        for m in p.get("resaltar", []):
            if m["sel"] in clics and (p.get("navegar") or "guardar" in m["sel"].lower()
                                      or "submit" in m["sel"].lower()):
                _hallazgo(h, "AVISO", pid, f"se resalta «{m['sel']}» después de pulsarlo: si el clic"
                          " cambia de pantalla el botón ya no existe. Resalta el RESULTADO"
                          " (la fila nueva, el aviso, el diálogo).")
        if p.get("al_decir") and instante(palabras_narr, p["al_decir"]) is None:
            _hallazgo(h, "ERROR", pid, f"la narración no dice «{p['al_decir']}» (marca)")
        for m in p.get("resaltar", []):
            selectores[m["sel"]] += 1

    for sel, n in selectores.items():
        if n > 2:
            _hallazgo(h, "AVISO", "guion", f"el elemento «{sel}» se marca {n} veces: ¿se repite la explicación?")
    return h


def _palabra_en(palabras, t):
    """La palabra que suena en el instante t (o la última antes)."""
    actual = None
    for p in palabras:
        if p["t"] <= t:
            actual = p["texto"]
        else:
            break
    return actual


def _contactos(rutas_frames, destino, columnas=4):
    """Hoja de contactos: los fotogramas de cada clic, en una sola imagen."""
    from PIL import Image, ImageDraw

    from .anotar import _fuente

    if not rutas_frames:
        return None
    ancho, alto = 480, 270
    filas = (len(rutas_frames) + columnas - 1) // columnas
    hoja = Image.new("RGB", (columnas * ancho, filas * (alto + 28)), (17, 24, 39))
    dib = ImageDraw.Draw(hoja)
    f = _fuente(18)
    for i, (ruta, rotulo) in enumerate(rutas_frames):
        x, y = (i % columnas) * ancho, (i // columnas) * (alto + 28)
        try:
            img = Image.open(ruta).resize((ancho, alto))
            hoja.paste(img, (x, y))
        except OSError:
            pass
        dib.text((x + 8, y + alto + 5), rotulo[:60], fill=(245, 166, 35), font=f)
    hoja.save(destino)
    return destino


def informe(guion, salida, video=None):
    segdir = salida / "grabacion" / "segmentos"
    revision = salida / "revision"
    revision.mkdir(exist_ok=True)
    for viejo in revision.glob("*.png"):
        viejo.unlink()
    video = video or salida / "video.mp4"

    lineas = [f"# Informe de grabación — {guion['titulo']}", ""]
    avisos, contactos = [], []
    t_video = 0.0
    for paso in guion["pasos"]:
        pid = paso["id"]
        seg = json.loads((segdir / f"{pid}.json").read_text(encoding="utf-8"))
        side = narrar.sidecar(salida, pid) or {}
        palabras = side.get("palabras", [])
        dur = seg["duracion"]
        lineas.append(f"## {pid} — {dur:.1f}s (voz {side.get('duracion', 0):.1f}s)"
                      f" · desde {t_video:.1f}s")
        if seg["tipo"] == "tarjeta":
            lineas.append("tarjeta")
        else:
            if seg.get("error"):
                avisos.append(f"{pid}: ERROR en la grabación — {seg['error']} → regrabar con --paso")
                lineas.append(f"**ERROR: {seg['error']}**")
            extra = dur - side.get("duracion", 0) - 0.6
            if extra > 0.5:
                avisos.append(f"{pid}: las acciones duraron {extra:.1f}s más que la voz (silencio al final)")
            eventos = seg.get("eventos", [])
            for ev in eventos:
                dicha = _palabra_en(palabras, ev["t"])
                linea = f"- {ev['t']:5.2f}s  {ev['tipo']:9} {ev['que']}"
                if dicha:
                    linea += f"  · sonaba «{dicha}»"
                # la visibilidad se MIDIÓ en el momento del evento; no se supone
                if ev.get("visible") is True:
                    linea += "  · visible entero"
                elif ev.get("visible") is False:
                    m = ev.get("medida", {})
                    linea += (f"  · **CORTADO** (elemento {m.get('arriba')}..{m.get('abajo')}px,"
                              f" franja {m.get('tope')}..{m.get('fondo')}px)")
                    avisos.append(f"{pid}: «{ev['que'][:60]}» no se veía entero al {ev['tipo']}"
                                  f" ({ev['t']:.1f}s) — ver su fotograma en revision/")
                lineas.append(linea)
                if ev["tipo"] == "alerta":
                    # toda alerta se explica: hace falta una marca sobre un
                    # diálogo/aviso en los 8 s siguientes a que apareció
                    explicada = any(e["tipo"] == "resaltar" and ev["t"] <= e["t"] <= ev["t"] + 8
                                    and any(k in e["que"] for k in ("dialog", "snack", "alert", "toast"))
                                    for e in eventos)
                    if not explicada:
                        avisos.append(f"{pid}: la alerta «{ev['que'][:70]}…» apareció a {ev['t']:.1f}s"
                                      " y no se señaló ni se explicó (regla: toda alerta se explica)")
                if ev["tipo"] in ("clic", "escribir", "subir", "alerta", "resaltar"):
                    # el fotograma se toma medio segundo después: el cursor ya
                    # llegó, el texto ya está escrito, la marca ya se ve
                    png = revision / f"{pid}-{ev['t']:05.2f}.png"
                    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                                    "-ss", f"{t_video + ev['t'] + 0.5:.3f}", "-i", str(video),
                                    "-frames:v", "1", str(png)], check=False)
                    estado = "CORTADO " if ev.get("visible") is False else ""
                    contactos.append((png, f"{estado}{pid} {ev['t']:.1f}s {ev['tipo']} «{dicha or ''}»"))
            # desfase entre la palabra pedida y el momento real del clic
            usados = set()
            # `escribir` se mide por el clic que lo inicia: el evento «escribir»
            # se anota al TERMINAR de teclear (para medir que el campo siguió
            # a la vista), y 20 letras tardan casi un segundo
            TIPO = {"click": "clic", "escribir": "clic", "resaltar": "resaltar",
                    "seleccionar": "seleccionar", "subir": "subir", "marcar": "clic"}
            for acc in paso.get("acciones", []):
                clave = acc.get("al_decir")
                if not isinstance(clave, str):
                    continue
                accion = next((k for k in acc if k in TIPO), None)
                if not accion:
                    continue
                v = acc[accion]
                sel = v if isinstance(v, str) else v.get("sel")
                # el mismo campo puede teclearse dos veces: se empareja por
                # tipo Y selector, en orden, sin reutilizar eventos
                ev = next((e for i, e in enumerate(seg.get("eventos", []))
                           if e["que"] == sel and e["tipo"] == TIPO[accion] and i not in usados), None)
                if ev:
                    usados.add(seg["eventos"].index(ev))
                t_pal = _instante_cercano(palabras, clave, ev["t"]) if ev else None
                if t_pal is not None and ev:
                    desfase = ev["t"] - t_pal
                    lineas.append(f"  · «{clave}» a {t_pal:.2f}s, clic a {ev['t']:.2f}s"
                                  f" (desfase {desfase:+.2f}s)")
                    if abs(desfase) > DESFASE_MAX:
                        avisos.append(f"{pid}: el clic en «{sel}» cayó {desfase:+.1f}s"
                                      f" respecto a «{clave}»")
        lineas.append("")
        t_video += dur

    hoja = _contactos(contactos, revision / "clics.png")
    lineas.insert(2, f"Duración total: {int(t_video) // 60:02d}:{int(t_video) % 60:02d}"
                     f" · {len(contactos)} clics/tecleos en cámara"
                     + (f" · hoja de contactos: `revision/clics.png`" if hoja else ""))
    lineas.insert(3, "")
    if avisos:
        lineas[4:4] = ["## Avisos", *[f"- {a}" for a in avisos], ""]
    else:
        lineas[4:4] = ["## Avisos", "- ninguno", ""]
    destino = salida / "informe-video.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    return destino, avisos
