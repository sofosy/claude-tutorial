"""Activa el acabado profesional (sonido, entrada/cierre, rótulos) en guiones de la serie Cajas.
Uso: python seeds/cajas/acabado.py cajas-05-cerrar-caja [...]"""
import json, sys
from pathlib import Path

for nombre in sys.argv[1:]:
    p = Path("guiones") / f"{nombre}.json"
    g = json.loads(p.read_text(encoding="utf-8"))
    g["loudnorm"] = {"lufs": -14, "tp": -1.5}
    g["marca_video"] = {"entrada_s": 3, "cierre_s": 3}
    g["rotulo_paso"] = {"segundos": 3.5}
    # la IP local del API se ve en Auditoría: en cámara, una IP de oficina verosímil
    g.setdefault("privacidad", {}).setdefault("mapa_fijo", {})["::1"] = "192.168.1.25"
    p.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("acabado:", nombre)
