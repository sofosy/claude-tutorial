#!/usr/bin/env bash
# Revisa, graba con ElevenLabs y da el veredicto de un video de la serie.
#   seeds/vendedores/grabar.sh 01-ficha [--entregar]
# Graba solo si revisar.mjs no tiene errores; la voz ya pagada sale de la caché.
set -uo pipefail
N=${1:?uso: grabar.sh <nn-nombre> [--entregar]}
G=guiones/vendedores-$N.json
if ! node seeds/_puertas/revisar.mjs "$G" --audio 2>&1 | tee /dev/stderr | grep -q "LISTO PARA GRABAR"; then
  echo "REVISAR: hay errores, no se graba"; exit 1
fi
ELEVEN_KEY=${ELEVEN_KEY:-$(python3 -c "import json;print(json.load(open('config.local.json'))['elevenlabs_api_key'])")} \
  ./.venv/bin/python tut.py video "vendedores-$N" > "salida/vendedores-$N.log" 2>&1 || { tail -20 "salida/vendedores-$N.log"; exit 1; }
V=$(node seeds/_puertas/veredicto.mjs "vendedores-$N" 2>&1)
echo "$V" | grep -E "✗|→|video"
if echo "$V" | grep -q "→ PUBLICABLE" && [[ "${2:-}" == "--entregar" ]]; then
  seeds/vendedores/entregar.sh "$N" >/dev/null && echo "entregado: $N"
fi
