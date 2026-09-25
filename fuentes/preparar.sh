#!/usr/bin/env bash
# Descarga del registro de npm las fuentes que la app pide a Google Fonts.
#
# En entornos donde fonts.googleapis.com está bloqueado, los íconos de Material
# se pintan como texto («menu», «home») y el video queda inservible. El guion
# declara `rutas_locales` y el grabador sirve estos archivos en lugar de pedirlos
# a Google. Los binarios no se versionan: se regeneran con este script.
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp -d)
( cd "$tmp" && npm pack --silent material-icons@1 @fontsource/roboto@5 >/dev/null \
  && for f in *.tgz; do mkdir "${f%.tgz}" && tar xzf "$f" -C "${f%.tgz}"; done )
cp "$tmp"/material-icons-*/package/iconfont/*.woff2 .
for w in 300 400 500; do
  cp "$tmp"/fontsource-roboto-*/package/files/roboto-latin-$w-normal.woff2 .
done
rm -rf "$tmp"
echo "fuentes listas en $(pwd)"
