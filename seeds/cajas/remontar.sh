#!/usr/bin/env bash
# Remonta (sin regrabar) los videos dados, uno a uno, y pasa la puerta 2. Log: seeds/cajas/remontar.log
set -u
cd "$(dirname "$0")/../.."
LOCK=seeds/_puertas/NAVEGADOR.lock; YO="REMONTANDO serie-cajas $$"; LOG=seeds/cajas/remontar.log
until ( set -o noclobber; echo "$YO" > "$LOCK" ) 2>/dev/null; do sleep 15; done
trap '[ "$(cat "$LOCK" 2>/dev/null)" = "$YO" ] && rm -f "$LOCK"' EXIT
for g in "$@"; do
  echo "[$(date +%H:%M:%S)] ── $g" >> "$LOG"
  .venv/Scripts/python.exe tut.py montar-video "$g" > "salida/$g/remontar.log" 2>&1 || echo "   MONTAJE FALLÓ" >> "$LOG"
  grep -a "AVISO: video.mp4" "salida/$g/remontar.log" >> "$LOG"
  node seeds/_puertas/veredicto.mjs "$g" > "salida/$g/veredicto.log" 2>&1
  echo "   $(grep -E 'PUBLICABLE|REGRABAR' "salida/$g/veredicto.log" | head -1)" >> "$LOG"
done
echo "[$(date +%H:%M:%S)] FIN" >> "$LOG"
