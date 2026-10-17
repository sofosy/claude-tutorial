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
D = "mat-dialog-container"
def invalidos(pag):
    return pag.evaluate("""() => [...document.querySelectorAll('mat-dialog-container [formcontrolname]')].map(e => e.getAttribute('formcontrolname') + '=' + (e.classList.contains('ng-invalid') ? 'INVALIDO' : 'ok') + ' «' + (e.value ?? e.innerText ?? '').toString().slice(0,40) + '»')""")
with sync_playwright() as p:
    nav = p.chromium.launch(headless=True)
    pag = nav.new_context(viewport={"width": 1280, "height": 720}).new_page()
    _sesion(pag, guion, {}, base); time.sleep(2)
    pag.locator("tr:has-text('Camiseta Germiva') button").first.click(); pag.wait_for_timeout(3500)
    pag.locator("button:has-text('Registrar Entrada')").click(); pag.wait_for_timeout(2000)
    print(pag.locator(D).inner_text()[:1500])
    pag.locator(D + " mat-select[formcontrolname='productVariantId']").click(); pag.wait_for_timeout(800)
    print("OPCIONES variante:", pag.locator("mat-option").all_inner_texts())
    pag.locator("mat-option:has-text('M + Corta')").click(); pag.wait_for_timeout(1200)
    print("tras variante:", invalidos(pag))
    pag.locator(D + " mat-select[formcontrolname='inventoryMovementTypeId']").click(); pag.wait_for_timeout(800)
    pag.locator("mat-option:has-text('Compras de mercancía')").click(); pag.wait_for_timeout(800)
    pag.locator(D + " [formcontrolname='partnerId'] input").click(); pag.keyboard.type("Textiles", delay=45); pag.wait_for_timeout(2500)
    print("OPCIONES proveedor:", pag.locator("mat-option").all_inner_texts()[:5])
    pag.keyboard.press("ArrowDown"); pag.keyboard.press("Enter"); pag.wait_for_timeout(800)
    pag.locator(D + " [formcontrolname='locationId'] input").click(); pag.wait_for_timeout(2500)
    print("OPCIONES ubicacion:", pag.locator("mat-option").all_inner_texts()[:5])
    pag.keyboard.press("ArrowDown"); pag.keyboard.press("Enter"); pag.wait_for_timeout(800)
    pag.locator(D + " button:has(mat-icon:text('auto_awesome'))").click(); pag.wait_for_timeout(800)
    pag.locator(D + " [formcontrolname='quantity']").click(); pag.keyboard.press("Control+A"); pag.keyboard.type("20")
    pag.locator(D + " [formcontrolname='unitPrice']").click(); pag.keyboard.press("Control+A"); pag.keyboard.type("400"); pag.wait_for_timeout(800)
    print("final:", invalidos(pag))
    print("boton habilitado:", pag.locator(D + " button:has-text('Registrar entrada')").is_enabled())
    pag.locator(D).evaluate("e => e.querySelector('.mat-mdc-dialog-content, mat-dialog-content')?.scrollTo(0,0)")
    pag.screenshot(path=str(OUT / "x12-top.png"))
    nav.close()
