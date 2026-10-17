#!/usr/bin/env bash
# Graba la serie «Seguridad» un video a la vez, como ÚNICO proceso pesado (copia adaptada de
# seeds/cajas/grabar-serie2.sh). Uso (desde claude-tutorial, DESACOPLADO con Start-Process — R19/R26):
#   bash seeds/seguridad/grabar-serie.sh seguridad-00-introduccion:E0 seguridad-02b-editor-permisos:E2a ...
#   Un video con un paso regrabado desde otro estado: seguridad-06b-rotar-pausar-revocar:E6c:03=E6c
# Por video: puerta 1 (revisar + verificar) → cerrojo → restaurar → tut video → [paso extra] →
# restaurar → soltar cerrojo → veredicto. Log por video en salida/<guion>/serie.log y resumen en
# seeds/seguridad/serie.log. Las apps (API :3001, front estático :4200) NO se tocan.
set -u
cd "$(dirname "$0")/../.."
PY=.venv/Scripts/python.exe
LOCK=seeds/_puertas/NAVEGADOR.lock
RES=seeds/seguridad/serie.log
YO="GRABANDO serie-seguridad $$"

tomar_cerrojo() {
  while ! ( set -o noclobber; echo "$YO" > "$LOCK" ) 2>/dev/null; do sleep 20; done
}
soltar_cerrojo() { [ "$(cat "$LOCK" 2>/dev/null)" = "$YO" ] && rm -f "$LOCK"; }
trap soltar_cerrojo EXIT

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$RES"; }

apps_vivas() {
  curl -s -o /dev/null --max-time 5 http://localhost:4200/ || return 1
  curl -s -o /dev/null --max-time 5 http://localhost:3001/ || return 1
}

log "INICIO serie ($*)"
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
  if ! apps_vivas; then log "   APPS CAÍDAS (:4200 o :3001) — no se graba"; continue; fi
  inicio=$(date +%s)
  tomar_cerrojo
  node seeds/seguridad/restaurar.mjs "$estado" >> "$L" 2>&1 || { log "   restaurar $estado FALLÓ"; soltar_cerrojo; continue; }
  # E6c: la lámina del programa del contador necesita la credencial recién restaurada (06b/06c)
  if [ "$estado" = "E6c" ]; then node marca/demo-integracion/preparar.mjs --estatico >> "$L" 2>&1 || { log "   preparar demo-integracion FALLÓ"; soltar_cerrojo; continue; }; fi
  "$PY" tut.py video "$guion" >> "$L" 2>&1; rc=$?
  if [ -n "${extra:-}" ]; then  # el paso extra se regraba aunque la corrida completa lo haya fallado
    paso=${extra%%=*}; est2=${extra#*=}
    node seeds/seguridad/restaurar.mjs "$est2" >> "$L" 2>&1
    [ "$est2" = "E6c" ] && node marca/demo-integracion/preparar.mjs --estatico >> "$L" 2>&1
    "$PY" tut.py video "$guion" --paso "$paso" >> "$L" 2>&1; rc=$?
  fi
  node seeds/seguridad/restaurar.mjs E0 >> "$L" 2>&1
  soltar_cerrojo
  if [ $rc -ne 0 ] || [ ! -f "$out/video.mp4" ] || [ "$(stat -c %Y "$out/video.mp4")" -lt "$inicio" ]; then
    log "   GRABACIÓN FALLÓ (rc=$rc o video.mp4 viejo) — ver $L"; continue
  fi
  node seeds/_puertas/veredicto.mjs "$guion" > "$out/veredicto.log" 2>&1
  log "   $(grep -E 'PUBLICABLE|REGRABAR' "$out/veredicto.log" | head -1)  ($(( $(date +%s) - inicio )) s)"
done
log "FIN serie"
