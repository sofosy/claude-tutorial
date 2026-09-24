"""G1 — Grabación en vivo: el navegador se graba mientras el guion se ejecuta.

Reemplaza a C1+C2 (captura + anotación de fotogramas fijos). La diferencia
de fondo: aquí el video es la grabación real de lo que pasa en pantalla —el
cursor viaja, el botón se pulsa, el menú se abre, la tabla se recarga— y la
narración se sincroniza con esas acciones porque el guion se ejecuta al ritmo
del audio, no al revés.

Cómo se consigue la sincronía sin editar a mano:

1. La voz se genera ANTES de grabar (C3), así que se conoce la duración de cada
   narración y el instante de cada palabra.
2. Cada paso del guion es un segmento: arranca cuando empieza su narración,
   ejecuta sus acciones de forma visible (cursor animado, clic con onda,
   texto tecleado) en la palabra que el guion indica (`al_decir`), y no
   termina hasta que la narración haya acabado. Si las acciones tardan más que
   la voz, el segmento se alarga; nunca se corta una frase.
3. Los fotogramas los entrega el propio Chrome (screencast de CDP) y una bomba
   los escribe a ffmpeg a 30 fps constantes con un reloj propio, así que el
   tiempo del video es exactamente el tiempo real.

El guion natural es UN paso por tarea: una narración de corrido (30–120 s) con
las acciones ancladas a sus palabras y marcas TRANSITORIAS (`resaltar` dentro
de `acciones`) que aparecen cuando la voz menciona algo y se apagan solas. El
esquema antiguo `vista` + `campos` (una marca por paso) sigue funcionando,
pero grabado en vivo se siente como una presentación de diapositivas.

El cursor, la onda del clic y los recuadros NO se dibujan después: son una
capa DOM inyectada en la página, grabada en los fotogramas. Lo que sí se
superpone después (G2) son la barra de texto, el chip de ruta y el zoom, que
sigue una línea de tiempo de «enfoques» registrada aquí: cada clic, tecleo o
marca deja constancia de dónde estaba la atención y en qué instante.

Salida: salida/<tutorial>/grabacion/master-<corrida>.mp4 + segmentos/<paso>.json
"""
import base64
import json
import subprocess
import threading
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

from . import narrar as m_narrar
from . import privacidad, tarjeta
from .anotar import COLORES
from .capturar import _rutas_locales, _sesion, _setup, _sub
from .rutas import RAIZ

# La página se cree un portátil de 1280×720 al 150 %: la interfaz sale grande y
# legible en YouTube, las media queries de la app ven 1280 (como un usuario
# real) y el screencast entrega 1920×1080 físicos. Probado: el screencast de
# CDP ignora `device_scale_factor` del contexto y captura a la resolución CSS,
# salvo que el navegador entero arranque con `--force-device-scale-factor`.
ANCHO_CSS, ALTO_CSS = 1280, 720
ESCALA = 1.5
ANCHO, ALTO = int(ANCHO_CSS * ESCALA), int(ALTO_CSS * ESCALA)
FPS = 30
PAD = 0.6            # respiro tras cada narración
ADELANTO = 0.45      # la voz arranca un instante antes de que el cursor se mueva
MOVER_MS = 550       # viaje del cursor hasta un elemento
TECLEO_MS = 45       # entre teclas al escribir
CALIDAD_JPEG = 90
ZOOM_MARCA = 1.3     # acercamiento cuando la voz señala algo
ZOOM_ACCION = 1.18   # acercamiento suave sobre lo que se pulsa o se escribe
MARCA_MS = 4500      # una marca transitoria sin `durante_ms` dura esto

_HEX = {k: "#%02x%02x%02x" % v for k, v in COLORES.items()}

# Capa de cursor, onda de clic, recuadro de resaltado y sustitución continua
# de datos privados. Se instala en CADA documento (init script), así sobrevive
# a las navegaciones completas; la posición del cursor y el mapa de privacidad
# se guardan en sessionStorage para que la recarga no los pierda ni un frame.
JS_CAPA = r"""
(() => {
  if (window.__tut) return;
  // El init script corre ANTES de que el documento tenga <html>: en ese
  // instante documentElement es null y cualquier appendChild revienta el
  // script entero sin aviso. Se instala en cuanto aparece la raíz.
  const instalar = () => {
  const css = `
    #__tut{position:fixed;inset:0;pointer-events:none;z-index:2147483647;overflow:hidden}
    #__tut_box{position:absolute;box-sizing:border-box;border:4px solid #f5a623;border-radius:9px;
      opacity:0;left:0;top:0;width:0;height:0;
      transition:left .45s cubic-bezier(.22,.8,.25,1),top .45s cubic-bezier(.22,.8,.25,1),
        width .45s cubic-bezier(.22,.8,.25,1),height .45s cubic-bezier(.22,.8,.25,1),
        opacity .25s ease,box-shadow .4s ease,border-color .3s ease}
    #__tut_box.sub{border-width:0 0 5px 0;border-radius:3px}
    #__tut_box.foco{box-shadow:0 0 0 9999px rgba(10,14,24,.62)}
    #__tut_rip{position:absolute;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;
      border:4px solid #f5a623;opacity:0}
    #__tut_rip.on{animation:__tut_rip .6s ease-out}
    @keyframes __tut_rip{0%{opacity:1;transform:scale(.5)}100%{opacity:0;transform:scale(4.5)}}
    /* El cursor es la señal principal del video: grande, con un halo ámbar
       que se enciende mientras viaja hacia una acción y pulsa al pulsar. */
    #__tut_cur{position:absolute;left:0;top:0;width:34px;height:46px;
      transform:translate(700px,470px);transition:transform .55s cubic-bezier(.22,.8,.25,1);
      filter:drop-shadow(0 3px 4px rgba(0,0,0,.5))}
    #__tut_halo{position:absolute;left:0;top:0;width:56px;height:56px;margin:-28px 0 0 -28px;border-radius:50%;
      background:rgba(245,166,35,.28);border:2px solid rgba(245,166,35,.85);opacity:0;
      transform:translate(700px,470px) scale(.6);
      transition:transform .55s cubic-bezier(.22,.8,.25,1),opacity .3s ease}
    #__tut_halo.on{opacity:1}
    #__tut_halo.pulse{animation:__tut_pulse .9s ease-in-out infinite}
    @keyframes __tut_pulse{0%,100%{box-shadow:0 0 0 0 rgba(245,166,35,.55)}50%{box-shadow:0 0 0 14px rgba(245,166,35,0)}}
  `;
  const st = document.createElement('style'); st.textContent = css;
  const capa = document.createElement('div'); capa.id = '__tut';
  capa.innerHTML = `<div id="__tut_box"></div><div id="__tut_halo"></div><div id="__tut_rip"></div>
    <svg id="__tut_cur" viewBox="0 0 24 32"><path d="M3.5 2.5 L3.5 24.5 L9 19.5 L12.8 28.8 L17 27 L13.2 18 L20.5 18 Z"
      fill="#fff" stroke="#111827" stroke-width="1.8" stroke-linejoin="round"/></svg>`;
  const raiz = document.documentElement;
  raiz.appendChild(st); raiz.appendChild(capa);
  const box = capa.querySelector('#__tut_box'), rip = capa.querySelector('#__tut_rip'),
        cur = capa.querySelector('#__tut_cur'), halo = capa.querySelector('#__tut_halo');
  let apagarHalo = null;

  // ---- privacidad: se aplica a todo lo que entra al DOM, sin esperar a Python
  let pares = [];
  try { pares = JSON.parse(sessionStorage.getItem('__tutPares') || '[]'); } catch (e) {}
  const rep = s => { for (const [a, b] of pares) if (a && s.includes(a)) s = s.split(a).join(b); return s; };
  const fijar = n => { const r = rep(n.nodeValue); if (r !== n.nodeValue) n.nodeValue = r; };
  const aplicar = root => {
    if (!pares.length || !root) return;
    if (root.nodeType === 3) return fijar(root);
    if (root.nodeType !== 1 || root.id === '__tut') return;
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n; while (n = w.nextNode()) fijar(n);
    root.querySelectorAll && root.querySelectorAll('input,textarea').forEach(e => {
      const r = rep(e.value || ''); if (r !== e.value) e.value = r; });
  };
  new MutationObserver(ms => {
    for (const m of ms) {
      if (m.type === 'characterData') fijar(m.target);
      else m.addedNodes.forEach(aplicar);
    }
  }).observe(document, {subtree: true, childList: true, characterData: true});
  document.addEventListener('DOMContentLoaded', () => aplicar(document.body));

  let pos = [700, 470];  // arranca fuera del centro, donde suele vivir el contenido
  try { pos = JSON.parse(sessionStorage.getItem('__tutCur') || 'null') || pos; } catch (e) {}
  cur.style.transitionDuration = '0ms';
  cur.style.transform = `translate(${pos[0] - 3.5}px,${pos[1] - 2.5}px)`;
  halo.style.transitionDuration = '0ms';
  halo.style.transform = `translate(${pos[0]}px,${pos[1]}px) scale(.6)`;

  window.__tut = {
    move(x, y, ms) {
      cur.style.transitionDuration = ms + 'ms';
      cur.style.transform = `translate(${x - 3.5}px,${y - 2.5}px)`;
      // el halo acompaña al cursor mientras señala y se apaga poco después
      halo.style.transitionDuration = ms + 'ms,.3s';
      halo.style.transform = `translate(${x}px,${y}px) scale(1)`;
      halo.classList.add('on'); halo.classList.add('pulse');
      if (apagarHalo) clearTimeout(apagarHalo);
      apagarHalo = setTimeout(() => { halo.classList.remove('on'); halo.classList.remove('pulse'); }, ms + 3500);
      try { sessionStorage.setItem('__tutCur', JSON.stringify([x, y])); } catch (e) {}
    },
    click(x, y) {
      rip.style.left = x + 'px'; rip.style.top = y + 'px';
      rip.classList.remove('on'); void rip.offsetWidth; rip.classList.add('on');
      halo.classList.add('on');
    },
    alertas() {
      // diálogos y avisos que la app pinta por su cuenta: toda alerta se explica
      const sel = 'mat-dialog-container, .mat-mdc-snack-bar-container, mat-snack-bar-container,' +
                  ' .swal2-popup, .toast-container .toast, app-custom-alert-dialog, [role=alertdialog], [role=alert]';
      return [...document.querySelectorAll(sel)].map(e => e.innerText.trim().replace(/\s+/g, ' ').slice(0, 160)).filter(Boolean);
    },
    box(r, estilo, color, margen) {
      const m = estilo === 'sub' ? 2 : (margen == null ? 6 : margen);
      box.className = estilo === 'sub' ? 'sub' : (estilo === 'foco' ? 'foco' : '');
      box.style.borderColor = color || '#f5a623';
      box.style.left = (r.x - m) + 'px'; box.style.top = (r.y - m) + 'px';
      box.style.width = (r.width + 2 * m) + 'px'; box.style.height = (r.height + 2 * m) + 'px';
      box.style.opacity = 1;
    },
    clear() { box.style.opacity = 0; box.className = ''; },
    priv(p) {
      pares = p; try { sessionStorage.setItem('__tutPares', JSON.stringify(p)); } catch (e) {}
      aplicar(document.body);
    }
  };
  };
  if (document.documentElement) instalar();
  else new MutationObserver((m, o) => {
    if (document.documentElement) { o.disconnect(); instalar(); }
  }).observe(document, {childList: true});
})();
"""


class Grabadora:
    """Screencast de CDP → ffmpeg, a 30 fps constantes con reloj propio.

    Chrome solo manda un fotograma cuando algo cambia en pantalla. Escribirlos
    tal cual daría un video de duración variable imposible de sincronizar, así
    que un hilo «bomba» escribe a ffmpeg el ÚLTIMO fotograma recibido tantas
    veces como ticks de 1/30 s hayan pasado. El tiempo del video es, por
    construcción, el tiempo real medido desde el arranque de la bomba.

    Los fotogramas no tocan el disco: un tutorial de media hora produciría
    varios GB en JPEG y el C: de esta máquina no los tiene.

    `programar(t, fn)` ejecuta `fn` cuando el reloj llegue a `t` (se revisa en
    cada espera): así una marca transitoria se apaga sola sin hilos extra.
    """

    def __init__(self, ctx, pag, destino):
        self.ctx, self.pag, self.destino = ctx, pag, destino
        self.ultimo = None
        self.pc0 = None
        self.escritos = 0
        self.frames_recibidos = 0
        self.pendientes = []
        self._parar = threading.Event()
        self._hilo = None
        self._proc = None
        self.cdp = None

    def arrancar(self):
        self._proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "image2pipe", "-framerate", str(FPS), "-vcodec", "mjpeg", "-i", "-",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-g", str(FPS),
             "-pix_fmt", "yuv420p", "-r", str(FPS), "-movflags", "+faststart",
             str(self.destino)],
            stdin=subprocess.PIPE, bufsize=0)
        self.cdp = self.ctx.new_cdp_session(self.pag)
        self.cdp.send("Page.enable")
        self.cdp.on("Page.screencastFrame", self._frame)
        self.cdp.send("Page.startScreencast", {
            "format": "jpeg", "quality": CALIDAD_JPEG,
            "maxWidth": ANCHO, "maxHeight": ALTO, "everyNthFrame": 1})
        for _ in range(100):
            if self.ultimo:
                break
            self.pag.wait_for_timeout(50)
        if not self.ultimo:
            raise SystemExit("El navegador no entregó ningún fotograma en 5 s")
        self.pc0 = time.perf_counter()
        self._hilo = threading.Thread(target=self._bomba, daemon=True)
        self._hilo.start()

    def _frame(self, params):
        self.ultimo = base64.b64decode(params["data"])
        self.frames_recibidos += 1
        try:
            self.cdp.send("Page.screencastFrameAck", {"sessionId": params["sessionId"]})
        except Exception:
            pass  # al detener, el último ack puede llegar tarde: no importa

    def _bomba(self):
        stdin = self._proc.stdin
        while True:
            debidos = int((time.perf_counter() - self.pc0) * FPS)
            while self.escritos < debidos:
                stdin.write(self.ultimo)
                self.escritos += 1
            if self._parar.is_set():
                break
            time.sleep(0.004)

    def ahora(self):
        """Tiempo del video, en segundos, en este instante."""
        return time.perf_counter() - self.pc0

    def programar(self, t, fn):
        self.pendientes.append((t, fn))

    sonda = None          # callable que revisa la pantalla en cada tick (alertas)
    _ultima_sonda = 0.0

    def tick(self):
        ahora = self.ahora()
        listos = [p for p in self.pendientes if p[0] <= ahora]
        for p in listos:
            self.pendientes.remove(p)
            p[1]()
        if self.sonda and ahora - self._ultima_sonda > 0.4:
            self._ultima_sonda = ahora
            self.sonda()

    def esperar_hasta(self, t):
        """Deja correr el reloj hasta el instante `t` del video.

        Se espera con el navegador y no con time.sleep: en la API síncrona de
        Playwright los eventos de CDP (los fotogramas) solo se despachan
        mientras el hilo principal está dentro de una llamada de Playwright.
        """
        while True:
            self.tick()
            falta = t - self.ahora()
            if falta <= 0:
                return
            self.pag.wait_for_timeout(min(falta * 1000, 200))

    def detener(self):
        self.esperar_hasta(self.ahora() + 0.2)
        self._parar.set()
        self._hilo.join(timeout=10)
        try:
            self.cdp.send("Page.stopScreencast")
        except Exception:
            pass
        self._proc.stdin.close()
        self._proc.wait()
        if self._proc.returncode:
            raise SystemExit(f"ffmpeg terminó con código {self._proc.returncode}")


class SelectorAusente(Exception):
    """Un selector del guion no aparece: se avisa, se salta y se sigue.

    En una grabación de media hora, morir por un selector que cambió tiraría
    todo lo grabado antes. El paso queda registrado con su error para que el
    informe lo destaque y se regrabe solo ese grupo con `--paso`.
    """


class Contexto:
    """Lo que toda acción necesita del paso en curso: reloj, línea de tiempo,
    palabras de la narración y dónde registrar eventos y enfoques."""

    def __init__(self, paso, reloj, inicio, palabras):
        self.paso, self.reloj, self.inicio, self.palabras = paso, reloj, inicio, palabras
        self.eventos, self.enfoques = [], []
        self.alertas_vistas = set()

    def sondear_alertas(self, pag):
        """Registra cada diálogo o aviso que la app muestre durante el paso.

        Regla del tutorial: toda alerta que aparezca en cámara se explica. El
        informe cruza estos eventos con las marcas para destacar la que quedó
        sin explicar.
        """
        try:
            textos = pag.evaluate("() => window.__tut ? __tut.alertas() : []")
        except Exception:
            return
        for texto in textos:
            if texto not in self.alertas_vistas:
                self.alertas_vistas.add(texto)
                self.registro("alerta", texto)

    def t(self):
        return round(self.reloj.ahora() - self.inicio, 3) if self.reloj else 0.0

    def registro(self, tipo, que, loc=None):
        """Anota el evento y, si hay elemento, la medición de si se ve entero."""
        ev = {"t": self.t(), "tipo": tipo, "que": que}
        if loc is not None:
            m = _medir_visible(loc)
            ev["visible"] = m.get("ok")
            if m.get("ok") is False:
                ev["medida"] = m
                print(f"    AVISO [{self.paso['id']}]: «{que}» NO se ve entero al {tipo}"
                      f" (elemento {m['arriba']}..{m['abajo']}px, franja visible"
                      f" {m['tope']}..{m['fondo']}px)")
        self.eventos.append(ev)

    def enfocar(self, caja_css, zoom):
        """Deja constancia de dónde está la atención: G2 acerca la cámara ahí."""
        self.enfoques.append({"t": self.t(), "zoom": zoom,
                              "caja": _caja_video(caja_css) if caja_css else None})


# ------------------------------------------------------------- acciones visibles

def _centro(caja):
    return caja["x"] + caja["width"] / 2, caja["y"] + caja["height"] / 2


def _caja_video(caja):
    """Caja CSS → píxeles del video (la escala del navegador)."""
    return [caja["x"] * ESCALA, caja["y"] * ESCALA,
            caja["width"] * ESCALA, caja["height"] * ESCALA]


def _mover(pag, x, y, ms=MOVER_MS):
    """Lleva el cursor dibujado y el ratón real al punto, con viaje animado.

    El ratón real va detrás para que la app reciba hover (tooltips, filas
    resaltadas) igual que con un usuario; el dibujado es el que se ve.
    """
    pag.evaluate("([x,y,ms]) => window.__tut && __tut.move(x,y,ms)", [x, y, ms])
    pag.mouse.move(x, y, steps=6)
    pag.wait_for_timeout(ms + 60)


MARGEN_VISTA = 28  # aire mínimo entre el elemento y las barras fijas

# Un formulario de ERP es más alto que la pantalla y tiene cabecera fija arriba
# y barra de acciones fija abajo. "Estar en el viewport" no basta: un campo
# puede quedar detrás de la barra de Guardar y el video enseña una cosa que no
# se ve. Antes de tocar, teclear o señalar algo se lleva al CENTRO de la franja
# realmente visible, con desplazamiento suave, como haría una persona.
# Barras fijas (cabecera arriba, acciones abajo). Pedir getComputedStyle de
# TODOS los elementos de una app Angular tarda ~0,5 s y retrasa cada clic; se
# mira solo a los candidatos baratos: lo que no tiene offsetParent (fixed) y
# los contenedores que por nombre suelen ser barras.
JS_FRANJA = """
  const franja = () => {
    // caché breve: las barras no cambian entre dos mediciones de la misma acción
    const c = window.__tutFranja;
    if (c && performance.now() - c.t < 800) return c.v;
    const cand = new Set(document.querySelectorAll(
      'header, footer, nav, mat-toolbar, [class*=sticky], [class*=fixed], [class*=footer],' +
      ' [class*=toolbar], [class*=actions], [class*=topbar], [class*=app-bar], [class*=navbar]'));
    // las barras fijas viven cerca de la raíz: se recorren solo 7 niveles
    const cola = [[document.body, 0]];
    while (cola.length) {
      const [n, d] = cola.shift();
      for (const h of n.children) { cand.add(h); if (d < 6) cola.push([h, d + 1]); }
    }
    let tope = 0, fondo = window.innerHeight;
    for (const e of cand) {
      if (e.id === '__tut' || e.closest('#__tut')) continue;
      const s = getComputedStyle(e);
      if (s.position !== 'fixed' && s.position !== 'sticky') continue;
      if (s.visibility === 'hidden' || s.display === 'none') continue;
      const r = e.getBoundingClientRect();
      if (r.width < window.innerWidth * 0.4 || r.height === 0) continue;
      if (r.top <= 2 && r.bottom < window.innerHeight * 0.5) tope = Math.max(tope, r.bottom);
      if (r.bottom >= window.innerHeight - 2 && r.top > window.innerHeight * 0.5) fondo = Math.min(fondo, r.top);
    }
    window.__tutFranja = {t: performance.now(), v: [tope, fondo]};
    return [tope, fondo];
  };
  // dentro de un diálogo o de un ancestro fijo (la propia barra de Guardar)
  // el elemento no puede quedar tapado por las barras
  const enFijo = () => {
    if (el.closest('.cdk-overlay-container, .cdk-overlay-pane')) return true;
    for (let n = el; n && n !== document.body; n = n.parentElement) {
      const p = getComputedStyle(n).position;
      if (p === 'fixed' || p === 'sticky') return true;
    }
    return false;
  };
"""

JS_A_LA_VISTA = "(el, margen) => {" + JS_FRANJA + """
  if (enFijo()) return {ok: true};
  const [tope, fondo] = franja();
  const r = el.getBoundingClientRect();
  if (r.top >= tope + margen && r.bottom <= fondo - margen) return {ok: true};
  const util = fondo - tope;
  const objetivo = r.height > util - 2 * margen ? tope + margen : tope + (util - r.height) / 2;
  const delta = Math.round(r.top - objetivo);
  let n = el.parentElement, contenedor = null;
  while (n) {
    const s = getComputedStyle(n);
    if (/(auto|scroll)/.test(s.overflowY) && n.scrollHeight > n.clientHeight + 1) { contenedor = n; break; }
    n = n.parentElement;
  }
  const caja = contenedor || document.scrollingElement;
  // posición ANTES de pedir el desplazamiento: si en el siguiente intento no ha
  // cambiado, es que la caja ya estaba topada y volver a pedirlo no hará nada
  const pos = Math.round(caja ? caja.scrollTop : window.scrollY);
  (contenedor || window).scrollBy({top: delta, behavior: 'smooth'});
  return {ok: false, delta, tope, fondo, pos};
}"""


# Medición sin efectos: ¿está el elemento entero dentro de la franja visible?
# Es la evidencia que queda en cada evento; no se da por hecho.
JS_VISIBLE = "(el, margen) => {" + JS_FRANJA + """
  const r = el.getBoundingClientRect();
  const dentroViewport = r.top >= 0 && r.bottom <= window.innerHeight && r.left >= 0 && r.right <= window.innerWidth;
  if (enFijo()) return {ok: dentroViewport, tope: 0, fondo: window.innerHeight,
                        arriba: Math.round(r.top), abajo: Math.round(r.bottom)};
  const [tope, fondo] = franja();
  const ok = dentroViewport && r.top >= tope && r.bottom <= fondo;
  return {ok, tope: Math.round(tope), fondo: Math.round(fondo),
          arriba: Math.round(r.top), abajo: Math.round(r.bottom)};
}"""


def _medir_visible(loc):
    try:
        return loc.evaluate(JS_VISIBLE, 0, timeout=4000)
    except Exception:
        return {"ok": None}


def _a_la_vista(pag, loc):
    """Desplaza suavemente hasta que el elemento quede entero en la franja visible.

    Hay elementos que NUNCA van a caber: los filtros pegados bajo la cabecera
    fija (ya no se puede subir más la página), una tabla más alta que la franja,
    una fila más ancha que el cuadro. Con ellos los tres intentos se gastaban
    enteros —1,56 s— y la voz llegaba a la frase siguiente antes que el clic.
    Por eso se compara la posición de desplazamiento entre un intento y el
    anterior: si no se movió, la caja está topada y seguir pidiéndolo no cambia
    nada. Se sale ya, se avisa una sola vez y el clic se da donde el elemento
    esté, que es lo que hace una persona.
    """
    anterior = None
    for _ in range(3):
        r = loc.evaluate(JS_A_LA_VISTA, MARGEN_VISTA, timeout=8000)
        if r.get("ok"):
            return True
        pos = r.get("pos")
        if anterior is not None and pos == anterior:
            return False  # topado: no hay desplazamiento que lo arregle
        anterior = pos
        pag.wait_for_timeout(520)  # lo que dura el desplazamiento suave
    return bool(loc.evaluate(JS_A_LA_VISTA, MARGEN_VISTA, timeout=8000).get("ok"))


def _localizar(pag, sel, timeout=8000):
    loc = pag.locator(sel).first
    try:
        loc.wait_for(state="visible", timeout=timeout)
    except PlaywrightTimeout:
        raise SelectorAusente(f"no aparece o no es visible: {sel}")
    loc.scroll_into_view_if_needed()
    if not _a_la_vista(pag, loc):
        print(f"    AVISO: «{sel}» no cabe entero en la franja visible;"
              " el video puede mostrarlo cortado.")
    pag.wait_for_timeout(150)  # que termine cualquier animación de entrada
    caja = loc.bounding_box()
    if not caja:
        raise SelectorAusente(f"sin caja: {sel}")
    return loc, caja


def _clic(pag, sel, ctx):
    loc, caja = _localizar(pag, sel)
    x, y = _centro(caja)
    ctx.enfocar(caja, ZOOM_ACCION)
    _mover(pag, x, y)
    pag.evaluate("([x,y]) => window.__tut && __tut.click(x,y)", [x, y])
    ctx.registro("clic", sel, loc)
    pag.mouse.click(x, y)
    pag.wait_for_timeout(180)
    return loc


def _escribir(pag, sel, texto, ctx):
    loc = _clic(pag, sel, ctx)
    pag.keyboard.press("Control+A")
    if texto:
        pag.keyboard.type(texto, delay=TECLEO_MS)
    else:
        pag.keyboard.press("Backspace")
    pag.wait_for_timeout(150)
    # se mide DESPUÉS de teclear: el campo tiene que seguir a la vista con su texto
    ctx.registro("escribir", sel, loc)


def _normal(palabra):
    return "".join(c for c in palabra.lower() if c.isalnum())


def instante(palabras, clave):
    """Segundo en que la narración pronuncia `clave` (una o varias palabras).

    Es lo que sincroniza la acción con la voz: «Elijo *Borrador* en el filtro»
    dispara el clic cuando se dice «Borrador», no cuando arranca la frase.
    Si la palabra aparece varias veces se toma la PRIMERA aún no usada
    (`instante` se llama con `desde` para avanzar). Devuelve None si no está.
    """
    if isinstance(clave, (int, float)):
        return float(clave)
    # las palabras vienen del motor de voz, que oyó las siglas escritas como se
    # pronuncian: el ancla del guion pasa por el mismo mapa o «Tipo de NCF» no
    # encontraría nunca su «ene-ce-efe».
    buscadas = [_normal(w) for w in m_narrar.para_voz(str(clave)).split()]
    dichas = [_normal(p["texto"]) for p in palabras]
    for i in range(len(dichas) - len(buscadas) + 1):
        if dichas[i:i + len(buscadas)] == buscadas:
            return palabras[i]["t"]
    return None


def _instante_desde(palabras, clave, desde):
    """Como `instante`, pero busca la primera aparición posterior a `desde`:
    en una narración larga la misma palabra puede repetirse."""
    if isinstance(clave, (int, float)):
        return float(clave)
    # las palabras vienen del motor de voz, que oyó las siglas escritas como se
    # pronuncian: el ancla del guion pasa por el mismo mapa o «Tipo de NCF» no
    # encontraría nunca su «ene-ce-efe».
    buscadas = [_normal(w) for w in m_narrar.para_voz(str(clave)).split()]
    dichas = [_normal(p["texto"]) for p in palabras]
    for i in range(len(dichas) - len(buscadas) + 1):
        if palabras[i]["t"] >= desde and dichas[i:i + len(buscadas)] == buscadas:
            return palabras[i]["t"]
    return instante(palabras, clave)


# lo que tarda el cursor en llegar y pulsar: viaje + localizar el elemento,
# comprobar que se ve entero y medirlo (unos 0,3 s en una app Angular grande)
ANTICIPO = MOVER_MS / 1000 + 0.45


def _esperar_palabra(ctx, clave, minimo=ADELANTO, anticipo=ANTICIPO):
    """Deja correr la grabación hasta que la voz esté por llegar a `clave`.

    Se descuenta el viaje del cursor: lo que debe coincidir con la palabra es
    el clic, no el arranque del movimiento. Las palabras ya «gastadas» por una
    acción anterior no se reutilizan: se busca desde el último punto.
    """
    if not ctx.reloj:
        return
    if clave is None:
        ctx.reloj.esperar_hasta(ctx.inicio + minimo)
        return
    t = _instante_desde(ctx.palabras, clave, ctx.t() + anticipo - 0.3)
    if t is None:
        print(f"    AVISO [{ctx.paso['id']}]: la narración no dice «{clave}»;"
              " la acción va al inicio.")
        ctx.reloj.esperar_hasta(ctx.inicio + minimo)
    else:
        ctx.reloj.esperar_hasta(ctx.inicio + max(t - anticipo, 0))


def _caja_texto(loc):
    b = loc.evaluate("""el => { const r = document.createRange(); r.selectNodeContents(el);
        const b = r.getBoundingClientRect();
        return b.width ? {x: b.x, y: b.y, width: b.width, height: b.height} : null; }""")
    return b or loc.bounding_box()


def _resaltar(pag, marca, ctx, cursor=True):
    """Muestra el recuadro, lleva el cursor al elemento y enfoca la cámara.

    Devuelve la caja CSS. Con `durante_ms` la marca se apaga sola: es la
    aclaración de paso («fíjate en este aviso») sin detener el flujo.
    """
    sel = marca["sel"]
    # tras un clic que guarda, la pantalla siguiente tarda: espera larga
    loc, caja = _localizar(pag, sel, timeout=15000)
    estilo = marca.get("estilo", "caja")
    if estilo == "subrayado":
        caja = _caja_texto(loc)
    if caja["x"] + caja["width"] > ANCHO_CSS or caja["x"] < 0:
        print(f"    AVISO [{ctx.paso['id']}]: «{sel}» queda fuera del ancho del cuadro"
              f" (x={int(caja['x'])}..{int(caja['x'] + caja['width'])} de {ANCHO_CSS}).")
    color = _HEX.get(marca.get("color", "ambar"), _HEX["ambar"])
    pag.evaluate("([r,e,c]) => window.__tut && __tut.box(r,e,c)",
                 [caja, {"subrayado": "sub", "foco": "foco"}.get(estilo, "caja"), color])
    ctx.registro("resaltar", sel, loc)
    ctx.enfocar(caja, marca.get("zoom", ZOOM_MARCA))
    if cursor:
        x = caja["x"] + min(caja["width"] * 0.5, caja["height"] * 2.2)
        y = caja["y"] + caja["height"] * 0.7
        _mover(pag, min(x, ANCHO_CSS - 40), y)
    durante = marca.get("durante_ms")
    if durante and ctx.reloj:
        # Cada marca lleva su número: el temporizador sólo apaga LA SUYA. Antes
        # apagaba lo que hubiera en pantalla, y si la marca siguiente ya había
        # arrancado la borraba a medio camino — medido: 46 de 116 marcas de una
        # serie duraban menos de la mitad de lo declarado (la peor, 0,7 s de 5).
        _MARCA_SEQ[0] += 1
        mia = _MARCA_SEQ[0]

        def apagar():
            if _MARCA_SEQ[0] != mia:
                return
            pag.evaluate("window.__tut && __tut.clear()")
            ctx.enfocar(None, 1.0)
        ctx.reloj.programar(ctx.reloj.ahora() + durante / 1000, apagar)
    return caja


_MARCA_SEQ = [0]


def _acciones(pag, ctx, variables):
    """Las acciones del guion, visibles y en su momento.

    Cada acción admite `al_decir`: la palabra de la narración en la que debe
    ocurrir. Sin ella, va inmediatamente después de la anterior. Además de las
    acciones de C1 (click, escribir, seleccionar, marcar, click_opcional,
    subir, presionar, esperar_ms) hay tres propias de la grabación:

    - `resaltar`: marca transitoria sobre un elemento (con `durante_ms`).
    - `quitar_marca`: apaga la marca y abre el plano.
    - `plano_general`: solo abre el plano (zoom 1) sin tocar la marca.
    """
    paso = ctx.paso
    for acc in paso.get("acciones", []):
        if ctx.reloj:
            ctx.reloj.tick()
        if acc.get("al_decir") is not None:
            # una marca no necesita que el cursor «llegue»: cae en la palabra
            _esperar_palabra(ctx, acc["al_decir"], minimo=0,
                             anticipo=0.25 if "resaltar" in acc else ANTICIPO)
        if "click" in acc:
            _clic(pag, acc["click"], ctx)
        elif "escribir" in acc:
            e = acc["escribir"]
            _escribir(pag, e["sel"], _sub(e["texto"], variables), ctx)
        elif "resaltar" in acc:
            marca = dict(acc, sel=acc["resaltar"]) if isinstance(acc["resaltar"], str) \
                else dict(acc["resaltar"])
            marca.setdefault("durante_ms", MARCA_MS)
            _resaltar(pag, marca, ctx, cursor=acc.get("cursor", True))
        elif "quitar_marca" in acc:
            pag.evaluate("window.__tut && __tut.clear()")
            ctx.enfocar(None, 1.0)
        elif "plano_general" in acc:
            ctx.enfocar(None, 1.0)
        elif "seleccionar" in acc:
            s = acc["seleccionar"]
            _, caja = _localizar(pag, s["sel"])
            ctx.enfocar(caja, ZOOM_ACCION)
            _mover(pag, *_centro(caja))
            pag.select_option(s["sel"], s["valor"])
            ctx.registro("seleccionar", s["sel"])
        elif "marcar" in acc:
            loc = pag.locator(acc["marcar"]).first
            if not loc.is_checked():
                _clic(pag, acc["marcar"], ctx)
        elif "click_opcional" in acc:
            loc = pag.locator(acc["click_opcional"]).first
            try:
                loc.wait_for(state="visible", timeout=acc.get("espera_ms", 4000))
            except PlaywrightTimeout:
                continue
            _clic(pag, acc["click_opcional"], ctx)
        elif "subir" in acc:
            s = acc["subir"]
            # Un `<input type=file>` puede estar OCULTO detrás de un botón
            # estilizado que sólo hace `input.click()` — así lo monta
            # `product-bulk-dialog.component.ts`, con el atributo `hidden`. Ahí
            # `_localizar` lanzaba SelectorAusente (exige `state=visible`) y con
            # ella se perdía el RESTO del paso, mientras que `ensayar.mjs`
            # pasaba limpio porque `setInputFiles` sí acepta un input oculto:
            # el fallo sólo aparecía en cámara. Con `ancla` el cursor viaja al
            # elemento VISIBLE que el usuario pulsaría y el archivo se le
            # entrega igual al input. Sin `ancla` el comportamiento es el de
            # siempre, byte a byte (los guiones que suben sobre un `label`
            # visible no cambian).
            # Con `ancla` se va DIRECTO al elemento visible: esperar a que el
            # input oculto sea visible gastaba los 8 s de `_localizar` y el
            # archivo llegaba ocho segundos tarde respecto a su palabra
            # (toma del 07/09, video 4: «Subo el archivo» +7,95 s).
            _, caja = _localizar(pag, s["ancla"] if s.get("ancla") else s["sel"])
            _mover(pag, *_centro(caja))
            pag.locator(s["sel"]).first.set_input_files(str(RAIZ / s["archivo"]))
            ctx.registro("subir", s["sel"])
        elif "presionar" in acc:
            p = acc["presionar"]
            if p.get("sel"):
                pag.press(p["sel"], p["tecla"])
            else:
                pag.keyboard.press(p["tecla"])
            ctx.registro("tecla", p["tecla"])
        elif "esperar_ms" in acc:
            pag.wait_for_timeout(acc["esperar_ms"])
        elif "al_decir" in acc and len(acc) == 1:
            pass  # solo esperar a la palabra: sirve para ritmar
        else:
            raise SystemExit(f"[{paso['id']}] acción desconocida: {acc}")


# --------------------------------------------------------------------- motor

def _narraciones(guion, pasos, salida):
    """Garantiza el audio de cada paso: la duración manda sobre el ritmo.

    Se re-narra solo lo que cambió (hash de texto+voz+velocidad): corregir una
    frase cuesta esa frase, no la voz del tutorial entero.
    """
    voz = guion.get("voz", {})
    vid, vel = voz.get("id", m_narrar.VOZ_DEFECTO), voz.get("velocidad", m_narrar.VELOCIDAD_DEFECTO)
    mapa = privacidad.cargar_mapa(salida)
    faltan = []
    for p in pasos:
        texto = privacidad.aplicar_a_texto(p["narracion"], mapa)
        side = m_narrar.sidecar(salida, p["id"])
        if (not side or side.get("hash") != m_narrar.hash_narracion(texto, vid, vel)
                or not side.get("palabras")
                or not (salida / "audio" / f"{p['id']}.mp3").exists()):
            faltan.append(p)
    if faltan:
        print(f"  narrando {len(faltan)} pasos (nuevos o con la redacción cambiada)…")
        m_narrar.narrar(guion, faltan, salida)
    return {p["id"]: m_narrar.sidecar(salida, p["id"]) for p in pasos}


def _navegar(pag, base, ruta, guion):
    """Cambia de pantalla como lo haría el usuario: sin recargar la app.

    Una app Angular tarda segundos en arrancar y pinta esqueletos mientras
    tanto; recargarla en cada paso llenaría el video de pantallas en blanco.
    Con `spa` (por defecto) la navegación es interna: se empuja la ruta al
    historial y se avisa al router con `popstate`, que es exactamente lo que
    hace el botón «atrás» del navegador. Solo se carga completo si no hay nada
    cargado (una página estática sin sesión) o si el guion desactiva `spa`.

    Volver a la MISMA ruta no reinicia la vista en un SPA, y muchos guiones
    re-navegan justo para limpiar filtros: se pasa por una ruta neutra antes.
    """
    destino = base + ruta
    if not guion.get("spa", True) or not pag.url.startswith(base):
        pag.goto(destino, wait_until="networkidle")
        return True
    empujar = ("r => { history.pushState({}, '', r);"
               " dispatchEvent(new PopStateEvent('popstate', {state: {}})); }")
    actual = pag.url[len(base):].split("?")[0]
    if actual == ruta.split("?")[0]:
        pag.evaluate(empujar, guion.get("ruta_neutra", "/"))
        pag.wait_for_timeout(400)
    pag.evaluate(empujar, ruta)
    pag.wait_for_timeout(300)
    pag.wait_for_load_state("networkidle")
    return False


def _empujar_privacidad(pag, mapa):
    if mapa:
        pag.evaluate("p => window.__tut && __tut.priv(p)",
                     sorted(mapa.items(), key=lambda kv: -len(kv[0])))


def grabar(guion, pasos, salida):
    duraciones = _narraciones(guion, pasos, salida)
    carpeta = salida / "grabacion"
    segmentos = carpeta / "segmentos"
    segmentos.mkdir(parents=True, exist_ok=True)
    corrida = time.strftime("%Y%m%d-%H%M%S")
    master = carpeta / f"master-{corrida}.mp4"
    base = guion["base_url"].rstrip("/")

    variables = dict(guion.get("variables", {}))
    db = guion.get("db")
    mapa_priv = privacidad.cargar_mapa(salida)
    cfg_priv = guion.get("privacidad")

    with sync_playwright() as p:
        nav = p.chromium.launch(args=[f"--force-device-scale-factor={ESCALA}"])
        ctx_nav = nav.new_context(viewport={"width": ANCHO_CSS, "height": ALTO_CSS},
                                  device_scale_factor=ESCALA)
        ctx_nav.add_init_script(JS_CAPA)
        _rutas_locales(ctx_nav, guion)
        _setup({"id": "guion", "setup": guion.get("setup")}, variables, db)
        pag = ctx_nav.new_page()
        _sesion(pag, guion, variables, base)

        # `privacidad.mapa_fijo`: sustituciones de texto declaradas por el guion
        # (p. ej. el host local del API en un enlace público → dominio real).
        # Se empujan una vez tras la sesión; la capa las aplica a todo lo que
        # entre al DOM y las conserva en sessionStorage entre navegaciones.
        fijo = (cfg_priv or {}).get("mapa_fijo") or {}
        if fijo:
            mapa_priv = {**fijo, **mapa_priv}
            _empujar_privacidad(pag, mapa_priv)

        grab = None
        for paso in pasos:
            pid = paso["id"]
            print(f"  · {pid}")
            dur_audio = duraciones[pid]["duracion"]
            palabras = duraciones[pid].get("palabras", [])

            if paso.get("tarjeta"):
                png = segmentos / f"{pid}.png"
                datos = {**guion.get("marca", {}), **paso["tarjeta"]}
                tarjeta.render(datos, png, [ANCHO, ALTO])
                (segmentos / f"{pid}.json").write_text(json.dumps({
                    "id": pid, "tipo": "tarjeta", "imagen": png.name,
                    "duracion": dur_audio + PAD, "tamano": [ANCHO, ALTO],
                }, indent=2, ensure_ascii=False), encoding="utf-8")
                continue

            # el setup (seeds, SQL) no es parte del video: corre con el reloj parado
            _setup(paso, variables, db)
            if grab is None:
                grab = Grabadora(ctx_nav, pag, master)
                grab.arrancar()

            inicio = grab.ahora()
            ctx = Contexto(paso, grab, inicio, palabras)
            grab.sonda = lambda: ctx.sondear_alertas(pag)
            navego, error, meta_marcas, cursor = False, None, [], None
            try:
                if paso.get("navegar"):
                    # la marca del paso anterior no debe sobrevivir bajo la barra nueva
                    pag.evaluate("window.__tut && __tut.clear()")
                    ctx.enfocar(None, 1.0)
                    _esperar_palabra(ctx, paso.get("al_decir_navegar"))
                    navego = _navegar(pag, base, _sub(paso["navegar"], variables), guion)
                    ctx.registro("navegar", paso["navegar"])
                    pag.evaluate("window.__tut && __tut.clear()")
                    _empujar_privacidad(pag, mapa_priv)
                elif paso.get("acciones") and paso["acciones"][0].get("al_decir") is None:
                    grab.esperar_hasta(inicio + ADELANTO)

                _acciones(pag, ctx, variables)
                if paso.get("esperar"):
                    espera = paso.get("esperar_timeout_ms", 30000)
                    try:
                        pag.wait_for_selector(paso["esperar"], timeout=espera)
                    except PlaywrightTimeout:
                        print(f"    sin respuesta; reintento las acciones de {pid}")
                        pag.wait_for_timeout(2000)
                        _acciones(pag, Contexto(paso, None, 0, palabras), variables)
                        pag.wait_for_selector(paso["esperar"], timeout=espera)
                if paso.get("pausa_ms"):
                    pag.wait_for_timeout(paso["pausa_ms"])

                for sel in paso.get("ocultar", []):
                    pag.eval_on_selector_all(
                        sel, "els => els.forEach(e =>"
                             " e.style.setProperty('display', 'none', 'important'))")
                encuadre = paso.get("desplazar")
                if encuadre:
                    pag.locator(encuadre["sel"]).first.evaluate(
                        "(el, b) => el.scrollIntoView({block: b, behavior: 'smooth'})",
                        encuadre.get("bloque", "start"))
                    pag.wait_for_timeout(700)

                if cfg_priv:
                    antes = len(mapa_priv)
                    mapa_priv = privacidad.sustituir(pag, cfg_priv, mapa_priv)
                    if len(mapa_priv) > antes:
                        print(f"    privacidad: {len(mapa_priv) - antes} valores nuevos")
                        _empujar_privacidad(pag, mapa_priv)

                # esquema antiguo: una marca fija por paso (vista + campos)
                marcas = paso.get("resaltar", [])
                if marcas:
                    if paso.get("al_decir"):
                        _esperar_palabra(ctx, paso["al_decir"], minimo=0, anticipo=0.25)
                    cur = paso.get("cursor", True)
                    caja = _resaltar(pag, dict(marcas[0], zoom=paso.get("kenburns", {}).get("zoom", ZOOM_MARCA)),
                                     ctx, cursor=cur is not False and not isinstance(cur, str))
                    meta_marcas.append(dict(marcas[0], caja=_caja_video(caja)))
                    if isinstance(cur, str):
                        _, destino = _localizar(pag, cur)
                        _mover(pag, *_centro(destino))
                elif not paso.get("acciones"):
                    pag.evaluate("window.__tut && __tut.clear()")
            except (SelectorAusente, PlaywrightTimeout) as e:
                # el paso se graba igual (la voz sigue) y queda marcado: el
                # informe lo destaca y se regraba solo ese grupo con --paso
                error = str(e).splitlines()[0][:200]
                print(f"    ERROR [{pid}]: {error}")
                pag.evaluate("window.__tut && __tut.clear()")

            grab.esperar_hasta(inicio + dur_audio + PAD)
            grab.tick()
            ctx.sondear_alertas(pag)
            grab.sonda = None
            fin = grab.ahora()
            (segmentos / f"{pid}.json").write_text(json.dumps({
                "id": pid, "tipo": "video", "master": master.name,
                "inicio": round(inicio, 3), "fin": round(fin, 3),
                "duracion": round(fin - inicio, 3),
                "duracion_audio": dur_audio,
                "navego": navego, "eventos": ctx.eventos, "enfoques": ctx.enfoques,
                "error": error,
                "tamano": [ANCHO, ALTO], "resaltar": meta_marcas,
                "texto_pantalla": paso.get("texto_pantalla"), "ruta": paso.get("ruta"),
            }, indent=2, ensure_ascii=False), encoding="utf-8")
            extra = fin - inicio - dur_audio - PAD
            aviso = f"  (+{extra:.1f}s: las acciones duraron más que la voz)" if extra > 0.3 else ""
            print(f"    {fin - inicio:.1f}s{aviso}")

        if grab:
            grab.detener()
            print(f"  maestro: {master.name}  ({grab.ahora():.0f}s,"
                  f" {grab.frames_recibidos} fotogramas del navegador)")
        nav.close()

    if mapa_priv:
        privacidad.guardar_mapa(salida, mapa_priv)
