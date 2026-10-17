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
def html(loc, n=3000):
    try: return loc.first.evaluate("e => e.outerHTML")[:n]
    except Exception as e: return f"<<{e}>>"
with sync_playwright() as p:
    nav = p.chromium.launch(headless=True)
    pag = nav.new_context(viewport={"width": 1280, "height": 720}).new_page()
    _sesion(pag, guion, {}, base); time.sleep(2)
    pag.goto(base + "/inventory/existencias"); pag.wait_for_timeout(3500)
    print("#### existencias body:\n", pag.locator("app-root").inner_text()[:2500])
    pag.locator("input[placeholder^='Buscar por código']").fill("Camiseta"); pag.wait_for_timeout(3000)
    fila = pag.locator("tbody tr:has-text('Camiseta')")
    print("#### fila:", fila.count(), "\n", fila.first.inner_text() if fila.count() else "")
    print("#### botones fila:", [(b.get_attribute('aria-label'), b.get_attribute('mattooltip'), b.inner_text()) for b in fila.first.locator('button').all()] if fila.count() else None)
    print("#### thead:", pag.locator("thead").first.inner_text().replace("\n"," | "))
    pag.screenshot(path=str(OUT / "x14-busqueda.png"))
    if fila.count():
        fila.first.locator("button").first.click(); pag.wait_for_timeout(2500)
        print("#### detalle:\n", pag.locator("app-root").inner_text()[:3000])
        pag.screenshot(path=str(OUT / "x14-detalle.png"))
    # variantes: barra de lote
    pag.goto(base + "/inventory/product/list"); pag.wait_for_timeout(2500)
    pag.locator("tr:has-text('Camiseta Germiva') button").first.click(); pag.wait_for_timeout(3500)
    pag.locator("mat-tab-group.product-tabs .mdc-tab:has-text('Variantes')").click(); pag.wait_for_timeout(1200)
    pag.locator("button:has-text('Generar todas')").click(); pag.wait_for_timeout(1500)
    pag.locator(".variants-table thead mat-checkbox").first.click(); pag.wait_for_timeout(1000)
    bar = pag.locator(":has(> button:has-text('Aplicar precio'))")
    print("#### barra lote:\n", html(bar, 2500))
    pag.screenshot(path=str(OUT / "x08-lote.png"))
    nav.close()
