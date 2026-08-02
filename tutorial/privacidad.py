"""Fase 2 — sustitución de datos privados y auditoría del resultado.

Se sustituye en vez de difuminar: la pantalla queda completa y legible, y la
narración puede leer los valores en voz alta porque son inventados. Difuminar
llena el video de manchas y vuelve la narración imposible.

La sustitución es determinista por hash con semilla: el mismo valor real produce
siempre el mismo valor falso, en todos los frames y en toda la narración. Sin eso
un mismo cliente aparecería con un nombre distinto en cada pantalla y el video
quedaría incoherente.
"""
import hashlib
import json
import re

# el rango 555 y el dominio ejemplo.com son marcas convencionales de ficción:
# permiten que la auditoría distinga un dato inventado de uno real que se coló
NOMBRES = ["María Fernanda", "Carlos", "Ana Lucía", "José Ramón", "Patricia",
           "Luis Alberto", "Rosa Elena", "Miguel Ángel", "Carmen", "Rafael"]
APELLIDOS = ["Rodríguez", "Peralta", "Santana", "Fernández", "Objío",
             "Guzmán", "Batista", "Mercedes", "Cabral", "Ureña"]
EMPRESAS = ["Distribuidora del Este SRL", "Comercial Altagracia SRL",
            "Servicios Integrales Caribe SRL", "Suplidora Nacional SRL",
            "Inversiones Bonao SRL", "Grupo Samaná SRL"]

PATRONES = {
    "rfc": r"\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b",
    "rnc": r"\b\d{9}\b",
    "cedula": r"\b\d{3}-\d{7}-\d\b",
    "email": r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b",
    "telefono": r"\b(?:809|829|849)[-. ]?\d{3}[-. ]?\d{4}\b",
    "tarjeta": r"\b\d{4}[- ]\d{4}[- ]\d{4}[- ]\d{4}\b",
}


def _n(tipo, valor, semilla, tope):
    h = hashlib.sha256(f"{semilla}|{tipo}|{valor}".encode()).hexdigest()
    return int(h[:12], 16) % tope


def falso(tipo, valor, semilla):
    """Valor inventado, estable para un mismo (tipo, valor, semilla)."""
    if tipo == "nombre":
        return NOMBRES[_n(tipo, valor, semilla, len(NOMBRES))]
    if tipo == "apellido":
        return APELLIDOS[_n(tipo, valor, semilla, len(APELLIDOS))]
    if tipo == "empresa":
        return EMPRESAS[_n(tipo, valor, semilla, len(EMPRESAS))]
    if tipo == "rnc":
        return f"9{_n(tipo, valor, semilla, 10 ** 8):08d}"
    if tipo == "rfc":
        # XAXX es el RFC genérico del SAT: inconfundiblemente de ejemplo
        return f"XAXX{_n(tipo, valor, semilla, 10 ** 6):06d}XX{_n(tipo, valor, semilla, 10)}"
    if tipo == "cedula":
        n = _n(tipo, valor, semilla, 10 ** 8)
        return f"{n % 1000:03d}-{n:07d}-{n % 10}"
    if tipo == "telefono":
        return f"809-555-{_n(tipo, valor, semilla, 10000):04d}"
    if tipo == "email":
        i = _n(tipo, valor, semilla, len(NOMBRES))
        usuario = NOMBRES[i].split()[0].lower()
        return f"{usuario}.{APELLIDOS[i].lower()}@ejemplo.com"
    if tipo == "tarjeta":
        return "4111 1111 1111 1111"
    return "—"


JS_RECOGER = """() => {
  const out = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; while (n = w.nextNode()) { const t = n.nodeValue.trim(); if (t) out.add(t); }
  document.querySelectorAll('input,textarea').forEach(e => { if (e.value) out.add(e.value); });
  return [...out];
}"""

JS_APLICAR = """(pares) => {
  const rep = s => { for (const [a, b] of pares) s = s.split(a).join(b); return s; };
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; while (n = w.nextNode()) {
    const r = rep(n.nodeValue); if (r !== n.nodeValue) n.nodeValue = r;
  }
  document.querySelectorAll('input,textarea').forEach(e => {
    const r = rep(e.value); if (r !== e.value) e.value = r;
  });
}"""


def _tipo_de(sel_o_texto, elemento_info):
    """Adivina el tipo por el nombre/etiqueta del campo (regla 2 del plan)."""
    t = (elemento_info or "").lower()
    for clave, tipo in [("rfc", "rfc"), ("rnc", "rnc"),
                        ("cedula", "cedula"), ("cédula", "cedula"),
                        ("mail", "email"), ("correo", "email"),
                        ("tel", "telefono"), ("phone", "telefono"),
                        ("empresa", "empresa"), ("legalname", "empresa"),
                        ("razon", "empresa"), ("apellido", "apellido"),
                        ("lastname", "apellido"), ("nombre", "nombre"),
                        ("name", "nombre")]:
        if clave in t:
            return tipo
    return None


def sustituir(pag, cfg, previo=None):
    """Reemplaza datos sensibles en el DOM, antes de la captura.

    `previo` son las sustituciones de los pasos anteriores. Es imprescindible:
    la página sobrevive entre pasos, así que un valor ya inventado sigue en
    pantalla y los patrones vuelven a reconocerlo. Sin esta guarda se sustituye
    lo sustituido, y el mismo cliente termina con un nombre distinto en cada
    pantalla — justo la incoherencia que la determinación busca evitar.
    """
    perfil = cfg.get("perfil", "estricto")
    if perfil == "ninguno":
        return {}
    semilla = cfg.get("semilla", "tutorial")
    previo = previo or {}
    mapa = dict(previo)
    ya_inventados = set(previo.values())

    # Valores de demo que NO se sustituyen: los datos que el guion escribe a
    # propósito y que la narración pronuncia en voz alta. Sin esta exención, un
    # nombre inventado por el guion se cambia por otro inventado por la
    # herramienta y la pantalla deja de coincidir con el audio.
    permitidos = [p.lower() for p in cfg.get("permitidos", [])]

    def registrar(tipo, valor):
        valor = (valor or "").strip()
        if not valor or valor in mapa or valor in ya_inventados:
            return
        if _es_inventado(tipo, valor):
            return
        if any(p in valor.lower() for p in permitidos):
            return
        mapa[valor] = falso(tipo, valor, semilla)

    # regla 1 — selectores declarados: la fuente más confiable.
    # se aplica a TODAS las coincidencias: el caso habitual es una columna de
    # tabla con muchas filas, no un campo suelto
    for regla in cfg.get("reglas", []):
        for el in pag.locator(regla["sel"]).all():
            try:
                real = (el.input_value() if el.evaluate("e => 'value' in e")
                        else el.inner_text())
            except Exception:
                continue
            registrar(regla["tipo"], real)

    # regla 2 — semántica del campo (nombre/etiqueta del input)
    for e in pag.locator("input,textarea").all():
        pista = " ".join(filter(None, [e.get_attribute("formcontrolname"),
                                       e.get_attribute("name"),
                                       e.get_attribute("id"),
                                       e.get_attribute("placeholder")]))
        tipo = _tipo_de(None, pista)
        if tipo:
            registrar(tipo, e.input_value() or "")

    # regla 3 — patrones sobre todo el texto visible (solo en perfil estricto)
    if perfil == "estricto":
        for texto in pag.evaluate(JS_RECOGER):
            for tipo, patron in PATRONES.items():
                for hallazgo in re.findall(patron, texto):
                    registrar(tipo, hallazgo)

    # regla 4 — red de seguridad: zonas que se difuminan sin clasificar
    for sel in cfg.get("zonas_privadas", []):
        pag.evaluate("""s => document.querySelectorAll(s)
            .forEach(e => e.style.filter = 'blur(7px)')""", sel)

    if mapa:
        # de más largo a más corto: si no, sustituir el dominio de un correo
        # rompería el correo completo antes de poder reemplazarlo entero
        pares = sorted(mapa.items(), key=lambda kv: -len(kv[0]))
        pag.evaluate(JS_APLICAR, pares)
    return mapa


def guardar_mapa(salida, mapa):
    (salida / "privacidad.json").write_text(
        json.dumps(mapa, indent=2, ensure_ascii=False), encoding="utf-8")


def cargar_mapa(salida):
    ruta = salida / "privacidad.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def aplicar_a_texto(texto, mapa):
    """Sustituye también en lo que se va a decir en voz alta.

    Sin esto la pantalla muestra el valor inventado y la narración pronuncia el
    real: además de filtrar el dato, el video se contradice a sí mismo.
    """
    for real, inventado in sorted(mapa.items(), key=lambda kv: -len(kv[0])):
        texto = texto.replace(real, inventado)
    return texto


# ---------------------------------------------------------------- auditoría

def _es_inventado(tipo, valor):
    if tipo == "telefono":
        return "555" in valor
    if tipo == "email":
        return valor.lower().endswith("@ejemplo.com")
    if tipo == "rnc":
        return valor.startswith("9")
    if tipo == "rfc":
        return valor.startswith("XAXX")
    if tipo == "tarjeta":
        return valor.replace(" ", "").replace("-", "") == "4111111111111111"
    return False


def auditar(salida, textos_extra=(), ids=None, permitidos=()):
    """Busca datos que parezcan reales en los frames YA renderizados.

    Corre sobre las imágenes finales, no sobre el DOM: así detecta lo que se coló
    por canvas, imágenes, PDFs incrustados o tooltips, que es justo donde la
    sustitución de DOM no alcanza.

    `permitidos` son los valores de demo exentos de sustitución (ver `sustituir`).
    El auditor tiene que conocer la misma lista: si no, marca como hallazgo cada
    dato inventado a propósito, y un informe lleno de falsos positivos deja de
    leerse — que es la única forma de que un dato real de verdad pase inadvertido.
    """
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        pytesseract = None

    hallazgos = []

    exentos = [x.lower() for x in permitidos]

    def revisar(texto, origen):
        for tipo, patron in PATRONES.items():
            for v in re.findall(patron, texto):
                if _es_inventado(tipo, v):
                    continue
                if any(e in v.lower() for e in exentos):
                    continue
                hallazgos.append((origen, tipo, v))

    if pytesseract:
        for png in sorted((salida / "anotados").glob("*.png")):
            # solo los frames del guion vigente: los sobrantes de una
            # compilación anterior no forman parte del video que se publica
            if ids is not None and png.stem not in ids:
                continue
            revisar(pytesseract.image_to_string(Image.open(png)), png.name)
    else:
        print("  aviso: pytesseract no disponible, no se revisaron los frames")

    for ruta in textos_extra:
        if ruta.exists():
            revisar(ruta.read_text(encoding="utf-8"), ruta.name)

    informe = salida / "auditoria.txt"
    if hallazgos:
        lineas = [f"{o}\t{t}\t{v}" for o, t, v in hallazgos]
        informe.write_text("POSIBLES DATOS REALES\n" + "\n".join(lineas) + "\n",
                           encoding="utf-8")
    else:
        informe.write_text("Sin hallazgos.\n", encoding="utf-8")
    return hallazgos

def ofuscar(salida, ids=None, permitidos=(), declarados=()):
    """Tapa en los frames renderizados los datos que la auditoría marcó.

    Es la última red antes de publicar. La sustitución de DOM cubre lo que el
    navegador pinta como texto, pero no lo que llega por canvas, un PDF
    incrustado o una imagen; y el OCR de la auditoría a veces lee mal un valor
    ya inventado y lo reporta igual. En ambos casos el video no puede subirse
    con un dato que parezca real, así que aquí se cubre con una banda opaca
    sobre el frame: se pierde legibilidad en ese punto, pero el video es
    publicable. Después hay que volver a montar.

    Devuelve la lista de (frame, tipo, valor) que tapó.
    """
    from PIL import Image, ImageDraw
    import pytesseract

    exentos = [x.lower() for x in permitidos]
    # los valores que el guion declara para tapar se cubren siempre, aunque no
    # coincidan con ningún patrón: es la lista explícita del autor
    forzados = [str(x) for x in declarados]
    tapados = []
    for png in sorted((salida / "anotados").glob("*.png")):
        if ids is not None and png.stem not in ids:
            continue
        img = Image.open(png)
        datos = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        dib = ImageDraw.Draw(img)
        cambios = 0
        for i, palabra in enumerate(datos["text"]):
            palabra = (palabra or "").strip()
            if not palabra:
                continue
            objetivos = [("declarado", f) for f in forzados if f in palabra]
            for tipo, patron in PATRONES.items():
                objetivos += [(tipo, v) for v in re.findall(patron, palabra)]
            for tipo, v in objetivos:
                if tipo != "declarado":
                    if _es_inventado(tipo, v) or any(e in v.lower() for e in exentos):
                        continue
                if True:
                    x, y = datos["left"][i], datos["top"][i]
                    w, h = datos["width"][i], datos["height"][i]
                    m = max(2, h // 6)
                    dib.rectangle([x - m, y - m, x + w + m, y + h + m], fill=(58, 62, 70))
                    tapados.append((png.name, tipo, v))
                    cambios += 1
                    break
        if cambios:
            img.save(png)
    return tapados

def _textos_del_guion(guion):
    """Todo el texto que el guion aporta: narración, rótulos y lo que escribe."""
    for paso in guion.get("pasos", []):
        for clave in ("narracion", "texto_pantalla", "ruta"):
            if paso.get(clave):
                yield f"{paso['id']}.{clave}", paso[clave]
        for tar in ([paso["tarjeta"]] if paso.get("tarjeta") else []):
            for k, v in tar.items():
                if isinstance(v, str):
                    yield f"{paso['id']}.tarjeta.{k}", v
        for i, acc in enumerate(paso.get("acciones", [])):
            e = acc.get("escribir")
            if e:
                yield f"{paso['id']}.escribir[{i}]", e.get("texto", "")
    for clave in ("titulo", "descripcion"):
        if guion.get(clave):
            yield clave, guion[clave]
    for clave in ("aprenderas", "errores_comunes"):
        for i, v in enumerate(guion.get(clave, [])):
            yield f"{clave}[{i}]", v


def revisar_guion(guion):
    """Analiza el guion antes de capturar y devuelve los datos sin declarar.

    Un RNC o un correo real escrito en el guion llega al video por narración,
    subtítulos y descripción de YouTube, donde la sustitución del DOM no alcanza.
    Detectarlo aquí cuesta segundos; detectarlo después de montar cuesta una
    recompilación entera, y no detectarlo cuesta que YouTube rechace el video.

    Cada valor tiene que estar en una de las dos listas de `privacidad`:
    `permitidos` (dato de demo, se muestra tal cual) u `ofuscar` (se tapa en los
    frames). Lo que no esté en ninguna se reporta.
    """
    cfg = guion.get("privacidad", {})
    exentos = [x.lower() for x in cfg.get("permitidos", [])]
    declarados = {str(x).lower() for x in cfg.get("ofuscar", [])}
    hallazgos, vistos = [], set()
    for donde, texto in _textos_del_guion(guion):
        for tipo, patron in PATRONES.items():
            for v in re.findall(patron, texto or ""):
                if _es_inventado(tipo, v):
                    continue
                if any(e in v.lower() for e in exentos):
                    continue
                if v.lower() in declarados:
                    continue
                if (donde, v) in vistos:
                    continue
                vistos.add((donde, v))
                hallazgos.append((donde, tipo, v))
    return hallazgos
