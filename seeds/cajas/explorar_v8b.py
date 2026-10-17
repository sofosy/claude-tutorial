"""Exploración 2 del video 8: ¿por dónde llega un usuario al cobro de una factura EMITIDA?
(ojo «Ver Detalles» del listado, ⋮ «Más acciones» de la factura, Ventas › Cobros › «Registrar cobro»).
Bajo cerrojo: node seeds/cajas/con-cerrojo.mjs "EXPLORANDO cajas-08" -- .venv/Scripts/python.exe seeds/cajas/explorar_v8b.py
No cobra nada (cancela los diálogos). Restaura S8 antes y después y deja el plan en 2.
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
        e.video = "v8"
        try:
            e.entrar("admin.progreso")
            p = e.page
            e.ir("/sales/invoices")
            p.wait_for_timeout(2500)
            fila = p.locator("table tbody tr").filter(has_text="Constructora").first
            fila.locator("button[aria-label='Ver Detalles']").click()
            p.wait_for_timeout(3500)
            e.cap("20-ver-detalles", extra={"url": p.url, "hay_panel_cobro": p.locator(".gm-doc-payment").count(),
                                            "boton_cobrar": p.locator("button:has-text('Cobrar')").count()})
            p.locator("button[aria-label='Más acciones']").first.click()
            p.wait_for_timeout(900)
            e.cap("21-mas-acciones-factura")
            p.keyboard.press("Escape"); p.wait_for_timeout(400)
            e.ir("/sales/payments")
            p.wait_for_timeout(2500)
            e.cap("22-cobros-lista")
            btn = p.locator("button:has-text('Registrar cobro'), button:has-text('Nuevo cobro'), button:has-text('Nuevo')").first
            btn.click(); p.wait_for_timeout(1500)
            e.cap("23-registrar-cobro")
            inp = p.locator("mat-dialog-container app-autocomplete input").first
            inp.click(); inp.type("1000", delay=60); p.wait_for_timeout(1800)
            e.cap("24-buscar-factura")
            p.locator("mat-option").first.click(); p.wait_for_timeout(2500)
            e.cap("25-factura-elegida")
        finally:
            e.browser.close()
            ex.node("restaurar.mjs", "S8")
            ex.node("plan-s8.mjs", "off")


if __name__ == "__main__":
    main()
