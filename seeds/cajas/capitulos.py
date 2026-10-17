"""Título de capítulo (YouTube) y rótulo en pantalla de cada paso de la serie Cajas.
Uso: python seeds/cajas/capitulos.py cajas-05-cerrar-caja [...]  (luego `tut.py montar-video`)"""
import json, sys
from pathlib import Path

TITULOS = {
    "cajas-01-tablero": ["El tablero de cajas", "Crear una caja nueva", "Configuración de cajas"],
    "cajas-02-configuracion": ["Denominaciones", "Políticas: fondo y tolerancias",
                               "Políticas: aprobaciones y cuadre", "Configurar la impresora"],
    "cajas-03-abrir-y-operar": ["Abrir la caja", "Registrar una entrada",
                                "Salida con ITBIS por aprobar", "Movimientos y resumen del turno"],
    "cajas-04-aprobar-y-transferir": ["Aprobar una salida", "Crear una transferencia", "Recibir la transferencia"],
    "cajas-05-cerrar-caja": ["Cerrar la caja", "Ingresar lo contado", "Registrar el conteo"],
    "cajas-06-cuadre-y-desbloqueo": ["Aprobar el cuadre", "Arqueo sorpresa", "Desbloquear una caja"],
    "cajas-07-historial-y-analisis": ["Historial de una caja", "Análisis", "Alertas y auditoría"],
}

for nombre in sys.argv[1:]:
    p = Path("guiones") / f"{nombre}.json"
    g = json.loads(p.read_text(encoding="utf-8"))
    titulos = TITULOS[nombre]
    assert len(titulos) == len(g["pasos"]), f"{nombre}: {len(g['pasos'])} pasos"
    for paso, t in zip(g["pasos"], titulos):
        paso["capitulo"] = t
        paso["rotulo"] = t
    p.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("capítulos:", nombre)
