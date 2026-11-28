#!/usr/bin/env bash
# Antes de cada grabación: trae lo nuevo de master en Germiva-api y germiva-website, lo une a la rama de
# trabajo y, si el API cambió, la recompila y la reinicia. El frontend (ng serve) recompila solo; se espera a
# que responda antes de devolver el control. Nunca correr con una grabación en curso: el navegador se recarga.
set -euo pipefail
cd "$(dirname "$0")/../../.."
cambio_api=0
for repo in Germiva-api germiva-website; do
  ( cd "$repo"
    git fetch -q origin master
    antes=$(git rev-parse HEAD)
    git merge --no-edit -q origin/master || { echo "CONFLICTO al unir master en $repo"; exit 1; }
    despues=$(git rev-parse HEAD)
    if [ "$antes" != "$despues" ]; then
      echo "$repo: unido master ($(git log --oneline "$antes".."$despues" | wc -l) commits)"
      [ "$repo" = Germiva-api ] && touch /tmp/claude-0/.api-cambio || touch /tmp/claude-0/.web-cambio
    else
      echo "$repo: al día con master"
    fi )
done
if [ -f /tmp/claude-0/.api-cambio ]; then
  rm -f /tmp/claude-0/.api-cambio
  cd Germiva-api
  node scripts/dev-build.js > .dev-env/api-build.log 2>&1
  npx typeorm migration:run -d ./dist/config/typeorm.js --transaction all >> .dev-env/migrations.log 2>&1
  node dist/scripts/sync-permissions-additive.js >> .dev-env/migrations.log 2>&1
  kill "$(cat .dev-env/api.pid)" 2>/dev/null || true
  sleep 2
  nohup node dist/main.js > .dev-env/api.log 2>&1 & echo $! > .dev-env/api.pid
  for i in $(seq 1 60); do curl -s -o /dev/null -w '%{http_code}' http://localhost:3001/api-json | grep -q 200 && break; sleep 3; done
  echo "API recompilada y reiniciada"
  cd ..
fi
if [ -f /tmp/claude-0/.web-cambio ]; then
  # Un ng serve que recompila crece ~3 GB y deja la grabación al borde del OOM: se reinicia limpio.
  rm -f /tmp/claude-0/.web-cambio
  ( cd Germiva-api && scripts/dev-env/down.sh --web >/dev/null 2>&1 || true
    pkill -f "ng serve" || true; sleep 4; pkill -f "esbuild --service" || true; sleep 1
    scripts/dev-env/up.sh --web > .dev-env/upweb.log 2>&1 )
  echo "frontend reiniciado"
fi
# 200 en la raíz no basta: hay que esperar a que ng serve termine de compilar (y servir /home).
for i in $(seq 1 180); do
  curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:4200/home | grep -q 200 \
    && tail -3 Germiva-api/.dev-env/web.log | grep -q -E "Local:|bundle generation complete|Page reload" && break
  sleep 5
done
echo "listo para grabar"
