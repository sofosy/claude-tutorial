"""Volcado del texto real de las vistas del tutorial de Productos (solo lectura salvo lo indicado)."""
import sys, time, json
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ)); sys.path.insert(0, str(RAIZ / "seeds" / "_puertas"))
for _f in (sys.stdout,):
    _f.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
from tutorial import grabar as g
from tutorial.capturar import _sesion
from ensayar import cargar

nombre, guion = cargar("productos")
base = guion["base_url"].rstrip("/")
OUT = RAIZ / "salida" / "productos" / "explorar"; OUT.mkdir(parents=True, exist_ok=True)

def txt(pag, sel="body"):
    try:
        return pag.locator(sel).first.inner_text(timeout=4000)
    except Exception as e:
        return f"<<{sel}: {e}>>"

def dump(pag, titulo, sel="body"):
    print(f"\n######## {titulo}\n{txt(pag, sel)[:4000]}")
    pag.screenshot(path=str(OUT / (titulo.replace(' ', '_').replace('/', '-') + ".png")))

with sync_playwright() as p:
    nav = p.chromium.launch(headless=True)
    ctx = nav.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
    pag = ctx.new_page()
    _sesion(pag, guion, {}, base)
    time.sleep(2)
    pid = pag.evaluate("""async () => { const r = await fetch('/api/x'); return 1 }""") if False else None
    # 1 · listado + importar
    pag.goto(base + "/inventory/product/list"); pag.wait_for_timeout(3000)
    dump(pag, "01 listado", "main")
    pag.locator("button:has-text('Importar / Exportar')").click(); pag.wait_for_timeout(1500)
    dump(pag, "02 importar", "mat-dialog-container")
    pag.locator("mat-dialog-container .mdc-tab:has-text('Exportar')").click(); pag.wait_for_timeout(1000)
    dump(pag, "02b exportar", "mat-dialog-container")
    pag.locator("mat-dialog-container button:has-text('Cerrar')").click(); pag.wait_for_timeout(800)
    # acciones de la fila: aria-labels
    fila = pag.locator("tr:has-text('Camiseta Germiva')").first
    print("\n######## 15 botones fila:", [ (b.get_attribute('aria-label'), b.get_attribute('mattooltip'), b.inner_text()) for b in fila.locator('button').all()])
    fila.locator("button").nth(1).click(); pag.wait_for_timeout(1200)
    dump(pag, "15 duplicar", "mat-dialog-container")
    pag.locator("mat-dialog-container button:has-text('Cancelar')").click(); pag.wait_for_timeout(600)
    fila.locator("button").nth(2).click(); pag.wait_for_timeout(1200)
    dump(pag, "15 desactivar", "mat-dialog-container")
    pag.keyboard.press("Escape"); pag.wait_for_timeout(600)
    fila.locator("button").nth(3).click(); pag.wait_for_timeout(1200)
    dump(pag, "15 eliminar", "mat-dialog-container")
    pag.keyboard.press("Escape"); pag.wait_for_timeout(600)
    # 3 · nuevo producto
    pag.locator("button:has-text('Nuevo Producto')").click(); pag.wait_for_timeout(2500)
    dump(pag, "03 nuevo", "main")
    pag.locator("[formcontrolname='name']").fill("Camiseta"); pag.wait_for_timeout(2000)
    dump(pag, "03b sugerencias", ".name-suggestions-panel")
    pag.keyboard.press("Escape")
    pag.locator("[formcontrolname='name']").fill(""); 
    pag.locator("app-custom-select[formcontrolname='productType'] input").fill("Camisetas"); pag.wait_for_timeout(1500)
    dump(pag, "04 categoria opciones", ".cdk-overlay-container")
    pag.keyboard.press("Escape")
    pag.locator("app-custom-select[formcontrolname='unitMeasure'] input").fill("Unidad"); pag.wait_for_timeout(1500)
    dump(pag, "04 unidad opciones", ".cdk-overlay-container")
    pag.keyboard.press("Escape")
    # 6 · ficha existente
    pag.goto(base + "/inventory/product/list"); pag.wait_for_timeout(2500)
    pag.locator("tr:has-text('Camiseta Germiva') button").first.click(); pag.wait_for_timeout(3500)
    dump(pag, "06 ficha", "main")
    for tab in ["Variantes", "Fiscal", "Configuración", "Insumos", "Historial"]:
        pag.locator(f"mat-tab-group.product-tabs .mdc-tab:has-text('{tab}')").click(); pag.wait_for_timeout(1500)
        dump(pag, f"tab {tab}", "mat-tab-group.product-tabs .mat-mdc-tab-body-active")
    pag.locator("mat-tab-group.product-tabs .mdc-tab:has-text('Variantes')").click(); pag.wait_for_timeout(1000)
    pag.locator("button:has-text('Generar todas')").click(); pag.wait_for_timeout(1500)
    hdr = pag.locator(".variants-table thead mat-checkbox").first
    hdr.click(); pag.wait_for_timeout(1000)
    dump(pag, "08 lote", "mat-tab-group.product-tabs .mat-mdc-tab-body-active")
    print("\n######## 08 botones lote:", [b.inner_text() for b in pag.locator(".variants button").all()][:30])
    try:
        pag.locator("button:has-text('Aplicar precio')").first.click(); pag.wait_for_timeout(1200)
        dump(pag, "08 aplicar precio", ".cdk-overlay-container")
        print("inputs overlay:", pag.locator(".cdk-overlay-container input").count(), "| inputs lote:", [ (i.get_attribute('placeholder'), i.get_attribute('class')) for i in pag.locator(".variants input").all()][:12])
    except Exception as e:
        print("aplicar precio:", e)
    # entrada
    pag.goto(base + "/inventory/product/list"); pag.wait_for_timeout(2500)
    try:
        pag.on("dialog", lambda d: d.accept())
    except Exception: pass
    pag.locator("tr:has-text('Camiseta Germiva') button").first.click(); pag.wait_for_timeout(3500)
    pag.locator("button:has-text('Registrar Entrada')").click(); pag.wait_for_timeout(2000)
    dump(pag, "12 entrada", "mat-dialog-container")
    pag.keyboard.press("Escape"); pag.wait_for_timeout(800)
    # existencias
    pag.goto(base + "/inventory/existencias"); pag.wait_for_timeout(3000)
    dump(pag, "14 existencias", "main")
    pag.locator("input[placeholder^='Buscar por código']").fill("Camiseta"); pag.wait_for_timeout(2500)
    dump(pag, "14b busqueda", "main")
    pag.keyboard.press("Enter"); pag.wait_for_timeout(2500)
    dump(pag, "14c enter", "main")
    print("\n######## 14 filas:", pag.locator("tbody tr").count(), "| con camiseta:", pag.locator("tbody tr:has-text('Camiseta')").count())
    # mantenimiento
    pag.goto(base + "/inventory/product/price-maintenance"); pag.wait_for_timeout(3000)
    dump(pag, "16 mantenimiento", "main")
    nav.close()
