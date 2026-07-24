#!/usr/bin/env python3
"""Generador de video tutoriales. Ver PLAN.md."""
import argparse

from tutorial import anotar as m_anotar
from tutorial import capturar as m_capturar
from tutorial import mapa as m_mapa
from tutorial import montar as m_montar
from tutorial import narrar as m_narrar
from tutorial import privacidad as m_privacidad
from tutorial.rutas import cargar_guion, dir_salida, pasos_filtrados

ETAPAS = ("capturar", "anotar", "narrar", "montar", "build")


def main():
    ap = argparse.ArgumentParser(prog="tut")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ETAPAS + ("auditar", "mapa"):
        p = sub.add_parser(c)
        p.add_argument("tutorial")
        if c in ETAPAS and c != "montar":
            p.add_argument("--paso", help="rehacer solo el paso con este prefijo")
    sub.add_parser("cobertura")

    a = ap.parse_args()

    if a.cmd == "cobertura":
        raise SystemExit(1 if m_mapa.cobertura() else 0)

    guion = cargar_guion(a.tutorial)
    salida = dir_salida(a.tutorial)

    if a.cmd == "mapa":
        m_mapa.construir(guion)
        return

    if a.cmd == "auditar":
        hallazgos = m_privacidad.auditar(
            salida, [salida / "youtube.txt", salida / "final.srt"],
            ids={p["id"] for p in guion["pasos"]})
        for origen, tipo, valor in hallazgos:
            print(f"  {origen}\t{tipo}\t{valor}")
        print(f"\n  {len(hallazgos)} posibles datos reales"
              f" → {salida / 'auditoria.txt'}")
        raise SystemExit(1 if hallazgos else 0)

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
