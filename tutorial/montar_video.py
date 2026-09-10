"""G2 — Montaje de la grabación: segmentos del maestro + voz + capas + zoom.

Cada segmento registrado por G1 es un tramo [inicio, fin] del video maestro
cuya narración arranca justo en `inicio`. El montaje corta ese tramo, le mezcla
su audio, le superpone la barra de texto y el chip de ruta, le aplica un
acercamiento suave hacia el elemento marcado y encadena los clips SIN
recodificar la unión: la grabación ya es continua, no hace falta disolvencia.

El acercamiento conserva el estado entre clips (zoom y centro), así que al
pasar de un campo al siguiente la cámara viaja, y al cambiar de pantalla se
abre de vuelta al plano general.
"""
import json
import subprocess

from . import narrar, privacidad
from .anotar import _capa
from .publicar import publicar

FPS = 30
ANCHO, ALTO = 1920, 1080
T_ZOOM = 1.1          # segundos que tarda la cámara en llegar al encuadre nuevo
PLANO_GENERAL = (1.0, 0.5, 0.5)
FUNDIDO_TARJETA = 0.4


def _zoom_seguro(seg, cxp, cyp, zoom_pedido):
    """El máximo zoom que deja las marcas dentro del cuadro (ver montar.py)."""
    marcas = [m["caja"] for m in seg.get("resaltar", [])]
    if not marcas:
        return zoom_pedido
    w, h = seg["tamano"]
    aire = 40
    dx = max(max(abs(x - cxp), abs(x + cw - cxp)) for x, _, cw, _ in marcas) + aire
    dy = max(max(abs(y - cyp), abs(y + ch - cyp)) for _, y, _, ch in marcas) + aire
    tope = min(w / (2 * dx), h / (2 * dy))
    return max(1.0, min(zoom_pedido, tope))


def _estado_enfoque(seg, caja, zoom):
    """(zoom, cx, cy) para mirar `caja` sin sacarla del cuadro."""
    w, h = seg["tamano"]
    if not caja or zoom <= 1.0 + 1e-3:
        return PLANO_GENERAL
    cxp, cyp = caja[0] + caja[2] / 2, caja[1] + caja[3] / 2
    falso = {"tamano": seg["tamano"], "resaltar": [{"caja": caja}]}
    return _zoom_seguro(falso, cxp, cyp, zoom), cxp / w, cyp / h


def _claves(seg, estado_inicial, zoom_pedido):
    """Fotogramas clave del zoom del clip: [(t, (z, cx, cy))].

    La grabación deja una línea de tiempo de enfoques (cada clic, tecleo y
    marca dice dónde estaba la atención y cuándo). La cámara los sigue: se
    acerca a lo que se pulsa o se señala y se abre al cambiar de pantalla.
    Los pasos del esquema antiguo (una marca fija) llegan como un solo enfoque.
    """
    claves = [(0.0, estado_inicial)]
    enfoques = seg.get("enfoques") or []
    if not enfoques and seg.get("kenburns"):
        kb = seg["kenburns"]
        enfoques = [{"t": 0.0, "caja": kb.get("caja"), "zoom": kb.get("zoom", zoom_pedido)}]
    for e in enfoques:
        claves.append((max(e["t"], 0.0), _estado_enfoque(seg, e.get("caja"), e.get("zoom", 1.0))))
    # dos enfoques casi simultáneos (clic + tecleo en el mismo campo): gana el último
    limpias = []
    for t, est in claves:
        if limpias and t - limpias[-1][0] < 0.2:
            limpias[-1] = (limpias[-1][0], est)
        else:
            limpias.append((t, est))
    return limpias


def _filtro_zoom(claves):
    """zoompan sobre video (d=1): un cuadro de salida por cuadro de entrada.

    `in` es el número del cuadro de entrada; como el maestro es CFR a 30 fps,
    in/FPS es el tiempo dentro del clip. Entre cada par de claves se
    interpola con suavizado durante T_ZOOM (o el hueco disponible, si es
    menor) y después se sostiene, con `if` anidados de la última a la primera.
    """
    if len(claves) == 1 and all(abs(a - b) < 1e-3 for a, b in zip(claves[0][1], PLANO_GENERAL)):
        return None  # plano general sostenido: no hay que tocar el cuadro
    t_expr = f"(in/{FPS})"

    def componente(i):
        z0, cx0, cy0 = claves[0][1]
        expr = [f"{z0:.4f}", f"{cx0:.4f}", f"{cy0:.4f}"][i]
        for k in range(1, len(claves)):
            tk, hasta = claves[k]
            desde = claves[k - 1][1]
            dur = T_ZOOM if k + 1 >= len(claves) else max(0.25, min(T_ZOOM, claves[k + 1][0] - tk))
            u = f"(max(0,min(1,({t_expr}-{tk:.3f})/{dur:.3f})))"
            s = f"({u}*{u}*(3-2*{u}))"
            a, b = desde[i], hasta[i]
            tramo = f"({a:.4f}+({b:.4f}-{a:.4f})*{s})"
            expr = f"if(gte({t_expr},{tk:.3f}),{tramo},{expr})"
        return expr

    z, px, py = componente(0), componente(1), componente(2)
    ex = f"max(0,min(iw-iw/zoom,{px}*iw-(iw/zoom)/2))"
    ey = f"max(0,min(ih-ih/zoom,{py}*ih-(ih/zoom)/2))"
    return f"zoompan=z='{z}':x='{ex}':y='{ey}':d=1:s={ANCHO}x{ALTO}:fps={FPS}"


CODEC = ["-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
         "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]


def _clip_video(seg, carpeta, mp3, barra, estado, zoom_pedido, destino, zoom_activo=False):
    # Por defecto NO hay zoom: la marca y el cursor ya dirigen la mirada y el
    # plano fijo se lee como una grabación honesta. `"zoom": true` en el
    # guion enciende la cámara que sigue la acción.
    claves = _claves(seg, estado, zoom_pedido) if zoom_activo else [(0.0, PLANO_GENERAL)]
    hasta = claves[-1][1]
    filtro = _filtro_zoom(claves)
    dur = seg["duracion"]
    entradas = ["-ss", f"{seg['inicio']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(carpeta / seg["master"]), "-i", str(mp3)]
    cadena = [filtro] if filtro else []
    if barra.exists():
        entradas += ["-i", str(barra)]
        video = f"[0:v]{','.join(cadena + ['null'])}[z];[z][2:v]overlay=0:0,format=yuv420p[v]"
    else:
        video = f"[0:v]{','.join(cadena + ['format=yuv420p'])}[v]"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *entradas,
         "-filter_complex", f"{video};[1:a]apad[a]", "-map", "[v]", "-map", "[a]",
         "-t", f"{dur:.3f}", *CODEC, str(destino)], check=True)
    return hasta


def _clip_tarjeta(seg, carpeta, mp3, destino):
    dur = seg["duracion"]
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-loop", "1", "-framerate", str(FPS), "-i", str(carpeta / seg["imagen"]),
         "-i", str(mp3),
         "-filter_complex",
         f"[0:v]scale={ANCHO}:{ALTO},fade=t=in:d={FUNDIDO_TARJETA},"
         f"fade=t=out:st={dur - FUNDIDO_TARJETA:.3f}:d={FUNDIDO_TARJETA},format=yuv420p[v];"
         f"[1:a]apad[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}", *CODEC, str(destino)],
        check=True)


def _unir(clips, destino):
    """Concatena sin recodificar. Escribe a un temporal y reemplaza: en Windows
    el MP4 anterior puede seguir bloqueado unos segundos (antivirus, indexador,
    un reproductor abierto) y ffmpeg moriría al sobrescribirlo."""
    import os
    import time

    lista = destino.with_suffix(".txt")
    lista.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    temporal = destino.with_name(destino.stem + ".tmp.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lista), "-c", "copy", "-movflags", "+faststart",
                    str(temporal)], check=True)
    lista.unlink()
    for intento in range(4):
        try:
            os.replace(temporal, destino)
            return destino
        except PermissionError:
            time.sleep(1.5)
    # sigue bloqueado (un reproductor abierto): se entrega con nombre fechado
    alterno = destino.with_name(f"{destino.stem}-{time.strftime('%Y%m%d-%H%M')}{destino.suffix}")
    os.replace(temporal, alterno)
    print(f"  AVISO: {destino.name} está abierto en otro programa; el video nuevo es {alterno.name}")
    return alterno


MAX_CUE = 84  # caracteres por subtítulo (dos líneas cómodas en 1080p)


def _frases(texto):
    """Parte la narración en trozos de subtítulo: por puntuación fuerte y, si
    un trozo sigue largo, por comas."""
    import re
    trozos = [t.strip() for t in re.split(r"(?<=[.;:!?…])\s+", texto) if t.strip()]
    salida = []
    for t in trozos:
        while len(t) > MAX_CUE:
            corte = t.rfind(",", 0, MAX_CUE)
            if corte < MAX_CUE // 3:
                corte = t.rfind(" ", 0, MAX_CUE)
            if corte <= 0:
                break
            salida.append(t[:corte + 1].strip())
            t = t[corte + 1:].strip()
        if t:
            salida.append(t)
    return salida


def cues(texto, palabras, dur, offset):
    """Subtítulos por frase, con tiempos reales de la voz.

    Los tiempos de palabra vienen de edge-tts; el texto se reparte entre ellos
    en proporción al número de palabras de cada frase, que es suficiente para
    que cada subtítulo entre y salga con lo que se está oyendo.
    """
    frases = _frases(texto)
    if not palabras or len(frases) <= 1:
        return [(offset, offset + dur, texto)] if len(frases) <= 1 else \
            [(offset + dur * i / len(frases), offset + dur * (i + 1) / len(frases), f)
             for i, f in enumerate(frases)]
    total = sum(len(f.split()) for f in frases)
    salida, acumulado = [], 0
    for f in frases:
        n = len(f.split())
        i0 = min(int(round(acumulado / total * len(palabras))), len(palabras) - 1)
        i1 = min(int(round((acumulado + n) / total * len(palabras))) - 1, len(palabras) - 1)
        i1 = max(i1, i0)
        t0 = palabras[i0]["t"]
        t1 = palabras[i1]["t"] + palabras[i1]["d"] + 0.2
        salida.append((offset + t0, offset + min(t1, dur), f))
        acumulado += n
    return salida


def _srt(entradas, destino):
    """`entradas`: (texto, duración del clip, palabras) por paso."""
    def ts(s):
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(s % 1 * 1000):03d}"

    lineas, t, n = [], 0.0, 0
    for texto, dur, palabras in entradas:
        for ini, fin, frase in cues(texto, palabras, dur, t):
            n += 1
            lineas.append(f"{n}\n{ts(ini)} --> {ts(fin)}\n{frase}\n")
        t += dur
    destino.write_text("\n".join(lineas), encoding="utf-8")


def _portada(clips, salida):
    """Un fotograma real del primer clip de pantalla, para la miniatura."""
    destino = salida / "grabacion" / "portada.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.5", "-i", str(clips[0]),
                    "-frames:v", "1", str(destino)], check=True)
    return destino


def montar(guion, salida):
    carpeta = salida / "grabacion"
    segdir = carpeta / "segmentos"
    clips_dir = salida / "clips-video"
    clips_dir.mkdir(parents=True, exist_ok=True)
    mapa_priv = privacidad.cargar_mapa(salida)

    rutas, textos, estado = [], [], PLANO_GENERAL
    portada = None
    for paso in guion["pasos"]:
        pid = paso["id"]
        ruta_seg = segdir / f"{pid}.json"
        if not ruta_seg.exists():
            raise SystemExit(f"Falta la grabación de '{pid}'. Corre: tut grabar")
        seg = json.loads(ruta_seg.read_text(encoding="utf-8"))
        mp3 = salida / "audio" / f"{pid}.mp3"
        if not mp3.exists():
            raise SystemExit(f"Falta el audio de '{pid}'. Corre: tut narrar")
        destino = clips_dir / f"{pid}.mp4"

        if seg["tipo"] == "tarjeta":
            _clip_tarjeta(seg, segdir, mp3, destino)
            estado = PLANO_GENERAL
            print(f"  · {pid}  ({seg['duracion']:.1f}s)  tarjeta")
        else:
            # Sin edición: el video es la grabación tal cual. Las capas (barra
            # de texto, chip de ruta) solo se pintan si el guion las pide con
            # `"capas": true`; la orientación la da la propia pantalla.
            barra = clips_dir / f"{pid}-barra.png"
            if guion.get("capas", False) and (seg.get("texto_pantalla") or seg.get("ruta")):
                al_fondo = any(m["caja"][1] + m["caja"][3] > seg["tamano"][1] * 0.80
                               for m in seg.get("resaltar", []))
                _capa(seg.get("texto_pantalla"), seg.get("ruta"), barra, arriba=al_fondo)
            elif barra.exists():
                barra.unlink()
            pedido = paso.get("kenburns", {}).get("zoom", 1.3)
            zoom_activo = bool(guion.get("zoom", False))
            estado = _clip_video(seg, carpeta, mp3, barra, estado, pedido, destino, zoom_activo)
            n_enf = len(seg.get("enfoques") or [])
            aviso = f"  {n_enf} enfoques" if (n_enf and zoom_activo) else "  plano general"
            print(f"  · {pid}  ({seg['duracion']:.1f}s){aviso}")
            if portada is None:
                portada = destino
        rutas.append(destino)
        side = narrar.sidecar(salida, pid) or {}
        textos.append((privacidad.aplicar_a_texto(paso["narracion"], mapa_priv),
                       seg["duracion"], side.get("palabras", [])))

    print("  unir…")
    final = _unir(rutas, salida / "video.mp4")
    _srt(textos, final.with_suffix(".srt"))
    print(f"\n  → {final}")
    duraciones = [d for _, d, _ in textos]
    publicar(guion, salida, duraciones, 0.0, mapa_priv, sufijo="-video",
             portada=_portada([portada], salida) if portada else None)

    from .verificar import informe
    ruta, avisos = informe(guion, salida, video=final)
    print(f"  → {ruta}" + (f"  ({len(avisos)} avisos)" if avisos else ""))
    for a in avisos:
        print(f"    AVISO {a}")
