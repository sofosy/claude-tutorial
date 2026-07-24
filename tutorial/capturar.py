"""C1 — Captura con Playwright.

Toma el screenshot de cada paso y extrae el bounding box REAL de cada elemento a
resaltar, leído del navegador. Es lo que hace que las marcas caigan exactas en vez
de aproximadas.
"""
import json
import shutil
import subprocess
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

from . import privacidad, tarjeta
from .rutas import RAIZ

ANCHO, ALTO = 1280, 720
CROMO = 48          # alto de la barra del navegador, en px CSS
ALTO_PAGINA = ALTO - CROMO   # así el frame final sigue siendo 16:9 exacto
ESCALA = 2  # device_scale_factor: capturar a 2x da margen para el zoom sin pixelar


def _env(ruta):
    env = {}
    for linea in Path(ruta).read_text(encoding="utf-8", errors="ignore").splitlines():
        linea = linea.strip()
        if "=" in linea and not linea.startswith("#"):
            k, v = linea.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _sql(db, query):
    """Consulta directa a la base. Devuelve la primera celda, o None."""
    if not db:
        raise SystemExit("El guion usa setup sql pero no declara el bloque 'db'")
    e = _env(db["env"])
    cliente = db.get("cliente") or shutil.which("mysql") or "mysql"
    r = subprocess.run(
        [cliente, "-h", e["DB_HOST"], "-P", e.get("DB_PORT", "3306"),
         "-u", e["DB_USERNAME"], "-p" + e["DB_PASSWORD"], e["DB_DATABASE"],
         "-N", "-e", query],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"Error de SQL: {r.stderr.strip()[:300]}")
    salida = r.stdout.strip()
    return salida.split("\t")[0] if salida else None


def _con_cromo(png, url):
    """Compone la barra del navegador encima de la captura.

    La URL real ubica al usuario mejor que cualquier etiqueta dibujada, y de paso
    le enseña la dirección a la que tiene que llegar. La barra es parte de la
    imagen, no una capa: así se comporta como en una grabación de pantalla.
    """
    from PIL import Image, ImageDraw

    from .anotar import _fuente

    pagina = Image.open(png)
    alto = CROMO * ESCALA
    img = Image.new("RGB", (pagina.width, pagina.height + alto), (48, 49, 52))
    dib = ImageDraw.Draw(img)

    r = 9 * ESCALA
    for i, color in enumerate([(237, 106, 94), (245, 191, 79), (98, 197, 84)]):
        cx = (24 + i * 22) * ESCALA
        dib.ellipse([cx - r, alto // 2 - r, cx + r, alto // 2 + r], fill=color)

    x0, x1 = 108 * ESCALA, pagina.width - 60 * ESCALA
    dib.rounded_rectangle([x0, 9 * ESCALA, x1, alto - 9 * ESCALA],
                          radius=8 * ESCALA, fill=(32, 33, 36))
    dib.text((x0 + 22 * ESCALA, alto // 2), url, fill=(190, 196, 204),
             font=_fuente(15 * ESCALA), anchor="lm")

    img.paste(pagina, (0, alto))
    img.save(png)


def _setup(paso, variables, db):
    """Deja el sistema en el estado que el paso necesita, antes de capturar.

    El resultado de una consulta se puede guardar en una variable y usarla luego
    en las acciones como {{nombre}}: es lo que permite grabar un flujo con código
    de verificación sin depender de que llegue un correo.
    """
    s = paso.get("setup")
    if not s:
        return
    if s["tipo"] == "shell":
        print(f"    setup shell: {s['cmd']}")
        subprocess.run(s["cmd"], shell=True, check=True, cwd=RAIZ)
    elif s["tipo"] == "sql":
        valor = _sql(db, _sub(s["query"], variables))
        if s.get("guardar_en"):
            variables[s["guardar_en"]] = valor
            print(f"    setup sql: {s['guardar_en']} = {valor}")
        else:
            print("    setup sql: ok")
    else:
        raise SystemExit(f"[{paso['id']}] setup tipo '{s['tipo']}' no soportado")


def _sub(texto, variables):
    for k, v in variables.items():
        texto = texto.replace("{{%s}}" % k, str(v))
    return texto


def _acciones(pag, paso, variables):
    for acc in paso.get("acciones", []):
        if "click" in acc:
            pag.click(acc["click"])
        elif "escribir" in acc:
            e = acc["escribir"]
            pag.fill(e["sel"], _sub(e["texto"], variables))
        elif "seleccionar" in acc:
            s = acc["seleccionar"]
            pag.select_option(s["sel"], s["valor"])
        elif "marcar" in acc:
            # Angular Material esconde el <input> real tras la etiqueta
            pag.locator(acc["marcar"]).first.check(force=True)
        elif "esperar_ms" in acc:
            pag.wait_for_timeout(acc["esperar_ms"])
        else:
            raise SystemExit(f"[{paso['id']}] acción desconocida: {acc}")


JS_CAJA_TEXTO = """el => {
  const r = document.createRange();
  r.selectNodeContents(el);
  const b = r.getBoundingClientRect();
  return b.width ? {x: b.x, y: b.y, width: b.width, height: b.height} : null;
}"""


def _caja(pag, sel, paso, solo_texto=False):
    """Caja del elemento, en píxeles del screenshot.

    `solo_texto` mide el texto en vez del elemento: una entrada de menú es un <a>
    de ancho completo, y subrayarla entera produce una línea que parece separador
    en vez de subrayado. Lo que hay que subrayar son las palabras.
    """
    loc = pag.locator(sel).first
    if loc.count() == 0:
        raise SystemExit(f"[{paso['id']}] selector sin resultados: {sel}")
    b = loc.evaluate(JS_CAJA_TEXTO) if solo_texto else None
    if b is None:
        b = loc.bounding_box()
    if b is None:
        raise SystemExit(f"[{paso['id']}] selector no visible: {sel}")
    # la barra del navegador desplaza la página hacia abajo en el frame final
    return [b["x"] * ESCALA, (b["y"] + CROMO) * ESCALA,
            b["width"] * ESCALA, b["height"] * ESCALA]


def capturar(guion, pasos, salida):
    frames = salida / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    base = guion["base_url"].rstrip("/")

    variables = dict(guion.get("variables", {}))
    db = guion.get("db")
    # se acumula entre pasos y se conserva: narración, subtítulos y descripción
    # tienen que usar los mismos valores inventados que quedaron en pantalla
    mapa_priv = privacidad.cargar_mapa(salida)

    with sync_playwright() as p:
        nav = p.chromium.launch()
        ctx = nav.new_context(viewport={"width": ANCHO, "height": ALTO_PAGINA},
                              device_scale_factor=ESCALA)
        pag = ctx.new_page()

        for paso in pasos:
            print(f"  · {paso['id']}")

            if paso.get("tarjeta"):  # título o cierre: no viene del navegador
                tam = [ANCHO * ESCALA, ALTO * ESCALA]
                # la marca sale de la config, no del guion: así todas las
                # tarjetas de todos los tutoriales quedan iguales
                datos = {**guion.get("marca", {}), **paso["tarjeta"]}
                tarjeta.render(datos, frames / f"{paso['id']}.png", tam)
                (frames / f"{paso['id']}.json").write_text(json.dumps(
                    {"tamano": tam, "resaltar": []}, indent=2), encoding="utf-8")
                continue

            _setup(paso, variables, db)
            if paso.get("navegar"):
                pag.goto(base + paso["navegar"], wait_until="networkidle")
            _acciones(pag, paso, variables)
            if paso.get("esperar"):
                espera = paso.get("esperar_timeout_ms", 30000)
                try:
                    pag.wait_for_selector(paso["esperar"], timeout=espera)
                except PlaywrightTimeout:
                    # los formularios de Angular a veces ignoran un click que
                    # llega antes de que terminen sus validaciones asíncronas.
                    # Reintentar una vez sale más barato que inflar las esperas
                    print(f"    sin respuesta; reintento las acciones de {paso['id']}")
                    pag.wait_for_timeout(3000)
                    _acciones(pag, paso, variables)
                    pag.wait_for_selector(paso["esperar"], timeout=espera)

            # la sustitución va antes de la captura y después de las acciones:
            # los datos sensibles pueden haber entrado al llenar el formulario
            cfg_priv = guion.get("privacidad")
            if cfg_priv:
                antes = len(mapa_priv)
                mapa_priv = privacidad.sustituir(pag, cfg_priv, mapa_priv)
                if len(mapa_priv) > antes:
                    print(f"    privacidad: {len(mapa_priv) - antes} valores nuevos"
                          f" ({len(mapa_priv)} en total)")

            marcas = paso.get("resaltar", [])
            if marcas:
                pag.locator(marcas[0]["sel"]).first.scroll_into_view_if_needed()
                pag.wait_for_timeout(300)  # deja asentar el scroll suave

            png = frames / f"{paso['id']}.png"
            pag.screenshot(path=str(png))
            # el video es para el público: se graba contra local, pero la barra
            # muestra el dominio real. Sin esto el tutorial enseña localhost
            _con_cromo(png, pag.url.replace(base, guion.get("url_publica", base)))

            meta = {
                "tamano": [ANCHO * ESCALA, ALTO * ESCALA],
                "resaltar": [
                    dict(m, caja=_caja(pag, m["sel"], paso,
                                       solo_texto=m.get("estilo") == "subrayado"))
                    for m in marcas
                ],
                "texto_pantalla": paso.get("texto_pantalla"),
                "ruta": paso.get("ruta"),
            }
            # por defecto el puntero va sobre la primera marca: es la acción
            # principal del paso. Se apunta a otra con "cursor": "<sel>", o se
            # quita con "cursor": false
            cur = paso.get("cursor", True)
            if cur is not False and marcas:
                meta["cursor"] = (_caja(pag, cur, paso) if isinstance(cur, str)
                                  else meta["resaltar"][0]["caja"])

            kb = paso.get("kenburns")
            if kb:
                meta["kenburns"] = {"zoom": kb.get("zoom", 1.3),
                                    "caja": _caja(pag, kb["hacia"], paso)}
            (frames / f"{paso['id']}.json").write_text(
                json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

        nav.close()

    if mapa_priv:
        privacidad.guardar_mapa(salida, mapa_priv)
