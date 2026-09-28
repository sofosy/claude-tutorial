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
CARTEL_MS = 6000     # un cartel sin `durante_ms` dura esto
DIAGRAMAS = RAIZ / "marca" / "diagramas"
# acciones que no mueven el cursor: caen en su palabra con el anticipo corto
ACCIONES_MARCA = ("resaltar", "cartel", "diagrama", "diagrama_fase", "diagrama_cerrar")

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

  // ---- insignia de paso, cartel y lámina de diagrama. Viven en un shadow
  // root: el CSS global de la app no los toca, el suyo no se escapa a la app,
  // y ni la sustitución de privacidad ni las sondas (alertas, barras fijas)
  // los ven. Van DEBAJO del cursor (primer hijo de la capa).
  const ui = document.createElement('div'); ui.id = '__tut_ui';
  ui.style.cssText = 'position:absolute;inset:0;pointer-events:none';
  capa.insertBefore(ui, capa.firstChild);
  const sr = ui.attachShadow({mode: 'open'});
  sr.innerHTML = `<style>
    :host{all:initial}
    *{box-sizing:border-box}
    #ins,#car,#lam{font-family:Inter,'Inter var',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
      -webkit-font-smoothing:antialiased}
    #ins{position:absolute;top:64px;left:50%;height:36px;max-width:640px;display:flex;align-items:center;gap:9px;
      padding:0 16px 0 7px;border-radius:18px;background:rgba(7,33,52,.9);color:#fff;font-size:14px;font-weight:600;
      white-space:nowrap;border:1px solid rgba(255,255,255,.14);box-shadow:0 6px 18px rgba(7,33,52,.28);
      opacity:0;transform:translate(-50%,-8px);transition:opacity .3s ease,transform .3s ease}
    #ins.on{opacity:1;transform:translate(-50%,0)}
    #ins svg{width:22px;height:22px;flex:none}
    #ins span{overflow:hidden;text-overflow:ellipsis}
    #car{position:absolute;left:88px;bottom:72px;width:max-content;max-width:420px;display:flex;gap:14px;
      align-items:flex-start;padding:16px 20px 16px 16px;border-radius:12px;background:rgba(7,33,52,.94);color:#fff;
      border:1px solid rgba(255,255,255,.12);box-shadow:0 12px 32px rgba(7,33,52,.32),0 2px 6px rgba(0,0,0,.12);
      opacity:0;transform:translateY(16px);transition:opacity .3s ease,transform .3s cubic-bezier(.22,.8,.25,1)}
    #car.on{opacity:1;transform:none}
    #car .ico{width:40px;height:40px;border-radius:10px;flex:none;display:grid;place-items:center}
    #car .ico svg{width:24px;height:24px}
    #car b{display:block;font-size:15px;font-weight:700;margin:1px 0 4px}
    #car p{margin:0;font-size:14.5px;line-height:1.45;font-weight:400;color:rgba(255,255,255,.88)}
    #lam{position:absolute;inset:0;display:none;opacity:0;transition:opacity .4s ease}
    #lam.on{opacity:1}
    #lam.claro{background:#F6F8FA;--tinta:#072134;--tinta-2:#4A5D6E;--tarjeta:#FFFFFF;--borde:#DCE3EA;--suave:#EEF2F6}
    #lam.oscuro{background:#072134;--tinta:#FFFFFF;--tinta-2:#B6C6D4;--tarjeta:#0E2E47;--borde:#2A4C66;--suave:#123754}
    #lam .dg{position:absolute;inset:0}
    #lam .dg>svg{display:block;width:100%;height:100%}
    #lam [data-fase]{opacity:0;transform:translateY(14px);
      transition:opacity .5s ease,transform .6s cubic-bezier(.22,.8,.25,1)}
    #lam [data-fase].on{opacity:1;transform:none}
  </style><div id="ins"></div><div id="lam"></div><div id="car"></div>`;
  const ins = sr.getElementById('ins'), car = sr.getElementById('car'), lam = sr.getElementById('lam');
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const ICONO_INS = {
    con: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#5BD34E"/><path d="M7 12.4l3.3 3.3L17.2 8.8" fill="none" stroke="#072134" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    sin: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#C62828"/><rect x="7.5" y="10.8" width="9" height="7.2" rx="1.6" fill="#fff"/><path d="M9.4 10.8V9a2.6 2.6 0 0 1 5.2 0v1.8" fill="none" stroke="#fff" stroke-width="1.9"/></svg>',
    info: '<svg viewBox="0 0 24 24"><path d="M12 1.5l8.5 3.2v6.1c0 5.3-3.6 9.2-8.5 11.5C7.1 20 3.5 16.1 3.5 10.8V4.7z" fill="#2F8FDB"/><circle cx="12" cy="7.6" r="1.4" fill="#fff"/><rect x="10.8" y="10.2" width="2.4" height="6.6" rx="1.2" fill="#fff"/></svg>',
  };
  const ICONO_CAR = {
    consejo: ['#F5A623', '<svg viewBox="0 0 24 24" fill="none" stroke="#072134" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21.2h4"/><path d="M12 2.8a6.2 6.2 0 0 0-3.7 11.2c.7.5 1.1 1.2 1.1 2V17h5.2v-1c0-.8.4-1.5 1.1-2A6.2 6.2 0 0 0 12 2.8z"/></svg>'],
    cuidado: ['#C62828', '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.2L2.4 20h19.2z"/><path d="M12 9.6v4.8"/><circle cx="12" cy="17.2" r=".6" fill="#fff"/></svg>'],
  };
  let insActual = null, carSeq = 0, lamCierre = null;
  const pintarIns = (d, animar) => {
    const clave = d ? JSON.stringify(d) : null;
    if (clave === insActual) return;
    insActual = clave;
    try { d ? sessionStorage.setItem('__tutIns', clave) : sessionStorage.removeItem('__tutIns'); } catch (e) {}
    if (!d) { ins.classList.remove('on'); return; }
    ins.innerHTML = (ICONO_INS[d.tipo] || ICONO_INS.info) + `<span>${esc(d.texto)}</span>`;
    ins.style.top = d.arriba != null ? d.arriba + 'px' : '';
    if (animar) { ins.classList.remove('on'); void ins.offsetWidth; ins.classList.add('on'); return; }
    // tras una recarga completa la insignia ya estaba: vuelve sin animación
    ins.style.transition = 'none'; ins.classList.add('on'); void ins.offsetWidth; ins.style.transition = '';
  };
  try { const g = sessionStorage.getItem('__tutIns'); if (g) pintarIns(JSON.parse(g), false); } catch (e) {}
  const faseLam = n => {
    const dg = lam.querySelector('.dg'); if (!dg) return;
    dg.querySelectorAll('[data-fase]').forEach(e => e.classList.toggle('on', +e.dataset.fase <= n));
    for (let k = 1; k <= 12; k++) dg.classList.toggle('fase-' + k, k <= n);
    dg.dataset.actual = n;
  };

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
    },
    // insignia del paso: {tipo: con|sin|info, texto, arriba?} o null. Queda en
    // sessionStorage, así que una recarga completa la vuelve a pintar.
    insignia(d) { pintarIns(d || null, true); },
    cartel(d) {
      const [fondo, svg] = ICONO_CAR[d.tipo] || ICONO_CAR.consejo;
      const titulo = d.titulo || (d.tipo === 'cuidado' ? 'Cuidado' : 'Consejo');
      car.innerHTML = `<div class="ico" style="background:${fondo}">${svg}</div>` +
        `<div><b>${esc(titulo)}</b><p>${esc(d.texto)}</p></div>`;
      // Sobre una lámina de diagrama el sitio de abajo a la izquierda tapa
      // tarjetas: el cartel prueba arriba a la derecha, luego abajo a la
      // derecha y luego su sitio de siempre, y se queda en la primera esquina
      // que no pisa ningún texto ni tarjeta de la lámina (también los de las
      // fases que aún no se revelan). Un subtítulo largo ocupa arriba a la
      // derecha (estado-documento), por eso no basta una esquina fija.
      const sitios = [['auto', '40px', '28px', 'auto'], ['auto', '40px', 'auto', '28px'], ['', '', '', '']];
      const poner = s => { [car.style.left, car.style.right, car.style.top, car.style.bottom] = s; };
      poner(sitios[2]);
      if (lam.classList.contains('on')) {
        const obst = [...lam.querySelectorAll('.dg text, .dg rect, .dg [data-fase]')].map(e => e.getBoundingClientRect())
          .filter(r => r.width > 2 && r.height > 2 && !(r.width > innerWidth * .8 && r.height > innerHeight * .8));
        const libre = () => { const c = car.getBoundingClientRect();
          return !obst.some(r => r.right > c.left && r.left < c.right && r.bottom > c.top - 16 && r.top < c.bottom + 16); };
        poner(sitios.find(s => { poner(s); return libre(); }) || sitios[0]);
      }
      car.classList.remove('on'); void car.offsetWidth; car.classList.add('on');
      return ++carSeq;
    },
    cartelFuera(id) { if (id == null || id === carSeq) car.classList.remove('on'); },
    // lámina a pantalla completa con un diagrama (fragmento HTML+SVG). Los
    // elementos con data-fase="N" aparecen cuando la fase llega a N; el
    // contenedor lleva además las clases fase-1…fase-N para efectos de CSS.
    diagrama(html, o) {
      o = o || {};
      if (lamCierre) { clearTimeout(lamCierre); lamCierre = null; }
      lam.className = o.fondo === 'oscuro' ? 'oscuro' : 'claro';
      lam.innerHTML = `<div class="dg">${html}</div>`;
      lam.style.display = 'block'; void lam.offsetWidth; lam.classList.add('on');
      cur.style.opacity = 0; halo.style.visibility = 'hidden';
      const f = o.fase == null ? 1 : o.fase;
      setTimeout(() => faseLam(f), 250);
    },
    fase(n) { faseLam(n); },
    diagramaCerrar() {
      lam.classList.remove('on');
      cur.style.opacity = ''; halo.style.visibility = '';
      lamCierre = setTimeout(() => { lam.style.display = 'none'; lam.innerHTML = ''; lamCierre = null; }, 450);
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

    def __init__(self, paso, reloj, inicio, palabras, pronunciacion=None):
        self.paso, self.reloj, self.inicio, self.palabras = paso, reloj, inicio, palabras
        # extra de `pronunciacion` propio del guion: el ancla `al_decir` tiene
        # que pasar por el MISMO mapa combinado que usó narrar.py al sintetizar
        # la voz, o una sigla remapeada solo por el guion nunca se encuentra.
        self.pronunciacion = pronunciacion
        self.eventos, self.enfoques = [], []
        self.alertas_vistas = set()
        self.diagrama = None   # número del diagrama que cierra el fin del paso

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

    def registro(self, tipo, que, loc=None, **extra):
        """Anota el evento y, si hay elemento, la medición de si se ve entero.

        `extra` va tal cual al evento (p. ej. `dur`: segundos que el cambio
        sigue en pantalla, que las puertas cuentan como «pantalla que cambia»).
        """
        ev = {"t": self.t(), "tipo": tipo, "que": que, **extra}
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
AIRE_INTERNO = 12  # holgura al meter un elemento en una lista interna con scroll

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

# G-14/G-19: antes se desplazaba el PRIMER ancestro con scroll (a menudo una
# lista interna) para centrar el elemento en la ventana, y además
# `scroll_into_view_if_needed` de Playwright centraba en cada contenedor. En
# pantallas con listas internas (consola de Seguridad) eso dejaba cabeceras de
# tabla cortadas y filas medio tapadas bajo el thead fijo. Ahora:
#  1. si el elemento YA se ve entero (franja de la ventana y rectángulo útil de
#     cada ancestro con scroll, descontando sus cabeceras/pies sticky) no se
#     mueve nada;
#  2. los contenedores INTERNOS se desplazan lo mínimo para que entre entero,
#     con `aire` px de holgura, sin quedar bajo sus elementos sticky;
#  3. la caja PRINCIPAL (la ventana, o el contenedor de página que ocupa casi
#     toda la franja) conserva el centrado de siempre cuando está fuera.
JS_A_LA_VISTA = "(el, [margen, aire]) => {" + JS_FRANJA + """
  const fijo = enFijo();
  const [tope, fondo] = fijo ? [0, window.innerHeight] : franja();
  const r0 = el.getBoundingClientRect();
  let top = r0.top, bot = r0.bottom, izq = r0.left, der = r0.right;
  const rueda = (s) => /(auto|scroll|overlay)/.test(s);
  const cajas = [];
  for (let n = el.parentElement; n && n !== document.body && n !== document.documentElement; n = n.parentElement) {
    const s = getComputedStyle(n);
    const v = rueda(s.overflowY) && n.scrollHeight > n.clientHeight + 1;
    const h = rueda(s.overflowX) && n.scrollWidth > n.clientWidth + 1;
    if (v || h) cajas.push({n, v, h});
  }
  const doc = document.scrollingElement;
  const docRueda = !!doc && doc.scrollHeight > window.innerHeight + 1;
  // la caja principal: la más externa si ocupa casi toda la franja; si no, la ventana
  let principal = null;
  if (!fijo) {
    const ult = cajas.filter(c => c.v).pop();
    if (ult && ult.n.clientHeight >= 0.6 * (fondo - tope)) principal = ult.n;
    else if (docRueda) principal = window;
  }
  // rectángulo útil de un contenedor: su área de contenido menos lo sticky/fixed
  // que vive dentro y se pega arriba o abajo (thead, cabeceras de bloque, leyendas)
  const SEL = 'thead, th, tfoot, [class*=sticky], [class*=header], [class*=head], [class*=footer],' +
              ' [class*=legend], [class*=leyenda], [class*=toolbar], [class*=actions]';
  const banda = (c) => {
    const cr = c.getBoundingClientRect();
    let a = cr.top + c.clientTop, b = a + c.clientHeight;
    const l = cr.left + c.clientLeft, rr = l + c.clientWidth;
    const alto = b - a;
    const cand = new Set(c.querySelectorAll(SEL));
    for (const h of c.children) { cand.add(h); for (const k of h.children) cand.add(k); }
    let k = 0, a2 = a, b2 = b;
    for (const e of cand) {
      if (++k > 400) break;
      if (e === el || e.contains(el) || el.contains(e)) continue;
      const s = getComputedStyle(e);
      if (s.position !== 'sticky' && s.position !== 'fixed') continue;
      if (s.visibility === 'hidden' || s.display === 'none') continue;
      const q = e.getBoundingClientRect();
      if (!q.height || !q.width || q.right <= l || q.left >= rr) continue;
      if (q.top <= a + 2 && q.bottom > a && q.bottom < a + alto * 0.5) a2 = Math.max(a2, q.bottom);
      if (q.bottom >= b - 2 && q.top < b && q.top > b - alto * 0.5) b2 = Math.min(b2, q.top);
    }
    return [a2, b2, l, rr];
  };
  const pos = cajas.map(c => Math.round(c.n.scrollTop) + ',' + Math.round(c.n.scrollLeft))
                   .join('|') + '|' + Math.round(window.scrollY);
  // cuánto mover para que [p, q] entre en [a, b] con `aire`: mínimo, o alineado
  // al principio si no cabe
  const minimo = (p, q, a, b) => {
    if (p >= a && q <= b) return 0;
    if (q - p > b - a - 2 * aire || p < a) return p - (a + aire);
    return q - (b - aire);
  };
  const plan = [];
  for (const c of cajas) {
    if (c.n === principal) continue;
    const [a, b, l, rr] = banda(c.n);
    let dy = c.v ? minimo(top, bot, a, b) : 0;
    let dx = c.h ? minimo(izq, der, l, rr) : 0;
    const maxY = c.n.scrollHeight - c.n.clientHeight, maxX = c.n.scrollWidth - c.n.clientWidth;
    const y = Math.max(0, Math.min(maxY, c.n.scrollTop + dy));
    const x = Math.max(0, Math.min(maxX, c.n.scrollLeft + dx));
    const ry = y - c.n.scrollTop, rx = x - c.n.scrollLeft;
    if (Math.abs(ry) < 1 && Math.abs(rx) < 1) continue;
    plan.push(() => c.n.scrollTo({top: y, left: x, behavior: 'smooth'}));
    top -= ry; bot -= ry; izq -= rx; der -= rx;
  }
  let a = tope, b = fondo;
  if (principal && principal !== window) {
    const [ca, cb] = banda(principal);
    a = Math.max(a, ca); b = Math.min(b, cb);
  }
  let visible = top >= a && bot <= b;
  if (!visible && principal) {
    const util = b - a, alto = bot - top;
    const objetivo = alto > util - 2 * margen ? a + margen : a + (util - alto) / 2;
    const delta = Math.round(top - objetivo);
    plan.push(() => principal.scrollBy({top: delta, behavior: 'smooth'}));
  }
  plan.forEach(f => f());
  // posición ANTES de pedir el desplazamiento: si en el siguiente intento no ha
  // cambiado, es que las cajas ya estaban topadas y volver a pedirlo no hará nada
  return {ok: !plan.length && visible, pasos: plan.length, tope, fondo, pos};
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
        r = loc.evaluate(JS_A_LA_VISTA, [MARGEN_VISTA, AIRE_INTERNO], timeout=8000)
        if r.get("ok"):
            return True
        pos = r.get("pos")
        if anterior is not None and pos == anterior:
            return False  # topado: no hay desplazamiento que lo arregle
        anterior = pos
        pag.wait_for_timeout(520)  # lo que dura el desplazamiento suave
    return bool(loc.evaluate(JS_A_LA_VISTA, [MARGEN_VISTA, AIRE_INTERNO], timeout=8000).get("ok"))


def _localizar(pag, sel, timeout=8000):
    loc = pag.locator(sel).first
    try:
        loc.wait_for(state="visible", timeout=timeout)
    except PlaywrightTimeout:
        raise SelectorAusente(f"no aparece o no es visible: {sel}")
    # sin `scroll_into_view_if_needed`: centra en CADA contenedor y cortaba
    # cabeceras de listas internas (G-14/G-19); `_a_la_vista` lo hace a medida
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


def instante(palabras, clave, pronunciacion=None):
    """Segundo en que la narración pronuncia `clave` (una o varias palabras).

    Es lo que sincroniza la acción con la voz: «Elijo *Borrador* en el filtro»
    dispara el clic cuando se dice «Borrador», no cuando arranca la frase.
    Si la palabra aparece varias veces se toma la PRIMERA aún no usada
    (`instante` se llama con `desde` para avanzar). Devuelve None si no está.
    """
    if isinstance(clave, (int, float)):
        return float(clave)
    # las palabras vienen del motor de voz, que oyó las siglas escritas como se
    # pronuncian: el ancla del guion pasa por el MISMO mapa combinado (global +
    # `pronunciacion` del guion) que usó narrar.para_voz al sintetizar, o una
    # sigla remapeada solo por el guion («API» → «a-pe-i») nunca se encuentra.
    buscadas = [_normal(w) for w in m_narrar.para_voz(str(clave), pronunciacion).split()]
    dichas = [_normal(p["texto"]) for p in palabras]
    for i in range(len(dichas) - len(buscadas) + 1):
        if dichas[i:i + len(buscadas)] == buscadas:
            return palabras[i]["t"]
    return None


def _instante_desde(palabras, clave, desde, pronunciacion=None):
    """Como `instante`, pero busca la primera aparición posterior a `desde`:
    en una narración larga la misma palabra puede repetirse."""
    if isinstance(clave, (int, float)):
        return float(clave)
    # ver comentario de `instante`: mismo mapa combinado (global + del guion).
    buscadas = [_normal(w) for w in m_narrar.para_voz(str(clave), pronunciacion).split()]
    dichas = [_normal(p["texto"]) for p in palabras]
    for i in range(len(dichas) - len(buscadas) + 1):
        if palabras[i]["t"] >= desde and dichas[i:i + len(buscadas)] == buscadas:
            return palabras[i]["t"]
    return instante(palabras, clave, pronunciacion)


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
    t = _instante_desde(ctx.palabras, clave, ctx.t() + anticipo - 0.3, ctx.pronunciacion)
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
_DIAG_SEQ = [0]   # número del diagrama abierto: los temporizadores solo tocan el suyo
_CTX = [None]     # contexto del paso en curso (un temporizador puede caer en el siguiente)


def _ctx_vivo(ctx):
    return _CTX[0] or ctx


# ------------------------------------------ insignia, cartel y diagrama (capa)

def _insignia(pag, datos):
    """Pinta (o quita, con None) la insignia fija del paso: arriba al centro."""
    try:
        pag.evaluate("d => window.__tut && __tut.insignia(d)", datos or None)
    except Exception:
        pass  # página a medio cargar: el init script la repinta desde sessionStorage


def _cartel(pag, ctx, acc):
    """Tarjeta flotante abajo a la izquierda que se va sola a los `durante_ms`."""
    datos = acc["cartel"]
    durante = acc.get("durante_ms", CARTEL_MS)
    mia = pag.evaluate("d => window.__tut ? __tut.cartel(d) : null", datos)
    ctx.registro("cartel", datos.get("titulo") or datos.get("tipo", "consejo"),
                 dur=round(durante / 1000, 3))
    if ctx.reloj:
        ctx.reloj.programar(ctx.reloj.ahora() + durante / 1000,
                            lambda: pag.evaluate("i => window.__tut && __tut.cartelFuera(i)", mia))


def _spec_diagrama(spec):
    """`"nombre"` o `{"nombre", "fondo", "fase", "pasos_ms"}` → dict."""
    return {"nombre": spec} if isinstance(spec, str) else dict(spec)


def _abrir_diagrama(pag, ctx, spec, durante=None):
    """Lámina a pantalla completa con `marca/diagramas/<nombre>.html`.

    Arranca en la fase 1 (o `fase`). `pasos_ms` revela las fases siguientes
    solas, a esos milisegundos desde la apertura; `diagrama_fase` las ancla a
    una palabra. Con `durante` se cierra sola; sin él, al acabar la voz del
    paso o con `diagrama_cerrar`.
    """
    nombre = spec["nombre"]
    ruta = DIAGRAMAS / f"{nombre}.html"
    if not ruta.exists():
        raise SelectorAusente(f"no existe el diagrama marca/diagramas/{nombre}.html")
    fase = spec.get("fase", 1)
    pag.evaluate("([h,o]) => window.__tut && __tut.diagrama(h,o)",
                 [ruta.read_text(encoding="utf-8"), {"fondo": spec.get("fondo", "claro"), "fase": fase}])
    _DIAG_SEQ[0] += 1
    mia = _DIAG_SEQ[0]
    extra = {"dur": round(durante / 1000, 3)} if durante else {}
    ctx.registro("diagrama", nombre, **extra)
    ctx.enfocar(None, 1.0)
    ctx.diagrama = None if durante else mia   # sin tiempo propio: lo cierra el fin del paso
    if not ctx.reloj:
        return
    t0 = ctx.reloj.ahora()
    for i, ms in enumerate(spec.get("pasos_ms") or []):
        def revelar(n=fase + 1 + i):
            if _DIAG_SEQ[0] == mia:
                _fase_diagrama(pag, _ctx_vivo(ctx), n)
        ctx.reloj.programar(t0 + ms / 1000, revelar)
    if durante:
        def cerrar():
            if _DIAG_SEQ[0] == mia:
                _cerrar_diagrama(pag, _ctx_vivo(ctx))
        ctx.reloj.programar(t0 + durante / 1000, cerrar)


def _fase_diagrama(pag, ctx, n):
    pag.evaluate("n => window.__tut && __tut.fase(n)", n)
    ctx.registro("diagrama_fase", str(n))


def _cerrar_diagrama(pag, ctx):
    _DIAG_SEQ[0] += 1   # invalida los temporizadores del que se cierra
    ctx.diagrama = None
    pag.evaluate("window.__tut && __tut.diagramaCerrar()")
    ctx.registro("diagrama_cerrar", "cerrar")


def _acciones(pag, ctx, variables):
    """Las acciones del guion, visibles y en su momento.

    Cada acción admite `al_decir`: la palabra de la narración en la que debe
    ocurrir. Sin ella, va inmediatamente después de la anterior. Además de las
    acciones de C1 (click, escribir, seleccionar, marcar, click_opcional,
    subir, presionar, esperar_ms) hay tres propias de la grabación:

    - `resaltar`: marca transitoria sobre un elemento (con `durante_ms`).
    - `quitar_marca`: apaga la marca y abre el plano.
    - `plano_general`: solo abre el plano (zoom 1) sin tocar la marca.
    - `cartel`: tarjeta de consejo/cuidado abajo a la izquierda (`durante_ms`).
    - `diagrama`, `diagrama_fase`, `diagrama_cerrar`: lámina a pantalla
      completa con revelado por fases (ver GRABACION.md).
    """
    paso = ctx.paso
    for acc in paso.get("acciones", []):
        if ctx.reloj:
            ctx.reloj.tick()
        if acc.get("al_decir") is not None:
            # una marca no necesita que el cursor «llegue»: cae en la palabra
            _esperar_palabra(ctx, acc["al_decir"], minimo=0,
                             anticipo=0.25 if any(k in acc for k in ACCIONES_MARCA) else ANTICIPO)
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
        elif "cartel" in acc:
            _cartel(pag, ctx, acc)
        elif "diagrama" in acc:
            spec = _spec_diagrama(acc["diagrama"])
            for k in ("fondo", "fase", "pasos_ms"):
                if k in acc:
                    spec[k] = acc[k]
            _abrir_diagrama(pag, ctx, spec, acc.get("durante_ms"))
        elif "diagrama_fase" in acc:
            _fase_diagrama(pag, ctx, int(acc["diagrama_fase"]))
        elif "diagrama_cerrar" in acc:
            _cerrar_diagrama(pag, ctx)
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
        insignia_previa = None
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
            ctx = Contexto(paso, grab, inicio, palabras, guion.get("pronunciacion"))
            _CTX[0] = ctx
            grab.sonda = lambda: ctx.sondear_alertas(pag)
            navego, error, meta_marcas, cursor = False, None, [], None
            # la insignia dura TODO el paso; un paso sin ella la quita
            insignia = paso.get("insignia") or None
            _insignia(pag, insignia)
            if insignia != insignia_previa:
                ctx.registro("insignia", insignia.get("texto", "") if insignia else "")
            insignia_previa = insignia
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
                    # la navegación pudo cambiar de documento (u origen): se re-empuja
                    _insignia(pag, insignia)
                elif paso.get("acciones") and paso["acciones"][0].get("al_decir") is None:
                    grab.esperar_hasta(inicio + ADELANTO)
                if paso.get("diagrama"):
                    _abrir_diagrama(pag, ctx, _spec_diagrama(paso["diagrama"]))

                _acciones(pag, ctx, variables)
                if paso.get("esperar"):
                    espera = paso.get("esperar_timeout_ms", 30000)
                    try:
                        pag.wait_for_selector(paso["esperar"], timeout=espera)
                    except PlaywrightTimeout:
                        print(f"    sin respuesta; reintento las acciones de {pid}")
                        pag.wait_for_timeout(2000)
                        _acciones(pag, Contexto(paso, None, 0, palabras, guion.get("pronunciacion")), variables)
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

            if ctx.diagrama is not None and _DIAG_SEQ[0] == ctx.diagrama:
                # la lámina se va con la última palabra: el fundido cae en este paso
                grab.esperar_hasta(inicio + dur_audio + 0.1)
                _cerrar_diagrama(pag, ctx)
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
