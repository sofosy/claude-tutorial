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
from .tarjeta import render_marca, render_rotulo

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


def _cadena_musica(entradas, i_next, musica, dur, salida_voz):
    """Añade la entrada de música (ya recortada a `dur` en su `offset` dentro
    de la pista preparada) y la mezcla bajo `salida_voz`. Devuelve
    (entradas, filtro_extra, etiqueta_audio_final).

    Sin `musica`, no toca nada: entradas y filtro quedan igual que hoy.
    """
    if not musica:
        return entradas, "", salida_voz
    entradas = entradas + ["-ss", f"{musica['offset']:.3f}", "-t", f"{dur:.3f}",
                            "-i", str(musica["pista"])]
    i_mus = i_next
    if musica["ducking"]:
        # la voz (ya con apad) comprime la música: baja sola cuando se habla
        # (una etiqueta de filtro se consume una sola vez: la voz se duplica)
        mezcla = (f"[{salida_voz}]asplit=2[{salida_voz}_sc][{salida_voz}_mx];"
                  f"[{i_mus}:a][{salida_voz}_sc]sidechaincompress="
                  f"threshold=0.05:ratio=8:attack=5:release=400[mus]")
        salida_voz = f"{salida_voz}_mx"
    else:
        mezcla = f"[{i_mus}:a]anull[mus]"
    mezcla += f";[{salida_voz}][mus]amix=inputs=2:duration=first:normalize=0[a]"
    return entradas, ";" + mezcla, "a"


def _clip_video(seg, carpeta, mp3, barra, estado, zoom_pedido, destino, zoom_activo=False, musica=None,
                rotulo=None):
    # Por defecto NO hay zoom: la marca y el cursor ya dirigen la mirada y el
    # plano fijo se lee como una grabación honesta. `"zoom": true` en el
    # guion enciende la cámara que sigue la acción.
    claves = _claves(seg, estado, zoom_pedido) if zoom_activo else [(0.0, PLANO_GENERAL)]
    hasta = claves[-1][1]
    filtro = _filtro_zoom(claves)
    dur = seg["duracion"]
    entradas = ["-ss", f"{seg['inicio']:.3f}", "-t", f"{dur:.3f}",
                "-i", str(carpeta / seg["master"]), "-i", str(mp3)]
    i_next = 2
    cadena = [filtro] if filtro else []
    if barra.exists():
        entradas += ["-i", str(barra)]
        i_next += 1
        video = f"[0:v]{','.join(cadena + ['null'])}[z];[z][2:v]overlay=0:0,format=yuv420p[v]"
    else:
        video = f"[0:v]{','.join(cadena + ['format=yuv420p'])}[v]"
    if rotulo:
        entradas, video, i_next = _con_rotulo(entradas, video, i_next, rotulo, dur)
    entradas, extra, salida_audio = _cadena_musica(entradas, i_next, musica, dur, "voz")
    audio = f"[1:a]apad[voz]{extra}"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *entradas,
         "-filter_complex", f"{video};{audio}", "-map", "[v]", "-map", f"[{salida_audio}]",
         "-t", f"{dur:.3f}", *CODEC, str(destino)], check=True)
    return hasta


# ── Rótulo de paso (`rotulo_paso`) ────────────────────────────────────────
ROTULO_MARGEN_X = 112   # pasa la franja de iconos del menú lateral (90 px)
ROTULO_MARGEN_Y = 34    # aire sobre el borde inferior del cuadro
ROTULO_ENTRA = 0.35     # aparece tras el primer tercio de segundo
ROTULO_FUNDIDO = 0.4


def _con_rotulo(entradas, video, i_next, rotulo, dur):
    """Encadena el rótulo del paso DESPUÉS del zoom y de la barra: se pinta
    sobre el cuadro final, así que el acercamiento no lo mueve ni lo agranda.
    Entra y sale con fundido de opacidad y deja de existir a los `segundos`."""
    seg_r = min(rotulo["segundos"], dur - 0.3)
    if seg_r < 1.0:
        return entradas, video, i_next
    entradas = entradas + ["-loop", "1", "-framerate", str(FPS), "-t", f"{seg_r:.3f}",
                           "-i", str(rotulo["png"])]
    _, h = rotulo["tam"]
    video = (video[:-len("[v]")] + "[b];"
             f"[{i_next}:v]format=rgba,"
             f"fade=t=in:st={ROTULO_ENTRA:.2f}:d={ROTULO_FUNDIDO}:alpha=1,"
             f"fade=t=out:st={seg_r - ROTULO_FUNDIDO:.3f}:d={ROTULO_FUNDIDO}:alpha=1[rt];"
             f"[b][rt]overlay={ROTULO_MARGEN_X}:{ALTO - ROTULO_MARGEN_Y - h}:eof_action=pass,"
             f"format=yuv420p[v]")
    return entradas, video, i_next + 1


def _rotulo_conf(guion):
    r = guion.get("rotulo_paso")
    if not r:
        return None
    return {"segundos": float((r if isinstance(r, dict) else {}).get("segundos", 3.5))}


def _portada_limpia(seg, carpeta, barra, destino_png):
    """Portada SIN rótulo: el mismo cuadro que `_portada` toma del primer clip
    (1,5 s), sacado del maestro con la barra (si la hay) y sin el rótulo, para
    que la miniatura no cambie al encender `rotulo_paso`. No reaplica el zoom:
    a 1,5 s del primer paso la cámara está en el plano general."""
    entradas = ["-ss", f"{seg['inicio']:.3f}", "-t", "1.534", "-i", str(carpeta / seg["master"])]
    if barra.exists():
        entradas += ["-i", str(barra)]
        filtro = f"[0:v]scale={ANCHO}:{ALTO}[z];[z][1:v]overlay=0:0[v]"
    else:
        filtro = f"[0:v]scale={ANCHO}:{ALTO}[v]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "2", *entradas,
                    "-filter_complex", filtro, "-map", "[v]", "-update", "1",
                    str(destino_png)], check=True)
    return destino_png


# ── Entrada y cierre de marca (`marca_video`) ────────────────────────────
REALCE_MUSICA_DB = 3.0   # sin voz encima, la música sube apenas en entrada/cierre
RAMPA_MUSICA = 1.0       # segundos en que vuelve a su nivel junto a la narración


def _marca_conf(guion):
    m = guion.get("marca_video")
    if not m:
        return None
    m = m if isinstance(m, dict) else {}
    return {"entrada_s": float(m.get("entrada_s", 3.0)), "cierre_s": float(m.get("cierre_s", 3.0))}


def _clip_marca(png, dur, destino, musica, tipo):
    """Imagen fija de marca + música (si hay) o silencio; nunca voz.

    Entrada: aparece desde blanco (el fondo es claro) y vuelve a blanco justo
    antes de la app. Cierre: aparece desde blanco y termina en negro. La
    música sube `REALCE_MUSICA_DB` mientras no hay voz y vuelve a su nivel en
    una rampa de `RAMPA_MUSICA` del lado donde está la narración."""
    fi, fo = (0.6, 0.45) if tipo == "entrada" else (0.45, 1.0)
    color_fin = "white" if tipo == "entrada" else "black"
    entradas = ["-loop", "1", "-framerate", str(FPS), "-i", str(png)]
    k = 10 ** (REALCE_MUSICA_DB / 20)
    r = min(RAMPA_MUSICA, dur / 2)
    if tipo == "entrada":
        gan = f"if(lt(t,{dur - r:.3f}),{k:.4f},{k:.4f}+(1-{k:.4f})*(t-{dur - r:.3f})/{r:.3f})"
    else:
        gan = f"if(lt(t,{r:.3f}),1+({k:.4f}-1)*t/{r:.3f},{k:.4f})"
    if musica:
        entradas += ["-ss", f"{musica['offset']:.3f}", "-t", f"{dur:.3f}", "-i", str(musica["pista"])]
        audio = f"[1:a]volume=volume='{gan}':eval=frame,apad[a]"
    else:
        entradas += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]
        audio = "[1:a]apad[a]"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-threads", "2", *entradas,
         "-filter_complex",
         f"[0:v]scale={ANCHO}:{ALTO},fade=t=in:d={fi}:color=white,"
         f"fade=t=out:st={dur - fo:.3f}:d={fo}:color={color_fin},format=yuv420p[v];{audio}",
         "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}", *CODEC, str(destino)], check=True)


# ── Sonoridad final (`loudnorm`) ─────────────────────────────────────────
def _loudnorm_conf(guion):
    cfg = guion.get("loudnorm")
    if not cfg:
        return None
    cfg = cfg if isinstance(cfg, dict) else {}
    return {"lufs": float(cfg.get("lufs", -14)), "tp": float(cfg.get("tp", -1.5))}


def _json_loudnorm(stderr):
    import re
    return json.loads(re.findall(r"\{[^{}]*\}", stderr)[-1])


def _normalizar_sonoridad(video, cfg):
    """Dos pasadas: la primera mide el audio del video montado con `loudnorm`;
    la segunda aplica UNA ganancia lineal que lo lleva a `lufs`. El video se
    copia tal cual (`-c:v copy`); solo se recodifica el audio, con los mismos
    parámetros del montaje, así que la duración no cambia.

    Si esa ganancia deja los picos bajo `tp`, se aplica con `loudnorm`
    linear=true. Si no cabe (voz TTS con algún pico suelto), `loudnorm` caería
    solo al modo dinámico y comprimiría toda la voz; en su lugar se aplica la
    misma ganancia con `volume` y un limitador rápido que solo toca esos
    picos (alimiter con compensación de latencia: no corre el audio)."""
    import os

    base = f"loudnorm=I={cfg['lufs']}:TP={cfg['tp']}"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-threads", "2", "-i", str(video),
                        "-vn", "-af", f"{base}:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    m = _json_loudnorm(r.stderr)
    ganancia = cfg["lufs"] - float(m["input_i"])
    if float(m["input_tp"]) + ganancia <= cfg["tp"] - 0.1:
        modo = "loudnorm lineal"
        # el modo lineal exige que el rango medido quepa en el objetivo: se le da
        lra = max(11.0, min(50.0, float(m["input_lra"]) + 1.0))
        filtro = (f"{base}:LRA={lra:.1f}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
                  f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
                  f":offset={m['target_offset']}:linear=true")
    else:
        modo = "ganancia lineal + limitador de picos"
        # medio dB de margen: el AAC puede subir un poco el pico real
        techo = 10 ** ((cfg["tp"] - 0.5) / 20)
        filtro = (f"volume={ganancia:.2f}dB,aresample=192000,"
                  f"alimiter=limit={techo:.4f}:attack=5:release=50:level=false:latency=true,"
                  f"aresample=44100")
    temporal = video.with_name(video.stem + ".ln.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-threads", "2",
                        "-i", str(video), "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", filtro,
                        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                        "-movflags", "+faststart", str(temporal)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit(f"la normalización de sonoridad falló:\n{r.stderr[-1500:]}")
    os.replace(temporal, video)
    print(f"  sonoridad: {m['input_i']} LUFS (pico {m['input_tp']} dBTP) → "
          f"{cfg['lufs']} LUFS / {cfg['tp']} dBTP · {ganancia:+.1f} dB, {modo}")
    return m


def _clip_tarjeta(seg, carpeta, mp3, destino, musica=None):
    dur = seg["duracion"]
    entradas = ["-loop", "1", "-framerate", str(FPS), "-i", str(carpeta / seg["imagen"]),
                "-i", str(mp3)]
    entradas, extra, salida_audio = _cadena_musica(entradas, 2, musica, dur, "voz")
    audio = f"[1:a]apad[voz]{extra}"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", *entradas,
         "-filter_complex",
         f"[0:v]scale={ANCHO}:{ALTO},fade=t=in:d={FUNDIDO_TARJETA},"
         f"fade=t=out:st={dur - FUNDIDO_TARJETA:.3f}:d={FUNDIDO_TARJETA},format=yuv420p[v];"
         f"{audio}",
         "-map", "[v]", "-map", f"[{salida_audio}]", "-t", f"{dur:.3f}", *CODEC, str(destino)],
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


def _srt(entradas, destino, inicio=0.0):
    """`entradas`: (texto, duración del clip, palabras) por paso. `inicio`
    corre todo (la entrada de marca va antes del primer paso)."""
    def ts(s):
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(s % 1 * 1000):03d}"

    lineas, t, n = [], inicio, 0
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


def _musica_conf(guion):
    """`musica` opcional (config.json o guion; el guion pisa la config, igual
    que `voz`). Sin la clave, no se toca nada del montaje de hoy."""
    m = guion.get("musica")
    if not m or not m.get("archivo"):
        return None
    return {
        "archivo": m["archivo"],
        "volumen_db": m.get("volumen_db", -24),
        "ducking": m.get("ducking", True),
        "fade_s": float(m.get("fade_s", 2.0)),
    }


def _duracion_total(guion, segdir):
    total = 0.0
    for paso in guion["pasos"]:
        ruta_seg = segdir / f"{paso['id']}.json"
        if ruta_seg.exists():
            total += json.loads(ruta_seg.read_text(encoding="utf-8"))["duracion"]
    return total


def _preparar_musica(cfg, total, carpeta):
    """Arma UNA pista continua del largo exacto del video (la fuente se repite
    en bucle con `-stream_loop`), ya con su volumen y sus fundidos de entrada
    y salida — así cada clip solo recorta su tramo (`-ss offset -t dur`) y el
    fundido cae, sin más cuentas, en el primer y el último clip."""
    destino = carpeta / "musica.wav"
    fade = min(cfg["fade_s"], total / 2) if total > 0 else 0.0
    filtro = f"volume={cfg['volumen_db']}dB"
    if fade > 0:
        filtro += (f",afade=t=in:d={fade:.3f},"
                   f"afade=t=out:st={max(0.0, total - fade):.3f}:d={fade:.3f}")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-stream_loop", "-1", "-i", str(cfg["archivo"]),
         "-t", f"{total:.3f}", "-af", filtro,
         "-ar", "44100", "-ac", "2", str(destino)], check=True)
    return destino


def montar(guion, salida):
    carpeta = salida / "grabacion"
    segdir = carpeta / "segmentos"
    clips_dir = salida / "clips-video"
    clips_dir.mkdir(parents=True, exist_ok=True)
    mapa_priv = privacidad.cargar_mapa(salida)

    marca_cfg = _marca_conf(guion)
    rotulo_cfg = _rotulo_conf(guion)
    entrada_s = marca_cfg["entrada_s"] if marca_cfg else 0.0
    cierre_s = marca_cfg["cierre_s"] if marca_cfg else 0.0

    musica_cfg = _musica_conf(guion)
    pista_musica = None
    if musica_cfg:
        pista_musica = _preparar_musica(
            musica_cfg, entrada_s + _duracion_total(guion, segdir) + cierre_s, carpeta)

    rutas, textos, estado = [], [], PLANO_GENERAL
    portada = None
    portada_png = None
    offset = entrada_s
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
        musica = ({"pista": pista_musica, "offset": offset, "ducking": musica_cfg["ducking"]}
                  if pista_musica else None)

        if seg["tipo"] == "tarjeta":
            _clip_tarjeta(seg, segdir, mp3, destino, musica=musica)
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
            rotulo = None
            # `rotulo` explícito; si no, lo que va antes del primer « · » de
            # `texto_pantalla` («Pantalla · detalle»): un rótulo es un título
            texto_r = ""
            if rotulo_cfg:
                texto_r = paso.get("rotulo") or (paso.get("texto_pantalla") or "").split(" · ")[0]
            if texto_r:
                png_r = clips_dir / f"{pid}-rotulo.png"
                tam_r = render_rotulo(privacidad.aplicar_a_texto(texto_r, mapa_priv), png_r, ALTO, ANCHO)
                rotulo = {"png": png_r, "tam": tam_r, "segundos": rotulo_cfg["segundos"]}
            estado = _clip_video(seg, carpeta, mp3, barra, estado, pedido, destino, zoom_activo,
                                  musica=musica, rotulo=rotulo)
            n_enf = len(seg.get("enfoques") or [])
            aviso = f"  {n_enf} enfoques" if (n_enf and zoom_activo) else "  plano general"
            print(f"  · {pid}  ({seg['duracion']:.1f}s){aviso}")
            if portada is None:
                portada = destino
                if rotulo:  # la miniatura sale del cuadro SIN rótulo
                    portada_png = _portada_limpia(seg, carpeta, barra,
                                                  salida / "grabacion" / "portada.png")
        offset += seg["duracion"]
        rutas.append(destino)
        side = narrar.sidecar(salida, pid) or {}
        textos.append((privacidad.aplicar_a_texto(paso["narracion"], mapa_priv),
                       seg["duracion"], side.get("palabras", [])))

    cuerpo = None
    if marca_cfg:
        marca = guion.get("marca") or {}
        datos = {"logo": marca.get("logo"), "simbolo": marca.get("simbolo"), "titulo": guion["titulo"],
                 "url": guion.get("url_publica"), "slogan": marca.get("slogan")}
        piezas = {}
        for tipo, dur, t0 in (("entrada", entrada_s, 0.0), ("cierre", cierre_s, offset)):
            if dur <= 0:
                continue
            png = clips_dir / f"_{tipo}.png"
            render_marca(tipo, datos, png)
            piezas[tipo] = clips_dir / f"_{tipo}.mp4"
            _clip_marca(png, dur, piezas[tipo],
                        {"pista": pista_musica, "offset": t0} if pista_musica else None, tipo)
            print(f"  · {tipo} de marca  ({dur:.1f}s)")
        print("  unir…")
        # los pasos se unen aparte: el informe mide los clics contra la línea
        # de tiempo de los pasos, que no sabe de la entrada puesta delante
        cuerpo = _unir(rutas, carpeta / "cuerpo.mp4")
        final = _unir([c for c in (piezas.get("entrada"), cuerpo, piezas.get("cierre")) if c],
                      salida / "video.mp4")
    else:
        print("  unir…")
        final = _unir(rutas, salida / "video.mp4")
    loud_cfg = _loudnorm_conf(guion)
    if loud_cfg:
        _normalizar_sonoridad(final, loud_cfg)
    _srt(textos, final.with_suffix(".srt"), inicio=entrada_s)
    print(f"\n  → {final}")
    duraciones = [d for _, d, _ in textos]
    if marca_cfg and duraciones:
        # capítulos: el primero sigue en 00:00 (YouTube lo exige) y absorbe la
        # entrada; los demás se corren `entrada_s`; el último absorbe el cierre
        duraciones[0] += entrada_s
        duraciones[-1] += cierre_s
    publicar(guion, salida, duraciones, 0.0, mapa_priv, sufijo="-video",
             portada=(portada_png or _portada([portada], salida)) if portada else None)

    from .verificar import informe
    ruta, avisos = informe(guion, salida, video=cuerpo or final)
    if cuerpo:
        cuerpo.unlink(missing_ok=True)
    print(f"  → {ruta}" + (f"  ({len(avisos)} avisos)" if avisos else ""))
    for a in avisos:
        print(f"    AVISO {a}")
