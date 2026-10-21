#!/usr/bin/env bash
# Copia a entregas/vendedores/ lo publicable de un video de la serie.
#   seeds/vendedores/entregar.sh 01-ficha
set -euo pipefail
N=${1:?uso: entregar.sh <nn-nombre>}
S=salida/vendedores-$N
D=entregas/vendedores
mkdir -p "$D"
cp "$S/video.mp4" "$D/$N.mp4"
cp "$S/video.srt" "$D/$N.srt"
cp "$S/youtube-video.txt" "$D/$N-youtube.txt"
cp "$S/miniatura-video.png" "$D/$N-miniatura.png"
ls -la "$D" | grep "$N"
