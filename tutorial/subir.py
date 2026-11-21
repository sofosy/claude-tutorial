"""Sube a YouTube los videos de `entregas/` que todavía no están en el canal.

    python -m tutorial.subir autorizar client_secret.json   # una sola vez, en tu máquina
    python -m tutorial.subir listar                         # qué falta (no sube nada)
    python -m tutorial.subir subir [--serie clientes] [--max 5] [--privacidad private]

Solo biblioteca estándar: corre igual en tu máquina que en GitHub Actions.

Qué cuenta como «ya subido»: lo anotado en `entregas/subidos.json` y, además,
cualquier video del canal con el mismo título (los que se subieron a mano).

La cuota diaria de la API alcanza para pocos videos. Cuando YouTube la corta,
el comando termina bien y deja el resto pendiente: la siguiente corrida (la
tarea diaria de GitHub Actions) sigue donde quedó.
"""
import argparse
import datetime
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTREGAS = RAIZ / "entregas"
REGISTRO = ENTREGAS / "subidos.json"
TOKEN_LOCAL = RAIZ / "youtube-token.json"

API = "https://www.googleapis.com/youtube/v3"
SUBIDA = "https://www.googleapis.com/upload/youtube/v3"
PERMISOS = ("https://www.googleapis.com/auth/youtube.upload "
            "https://www.googleapis.com/auth/youtube.force-ssl")

# Motivos con los que YouTube dice «por hoy no más»: no son un fallo, se sigue mañana.
LIMITES = {"quotaExceeded", "dailyLimitExceeded", "uploadLimitExceeded",
           "rateLimitExceeded", "userRateLimitExceeded"}

# Copias que no van al canal: versiones livianas, verticales y entregas viejas.
EXCLUIR = re.compile(r"liviano|720p|Instagram Reel|/anterior |/v\d+-\d{4}", re.I)


class Limite(Exception):
    """YouTube cortó por cuota o por tope de subidas del canal."""


# ───────────────────────────── qué hay para subir ─────────────────────────────

def _primero(*rutas):
    return next((r for r in rutas if r.exists()), None)


def _seccion(texto, desde, hasta):
    """Lo que hay entre el encabezado `desde` y el primero de los `hasta`."""
    m = re.search(desde, texto, re.M)
    if not m:
        return ""
    resto = texto[m.end():]
    cortes = [c.start() for c in (re.search(h, resto, re.M) for h in hasta) if c]
    return resto[:min(cortes)] if cortes else resto


def _leer_paquete(txt):
    """`…-youtube.txt` del motor: TÍTULO / DESCRIPCIÓN / 🏷️ ETIQUETAS."""
    t = txt.read_text(encoding="utf-8")
    raya = r"^=+\s*$\n"
    titulo = _seccion(t, r"^TÍTULO\s*$\n" + raya, [r"^DESCRIPCIÓN\s*$"]).strip()
    desc = _seccion(t, r"^DESCRIPCIÓN\s*$\n" + raya,
                    [r"^🏷️ ETIQUETAS", r"^—\s*$", r"^TRANSCRIPCIÓN\s*$"]).strip()
    tags = _seccion(t, r"^🏷️ ETIQUETAS\s*$\n", [r"^—\s*$", r"^\s*$"]).strip()
    return titulo, desc, tags


def _leer_comercial(txt):
    """«Textos para publicar.txt» de los comerciales: bloque YOUTUBE (video)."""
    t = txt.read_text(encoding="utf-8")
    bloque = _seccion(t, r"^YOUTUBE \(video\).*$\n", [r"^YOUTUBE SHORTS", r"^INSTAGRAM"])
    titulo = _seccion(bloque, r"^Título:\s*$\n", [r"^\s*$"]).strip()
    desc = _seccion(bloque, r"^Descripción:\s*$\n", [r"^Etiquetas:"]).strip()
    tags = _seccion(bloque, r"^Etiquetas:", [r"^\s*$"]).strip()
    return titulo, desc, tags


def _recortar(texto, tope):
    """YouTube mide en bytes y rechaza los signos < y >."""
    texto = texto.replace("<", "‹").replace(">", "›")
    while len(texto.encode("utf-8")) > tope:
        texto = texto[:-1]
    return texto


def descubrir():
    """Cada MP4 de `entregas/` que trae su texto de YouTube al lado."""
    videos, sin_texto = [], []
    for mp4 in sorted(ENTREGAS.rglob("*.mp4")):
        rel = mp4.relative_to(ENTREGAS).as_posix()
        if EXCLUIR.search("/" + rel):
            continue
        d, s = mp4.parent, mp4.stem
        unico = len(list(d.glob("*.mp4"))) == 1
        comercial = s == "YouTube - horizontal"
        txt = _primero(d / f"{s}-youtube.txt", d / f"{s} - descripcion YouTube.txt",
                       d / f"{s} - YouTube.txt",
                       *([d / "Textos para publicar.txt"] if comercial else []),
                       *([d / "youtube-video.txt"] if unico else []))
        if not txt:
            sin_texto.append(rel)
            continue
        titulo, desc, tags = (_leer_comercial if txt.name.startswith("Textos") else _leer_paquete)(txt)
        if not titulo:
            sin_texto.append(rel)
            continue
        etiquetas, largo = [], 0
        for e in (x.strip() for x in tags.split(",")):
            if e and largo + len(e) + 3 <= 480:      # tope de 500 entre todas
                etiquetas.append(e)
                largo += len(e) + 3
        videos.append({
            "rel": rel, "mp4": mp4, "serie": rel.split("/")[0],
            "titulo": _recortar(" ".join(titulo.split()), 100),
            "descripcion": _recortar(desc, 4900),
            "etiquetas": etiquetas,
            "miniatura": _primero(d / f"{s}-miniatura.png", d / f"{s} - miniatura.png",
                                  d / "YouTube - miniatura.jpg",
                                  *([d / "miniatura-video.png", d / "miniatura.png"] if unico else [])),
            "srt": _primero(mp4.with_suffix(".srt"),
                            *([d / "video.srt"] if unico else [])),
        })
    return videos, sin_texto


# ───────────────────────────────── la API ─────────────────────────────────────

def _credenciales():
    """Variables de entorno (GitHub Actions) o `youtube-token.json` (tu máquina)."""
    claves = ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")
    if all(os.environ.get(k) for k in claves):
        return tuple(os.environ[k] for k in claves)
    if TOKEN_LOCAL.exists():
        t = json.loads(TOKEN_LOCAL.read_text(encoding="utf-8"))
        return t["client_id"], t["client_secret"], t["refresh_token"]
    return None


def _pedir(url, metodo="GET", cuerpo=None, cabeceras=None, token=None, crudo=False):
    cab = dict(cabeceras or {})
    if token:
        cab["Authorization"] = f"Bearer {token}"
    if isinstance(cuerpo, (dict, list)):
        cuerpo = json.dumps(cuerpo).encode("utf-8")
        cab.setdefault("Content-Type", "application/json; charset=UTF-8")
    pet = urllib.request.Request(url, data=cuerpo, method=metodo, headers=cab)
    try:
        with urllib.request.urlopen(pet, timeout=900) as r:
            datos = r.read()
            if crudo:
                return r
            return json.loads(datos) if datos else {}
    except urllib.error.HTTPError as e:
        texto = e.read().decode("utf-8", "replace")
        try:
            err = json.loads(texto).get("error", {})
            motivos = {x.get("reason") for x in err.get("errors", [])} if isinstance(err, dict) else set()
            mensaje = err.get("message", texto) if isinstance(err, dict) else str(err)
        except ValueError:
            motivos, mensaje = set(), texto
        if motivos & LIMITES:
            raise Limite(f"{', '.join(sorted(motivos & LIMITES))}: {mensaje}") from None
        raise RuntimeError(f"HTTP {e.code} {', '.join(sorted(m for m in motivos if m))}: {mensaje}") from None


def _token(cred):
    cid, secreto, refresco = cred
    datos = urllib.parse.urlencode({
        "client_id": cid, "client_secret": secreto,
        "refresh_token": refresco, "grant_type": "refresh_token"}).encode()
    try:
        return _pedir("https://oauth2.googleapis.com/token", "POST", datos,
                      {"Content-Type": "application/x-www-form-urlencoded"})["access_token"]
    except RuntimeError as e:
        raise SystemExit(
            f"  No se pudo renovar el acceso a YouTube ({e}).\n"
            "  Si dice invalid_grant, la autorización caducó o fue revocada: repite\n"
            "  `python -m tutorial.subir autorizar client_secret.json` y actualiza\n"
            "  el secreto YT_REFRESH_TOKEN.") from None


def _clave(titulo):
    """Título sin tildes, signos ni mayúsculas, para comparar con el canal."""
    plano = unicodedata.normalize("NFKD", titulo).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", plano.lower()).strip()


def _del_canal(token):
    """{título normalizado: id} de todo lo que ya está subido al canal."""
    canal = _pedir(f"{API}/channels?part=contentDetails&mine=true", token=token)
    if not canal.get("items"):
        raise SystemExit("  La cuenta autorizada no tiene canal de YouTube.")
    lista = canal["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    hay, pagina = {}, ""
    while True:
        r = _pedir(f"{API}/playlistItems?part=snippet&maxResults=50&playlistId={lista}"
                   + (f"&pageToken={pagina}" if pagina else ""), token=token)
        for it in r.get("items", []):
            hay[_clave(it["snippet"]["title"])] = it["snippet"]["resourceId"]["videoId"]
        pagina = r.get("nextPageToken")
        if not pagina:
            return hay


def _subir_video(v, privacidad, token):
    meta = {
        "snippet": {"title": v["titulo"], "description": v["descripcion"],
                    "tags": v["etiquetas"], "categoryId": "27",   # Educación
                    "defaultLanguage": "es", "defaultAudioLanguage": "es"},
        "status": {"privacyStatus": privacidad, "selfDeclaredMadeForKids": False},
    }
    peso = v["mp4"].stat().st_size
    sesion = _pedir(f"{SUBIDA}/videos?uploadType=resumable&part=snippet,status", "POST", meta,
                    {"X-Upload-Content-Type": "video/mp4",
                     "X-Upload-Content-Length": str(peso)}, token, crudo=True)
    with open(v["mp4"], "rb") as f:
        return _pedir(sesion.headers["Location"], "PUT", f,
                      {"Content-Type": "video/mp4", "Content-Length": str(peso)}, token)["id"]


def _subir_miniatura(vid, ruta, token):
    tipo = "image/jpeg" if ruta.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    _pedir(f"{SUBIDA}/thumbnails/set?videoId={vid}&uploadType=media", "POST",
           ruta.read_bytes(), {"Content-Type": tipo}, token)


def _subir_subtitulos(vid, ruta, token):
    borde = "tutorial-subir-borde"
    meta = json.dumps({"snippet": {"videoId": vid, "language": "es", "name": ""}})
    cuerpo = (f"--{borde}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n"
              f"--{borde}\r\nContent-Type: application/octet-stream\r\n\r\n").encode("utf-8") \
        + ruta.read_bytes() + f"\r\n--{borde}--\r\n".encode()
    _pedir(f"{SUBIDA}/captions?uploadType=multipart&part=snippet", "POST", cuerpo,
           {"Content-Type": f"multipart/related; boundary={borde}"}, token)


# ──────────────────────────────── comandos ────────────────────────────────────

def _cargar_registro():
    return json.loads(REGISTRO.read_text(encoding="utf-8")) if REGISTRO.exists() else {}


def _guardar_registro(reg):
    REGISTRO.write_text(json.dumps(reg, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")


def _pendiente(v, e):
    """Qué le falta a un video: el video mismo, la miniatura o los subtítulos."""
    if not e:
        return ["video"] + (["miniatura"] if v["miniatura"] else []) + (["subtítulos"] if v["srt"] else [])
    falta = []
    if v["miniatura"] and e.get("miniatura") == "pendiente":
        falta.append("miniatura")
    if v["srt"] and e.get("subtitulos") == "pendiente":
        falta.append("subtítulos")
    return falta


def cmd_listar(a):
    videos, sin_texto = descubrir()
    reg = _cargar_registro()
    cred = _credenciales()
    canal = _del_canal(_token(cred)) if cred else {}
    if not cred:
        print("  (sin credenciales: se compara solo contra entregas/subidos.json)\n")
    faltan = 0
    for v in videos:
        if a.serie and v["serie"] != a.serie:
            continue
        e = reg.get(v["rel"])
        if not e and _clave(v["titulo"]) in canal:
            print(f"  en el canal  {v['rel']}  → {canal[_clave(v['titulo'])]}")
            continue
        falta = _pendiente(v, e)
        if falta:
            faltan += 1
            print(f"  FALTA        {v['rel']}  ({', '.join(falta)})")
        elif a.todo:
            print(f"  subido       {v['rel']}  → {e['id']}")
    print(f"\n  {faltan} por subir de {len(videos)} videos con texto de YouTube.")
    if sin_texto and a.todo:
        print("\n  Sin texto de YouTube al lado (no se suben):")
        for r in sin_texto:
            print(f"    {r}")


def cmd_subir(a):
    cred = _credenciales()
    if not cred:
        raise SystemExit("  Faltan credenciales: define YT_CLIENT_ID, YT_CLIENT_SECRET y\n"
                         "  YT_REFRESH_TOKEN, o corre antes `python -m tutorial.subir autorizar`.")
    token = _token(cred)
    videos, _ = descubrir()
    reg = _cargar_registro()
    canal = _del_canal(token)
    hoy = datetime.date.today().isoformat()
    subidos = 0
    try:
        for v in videos:
            if a.serie and v["serie"] != a.serie:
                continue
            e = reg.get(v["rel"])
            if not e and _clave(v["titulo"]) in canal:
                # ya estaba en el canal (subido a mano): se anota y no se toca
                reg[v["rel"]] = {"id": canal[_clave(v["titulo"])], "titulo": v["titulo"],
                                 "origen": "ya estaba en el canal"}
                _guardar_registro(reg)
                continue
            if not _pendiente(v, e):
                continue
            if not e:
                if a.max and subidos >= a.max:
                    break
                print(f"  ↑ {v['rel']}  ({v['mp4'].stat().st_size / 1e6:.0f} MB)")
                vid = _subir_video(v, a.privacidad, token)
                e = reg[v["rel"]] = {
                    "id": vid, "titulo": v["titulo"], "fecha": hoy, "privacidad": a.privacidad,
                    "miniatura": "pendiente" if v["miniatura"] else "no hay",
                    "subtitulos": "pendiente" if v["srt"] else "no hay"}
                _guardar_registro(reg)
                subidos += 1
                print(f"    https://youtu.be/{vid}")
            for campo, ruta, fn in (("miniatura", v["miniatura"], _subir_miniatura),
                                    ("subtitulos", v["srt"], _subir_subtitulos)):
                if ruta and e.get(campo) == "pendiente":
                    try:
                        fn(e["id"], ruta, token)
                        e[campo] = "subida" if campo == "miniatura" else "subidos"
                    except RuntimeError as err:
                        # p. ej. canal sin verificar: no admite miniaturas propias.
                        # Se anota y no se reintenta solo, para no gastar cuota.
                        e[campo] = f"falló: {err}"[:300]
                        print(f"    aviso: {campo} no se pudo subir — {err}")
                    _guardar_registro(reg)
    except Limite as lim:
        print(f"\n  YouTube cortó por hoy ({lim}).")
    faltan = sum(1 for v in videos
                 if (not a.serie or v["serie"] == a.serie) and _pendiente(v, reg.get(v["rel"])))
    print(f"\n  {subidos} videos subidos en esta corrida; quedan {faltan} pendientes.")
    salida = os.environ.get("GITHUB_OUTPUT")
    if salida:
        with open(salida, "a", encoding="utf-8") as f:
            f.write(f"subidos={subidos}\npendientes={faltan}\n")


def cmd_autorizar(a):
    """Flujo OAuth de escritorio: abre el navegador y guarda el permiso."""
    import http.server
    import secrets
    import webbrowser

    datos = json.loads(Path(a.cliente).read_text(encoding="utf-8"))
    cli = datos.get("installed") or datos.get("web")
    if not cli:
        raise SystemExit("  Ese JSON no es un cliente OAuth («installed»). Créalo en Google Cloud:\n"
                         "  APIs y servicios › Credenciales › Crear ID de cliente de OAuth › App de escritorio.")
    estado, recibido = secrets.token_urlsafe(16), {}

    class Manejador(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] == estado:
                recibido.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Listo. Ya puedes cerrar esta pestaña.".encode("utf-8"))

        def log_message(self, *_):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), Manejador)
    redir = f"http://127.0.0.1:{srv.server_port}"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cli["client_id"], "redirect_uri": redir, "response_type": "code",
        "scope": PERMISOS, "access_type": "offline", "prompt": "consent", "state": estado})
    print(f"  Abre este enlace y entra con la cuenta DEL CANAL:\n\n  {url}\n")
    webbrowser.open(url)
    while "code" not in recibido and "error" not in recibido:
        srv.handle_request()
    if "error" in recibido:
        raise SystemExit(f"  Google no dio el permiso: {recibido['error']}")
    tok = _pedir("https://oauth2.googleapis.com/token", "POST", urllib.parse.urlencode({
        "code": recibido["code"], "client_id": cli["client_id"],
        "client_secret": cli["client_secret"], "redirect_uri": redir,
        "grant_type": "authorization_code"}).encode(),
        {"Content-Type": "application/x-www-form-urlencoded"})
    TOKEN_LOCAL.write_text(json.dumps({
        "client_id": cli["client_id"], "client_secret": cli["client_secret"],
        "refresh_token": tok["refresh_token"]}, indent=2) + "\n", encoding="utf-8")
    print(f"  Permiso guardado en {TOKEN_LOCAL.name} (no se versiona).\n"
          "  Para la subida automática diaria, copia sus tres valores a los secretos del\n"
          "  repositorio en GitHub: YT_CLIENT_ID, YT_CLIENT_SECRET y YT_REFRESH_TOKEN.")


def main():
    for flujo in (sys.stdout, sys.stderr):
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="python -m tutorial.subir", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("autorizar", help="dar permiso sobre el canal (una vez)")
    p.add_argument("cliente", help="client_secret….json descargado de Google Cloud")
    p = sub.add_parser("listar", help="qué falta por subir")
    p.add_argument("--serie")
    p.add_argument("--todo", action="store_true", help="mostrar también lo ya subido y lo excluido")
    p = sub.add_parser("subir", help="subir lo que falta hasta que YouTube corte")
    p.add_argument("--serie", help="solo una carpeta de entregas/ (p. ej. clientes)")
    p.add_argument("--max", type=int, default=0, help="tope de videos en esta corrida (0 = sin tope)")
    p.add_argument("--privacidad", default=os.environ.get("YT_PRIVACIDAD") or "private",
                   choices=("private", "unlisted", "public"))
    a = ap.parse_args()
    {"autorizar": cmd_autorizar, "listar": cmd_listar, "subir": cmd_subir}[a.cmd](a)


if __name__ == "__main__":
    main()
