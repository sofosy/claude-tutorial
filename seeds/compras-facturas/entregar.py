"""Copia los videos de la serie «Compras · Entrada de facturas» a entregas/compras-facturas/ y arma INDICE.md.
    python3 seeds/compras-facturas/entregar.py [NN ...]
Sin argumentos entrega todos los que tengan video.mp4 en salida/. El índice se rehace siempre con lo que haya en entregas/."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "entregas" / "compras-facturas"
SERIE = "compras-facturas-"


def duracion(mp4):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(mp4)],
                       capture_output=True, text=True, check=True)
    s = round(float(r.stdout.strip()))
    return f"{s // 60}:{s % 60:02d}"


def entregar(solo):
    DESTINO.mkdir(parents=True, exist_ok=True)
    for salida in sorted((RAIZ / "salida").glob(f"{SERIE}*")):
        corto = salida.name[len(SERIE):]
        if solo and corto[:2] not in solo:
            continue
        if not (salida / "video.mp4").exists():
            continue
        for origen, sufijo in (("video.mp4", ".mp4"), ("video.srt", ".srt"), ("youtube-video.txt", "-youtube.txt"),
                               ("miniatura-video.png", "-miniatura.png")):
            if (salida / origen).exists():
                shutil.copy2(salida / origen, DESTINO / f"{corto}{sufijo}")
        print("entregado", corto)


def seccion(texto, titulo):
    m = re.search(rf"{titulo}\n(.*?)(?:\n\n|\Z)", texto, re.S)
    return m.group(1).strip().splitlines() if m else []


def indice():
    filas, detalle = [], []
    for mp4 in sorted(DESTINO.glob("[0-9][0-9]-*.mp4")):
        corto = mp4.stem
        yt = (DESTINO / f"{corto}-youtube.txt").read_text(encoding="utf-8")
        titulo = yt.split("\n")[2].strip()
        nombre = titulo.split(":", 1)[1].strip() if ":" in titulo else titulo
        nombre = nombre[0].upper() + nombre[1:]
        dur = duracion(mp4)
        n = int(corto[:2])
        filas.append(f"| {n} | [{nombre}]({mp4.name}) | {dur} |")
        caps = [c.strip() for c in seccion(yt, "⏱️ CAPÍTULOS")]
        apr = [a.strip().lstrip("•").strip() for a in seccion(yt, "📋 EN ESTE VIDEO APRENDERÁS")]
        detalle.append(f"### {n}. {nombre} ({dur})\n\n" + "\n".join(f"- {c}" for c in caps)
                       + "\n\nAprenderás:\n" + "\n".join(f"- {a}" for a in apr) + "\n")
    texto = (
        "# Germiva ERP · Serie de tutoriales: Compras — entrada de facturas\n\n"
        "Once videos cortos sobre todas las formas de dar entrada a una factura de compra, grabados en vivo sobre la "
        "empresa de demostración «Ferretería Germiva» (datos ficticios, RNC del rango 130555) con las pantallas de "
        "noviembre de 2026 y la misma voz de la serie de Productos.\n\n"
        "La regla que ordena la serie: ¿el comprobante lo emitió el proveedor? Va al buzón de **Facturas Recibidas** "
        "(videos 2 a 6). ¿Ya recibiste la mercancía con su orden? Desde la **recepción** (videos 7 y 8). ¿Lo emite tu "
        "empresa? **Nueva Factura** (videos 9 a 11).\n\n"
        "| # | Video | Duración |\n|---|---|---|\n" + "\n".join(filas) + "\n\n"
        "Cada video trae su `.srt` (subtítulos), `-youtube.txt` (título, descripción y capítulos) y `-miniatura.png`.\n"
        "Los guiones (`guiones/compras-facturas-NN-*.json`) se generan desde `seeds/compras-facturas/_guiones.py`. "
        "Datos de partida: `node seeds/compras-facturas/preparar.mjs A|B` (el video 4 lee la factura con IA: exporta "
        "`OPENAI_API_KEY` antes; la clave solo se guarda en la base local). Los archivos que se suben salen de "
        "`seeds/compras-facturas/archivos.py` y `factura-ferremateriales.html`.\n\n"
        "## Capítulos\n\n" + "\n".join(detalle)
    )
    (DESTINO / "INDICE.md").write_text(texto, encoding="utf-8")
    print("índice con", len(filas), "videos")


if __name__ == "__main__":
    entregar(set(sys.argv[1:]))
    indice()
