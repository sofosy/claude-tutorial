"""Exploración 3 del video 8: el camino del guion con la factura en BORRADOR (S8).
Mi caja → riel Ventas → Facturas → lápiz «Editar» → pago combinado → «Guardar y Cobrar» → factura pagada
→ Pagos → Mi caja → Cuadre → Volver.
Bajo cerrojo: node seeds/cajas/con-cerrojo.mjs "EXPLORANDO cajas-08" -- .venv/Scripts/python.exe seeds/cajas/explorar_v8c.py
Restaura S8 antes y después y deja el plan en 2.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import explorar as ex  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PANEL = ".inline-payment-panel"


def main():
    ex.node("restaurar.mjs", "S8")
    with sync_playwright() as pw:
        e = ex.Explorador(pw)
        e.video = "v8"
        errores = []
        try:
            e.entrar("admin.progreso")
            p = e.page
            p.on("response", lambda r: errores.append(f"{r.status} {r.request.method} {r.url}") if r.status >= 400 else None)
            e.ir("/cashier?section=caja", ".session-bar")
            e.cap("30-mi-caja-antes")
            p.locator(".module-rail button[aria-label='Ventas']").click(); p.wait_for_timeout(1000)
            p.locator("a[href='/sales/invoices']").first.click(); p.wait_for_timeout(3000)
            e.cap("31-lista-borrador", extra={"acciones_fila": p.locator("table tbody tr").first.locator("button").evaluate_all("bs => bs.map(b => [b.getAttribute('aria-label'), b.innerText.trim(), JSON.stringify(b.getBoundingClientRect())])")})
            p.locator("table tbody tr").filter(has_text="Constructora").first.locator("button[aria-label='Editar']").click()
            p.wait_for_timeout(4000)
            e.cap("32-factura-borrador", extra={"url": p.url, "collapse": p.locator("button.panel-collapse").count(),
                                               "footer": p.locator("button:has-text('Cobrar')").all_inner_texts()})
            p.locator(".gm-doc-payment").scroll_into_view_if_needed(); p.wait_for_timeout(800)
            e.cap("33-cobro-borrador")
            p.locator("mat-checkbox.ipp-split-toggle").click(); p.wait_for_timeout(600)
            a = p.locator(f"{PANEL} input[formcontrolname='amount']")
            a.click(); p.keyboard.press("Control+A"); p.keyboard.type("5000", delay=45); p.wait_for_timeout(500)
            e.cap("34-efectivo-tecleado")
            p.locator(f"{PANEL} button.ipp-exact-btn").click(); p.wait_for_timeout(500)
            e.cap("35-exacto")
            p.locator("button.ipp-add-tender__btn").click(); p.wait_for_timeout(800)
            p.locator(".gm-doc-seg__opt:has-text('Tarjeta')").click(); p.wait_for_timeout(600)
            c = p.locator(f"{PANEL} input[formcontrolname='cardNumber']")
            c.click(); p.keyboard.type("4821", delay=45)
            p.locator(f"{PANEL} mat-select[formcontrolname='cardType']").click(); p.wait_for_timeout(500)
            p.locator("mat-option:has-text('Visa')").click(); p.wait_for_timeout(300)
            z = p.locator(f"{PANEL} input[formcontrolname='authorizationCode']")
            z.click(); p.keyboard.type("738214", delay=45); p.wait_for_timeout(400)
            e.cap("36-tarjeta")
            p.locator("button.ipp-add-tender__btn").click(); p.wait_for_timeout(800)
            e.cap("37-recibo-completo", extra={"outcome": p.locator(".ipp-outcome").inner_text(),
                                              "footer": [b for b in p.locator("button").all_inner_texts() if 'obrar' in b]})
            n = len(e.toasts)
            p.locator("button:has-text('Guardar y Cobrar')").last.click()
            import time
            t0 = time.time()
            for _ in range(30):
                p.wait_for_timeout(300)
                if e.info()["dialogos"] or len(e.toasts) > n:
                    break
            e.cap("38-tras-guardar-y-cobrar", extra={"segundos": round(time.time() - t0, 1), "toasts": e.toasts[n:]})
            p.wait_for_timeout(2000)
            e.cap("39-tras-2s", extra={"toasts": e.toasts[n:]})
            for sel in ("mat-dialog-container button:has-text('Aceptar')", ".custom-alert-dialog-style button.confirm-button"):
                if p.locator(sel).count():
                    p.locator(sel).first.click(); p.wait_for_timeout(2500)
                    break
            e.cap("40-factura-pagada", extra={"url": p.url, "toasts": e.toasts[n:],
                                             "cabecera": p.locator("h1, .gm-doc-head, .page-hero").first.inner_text()[:400] if p.locator("h1").count() else ""})
            p.evaluate("() => window.scrollTo(0,0)"); p.wait_for_timeout(500)
            e.cap("41-factura-pagada-arriba")
            p.locator("button:has-text('Versiones e historial')").click(); p.wait_for_timeout(1000)
            p.locator(".mat-mdc-tab:has-text('Pagos')").first.click(); p.wait_for_timeout(1500)
            p.locator(".mat-mdc-tab-body-active table").first.scroll_into_view_if_needed(); p.wait_for_timeout(500)
            e.cap("42-pagos")
            p.locator(".module-rail a[href='/cashier']").click(); p.wait_for_timeout(3000)
            e.cap("43-riel-cajas", extra={"url": p.url})
            e.ir("/cashier?section=caja", ".session-bar")
            e.cap("44-mi-caja-despues")
            p.locator("button.quick-action--reconcile").click(); p.wait_for_timeout(3500)
            e.cap("45-cuadre")
            p.locator(".detail-row:has-text('Tarjeta')").first.scroll_into_view_if_needed(); p.wait_for_timeout(500)
            e.cap("46-cuadre-tarjeta")
        finally:
            print("errores http:", errores[:20])
            e.browser.close()
            ex.node("restaurar.mjs", "S8")
            ex.node("plan-s8.mjs", "off")


if __name__ == "__main__":
    main()
