#!/usr/bin/env bash
# Deja la base local en el estado de partida del tutorial de Productos:
# instantánea sembrada del dev-env + empresa de demo + ubicación y proveedor.
set -euo pipefail
API=${API_URL:-http://localhost:3001/api}
SNAP=${GERMIVA_API_DIR:-../Germiva-api}/.dev-env/seeded.sql.gz
M="docker exec -i germiva-dev-mysql mysql -uroot"
$M -e "DROP DATABASE germiva; CREATE DATABASE germiva CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
gunzip -c "$SNAP" | $M germiva
$M germiva -e "UPDATE companies SET legalName='Tienda Germiva Demo S.R.L.', tradeName='Tienda Germiva', rnc='130555001', email='ventas@tienda.germiva.com', website='https://germiva.com' WHERE id=1; UPDATE users SET email='admin@germiva.com' WHERE id=1;"
TOK=$(curl -sS -X POST $API/auth/dev/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['accessToken'])")
api(){ curl -sS -f -o /dev/null -X "$1" "$API$2" -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d "$3"; }
$M germiva -e "UPDATE attributes SET options='[\"S\", \"M\", \"L\", \"XL\"]' WHERE id=2 AND company_id=1;"
api POST /v1/inventory/location '{"position":"Pasillo A - Estante 1","warehouse":1}'
api POST /v1/partner '{"name":"Textiles Germiva del Caribe","tin":"130555002","partnerType":["SUPPLIER"],"partnerCategory":"BUSINESS"}'
docker exec germiva-dev-redis redis-cli FLUSHALL >/dev/null 2>&1 || true
echo "datos de partida listos"
