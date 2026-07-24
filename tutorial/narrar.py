"""C3 — Narración con edge-tts.

Único punto de contacto con el motor de voz: cambiar a ElevenLabs u otro motor
solo toca este archivo (edge-tts usa un endpoint no oficial de Microsoft).
"""
import asyncio
import json
import subprocess

import edge_tts

from . import privacidad

VOZ_DEFECTO = "es-MX-DaliaNeural"
VELOCIDAD_DEFECTO = "-8%"  # la narración técnica se entiende mejor un poco lenta


async def _sintetizar(texto, voz, velocidad, destino):
    com = edge_tts.Communicate(texto, voz, rate=velocidad)
    await com.save(str(destino))


def duracion(archivo):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(archivo)],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


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
        asyncio.run(_sintetizar(texto, vid, vel, mp3))
        duraciones[pid] = duracion(mp3)
        print(f"  · {pid}  ({duraciones[pid]:.1f}s)")

    # se acumula para que --paso no borre las duraciones de los demás
    ruta = dest / "duraciones.json"
    previas = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    previas.update(duraciones)
    ruta.write_text(json.dumps(previas, indent=2), encoding="utf-8")
