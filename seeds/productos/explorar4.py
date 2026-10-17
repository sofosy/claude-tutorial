import sys, time
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ)); sys.path.insert(0, str(RAIZ / "seeds" / "_puertas"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
from tutorial.capturar import _sesion
from ensayar import cargar
nombre, guion = cargar("productos"); base = guion["base_url"].rstrip("/")
OUT = RAIZ / "salida" / "productos" / "explorar"
with sync_playwright() as p:
    nav = p.chromium.launch(headless=True)
    pag = nav.new_context(viewport={"width": 1280, "height": 720}).new_page()
    _sesion(pag, guion, {}, base); time.sleep(2)
    pag.goto(base + "/inventory/existencias"); pag.wait_for_timeout(3500)
    inp = pag.locator("mat-form-field:has(mat-label:text-is('Buscar')) input")
    print("inputs Buscar:", inp.count(), inp.first.get_attribute("placeholder"))
    inp.first.click(); pag.keyboard.type("Camiseta", delay=45); pag.wait_for_timeout(1500)
    print("sin filtrar:", pag.locator("tbody tr:has-text('Camiseta')").count())
    pag.locator("button[aria-label='Aplicar filtros']").click(); pag.wait_for_timeout(2500)
    f = pag.locator("tbody tr:has-text('Camiseta')")
    print("con filtrar:", f.count(), "| total filas:", pag.locator("tbody tr").count())
    if f.count():
        print("fila:", f.first.inner_text().replace("\n"," | "))
        print("tds:", [t.inner_text()[:25] for t in f.first.locator("td").all()])
        f.first.locator("button").first.click(); pag.wait_for_timeout(3000)
        print("URL:", pag.url)
        print("DETALLE:\n", pag.locator("app-root").inner_text()[-2500:])
        pag.screenshot(path=str(OUT / "x14-detalle.png"))
        print("tabs:", pag.locator("[role=tab], a:has-text('Movimientos')").all_inner_texts())
    nav.close()
