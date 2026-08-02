"""C4 — Montaje con ffmpeg: Ken Burns por paso + concatenación + subtítulos.

La duración de cada clip la manda el audio, nunca un tiempo fijo: así jamás se
corta una frase a la mitad.
"""
import json
import subprocess

from . import privacidad
from .publicar import publicar

FPS = 30
ANCHO, ALTO = 1920, 1080
PAD = 0.6        # respiro al final de cada narración, en segundos
PRESCALE = 2     # ver _kenburns()
PLANO_GENERAL = (1.0, 0.5, 0.5)
TRANSICION = 0.35  # disolvencia entre clips; cabe dentro del PAD
ESPERA = 0.35      # fracción del clip en plano general antes de acercarse


def _zoom_seguro(meta, cxp, cyp, zoom_pedido):
    """Limita el zoom para que las marcas no queden fuera de cuadro.

    Hacer zoom hacia un panel y recortar el campo que estás señalando es el peor
    resultado posible, y pasa en cuanto la zona marcada es más ancha que el
    encuadre. En vez de pedirle al autor que calibre el zoom a mano por paso, se
    calcula el máximo que mantiene todas las marcas dentro y se recorta ahí.
    """
    marcas = [m["caja"] for m in meta.get("resaltar", [])]
    if not marcas:
        return zoom_pedido

    w, h = meta["tamano"]
    aire = 40
    dx = max(max(abs(x - cxp), abs(x + cw - cxp)) for x, _, cw, _ in marcas) + aire
    dy = max(max(abs(y - cyp), abs(y + ch - cyp)) for _, y, _, ch in marcas) + aire
    tope = min(w / (2 * dx), h / (2 * dy))
    return max(1.0, min(zoom_pedido, tope))


def _kenburns(meta, zoom_pedido, nframes):
    """Movimiento del clip: pantalla completa y, si hay marca, acercamiento.

    Todo clip abre en plano general y lo sostiene durante `ESPERA` de su
    duración. El acercamiento es un énfasis sobre el componente marcado, no el
    estado normal del video: sin la espera, el usuario nunca llega a ver la
    pantalla entera y pierde la referencia de dónde está.

    Un paso sin marcas no se acerca nunca.

    zoompan calcula el recorte en píxeles enteros, lo que produce un temblor muy
    visible. Escalar la imagen antes (PRESCALE) le da precisión sub-píxel y el
    movimiento sale limpio. Es la razón de que el filtro empiece con un scale.

    Las tomas de vista completa pasan por el mismo zoompan con zoom fijo en 1: un
    `scale` a secas sobre una imagen única produce un video de UN fotograma
    estirado a toda la duración, que algunos reproductores no saben mostrar y del
    que no se puede extraer un frame. zoompan es lo que garantiza los 30 fps.
    """
    w, h = meta["tamano"]
    if meta.get("kenburns"):
        caja = meta["kenburns"].get("caja")
        # sin caja el acercamiento va al centro: se usa cuando lo que hay que
        # mirar es la pantalla completa y no un componente concreto
        cxp, cyp = ((caja[0] + caja[2] / 2, caja[1] + caja[3] / 2) if caja
                    else (w / 2, h / 2))
        z1 = _zoom_seguro(meta, cxp, cyp, zoom_pedido)
        cx1, cy1 = cxp / w, cyp / h
    else:
        z1, cx1, cy1 = 1.0, 0.5, 0.5
    z0, cx0, cy0 = PLANO_GENERAL

    # se sostiene el plano general y después se suaviza el acercamiento
    t = f"(on/{max(nframes - 1, 1)})"
    u = f"(max(0,min(1,({t}-{ESPERA})/{1 - ESPERA:.4f})))"
    s = f"({u}*{u}*(3-2*{u}))"
    z = f"({z0:.4f}+({z1:.4f}-{z0:.4f})*{s})"
    px = f"({cx0:.4f}+({cx1:.4f}-{cx0:.4f})*{s})"
    py = f"({cy0:.4f}+({cy1:.4f}-{cy0:.4f})*{s})"
    ex = f"max(0,min(iw-iw/zoom,{px}*iw-(iw/zoom)/2))"
    ey = f"max(0,min(ih-ih/zoom,{py}*ih-(ih/zoom)/2))"

    filtro = (f"scale=iw*{PRESCALE}:ih*{PRESCALE},"
              f"zoompan=z='{z}':x='{ex}':y='{ey}'"
              f":d={nframes}:s={ANCHO}x{ALTO}:fps={FPS}")
    return filtro, (z1, cx1, cy1)


def _clip(png, mp3, barra, meta, zoom_pedido, dur, destino):
    nframes = max(int(round(dur * FPS)), 2)
    kb, fin = _kenburns(meta, zoom_pedido, nframes)

    entradas = ["-i", str(png), "-i", str(mp3)]
    if barra.exists():
        # la barra se superpone DESPUÉS del zoom, para que no la recorte
        entradas += ["-i", str(barra)]
        video = f"[0:v]{kb}[z];[z][2:v]overlay=0:0,format=yuv420p[v]"
    else:
        video = f"[0:v]{kb},format=yuv420p[v]"

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *entradas,
         "-filter_complex", f"{video};[1:a]apad[a]", "-map", "[v]", "-map", "[a]",
         "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         str(destino)], check=True)
    return fin


def _duracion(archivo):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(archivo)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def _unir(clips, destino):
    """Encadena los clips con disolvencia en vez de corte seco.

    El estilo `foco` oscurece la pantalla completa, así que entrar o salir de un
    paso con foco produce un destello en el corte. La disolvencia lo absorbe, y
    de paso suaviza el cambio de encuadre cuando sí hay que cambiar de pantalla.

    Cabe dentro del silencio final de cada narración (PAD), así que no se come
    ninguna palabra.
    """
    duraciones = [_duracion(c) for c in clips]
    entradas = []
    for c in clips:
        entradas += ["-i", str(c)]

    filtros, v, a, acum = [], "[0:v]", "[0:a]", duraciones[0]
    for i in range(1, len(clips)):
        off = acum - i * TRANSICION
        filtros.append(f"{v}[{i}:v]xfade=transition=fade:"
                       f"duration={TRANSICION}:offset={off:.3f}[v{i}]")
        filtros.append(f"{a}[{i}:a]acrossfade=d={TRANSICION}[a{i}]")
        v, a = f"[v{i}]", f"[a{i}]"
        acum += duraciones[i]

    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *entradas,
         "-filter_complex", ";".join(filtros),
         "-map", v, "-map", a,
         "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         str(destino)], check=True)
    return duraciones


def _srt(segmentos, destino):
    def ts(s):
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(s % 1 * 1000):03d}"

    lineas, t = [], 0.0
    for i, (texto, dur) in enumerate(segmentos, 1):
        # la disolvencia solapa los clips: sin descontarla, los subtítulos se
        # van desfasando y al final del video llevan varios segundos de atraso
        efectiva = dur - (TRANSICION if i > 1 else 0)
        lineas.append(f"{i}\n{ts(t)} --> {ts(t + efectiva)}\n{texto}\n")
        t += efectiva
    destino.write_text("\n".join(lineas), encoding="utf-8")


def montar(guion, salida):
    """Monta el video completo. Siempre usa todos los pasos del guion."""
    clips_dir = salida / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    duraciones = json.loads((salida / "audio" / "duraciones.json").read_text())

    mapa_priv = privacidad.cargar_mapa(salida)
    rutas, segmentos = [], []
    for paso in guion["pasos"]:
        pid = paso["id"]
        if pid not in duraciones:
            raise SystemExit(f"Falta el audio de '{pid}'. Corre: tut narrar")
        meta = json.loads((salida / "frames" / f"{pid}.json").read_text(encoding="utf-8"))
        dur = duraciones[pid] + PAD
        destino = clips_dir / f"{pid}.mp4"
        pedido = paso.get("kenburns", {}).get("zoom", 1.3)
        zoom = _clip(salida / "anotados" / f"{pid}.png",
                     salida / "audio" / f"{pid}.mp3",
                     salida / "barras" / f"{pid}.png",
                     meta, pedido, dur, destino)[0]
        aviso = ""
        if meta.get("kenburns") and zoom < pedido - 0.01:
            aviso = f"  zoom {pedido}→{zoom:.2f} (recortado para no cortar las marcas)"
        elif not meta.get("kenburns"):
            aviso = "  vista completa"
        print(f"  · {pid}  ({dur:.1f}s){aviso}")
        rutas.append(destino)
        segmentos.append((privacidad.aplicar_a_texto(
            paso["narracion"], mapa_priv), dur))

    final = salida / "final.mp4"
    print(f"  unir con disolvencia de {TRANSICION}s…")
    duraciones = _unir(rutas, final)
    _srt([(t, d) for (t, _), d in zip(segmentos, duraciones)],
         salida / "final.srt")
    print(f"\n  → {final}")
    publicar(guion, salida, duraciones, TRANSICION, mapa_priv)
