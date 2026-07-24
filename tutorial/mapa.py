"""Fase 3 — inventario de vistas y verificación de cobertura.

Sin inventario, "cubrir todas las vistas" es una intención que nadie puede
comprobar: se documenta lo que uno recuerda y las pantallas secundarias se quedan
fuera sin que nadie lo note. El mapa convierte eso en un hecho verificable.
"""
import json

from playwright.sync_api import sync_playwright

from .rutas import RAIZ

JS_ENLACES = """() => {
  const vistos = new Map();
  document.querySelectorAll('a[href], [routerlink], [ng-reflect-router-link]').forEach(e => {
    const destino = e.getAttribute('routerlink')
      || e.getAttribute('ng-reflect-router-link')
      || e.getAttribute('href');
    if (!destino || destino.startsWith('#') || destino.startsWith('http')) return;
    const texto = (e.innerText || e.textContent || '').trim().split('\\n')[0];
    if (!vistos.has(destino)) vistos.set(destino, {destino, etiqueta: texto,
      zona: e.closest('nav,aside,[role=navigation]') ? 'menu' : 'contenido'});
  });
  return [...vistos.values()];
}"""


def construir(guion, profundidad=2):
    """Recorre la navegación y enumera las vistas alcanzables."""
    base = guion["base_url"].rstrip("/")
    inicio = guion.get("mapa_inicio", "/")
    vistas, pendientes, visitados = {}, [inicio], set()

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_context(viewport={"width": 1440, "height": 900}).new_page()
        for nivel in range(profundidad):
            siguiente = []
            for ruta in pendientes:
                if ruta in visitados:
                    continue
                visitados.add(ruta)
                try:
                    pag.goto(base + ruta, wait_until="networkidle", timeout=30000)
                    pag.wait_for_timeout(800)
                except Exception as e:
                    vistas[ruta] = {"ruta": ruta, "error": type(e).__name__}
                    continue
                enlaces = pag.evaluate(JS_ENLACES)
                vistas[ruta] = {
                    "ruta": ruta,
                    "titulo_ui": pag.title(),
                    "url_final": pag.url.replace(base, ""),
                    "accesos": [e for e in enlaces if e["zona"] == "menu"],
                }
                siguiente += [e["destino"] if e["destino"].startswith("/")
                              else "/" + e["destino"] for e in enlaces]
            pendientes = siguiente
        nav.close()

    destino = RAIZ / "fichas" / "mapa.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps({"base_url": base, "vistas": list(vistas.values())},
                                  indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  {len(vistas)} vistas → {destino}")
    return vistas


def cobertura():
    """Vistas del mapa que ningún guion narra todavía."""
    mapa = RAIZ / "fichas" / "mapa.json"
    if not mapa.exists():
        raise SystemExit("No existe fichas/mapa.json. Corre primero: tut mapa <guion>")
    vistas = json.loads(mapa.read_text(encoding="utf-8"))["vistas"]

    narradas = set()
    for g in (RAIZ / "guiones").glob("*.json"):
        datos = json.loads(g.read_text(encoding="utf-8"))
        for paso in datos.get("pasos", []):
            if paso.get("navegar"):
                narradas.add(paso["navegar"])

    faltan = [v for v in vistas if v["ruta"] not in narradas
              and v.get("url_final") not in narradas]
    for v in faltan:
        print(f"  SIN CUBRIR  {v['ruta']}  ({v.get('titulo_ui', '?')})")
    print(f"\n  {len(vistas) - len(faltan)}/{len(vistas)} vistas cubiertas")
    return faltan
