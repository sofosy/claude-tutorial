"""Exploración del video 8 «Cobrar una factura en la caja: pago combinado» (autor video 8, 2026-09-23).

Uso (desde claude-tutorial, BAJO CERROJO):
    node seeds/cajas/con-cerrojo.mjs "EXPLORANDO cajas-08" -- .venv/Scripts/python.exe seeds/cajas/explorar_v8.py [fase]
Restaura S8 antes y después. Salida: guiones/exploracion-cajas/v8-*.png/.json
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import explorar as ex  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402


USUARIO = "admin.progreso"


def main(fase: str):
    ex.node("restaurar.mjs", "S8")
    ex.node("plan-s8.mjs", "ver")
    with sync_playwright() as pw:
        e = ex.Explorador(pw)
        e.video = "v8"
        errores = []
        try:
            e.entrar(USUARIO)
            p = e.page
            p.on("response", lambda r: errores.append(f"{r.status} {r.request.method} {r.url}") if r.status >= 400 else None)
            e.ir("/cashier?section=caja", ".session-bar")
            e.cap("01-mi-caja-antes")
            # riel: ¿la cajera tiene Ventas?
            e.cap("02-riel", extra={"riel": p.evaluate("() => [...document.querySelectorAll('a[href]')].map(a => [a.getAttribute('href'), (a.getAttribute('aria-label')||a.innerText||'').trim().slice(0,40)]).filter(x => x[0].startsWith('/'))")})
            p.locator(".module-rail button[aria-label='Ventas']").click()
            p.wait_for_timeout(1200)
            e.cap("02c-panel-ventas", extra={"items": p.evaluate("() => [...document.querySelectorAll('a[href*=sales]')].filter(a => a.getBoundingClientRect().width > 0).map(a => [a.getAttribute('href'), (a.innerText||'').trim(), [a.getBoundingClientRect().x, a.getBoundingClientRect().y]])")})
            p.locator("a[href='/sales/invoices']").first.click()
            p.wait_for_timeout(3000)
            e.cap("03-facturas-lista", extra={"fila_html": p.locator("table tbody tr").first.inner_html()[:3000]})
            if fase == "lista":
                return
            # el riel: ¿dónde está Ventas?
            e.cap("02b-riel-admin", extra={"rail": p.evaluate("() => [...document.querySelectorAll('.module-rail a, .module-rail button, nav a')].map(a => [a.tagName, a.getAttribute('href'), a.getAttribute('aria-label'), a.getAttribute('mattooltip'), (a.innerText||'').trim().slice(0,30), JSON.stringify([...a.getBoundingClientRect().toJSON ? [a.getBoundingClientRect().x,a.getBoundingClientRect().y] : []])])")})
            fila = p.locator("table tbody tr").filter(has_text="Constructora").first
            fila.locator("button:has(mat-icon:text-is('more_vert'))").click()
            p.wait_for_timeout(800)
            e.cap("03m-menu-fila")
            p.keyboard.press("Escape"); p.wait_for_timeout(400)
            fila.locator("td").nth(0).click()
            p.wait_for_timeout(3500)
            e.cap("04-factura-abierta", extra={"url": p.url})
            if "/1000000001" not in p.url:
                e.ir("/sales/invoices/1000000001")
                p.wait_for_timeout(3500)
                e.cap("04b-factura-ruta-directa", extra={"url": p.url})
            sec = p.locator(".gm-doc-payment")
            sec.scroll_into_view_if_needed()
            p.wait_for_timeout(800)
            e.cap("05-seccion-cobro", extra={"url": p.url})
            if fase == "factura":
                return
            p.locator("mat-checkbox.ipp-split-toggle").click()
            p.wait_for_timeout(800)
            e.cap("06-combinado-activado")
            p.locator(".gm-doc-seg__opt:has-text('Efectivo')").click()
            p.locator(".inline-payment-panel input[formcontrolname='amount']").fill("5000")
            p.wait_for_timeout(300)
            rec = p.locator(".inline-payment-panel input[formcontrolname='amountReceived']")
            if rec.count():
                rec.fill("5000")
            p.wait_for_timeout(500)
            e.cap("07-efectivo-lleno")
            p.locator("button.ipp-add-tender__btn").click()
            p.wait_for_timeout(900)
            e.cap("08-efectivo-agregado")
            p.locator(".gm-doc-seg__opt:has-text('Tarjeta')").click()
            p.wait_for_timeout(700)
            e.cap("09-tarjeta-elegida")
            amt = p.locator(".inline-payment-panel input[formcontrolname='amount']")
            if not amt.input_value():
                amt.fill("3850")
            p.locator(".inline-payment-panel input[formcontrolname='cardNumber']").fill("4821")
            p.locator(".inline-payment-panel mat-select[formcontrolname='cardType']").click()
            p.wait_for_timeout(600)
            e.cap("10-tipos-tarjeta", extra={"opciones": p.locator("mat-option").all_inner_texts()})
            p.locator("mat-option").first.click()
            p.locator(".inline-payment-panel input[formcontrolname='authorizationCode']").fill("738214")
            p.wait_for_timeout(500)
            e.cap("11-tarjeta-llena")
            p.locator("button.ipp-add-tender__btn").click()
            p.wait_for_timeout(900)
            e.cap("12-dos-metodos")
            if fase == "sin-cobrar":
                return
            n = len(e.toasts)
            p.locator("button:has-text('Cobrar')").last.click()
            for i in range(8):
                p.wait_for_timeout(700)
                if e.info()["dialogos"] or len(e.toasts) > n:
                    break
            e.cap("13-tras-cobrar")
            p.wait_for_timeout(2500)
            e.cap("14-tras-cobrar-2")
            for sel in (".custom-alert-dialog-style button.confirm-button", "mat-dialog-container button:has-text('Aceptar')"):
                if p.locator(sel).count():
                    p.locator(sel).first.click()
                    p.wait_for_timeout(1500)
                    break
            e.cap("15-factura-pagada")
            p.evaluate("() => window.scrollTo(0, 0)")
            p.wait_for_timeout(600)
            e.cap("16-factura-pagada-arriba")
            ir = p.locator("button:has-text('Imprimir recibo')")
            ir.scroll_into_view_if_needed(); p.wait_for_timeout(600)
            e.cap("16b-resumen-pago", extra={"html": ir.locator("xpath=ancestor::*[contains(@class,'summary') or contains(@class,'payment')][1]").first.inner_text()[:1500] if ir.count() else ""})
            p.locator("button:has-text('Versiones e historial')").click(); p.wait_for_timeout(1200)
            e.cap("16c-versiones-abierto")
            p.locator(".mat-mdc-tab:has-text('Pagos')").first.click(); p.wait_for_timeout(1500)
            p.locator(".mat-mdc-tab:has-text('Pagos')").first.scroll_into_view_if_needed(); p.wait_for_timeout(500)
            e.cap("16d-pestana-pagos", extra={"tabla": p.locator(".mat-mdc-tab-body-active table").first.inner_text()[:1500] if p.locator(".mat-mdc-tab-body-active table").count() else "sin tabla"})
            e.ir("/cashier?section=caja", ".session-bar")
            e.cap("17-mi-caja-despues")
            p.locator("button.quick-action--reconcile").click()
            p.wait_for_timeout(3000)
            e.cap("18-conteo-cierre")
            print("recs", ex.subprocess.run(["C:/Program Files/MySQL/MySQL Server 9.7/bin/mysql.exe","-h","127.0.0.1","-u","root","-N","germiva","-e","SELECT COUNT(*) FROM cashier_reconciliations WHERE company_id=43; SELECT COUNT(*) FROM cash_counts WHERE company_id=43"],capture_output=True,text=True).stdout)
            p.locator("button:has-text('Volver')").first.click(); p.wait_for_timeout(2000)
            e.cap("19-tras-volver")
        finally:
            print("errores http:", errores[:20])
            e.browser.close()
            ex.node("restaurar.mjs", "S8")
            ex.node("plan-s8.mjs", "off")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "todo")
