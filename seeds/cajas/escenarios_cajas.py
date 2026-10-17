"""Recorridos de exploración por video (los llama explorar.py).

Cada video parte de su estado (restaurar.mjs S#), entra con el ROL que lo graba y recorre sus pasos.
Los diálogos que el video solo SEÑALA se abren y se CANCELAN; la acción principal de cada video se
ejecuta de verdad por la UI (así se registran el toast/diálogo reales y el estado de salida, que se
fija como canon del estado siguiente: S3, S4, S5, S6)."""
import subprocess
import traceback
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def node(*args):
    r = subprocess.run(["node", *args], cwd=str(AQUI), capture_output=True, text=True, encoding="utf8")
    salida = (r.stdout + r.stderr).strip()
    print("   ", salida.splitlines()[-1] if salida else "", flush=True)
    if r.returncode:
        raise SystemExit("node " + " ".join(args) + " falló: " + salida)

HUB = "/cashier?section="
DLG = "mat-dialog-container"


def _paso(ex, nombre, fn):
    try:
        fn()
        return True
    except Exception as e:  # la exploración sigue; queda evidencia del fallo
        print(f"  ✗ {ex.video}-{nombre}: {str(e).splitlines()[0][:200]}", flush=True)
        try:
            ex.cap(f"ERROR-{nombre}", notas=traceback.format_exc()[-1500:])
        except Exception:
            pass
        return False


def teclear(ex, sel, texto, limpiar=True):
    loc = ex.page.locator(sel).first
    loc.scroll_into_view_if_needed()
    try:
        loc.click(timeout=3000)
    except Exception:
        loc.focus()
    if limpiar:
        loc.fill("")
    ex.page.keyboard.type(str(texto), delay=20)
    ex.page.wait_for_timeout(250)


def elegir(ex, sel_select, opcion):
    ex.page.locator(sel_select).first.click()
    ex.page.wait_for_timeout(500)
    ex.page.locator(f"mat-option:has-text('{opcion}')").first.click()
    ex.page.wait_for_timeout(500)


def auto(ex, sel_input, texto, opcion):
    teclear(ex, sel_input, texto)
    ex.page.wait_for_timeout(1500)
    ex.page.locator(f"mat-option:has-text('{opcion}')").first.click()
    ex.page.wait_for_timeout(600)


def accion(ex, sel, nombre_toast):
    """Pulsa y registra el toast o el diálogo que salga (texto exacto)."""
    n = len(ex.toasts)
    ex.clic(sel, 300)
    t = ex.esperar_toast(n, 9000)
    ex.page.wait_for_timeout(400)
    ex.cap(nombre_toast, notas=f"toast: {t!r}")
    return t


# ── Video 1 — tablero y tus cajas (admin, S0) ────────────────────────────────
def v1(ex):
    node("restaurar.mjs", "S0")
    ex.entrar("admin.progreso")
    ex.ir(HUB + "cajas", "article.board-card")
    ex.cap("01-tablero", notas="S0, admin")
    _paso(ex, "01-filtro-abiertas", lambda: (ex.clic(".board-toolbar nav button.segmented__option:has-text('Abiertas')"),
                                             ex.cap("01-filtro-abiertas"),
                                             ex.clic(".board-toolbar nav button.segmented__option:has-text('Todas')")))
    _paso(ex, "01-menu-tarjeta", lambda: (ex.clic("article.board-card[aria-label='Caja Caja Mostrador 2'] button.board-card__menu"),
                                          ex.cap("01-menu-tarjeta"), ex.page.keyboard.press("Escape")))

    def nueva():
        ex.clic("button.board-toolbar__new")
        ex.cap("02-nueva-caja-vacia")
        d = ".cashier-form-dialog"
        teclear(ex, f"{d} input[formcontrolname='name']", "Caja Mostrador 3")
        teclear(ex, f"{d} input[formcontrolname='code']", "CAJA-03")
        teclear(ex, f"{d} input[formcontrolname='location']", "Área de ventas — piso 2")
        ex.page.locator(f"{d} mat-checkbox:has-text('Transferencia')").first.click()
        ex.cap("02-nueva-caja-llena-arriba")
        teclear(ex, f"{d} input[formcontrolname='minCashLimit']", "1000")
        teclear(ex, f"{d} input[formcontrolname='maxCashLimit']", "60000")
        ex.cap("02-nueva-caja-llena-abajo", notas="tras teclear límites (el diálogo hace scroll interno)")
        accion(ex, f"{d} button:has-text('Crear caja')", "02-nueva-caja-toast")
    _paso(ex, "02-nueva-caja", nueva)

    def panel():
        ex.clic(".page-hero-actions button:has-text('Configuración')")
        ex.cap("03-panel-cajas")
        ex.clic("tr:has-text('Caja Mostrador 3') button:has(mat-icon:text-is('more_vert'))")
        ex.cap("03-menu-fila-mostrador3")
        ex.page.keyboard.press("Escape")
        ex.page.wait_for_timeout(400)
        ex.clic(".toolbar-archived button:has-text('Archivadas')")
        ex.cap("03-archivadas")
        ex.clic(".toolbar-archived button:has-text('Operativas')")
        ex.clic(".settings-sheet__header button.cashier-sheet-close")
        ex.cap("03-panel-cerrado")
    _paso(ex, "03-panel", panel)


# ── Video 2 — denominaciones y políticas (admin, S0) ─────────────────────────
def v2(ex):
    node("restaurar.mjs", "S0")
    ex.entrar("admin.progreso")
    ex.ir("/cashier?section=cajas&config=denominaciones", "text=Nueva denominación")
    ex.cap("01-denominaciones")

    def denom():
        ex.clic("button:has-text('Nueva denominación')")
        ex.cap("01-nueva-denominacion-vacia")
        teclear(ex, f"{DLG} input[formcontrolname='nameCount']", "Veinte")
        teclear(ex, f"{DLG} input[formcontrolname='valueCount']", "20")
        ex.page.locator(f"{DLG} .type-seg button:has-text('Billete')").first.click()
        teclear(ex, f"{DLG} input[formcontrolname='sort']", "7")
        ex.cap("01-nueva-denominacion-llena")
        accion(ex, f"{DLG} button:has-text('Crear denominación')", "01-denominacion-toast")
    _paso(ex, "01-denominacion", denom)

    def politicas():
        ex.clic("nav.segmented--sub button.segmented__option:has-text('Políticas')")
        ex.page.wait_for_timeout(1200)
        ex.cap("02-politicas-arriba")
        for i, y in enumerate((600, 1200, 1800, 2600)):
            ex.page.mouse.move(900, 400)
            ex.page.mouse.wheel(0, 600)
            ex.page.wait_for_timeout(500)
            ex.cap(f"02-politicas-scroll{i + 1}")
        teclear(ex, "input[formcontrolname='alertThresholdLow']", "1000")
        teclear(ex, "input[formcontrolname='alertThresholdHigh']", "60000")
        ex.cap("03-umbrales-llenos")
        accion(ex, "button[type=submit]:has-text('Guardar configuración')", "03-politicas-toast")
    _paso(ex, "02-politicas", politicas)


# ── Video 3 — abre tu caja y registra (yohanna, S1 → S3) ──────────────────────
def v3(ex):
    node("restaurar.mjs", "S1")
    ex.entrar("yohanna.peralta")
    ex.ir("/cashier", "article.board-card, .gm-state")
    ex.cap("00-aterrizaje-sin-section", notas="a dónde cae la cajera sin ?section=")
    ex.ir(HUB + "cajas", "article.board-card")
    ex.cap("01-tablero-cajera")

    def abrir():
        ex.clic("article.board-card[aria-label='Caja Caja Principal'] .board-card__foot button:has-text('Abrir sesión')", 1500)
        ex.cap("01-abrir-mi-caja")
        teclear(ex, f"{DLG} textarea[formcontrolname='notes']", "Turno de la mañana")
        ex.cap("01-abrir-mi-caja-lleno")
        n = len(ex.toasts)
        ex.clic(f"{DLG} button:has-text('Abrir caja')", 300)
        t = ex.esperar_toast(n, 9000)
        ex.page.wait_for_timeout(2000)
        ex.cap("01-mi-caja-recien-abierta", notas=f"toast: {t!r}")
    if not _paso(ex, "01-abrir", abrir):
        return

    def entrada():
        ex.clic("button.quick-action--in", 1500)
        ex.cap("02-entrada-vacia")
        teclear(ex, f"{DLG} input[formcontrolname='amount']", "2000")
        auto(ex, f"{DLG} app-autocomplete:has(mat-label:text-is('Cuenta contable')) input", "Otros ingresos", "Otros ingresos diversos")
        teclear(ex, f"{DLG} textarea[formcontrolname='notes']", "Cambio en monedas traído del banco")
        ex.cap("02-entrada-llena")
        accion(ex, f"{DLG} button:has-text('Crear movimiento')", "02-entrada-toast")
    _paso(ex, "02-entrada", entrada)

    def salida():
        ex.clic("button.quick-action--out", 1500)
        teclear(ex, f"{DLG} input[formcontrolname='amount']", "6500")
        ex.page.locator(f"{DLG} button:has(mat-icon:text-is('percent'))").first.click()
        ex.page.wait_for_timeout(400)
        auto(ex, f"{DLG} app-autocomplete:has(mat-label:text-is('Cuenta contable')) input", "Otros gastos", "Otros gastos generales")
        teclear(ex, f"{DLG} textarea[formcontrolname='notes']", "Pago del mantenimiento del aire acondicionado")
        ex.cap("03-salida-llena")
        ex.page.locator(f"{DLG} .movement-summary").first.scroll_into_view_if_needed()
        ex.cap("03-salida-resumen")
        accion(ex, f"{DLG} button:has-text('Crear movimiento')", "03-salida-toast")
    _paso(ex, "03-salida", salida)

    def resumen():
        ex.clic(".workspace-tabs .mat-mdc-tab:has-text('Resumen')", 1200)
        ex.cap("04-resumen")
        ex.clic(".workspace-tabs .mat-mdc-tab:has-text('Movimientos')", 1200)
        ex.cap("04-movimientos")
        ex.clic("app-simple-movement-list button[aria-label='Ver detalle']", 1200)
        ex.cap("04-detalle-movimiento")
        ex.cancelar_dialogo()
        ex.clic("app-simple-movement-list button[aria-label='Anular movimiento']", 1200)
        ex.cap("04-anular-movimiento")
        ex.cancelar_dialogo()
    _paso(ex, "04-resumen", resumen)

    def no_cierra():  # «Aún no puedes cerrar la caja» (salida por aprobar)
        ex.clic(".session-bar__actions button:has-text('Cerrar caja')", 1500)
        ex.cap("05-alt-aun-no-puedes-cerrar")
        ex.page.keyboard.press("Escape")
        ex.page.wait_for_timeout(500)
        c = ex.page.locator(".custom-alert-dialog-style button.confirm-button")
        if c.count() and c.first.is_visible():
            c.first.click()
    _paso(ex, "05-alt-no-cierra", no_cierra)
    _paso(ex, "impresora-cajera", lambda: impresora(ex, "cajera", guardar=True))
    node("fijar.mjs", "S3")


def impresora(ex, rol, guardar):
    """⋮ «Ajustes de este equipo» → «Configurar impresora» (con sesión abierta, modo Flexible)."""
    v = ex.video
    ex.video = "impresora"
    try:
        ex.ir(HUB + "caja", "header.session-bar")
        ex.clic("button[aria-label='Ajustes de este equipo']")
        ex.cap(f"{rol}-01-menu-equipo")
        ex.clic(".mat-mdc-menu-panel button:has(mat-icon:text-is('print'))", 1800)
        ex.cap(f"{rol}-02-dialogo")
        if not guardar:
            ex.cancelar_dialogo()
            return
        teclear(ex, f"{DLG} input[formcontrolname='printerVendorId']", "0483")
        teclear(ex, f"{DLG} input[formcontrolname='printerProductId']", "070b")
        ex.cap(f"{rol}-03-dialogo-lleno")
        n = len(ex.toasts)
        ex.clic(f"{DLG} button:has-text('Guardar')", 300)
        t = ex.esperar_toast(n, 8000)
        ex.page.wait_for_timeout(800)
        ls = ex.page.evaluate("() => Object.fromEntries(Object.keys(localStorage).filter(k => /hard|printer|impres|station|cashier/i.test(k)).map(k => [k, localStorage.getItem(k)]))")
        ex.cap(f"{rol}-04-tras-guardar", notas=f"toast: {t!r}", extra={"localStorage": ls})
        if ex.page.locator(DLG).count():
            ex.cancelar_dialogo()
    finally:
        ex.video = v


# ── Video 4 — aprobar y transferir (carmen, S3 → S4) ──────────────────────────
def v4(ex):
    node("restaurar.mjs", "S3")
    ex.entrar("carmen.rosario")
    ex.ir(HUB + "aprobaciones", "text=Movimientos pendientes de aprobación")
    ex.cap("01-por-aprobar")

    def aprobar():
        ex.clic("tr:has-text('6,500') button[aria-label='Aprobar']", 1000)
        ex.cap("01-aprobar-dialogo")
        accion(ex, ".custom-alert-dialog-style button.confirm-button", "01-aprobar-toast")
    _paso(ex, "01-aprobar", aprobar)

    def transferir():
        ex.ir(HUB + "historial&tab=transferencias", "nav[aria-label='Listados del historial']")
        ex.cap("02-historial-transferencias")
        ex.clic("button:has-text('Nueva transferencia')", 1500)
        ex.cap("02-nueva-transferencia-vacia")
        elegir(ex, f"{DLG} mat-select[formcontrolname='sourceCashier']", "Caja Mostrador 2")
        elegir(ex, f"{DLG} mat-select[formcontrolname='targetCashier']", "Caja Principal")
        teclear(ex, f"{DLG} input[formcontrolname='amount']", "3000")
        teclear(ex, f"{DLG} textarea[formcontrolname='notes']", "Reposición de cambio para la caja principal")
        ex.cap("02-nueva-transferencia-llena")
        accion(ex, f"{DLG} button:has-text('Crear transferencia')", "02-transferencia-toast")
    _paso(ex, "02-transferir", transferir)

    def recibir():
        ex.clic("tr:has-text('TRF-2026-00001') button[mattooltip='Recibir']", 1500)
        ex.cap("03-recibir-dialogo")
        accion(ex, f"{DLG} button:has-text('Confirmar recepción')", "03-recibir-toast")
    _paso(ex, "03-recibir", recibir)
    node("fijar.mjs", "S4")


# ── Video 5 — cierre con conteo (yohanna, S4 → S5) ────────────────────────────
def v5(ex):
    node("restaurar.mjs", "S4")
    ex.entrar("yohanna.peralta")
    ex.ir(HUB + "caja", "header.session-bar")
    ex.cap("01-mi-caja-con-todo")

    def cerrar():
        ex.clic(".session-bar__actions button:has-text('Cerrar caja')", 1500)
        ex.cap("01-conteo-requerido-dialogo")
        ex.clic(".custom-alert-dialog-style button.confirm-button", 3000)
        ex.cap("01-pagina-conteo")
    if not _paso(ex, "01-cerrar", cerrar):
        return

    def montos():
        ex.page.locator("button:has-text('Ver cálculo')").first.click() if ex.page.locator("button:has-text('Ver cálculo')").count() else None
        ex.page.wait_for_timeout(500)
        ex.cap("02-ingresar-montos")
        sel = ".detail-row:has(.method-label:has-text('Efectivo')) input[formcontrolname='actualAmount']"
        if not ex.page.locator(sel).count():
            sel = "input[formcontrolname='actualAmount']"
        teclear(ex, sel, "3480")
        ex.page.keyboard.press("Tab")
        ex.page.wait_for_timeout(600)
        teclear(ex, "input[formcontrolname='justification']", "Faltan 20 pesos en monedas")
        ex.cap("02-montos-llenos")
        ex.clic("button:has-text('Siguiente')", 1500)
        ex.cap("03-confirmar-cuadre")
        accion(ex, "button:has-text('Registrar conteo')", "03-registrar-toast")
        ex.page.wait_for_timeout(1500)
        ex.cap("03-vuelta-a-mi-caja")
    _paso(ex, "02-montos", montos)
    node("fijar.mjs", "S5")


# ── Video 6 — cuadre oficial, arqueo, desbloqueo (carmen, S5 → S6) ────────────
def v6(ex):
    node("restaurar.mjs", "S5")
    ex.entrar("carmen.rosario")
    ex.ir(HUB + "aprobaciones", "text=Cuadres pendientes de confirmación")
    ex.cap("01-por-aprobar-cuadres")

    def cuadre():
        ex.clic("button[aria-label='Ver detalle del cuadre']", 2000)
        ex.cap("01-detalle-cuadre")
        ex.page.locator(f"{DLG} mat-checkbox:has-text('Corregir el conteo')").first.click()
        ex.page.wait_for_timeout(600)
        ex.cap("01-detalle-cuadre-corregir", notas="solo para ver el reconteo; se desmarca")
        ex.page.locator(f"{DLG} mat-checkbox:has-text('Corregir el conteo')").first.click()
        ex.clic(f"{DLG} button:has-text('Aprobar cuadre')", 900)
        ex.cap("01-aprobar-cuadre-confirmacion")
        accion(ex, ".custom-alert-dialog-style button.confirm-button", "01-aprobar-cuadre-toast")
    _paso(ex, "01-cuadre", cuadre)

    def arqueo():
        ex.ir(HUB + "historial&tab=cuadres", "nav[aria-label='Listados del historial']")
        ex.cap("02-historial-cuadres")
        ex.clic("button:has-text('Nuevo cuadre')", 2500)
        ex.cap("02-generar-cuadre-paso1")
        auto(ex, "app-autocomplete:has(mat-label:text-is('Sesión de caja')) input", "Mostrador", "Caja Mostrador 2")
        elegir(ex, "mat-select[formcontrolname='reconciliationType']", "Arqueo sorpresa")
        ex.cap("02-paso1-lleno")
        ex.clic("button:has-text('Continuar')", 2000)
        ex.cap("02-paso2")
        esperado = ex.page.evaluate("() => { const r = document.querySelector('.detail-row'); return r ? r.innerText : ''; }")
        sel = ".detail-row:has(.method-label:has-text('Efectivo')) input[formcontrolname='actualAmount']"
        teclear(ex, sel, "3050")
        ex.page.keyboard.press("Tab")
        ex.cap("02-paso2-lleno", notas=f"fila: {esperado!r}")
        ex.clic("button:has-text('Siguiente')", 1500)
        ex.cap("02-paso3")
        accion(ex, "button:has-text('Generar cuadre')", "02-arqueo-toast")
    _paso(ex, "02-arqueo", arqueo)

    def desbloquear():
        ex.ir(HUB + "cajas&estado=bloqueadas", "article.board-card")
        ex.cap("03-tablero-bloqueadas")
        ex.clic("article.board-card[aria-label='Caja Caja Sucursal Santiago'] .board-card__foot button:has-text('Desbloquear')", 1500)
        ex.cap("03-desbloquear-dialogo")
        teclear(ex, f"{DLG} textarea[formcontrolname='notes']", "Arqueo revisado con la gerencia: el faltante quedó justificado")
        ex.page.locator(f"{DLG} mat-checkbox:has-text('Confirmo')").first.click()
        ex.cap("03-desbloquear-lleno")
        accion(ex, f"{DLG} button:has-text('Desbloquear caja')", "03-desbloquear-toast")
    _paso(ex, "03-desbloquear", desbloquear)
    node("fijar.mjs", "S6")


# ── Video 7 — historial y análisis (carmen, S6) ──────────────────────────────
def v7(ex):
    node("restaurar.mjs", "S6")
    ex.entrar("carmen.rosario")
    ex.ir(HUB + "cajas", "article.board-card")

    def sesiones():
        ex.clic("article.board-card[aria-label='Caja Caja Principal'] button.board-card__menu")
        ex.cap("01-menu-tarjeta-principal")
        ex.clic(".mat-mdc-menu-panel button:has-text('Sesiones')", 2000)
        ex.cap("01-historial-sesiones-principal")
        for tab in ("Movimientos", "Transferencias", "Cuadres"):
            ex.clic(f"nav[aria-label='Listados del historial'] button:has-text('{tab}')", 1500)
            ex.cap(f"01-historial-{tab.lower()}")
    _paso(ex, "01-historial", sesiones)

    def analisis():
        ex.ir(HUB + "analisis", "text=Reporte diario")
        ex.cap("02-analisis-diario")
        for tab, tag in (("Cuadres y análisis", "cuadres"), ("Rendimiento", "rendimiento"), ("Alertas", "alertas"), ("Auditoría", "auditoria")):
            ex.clic(f"button:has-text('{tab}'), [role=tab]:has-text('{tab}')", 2000)
            ex.cap(f"0{2 if tag in ('cuadres', 'rendimiento') else 3}-analisis-{tag}")
    _paso(ex, "02-analisis", analisis)


# ── Impresora con el rol que SÍ puede guardar (admin con sesión propia, S0) ───
def impresora_admin(ex):
    node("restaurar.mjs", "S0")
    ex.entrar("admin.progreso")
    ex.video = "impresora"
    ex.ir(HUB + "cajas", "article.board-card")

    def abrir():
        ex.clic("article.board-card[aria-label='Caja Caja Principal'] .board-card__foot button:has-text('Abrir sesión')", 1500)
        ex.clic(f"{DLG} button:has-text('Abrir caja')", 3000)
    if _paso(ex, "admin-abrir", abrir):
        _paso(ex, "admin", lambda: impresora(ex, "admin", guardar=True))


ESCENARIOS = {"v1": v1, "v2": v2, "v3": v3, "v4": v4, "v5": v5, "v6": v6, "v7": v7, "impresora": impresora_admin}


# ── Verificación puntual de selectores dudosos (cuenta nodos VISIBLES) ───────
def _contar(ex, sels):
    r = {}
    for s in sels:
        try:
            loc = ex.page.locator(s)
            n = loc.count()
            r[s] = f"{sum(1 for i in range(min(n, 8)) if loc.nth(i).is_visible())}/{n}"
        except Exception as e:
            r[s] = "ERROR " + str(e).splitlines()[0][:60]
    return r


def verificar(ex):
    import json as _j
    out = {}
    node("restaurar.mjs", "S4")
    ex.entrar("yohanna.peralta")
    ex.ir(HUB + "caja", "header.session-bar")
    out["mi-caja (yohanna, S4)"] = _contar(ex, [
        "#cashier-hub-tab-cajas", "#cashier-hub-tab-caja", "button.panel-collapse",
        "a[href='/cashier']", "a[href*='cashier']", ".sidebar a:has-text('Cajas')", "[mattooltip='Cajas']",
        "header.session-bar", "section.breakdown-panel", "button.quick-action--in", "button.quick-action--out",
        "button.quick-action--reconcile", ".session-bar__actions button:has-text('Cerrar caja')",
        ".workspace-tabs .mat-mdc-tab:has-text('Movimientos')", ".workspace-tabs .mat-mdc-tab:has-text('Resumen')",
        "app-simple-movement-list button[aria-label='Ver detalle']", "app-simple-movement-list tr:has-text('MOV-2026-00010')",
        ".chatbot-fab"])
    ex.page.goto("http://localhost:4200/cashier/reconciliation/new?session=513&returnUrl=%2Fcashier%3Fsection%3Dcaja", wait_until="networkidle")
    ex.page.wait_for_timeout(2500)
    out["conteo (yohanna, S4)"] = _contar(ex, [
        ".detail-row:has(.method-label:has-text('Efectivo')) input[formcontrolname='actualAmount']",
        "input[formcontrolname='actualAmount'][aria-label='Monto recibido']", ".step-label",
        "button:has-text('Ver cálculo')", "button:has-text('Siguiente')", "h1:has-text('Conteo de cierre (previo al cuadre)')",
        "mat-step-header:has-text('Ingresar montos')"])
    ex.entrar("carmen.rosario")
    ex.ir(HUB + "cajas", "article.board-card")
    out["tablero (carmen, S4)"] = _contar(ex, [
        "article.board-card[aria-label='Caja Caja Principal']", "article.board-card[aria-label='Caja Caja Mostrador 2'] .board-card__foot button:has-text('Ver sesión')",
        "article.board-card[aria-label='Caja Caja Sucursal Santiago'] .board-card__foot button:has-text('Desbloquear')",
        ".board-card__note", "button.board-toolbar__new", "#cashier-hub-tab-aprobaciones .gm-badge--warning",
        ".page-hero-actions button:has-text('Configuración')"])
    ex.ir(HUB + "historial&tab=movimientos", "nav[aria-label='Listados del historial']")
    out["historial (carmen, S4)"] = _contar(ex, [
        "nav[aria-label='Listados del historial'] button:has-text('Sesiones')",
        "nav[aria-label='Listados del historial'] button:has-text('Movimientos')",
        "nav[aria-label='Listados del historial'] button:has-text('Transferencias')",
        "nav[aria-label='Listados del historial'] button:has-text('Cuadres')",
        "tr:has-text('MOV-2026-00010') button[aria-label='Ver detalle']", "button:has-text('Nuevo movimiento')"])
    (AQUI.parent.parent / "guiones" / "exploracion-cajas" / "verificacion-selectores.json").write_text(
        _j.dumps(out, ensure_ascii=False, indent=1), encoding="utf8")
    print(_j.dumps(out, ensure_ascii=False, indent=1))


ESCENARIOS["verificar"] = verificar
