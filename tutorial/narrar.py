"""C3 — Narración con edge-tts, ElevenLabs o espeak-ng.

Único punto de contacto con el motor de voz. El motor lo elige el prefijo del
`voz.id`: «eleven:<voice_id>» (clave en ELEVEN_KEY), «espeak:<voz>» o, sin prefijo, una voz de
edge-tts (endpoint no oficial de Microsoft).

Además del MP3, guarda por paso un sidecar `<paso>.json` con:

- `hash` del texto+voz+velocidad: el modo de grabación re-narra SOLO los pasos
  cuya redacción cambió, en vez de regenerar la voz entera cada corrida.
- `palabras`: el instante en que se pronuncia cada palabra (edge-tts lo reporta
  con precisión de milisegundos). Es lo que permite disparar un clic en la
  palabra exacta de la narración y cortar los subtítulos por frase.
"""
import asyncio
import hashlib
import json
import re
import shutil
import subprocess

import tempfile
from pathlib import Path

from . import privacidad

VOZ_DEFECTO = "es-MX-DaliaNeural"
VELOCIDAD_DEFECTO = "-8%"  # la narración técnica se entiende mejor un poco lenta

# ── Cómo se PRONUNCIAN las siglas ──────────────────────────────────────────
#
# La voz sintética lee una sigla en mayúsculas como si fuera una palabra:
# «ITBIS» le sale algo parecido a «ipis», que no es lo que dice nadie en la
# República Dominicana (se dice «itebís»). Escribir «itebís» en el guion
# arreglaría la voz pero ensuciaría el subtítulo, que debe decir ITBIS.
#
# Por eso la sustitución ocurre sólo en el texto que se manda al motor de voz.
# El subtítulo se arma del guion original (`montar_video` usa
# `paso["narracion"]`), así que en pantalla se sigue leyendo la sigla.
#
# El guion o `config.json` pueden ampliar el mapa con la clave `pronunciacion`.
#
# Cuidado al añadir: la sustitución debe conservar el NÚMERO DE PALABRAS —los
# subtítulos se reparten en proporción a las palabras—, así que las siglas que
# se deletrean van con guiones («ene-ce-efe»), no con espacios. Y `al_decir`
# pasa por este mismo mapa antes de buscarse, así que una sigla remapeada
# sigue sirviendo de ancla.
PRONUNCIACION = {
    "ITBIS": "itebís",
    "NCF": "ene-ce-efe",
    "RNC": "erre-ene-ce",
    "DGII": "de-ge-i-i",
    "ARS": "a-erre-ese",
    "SRL": "ese-erre-ele",
    "B01": "be cero uno",
    "B02": "be cero dos",
    "B03": "be cero tres",
    "B04": "be cero cuatro",
}


def para_voz(texto, extra=None):
    """El texto tal como hay que dárselo al motor de voz."""
    mapa = {**PRONUNCIACION, **(extra or {})}
    for sigla, dicho in mapa.items():
        # sólo la sigla suelta: no tocar «B04» dentro de «B0400000001»
        texto = re.sub(rf"(?<![\w-]){re.escape(sigla)}(?![\w-])", dicho, texto)
    return texto


def _sintetizar_espeak(texto, voz, velocidad, destino):
    """Voz offline (espeak-ng + mbrola) para entornos sin acceso a edge-tts.

    Suena más sintética, pero no depende de la red. espeak-ng no reporta el
    instante de cada palabra, así que se sintetiza FRASE por frase (el tiempo
    de cada frase es exacto) y dentro de la frase las palabras se reparten en
    proporción a sus letras: basta para anclar `al_decir` y los subtítulos.

    `voz` = "espeak:<voz>" (p. ej. "espeak:mb-es3"); `velocidad` = "+12%" se
    traduce a palabras por minuto sobre 150.
    """
    nombre = voz.split(":", 1)[1] or "mb-es3"
    pct = int(re.sub(r"[^-+0-9]", "", velocidad) or 0)
    wpm = str(int(150 * (1 + pct / 100)))
    frases = [f.strip() for f in re.split(r"(?<=[.!?…:;])\s+", texto) if f.strip()]
    palabras, t = [], 0.0
    with tempfile.TemporaryDirectory() as tmp:
        lista = []
        for i, frase in enumerate(frases):
            wav = Path(tmp) / f"{i:04d}.wav"
            subprocess.run(["espeak-ng", "-v", nombre, "-s", wpm, "-w", str(wav), frase],
                           check=True, capture_output=True)
            d = duracion(wav)
            lista.append(wav)
            trozos = frase.split()
            pesos = [max(len(re.sub(r"\W", "", w)), 1) + 1 for w in trozos]
            util, cursor = d * 0.92, t + d * 0.03
            for w, peso in zip(trozos, pesos):
                dw = util * peso / sum(pesos)
                palabras.append({"t": round(cursor, 3), "d": round(dw, 3),
                                 "texto": re.sub(r"^\W+|\W+$", "", w) or w})
                cursor += dw
            t += d
        concat = Path(tmp) / "lista.txt"
        concat.write_text("".join(f"file '{w.as_posix()}'\n" for w in lista), encoding="utf-8")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "2", "-f", "concat", "-safe", "0",
                        "-i", str(concat), "-ar", "24000", "-ac", "1", "-b:a", "96k",
                        str(destino)], check=True)
    return palabras


def _jota_ms(mp3, t):
    """ms de fricción sorda desde `t`: distingue «Jermiva» (jota) de «Yermiva».
    Misma medida que salida/comercial-contadores/tools/probar_marca.py."""
    import numpy as np
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                       capture_output=True).stdout
    x = np.frombuffer(b, np.int16).astype(np.float32) / 32768
    fr = 160; i0 = max(0, int((t - 0.08) * 16000) // fr); mejor = 0
    for ini in range(i0, i0 + 12):
        n = 0
        for i in range(ini, ini + 25):
            seg = x[i * fr:(i + 2) * fr]
            if len(seg) < 2 * fr: break
            seg = seg - seg.mean()
            if np.sqrt(np.mean(seg ** 2)) < 0.004: break
            ac = np.correlate(seg, seg, "full")[len(seg) - 1:]
            if ac[0] <= 0 or ac[40:230].max() / ac[0] > 0.45: break
            n += 1
        mejor = max(mejor, n)
    return mejor * 10


def _sintetizar_eleven(texto, voz, destino):
    """ElevenLabs (`voz` = "eleven:<voice_id>", clave en la variable ELEVEN_KEY).

    Pide el audio con marcas por carácter y las agrupa en palabras. La marca se
    dice con JOTA: «Germiva» se manda como «Jermiva» (misma cantidad de palabras)
    y, si la medida de la jota sale corta («Yermiva»), se repite la toma.
    """
    import base64, os, urllib.request
    vid = voz.split(":", 1)[1]
    dicho = re.sub(r"Germiva", "Jermiva", texto)
    cuerpo = json.dumps({"text": dicho, "model_id": "eleven_multilingual_v2", "language_code": "es",
                         "voice_settings": {"stability": 0.45, "similarity_boost": 0.85, "style": 0.30,
                                            "use_speaker_boost": True}}, ensure_ascii=False).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128"
    for intento in range(5):
        req = urllib.request.Request(url, data=cuerpo, headers={"xi-api-key": os.environ["ELEVEN_KEY"],
                                                                 "Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.loads(r.read())
        Path(destino).write_bytes(base64.b64decode(d["audio_base64"]))
        al = d["alignment"]
        anclas = [m.start() for m in re.finditer("Jermiva", dicho)]
        if not anclas: break
        peor = min(_jota_ms(destino, al["character_start_times_seconds"][k]) for k in anclas)
        if peor >= 80: break
        print(f"    jota corta ({peor} ms), repito la toma")
    chars, ini, fin = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    palabras, actual, t0, t1 = [], "", None, None
    for c, a, b in zip(chars + [" "], ini + [0], fin + [0]):
        if c.isspace():
            if actual:
                limpio = re.sub(r"^\W+|\W+$", "", actual) or actual
                palabras.append({"t": round(t0, 3), "d": round(t1 - t0, 3), "texto": limpio})
            actual, t0 = "", None
        else:
            actual += c
            t0 = a if t0 is None else t0
            t1 = b
    return palabras


# ElevenLabs cobra por carácter: el audio ya pagado se guarda por hash de su
# texto aquí (fuera de cada `salida/<tutorial>/`), para que borrar o rehacer
# una salida no vuelva a pagar la misma frase.
CACHE_VOZ = Path(__file__).resolve().parent.parent / "salida" / "_voz"


def _sintetizar_eleven_con_cache(texto, voz, destino):
    clave = hash_narracion(texto, voz, "")
    mp3, js = CACHE_VOZ / f"{clave}.mp3", CACHE_VOZ / f"{clave}.json"
    if mp3.exists() and js.exists():
        shutil.copyfile(mp3, destino)
        return json.loads(js.read_text(encoding="utf-8"))
    palabras = _sintetizar_eleven(texto, voz, destino)
    CACHE_VOZ.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(destino, mp3)
    js.write_text(json.dumps(palabras, ensure_ascii=False), encoding="utf-8")
    return palabras


async def _sintetizar(texto, voz, velocidad, destino):
    """Escribe el MP3 y devuelve las marcas de palabra (segundos)."""
    if voz.startswith("espeak:"):
        return _sintetizar_espeak(texto, voz, velocidad, destino)
    if voz.startswith("eleven:"):
        return _sintetizar_eleven_con_cache(texto, voz, destino)
    import edge_tts  # sólo si se usa: el motor offline no lo necesita
    # edge-tts ≥ 7 manda límites de FRASE por defecto; los de palabra hay que pedirlos
    com = edge_tts.Communicate(texto, voz, rate=velocidad, boundary="WordBoundary")
    palabras = []
    with open(destino, "wb") as f:
        async for trozo in com.stream():
            if trozo["type"] == "audio":
                f.write(trozo["data"])
            elif trozo["type"] == "WordBoundary":
                # offset y duration vienen en unidades de 100 ns
                palabras.append({"t": round(trozo["offset"] / 1e7, 3),
                                 "d": round(trozo["duration"] / 1e7, 3),
                                 "texto": trozo["text"]})
    return palabras


def duracion(archivo):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(archivo)],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def hash_narracion(texto, voz, velocidad):
    return hashlib.sha256(f"{voz}|{velocidad}|{texto}".encode("utf-8")).hexdigest()[:16]


def sidecar(salida, pid):
    ruta = salida / "audio" / f"{pid}.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


def narrar(guion, pasos, salida):
    dest = salida / "audio"
    dest.mkdir(parents=True, exist_ok=True)
    voz = guion.get("voz", {})
    vid = voz.get("id", VOZ_DEFECTO)
    vel = voz.get("velocidad", VELOCIDAD_DEFECTO)

    mapa = privacidad.cargar_mapa(salida)
    duraciones = {}
    for paso in pasos:
        pid = paso["id"]
        mp3 = dest / f"{pid}.mp3"
        texto = privacidad.aplicar_a_texto(paso["narracion"], mapa)
        # lo que se le da a la voz no es lo que se lee en el subtítulo: las
        # siglas van escritas como se pronuncian (ver PRONUNCIACION)
        dicho = para_voz(texto, guion.get("pronunciacion"))
        palabras = asyncio.run(_sintetizar(dicho, vid, vel, mp3))
        duraciones[pid] = duracion(mp3)
        (dest / f"{pid}.json").write_text(json.dumps({
            "hash": hash_narracion(dicho, vid, vel),
            "duracion": duraciones[pid],
            "palabras": palabras,
        }, ensure_ascii=False), encoding="utf-8")
        print(f"  · {pid}  ({duraciones[pid]:.1f}s)")

    # se acumula para que --paso no borre las duraciones de los demás
    ruta = dest / "duraciones.json"
    previas = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    previas.update(duraciones)
    ruta.write_text(json.dumps(previas, indent=2), encoding="utf-8")
