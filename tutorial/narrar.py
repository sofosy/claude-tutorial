"""C3 — Narración con edge-tts.

Único punto de contacto con el motor de voz: cambiar a ElevenLabs u otro motor
solo toca este archivo (edge-tts usa un endpoint no oficial de Microsoft).

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
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                        "-i", str(concat), "-ar", "24000", "-ac", "1", "-b:a", "96k",
                        str(destino)], check=True)
    return palabras


async def _sintetizar(texto, voz, velocidad, destino):
    """Escribe el MP3 y devuelve las marcas de palabra (segundos)."""
    if voz.startswith("espeak:"):
        return _sintetizar_espeak(texto, voz, velocidad, destino)
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
