# python seeds/citas/explorar.py <nombre> <ruta> [js-acciones...]
# Abre la ruta con la sesión de la clínica a 1280x720, ejecuta pasos y guarda captura + texto.
# Pasos: "click:<selector>", "fill:<selector>=<texto>", "wait:<ms>", "goto:<ruta>", "shot:<nombre>", "text:<selector>", "eval:<js>"
import sys, time, json
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ)); sys.path.insert(0, str(RAIZ / "seeds" / "_puertas"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
from tutorial.capturar import _sesion, _rutas_locales
from ensayar import cargar
import os; nombre, guion = cargar(os.environ.get("GUION", "clinica")); base = guion["base_url"].rstrip("/")
OUT = RAIZ / "salida" / "clinica" / "explorar"; OUT.mkdir(parents=True, exist_ok=True)
tag, ruta, *pasos = sys.argv[1:]
UI_JS = """() => { const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; };
 const out = [];
 document.querySelectorAll('button, a[href], [role=tab], mat-slide-toggle, mat-checkbox, mat-form-field, [role=menuitem], mat-option').forEach(e => { if (!vis(e)) return;
   const t = (e.innerText || e.getAttribute('aria-label') || '').replace(/\\s+/g, ' ').trim().slice(0, 70);
   const fc = e.querySelector && (e.querySelector('[formcontrolname]')?.getAttribute('formcontrolname') || '');
   out.push(e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ').filter(c => c && !c.startsWith('mat-mdc') && !c.startsWith('mdc') && !c.startsWith('ng-') && !c.startsWith('cdk')).slice(0, 3).join('.') : '') + (fc ? ' [fc=' + fc + ']' : '') + ' | ' + t); });
 return out; }"""
publico = ruta.startswith("!")
with sync_playwright() as p:
    nav = p.chromium.launch(headless=True)
    ctx = nav.new_context(viewport={"width": 1280, "height": 720}); _rutas_locales(ctx, guion)
    pag = ctx.new_page()
    errores = []
    pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pag.on("response", lambda r: errores.append(f"HTTP {r.status} {r.request.method} {r.url}") if r.status >= 400 and "/api/" in r.url else None)
    if not publico:
        _sesion(pag, guion, {}, base); time.sleep(1.5)
    pag.goto(base + ruta.lstrip("!")); pag.wait_for_timeout(3500)
    n = 0
    def shot(nm):
        pag.screenshot(path=str(OUT / f"{tag}-{nm}.png"))
    for paso in pasos:
        k, _, v = paso.partition(":")
        try:
            if k == "click": pag.locator(v).first.click(timeout=8000); pag.wait_for_timeout(1500)
            elif k == "fill":
                s, _, t = v.rpartition("="); pag.locator(s).first.fill(t); pag.wait_for_timeout(800)
            elif k == "type":
                s, _, t = v.rpartition("="); pag.locator(s).first.click(); pag.keyboard.type(t, delay=30); pag.wait_for_timeout(1200)
            elif k == "wait": pag.wait_for_timeout(int(v))
            elif k == "goto": pag.goto(base + v); pag.wait_for_timeout(3500)
            elif k == "shot": shot(v)
            elif k == "text": print(f"--- text {v}\n", pag.locator(v).first.inner_text()[:4000])
            elif k == "eval": print("--- eval:", json.dumps(pag.evaluate(v), ensure_ascii=False)[:5000])
            elif k == "ui":
                print("--- ui:", json.dumps(pag.evaluate(UI_JS), ensure_ascii=False)[:8000])
            elif k == "tclick": pag.locator(v).first.click(click_count=3, timeout=8000); pag.wait_for_timeout(600)
            elif k == "sign":
                b = pag.locator(v).first.bounding_box(); import math
                pag.mouse.move(b["x"]+30, b["y"]+b["height"]/2); pag.mouse.down()
                for i in range(40): pag.mouse.move(b["x"]+30+i*(b["width"]-60)/40, b["y"]+b["height"]/2+18*math.sin(i/3))
                pag.mouse.up(); pag.wait_for_timeout(500)
            elif k == "kb": pag.keyboard.type(v, delay=15); pag.wait_for_timeout(400)
            elif k == "press": pag.keyboard.press(v); pag.wait_for_timeout(800)
        except Exception as e:
            print(f"!! {paso}: {str(e)[:300]}")
    shot("fin")
    print("URL:", pag.url)
    print("--- TEXTO:\n", pag.locator("body").inner_text()[:6000])
    if errores: print("--- ERRORES:\n", "\n".join(dict.fromkeys(errores))[:3000])
    nav.close()
