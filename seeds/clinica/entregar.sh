#!/usr/bin/env bash
# seeds/clinica/entregar.sh <guion> <carpeta de entregas> "<Parte N - Título>"
# Copia el video, la descripción de YouTube y la miniatura a entregas/. Sin .srt: el pedido es sin subtítulos.
set -euo pipefail
cd "$(dirname "$0")/../.."
g=$1; dest="entregas/$2"; nombre=$3
mkdir -p "$dest"
cp "salida/$g/video.mp4" "$dest/$nombre.mp4"
cp "salida/$g/youtube-video.txt" "$dest/$nombre - descripcion YouTube.txt"
cp "salida/$g/miniatura-video.png" "$dest/$nombre - miniatura.png"
ls -la "$dest" | tail -4
