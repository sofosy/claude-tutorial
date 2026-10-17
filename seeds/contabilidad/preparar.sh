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
M="docker exec -i germiva-dev-mysql mysql -uroot"
restaurar() {
  $M -e "DROP DATABASE IF EXISTS germiva; CREATE DATABASE germiva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
  gunzip -c "$1" | $M germiva
}
if [[ ! -f "$BASE" || "$BASE" -ot "$SNAP" ]]; then
  restaurar "$SNAP"
  (cd "$API_DIR" && npx typeorm migration:run -d ./dist/config/typeorm.js --transaction all >/dev/null \
     && node dist/scripts/sync-permissions-additive.js >/dev/null)
  docker exec germiva-dev-mysql mysqldump -uroot --single-transaction germiva | gzip > "$BASE"
else
  restaurar "$BASE"
fi
$M germiva -e "UPDATE companies SET legalName='Distribuidora Germiva Demo S.R.L.', tradeName='Distribuidora Germiva', rnc='130555001', email='contabilidad@distribuidora.germiva.com', website='https://germiva.com' WHERE id=1; UPDATE users SET email='admin@germiva.com' WHERE id=1;"
docker exec germiva-dev-redis redis-cli FLUSHALL >/dev/null 2>&1 || true
python3 "$(dirname "$0")/preparar.py" "$ESTADO"
echo "datos de partida listos: $ESTADO"
