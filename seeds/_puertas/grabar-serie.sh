#!/usr/bin/env bash
# Revisa, ensaya, graba y da el veredicto de un video de las series Clientes y Cobros.
#   seeds/_puertas/grabar-serie.sh clientes 02-empresa-con-rnc [--entregar]
# Voz: la del guion (edge-tts). Graba solo si revisar.mjs y el ensayo pasan.
set -uo pipefail
SERIE=${1:?uso: grabar-serie.sh <clientes|cobros> <nn-nombre> [--entregar]}
N=${2:?falta el video}
G=guiones/$SERIE-$N.json
node seeds/_puertas/revisar.mjs "$G" --audio 2>&1 | grep -E "ERROR|Resumen" | tee /dev/stderr | grep -q "LISTO PARA GRABAR" || { echo "REVISAR: hay errores, no se graba"; exit 1; }
./.venv/bin/python seeds/_puertas/ensayar.py "$G" > "salida/$SERIE-$N-ensayo.log" 2>&1 || { grep -E "FALLO" "salida/$SERIE-$N-ensayo.log" | head; echo "ENSAYO: fallos, no se graba"; exit 1; }
./.venv/bin/python tut.py video "$SERIE-$N" > "salida/$SERIE-$N.log" 2>&1 || { tail -20 "salida/$SERIE-$N.log"; exit 1; }
V=$(node seeds/_puertas/veredicto.mjs "$SERIE-$N" 2>&1)
echo "$V" | grep -E "✗|→|video"
if echo "$V" | grep -q "→ PUBLICABLE" && [[ "${3:-}" == "--entregar" ]]; then
  D=entregas/$SERIE; S=salida/$SERIE-$N; mkdir -p "$D"
  cp "$S/video.mp4" "$D/$N.mp4"; cp "$S/video.srt" "$D/$N.srt"
  cp "$S/youtube-video.txt" "$D/$N-youtube.txt"; cp "$S/miniatura-video.png" "$D/$N-miniatura.png"
  echo "entregado: $D/$N"
fi
