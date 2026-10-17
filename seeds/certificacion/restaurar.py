# .venv/Scripts/python.exe seeds/certificacion/restaurar.py A|B
# Serie «Certificación e-CF» (12/10/2026). Devuelve la base `germiva` al canon (seeds/certificacion/canon.sql:
# master del 12/10 + padrón ficticio + empresa principal renombrada a SOFOSY) sin binlog (R14), vacía Redis y
# aplica el estado:
#   A  canon tal cual: ninguna solicitud (video 1, la contadora llena el formulario).
#   B  A + SC-000001 (Carolina Méndez, contadora, 3 clientes, comprobante validado por la IA y empresas creadas)
#        + SC-000002 (Ramón Guzmán, dueño, PDF escaneado: «Sin verificar»). Video 2, el administrador.
#      Las solicitudes se envían por el formulario real (seeds/certificacion/llenar.py), como en el video 1.
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
API = RAIZ.parent / "germiva" / "Germiva-api"
MYSQL = r"C:\Program Files\MySQL\MySQL Server 9.7\bin\mysql.exe"
PY = str(RAIZ / ".venv" / "Scripts" / "python.exe")
estado = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
t0 = time.time()


def log(*a):
    print(f"[{time.time() - t0:5.0f}s]", *a, flush=True)


def clave_bd():
    for linea in (API / ".env").read_text(encoding="utf-8").splitlines():
        if linea.startswith("DB_PASSWORD="):
            return linea.split("=", 1)[1].strip().strip('"')
    return ""


ENV = {**os.environ, "MYSQL_PWD": clave_bd()}


def sql(q):
    r = subprocess.run([MYSQL, "-uroot", "--default-character-set=utf8mb4", "-N", "germiva", "-e", q],
                       env=ENV, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit("SQL: " + r.stderr[:500])
    return r.stdout.strip()


# 1. canon (el volcado va por stdin desde el archivo: no pasa por la memoria de Python)
with open(AQUI / "canon.sql", "rb") as volcado:
    r = subprocess.run([MYSQL, "-uroot", "--default-character-set=utf8mb4",
                        "--init-command=SET SESSION sql_log_bin=0", "germiva"], stdin=volcado, env=ENV,
                       capture_output=True)
if r.returncode:
    raise SystemExit("canon: " + r.stderr.decode("utf-8", "replace")[:1500])
log("canon cargado")
subprocess.run(["docker", "exec", "germiva-redis", "redis-cli", "FLUSHALL"], capture_output=True)
log("redis vacío")

if estado == "B":
    for quien in ("contadora", "cliente"):
        r = subprocess.run([PY, str(AQUI / "llenar.py"), quien, "--enviar"], cwd=RAIZ, capture_output=True,
                           text=True, encoding="utf-8")
        if "Recibimos tu solicitud" not in r.stdout:
            raise SystemExit(f"envío {quien} falló:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
        log("enviada", quien)
    # la cola crea las 3 empresas de la contadora: esperar a que termine
    for _ in range(90):
        hechas = sql("SELECT COUNT(*) FROM certification_request_companies c JOIN certification_requests r "
                     "ON r.id=c.request_id WHERE r.code='SC-000001' AND c.created_company_id IS NOT NULL")
        if hechas == "3":
            break
        time.sleep(2)
    else:
        raise SystemExit("la cola no creó las 3 empresas")
    time.sleep(4)
    # sin aviso emergente al entrar (solo sale si la notificación tiene < 15 min): el video lo cuenta en voz
    sql("UPDATE company_notifications SET published_at = DATE_SUB(published_at, INTERVAL 1 DAY) "
        "WHERE title LIKE 'Solicitud de certificaci%'")
    log("estado B listo:", sql("SELECT GROUP_CONCAT(CONCAT(code,'=',status) SEPARATOR ' ') FROM certification_requests"))
log(f"estado {estado} listo")
