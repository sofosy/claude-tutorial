# .venv/Scripts/python.exe seeds/certificacion/llenar.py contadora|cliente [--enviar] [--shots PREFIJO]
# Llena el formulario público /certificacion como lo hace el video (headless, 1280x720).
# contadora = Carolina Méndez (firma MENDEZ ROSARIO & ASOCIADOS) con 3 clientes, transferencia + comprobante.
# cliente   = Ramón Guzmán (Lavandería Agua Clara), 1 empresa, transferencia + comprobante en PDF escaneado.
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
OUT = RAIZ / "salida" / "certificacion-explorar"; OUT.mkdir(parents=True, exist_ok=True)
quien = sys.argv[1]
enviar = "--enviar" in sys.argv
pref = sys.argv[sys.argv.index("--shots") + 1] if "--shots" in sys.argv else f"llenar-{quien}"

CONTADORA = {
    "rol": "Soy el contador", "doc": "40238105718", "email": "carolina.mendez@example.com", "tel": "8095550187",
    "firma": "130555311", "exequatur": "4587",
    "clientes": [
        ("130555321", "Pedro Almonte", "pedro.almonte@example.com", "YEARLY", "Crecimiento"),
        ("130555338", "Yesenia Castillo", "yesenia.castillo@example.com", "MONTHLY", "ERP · Estándar"),
        ("40226441919", None, "josemiguel.tavarez@example.com", "MONTHLY", "Facturación · Inicial"),
    ],
    "comprobante": AQUI / "comprobante-contadora.png", "ref": "784512369", "banco": "Banco Ámbar",
}
CLIENTE = {
    "rol": "Soy el cliente", "doc": "00117350819", "email": "ramon.guzman@example.com", "tel": "8295550143",
    "clientes": [("130555346", "Ramón Guzmán", None, "MONTHLY", "Facturación · Crecimiento")],
    "comprobante": AQUI / "comprobante-cliente.pdf", "ref": "", "banco": "",
}
D = CONTADORA if quien == "contadora" else CLIENTE

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_context(viewport={"width": 1280, "height": 720}).new_page()
    errs = []
    pg.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 and "/api/" in r.url else None)
    pg.goto("http://localhost:4200/certificacion"); pg.wait_for_timeout(3000)

    def t(loc, txt):
        loc.click(); pg.keyboard.type(txt, delay=8); pg.wait_for_timeout(300)

    pg.click(f"button.role-option:has-text('{D['rol']}')")
    t(pg.locator("app-document-lookup-field input").first, D["doc"]); pg.keyboard.press("Tab"); pg.wait_for_timeout(1200)
    t(pg.locator("input[formcontrolname='email']").first, D["email"]); t(pg.locator("input[formcontrolname='phone']").first, D["tel"])
    pg.click("button:has-text('Continuar')"); pg.wait_for_timeout(1200)
    if quien == "contadora":
        pg.locator("app-document-lookup-field input").first.fill("")
        t(pg.locator("app-document-lookup-field input").first, D["firma"]); pg.keyboard.press("Tab"); pg.wait_for_timeout(1200)
        t(pg.locator("input[formcontrolname='licenseNumber']"), D["exequatur"])
        pg.click("mat-slide-toggle[formcontrolname='refersClients'] button")
        pg.click("button:has-text('Continuar')"); pg.wait_for_timeout(1200)
    for i, (rnc, own, mail, cyc, plan) in enumerate(D["clientes"]):
        if i > 0:
            pg.click("button.add-company"); pg.wait_for_timeout(800)
        card = pg.locator("app-certification-company-card").nth(i)
        doc = card.locator("app-document-lookup-field input")
        if doc.input_value() != rnc:
            doc.fill(""); t(doc, rnc); pg.keyboard.press("Tab"); pg.wait_for_timeout(1500)
        if own and card.locator("input[formcontrolname='ownerName']").count():
            o = card.locator("input[formcontrolname='ownerName']")
            if not o.input_value(): t(o, own)
        if mail:
            m = card.locator("input[formcontrolname='ownerEmail']")
            if not m.input_value(): t(m, mail)
        card.locator(f"mat-button-toggle[value='{cyc}'] button").click()
        card.locator("mat-select[formcontrolname='plan']").click(); pg.wait_for_timeout(500)
        pg.locator(f"mat-option:has-text('{plan}')").first.click()
        for d in ["Lun", "Mié", "Vie"]:
            card.locator(f"mat-chip-option:has-text('{d}')").click()
        card.locator("mat-select[formcontrolname='lifeTestFrom']").click(); pg.locator("mat-option:has-text('9:00 a. m.')").first.click()
        card.locator("mat-select[formcontrolname='lifeTestTo']").click(); pg.locator("mat-option:has-text('12:00 m.')").first.click()
        pg.wait_for_timeout(400)
    pg.click("button:has-text('Continuar')"); pg.wait_for_timeout(1200)
    if quien == "cliente":  # contador y referido: opcionales, sin marcar
        pg.click("button:has-text('Continuar')"); pg.wait_for_timeout(1000)
        pg.click("button:has-text('Continuar')"); pg.wait_for_timeout(1000)
    pg.click("button.pay-method:has-text('Transferencia')"); pg.wait_for_timeout(600)
    pg.locator("app-payment-proof-picker input[type=file]").set_input_files(str(D["comprobante"])); pg.wait_for_timeout(800)
    if D["ref"]:
        t(pg.locator("input[formcontrolname='reference']"), D["ref"])
        t(pg.locator("input[formcontrolname='bank']"), D["banco"])
    pg.click("mat-checkbox[formcontrolname='termsAccepted'] input")
    pg.screenshot(path=str(OUT / f"{pref}-antes.png"), full_page=True)
    if enviar:
        pg.click("button[type=submit]:has-text('Enviar solicitud')")
        pg.wait_for_selector("section.sent, .note--error", timeout=120000)
        pg.wait_for_timeout(1500)
        pg.screenshot(path=str(OUT / f"{pref}-enviada.png"), full_page=True)
        print(pg.locator("section.sent, .note--error").first.inner_text()[:1500])
    print("ERRS", errs)
    b.close()
