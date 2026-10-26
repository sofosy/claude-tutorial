#!/usr/bin/env bash
# Deja la base local en el estado de partida del video de importar/exportar empleados.
#   seeds/rrhh/preparar.sh
# Parte SIEMPRE de la instantánea sembrada del dev-env, así cada toma encuentra lo
# mismo: sin los dos empleados de importar-demo.xlsx (el video los crea) y sin
# importaciones a medias (con una en cola, el diálogo abre en «sigue en curso»).
set -euo pipefail
API_DIR=$(cd "${GERMIVA_API_DIR:-../Germiva-api}" && pwd)
SNAP=$API_DIR/.dev-env/seeded.sql.gz
# La instantánea puede ir atrasada respecto de las migraciones: la primera vez se
# le aplican y el resultado se guarda como base de la serie.
BASE=$API_DIR/.dev-env/rrhh-base.sql.gz
M="docker exec -i germiva-dev-mysql mysql -uroot"
docker start germiva-dev-mysql >/dev/null
for _ in $(seq 1 60); do $M -e 'SELECT 1' >/dev/null 2>&1 && break; sleep 2; done
restaurar() {
  $M -e "DROP DATABASE IF EXISTS germiva; CREATE DATABASE germiva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
  gunzip -c "$1" | $M germiva
}
if [[ ! -f "$BASE" || "$BASE" -ot "$SNAP" ]]; then
  restaurar "$SNAP"
  (cd "$API_DIR" && npx typeorm migration:run -d ./dist/config/typeorm.js --transaction all >/dev/null \
     && node dist/scripts/sync-permissions-additive.js >/dev/null)
  docker exec germiva-dev-mysql mysqldump -uroot --single-transaction --routines germiva | gzip > "$BASE"
else
  restaurar "$BASE"
fi
# La base nueva vuelve a numerar las importaciones desde 1: si Redis recuerda un
# «job 1» ya terminado, BullMQ descarta el nuevo y el diálogo se queda esperando.
# En la nube Redis corre fuera de Docker: de ahí el segundo intento.
docker exec germiva-dev-redis redis-cli FLUSHALL >/dev/null 2>&1 || redis-cli FLUSHALL >/dev/null 2>&1 || true
# Datos inventados en pantalla, como el resto de las series: la empresa de demo y
# solo los tres empleados de la serie Vendedores (con «Germiva» en el nombre). Los
# empleados sembrados llevan nombres con caracteres rotos (PE�A) que no se publican.
$M germiva -e "UPDATE companies SET legalName='Distribuidora Germiva Demo S.R.L.', tradeName='Distribuidora Germiva', rnc='130555001', email='ventas@distribuidora.germiva.com', website='https://germiva.com' WHERE id=1; UPDATE users SET email='admin@germiva.com' WHERE id=1; UPDATE partners SET deleted_at=NOW() WHERE company_id=1 AND deleted_at IS NULL AND FIND_IN_SET('EMPLOYEE', partnerType);"
python3 - "$(dirname "$0")/../vendedores" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
import preparar as v
v.TOKEN = v.entrar("admin", "admin")
# El aviso «Configuración incompleta» taparía la pantalla al entrar en el video.
v.llamar("POST", "/v1/user-preferences/incomplete-config-notice/claim", {})
v.crear_empleados()
PY
echo "datos de partida listos: rrhh"
