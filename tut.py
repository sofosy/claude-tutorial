#!/usr/bin/env python3
"""Generador de video tutoriales. Ver PLAN.md."""
import argparse
import sys

# La consola de Windows usa cp1252 y el progreso se imprime con «·», flechas y
# acentos: sin esto, el motor muere con UnicodeEncodeError DESPUÉS de haber
# capturado o narrado, y el fallo aparenta ser del paso y no de la terminal.
for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

from tutorial import anotar as m_anotar
from tutorial import capturar as m_capturar
from tutorial import grabar as m_grabar
from tutorial import mapa as m_mapa
from tutorial import montar as m_montar
from tutorial import montar_video as m_montar_video
from tutorial import narrar as m_narrar
from tutorial import privacidad as m_privacidad
from tutorial.rutas import cargar_guion, dir_salida, pasos_filtrados

ETAPAS = ("capturar", "anotar", "narrar", "montar", "build")
# Modo de grabación en vivo (ver GRABACION.md): `video` = grabar + montar-video.
GRABACION = ("grabar", "montar-video", "video")


def _revisar(guion):
    """Analiza el guion y reporta datos que parecen reales sin declarar.

    Devuelve 1 si hay hallazgos, para poder usarlo como código de salida.
    """
    hallazgos = m_privacidad.revisar_guion(guion)
    for donde, tipo, valor in hallazgos:
        print(f"  guion  {donde}\t{tipo}\t{valor}")
    if hallazgos:
        print(f"\n  {len(hallazgos)} datos sin declarar en el guion."
              " Agrégalos a privacidad.permitidos (dato de demo)"
              " o a privacidad.ofuscar (se tapa en los frames).")
    return 1 if hallazgos else 0


def main():
    ap = argparse.ArgumentParser(prog="tut")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ETAPAS + GRABACION + ("auditar", "ofuscar", "revisar", "verificar", "mapa"):
        p = sub.add_parser(c)
        p.add_argument("tutorial")
        if c in ETAPAS + GRABACION and c not in ("montar", "montar-video"):
            p.add_argument("--paso", help="rehacer solo el paso con este prefijo")
        if c == "auditar":
            p.add_argument("--video", action="store_true",
                           help="auditar fotogramas de video.mp4 (modo grabación)")
    sub.add_parser("cobertura")

    a = ap.parse_args()

    if a.cmd == "cobertura":
        raise SystemExit(1 if m_mapa.cobertura() else 0)

    guion = cargar_guion(a.tutorial)
    salida = dir_salida(a.tutorial)

    if a.cmd == "mapa":
        m_mapa.construir(guion)
        return

    if a.cmd == "revisar":
        raise SystemExit(_revisar(guion))

    if a.cmd == "verificar":
        from tutorial import verificar as m_verificar
        hallazgos = m_verificar.revisar_guion(guion)
        for nivel, paso, texto in hallazgos:
            print(f"  {nivel:5} {paso}\t{texto}")
        errores = sum(1 for n, _, _ in hallazgos if n == "ERROR")
        print(f"\n  {errores} errores, {len(hallazgos) - errores} avisos"
              " — regla: cada clic y cada vista se explican.")
        raise SystemExit(1 if errores else 0)

    if a.cmd == "ofuscar":
        cfg = guion.get("privacidad", {})
        tapados = m_privacidad.ofuscar(
            salida, ids={p["id"] for p in guion["pasos"]},
            permitidos=cfg.get("permitidos", ()),
            declarados=cfg.get("ofuscar", ()),
            binario=guion.get("tesseract"))
        for origen, tipo, valor in tapados:
            print(f"  tapado  {origen}\t{tipo}\t{valor}")
        print(f"\n  {len(tapados)} valores cubiertos."
              + (" Vuelve a montar para que entren al video."
                 if tapados else " No había nada que tapar."))
        return

    if a.cmd == "auditar":
        if a.video:
            # un fotograma cada 2 s del video final: cada paso dura más que eso,
            # así que ninguna pantalla se queda sin revisar
            import subprocess
            carpeta = salida / "auditoria-video"
            carpeta.mkdir(exist_ok=True)
            for viejo in carpeta.glob("*.png"):
                viejo.unlink()
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(salida / "video.mp4"),
                            "-vf", "fps=1/2", str(carpeta / "%05d.png")], check=True)
            hallazgos = m_privacidad.auditar(
                salida, [salida / "youtube-video.txt", salida / "video.srt"],
                permitidos=guion.get("privacidad", {}).get("permitidos", ()),
                binario=guion.get("tesseract"), carpeta=carpeta,
                informe="auditoria-video.txt")
            nombre = "auditoria-video.txt"
        else:
            hallazgos = m_privacidad.auditar(
                salida, [salida / "youtube.txt", salida / "final.srt"],
                ids={p["id"] for p in guion["pasos"]},
                permitidos=guion.get("privacidad", {}).get("permitidos", ()),
                binario=guion.get("tesseract"))
            nombre = "auditoria.txt"
        for origen, tipo, valor in hallazgos:
            print(f"  {origen}\t{tipo}\t{valor}")
        print(f"\n  {len(hallazgos)} posibles datos reales"
              f" → {salida / nombre}")
        raise SystemExit(1 if hallazgos else 0)

    if a.cmd in GRABACION:
        if a.cmd != "montar-video":
            from tutorial import verificar as m_verificar
            for nivel, paso, texto in m_verificar.revisar_guion(guion):
                print(f"  {nivel:5} {paso}\t{texto}")
            pasos = pasos_filtrados(guion, getattr(a, "paso", None))
            print("G1 grabar")
            m_grabar.grabar(guion, pasos, salida)
        if a.cmd != "grabar":
            print("G2 montar")
            m_montar_video.montar(guion, salida)
        return

    if a.cmd in ("capturar", "build"):
        _revisar(guion)

    pasos = pasos_filtrados(guion, getattr(a, "paso", None))
    if a.cmd in ("capturar", "build"):
        print("C1 capturar")
        m_capturar.capturar(guion, pasos, salida)
    if a.cmd in ("anotar", "build"):
        print("C2 anotar")
        m_anotar.anotar(pasos, salida)
    if a.cmd in ("narrar", "build"):
        print("C3 narrar")
        m_narrar.narrar(guion, pasos, salida)
    if a.cmd in ("montar", "build"):
        print("C4 montar")
        m_montar.montar(guion, salida)


if __name__ == "__main__":
    main()
