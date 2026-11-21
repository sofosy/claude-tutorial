#!/usr/bin/env bash
# Deja la base local en el estado de partida de un video de la serie Contabilidad.
#   seeds/contabilidad/preparar.sh <catalogo|balance-inicial|bancos|cierre-mensual|cierre-anual|revaluacion>
# Parte SIEMPRE de la instantánea sembrada del dev-env (el mismo estado en cada toma)
# y arma por el API lo que el video necesita encontrar hecho.
set -euo pipefail
ESTADO=${1:?uso: preparar.sh <estado>}
API_DIR=$(cd "${GERMIVA_API_DIR:-../Germiva-api}" && pwd)
SNAP=$API_DIR/.dev-env/seeded.sql.gz
# La instantánea sembrada puede ir atrasada respecto de las migraciones de la
# rama: la primera vez se le aplican y el resultado se guarda como base de la
# serie, para que cada toma restaure en segundos el mismo estado.
BASE=$API_DIR/.dev-env/contabilidad-base.sql.gz
# Segunda pila para ENSAYAR mientras otra toma se graba: GERMIVA_DB=germiva_ensayo
# y TUT_API=http://localhost:3002/api (una API aparte sobre esa base). Nunca
# reinicia MySQL ni vacía Redis: eso tumbaría la grabación en curso.
DB=${GERMIVA_DB:-germiva}
M="docker exec -i germiva-dev-mysql mysql -uroot"
# MySQL 8 no devuelve la memoria de cada DROP/CREATE + restauración (unos
# 400 MB por toma): tras una tanda de grabaciones el kernel lo mataba por
# falta de memoria a mitad de un video. Por encima de 2.5 GB se reinicia
# antes de restaurar; la API vuelve a conectar sola.
memoria_mysql_mb() {
  local mb
  mb=$(docker stats --no-stream --format '{{.MemUsage}}' germiva-dev-mysql 2>/dev/null | cut -d/ -f1 \
    | awk '/GiB/{sub("GiB","");print int($1*1024)} /MiB/{sub("MiB","");print int($1)}')
  # En el contenedor de la nube `docker stats` no devuelve nada (sin cgroups de
  # memoria) y el reinicio nunca se disparaba: tras unas tomas el kernel mató a
  # mysqld con ~9 GB. El proceso se ve desde el host: se suma su RSS.
  [[ -n "$mb" ]] || mb=$(ps -C mysqld -o rss= 2>/dev/null | awk '{s+=$1} END {print int(s/1024)}')
  echo "${mb:-0}"
}
# El apagado espera hasta 90 s: con el plazo de 10 s de `docker restart`, una
# consulta colgada hacía que lo mataran (137) y el contenedor quedaba detenido.
if [[ "$DB" == germiva && "$(memoria_mysql_mb || echo 0)" -gt 2560 ]]; then
  docker stop -t 90 germiva-dev-mysql >/dev/null || true
fi
docker start germiva-dev-mysql >/dev/null
for _ in $(seq 1 60); do $M -e 'SELECT 1' >/dev/null 2>&1 && break; sleep 2; done
restaurar() {
  $M -e "DROP DATABASE IF EXISTS $DB; CREATE DATABASE $DB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
  gunzip -c "$1" | $M "$DB"
}
if [[ "$DB" == germiva && ( ! -f "$BASE" || "$BASE" -ot "$SNAP" ) ]]; then
  restaurar "$SNAP"
  (cd "$API_DIR" && npx typeorm migration:run -d ./dist/config/typeorm.js --transaction all >/dev/null \
     && node dist/scripts/sync-permissions-additive.js >/dev/null)
  # --routines: sin él la base de la serie perdía las funciones del esquema
  # (FUZZY_WORD_DISTANCE) y el buscador de clientes fallaba en los videos.
  docker exec germiva-dev-mysql mysqldump -uroot --single-transaction --routines germiva | gzip > "$BASE"
else
  # La pila de ensayo comparte MySQL con la de grabación, que lo reinicia al
  # pasar de 2.5 GB: si la restauración cae en ese momento, se reintenta.
  for intento in 1 2 3 4; do
    restaurar "$BASE" && break
    [[ $intento == 4 ]] && exit 1
    sleep 20
    for _ in $(seq 1 60); do $M -e 'SELECT 1' >/dev/null 2>&1 && break; sleep 2; done
  done
fi
$M "$DB" -e "UPDATE companies SET legalName='Distribuidora Germiva Demo S.R.L.', tradeName='Distribuidora Germiva', rnc='130555001', email='contabilidad@distribuidora.germiva.com', website='https://germiva.com' WHERE id=1; UPDATE users SET email='admin@germiva.com' WHERE id=1;"
if [[ "$DB" == germiva ]]; then
  docker exec germiva-dev-redis redis-cli FLUSHALL >/dev/null 2>&1 || redis-cli FLUSHALL >/dev/null 2>&1 || true
fi
python3 "$(dirname "$0")/preparar.py" "$ESTADO"
echo "datos de partida listos: $ESTADO"
