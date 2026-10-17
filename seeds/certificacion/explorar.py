# python seeds/certificacion/explorar.py <tag> <ruta|!ruta-publica> [pasos...]
# Pasos: click:<sel> fill:<sel>=<t> type:<sel>=<t> press:<k> wait:<ms> goto:<ruta> shot:<n> text:<sel> eval:<js> upload:<sel>=<file>
import sys, time, json, urllib.request
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
BASE = "http://localhost:4200"
OUT = RAIZ / "salida" / "certificacion-explorar"; OUT.mkdir(parents=True, exist_ok=True)
tag, ruta, *pasos = sys.argv[1:]
publico = ruta.startswith("!")
with sync_playwright() as p:
    nav = p.chromium.launch(headless=True)
    ctx = nav.new_context(viewport={"width": 1280, "height": 720})
    pag = ctx.new_page()
    errores = []
    pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pag.on("response", lambda r: errores.append(f"HTTP {r.status} {r.request.method} {r.url}") if r.status >= 400 and "/api/" in r.url else None)
    if not publico:
        rq = urllib.request.Request("http://localhost:3001/api/auth/dev/login", data=json.dumps({"username": "admin", "password": "admin"}).encode(), headers={"Content-Type": "application/json"}); r = json.load(urllib.request.urlopen(rq))
        pag.goto(BASE + "/authentication/signin"); pag.wait_for_timeout(1500)
        pag.evaluate("d => { localStorage.setItem('aut', JSON.stringify(d)); }", {**r, "__v": 2})
    pag.goto(BASE + ruta.lstrip("!")); pag.wait_for_timeout(3500)
    def shot(nm): pag.screenshot(path=str(OUT / f"{tag}-{nm}.png"))
    for paso in pasos:
        k, _, v = paso.partition(":")
        try:
            if k == "click": pag.locator(v).first.click(timeout=8000); pag.wait_for_timeout(1200)
            elif k == "fill":
                s, _, t = v.rpartition("="); pag.locator(s).first.fill(t); pag.wait_for_timeout(600)
            elif k == "type":
                s, _, t = v.rpartition("="); pag.locator(s).first.click(); pag.keyboard.type(t, delay=20); pag.wait_for_timeout(1000)
            elif k == "upload":
                s, _, t = v.rpartition("="); pag.locator(s).first.set_input_files(t); pag.wait_for_timeout(1000)
            elif k == "wait": pag.wait_for_timeout(int(v))
            elif k == "goto": pag.goto(BASE + v); pag.wait_for_timeout(3500)
            elif k == "shot": shot(v)
            elif k == "full": pag.screenshot(path=str(OUT / f"{tag}-{v}.png"), full_page=True)
            elif k == "text": print(f"--- text {v}\n", pag.locator(v).first.inner_text()[:5000])
            elif k == "eval": print("--- eval:", json.dumps(pag.evaluate(v), ensure_ascii=False)[:6000])
            elif k == "press": pag.keyboard.press(v); pag.wait_for_timeout(700)
        except Exception as e:
            print(f"!! {paso}: {str(e)[:300]}")
    shot("fin")
    print("URL:", pag.url)
    if errores: print("--- ERRORES:\n", "\n".join(dict.fromkeys(errores))[:3000])
    nav.close()
