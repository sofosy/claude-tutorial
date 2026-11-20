#!/usr/bin/env bash
# Graba en fila varios videos de la serie, esperando a que termine la toma en curso.
#   seeds/contabilidad/cola.sh 41-centro-en-compras 43-informes-por-centro
cd "$(dirname "$0")/../.."
export ELEVEN_KEY=${ELEVEN_KEY:-x}
while pgrep -f "[t]ut.py video" >/dev/null; do sleep 5; done
for v in "$@"; do
  echo "### $v"
  seeds/contabilidad/grabar.sh "$v" --entregar 2>&1 | grep -E "ERROR|✗|→|video|entregado|rror"
done
