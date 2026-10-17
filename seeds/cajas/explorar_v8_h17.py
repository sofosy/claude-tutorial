"""Evidencia de H-17 (autor video 8): el admin abre la factura de S8 con la empresa en el plan 2.
Bajo cerrojo: node seeds/cajas/con-cerrojo.mjs "EXPLORANDO cajas-08" -- .venv/Scripts/python.exe seeds/cajas/explorar_v8_h17.py
Solo lectura por la UI (no cobra). Restaura S8 antes; al final restaura S0 y deja el plan en 2.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import explorar as ex  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402


def main():
    ex.node("restaurar.mjs", "S8")
    with sync_playwright() as pw:
        e = ex.Explorador(pw)
        e.video = "v8h17"
        errores = []
        try:
            ex.node("plan-s8.mjs", "off"); e.entrar("admin.progreso")
            p = e.page
            p.on("response", lambda r: errores.append(f"{r.status} {r.request.method} {r.url}") if r.status >= 400 else None)
            e.ir("/cashier?section=caja")
            e.cap("01-riel", extra={"riel": p.evaluate("() => [...document.querySelectorAll('.module-rail a, .module-rail button')].map(a => a.getAttribute('aria-label') || a.getAttribute('href'))")})
            e.ir("/sales/invoices")
            p.wait_for_timeout(2500)
            e.cap("02-facturas-por-url")
            p.locator("table tbody tr").filter(has_text="Constructora").first.locator("button[aria-label='Editar']").click()
            p.wait_for_timeout(4000)
            e.cap("03-factura-abierta", extra={"errores_http": list(errores)})
        finally:
            print("errores http:", errores[:20])
            e.browser.close()
            ex.node("restaurar.mjs", "S0")
            ex.node("plan-s8.mjs", "off")


if __name__ == "__main__":
    main()
