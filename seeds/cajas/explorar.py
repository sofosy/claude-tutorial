"""Exploración del DOM vivo de Cajas para la serie de videos (empresa demo 43).

Uso (desde claude-tutorial):
    .venv/Scripts/python.exe seeds/cajas/explorar.py v1 [v2 ...]      # un video o varios
    .venv/Scripts/python.exe seeds/cajas/explorar.py todo

Cada vista/diálogo queda en guiones/exploracion-cajas/<video>-<pantalla>.png + .json con:
títulos, botones visibles (texto, aria-label, selector propuesto y cuántos nodos casa en vivo),
mat-form-field (mat-label, formcontrolname), tablas (cabeceras + 2 filas), pestañas, tarjetas,
diálogos, toasts, caja (x,y,w,h) de cada cosa, si cabe en 1280x720 y si choca con .chatbot-fab.

Headless, 1280x720, device_scale_factor 1.5. Login real por la UI. Un solo navegador a la vez:
cerrojo seeds/_puertas/NAVEGADOR.lock (contenido «EXPLORANDO datos-cajas»).
Los estados posteriores a S0 se preparan por API (seeds/cajas/*.mjs) y al final se restaura S0.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import sync_playwright, Page

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parents[2]          # claude-tutorial
AQUI = Path(__file__).resolve().parent
SALIDA = RAIZ / "guiones" / "exploracion-cajas"
LOCK = RAIZ / "seeds" / "_puertas" / "NAVEGADOR.lock"
MARCA_LOCK = "EXPLORANDO datos-cajas"
BASE = "http://localhost:4200"
CLAVE = "Demo2026!"
FAB = (1200, 640, 56, 56)  # .chatbot-fab esperado (x, y, w, h)

JS_INFO = r"""
() => {
  const vis = (e) => {
    if (!e) return false;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    const s = getComputedStyle(e);
    if (s.visibility === 'hidden' || s.display === 'none' || +s.opacity === 0) return false;
    return true;
  };
  const box = (e) => { const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; };
  const txt = (e) => (e?.innerText || e?.textContent || '').replace(/\s+/g, ' ').trim();
  const q = (s, root = document) => [...root.querySelectorAll(s)].filter(vis);
  const esc = (s) => s.replace(/'/g, "\\'");
  // ámbito: el overlay más alto si hay diálogo/menú abierto
  const overlays = q('.cdk-overlay-pane');
  const scopeOf = (e) => {
    const d = e.closest('mat-dialog-container, .mat-mdc-dialog-container');
    if (d) { const c = [...(d.querySelector('[class]')?.classList || [])][0]; return d.closest('.cdk-overlay-pane') ? '.cdk-overlay-pane mat-dialog-container' : ''; }
    if (e.closest('.mat-mdc-menu-panel')) return '.mat-mdc-menu-panel';
    return '';
  };
  const icon = (e) => txt(e.querySelector('mat-icon'));
  const sinIcono = (e) => { const c = e.cloneNode(true); c.querySelectorAll('mat-icon').forEach(i => i.remove()); return txt(c); };
  const botones = q('button, a[mat-button], a[mat-raised-button], a[mat-flat-button], [role=menuitem], [role=tab]').map(b => {
    const t = sinIcono(b), aria = b.getAttribute('aria-label') || '', id = b.id || '';
    const cls = [...b.classList].filter(c => !/^(mat-|mdc-|cdk-|ng-)/.test(c)).slice(0, 3);
    const sc = scopeOf(b);
    let sel;
    if (id && !/^mat-|^cdk-/.test(id)) sel = `#${id}`;
    else if (aria) sel = `${sc ? sc + ' ' : ''}${b.tagName.toLowerCase()}[aria-label='${esc(aria)}']`;
    else if (t) sel = `${sc ? sc + ' ' : ''}${b.tagName.toLowerCase()}:has-text('${esc(t.slice(0, 40))}')`;
    else if (icon(b)) sel = `${sc ? sc + ' ' : ''}button:has(mat-icon:text-is('${icon(b)}'))`;
    return { texto: t, icono: icon(b), aria, id, clases: cls, tooltip: b.getAttribute('mattooltip') || b.getAttribute('ng-reflect-message') || '',
             deshabilitado: b.disabled || b.getAttribute('aria-disabled') === 'true', caja: box(b), sel };
  });
  const campos = q('mat-form-field').map(f => {
    const lab = txt(f.querySelector('mat-label, label'));
    const inp = f.querySelector('input, textarea, mat-select, select');
    const fcn = inp?.getAttribute('formcontrolname') || f.querySelector('[formcontrolname]')?.getAttribute('formcontrolname') || '';
    const hint = txt(f.querySelector('mat-hint')), err = txt(f.querySelector('mat-error'));
    let valor = '';
    if (inp?.tagName === 'MAT-SELECT') valor = txt(inp.querySelector('.mat-mdc-select-value'));
    else if (inp) valor = inp.value ?? '';
    return { label: lab, formcontrolname: fcn, tipo: inp?.tagName.toLowerCase() + (inp?.type ? ':' + inp.type : ''),
             placeholder: inp?.getAttribute('placeholder') || '', valor, hint, error: err,
             deshabilitado: !!(inp?.disabled || inp?.getAttribute('aria-disabled') === 'true'), caja: box(f),
             sel: fcn ? `[formcontrolname='${fcn}']` : (lab ? `mat-form-field:has(mat-label:text-is('${esc(lab)}'))` : '') };
  });
  const checks = q('mat-checkbox, mat-slide-toggle, mat-radio-button').map(c => ({
    texto: txt(c), formcontrolname: c.getAttribute('formcontrolname') || '',
    marcado: !!c.querySelector('input:checked') || c.classList.contains('mat-mdc-checkbox-checked'), caja: box(c) }));
  const tablas = q('table').map(t => ({
    clases: [...t.classList].slice(0, 3), cabeceras: [...t.querySelectorAll('thead th')].map(txt),
    filas: [...t.querySelectorAll('tbody tr')].slice(0, 2).map(r => [...r.querySelectorAll('td')].map(txt)),
    total_filas: t.querySelectorAll('tbody tr').length, caja: box(t) }));
  const pestañas = q('[role=tab], .segmented__option, .mat-mdc-tab').map(t => ({
    texto: txt(t), seleccionada: t.getAttribute('aria-selected') === 'true' || t.classList.contains('is-active') || t.classList.contains('segmented__option--active') || t.getAttribute('aria-pressed') === 'true', id: t.id || '', caja: box(t) }));
  const tarjetas = q('article.board-card').map(a => ({ aria: a.getAttribute('aria-label'), texto: txt(a).slice(0, 220), caja: box(a) }));
  const titulos = q('h1, h2, h3, h4, .page-hero-title, .page-hero-subtitle, .gm-state__t').map(h => ({ tag: h.tagName.toLowerCase(), clase: h.className?.toString().slice(0, 60), texto: txt(h).slice(0, 160), caja: box(h) }));
  const dialogos = q('mat-dialog-container, .mat-mdc-dialog-container').map(d => ({ titulo: txt(d.querySelector('h1,h2,h3')), clases: [...(d.closest('.cdk-overlay-pane')?.classList || [])].join(' '), caja: box(d), texto: txt(d).slice(0, 900) }));
  const menus = q('.mat-mdc-menu-panel').map(m => ({ items: q('[mat-menu-item], .mat-mdc-menu-item', m).map(i => ({ texto: sinIcono(i), icono: icon(i), caja: box(i) })), caja: box(m) }));
  const toasts = q('.mat-mdc-snack-bar-container').map(s => ({ texto: txt(s), caja: box(s) }));
  const alertas = q('.gm-dialog-alert, .gm-alert, .pcd-feedback, .foreign-session-banner, .board-card__note').map(a => ({ clase: a.className.toString().slice(0, 80), texto: txt(a).slice(0, 300), caja: box(a) }));
  const fabEl = document.querySelector('.chatbot-fab');
  let fab = fabEl && vis(fabEl) ? box(fabEl) : null;
  if (fab) { const top = document.elementFromPoint(fab[0] + fab[2] / 2, fab[1] + fab[3] / 2); if (!top || !top.closest('.chatbot-fab')) fab = null; }  // tapado por un overlay
  const choca = (c) => fab && c[0] < fab[0] + fab[2] && c[0] + c[2] > fab[0] && c[1] < fab[1] + fab[3] && c[1] + c[3] > fab[1];
  const chocan = [...botones.map(b => ({ que: 'boton', txt: b.texto || b.aria || b.icono, caja: b.caja })),
                  ...campos.map(c => ({ que: 'campo', txt: c.label, caja: c.caja }))].filter(x => choca(x.caja) && !/asistente|chat|Germi/i.test(x.txt));
  const fuera = [...botones.map(b => ({ que: 'boton', txt: b.texto || b.aria || b.icono, caja: b.caja })),
                 ...campos.map(c => ({ que: 'campo', txt: c.label, caja: c.caja }))].filter(x => x.caja[1] + x.caja[3] > innerHeight || x.caja[0] + x.caja[2] > innerWidth);
  const sc = document.scrollingElement;
  const scrollers = q('main, .main-content, .content, mat-sidenav-content, .page-body, .cashier-hub, .mat-mdc-dialog-content, .mat-mdc-tab-body-content').filter(e => e.scrollHeight > e.clientHeight + 4)
     .map(e => ({ el: e.tagName.toLowerCase() + '.' + [...e.classList].slice(0, 2).join('.'), scrollHeight: e.scrollHeight, clientHeight: e.clientHeight }));
  return { url: location.pathname + location.search, viewport: [innerWidth, innerHeight],
           documento: { scrollHeight: sc.scrollHeight, clientHeight: sc.clientHeight }, con_scroll: scrollers,
           titulos, botones, campos, casillas: checks, tablas, pestañas, tarjetas, dialogos, menus, toasts, avisos: alertas,
           chatbot_fab: fab, chocan_con_fab: chocan, fuera_de_1280x720: fuera };
}
"""


def lock_tomar():
    while True:
        try:
            fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, MARCA_LOCK.encode())
            os.close(fd)
            return
        except FileExistsError:
            try:
                dueño = LOCK.read_text(encoding="utf8", errors="replace").strip()
            except OSError:
                dueño = "?"
            print(f"  · NAVEGADOR.lock ocupado por «{dueño}»; espero 15 s…", flush=True)
            time.sleep(15)


def lock_soltar():
    try:
        if LOCK.read_text(encoding="utf8", errors="replace").strip() == MARCA_LOCK:
            LOCK.unlink()
    except FileNotFoundError:
        pass


def node(*args: str) -> str:
    r = subprocess.run(["node", *args], cwd=str(AQUI), capture_output=True, text=True, encoding="utf8")
    print("   ", (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "", flush=True)
    if r.returncode:
        raise SystemExit(f"node {' '.join(args)} falló:\n{r.stdout}\n{r.stderr}")
    return r.stdout


class Explorador:
    def __init__(self, pw):
        self.pw = pw
        self.browser = pw.chromium.launch(headless=True)
        self.page: Page | None = None
        self.ctx = None
        self.video = "v0"
        self.toasts: list[str] = []

    # ── sesión ────────────────────────────────────────────────────────────
    def entrar(self, usuario: str):
        if self.ctx:
            self.ctx.close()
        self.ctx = self.browser.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5,
                                            locale="es-DO", timezone_id="America/Santo_Domingo")
        self.page = p = self.ctx.new_page()
        p.set_default_timeout(15000)
        # todo toast que aparezca queda registrado con su texto exacto
        p.expose_function("__toast", lambda t: self.toasts.append(t.removesuffix(" Cerrar")))
        p.add_init_script("""
          new MutationObserver(() => {
            document.querySelectorAll('.mat-mdc-snack-bar-container:not([data-visto])').forEach(s => {
              s.setAttribute('data-visto', '1');
              setTimeout(() => window.__toast && window.__toast((s.innerText||'').replace(/\\s+/g,' ').trim()), 150);
            });
          }).observe(document, {childList: true, subtree: true});
        """)
        p.goto(BASE + "/authentication/signin", wait_until="networkidle")
        p.fill("input[formcontrolname='username']", usuario)
        p.fill("input[formcontrolname='password']", CLAVE)
        p.click("button.auth-primary-btn")
        p.wait_for_url(lambda u: "signin" not in u, timeout=30000)
        p.wait_for_timeout(2500)
        modales = self.info()["dialogos"]
        if modales:
            print(f"  ! {usuario}: modal al entrar → {[m['titulo'] for m in modales]}")
            self.cap("login", f"modal-al-entrar-{usuario}")
        for sel in ("button.close-btn", "button:has-text('Recordar más tarde')"):
            try:
                if p.locator(sel).first.is_visible():
                    p.locator(sel).first.click()
                    p.wait_for_timeout(500)
            except Exception:
                pass
        print(f"  · sesión UI: {usuario} → {p.url}")

    def ir(self, ruta: str, esperar: str | None = None):
        self.page.goto(BASE + ruta, wait_until="networkidle")
        if esperar:
            self.page.wait_for_selector(esperar, state="visible")
        self.page.wait_for_timeout(1200)

    def info(self) -> dict:
        return self.page.evaluate(JS_INFO)

    # ── captura ──────────────────────────────────────────────────────────
    def cap(self, video_o_pantalla: str, pantalla: str | None = None, notas: str = "", extra: dict | None = None) -> dict:
        if pantalla is None:
            video, pantalla = self.video, video_o_pantalla
        else:
            video = video_o_pantalla
        p = self.page
        p.wait_for_timeout(400)
        d = self.info()
        # verificación en vivo de cada selector propuesto (cuántos nodos VISIBLES casa)
        for grupo in ("botones", "campos"):
            for it in d[grupo]:
                sel = it.get("sel")
                if not sel:
                    continue
                try:
                    loc = p.locator(sel)
                    n = loc.count()
                    vis = sum(1 for i in range(min(n, 6)) if loc.nth(i).is_visible())
                    it["sel_casa"] = f"{vis} visible(s) de {n}"
                except Exception as e:
                    it["sel_casa"] = f"ERROR {str(e).splitlines()[0][:80]}"
        d["video"], d["pantalla"], d["notas"] = video, pantalla, notas
        d["toasts_vistos_hasta_ahora"] = list(self.toasts)
        if extra:
            d["extra"] = extra
        base = SALIDA / f"{video}-{pantalla}"
        p.screenshot(path=str(base.with_suffix(".png")))
        base.with_suffix(".json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
        aviso = ""
        if d["chocan_con_fab"]:
            aviso += f" CHOCA-FAB:{[x['txt'] for x in d['chocan_con_fab']]}"
        if d["fuera_de_1280x720"]:
            aviso += f" FUERA:{[x['txt'] for x in d['fuera_de_1280x720']][:6]}"
        print(f"  ✓ {video}-{pantalla}{aviso}", flush=True)
        return d

    def clic(self, sel: str, espera_ms: int = 900):
        self.page.locator(sel).first.click()
        self.page.wait_for_timeout(espera_ms)

    def esperar_toast(self, n_antes: int, ms: int = 8000) -> str:
        fin = time.time() + ms / 1000
        while time.time() < fin:
            if len(self.toasts) > n_antes:
                return self.toasts[-1]
            self.page.wait_for_timeout(150)
        return ""

    def cancelar_dialogo(self):
        p = self.page
        for sel in ("mat-dialog-container button:has-text('Cancelar')", "mat-dialog-container button:has-text('Cerrar')",
                    "button.cashier-sheet-close"):
            loc = p.locator(sel)
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                p.wait_for_timeout(700)
                # «¿descartar cambios?»
                conf = p.locator(".custom-alert-dialog-style button.confirm-button")
                if conf.count() and conf.first.is_visible():
                    self.cap(f"confirmar-descartar-{int(time.time()) % 1000}", notas="aviso al cancelar con datos")
                    conf.first.click()
                    p.wait_for_timeout(600)
                return
        p.keyboard.press("Escape")
        p.wait_for_timeout(600)

    def cerrar(self):
        if self.ctx:
            self.ctx.close()
        self.browser.close()


# ── escenarios por video ────────────────────────────────────────────────────
from escenarios_cajas import ESCENARIOS  # noqa: E402  (mismo directorio)


def main(argv):
    pedidos = [a for a in argv if not a.startswith("--")] or ["todo"]
    if pedidos == ["todo"]:
        pedidos = list(ESCENARIOS)
    SALIDA.mkdir(parents=True, exist_ok=True)
    lock_tomar()
    try:
        with sync_playwright() as pw:
            ex = Explorador(pw)
            try:
                for v in pedidos:
                    print(f"── {v}", flush=True)
                    ex.video = v
                    ESCENARIOS[v](ex)
            finally:
                ex.cerrar()
    finally:
        lock_soltar()
        if "--sin-restaurar" not in argv:
            node("restaurar.mjs", "S0")


if __name__ == "__main__":
    sys.path.insert(0, str(AQUI))
    main(sys.argv[1:])
