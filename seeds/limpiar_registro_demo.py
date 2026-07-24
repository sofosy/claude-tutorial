#!/usr/bin/env python3
"""Borra el usuario y la empresa de demo para poder re-grabar el registro.

Las dependencias se descubren en information_schema en vez de escribirse a mano:
el esquema de Germiva cambia con cada migración, y una lista fija de tablas se
rompe en silencio la primera vez que alguien agrega una relación nueva.

Uso:  python seeds/limpiar_registro_demo.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CFG = json.loads((RAIZ / "config.local.json").read_text(encoding="utf-8"))

ENV = Path(CFG["db"]["env"])
MYSQL = CFG["db"].get("cliente") or shutil.which("mysql") or "mysql"
EMAIL = CFG["variables"]["correo_demo"]
RNC = CFG["variables"]["rnc_demo"]


def env():
    d = {}
    for linea in ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
        linea = linea.strip()
        if "=" in linea and not linea.startswith("#"):
            k, v = linea.split("=", 1)
            d[k.strip()] = v.strip().strip('"').strip("'")
    return d


E = env()


def sql(consulta):
    r = subprocess.run(
        [MYSQL, "-h", E["DB_HOST"], "-P", E.get("DB_PORT", "3306"),
         "-u", E["DB_USERNAME"], "-p" + E["DB_PASSWORD"], E["DB_DATABASE"],
         "-N", "-e", consulta],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR SQL:", r.stderr.strip()[:300], file=sys.stderr)
        sys.exit(1)
    return [l.split("\t") for l in r.stdout.strip().splitlines() if l]


def hijos(tabla):
    """Tablas que apuntan a `tabla` por clave foránea."""
    return sql(f"""
        SELECT TABLE_NAME, COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA='{E['DB_DATABASE']}'
          AND REFERENCED_TABLE_NAME='{tabla}' AND REFERENCED_COLUMN_NAME='id';""")


usuarios = [f[0] for f in sql(f"SELECT id FROM users WHERE email='{EMAIL}';")]
empresas = [f[0] for f in sql(
    f"SELECT id FROM companies WHERE rnc='{RNC}'"
    + (f" OR user_id IN ({','.join(usuarios)})" if usuarios else "") + ";")]

if not usuarios and not empresas:
    print("nada que limpiar")
    sys.exit(0)

ordenes = ["SET FOREIGN_KEY_CHECKS=0;"]
for padre, ids in (("companies", empresas), ("users", usuarios)):
    if not ids:
        continue
    lista = ",".join(ids)
    for tabla, col in hijos(padre):
        ordenes.append(f"DELETE FROM `{tabla}` WHERE `{col}` IN ({lista});")
    ordenes.append(f"DELETE FROM `{padre}` WHERE id IN ({lista});")
ordenes.append("SET FOREIGN_KEY_CHECKS=1;")

sql(" ".join(ordenes))
print(f"limpiado: usuarios={usuarios or '-'} empresas={empresas or '-'}")
