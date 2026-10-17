"""Reúne la serie Cajas en UNA carpeta, numerada en orden de aprendizaje.
Uso (desde claude-tutorial): .venv/Scripts/python.exe seeds/cajas/publicar.py
Destino: germiva/claude-tutoriales/cajas/  (video, subtítulos, texto de YouTube, miniatura, INDICE.md)"""
import json
import re
import shutil
import subprocess
from pathlib import Path

SERIE = [
    "cajas-01-tablero", "cajas-02-configuracion", "cajas-03-abrir-y-operar",
    "cajas-08-cobro-factura",  # 4.º: el cobro de una factura entra a la caja abierta
    "cajas-04-aprobar-y-transferir", "cajas-05-cerrar-caja",
    "cajas-06-cuadre-y-desbloqueo", "cajas-07-historial-y-analisis",
]
RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ.parent / "claude-tutoriales" / "cajas"


def duracion(mp4):
    s = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout
    s = float(s.strip())
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def capitulos(txt):
    bloque = txt.split("CAPÍTULOS", 1)[-1].split("\n\n", 1)[0]
    return [l.strip() for l in bloque.splitlines() if re.match(r"\s*\d\d:\d\d", l)]


DESTINO.mkdir(parents=True, exist_ok=True)
filas, detalle = [], []
for n, nombre in enumerate(SERIE, 1):
    salida = RAIZ / "salida" / nombre
    guion = json.loads((RAIZ / "guiones" / f"{nombre}.json").read_text(encoding="utf-8"))
    base = f"{n:02d}-{nombre.split('-', 2)[2]}"
    shutil.copy2(salida / "video.mp4", DESTINO / f"{base}.mp4")
    shutil.copy2(salida / "video.srt", DESTINO / f"{base}.srt")
    shutil.copy2(salida / "youtube-video.txt", DESTINO / f"{base}-youtube.txt")
    shutil.copy2(salida / "miniatura-video.png", DESTINO / f"{base}-miniatura.png")
    titulo = guion["titulo"].split(" · ", 1)[-1]
    rol = guion["sesion"]["usuario"]
    dur = duracion(salida / "video.mp4")
    filas.append(f"| {n} | [{titulo}]({base}.mp4) | {dur} | {rol} |")
    caps = capitulos((salida / "youtube-video.txt").read_text(encoding="utf-8"))
    detalle.append(f"### {n}. {titulo} ({dur})\n\n" + "\n".join(f"- {c}" for c in caps)
                   + "\n\nAprenderás:\n" + "\n".join(f"- {a}" for a in guion.get("aprenderas", [])))
    print(f"{base}  {dur}")

(DESTINO / "INDICE.md").write_text(
    "# Germiva ERP · Serie de tutoriales: Cajas\n\n"
    "Ocho videos que recorren un día completo de caja, en el orden en que se aprende: "
    "configurar, abrir, operar, cobrar facturas, aprobar, cerrar, cuadrar y consultar. Grabados en vivo sobre "
    "la empresa de demostración «Ferretería El Progreso» (datos ficticios).\n\n"
    "| # | Video | Duración | Lo graba el rol |\n|---|---|---|---|\n" + "\n".join(filas)
    + "\n\nCada video trae su `.srt` (subtítulos), `-youtube.txt` (título, descripción y "
    "capítulos) y `-miniatura.png`.\n\n## Capítulos\n\n" + "\n\n".join(detalle)
    + "\n\n---\nMúsica: «Elevator Music» de Alex McCulloch (CC0, OpenGameArt). Tipografía: Inter (OFL).\n",
    encoding="utf-8")
print("->", DESTINO)
