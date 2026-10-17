"""Ensayo de un guion: ejecuta TODOS sus pasos contra la app real, sin voz,
sin screencast y sin esperar a las palabras, usando las MISMAS funciones del
motor (tutorial/grabar.py) para localizar, centrar en la franja visible y
pulsar con el ratón en el centro del elemento (R6: imitar al motor, no a
`locator.click()` de Playwright).

    .venv/Scripts/python.exe seeds/_puertas/ensayar.py <modulo|ruta.json> [--paso ID] [--headed] [--salida DIR]

OJO: escribe en la base igual que la grabación (crea movimientos, etc.).

Salida: una línea por acción `OK|FALLO  <tipo> <selector>  visible=entero|CORTADO  (ms)`,
las alertas que aparecieron y una captura por paso en salida/<modulo>/ensayo/<paso>.png.
Código de salida: 0 todo OK · 1 hubo fallos · 2 no se ejecutó ningún paso
(login fallido, API caída: R28, un ensayo vacío NO es un verde).
"""
import argparse
import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
for _f in (sys.stdout, sys.stderr):
    if hasattr(_f, "reconfigure"):
        _f.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import TimeoutError as PlaywrightTimeout  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

from tutorial import grabar as g  # noqa: E402
from tutorial import rutas  # noqa: E402
from tutorial.capturar import _sesion, _setup, _sub  # noqa: E402

PAUSA_MS = 400  # entre acciones: sin voz no hay palabra que esperar


def cargar(arg):
    """Nombre de módulo (guiones/<m>.json) o ruta a un .json, con config encima."""
    if not arg.lower().endswith(".json"):
        return arg, rutas.cargar_guion(arg)
    ruta = Path(arg).resolve()
    guion = {}
    for capa in (rutas._leer("config.json"), rutas._leer("config.local.json"),
                 json.loads(ruta.read_text(encoding="utf-8"))):
        guion.update({k: v for k, v in capa.items() if not k.startswith("_")})
    guion["pasos"] = [p for base in guion["pasos"] for p in rutas._expandir_campos(base)]
    return ruta.stem, guion


def _visible(ctx, desde):
    """Lo que el motor MIDIÓ al registrar la acción (el último evento con medida)."""
    for ev in reversed(ctx.eventos[desde:]):
        if "visible" in ev:
            return {True: "entero", False: "CORTADO"}.get(ev["visible"], "?")
    return "-"


def _una(pag, ctx, acc, variables):
    """Ejecuta una acción como grabar._acciones, sin reloj. Devuelve (tipo, sel)."""
    if "click" in acc:
        g._clic(pag, acc["click"], ctx)
        return "click", acc["click"]
    if "arrastrar" in acc:
        g._arrastrar(pag, acc["arrastrar"], ctx)
        return "arrastrar", acc["arrastrar"]["desde"]
    if "escribir" in acc:
        e = acc["escribir"]
        g._escribir(pag, e["sel"], _sub(e["texto"], variables), ctx)
        return "escribir", e["sel"]
    if "resaltar" in acc:
        marca = dict(acc, sel=acc["resaltar"]) if isinstance(acc["resaltar"], str) else dict(acc["resaltar"])
        g._resaltar(pag, marca, ctx, cursor=acc.get("cursor", True))
        pag.evaluate("window.__tut && __tut.clear()")  # sin reloj no se apaga sola
        return "resaltar", marca["sel"]
    if "seleccionar" in acc:
        s = acc["seleccionar"]
        _, caja = g._localizar(pag, s["sel"])
        g._mover(pag, *g._centro(caja))
        pag.select_option(s["sel"], s["valor"])
        ctx.registro("seleccionar", s["sel"])
        return "seleccionar", s["sel"]
    if "marcar" in acc:
        if not pag.locator(acc["marcar"]).first.is_checked():
            g._clic(pag, acc["marcar"], ctx)
        return "marcar", acc["marcar"]
    if "click_opcional" in acc:
        loc = pag.locator(acc["click_opcional"]).first
        try:
            loc.wait_for(state="visible", timeout=acc.get("espera_ms", 4000))
        except PlaywrightTimeout:
            return "click_opcional(no salió)", acc["click_opcional"]
        g._clic(pag, acc["click_opcional"], ctx)
        return "click_opcional", acc["click_opcional"]
    if "subir" in acc:
        s = acc["subir"]
        _, caja = g._localizar(pag, s["ancla"] if s.get("ancla") else s["sel"])
        g._mover(pag, *g._centro(caja))
        pag.locator(s["sel"]).first.set_input_files(str(RAIZ / s["archivo"]))
        ctx.registro("subir", s["sel"])
        return "subir", s["sel"]
    if "presionar" in acc:
        p = acc["presionar"]
        pag.press(p["sel"], p["tecla"]) if p.get("sel") else pag.keyboard.press(p["tecla"])
        return "presionar", p["tecla"]
    if "esperar_ms" in acc:
        pag.wait_for_timeout(acc["esperar_ms"])
        return "esperar_ms", str(acc["esperar_ms"])
    if "quitar_marca" in acc or "plano_general" in acc:
        pag.evaluate("window.__tut && __tut.clear()")
        return "quitar_marca" if "quitar_marca" in acc else "plano_general", ""
    if "insignia" in acc:
        datos = acc["insignia"]
        g._insignia_accion(pag, ctx, acc)
        if datos:
            _capa_ok(pag, "ins", datos.get("texto", ""))
        else:
            pag.wait_for_timeout(350)
            on = pag.evaluate("""() => { const h = document.getElementById('__tut_ui');
                const e = h && h.shadowRoot && h.shadowRoot.getElementById('ins');
                return e ? e.classList.contains('on') : null; }""")
            if on:
                raise RuntimeError("insignia: sigue mostrando la anterior tras quitarla con null")
        return "insignia", (datos or {}).get("texto", "quitar")
    if "cartel" in acc:
        g._cartel(pag, ctx, acc)
        _capa_ok(pag, "car", acc["cartel"].get("texto", ""))
        pag.evaluate("window.__tut && __tut.cartelFuera(null)")  # sin reloj no se va sola
        return "cartel", acc["cartel"].get("titulo") or acc["cartel"].get("tipo", "consejo")
    if "diagrama" in acc:
        spec = g._spec_diagrama(acc["diagrama"])
        for k in ("fondo", "fase", "pasos_ms"):
            if k in acc:
                spec[k] = acc[k]
        g._abrir_diagrama(pag, ctx, spec, acc.get("durante_ms"))
        _capa_ok(pag, "lam", "")
        return "diagrama", spec["nombre"]
    if "diagrama_fase" in acc:
        n = int(acc["diagrama_fase"])
        g._fase_diagrama(pag, ctx, n)
        _fase_ok(pag, n)
        return "diagrama_fase", str(n)
    if "diagrama_cerrar" in acc:
        g._cerrar_diagrama(pag, ctx)
        return "diagrama_cerrar", ""
    if "al_decir" in acc and len(acc) == 1:
        return "ritmo", ""
    raise ValueError(f"acción desconocida: {acc}")


def _capa_ok(pag, ident, texto):
    """La capa del motor (shadow root de #__tut_ui) pintó el elemento: `on` y con su texto."""
    pag.wait_for_timeout(350)
    est = pag.evaluate("""([i, t]) => { const h = document.getElementById('__tut_ui');
        const e = h && h.shadowRoot && h.shadowRoot.getElementById(i);
        return e ? {on: e.classList.contains('on'), txt: e.innerText || ''} : null; }""", [ident, texto])
    if not est or not est["on"]:
        raise RuntimeError(f"la capa no muestra #{ident}")
    if texto and texto[:30] not in est["txt"]:
        raise RuntimeError(f"#{ident} no trae el texto «{texto[:30]}…»: «{est['txt'][:60]}»")


def _fase_ok(pag, n):
    """La lámina tiene elementos data-fase=n y quedaron visibles."""
    pag.wait_for_timeout(350)
    r = pag.evaluate("""n => { const h = document.getElementById('__tut_ui');
        const l = h && h.shadowRoot && h.shadowRoot.getElementById('lam');
        if (!l || !l.classList.contains('on')) return -1;
        const e = [...l.querySelectorAll(`[data-fase="${n}"]`)];
        return e.length ? e.filter(x => x.classList.contains('on')).length : 0; }""", n)
    if r == -1:
        raise RuntimeError("no hay lámina abierta")
    if r == 0:
        raise RuntimeError(f"la lámina no tiene (o no revela) elementos data-fase={n}")


def main():
    ap = argparse.ArgumentParser(prog="ensayar")
    ap.add_argument("modulo")
    ap.add_argument("--paso", help="solo los pasos cuyo id empieza así (como tut --paso)")
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--salida", help="carpeta de capturas (por defecto salida/<modulo>/ensayo)")
    a = ap.parse_args()

    nombre, guion = cargar(a.modulo)
    pasos = rutas.pasos_filtrados(guion, a.paso)
    base = guion["base_url"].rstrip("/")
    variables = dict(guion.get("variables", {}))
    db = guion.get("db")
    capturas = Path(a.salida) if a.salida else RAIZ / "salida" / nombre / "ensayo"
    capturas.mkdir(parents=True, exist_ok=True)

    fallos, acciones_ok, pasos_hechos = [], 0, 0
    print(f"ensayo · {nombre} · {len(pasos)} pasos · {base}")
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=not a.headed,
                                args=[f"--force-device-scale-factor={g.ESCALA}", *g.ARGS_IDIOMA])
        try:
            ctx_nav = nav.new_context(viewport={"width": g.ANCHO_CSS, "height": g.ALTO_CSS},
                                      device_scale_factor=g.ESCALA,
                                      **({"timezone_id": guion["zona_horaria"]} if guion.get("zona_horaria") else {}))
            ctx_nav.add_init_script(g.JS_CAPA)  # cursor, marca y sonda de alertas del motor
            pag = ctx_nav.new_page()
            try:
                _setup({"id": "guion", "setup": guion.get("setup")}, variables, db)
                _sesion(pag, guion, variables, base)
            except Exception as e:  # noqa: BLE001
                print(f"FALLO  sesión: {str(e).splitlines()[0][:200]}")
                print("\n0 pasos ejecutados: login fallido o app/API caídas (R28) → exit 2")
                sys.exit(2)
            if guion.get("sesion") and any(k in pag.url.lower() for k in ("login", "signin", "authentication")):
                print(f"FALLO  sesión: tras el login la URL sigue en {pag.url}")
                print("\n0 pasos ejecutados: login fallido (R28) → exit 2")
                sys.exit(2)

            for paso in pasos:
                pid = paso["id"]
                print(f"\n── paso {pid}")
                if paso.get("tarjeta"):
                    print("   (tarjeta: nada que ejecutar)")
                    continue
                ctx = g.Contexto(paso, None, 0, [])
                alertas_previas = 0

                def correr(tipo, sel, fn):
                    nonlocal acciones_ok, alertas_previas
                    n0, t0 = len(ctx.eventos), time.perf_counter()
                    try:
                        fn()
                        est = "OK"
                        acciones_ok += 1
                    except (g.SelectorAusente, PlaywrightTimeout, Exception) as e:  # noqa: BLE001
                        est = "FALLO"
                        fallos.append(f"{pid}: {tipo} {sel} — {str(e).splitlines()[0][:160]}")
                    ms = int((time.perf_counter() - t0) * 1000)
                    vis = _visible(ctx, n0)
                    print(f"   {est:5}  {tipo} {sel}  visible={vis}  ({ms} ms)"
                          + (f"\n          ↳ {fallos[-1].split(' — ', 1)[1]}" if est == "FALLO" else ""))
                    ctx.sondear_alertas(pag)
                    for ev in [e for e in ctx.eventos if e["tipo"] == "alerta"][alertas_previas:]:
                        print(f"          alerta: «{ev['que'][:120]}»")
                    alertas_previas = len([e for e in ctx.eventos if e["tipo"] == "alerta"])
                    return est == "OK"

                try:
                    _setup(paso, variables, db)
                except Exception as e:  # noqa: BLE001
                    fallos.append(f"{pid}: setup — {e}")
                    print(f"   FALLO  setup  ({e})")
                    continue
                pasos_hechos += 1

                insignia = paso.get("insignia") or None
                g._insignia(pag, insignia)
                if paso.get("navegar"):
                    ruta = _sub(paso["navegar"], variables)

                    def nav_fn():
                        g._navegar(pag, base, ruta, guion)
                        pag.evaluate("window.__tut && __tut.clear()")
                        g._insignia(pag, insignia)
                    correr("navegar", ruta, nav_fn)
                if insignia:
                    correr("insignia", insignia.get("texto", ""),
                           lambda: _capa_ok(pag, "ins", insignia.get("texto", "")))
                if paso.get("diagrama"):
                    def diag_fn():
                        g._abrir_diagrama(pag, ctx, g._spec_diagrama(paso["diagrama"]))
                        _capa_ok(pag, "lam", "")
                    correr("diagrama(paso)", str(paso["diagrama"]), diag_fn)

                for acc in paso.get("acciones", []):
                    info = {}

                    def fn(acc=acc):
                        info["r"] = _una(pag, ctx, acc, variables)
                    tipo = next((k for k in acc if k != "al_decir" and not k.endswith("_ms") and k != "cursor"), "?")
                    if "esperar_ms" in acc:
                        tipo = "esperar_ms"
                    val = acc.get(tipo)
                    sel = val if isinstance(val, str) else (val.get("sel", "") if isinstance(val, dict) else str(val or ""))
                    correr(tipo, sel, fn)
                    pag.wait_for_timeout(PAUSA_MS)

                if paso.get("esperar"):
                    correr("esperar", paso["esperar"], lambda: pag.wait_for_selector(
                        paso["esperar"], timeout=paso.get("esperar_timeout_ms", 30000)))
                if paso.get("pausa_ms"):
                    pag.wait_for_timeout(paso["pausa_ms"])
                for sel in paso.get("ocultar", []):
                    pag.eval_on_selector_all(sel, "els => els.forEach(e => e.style.setProperty('display','none','important'))")
                if paso.get("resaltar"):  # esquema antiguo: una marca fija por paso
                    m = paso["resaltar"][0]
                    correr("resaltar(paso)", m["sel"], lambda: g._resaltar(pag, dict(m), ctx, cursor=False))

                destino = capturas / f"{pid}.png"
                try:
                    pag.screenshot(path=str(destino))
                except Exception as e:  # noqa: BLE001
                    print(f"   (sin captura: {e})")
                pag.evaluate("window.__tut && __tut.clear()")
                if ctx.diagrama is not None:  # el motor cierra la lámina al acabar la voz del paso
                    g._cerrar_diagrama(pag, ctx)
                    pag.wait_for_timeout(500)
        finally:
            nav.close()

    print(f"\nResumen: {pasos_hechos} pasos · {acciones_ok} acciones OK · {len(fallos)} fallos"
          f" · capturas en {capturas}")
    for f in fallos:
        print(f"  ✗ {f}")
    if pasos_hechos == 0:
        print("0 pasos ejecutados → exit 2 (un ensayo vacío no es un verde)")
        sys.exit(2)
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
