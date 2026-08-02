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
    for c in ETAPAS + ("auditar", "ofuscar", "revisar", "mapa"):
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

    if a.cmd == "revisar":
        raise SystemExit(_revisar(guion))

    if a.cmd == "ofuscar":
        cfg = guion.get("privacidad", {})
        tapados = m_privacidad.ofuscar(
            salida, ids={p["id"] for p in guion["pasos"]},
            permitidos=cfg.get("permitidos", ()),
            declarados=cfg.get("ofuscar", ()))
        for origen, tipo, valor in tapados:
            print(f"  tapado  {origen}\t{tipo}\t{valor}")
        print(f"\n  {len(tapados)} valores cubiertos."
              + (" Vuelve a montar para que entren al video."
                 if tapados else " No había nada que tapar."))
        return

    if a.cmd == "auditar":
        hallazgos = m_privacidad.auditar(
            salida, [salida / "youtube.txt", salida / "final.srt"],
            ids={p["id"] for p in guion["pasos"]},
            permitidos=guion.get("privacidad", {}).get("permitidos", ()))
        for origen, tipo, valor in hallazgos:
            print(f"  {origen}\t{tipo}\t{valor}")
        print(f"\n  {len(hallazgos)} posibles datos reales"
              f" → {salida / 'auditoria.txt'}")
        raise SystemExit(1 if hallazgos else 0)

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
