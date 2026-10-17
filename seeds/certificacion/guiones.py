# python seeds/certificacion/guiones.py  →  guiones/certificacion-0N-*.json
# Serie «Certificación e-CF» (12/10/2026): el formulario público /certificacion (lo llena una contadora con
# tres clientes) y la bandeja «Solicitudes de certificación» del equipo de Germiva (aprobar y confirmar).
# Datos ficticios: padrón local sembrado en canon.sql (ver restaurar.py). Comprobantes: comprobante.py.
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

COMUN = {
    "base_url": "http://localhost:4200",
    "zona_horaria": "America/Santo_Domingo",
    "voz": {"id": "eleven:I5NYaSWx7PlnVVFV0t2B", "velocidad": "+0%"},
    "musica": {"archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -32, "ducking": True, "fade_s": 2},
    "loudnorm": {"lufs": -14, "tp": -1.5},
    "marca_video": {"entrada_s": 3, "cierre_s": 3},
    "rotulo_paso": {"segundos": 3.5},
    "css_global": ["app-chatbot-widget{display:none!important}", ".chatbot-fab{display:none!important}"],
    "pronunciacion": {
        "e-CF": "e-ce-efe", "IA": "i-a", "ERP": "e-erre-pe", "SOFOSY": "Sofosi", "INDOTEL": "Indotel",
        "3D": "tres-de",
    },
    "privacidad": {
        "_perfil": "Todos los datos son ficticios (padrón local sembrado por seeds/certificacion, correos @example.com) "
                   "y la narración los nombra: no se sustituye nada.",
        "perfil": "ninguno",
        "permitidos": [
            "example.com", "1305553", "130555", "40238105718", "40226441919", "00117350819", "784512369", "8095550187",
            "8295550143", "4587", "SOFOSY", "germiva", "Méndez", "MENDEZ", "Almonte", "Castillo", "Tavárez", "TAVAREZ",
            "Guzmán", "GUZMAN", "Banco Ámbar",
        ],
        "mapa_fijo": {"localhost:3001": "api.germiva.com", "localhost:4200": "germiva.com"},
    },
}

SESION_ADMIN = {
    "tipo": "api",
    "url": "http://localhost:3001/api/auth/dev/login",
    "cuerpo": {"username": "admin", "password": "admin"},
    "clave": "aut",
    "extra": {"__v": 2},
    "navegar": "/home",
}


def click(sel, palabra, **kw):
    return {"click": sel, "al_decir": palabra, **kw}


def marca(sel, palabra, ms=4500, **kw):
    a = {"resaltar": sel, "durante_ms": ms, **kw}
    if palabra is not None:
        a["al_decir"] = palabra
    return a


def escribir(sel, texto, palabra):
    return {"escribir": {"sel": sel, "texto": texto}, "al_decir": palabra}


def guion(nombre, titulo, descripcion, extra, aprenderas, errores, pasos, comentario=""):
    g = {"titulo": titulo, "descripcion": descripcion, "_comentario": comentario, **COMUN, **extra,
         "aprenderas": aprenderas, "errores_comunes": errores, "pasos": pasos}
    destino = RAIZ / "guiones" / f"{nombre}.json"
    destino.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    print("escrito", destino.name, "·", len(pasos), "pasos")


# ── Selectores del formulario público ─────────────────────────────────────────────────────────────
SIGUIENTE = "form .actions button.btn-primary:has-text('Continuar')"
DOC = "app-document-lookup-field input"
LOOKUP = ".lookup-status__line"


def C(n, sel=""):
    """Dentro de la tarjeta del cliente n (1, 2, 3)."""
    return f"div.companies app-certification-company-card:nth-child({n}) {sel}".strip()


def opcion(texto):
    return f"mat-option:has-text('{texto}')"


# ══ VIDEO 1 · La contadora llena el formulario ════════════════════════════════════════════════════
guion(
    "certificacion-01-contador",
    "Certificación e-CF · Parte 1: solicitarla como contador para tus clientes",
    "Cómo un contador solicita en germiva.com/certificacion la certificación de facturación electrónica (e-CF) "
    "de sus clientes: sus datos, su firma contable y el Programa de Socios, la comisión por referir a sus "
    "clientes, cada empresa con su plan y su prueba de vida, el resumen de lo que se va a crear y el pago por "
    "transferencia con el comprobante que revisa la inteligencia artificial.",
    {"setup": {"tipo": "shell", "cmd": "python seeds/certificacion/restaurar.py A"},
     # Sin usuario: esta «sesión» solo PRECARGA /certificacion antes de que arranque la cámara (si no, los
     # primeros segundos salen en blanco). La respuesta del login se guarda en una clave que la app no lee.
     "sesion": {**SESION_ADMIN, "clave": "__precarga_tutorial", "navegar": "/certificacion",
                "esperar": "button.role-option"}},
    [
        "Abrir el formulario público de certificación y elegir «Soy el contador»",
        "Registrar tu firma contable con su RNC y pedir el ingreso al Programa de Socios con tu exequátur",
        "Marcar que tú refieres a tus clientes para cobrar tu comisión",
        "Agregar cada cliente (empresa con RNC o persona física con cédula) con su plan y su prueba de vida",
        "Pagar por transferencia, subir el comprobante y enviar la solicitud",
    ],
    [
        "Escribir el correo de otra persona como dueño: con ese correo entra al sistema y recibe su contraseña",
        "Dejar la cédula personal en «Tu firma» cuando trabajas con una firma que tiene RNC",
        "Creer que la certificación incluye el certificado digital: se compra aparte a una entidad del INDOTEL",
        "Olvidar los días y el horario de la prueba de vida: sin ellos el formulario no avanza",
        "Subir una foto de otra cosa como comprobante: la IA la rechaza y no se crea nada",
    ],
    [
        {
            "id": "01-inicio",
            "capitulo": "La página de certificación",
            "rotulo": "germiva.com/certificacion",
            "ruta": "germiva.com › Certificación",
            "texto_pantalla": "Certificación de facturación electrónica · ¿Quién llena el formulario?",
            "navegar": "/certificacion",
            "narracion": (
                "Vamos a solicitar la certificación de facturación electrónica de tres clientes, como lo hace un "
                "contador. Facturar electrónicamente es emitir e-CF, los comprobantes fiscales electrónicos que "
                "pide la DGII, la Dirección General de Impuestos Internos. Esta es la página de certificación de "
                "Germiva, y la abre cualquiera, sin usuario. Arriba dice lo esencial: nosotros hacemos la "
                "certificación con la DGII, y toma de uno a tres días si la empresa no tiene nada pendiente. "
                "A la izquierda están los pasos del formulario; a la derecha se llena el paso en el que vas. "
                "La primera pregunta es quién llena el formulario: el dueño de la empresa, o su contador. Para "
                "este video elijo Soy el contador. Fíjate que los pasos "
                "cambiaron: tus datos, tu firma, tus clientes y el pago. Y aparece una nota: con este formulario "
                "te creamos, o reconocemos, tu cuenta de contador."
            ),
            "acciones": [
                marca("header.page-hero .wrap", "facturación electrónica de tres", 6000, cursor=False),
                marca("nav.stepper ol li:first-child", "comprobantes fiscales electrónicos", 5000, cursor=False),
                marca("header.page-hero h1", "Esta es la página", 3500, cursor=False),
                marca("header.page-hero p", "lo esencial", 6000),
                marca("nav.stepper", "los pasos del formulario", 3500),
                marca("form.card h2", "se llena el paso", 3500),
                marca("div.role-picker", "quién llena", 3000),
                click("button.role-option:has-text('Soy el contador')", "elijo Soy el contador"),
                marca("nav.stepper ol", "pasos cambiaron", 5000),
                marca("p.role-note", "una nota", 5000),
            ],
        },
        {
            "id": "02-datos",
            "capitulo": "Tus datos",
            "rotulo": "Tus datos",
            "ruta": "Certificación › Paso 1: Tus datos",
            "texto_pantalla": "Tus datos · cédula o RNC, nombre, correo y teléfono",
            "narracion": (
                "Abajo van tus datos. El primer campo es tu cédula, o el RNC de tu firma; el RNC es el número con "
                "el que la DGII identifica a una empresa. Escribo mi cédula. Al terminar, Germiva la busca sola en "
                "el padrón de la DGII, la lista oficial de contribuyentes, y completa el nombre: Carolina Méndez "
                "Rosario. Si no te encuentra, lo escribes tú. Sigue el correo, que es donde te avisamos el avance "
                "de la solicitud. Lo escribo: carolina punto méndez, arroba example punto com, todo en minúsculas. "
                "Ahora va el teléfono o WhatsApp, con su código de área: ocho cero nueve, cinco cinco cinco, cero "
                "uno ocho siete. Con todo listo, pulso Continuar."
            ),
            "acciones": [
                marca(DOC, "El primer campo", 3500),
                escribir(DOC, "40238105718", "Escribo mi cédula"),
                marca(LOOKUP, "la lista oficial", 5000),
                marca("input[formcontrolname='name']", "completa el nombre", 4000),
                escribir("input[formcontrolname='email']", "carolina.mendez@example.com", "Lo escribo"),
                escribir("input[formcontrolname='phone']", "8095550187", "el teléfono"),
                click(SIGUIENTE, "pulso Continuar"),
            ],
        },
        {
            "id": "03-firma",
            "capitulo": "Tu firma y el Programa de Socios",
            "rotulo": "Tu firma contable",
            "ruta": "Certificación › Paso 2: Tu firma",
            "texto_pantalla": "Tu firma contable · RNC, exequátur y comisión por referir",
            "narracion": (
                "Paso dos: tu firma contable. Este recuadro dice para qué son estos datos: te creamos tu cuenta de "
                "contador en Germiva, y desde Mi Cartera trabajas con todos tus clientes, su contabilidad, sus "
                "facturas y sus reportes de la DGII. El formulario trajo mi cédula. Como trabajo con una firma, la "
                "cambio por el RNC de la firma, que es el que va en sus facturas. La encontró en el padrón: Méndez "
                "Rosario y Asociados. El correo y "
                "el teléfono vienen del paso anterior, y ese correo será tu usuario para entrar. Ahora el número de "
                "exequátur, el que te autoriza a ejercer como contador. Es opcional, pero con él pedimos tu ingreso "
                "al Programa de Socios: tu firma recibe la herramienta completa, sin costo. Por último, activo Yo "
                "les recomendé Germiva a estos clientes. Así ganas una comisión por lo que pague cada uno: si es tu "
                "primera vez como referidor, el veinte por ciento de lo que pague en sus primeros doce meses. "
                "Continuar."
            ),
            "acciones": [
                marca("form .note--info p:first-child", "Este recuadro", 5000),
                marca("form .note--info p:first-child strong:nth-of-type(2)", "desde Mi Cartera", 4500),
                marca("form .note--info p:nth-child(2)", "reportes de la DGII", 4000),
                escribir(DOC, "130555311", "la cambio"),
                marca(LOOKUP, "La encontró", 3000),
                marca("input[formcontrolname='name']", "Méndez Rosario", 3000),
                marca("input[formcontrolname='email']", "usuario para entrar", 3500),
                escribir("input[formcontrolname='licenseNumber']", "4587", "número de exequátur"),
                marca("mat-form-field:has(input[formcontrolname='licenseNumber']) mat-hint", "Programa de Socios", 5000),
                click("mat-slide-toggle[formcontrolname='refersClients'] button", "activo Yo les"),
                marca("form .note--info:has(mat-slide-toggle) ul", "ganas una comisión", 8000),
                click(SIGUIENTE, "Continuar"),
            ],
        },
        {
            "id": "04-cliente-1",
            "capitulo": "Tus clientes: la primera empresa",
            "rotulo": "Cliente 1",
            "ruta": "Certificación › Paso 3: Tus clientes",
            "texto_pantalla": "Tus clientes · lo que incluye cada empresa, RNC, dueño y correo",
            "narracion": (
                "Paso tres: tus clientes. Arriba está lo que va incluido en cada empresa: el equipo de Germiva hace "
                "todo el proceso de certificación por seis mil pesos, con el ITBIS incluido, en un solo pago. El "
                "ITBIS es el impuesto a las ventas. El dueño solo hace la prueba de vida, una videollamada corta "
                "con la entidad certificadora. Y una aclaración importante: no incluye el certificado digital, el "
                "archivo con el que se firman las facturas; se compra aparte a una entidad autorizada por el "
                "INDOTEL, el Instituto Dominicano de las Telecomunicaciones; te guiamos. Ahora, el cliente uno: su tarjeta lleva todo lo de esa empresa. Escribo su "
                "RNC, el de la empresa que se va a certificar. Germiva lo encontró en el padrón y completó la razón "
                "social: Distribuidora Caribe Azul. El dueño o responsable es Pedro Almonte; es quien va a usar el "
                "sistema en esa empresa. Su correo es clave: con él entra al sistema, y a ese correo le llega el "
                "mensaje para crear su contraseña."
            ),
            "acciones": [
                marca("form .service-note p:nth-child(1)", "va incluido", 5500),
                marca("form .service-note p:nth-child(1) strong:nth-of-type(2)", "prueba de vida", 4000),
                marca("form .service-note p:nth-child(2)", "no incluye", 7000),
                marca(C(1, "h3"), "el cliente uno", 3000),
                escribir(C(1, DOC), "130555321", "Escribo su RNC"),
                marca(C(1, LOOKUP), "lo encontró", 3000),
                marca(C(1, "input[formcontrolname='legalName']"), "razón social", 3000),
                escribir(C(1, "input[formcontrolname='ownerName']"), "Pedro Almonte", "dueño o responsable"),
                escribir(C(1, "input[formcontrolname='ownerEmail']"), "pedro.almonte@example.com", "Su correo"),
                marca(C(1, "mat-form-field:has(input[formcontrolname='ownerEmail'])"), "crear su contraseña", 3500),
            ],
        },
        {
            "id": "05-plan-y-prueba-de-vida",
            "capitulo": "El plan y la prueba de vida",
            "rotulo": "Plan, factura y prueba de vida",
            "ruta": "Certificación › Paso 3: Tus clientes › Cliente 1",
            "texto_pantalla": "Ciclo y plan · factura de la empresa · qué tiene ya · prueba de vida",
            "narracion": (
                "Ahora el plan de Germiva que va a usar la empresa. Primero el ciclo: anual, con su descuento, o "
                "mensual. Elijo Anual. Ahora, en el campo Plan, abro la lista de planes; cada uno trae su precio en "
                "el ciclo que elegiste. Escojo Facturación Crecimiento. Debajo aparece la factura de esta empresa: el plan más "
                "la certificación. La casilla Factura a nombre de esta empresa viene marcada; si la quitas, la "
                "factura sale a tu nombre, porque eres tú quien paga. Luego, Qué tiene ya, que es opcional: si la "
                "empresa ya tiene el certificado digital, acceso a la Oficina Virtual de la DGII, o si ya pidió ser "
                "emisor electrónico. Cada respuesta le ahorra tiempo al equipo. Marco que sí tiene acceso a la "
                "Oficina Virtual. Y la prueba de vida: los días y el horario en que el dueño puede hacer la "
                "videollamada. Elijo el lunes, que es el día que más le conviene, y también el miércoles. Ahora el "
                "horario: en Desde abro la lista. Abajo sale un aviso en rojo que solo recuerda que falta el horario. "
                "Elijo las nueve de la mañana, que es la hora de entrada; y en Hasta abro la otra lista y elijo las "
                "doce del mediodía. Con el horario completo, el aviso desaparece."
            ),
            "acciones": [
                marca(C(1, "mat-button-toggle-group[formcontrolname='billingCycle']"), "Primero el ciclo", 3000),
                click(C(1, "mat-button-toggle[value='YEARLY'] button"), "Elijo Anual"),
                click(C(1, "mat-select[formcontrolname='plan']"), "lista de planes"),
                click(opcion("Facturación · Crecimiento"), "Escojo Facturación"),
                marca(C(1, ".invoice__total"), "la factura de esta empresa", 4500),
                marca(C(1, "mat-checkbox[formcontrolname='invoiceToCompany']"), "viene marcada", 5500),
                marca(C(1, "ul.questions"), "Qué tiene ya", 6000),
                click(C(1, "li.question:nth-child(2) mat-button-toggle:first-child button"), "Marco que sí"),
                marca(C(1, "div.life-test"), "la prueba de vida", 3500),
                click(C(1, "mat-chip-option:has-text('Lun')"), "el lunes"),
                click(C(1, "mat-chip-option:has-text('Mié')"), "el miércoles"),
                click(C(1, "mat-select[formcontrolname='lifeTestFrom']"), "en Desde"),
                marca(C(1, "p.field-error"), "un aviso en rojo", 3500, cursor=False),
                click(opcion("9:00 a. m."), "las nueve"),
                click(C(1, "mat-select[formcontrolname='lifeTestTo']"), "en Hasta"),
                click(opcion("12:00 m."), "las doce"),
            ],
        },
        {
            "id": "06-cliente-2",
            "capitulo": "Agregar otra empresa",
            "rotulo": "Cliente 2",
            "ruta": "Certificación › Paso 3: Tus clientes › Cliente 2",
            "texto_pantalla": "Agregar otra empresa · cada una con su propio plan",
            "narracion": (
                "Para el segundo cliente pulso Agregar otra empresa, debajo de la tarjeta. Aparece el Cliente dos, "
                "en blanco: cada empresa elige su propio plan. Escribo el RNC, y Germiva completa el nombre de la "
                "empresa: es el Restaurante Sabor Criollo. La dueña es Yesenia Castillo: ella firma por el "
                "restaurante y recibe el acceso. Ahora escribo su correo: yesenia punto castillo, arroba example "
                "punto com. Este cliente paga cada mes, así que pulso Mensual. Luego voy al campo Plan, abro la "
                "lista, bajo un poco, y elijo ERP Estándar, un plan del sistema de gestión completo. Su prueba de vida: el martes, y si ese día no puede, el "
                "jueves. Para el horario de la tarde, en Desde abro la lista y elijo las dos de la tarde, y en "
                "Hasta, abro la otra y elijo las cinco."
            ),
            "acciones": [
                click("button.add-company", "Agregar otra empresa"),
                marca(C(2, "h3"), "Cliente dos", 2500),
                escribir(C(2, DOC), "130555338", "Escribo el RNC"),
                marca(C(2, "input[formcontrolname='legalName']"), "es el Restaurante", 2500),
                escribir(C(2, "input[formcontrolname='ownerName']"), "Yesenia Castillo", "La dueña"),
                escribir(C(2, "input[formcontrolname='ownerEmail']"), "yesenia.castillo@example.com", "escribo su correo"),
                click(C(2, "mat-button-toggle[value='MONTHLY'] button"), "pulso Mensual"),
                click(C(2, "mat-select[formcontrolname='plan']"), "abro la lista, bajo"),
                click(opcion("ERP · Estándar"), "ERP Estándar"),
                click(C(2, "mat-chip-option:has-text('Mar')"), "el martes"),
                click(C(2, "mat-chip-option:has-text('Jue')"), "el jueves"),
                click(C(2, "mat-select[formcontrolname='lifeTestFrom']"), "en Desde"),
                marca(C(2, "p.field-error"), None, 2500, cursor=False),
                click(opcion("2:00 p. m."), "las dos"),
                click(C(2, "mat-select[formcontrolname='lifeTestTo']"), "en Hasta"),
                click(opcion("5:00 p. m."), "las cinco"),
            ],
        },
        {
            "id": "07-cliente-3",
            "capitulo": "Un cliente persona física",
            "rotulo": "Cliente 3 · persona física",
            "ruta": "Certificación › Paso 3: Tus clientes › Cliente 3",
            "texto_pantalla": "Persona física · se registra con su cédula",
            "narracion": (
                "El tercero es una persona física: factura con su cédula, no con un RNC. Agrego otra empresa, y en "
                "el primer campo escribo su cédula. Con una cédula, fíjate, el campo de al lado cambia: ahora dice "
                "Nombre y apellido, como en la cédula, y ya no se pide el dueño aparte, porque es la misma persona: "
                "José Miguel Tavárez. Escribo su correo: josé miguel punto tavárez, todo junto, arroba example "
                "punto com. Este también paga mensual: pulso Mensual. En el campo Plan abro la lista, y esta vez "
                "elijo Facturación Inicial. Su prueba de vida es el sábado. Y para el horario, en Desde abro la "
                "lista y elijo las diez de la mañana, y en Hasta, abro la otra y elijo la una de la tarde. Si una "
                "empresa sobra, la quitas con Quitar, arriba a la derecha de su tarjeta; y puedes enviar hasta "
                "treinta empresas en una sola solicitud. Pulso Continuar."
            ),
            "acciones": [
                click("button.add-company", "Agrego otra empresa"),
                escribir(C(3, DOC), "40226441919", "escribo su cédula"),
                marca(C(3, "mat-form-field:has(input[formcontrolname='legalName'])"), "Nombre y apellido", 5000),
                escribir(C(3, "input[formcontrolname='ownerEmail']"), "josemiguel.tavarez@example.com", "Escribo su correo"),
                click(C(3, "mat-button-toggle[value='MONTHLY'] button"), "pulso Mensual"),
                click(C(3, "mat-select[formcontrolname='plan']"), "Plan abro la lista"),
                click(opcion("Facturación · Inicial"), "Facturación Inicial"),
                click(C(3, "mat-chip-option:has-text('Sáb')"), "el sábado"),
                click(C(3, "mat-select[formcontrolname='lifeTestFrom']"), "en Desde"),
                marca(C(3, "p.field-error"), None, 2500, cursor=False),
                click(opcion("10:00 a. m."), "las diez"),
                click(C(3, "mat-select[formcontrolname='lifeTestTo']"), "en Hasta"),
                click(opcion("1:00 p. m."), "la una"),
                marca(C(3, "button.company-card__remove"), "con Quitar", 3500),
                click(SIGUIENTE, "Pulso Continuar"),
            ],
        },
        {
            "id": "08-pago",
            "capitulo": "Resumen, pago y envío",
            "rotulo": "Pago y envío",
            "ruta": "Certificación › Paso 4: Pago y envío",
            "texto_pantalla": "Resumen · qué pasa al enviar · transferencia con comprobante",
            "narracion": (
                "Último paso: pago y envío. Arriba, el resumen: cada empresa con su plan más la certificación, y el "
                "total. Debajo, Al enviar el formulario: la lista de lo que va a pasar, escrita según tus "
                "respuestas. Ahora, cómo vas a pagar. Con tarjeta se paga aquí mismo al enviar, de forma segura con "
                "3D Secure. Yo pagué por transferencia, así que elijo Transferencia o depósito. La lista de arriba "
                "cambió: ahora todo empieza con el comprobante validado. Subo el comprobante, la captura de la "
                "transferencia; la inteligencia artificial lo revisa al enviar. Si todavía no has pagado, puedes "
                "enviar igual y subirlo después desde el enlace del correo. Los datos del pago son opcionales: "
                "anoto la referencia, que es el número de la transferencia en tu banco, y el nombre del banco, que "
                "ayuda al equipo a encontrar el pago más rápido. Acepto los términos y condiciones, y pulso Enviar "
                "solicitud."
            ),
            "acciones": [
                marca(".summary__list", "el resumen", 5000),
                marca("ul.outcomes li:first-child", "lo que va a pasar", 5000),
                marca("div.pay-methods", "cómo vas a pagar", 2500),
                marca("button.pay-method:has-text('Tarjeta')", "Con tarjeta", 4500),
                click("button.pay-method:has-text('Transferencia')", "elijo Transferencia"),
                marca("ul.outcomes li:nth-child(3)", "La lista de arriba", 4500),
                {"subir": {"sel": "app-payment-proof-picker input[type=file]", "ancla": "app-payment-proof-picker label.proof__pick",
                           "archivo": "seeds/certificacion/comprobante-contadora.png"}, "al_decir": "Subo el comprobante"},
                marca("app-payment-proof-picker .proof", "lo revisa al enviar", 4000),
                escribir("input[formcontrolname='reference']", "784512369", "la referencia"),
                escribir("input[formcontrolname='bank']", "Banco Ámbar", "el nombre del banco"),
                click("mat-checkbox[formcontrolname='termsAccepted'] .mdc-checkbox", "Acepto los términos"),
                click("button[type=submit]", "Enviar solicitud"),
            ],
        },
        {
            "id": "09-enviada",
            "capitulo": "Solicitud enviada",
            "rotulo": "¡Recibimos tu solicitud!",
            "ruta": "Certificación › Solicitud enviada",
            "texto_pantalla": "Número de solicitud · las empresas se están creando",
            "narracion": (
                "En un par de segundos, Germiva subió la captura y la inteligencia artificial la revisó: confirmó que "
                "es un pago real, y tomó el monto, la fecha, la referencia y el banco. Listo: Recibimos tu "
                "solicitud, con su número; guárdalo para cualquier consulta. Como el "
                "comprobante se validó, ya estamos creando las tres empresas, y te avisamos por correo cuando cada "
                "una esté lista. Abajo están las empresas de la solicitud. ¿Qué sigue? Cada dueño recibe su correo "
                "para crear su contraseña. Cuando el equipo de Germiva confirma el pago, quedas como contador de "
                "cada cliente, se registra tu comisión de referidor, y Éxito del Cliente los acompaña en la "
                "certificación con la DGII. Desde Mi Cartera, en tu cuenta de contador, sigues el avance de cada uno."
            ),
            "acciones": [
                marca("section.sent", None, 4000, cursor=False),
                marca(".sent__code", "con su número", 4500),
                marca("section.sent > p:nth-of-type(2)", "ya estamos creando", 6000),
                marca("ul.sent__companies", "empresas de la solicitud", 5000),
                marca("ul.sent__companies li:nth-child(1)", "Cada dueño", 4500),
                marca("ul.sent__companies li:nth-child(2)", "quedas como contador", 5000),
                marca("ul.sent__companies li:nth-child(3)", "Éxito del Cliente", 5000),
                marca("section.sent h2", "Mi Cartera", 4000),
            ],
        },
    ],
    comentario=(
        "Video 1 de la serie Certificación (12/10/2026), master del 12/10 (API #1500/#1502/#1503, web "
        "#1356/#1357/#1358). Se graba SIN sesión. setup: restaurar.py A (canon sin solicitudes). Datos del padrón "
        "local sembrados en canon.sql: cédula 40238105718 CAROLINA MENDEZ ROSARIO, firma 130555311, clientes "
        "130555321 / 130555338 / cédula 40226441919. Total 31,400 = comprobante-contadora.png. La IA (credencial "
        "OpenAI de plataforma, gpt-4o-mini) valida el comprobante y la cola crea las empresas al enviar."
    ),
)


# ══ VIDEO 2 · El equipo de Germiva aprueba y confirma ═════════════════════════════════════════════
DLG = "mat-dialog-container"
ACC = "mat-dialog-actions"
FILA1 = "table tbody tr:has-text('SC-000001')"
FILA2 = "table tbody tr:has-text('SC-000002')"
ALERTA = ".custom-alert-dialog-panel mat-dialog-container"

guion(
    "certificacion-02-administrador",
    "Certificación e-CF · Parte 2: aprobar y confirmar las solicitudes (equipo de Germiva)",
    "Para el equipo de Germiva: dónde llegan las solicitudes del formulario de certificación, qué crea el sistema "
    "solo cuando la IA valida el comprobante (la empresa del contador, su solicitud al Programa de Socios, cada "
    "empresa en prueba con su plan y el cargo de la certificación), qué hace «Confirmar el pago» (firma verificada, "
    "contador vinculado, referidor y referidos, cobro de cada suscripción y Éxito del Cliente), cómo aprobar a mano "
    "un comprobante que la IA no pudo leer y cuándo rechazar.",
    {"sesion": SESION_ADMIN,
     "setup": {"tipo": "shell", "cmd": "python seeds/certificacion/restaurar.py B"}},
    [
        "Encontrar las solicitudes de certificación en Éxito del Cliente",
        "Leer una solicitud: quién la envió, el contador, el comprobante y lo que leyó la IA",
        "Entender todo lo que el sistema crea al recibir el formulario con el comprobante válido",
        "Confirmar el pago y saber qué se crea: firma, vínculos, referidos, cobros y Éxito del Cliente",
        "Aprobar a mano un comprobante que la IA no pudo verificar, y cuándo rechazar",
    ],
    [
        "Confirmar el pago sin haber visto el dinero en el banco: «Validado por IA» no es el estado de cuenta",
        "Aprobar a mano un comprobante sin verificarlo: al aprobarlo se crean las empresas",
        "Desmarcar «Aprobar la firma del contador»: sin firma verificada no se vincula a sus clientes",
        "Rechazar esperando que se borren las empresas: las ya creadas quedan en su prueba",
    ],
    [
        {
            "id": "01-bandeja",
            "capitulo": "La bandeja de solicitudes",
            "rotulo": "Solicitudes de certificación",
            "ruta": "Éxito del Cliente › Solicitudes de certificación",
            "texto_pantalla": "Solicitudes de certificación · lo que llega del formulario público",
            "narracion": (
                "Este video es para el equipo de Germiva que atiende las solicitudes de certificación de "
                "facturación electrónica: las que llegan del formulario público, el de germiva punto com barra "
                "certificación. Cuando llega una, el sistema te avisa en la campanita de notificaciones. Para "
                "verlas entro a Éxito del Cliente y abro Solicitudes de certificación. Esta pantalla solo existe "
                "en la empresa principal, SOFOSY, y la ve quien tiene el permiso. Recojo el panel del menú para "
                "ganar espacio. Cada fila es una solicitud: su número, quién la envió, si es un cliente o un "
                "contador, y su correo; las empresas que trae; el estado del comprobante de pago, revisado por la "
                "inteligencia artificial; la fecha, y el estado de la solicitud. Las dos dicen Validando el pago: "
                "esperan por nosotros. Arriba se filtran por número, estado o tipo de solicitante."
            ),
            "acciones": [
                marca("nav.module-rail", "equipo de Germiva", 4000, cursor=False),
                marca("nav.module-rail [aria-label='Éxito del Cliente']", "las que llegan", 5000, cursor=False),
                marca("app-unified-notification-bell", "la campanita", 3500),
                click("nav.module-rail [aria-label='Éxito del Cliente']", "entro a Éxito del Cliente"),
                click(".panel-item:has-text('Solicitudes de certificación')", "abro Solicitudes"),
                marca("button.gm-company-chip", "SOFOSY", 3500),
                click("button.panel-collapse", "Recojo el panel"),
                marca(FILA1 + " td:nth-child(1)", "su número", 2500),
                marca(FILA1 + " td:nth-child(2)", "quién la envió", 4500),
                marca(FILA1 + " td:nth-child(3)", "las empresas que trae", 3000),
                marca(FILA1 + " td:nth-child(4)", "el estado del comprobante", 4500),
                marca(FILA1 + " td:nth-child(6)", "Validando el pago", 4500),
                marca("app-dynamic-filters", "se filtran", 4000),
            ],
        },
        {
            "id": "02-solicitud",
            "capitulo": "Leer una solicitud",
            "rotulo": "La solicitud de la contadora",
            "ruta": "Solicitudes de certificación › Revisar",
            "texto_pantalla": "Quién la envió · el contador · el comprobante y lo que leyó la IA",
            "narracion": (
                "Abro la de Carolina Méndez con Revisar, al final de su fila. Arriba, el número y el estado. Debajo, "
                "que la envió un contador y que paga por transferencia. Quien la envió: su nombre, su cédula, su "
                "correo y su teléfono. Al lado, el contador: su firma, Méndez Rosario y Asociados. Dice Empresa "
                "creada por la solicitud, porque no estaba en Germiva; trae su exequátur, y Refiere a sus clientes, "
                "o sea, que cobra comisión por ellos. Más abajo, el comprobante de pago: la captura que subió, y lo "
                "que leyó la inteligencia artificial: el monto, la fecha, la referencia, el banco, a quién se le "
                "pagó, y qué tan segura está. Validado por IA, es decir, por la inteligencia artificial, quiere decir que la reconoció como un pago real y "
                "completo. Aun así, antes de confirmar, se comprueba en el banco que el dinero entró."
            ),
            "acciones": [
                click(FILA1 + " td:last-child button", "con Revisar"),
                marca(DLG + " h2", "el número y el estado", 3500, cursor=False),
                marca(DLG + " p.meta", "envió un contador", 4000),
                marca(DLG + " section.box:has(h3:has-text('Quien la envió'))", "Quien la envió", 4500),
                marca(DLG + " section.box:has(h3:has-text('Contador'))", "el contador", 4000),
                marca(DLG + " section.box:has(h3:has-text('Contador')) p.small", "Empresa creada", 7500),
                marca(DLG + " .proof__image", "la captura que subió", 3500),
                marca(DLG + " .proof__data dl", "lo que leyó", 8000),
                marca(DLG + " .proof__data .chip", "Validado por IA", 4500),
                marca(DLG + " .proof__data dd:nth-of-type(1)", "en el banco", 4000),
            ],
        },
        {
            "id": "03-lo-que-se-creo",
            "capitulo": "Lo que se creó al enviar el formulario",
            "rotulo": "Empresas y bitácora",
            "ruta": "Solicitudes de certificación › Revisar › Empresas y bitácora",
            "texto_pantalla": "Empresas de la solicitud · bitácora de pasos automáticos",
            "narracion": (
                "Bajo el comprobante están las empresas. Cada una con su RNC, su plan y su precio; el dueño y su "
                "correo; lo que ya tiene; los días y horas de su prueba de vida, y que el proceso completo lo hace "
                "el equipo, con su cargo de seis mil pesos. Al pie de cada empresa hay cinco estados. Empresa creada "
                "ya está en verde; los otros cuatro esperan a que confirmemos el pago. Y al final, la bitácora de "
                "pasos automáticos: todo lo que el sistema hizo solo, en cuanto la IA validó el comprobante. Uno: "
                "creó la empresa del contador y le envió su acceso. Dos: pidió su ingreso al Programa de Socios con "
                "el exequátur. Tres: creó cada empresa en la prueba del plan elegido, y su dueño recibió el correo "
                "para crear su contraseña. Y cuatro: cargó la certificación en la suscripción de cada empresa, para "
                "su próximo cobro. Nada de esto está pagado todavía: eso lo hace el siguiente paso."
            ),
            "acciones": [
                marca(DLG + " article.company:nth-of-type(1) header", "están las empresas", 4500),
                marca(DLG + " article.company:nth-of-type(1) ul.tags", "lo que ya tiene", 3000),
                marca(DLG + " article.company:nth-of-type(1) ul.tags + p.small", "prueba de vida", 5500),
                marca(DLG + " article.company:nth-of-type(1) ul.states", "cinco estados", 3500),
                marca(DLG + " article.company:nth-of-type(1) ul.states li:first-child", "Empresa creada", 3000),
                marca(DLG + " article.company:nth-of-type(1) ul.states li:nth-child(2)", "los otros cuatro", 3500),
                marca(DLG + " ul.log", "la bitácora", 4000),
                marca(DLG + " ul.log li:nth-child(1)", "Uno", 4000),
                marca(DLG + " ul.log li:nth-child(2)", "Dos", 4000),
                marca(DLG + " ul.log li:nth-child(3)", "Tres", 5500),
                marca(DLG + " ul.log li:nth-child(4)", "Y cuatro", 5000),
                marca(DLG + " ul.log li:last-child", "Nada de esto", 3500),
            ],
        },
        {
            "id": "04-confirmar",
            "capitulo": "Confirmar el pago",
            "rotulo": "Confirmar el pago",
            "ruta": "Solicitudes de certificación › Revisar › Confirmar el pago",
            "texto_pantalla": "Confirmar el pago · qué se registra y qué se crea",
            "narracion": (
                "Ya comprobé en el banco que entraron los treinta y un mil cuatrocientos pesos. Pulso Confirmar el "
                "pago, abajo a la derecha. Se abre un panel que dice lo que va a pasar: se vincula al contador con "
                "sus clientes, se registra al referidor con su veinte por ciento, se cobra cada suscripción con su "
                "plan, y cada empresa entra a la cartera de Éxito del Cliente. Debajo, lo que se registrará como "
                "cobrado, lo que se le pidió y lo que dice el comprobante. El cobro puede ser unos pesos distinto "
                "al precio de lista, porque el primer mes se ajusta al día de facturación. Dos casillas, marcadas: "
                "Registrar el cobro de cada suscripción, que las activa, y Aprobar la firma del contador en el "
                "Programa de Socios; sin firma verificada, el contador no puede quedar vinculado a sus clientes. Hay "
                "un campo de notas, opcional. Ahora pulso el botón azul, Confirmar el pago. Los botones se apagan "
                "mientras el sistema trabaja, una empresa detrás de otra: aprueba la firma, vincula al contador con "
                "cada cliente, registra al referidor, cobra cada suscripción con su factura y pasa cada empresa a "
                "Éxito del Cliente. Con tres empresas toma unos segundos: no cierres la ventana. Al terminar avisa: Pago confirmado; revisa la bitácora, y "
                "si algo quedó pendiente, corrígelo y vuelve a confirmar. Acepto."
            ),
            "acciones": [
                click(ACC + " button:has-text('Confirmar el pago')", "pago, abajo"),
                marca(DLG + " section.box--action > p.small", "lo que va a pasar", 9000),
                marca(DLG + " p.amounts", "registrará como cobrado", 9000),
                marca(DLG + " section.box--action mat-checkbox:nth-of-type(1)", "Registrar el cobro", 3500),
                marca(DLG + " section.box--action mat-checkbox:nth-of-type(2)", "Aprobar la firma", 6000),
                marca(DLG + " section.box--action mat-form-field", "campo de notas", 2500),
                click(ACC + " button.mat-primary:has-text('Confirmar el pago')", "botón azul"),
                marca(ACC, "Los botones se apagan", 5000, cursor=False),
                marca(DLG + " h2", "con cada cliente", 5000, cursor=False),
                # la confirmación tarda 10–18 s según la toma: el aviso se marca en cuanto existe
                marca(ALERTA, None, 9000, cursor=False),
                marca(ALERTA + " button:has-text('Aceptar')", "Al terminar avisa", 4000, cursor=False),
                click(ALERTA + " button:has-text('Aceptar')", "Acepto"),
            ],
        },
        {
            "id": "05-confirmada",
            "capitulo": "Lo que creó la confirmación",
            "rotulo": "Pago confirmado",
            "ruta": "Solicitudes de certificación › Revisar › Bitácora",
            "texto_pantalla": "Pago confirmado · firma, vínculos, referidos, cobros y Éxito del Cliente",
            "narracion": (
                "La solicitud pasó a Pago confirmado, y en cada empresa los cinco estados están en verde. La "
                "bitácora suma lo que hizo la confirmación. La firma quedó verificada en el Programa de Socios, con "
                "el plan Contador sin costo. La firma quedó como contador de cada empresa, con el nivel "
                "Contabilidad: ya puede entrar a trabajar en ellas. El contador quedó dado de alta como referidor, "
                "con el plan del veinte por ciento el primer año, y recibió su acceso al portal. Cada empresa quedó "
                "atribuida a él como referida. El monto del comprobante cubre lo que se pidió. Se registró el cobro "
                "del plan de cada empresa, con la certificación, y su suscripción quedó activa; la factura la emite "
                "SOFOSY a nombre de cada empresa. Y por último, cada empresa entró a la cartera de Éxito del "
                "Cliente con su plan de bienvenida. Y a quien llenó el formulario le llega el correo de confirmación. "
                "Cierro el detalle."
            ),
            "acciones": [
                {"click_opcional": ALERTA + " button:has-text('Aceptar')", "espera_ms": 150},
                marca(DLG + " h2 .chip", None, 3500, cursor=False),
                marca(DLG + " article.company:nth-of-type(1) ul.states", "los cinco estados", 4000),
                marca(DLG + " ul.log li:has-text('Firma verificada')", "La firma quedó verificada", 5000),
                marca(DLG + " ul.log li:has-text('Contador de DISTRIBUIDORA')", "como contador de cada", 6000),
                marca(DLG + " ul.log li:has-text('Referidor')", "dado de alta", 7000),
                marca(DLG + " ul.log li:has-text('Referido DISTRIBUIDORA')", "atribuida", 3500),
                marca(DLG + " ul.log li:has-text('Monto del comprobante')", "El monto", 3500),
                marca(DLG + " ul.log li:has-text('Cobro del plan de DISTRIBUIDORA')", "Se registró el cobro", 8000),
                marca(DLG + " ul.log li:has-text('Éxito del Cliente: DISTRIBUIDORA')", "entró a la cartera", 5000),
                click(ACC + " button:has-text('Cerrar')", "Cierro el detalle"),
            ],
        },
        {
            "id": "06-aprobar-a-mano",
            "capitulo": "Un comprobante sin verificar",
            "rotulo": "Aprobar el comprobante a mano",
            "ruta": "Solicitudes de certificación › Revisar › Aprobar el comprobante",
            "texto_pantalla": "Sin verificar · aprobar el comprobante a mano para crear las empresas",
            "narracion": (
                "En la lista, la primera ya dice Pago confirmado. La otra la envió un dueño, Ramón Guzmán, y su "
                "comprobante dice Sin verificar. Para revisarla, la abro con su botón. Se abre el detalle: subió un "
                "PDF escaneado, y la IA no pudo leerlo; la advertencia de abajo lo dice: revisa el comprobante a "
                "mano. Mientras el comprobante no esté aceptado no se crea nada: la empresa sale pendiente, y "
                "Confirmar el pago está apagado, con el motivo al lado: falta aceptar el comprobante de pago. "
                "Verifico el pago en el banco, y pulso Aprobar el comprobante. El panel avisa: hazlo solo si "
                "verificaste el pago, porque al aprobarlo se crean las empresas. Anoto qué verifiqué: "
                "transferencia vista en el estado de cuenta, que es lo que confirma el pago. Y pulso Aprobar y "
                "crear las empresas. El sistema lo registra, y enseguida sale un aviso: comprobante aprobado, las "
                "empresas se están creando. Acepto."
            ),
            "acciones": [
                {"click_opcional": ACC + " button:has-text('Cerrar')", "espera_ms": 800},
                marca(FILA1 + " td:nth-child(6)", "Pago confirmado", 3000),
                marca(FILA2 + " td:nth-child(4)", "Sin verificar", 4000),
                click(FILA2 + " td:last-child button", "con su botón"),
                marca(DLG + " a.proof__pdf", "PDF escaneado", 3000, cursor=False),
                marca(DLG + " .proof__data p.alert", "la advertencia", 4500),
                marca(DLG + " ul.states li:first-child", "sale pendiente", 3000),
                marca(ACC + " span.blocker", "el motivo al lado", 5000),
                click(ACC + " button:has-text('Aprobar el comprobante')", "pulso Aprobar el comprobante"),
                marca(DLG + " section.box--action", "El panel avisa", 6000),
                escribir(DLG + " section.box--action input", "Transferencia vista en el estado de cuenta", "Anoto"),
                click(ACC + " button:has-text('Aprobar y crear las empresas')", "pulso Aprobar y crear"),
                marca(ALERTA, "sale un aviso", 4500, cursor=False),
                click(ALERTA + " button:has-text('Aceptar')", "Acepto"),
            ],
        },
        {
            "id": "07-creada-y-rechazar",
            "capitulo": "Después de aprobar, y cuándo rechazar",
            "rotulo": "Bitácora y rechazo",
            "ruta": "Solicitudes de certificación › Revisar",
            "texto_pantalla": "Empresa creada · Confirmar el pago se enciende · Rechazar",
            "narracion": (
                "En unos segundos la bitácora muestra lo mismo que vimos en la otra: la empresa, creada en la "
                "prueba de su plan, y el cargo de la certificación en su suscripción. Ahora Confirmar el pago está "
                "encendido, y se confirma igual que la anterior. ¿Y si el pago nunca llegó? Para eso está Rechazar. "
                "Se escribe el motivo, y se lo enviamos por correo a quien llenó el formulario. Ojo: las empresas "
                "ya creadas no se borran; quedan en su prueba. Como este pago sí está, pulso Volver y no la rechazo. "
                "Así se atienden las solicitudes de certificación: revisar, aprobar el comprobante si la IA no "
                "pudo, y confirmar el pago cuando el dinero está en el banco."
            ),
            "acciones": [
                marca(DLG + " ul.log li:nth-child(1)", "la empresa, creada", 4500, cursor=False),
                marca(DLG + " ul.log li:nth-child(2)", "el cargo", 3500),
                marca(ACC + " button:has-text('Confirmar el pago')", "está encendido", 4000),
                click(ACC + " button:has-text('Rechazar')", "Para eso está Rechazar"),
                marca(DLG + " section.box--action textarea", "el motivo", 4500),
                marca(DLG + " section.box--action p.small", "no se borran", 5000),
                click(ACC + " button:has-text('Volver')", "pulso Volver"),
                marca(ACC + " button:has-text('Confirmar el pago')", "confirmar el pago cuando", 4000),
            ],
        },
    ],
    comentario=(
        "Video 2 de la serie Certificación (12/10/2026). setup: restaurar.py B = canon + SC-000001 (contadora, "
        "Validado por IA, 3 empresas creadas por la cola) + SC-000002 (Ramón Guzmán, PDF escaneado, Sin verificar), "
        "enviadas por el formulario real; las notificaciones se atrasan un día para que no salga el aviso emergente "
        "al entrar. La empresa principal local (id 1) se renombró a SOFOSY S.R.L. en canon.sql para que el video "
        "muestre la empresa real del equipo; al terminar la serie se devuelve a «Tienda Germiva»."
    ),
)
