"""Cliente mínimo de la API local de Germiva para sembrar la demo comercial a contadores.
Login de desarrollo (sin reCAPTCHA, solo local) con la clave demo de config.local.json."""
import json, pathlib, urllib.request, urllib.error, subprocess, os
RAIZ = pathlib.Path(__file__).resolve().parents[2]
API = "http://localhost:3001/api"
CLAVE = json.load(open(RAIZ / "config.local.json", encoding="utf-8"))["variables"]["clave_demo"]
_tokens = {}

def login(usuario):
    if usuario not in _tokens:
        d = _req("POST", "/auth/dev/login", {"username": usuario, "password": CLAVE}, token=None)
        _tokens[usuario] = d["accessToken"]
    return _tokens[usuario]

def _req(metodo, ruta, cuerpo=None, token=None, permitir=()):
    h = {"Content-Type": "application/json"}
    if token: h["Authorization"] = "Bearer " + token
    data = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8") if cuerpo is not None else None
    import time
    for intento in range(8):
        r = urllib.request.Request(API + ruta, data=data, headers=h, method=metodo)
        try:
            with urllib.request.urlopen(r, timeout=120) as resp:
                b = resp.read(); return json.loads(b) if b else None
        except urllib.error.HTTPError as e:
            cuerpo_err = e.read().decode("utf-8", "replace")
            if e.code in (429, 503) and intento < 7:   # límite de peticiones u ocupado: esperar y reintentar
                time.sleep(3 * (intento + 1)); continue
            if e.code in permitir: return {"_error": e.code, "_cuerpo": cuerpo_err}
            raise RuntimeError(f"{metodo} {ruta} -> {e.code}: {cuerpo_err[:600]}")

def api(usuario, metodo, ruta, cuerpo=None, permitir=()):
    return _req(metodo, ruta, cuerpo, login(usuario), permitir)

def sql(q):
    """SELECT/UPDATE directo a la base local (solo para lo que la API no expone)."""
    env = {**os.environ, "MYSQL_PWD": [l.split("=", 1)[1] for l in (RAIZ.parent / "germiva/Germiva-api/.env").read_text().splitlines() if l.startswith("DB_PASSWORD=")][0]}
    out = subprocess.run([r"C:\Program Files\MySQL\MySQL Server 9.7\bin\mysql.exe", "-uroot", "-h127.0.0.1", "germiva",
                          "--default-character-set=utf8mb4", "-N", "-B", "-e", q], capture_output=True, text=True, encoding="utf-8", env=env)
    if out.returncode: raise RuntimeError(out.stderr)
    return [l.split("\t") for l in out.stdout.splitlines()]

def cambiar_empresa(usuario, company_id):
    """PATCH /v1/company/switch/:id y guarda el token nuevo (la empresa activa va en el JWT)."""
    d = _req("PATCH", f"/v1/company/switch/{company_id}", {}, login(usuario))
    _tokens[usuario] = d["accessToken"]
    return d
