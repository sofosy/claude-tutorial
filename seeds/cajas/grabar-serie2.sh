#!/usr/bin/env bash
# Graba la serie de Cajas en serie, un video a la vez, como ÚNICO proceso pesado.
# Uso (desde claude-tutorial, DESACOPLADO con Start-Process — R19/R26):
#   bash seeds/cajas/grabar-serie.sh cajas-01-tablero:S0 cajas-03-abrir-y-operar:S1 ...
#   Un video con un paso que parte de otro estado: cajas-02-configuracion:S0:04=S2i
# Por video: puerta 1 (revisar + verificar) → restaurar → tut video → [paso extra] → restaurar
# → veredicto. Log por video en salida/<guion>/serie.log y resumen en seeds/cajas/serie.log.
set -u
cd "$(dirname "$0")/../.."
PY=.venv/Scripts/python.exe
LOCK=seeds/_puertas/NAVEGADOR.lock
RES=seeds/cajas/serie.log
YO="GRABANDO serie-cajas $$"

tomar_cerrojo() {
  while ! ( set -o noclobber; echo "$YO" > "$LOCK" ) 2>/dev/null; do sleep 20; done
}
soltar_cerrojo() { [ "$(cat "$LOCK" 2>/dev/null)" = "$YO" ] && rm -f "$LOCK"; }
trap soltar_cerrojo EXIT

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$RES"; }

for item in "$@"; do
  IFS=: read -r guion estado extra <<< "$item"
  out="salida/$guion"; mkdir -p "$out"; L="$out/serie.log"
  log "── $guion (parte de $estado${extra:+, extra $extra})"
  if ! node seeds/_puertas/revisar.mjs "$guion" > "$out/revisar.log" 2>&1; then
    log "   PUERTA 1 FALLA (revisar) — no se graba"; continue
  fi
  if ! "$PY" tut.py verificar "$guion" > "$out/verificar.log" 2>&1; then
    log "   PUERTA 1 FALLA (verificar) — no se graba"; continue
  fi
  inicio=$(date +%s)
  tomar_cerrojo
  node seeds/cajas/restaurar.mjs "$estado" >> "$L" 2>&1 || { log "   restaurar $estado FALLÓ"; soltar_cerrojo; continue; }
  "$PY" tut.py video "$guion" >> "$L" 2>&1; rc=$?
  if [ -n "${extra:-}" ]; then  # el paso extra se regraba aunque la corrida completa lo haya fallado
    paso=${extra%%=*}; est2=${extra#*=}
    node seeds/cajas/restaurar.mjs "$est2" >> "$L" 2>&1
    "$PY" tut.py video "$guion" --paso "$paso" >> "$L" 2>&1; rc=$?
  fi
  node seeds/cajas/restaurar.mjs "$estado" >> "$L" 2>&1
  soltar_cerrojo
  if [ $rc -ne 0 ] || [ ! -f "$out/video.mp4" ] || [ "$(stat -c %Y "$out/video.mp4")" -lt "$inicio" ]; then
    log "   GRABACIÓN FALLÓ (rc=$rc o video.mp4 viejo) — ver $L"; continue
  fi
  node seeds/_puertas/veredicto.mjs "$guion" > "$out/veredicto.log" 2>&1
  log "   $(grep -E 'PUBLICABLE|REGRABAR' "$out/veredicto.log" | head -1)  ($(( $(date +%s) - inicio )) s)"
done
log "FIN serie"
