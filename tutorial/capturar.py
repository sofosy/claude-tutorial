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
        elif "click_opcional" in acc:
            # avisos del arranque que aparecen o no según el estado de la
            # sesión: si no está, no es un error, es que no había nada que cerrar
            loc = pag.locator(acc["click_opcional"]).first
            try:
                loc.click(timeout=acc.get("espera_ms", 4000))
            except PlaywrightTimeout:
                pass
        elif "subir" in acc:
            # el <input type=file> suele estar oculto tras un botón: se le
            # pasa el archivo directamente, sin abrir el diálogo del sistema
            s = acc["subir"]
            pag.locator(s["sel"]).first.set_input_files(str(RAIZ / s["archivo"]))
        elif "presionar" in acc:
            # los campos de etiquetas (app-chips) confirman con Enter: sin esto
            # el texto queda escrito pero la etiqueta nunca se agrega
            p = acc["presionar"]
            pag.press(p["sel"], p["tecla"])
        elif "esperar_ms" in acc:
            pag.wait_for_timeout(acc["esperar_ms"])
        else:
            raise SystemExit(f"[{paso['id']}] acción desconocida: {acc}")


def _sesion(pag, guion, variables, base):
    """Entra a la aplicación antes del primer paso, sin capturar nada.

    Una corrida de `capturar` abre un solo contexto de navegador, así que la
    sesión vive para todo el guion. Se hace aquí y no como paso porque el
    formulario de acceso no es parte de ningún tutorial: sale en todos y no
    enseña nada. Los selectores tienen valor por defecto y se pueden
    sobrescribir para otra aplicación.
    """
    s = guion.get("sesion")
    if not s:
        return
    pag.goto(base + s.get("navegar", "/authentication/signin"),
             wait_until="networkidle")
    pag.fill(s.get("sel_usuario", "input[formcontrolname='username']"),
             _sub(s["usuario"], variables))
    pag.fill(s.get("sel_clave", "input[formcontrolname='password']"),
             _sub(s["clave"], variables))
    pag.click(s.get("sel_entrar", "button.login-button"))
    if s.get("esperar"):
        pag.wait_for_selector(s["esperar"], timeout=s.get("esperar_timeout_ms", 30000))
    else:
        # sin selector que esperar, basta con salir de la pantalla de acceso
        pag.wait_for_url(lambda u: "signin" not in u, timeout=30000)
    print(f"  · sesión: {_sub(s['usuario'], variables)}")


JS_ENCUADRAR = """(el) => {
  // La aplicación tiene cabecera fija y el contenido scrollea por debajo, así
  // que "estar dentro del viewport" no basta: un elemento puede quedar tapado
  // por la barra superior. Se mide el estorbo real en vez de suponerlo.
  const estorbo = () => {
    let tope = 0;
    for (const e of document.querySelectorAll('body *')) {
      const s = getComputedStyle(e);
      if (s.position !== 'fixed' && s.position !== 'sticky') continue;
      if (s.visibility === 'hidden' || s.display === 'none') continue;
      const r = e.getBoundingClientRect();
      // solo lo que se pega arriba y cubre buena parte del ancho
      if (r.top <= 2 && r.bottom > tope && r.width > window.innerWidth * 0.4
          && r.bottom < window.innerHeight * 0.5) tope = r.bottom;
    }
    return tope;
  };
  // Un diálogo se pinta ENCIMA de la cabecera (vive en la capa de overlay y es
  // de posición fija), así que la cabecera no lo tapa: descontarla ahí daría un
  // falso aviso y obligaría a partir un paso que en realidad se ve completo.
  const enOverlay = (() => {
    if (el.closest('.cdk-overlay-container, .cdk-overlay-pane')) return true;
    // basta con que un ANCESTRO sea fijo: un botón dentro del propio banner
    // superior no puede estar tapado por ese banner
    for (let n = el; n; n = n.parentElement) {
      const pos = getComputedStyle(n).position;
      if (pos === 'fixed' || pos === 'sticky') return true;
    }
    return false;
  })();
  const tope = enOverlay ? 0 : estorbo();
  const util = window.innerHeight - tope;
  const visible = () => {
    const r = el.getBoundingClientRect();
    return r.top >= tope - 1 && r.bottom <= window.innerHeight + 1;
  };
  const alto = () => el.getBoundingClientRect().height;

  if (visible()) return {ok: true, alto: alto(), tope};
  if (alto() > util) return {ok: false, alto: alto(), tope};

  // Se desplaza el contenedor que de verdad scrollea (puede ser la ventana o
  // un contenedor interno), lo justo para dejarlo libre de la cabecera.
  const contenedor = (() => {
    let n = el.parentElement;
    while (n) {
      const s = getComputedStyle(n);
      if (/(auto|scroll)/.test(s.overflowY) && n.scrollHeight > n.clientHeight) return n;
      n = n.parentElement;
    }
    return document.scrollingElement;
  })();
  for (let i = 0; i < 4 && !visible(); i++) {
    const r = el.getBoundingClientRect();
    const delta = r.top < tope ? r.top - tope - 12
                               : r.bottom - window.innerHeight + 12;
    if (Math.abs(delta) < 1) break;
    contenedor.scrollTop += delta;
    if (!visible()) window.scrollBy(0, delta);
  }
  return {ok: visible(), alto: alto(), tope};
}"""


def _encuadrar(pag, sel, paso):
    """Deja el componente explicado completamente dentro del encuadre.

    Es la garantía mecánica de que el video nunca muestra a medias la sección de
    la que habla la narración: revisarlo a ojo frame por frame no escala, y un
    componente cortado contradice lo que se está explicando. Se reintenta porque
    Angular puede seguir creciendo la vista después del primer scroll.
    """
    loc = pag.locator(sel).first
    for intento in range(3):
        r = loc.evaluate(JS_ENCUADRAR)
        pag.wait_for_timeout(350)
        if r["ok"]:
            return
    print(f"    AVISO [{paso['id']}]: «{sel}» no se ve entero"
          f" (alto {int(r['alto'])}px, cabecera fija {int(r['tope'])}px)."
          f" Divide el paso o marca una parte.")


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
        # El setup del guion prepara el entorno ANTES de entrar: un seed que
        # borra y vuelve a crear la empresa desde cero también borra el usuario
        # con el que se inicia sesión, así que hacerlo después dejaría la sesión
        # del navegador inválida a media captura.
        _setup({"id": "guion", "setup": guion.get("setup")}, variables, db)

        pag = ctx.new_page()
        _sesion(pag, guion, variables, base)

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

            # Un selector puede existir mientras la vista sigue cargando: los
            # listados de Germiva pintan primero un esqueleto gris. `pausa_ms`
            # espera a que la pantalla quede como la verá el usuario, antes de
            # sustituir datos y de medir las cajas de las marcas.
            if paso.get("pausa_ms"):
                pag.wait_for_timeout(paso["pausa_ms"])

            marcas = paso.get("resaltar", [])
            # Encuadre. Por defecto se centra la marca, que es lo que se quiere
            # casi siempre. `desplazar` lo hace a mano cuando centrar corta por
            # la mitad lo que hay que mostrar entero (una tarjeta con su botón,
            # una tabla con su encabezado). Va DESPUÉS de la pausa: si la vista
            # todavía estaba creciendo, un scroll anterior queda obsoleto.
            # Componentes que no son el tema del paso y que no deben salir. El
            # caso real: Germiva sirve el resumen de la cartera de un caché de
            # 5 minutos, así que después de un cambio hecho en cámara muestra el
            # número anterior. Antes que enseñar un dato falso, se saca del plano.
            for sel in paso.get("ocultar", []):
                pag.eval_on_selector_all(
                    sel, "els => els.forEach(e => e.style.display = 'none')")
            if paso.get("ocultar"):
                pag.wait_for_timeout(200)

            encuadre = paso.get("desplazar")
            if encuadre:
                # Encuadre explícito del autor: alinea siempre, aunque el
                # elemento ya se viera. Sirve para decidir qué queda FUERA del
                # plano, no solo qué entra.
                pag.locator(encuadre["sel"]).first.evaluate(
                    "(el, b) => el.scrollIntoView({block: b, behavior: 'instant'})",
                    encuadre.get("bloque", "start"))
                pag.wait_for_timeout(400)
            if marcas:
                # y en cualquier caso, la marca tiene que verse completa
                _encuadrar(pag, marcas[0]["sel"], paso)

            # La sustitución va lo más pegada posible al screenshot, y después
            # del scroll: Angular vuelve a pintar sus componentes al cambiar de
            # ruta o al terminar de cargar, y un valor ya sustituido reaparece
            # con su texto original si queda tiempo entre sustituir y capturar.
            cfg_priv = guion.get("privacidad")
            if cfg_priv:
                antes = len(mapa_priv)
                mapa_priv = privacidad.sustituir(pag, cfg_priv, mapa_priv)
                if len(mapa_priv) > antes:
                    print(f"    privacidad: {len(mapa_priv) - antes} valores nuevos"
                          f" ({len(mapa_priv)} en total)")

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
                # sin `hacia` el acercamiento va al centro del frame: es lo que
                # se quiere cuando lo que hay que mirar es la pantalla entera
                # (una tabla completa) y no un elemento concreto
                meta["kenburns"] = {"zoom": kb.get("zoom", 1.3)}
                if kb.get("hacia"):
                    meta["kenburns"]["caja"] = _caja(pag, kb["hacia"], paso)
            (frames / f"{paso['id']}.json").write_text(
                json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

        nav.close()

    if mapa_priv:
        privacidad.guardar_mapa(salida, mapa_priv)
