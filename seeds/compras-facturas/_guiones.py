"""Genera los guiones CORTOS de la serie «Compras · Entrada de facturas» (guiones/compras-facturas-NN-*.json), nov. 2026.
    python3 seeds/compras-facturas/_guiones.py
Editar aquí y regenerar. Datos de partida: node seeds/compras-facturas/preparar.mjs A|B (con OPENAI_API_KEY para la IA)."""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "seeds" / "fabricacion"))
from _guiones import COMUN as BASE, clic, marca, teclea  # noqa: E402

COMUN = {**BASE,
         "pronunciacion": {"ITBIS": "itebís", "DGII": "de-ge-i-i", "RNC": "erre-ene-ce", "NCF": "ene-ce-efe",
                           "606": "seis-cero-seis", "IA": "i-a", "PDF": "pe-de-efe", "e-CF": "e-ce-efe",
                           "E31": "e-treinta-y-uno", "B01": "be-cero-uno", "B11": "be-once", "E41": "e-cuarenta-y-uno",
                           "B13": "be-trece", "E43": "e-cuarenta-y-tres", "B17": "be-diecisiete", "E47": "e-cuarenta-y-siete"},
         "privacidad": {"perfil": "ninguno",
                        "permitidos": ["germiva", "130555", "Ferretería", "Cementos", "Pinturas", "Papelería", "Seguridad",
                                       "Lubricantes", "Climatización", "Limpieza", "Mantenimiento", "Ferremateriales", "Ramón"],
                        "mapa_fijo": {"localhost:3001": "api.germiva.com", "localhost:4200": "germiva.com"}}}
SESION = COMUN["sesion"]
BUZON = {**SESION, "navegar": "/purchases/received-invoices", "esperar": "button:has-text('Registrar manual')"}
DLG = "mat-dialog-container"
ALERTA = ".custom-alert-dialog-panel mat-dialog-container"
def tid(x): return f"{DLG} [data-testid='{x}']"
def campo_id(i): return f"{DLG} .fld:has(#{i})"
def fila(texto): return f"table tbody tr:has-text('{texto}')"
def cartel(titulo, texto, decir, ms=6500, tipo="consejo"): return {"cartel": {"tipo": tipo, "titulo": titulo, "texto": texto}, "durante_ms": ms, "al_decir": decir}
def tecla(t, decir): return {"presionar": {"tecla": t}, "al_decir": decir}
def subir(sel, archivo, decir, ancla=None): return {"subir": {"sel": sel, "archivo": archivo, **({"ancla": ancla} if ancla else {})}, "al_decir": decir}
def preparar(e): return {"tipo": "shell", "cmd": f"node seeds/compras-facturas/preparar.mjs {e}"}
SEG = lambda texto: f"{DLG} button.seg__btn:has-text('{texto}')"
PANEL_ITEM = lambda texto: f".panel-item:has-text('{texto}')"

VIDEOS = {}

# ───────────────────────── 01 · Por dónde entra cada factura ─────────────────────────
VIDEOS["compras-facturas-01-por-donde-entra"] = {
    "titulo": "Compras · Entrada de facturas 1: por dónde entra cada factura",
    "descripcion": "Primer video de la serie de entrada de facturas de compra en Germiva ERP. Una sola pregunta decide la pantalla: ¿quién emitió el comprobante? Vemos el buzón de facturas recibidas, sus cuatro puertas de entrada, el listado de Facturas y cuándo se usa «Nueva Factura».",
    "_comentario": "Serie Compras · Entrada de facturas (nov. 2026), video 1. Estado B (preparar.mjs B): buzón con las dos facturas de la plantilla con entrada (Lubricantes y Climatización, origen Manual), y pendientes los tres e-CF del reporte de la DGII (Limpieza ×2 y Mantenimiento) y la de Ferremateriales leída con IA. No crea nada.",
    "sesion": {**SESION, "navegar": "/purchases/received-invoices", "esperar": "button:has-text('Registrar manual')"},
    "setup": preparar("B"),
    "aprenderas": ["La pregunta que decide la pantalla: ¿quién emitió el comprobante?", "Las cuatro formas de que una factura llegue al buzón", "Qué significa «Pendiente» y «Con entrada»", "Cuándo se usa «Nueva Factura» y el listado único de Facturas"],
    "errores_comunes": ["Registrar en «Nueva Factura» un crédito fiscal que te entregó el proveedor: va al buzón", "Creer que una factura del buzón ya es una compra: hasta darle entrada no tiene asiento ni deuda", "Registrar dos veces la factura de una mercancía ya recibida: se coteja contra la recepción"],
    "pasos": [
        {
            "id": "01-pregunta", "capitulo": "Quién emitió el comprobante", "rotulo": "Por dónde entra",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "En Germiva, una factura de compra puede entrar de varias formas, y una sola pregunta decide por dónde: ¿quién emitió el comprobante? Si te lo entregó el proveedor, como un crédito fiscal, va a Facturas Recibidas, que es esta pantalla: el buzón de Compras. Cada fila es una factura de un proveedor. Mientras está pendiente, todavía no es una compra: no tiene asiento ni deuda. Lo es cuando alguien le da entrada.",
            "acciones": [
                cartel("En este video", "Por dónde entra cada factura de compra, según quién emitió el comprobante.", "una sola pregunta", 7000),
                marca(PANEL_ITEM("Facturas Recibidas"), "va a Facturas Recibidas", 3000),
                marca(fila("E310000004512") + " td:nth-child(2)", "Cada fila", 3000),
                marca(fila("E310000004512") + " td:has-text('Pendiente')", "está pendiente", 2500),
                marca(fila("E310000002201") + " td:has-text('Con entrada')", "le da entrada", 3000),
            ],
        },
        {
            "id": "02-puertas", "capitulo": "Las puertas del buzón", "rotulo": "Las puertas del buzón",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "Al buzón se llega por cuatro puertas. Importar con IA: subes la foto o el PDF y el sistema lee la factura; también llegan así las que envías por el WhatsApp de Germiva. Registrar manual, para copiar una factura de papel. Importar y exportar: una plantilla de Excel con muchas facturas, o el reporte de comprobantes recibidos que bajas de la DGII. Y la cuarta: el comprobante electrónico que el proveedor te envía entra solo. El filtro Origen dice por cuál llegó cada una.",
            "acciones": [
                clic("button.panel-collapse", "cuatro puertas"),
                marca("button:has-text('Importar con IA')", "Importar con IA", 5500),
                marca("button:has-text('Registrar manual')", "Registrar manual", 3000),
                marca("button:has-text('Importar / Exportar')", "Importar y exportar", 5500),
                marca(fila("E310000004512") + " td:has-text('Reporte DGII')", "el reporte de comprobantes", 2500),
                marca("mat-form-field:has(mat-label:has-text('Origen'))", "El filtro Origen", 2500),
                marca("table thead th:has-text('Origen')", "por cuál llegó", 3500),
            ],
        },
        {
            "id": "03-propios", "capitulo": "Comprobantes que emite tu empresa", "rotulo": "Nueva Factura",
            "ruta": "Compras › Facturas", "navegar": "/purchases/invoices", "al_decir_navegar": "Facturas",
            "narracion": "¿Y si el comprobante lo emite tu empresa? Entonces se registra en Compras, Facturas. Aquí está el listado único de compras: todas aparecen en él, entren por donde entren. Nueva Factura es solo para los tres comprobantes que numera tu empresa: el de compras a un proveedor informal, el de gastos menores y el de pagos al exterior. Por eso no tiene campo para el NCF: lo pone tu secuencia.",
            "acciones": [
                marca(fila("E310000002201"), "el listado único", 4000),
                marca("button:has-text('Nueva Factura')", "Nueva Factura es solo", 9000),
            ],
        },
        {
            "id": "04-recepcion", "capitulo": "Mercancía ya recibida", "rotulo": "Desde la recepción",
            "ruta": "Compras › Recepciones", "navegar": "/purchases/receipts", "al_decir_navegar": "Recepciones",
            "narracion": "Un caso más: si la mercancía llegó con una orden de compra y ya la recibiste, la factura se registra desde Recepciones, cotejándola contra lo que entró al almacén. Así el costo no se carga dos veces. En los próximos videos vemos cada forma, paso a paso: a mano, con IA, con plantilla, con el reporte de la DGII, desde la recepción y con los comprobantes propios.",
            "acciones": [
                marca(fila("REC-2026-000001") + " td:nth-child(1)", "ya la recibiste", 2500),
                marca(fila("REC-2026-000001") + " td:has-text('Completada')", "cotejándola", 3000),
                cartel("Regla", "¿Lo emitió el proveedor? Buzón. ¿Lo emite tu empresa? Nueva Factura. ¿Ya recibiste la mercancía? Desde la recepción.", "En los próximos videos", 9000),
            ],
        },
    ],
}

# ───────────────────────── 02 · Registrar a mano por totales ─────────────────────────
NCF2 = "E310000000845"
VIDEOS["compras-facturas-02-manual-por-totales"] = {
    "titulo": "Compras · Entrada de facturas 2: registrar a mano, por totales",
    "descripcion": "Segundo video de la serie de entrada de facturas de compra en Germiva ERP. Registramos a mano una factura de papel copiando solo su pie: subtotal, ITBIS y total. El proveedor, la categoría 606, el plazo y la cuenta de gasto salen de su ficha, y antes de guardar ves el asiento y el 606.",
    "_comentario": f"Serie Compras · Entrada de facturas (nov. 2026), video 2. Estado A. Seguridad Germiva del Caribe (RNC 130555109, plazo 30, categoría 02, cuenta 6.03.04 Vigilancia y seguridad). NCF {NCF2}, emisión 15/11/2026, crédito 30 días; subtotal 25,000, ITBIS 4,500, total 29,500.",
    "sesion": BUZON, "setup": preparar("A"),
    "aprenderas": ["Abrir la captura manual y sus tres partes", "Elegir el proveedor y aprovechar su ficha: categoría 606, plazo y cuenta", "Copiar el pie de la factura por totales", "Leer el asiento y el 606 antes de dar entrada", "Guardar borradores para registrar varias facturas"],
    "errores_comunes": ["Escribir el subtotal después del descuento: va el de antes", "Dejar la categoría 606 vacía: la compra sale incompleta en el 606", "Registrar al contado una factura a crédito: no nace la cuenta por pagar"],
    "pasos": [
        {
            "id": "01-abrir", "capitulo": "La captura manual", "rotulo": "Registrar manual",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "Tenemos en la mano una factura de papel de la compañía de vigilancia, y la vamos a registrar en el buzón de facturas recibidas. Pulso Registrar manual. La captura tiene tres partes numeradas: proveedor y comprobante, condiciones de pago y montos. Y a la derecha, el resumen, el asiento que se va a generar y lo que pide el 606, que se actualizan mientras escribo.",
            "acciones": [
                clic("button:has-text('Registrar manual')", "Pulso Registrar manual"),
                marca(f"{DLG} section[aria-labelledby='entry-sec-1'] .entry-section__title", "tres partes", 2000, cursor=False),
                marca(f"{DLG} section[aria-labelledby='entry-sec-2'] .entry-section__title", "condiciones de pago", 1500, cursor=False),
                marca(f"{DLG} section[aria-labelledby='entry-sec-3'] .entry-section__title", "montos", 1500, cursor=False),
                marca(f"{DLG} .entry-rail section[aria-labelledby='entry-summary-title']", "a la derecha", 6000, cursor=False),
            ],
        },
        {
            "id": "02-proveedor", "capitulo": "Proveedor y comprobante", "rotulo": "Proveedor y comprobante",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "Empiezo por el proveedor. Escribo seguridad, y en la lista aparece Seguridad Germiva del Caribe; la elijo. Debajo queda su RNC, tomado de la ficha. Si no existiera, desde este mismo campo lo tomas del padrón de la DGII o lo creas. El tipo de comprobante viene en crédito fiscal. En NCF copio el número tal como viene en la factura. La fecha de emisión: quince de noviembre. Y fíjate en la categoría 606: ya vino de la ficha del proveedor.",
            "acciones": [
                teclea(f"{DLG} app-partner-document-select input", "Seguridad", "Escribo seguridad"),
                clic("mat-option:has-text('Seguridad Germiva')", "la elijo"),
                marca(tid("supplier-rnc"), "su RNC", 3500),
                marca(campo_id("f-ncf-type"), "El tipo de comprobante", 2500),
                teclea("#f-ncf", NCF2, "En NCF copio"),
                teclea("#f-issue", "15/11/2026", "La fecha de emisión"),
                marca(campo_id("f-606"), "la categoría 606", 4500),
            ],
        },
        {
            "id": "03-condiciones", "capitulo": "Condiciones de pago", "rotulo": "Condiciones de pago",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "Segundo, las condiciones de pago. Esta factura es a crédito. El plazo ya dice treinta días, porque así está en la ficha del proveedor, y la fecha límite se calculó sola: emisión más plazo. Con esto, al dar entrada nace la cuenta por pagar.",
            "acciones": [
                marca(SEG("Crédito"), "es a crédito", 2500),
                marca(campo_id("f-days"), "treinta días", 3500),
                marca(campo_id("f-due"), "la fecha límite", 5000),
            ],
        },
        {
            "id": "04-montos", "capitulo": "Montos por totales", "rotulo": "Montos por totales",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "Tercero, los montos. La captura abre por totales: copio el pie de la factura, sin desglosar productos. En concepto escribo qué se compró. La cuenta de gasto también la propone la ficha del proveedor: vigilancia y seguridad. Ahora el pie. Subtotal: veinticinco mil. ITBIS facturado: cuatro mil quinientos, y al lado confirma que es el dieciocho por ciento del gravado. Y el total de la factura: veintinueve mil quinientos. El sistema lo compara con el total calculado, y cuadra.",
            "acciones": [
                marca(tid("mode-totals"), "abre por totales", 3000),
                teclea(tid("totals-concept"), "Servicio de vigilancia de noviembre", "En concepto escribo"),
                marca(f"{DLG} .fld:has([data-testid='totals-account'])", "La cuenta de gasto", 4000),
                teclea(tid("totals-subtotal"), "25000", "Subtotal"),
                teclea(tid("totals-itbis"), "4500", "ITBIS facturado"),
                marca(tid("itbis-hint"), "dieciocho por ciento", 3000),
                teclea(tid("totals-document-total"), "29500", "el total de la factura"),
                marca(f"{DLG} .fld:has([data-testid='totals-document-total'])", "y cuadra", 3000),
            ],
        },
        {
            "id": "05-dar-entrada", "capitulo": "Asiento, 606 y dar entrada", "rotulo": "Dar entrada",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "Antes de guardar, mira la derecha. El resumen cuadra con la factura del proveedor. En el asiento, el gasto de vigilancia y el ITBIS por adelantar van al débito, y la cuenta por pagar al proveedor, al crédito. Y la lista del 606 está completa. Si todavía no la vas a registrar, Guardar borrador la deja pendiente, y Borrador y otra abre una captura en blanco para la siguiente. Esta está lista: pulso Dar entrada. El sistema crea la factura, su asiento y la cuenta por pagar. El aviso confirma que se creó la factura de compra, y acepto. La fila queda con entrada, con su número de factura.",
            "acciones": [
                marca(tid("summary-status"), "El resumen cuadra", 3000, cursor=False),
                marca(f"{DLG} .entry-rail .journal", "En el asiento", 7000, cursor=False),
                marca(f"{DLG} .entry-rail ul.checks", "la lista del 606", 2500, cursor=False),
                marca(tid("save-draft"), "Guardar borrador", 3000),
                marca(f"{DLG} button:has-text('Borrador y otra')", "Borrador y otra", 3500),
                clic(tid("submit-entry"), "pulso Dar entrada"),
                marca(ALERTA, "El aviso confirma", 2500, cursor=False),
                clic(f"{ALERTA} button:has-text('Aceptar')", "y acepto"),
                marca(fila(NCF2) + " td:has-text('Con entrada')", "La fila queda", 4000, cursor=False),
            ],
        },
    ],
}

# ───────────────────────── 03 · Registrar a mano por líneas, al contado ─────────────────────────
NCF3 = "E310000001290"
VIDEOS["compras-facturas-03-manual-por-lineas"] = {
    "titulo": "Compras · Entrada de facturas 3: por líneas y al contado",
    "descripcion": "Tercer video de la serie de entrada de facturas de compra en Germiva ERP. Registramos una factura pagada en el momento, detallando cada artículo: una línea gravada al 18 % y otra exenta. Vemos el método de pago, el ITBIS de cada línea y por qué una compra al contado no deja cuenta por pagar.",
    "_comentario": f"Serie Compras · Entrada de facturas (nov. 2026), video 3. Estado A. Papelería Germiva (RNC 130555125, categoría 09, sin plazo). NCF {NCF3}, emisión 18/11/2026, contado por transferencia. Líneas: 10 Resma de papel 8.5 x 11 a 285 (18 %, ITBIS 513) y 2 Libro de registro contable a 450 (exento). Subtotal 3,750, ITBIS 513, total 4,263.",
    "sesion": BUZON, "setup": preparar("A"),
    "aprenderas": ["Registrar al contado y elegir el método de pago", "Cambiar a la captura por líneas", "Poner la tasa de ITBIS de cada línea, incluida una exenta", "Por qué la compra al contado nace pagada y sin cuenta por pagar"],
    "errores_comunes": ["Registrar después otro pago para una compra que entró al contado: ya está pagada", "Escribir a mano el ITBIS de una línea cuando la tasa lo calcula", "Dejar gravada una línea que la factura trae exenta"],
    "pasos": [
        {
            "id": "01-proveedor", "capitulo": "Proveedor y contado", "rotulo": "Al contado",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "Esta vez la factura es de la papelería, y la pagamos en el momento, por transferencia. Pulso Registrar manual. Busco el proveedor: escribo papelería y lo elijo. Copio el NCF y la fecha de emisión: dieciocho de noviembre. En condiciones de pago, elijo contado. Desaparecen el plazo y la fecha límite, y aparece el método de pago: lo abro y elijo transferencia bancaria. Y en caja o banco, la cuenta de donde salió el dinero: el banco. Al contado, la factura nace pagada y no deja cuenta por pagar.",
            "acciones": [
                clic("button:has-text('Registrar manual')", "Pulso Registrar manual"),
                teclea(f"{DLG} app-partner-document-select input", "Papeler", "escribo papelería"),
                clic("mat-option:has-text('Papelería Germiva')", "lo elijo"),
                teclea("#f-ncf", NCF3, "Copio el NCF"),
                teclea("#f-issue", "18/11/2026", "dieciocho de noviembre"),
                clic(SEG("Contado"), "elijo contado"),
                clic("#f-method", "lo abro"),
                clic("mat-option:has-text('Transferencia')", "transferencia bancaria"),
                clic(f"{DLG} input[placeholder*='de cuál sale']", "Y en caja o banco"),
                clic("mat-option:has-text('Banco 1')", "el banco"),
                marca(campo_id("f-method"), "nace pagada", 4000),
            ],
        },
        {
            "id": "02-lineas", "capitulo": "Por líneas", "rotulo": "Por líneas",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "Ahora los montos. Quiero detallar cada artículo, así que paso a por líneas. En la primera línea escribo la descripción: resma de papel. Cantidad: diez. Precio: doscientos ochenta y cinco. Como es la primera compra a este proveedor, la tasa y el tipo vienen sugeridos para que los confirmes. El tipo, bien, está correcto. La tasa la abro y elijo el dieciocho por ciento, y el ITBIS sale calculado, en gris: quinientos trece. Agrego otra línea para los libros de registro: dos, a cuatrocientos cincuenta. Estos no llevan ITBIS, así que abro la tasa y elijo exento.",
            "acciones": [
                clic(tid("mode-lines"), "paso a por líneas"),
                teclea(f"{DLG} input[formcontrolname='description'] >> nth=0", "Resma de papel 8.5 x 11", "escribo la descripción"),
                teclea(f"{DLG} input[formcontrolname='quantity'] >> nth=0", "10", "Cantidad"),
                teclea(f"{DLG} input[formcontrolname='unitPrice'] >> nth=0", "285", "Precio"),
                marca(f"{DLG} mat-select[formcontrolname='goodOrServiceIndicator'] >> nth=0", "El tipo, bien", 2500),
                clic(f"{DLG} mat-select[formcontrolname='taxRateCode'] >> nth=0", "La tasa la abro"),
                clic("mat-option:has-text('ITBIS 18%')", "dieciocho por ciento"),
                marca(tid("line-tax-0"), "sale calculado", 3500),
                clic(f"{DLG} button:has-text('Agregar línea')", "Agrego otra línea"),
                teclea(f"{DLG} input[formcontrolname='description'] >> nth=1", "Libro de registro contable", "libros de registro"),
                teclea(f"{DLG} input[formcontrolname='quantity'] >> nth=1", "2", "dos"),
                teclea(f"{DLG} input[formcontrolname='unitPrice'] >> nth=1", "450", "cuatrocientos cincuenta"),
                clic(f"{DLG} mat-select[formcontrolname='taxRateCode'] >> nth=1", "abro la tasa"),
                clic("mat-option:has-text('Exento')", "elijo exento"),
            ],
        },
        {
            "id": "03-dar-entrada", "capitulo": "Resumen y dar entrada", "rotulo": "Dar entrada",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "A la derecha, el resumen separa lo exento de lo gravado, con su ITBIS, y el total: cuatro mil doscientos sesenta y tres. En el 606, una compra de bienes con su ITBIS por adelantar. Pulso Dar entrada. El sistema registra la compra y, en el mismo paso, su pago. El aviso confirma la factura, y acepto. En el buzón queda con entrada, y en Compras, Facturas, ya aparece pagada. Un detalle: no le registres otro pago, porque ya se registró al dar entrada.",
            "acciones": [
                marca(f"{DLG} .entry-rail section[aria-labelledby='entry-summary-title']", "el resumen separa", 6000, cursor=False),
                marca(f"{DLG} .entry-rail ul.checks", "En el 606", 3500, cursor=False),
                clic(tid("submit-entry"), "Pulso Dar entrada"),
                marca(ALERTA, "El aviso confirma", 2000, cursor=False),
                clic(f"{ALERTA} button:has-text('Aceptar')", "y acepto"),
                marca(fila(NCF3) + " td:has-text('Con entrada')", "queda con entrada", 3000),
                cartel("Cuidado", "Una compra al contado ya está pagada: no le registres otro pago.", "Un detalle", 6500, "cuidado"),
            ],
        },
    ],
}

# ───────────────────────── 04 · Importar con IA ─────────────────────────
NCF4 = "E310002458319"
VIDEOS["compras-facturas-04-importar-con-ia"] = {
    "titulo": "Compras · Entrada de facturas 4: importar con IA",
    "descripcion": "Cuarto video de la serie de entrada de facturas de compra en Germiva ERP. Subimos la foto de una factura, la IA la lee en segundos y la revisamos al lado del documento original antes de darle entrada. El proveedor que no existe se crea solo con su RNC.",
    "_comentario": f"Serie Compras · Entrada de facturas (nov. 2026), video 4. Estado A + credencial OpenAI (gpt-4.1-mini) en la base local. Foto: seeds/compras-facturas/factura-ferremateriales.jpg (Ferremateriales Germiva, RNC 130555117, sin ficha; {NCF4}, 18/11/2026, crédito 30 días; 10 tubos a 185, 4 pegamentos a 450, 20 codos a 25; subtotal 4,150, ITBIS 747, total 4,897).",
    "sesion": BUZON, "setup": preparar("A"),
    "aprenderas": ["Subir fotos o PDF de facturas con «Importar con IA»", "Revisar lo leído al lado del documento original", "Qué pasa cuando el proveedor no está registrado", "Dar entrada a la factura revisada"],
    "errores_comunes": ["Dar entrada sin revisar: la IA puede equivocarse y quien da entrada responde por los datos", "Esperar que la IA adivine el destino del ITBIS: viene en «por adelantar»", "Subir dos veces la misma factura: el sistema avisa el NCF repetido"],
    "pasos": [
        {
            "id": "01-subir", "capitulo": "Subir la foto", "rotulo": "Importar con IA",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "La forma más rápida: dejar que la IA lea la factura. Pulso Importar con IA. Arriba, un aviso importante: la IA puede equivocarse, y quien da entrada debe verificar los datos. Debajo, tu cupo de IA. Arrastro aquí la foto de la factura, o la selecciono; puedes poner hasta veinte en la cola, en foto o en PDF. Pulso Procesar con IA, y en unos segundos la factura está leída: ya dice el proveedor, el NCF y el total. Cierro, y en el buzón aparece pendiente, con origen IA.",
            "acciones": [
                clic("button:has-text('Importar con IA')", "Pulso Importar con IA"),
                marca(f"{DLG} .gm-dialog-alert--warning, {DLG} .gm-dialog-alert", "un aviso importante", 4500, cursor=False),
                marca(f"{DLG} .quota", "tu cupo", 2000, cursor=False),
                subir(f"{DLG} input[type=file]", "seeds/compras-facturas/factura-ferremateriales.jpg", "o la selecciono", ancla=f"{DLG} .dropzone, {DLG} [class*='drop']"),
                clic(f"{DLG} button:has-text('Procesar')", "Pulso Procesar con IA"),
                marca(f"{DLG} li:has-text('factura-ferremateriales'), {DLG} [class*='queue'] :text('factura-ferremateriales')", "ya dice el proveedor", 4500, cursor=False),
                clic(f"{DLG} button:has-text('Cerrar')", "Cierro"),
                marca(fila("FERREMATERIALES") + " td:has-text('Pendiente')", "aparece pendiente", 3500),
            ],
        },
        {
            "id": "02-revisar", "capitulo": "Revisar contra el original", "rotulo": "La revisión",
            "ruta": "Compras › Facturas Recibidas › Dar entrada",
            "narracion": "Ahora la reviso. Pulso Dar entrada, revisión, y amplío la ventana a pantalla completa. A la izquierda está el documento original, con zoom y giro, para cotejar cada dato. A la derecha, lo que leyó la IA, en las mismas tres partes de la captura manual. Este proveedor no está registrado: el aviso dice que al dar entrada se crea con este nombre y este RNC, así que verifico el RNC contra la factura. El NCF y la fecha coinciden. La categoría 606 la confirmo yo: abro la lista y elijo compras que forman parte del costo de venta. La condición dice crédito treinta días, y la IA puso el plazo y la fecha límite.",
            "acciones": [
                clic(fila("FERREMATERIALES") + " button[aria-label='Dar entrada (revisión)']", "Pulso Dar entrada"),
                clic(f"{DLG} button:has(mat-icon:text-is('fullscreen'))", "pantalla completa"),
                marca(f"{DLG} .document-pane", "el documento original", 4500, cursor=False),
                marca(f"{DLG} .form-pane", "lo que leyó la IA", 3000, cursor=False),
                marca(f"{DLG} .gm-dialog-alert:has-text('no corresponde')", "no está registrado", 6000, cursor=False),
                marca(campo_id("f-rnc"), "verifico el RNC", 2500),
                marca(campo_id("f-ncf"), "El NCF", 1800),
                marca(campo_id("f-issue"), "la fecha", 1800),
                clic("#f-606", "abro la lista"),
                clic("mat-option:has-text('09')", "compras que forman parte"),
                marca(campo_id("f-days"), "puso el plazo", 3500),
            ],
        },
        {
            "id": "03-lineas-entrada", "capitulo": "Líneas y dar entrada", "rotulo": "Dar entrada",
            "ruta": "Compras › Facturas Recibidas › Dar entrada",
            "narracion": "Bajo a los montos. La IA leyó las tres líneas, con su cantidad, su precio y su ITBIS al dieciocho por ciento, y el resumen dice que cuadra con el total del documento. Revisa también el tipo de cada línea: son tubos, pegamento y codos, así que todas deben decir bien, y así las leyó la IA. Si la factura fuera de mercancía que debe entrar al almacén, aquí marcarías mercancía por recibir en cada línea. Todo coincide: pulso Dar entrada. El sistema crea el proveedor nuevo y la factura, en un solo paso. Se creó la factura. Acepto.",
            "acciones": [
                marca(f"{DLG} section[aria-labelledby='entry-sec-3']", "las tres líneas", 5500, cursor=False),
                marca(tid("summary-status"), "dice que cuadra", 3500, cursor=False),
                marca(f"{DLG} mat-select[formcontrolname='goodOrServiceIndicator'] >> nth=2", "todas deben decir bien", 4000),
                marca(f"{DLG} mat-slide-toggle.line-goods-toggle >> nth=2", "mercancía por recibir", 4000),
                clic(tid("submit-entry"), "pulso Dar entrada"),
                marca(ALERTA, "Se creó la factura", 3000, cursor=False),
                clic(f"{ALERTA} button:has-text('Aceptar')", "Acepto"),
            ],
        },
    ],
}

# ───────────────────────── 05 · Plantilla de Excel y entrada por lote ─────────────────────────
VIDEOS["compras-facturas-05-plantilla-y-lote"] = {
    "titulo": "Compras · Entrada de facturas 5: plantilla de Excel y entrada por lote",
    "descripcion": "Quinto video de la serie de entrada de facturas de compra en Germiva ERP. Cargamos varias facturas de una vez con la plantilla de Excel del buzón y les damos entrada en lote, con una sola confirmación.",
    "_comentario": "Serie Compras · Entrada de facturas (nov. 2026), video 5. Estado A. Archivo seeds/compras-facturas/facturas-plantilla.xlsx (archivos.py): F-1 Lubricantes Germiva (130555133) E310000002201, dos renglones (6 aceite a 1,150 + 2 filtros a 475; ITBIS 1,413; total 9,263); F-2 Climatización Germiva (130555141) E310000088410 (4,200 + 756 = 4,956).",
    "sesion": BUZON, "setup": preparar("A"),
    "aprenderas": ["Descargar la plantilla del buzón y cómo se llena", "Importar el archivo: las facturas quedan pendientes", "Dar entrada a varias facturas en lote", "Cuándo una factura no entra por lote"],
    "errores_comunes": ["Dejar una fila con errores: si una falla, no se importa ninguna", "Dar entrada por lote a documentos sin verificar", "Usar claves distintas para los renglones de una misma factura"],
    "pasos": [
        {
            "id": "01-plantilla", "capitulo": "La plantilla", "rotulo": "Importar / Exportar",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "Cuando tienes muchas facturas, por ejemplo las que te pasa tu contador en una hoja de cálculo, las cargas de una vez. Pulso Importar y exportar. Primero descargas la plantilla, en Excel o en CSV: una fila por renglón de factura, y la misma clave agrupa los renglones de una factura. Trae instrucciones y un ejemplo. Ya la llené con dos facturas: una de lubricantes con dos renglones y otra de climatización.",
            "acciones": [
                clic("button:has-text('Importar / Exportar')", "Pulso Importar y exportar"),
                marca(f"{DLG} button:has-text('Plantilla Excel')", "descargas la plantilla", 5500),
                cartel("La plantilla", "Factura · RNC · Proveedor · NCF · Tipo · Fecha · Concepto · Cantidad · Precio · ITBIS", "Trae instrucciones", 8000),
            ],
        },
        {
            "id": "02-importar", "capitulo": "Importar el archivo", "rotulo": "Importar el archivo",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "Más abajo, en importar el archivo, subo la plantilla llena. El sistema valida todas las filas antes de crear nada: si una tiene errores, no se importa ninguna, y te dice cuál corregir. Aquí todo estaba bien: dos facturas creadas, pendientes para revisión. Cierro, y ahí están en el buzón, pendientes.",
            "acciones": [
                subir(f"{DLG} input[type=file]", "seeds/compras-facturas/facturas-plantilla.xlsx", "subo la plantilla", ancla=f"{DLG} button:has-text('Elegir'), {DLG} button:has-text('Seleccionar'), {DLG} [class*='drop'], {DLG} button:has-text('Subir')"),
                marca(f"{DLG} .gm-dialog-alert--success, {DLG} .gm-dialog-alert:has-text('creada')", "dos facturas creadas", 4000, cursor=False),
                clic(f"{DLG} button:has-text('Cerrar') >> nth=-1", "Cierro"),
                marca(fila("E310000002201") + " td:nth-child(2)", "ahí están", 2500),
            ],
        },
        {
            "id": "03-lote", "capitulo": "Dar entrada en lote", "rotulo": "Entrada por lote",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "Como ya las verifiqué en la hoja, les doy entrada juntas. Recojo el panel para ver mejor, y marco las dos filas. Arriba aparece el botón Dar entrada, con la cantidad marcada; lo pulso, y confirmo. El sistema crea una factura de compra por cada fila, una tras otra, con su asiento y su cuenta por pagar. Listo: las dos facturas entraron, cada una con su número. Ojo: el lote usa los datos tal como vinieron. Una factura que necesita una decisión, como una nota de crédito o una mercancía ya recibida, no entra por lote: ábrela con la revisión.",
            "acciones": [
                clic("button.panel-collapse", "Recojo el panel"),
                clic(fila("E310000002201") + " input[type=checkbox]", "marco las dos"),
                clic(fila("E310000088410") + " input[type=checkbox]", "las dos filas"),
                clic("button:has-text('Dar entrada (')", "lo pulso"),
                clic(f"{DLG} button:has-text('Sí, dar entrada')", "y confirmo"),
                marca(ALERTA, "Listo", 2500, cursor=False),
                clic(f"{ALERTA} button:has-text('Aceptar')", "las dos facturas entraron"),
                marca(fila("E310000002201") + " td:has-text('Con entrada')", "cada una con su número", 3000),
                cartel("Cuidado", "El lote usa los datos tal como vinieron: úsalo solo con documentos verificados.", "Ojo", 7000, "cuidado"),
            ],
        },
    ],
}

# ───────────────────────── 06 · Reporte de e-CF recibidos de la DGII ─────────────────────────
VIDEOS["compras-facturas-06-reporte-dgii"] = {
    "titulo": "Compras · Entrada de facturas 6: el reporte de e-CF recibidos de la DGII",
    "descripcion": "Sexto video de la serie de entrada de facturas de compra en Germiva ERP. Subimos el reporte de comprobantes electrónicos recibidos que se descarga de la Oficina Virtual de la DGII: el sistema lo lee sin IA, crea una factura pendiente por comprobante y conserva los montos que la DGII tiene registrados.",
    "_comentario": "Serie Compras · Entrada de facturas (nov. 2026), video 6. Estado A. Archivo seeds/compras-facturas/reporte-dgii-ecf-recibidos.xlsx (archivos.py): Limpieza Germiva (130555151) E310000004512 (2,124 / 324) y E310000004530 (1,416 / 216); Mantenimiento Germiva (130555168) E310000000981 (8,260 / 1,260). Receptor 130555001. Se da entrada por revisión a la de Mantenimiento con categoría 02 y emisión del día de recepción.",
    "sesion": BUZON, "setup": preparar("A"),
    "aprenderas": ["Qué es el reporte de e-CF recibidos y dónde se sube", "Qué hace el sistema con cada comprobante del reporte", "Qué datos quedan fijos y cuáles completas tú", "Dar entrada a un comprobante del reporte"],
    "errores_comunes": ["Cambiar el total o el ITBIS: son los que la DGII tiene registrados y cruzarán con tu 606", "Subir el reporte desde una sucursal: se importa desde la casa matriz", "Dar entrada por lote a un comprobante en otra moneda: va por la revisión"],
    "pasos": [
        {
            "id": "01-subir", "capitulo": "Subir el reporte", "rotulo": "Reporte de la DGII",
            "ruta": "Compras › Facturas Recibidas",
            "narracion": "En la Oficina Virtual de la DGII puedes descargar el reporte de los comprobantes electrónicos que te emitieron tus proveedores. Ese archivo se sube aquí mismo. Pulso Importar y exportar, y lo subo, tal como lo bajé. El sistema lo reconoce solo, lo lee sin IA y sin gastar cupo. Leyó tres comprobantes, los tres pasaron al buzón, y avisa de los proveedores nuevos: se crean con la razón social del padrón al darle entrada a su primera factura.",
            "acciones": [
                clic("button:has-text('Importar / Exportar')", "Pulso Importar y exportar"),
                subir(f"{DLG} input[type=file]", "seeds/compras-facturas/reporte-dgii-ecf-recibidos.xlsx", "y lo subo", ancla=f"{DLG} button:has-text('Elegir'), {DLG} button:has-text('Seleccionar'), {DLG} [class*='drop'], {DLG} button:has-text('Subir')"),
                marca(f"{DLG} .gm-dialog-facts, {DLG} app-dgii-report-summary", "Leyó tres comprobantes", 4500, cursor=False),
                marca(f"{DLG} app-dgii-report-summary :text('PROVEEDORES NUEVOS'), {DLG} :text('Proveedores nuevos')", "los proveedores nuevos", 5500, cursor=False),
            ],
        },
        {
            "id": "02-revisar", "capitulo": "Lo que queda fijo", "rotulo": "Revisión del comprobante",
            "ruta": "Compras › Facturas Recibidas › Dar entrada",
            "narracion": "Cierro. Los tres quedaron pendientes, con origen reporte DGII. Abro la revisión del de mantenimiento. El e-NCF, el RNC, el total y el ITBIS son los que la DGII tiene registrados, y no se cambian: son los que van a cruzar con tu 606. El reporte no trae la fecha de emisión ni el detalle, así que eso lo confirmas tú. Elijo la categoría 606: gastos por trabajos, suministros y servicios. Y como es a crédito, escribo el plazo, treinta días, y la fecha límite se calcula sola.",
            "acciones": [
                clic(f"{DLG} button:has-text('Cerrar') >> nth=-1", "Cierro"),
                marca(fila("E310000000981") + " td:has-text('Reporte DGII')", "origen reporte DGII", 2500),
                clic(fila("E310000000981") + " button[aria-label='Dar entrada (revisión)']", "Abro la revisión"),
                marca(f"{DLG} .gm-dialog-facts, {DLG} .gm-dialog-note", "no se cambian", 6000, cursor=False),
                marca(campo_id("f-issue"), "la fecha de emisión", 4000),
                clic("#f-606", "Elijo la categoría"),
                clic("mat-option:has-text('02')", "gastos por trabajos"),
                teclea("#f-days", "30", "escribo el plazo"),
                marca(campo_id("f-due"), "la fecha límite", 2500),
            ],
        },
        {
            "id": "03-entrada", "capitulo": "Dar entrada", "rotulo": "Dar entrada",
            "ruta": "Compras › Facturas Recibidas › Dar entrada",
            "narracion": "Al dar entrada, el total y el ITBIS tienen que coincidir con los de la DGII; aquí cuadran. Pulso Dar entrada. El sistema registra al proveedor con su nombre del padrón y crea la factura. Se creó la factura. Acepto. Los otros dos puedes revisarlos igual, o marcarlos y darles entrada por lote. Y la pestaña Cuadre con la DGII compara tu 606 con lo que la DGII tiene, para que no se te escape ninguno.",
            "acciones": [
                marca(tid("summary-status"), "aquí cuadran", 3000, cursor=False),
                clic(tid("submit-entry"), "Pulso Dar entrada"),
                marca(ALERTA, "Se creó la factura", 3500, cursor=False),
                clic(f"{ALERTA} button:has-text('Aceptar')", "Acepto"),
                marca(fila("E310000004512"), "Los otros dos", 3000),
                marca("a:has-text('Cuadre con la DGII'), [role=tab]:has-text('Cuadre con la DGII'), :text('Cuadre con la DGII')", "Cuadre con la DGII", 5000),
            ],
        },
    ],
}

# ───────────────────────── 07 · Factura de una mercancía ya recibida ─────────────────────────
NCF7 = "E310000003377"
VIDEOS["compras-facturas-07-cotejar-recepcion"] = {
    "titulo": "Compras · Entrada de facturas 7: la factura de una mercancía ya recibida",
    "descripcion": "Séptimo video de la serie de entrada de facturas de compra en Germiva ERP. Cuando la mercancía ya entró al almacén con su orden de compra, la factura del proveedor se registra desde la recepción: las líneas salen de lo aceptado y el costo no se carga dos veces.",
    "_comentario": f"Serie Compras · Entrada de facturas (nov. 2026), video 7. Estado A: COM-2026-000001 de Cementos Germiva del Cibao (130555176, plazo 30, categoría 09) recibida y procesada como REC-2026-000001 (100 cementos a 395 + 50 varillas a 245 = 51,750; ITBIS 9,315; total 61,065), sin factura. NCF {NCF7}. La categoría y el plazo vienen de la ficha desde fix/compras-entrada-de-facturas.",
    "sesion": {**SESION, "navegar": "/purchases/receipts", "esperar": "button:has-text('Crear Recepción')"},
    "setup": preparar("A"),
    "aprenderas": ["Encontrar la recepción procesada y sin facturar", "Generar la factura de compra desde la recepción", "Qué se coteja: cantidades aceptadas y precio de la orden", "Registrar la factura cotejada y cerrar la recepción"],
    "errores_comunes": ["Registrar la factura en el buzón aparte: el costo de la mercancía se carga dos veces", "Cambiar la cantidad para que cuadre: se factura lo aceptado; si el proveedor facturó otra cantidad, corrige la recepción", "Facturar una recepción que todavía no se procesó a inventario"],
    "pasos": [
        {
            "id": "01-recepcion", "capitulo": "La recepción sin facturar", "rotulo": "La recepción",
            "ruta": "Compras › Recepciones",
            "narracion": "Llegó la factura de los cementos, pero esa mercancía ya la recibimos: entró al almacén con su orden de compra. Por eso no se registra en el buzón, sino desde la recepción. Esta es la pantalla de Recepciones; cada fila es una entrega de un proveedor. La del cemento está completada y procesada a inventario. La abro con el ojo. Arriba, su orden y su proveedor; abajo, lo que se recibió: cien sacos de cemento y cincuenta varillas. Al pie, pulso Generar factura de compra.",
            "acciones": [
                marca(fila("REC-2026-000001") + " td:nth-child(1)", "cada fila", 3000),
                marca(fila("REC-2026-000001") + " td:has-text('Completada')", "está completada", 3500),
                clic(fila("REC-2026-000001") + " button:has(mat-icon:text-is('visibility'))", "La abro con el ojo"),
                marca(".page-hero, .doc-hero, h1", "su orden y su proveedor", 3000),
                marca("mat-card.products-services-section", "lo que se recibió", 4500),
                clic("button:has-text('Generar factura de compra')", "pulso Generar factura"),
            ],
        },
        {
            "id": "02-cotejo", "capitulo": "Cotejar la factura", "rotulo": "Cotejo",
            "ruta": "Compras › Facturas Recibidas › Facturar recepción",
            "narracion": "Se abre la factura de la recepción. Arriba, el resumen de lo que entró: la recepción, la orden, el proveedor y el valor recibido. Las líneas salen de la cantidad aceptada, al precio de la orden: la cantidad no se edita aquí, y el precio solo se corrige si el proveedor facturó otro. La categoría 606 y el plazo de treinta días vienen de la ficha del proveedor. Copio el NCF de la factura y la fecha de emisión.",
            "acciones": [
                marca(f"{DLG} .gm-dialog-facts", "el resumen de lo que entró", 5000, cursor=False),
                marca(f"{DLG} section[aria-labelledby='entry-sec-3']", "Las líneas salen", 7000, cursor=False),
                marca(campo_id("f-606"), "La categoría 606", 2500),
                marca(campo_id("f-days"), "el plazo de treinta días", 2500),
                teclea("#f-ncf", NCF7, "Copio el NCF"),
                teclea("#f-issue", "20/11/2026", "la fecha de emisión"),
            ],
        },
        {
            "id": "03-registrar", "capitulo": "Registrar la factura cotejada", "rotulo": "Registrar",
            "ruta": "Compras › Facturas Recibidas › Facturar recepción",
            "narracion": "En el asiento, el débito va a mercancía por recibir, que es la cuenta puente de la recepción: así el costo no se carga dos veces. Pulso Registrar factura cotejada. El sistema registra la compra y cierra la recepción como facturada. La factura queda registrada. Acepto. Desde ahora, la factura muestra el cruce con la orden y la recepción: lo pedido, lo recibido y lo facturado.",
            "acciones": [
                marca(f"{DLG} .entry-rail .journal", "En el asiento", 6500, cursor=False),
                clic(f"{DLG} button:has-text('Registrar factura cotejada')", "Pulso Registrar factura cotejada"),
                marca(ALERTA, "La factura queda registrada", 3500, cursor=False),
                clic(f"{ALERTA} button:has-text('Aceptar')", "Acepto"),
                cartel("Cruce de tres vías", "Lo pedido, lo recibido y lo facturado, en la pestaña «Cruce con orden y recepción» de la factura.", "Desde ahora", 7500),
            ],
        },
    ],
}

# ───────────────────────── 08 · La factura llega antes que la mercancía ─────────────────────────
NCF8 = "E310000006018"
VIDEOS["compras-facturas-08-mercancia-por-recibir"] = {
    "titulo": "Compras · Entrada de facturas 8: la factura llega antes que la mercancía",
    "descripcion": "Octavo video de la serie de entrada de facturas de compra en Germiva ERP. Si la factura llega primero, se registra marcando sus líneas como mercancía por recibir: al dar entrada, el sistema abre la recepción en borrador para que el almacén la complete cuando llegue la mercancía.",
    "_comentario": f"Serie Compras · Entrada de facturas (nov. 2026), video 8. Estado A. Pinturas Germiva (130555184, plazo 15, categoría 09). NCF {NCF8}, emisión 19/11/2026. Una línea: 12 Pintura acrílica blanca galón a 890 (18 %, ITBIS 1,922.40; total 12,602.40), marcada «Mercancía por recibir». Al dar entrada se abre la recepción en borrador.",
    "sesion": BUZON, "setup": preparar("A"),
    "aprenderas": ["Registrar una factura de mercancía que todavía no llega", "Marcar las líneas como «Mercancía por recibir»", "La recepción en borrador que abre el sistema", "Quién completa esa recepción y cuándo se mueve el inventario"],
    "errores_comunes": ["Mandar la mercancía a una cuenta de gasto: no entraría nunca al inventario", "Esperar que el inventario suba al dar entrada: sube al procesar la recepción", "Cotejar la factura otra vez cuando llega la mercancía: ya está registrada"],
    "pasos": [
        {
            "id": "01-captura", "capitulo": "La factura que llega primero", "rotulo": "Mercancía por recibir",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "La pinturería nos mandó la factura, pero la pintura llega la semana que viene. La registramos ya, para tener la deuda al día. Pulso Registrar manual y elijo el proveedor: pinturas. El plazo de quince días y la categoría 606 salen de su ficha. Copio el NCF y la fecha de emisión. En los montos paso a por líneas, y escribo la línea: pintura acrílica blanca, doce galones a ochocientos noventa. La tasa la confirmo yo: abro la lista y elijo el dieciocho por ciento.",
            "acciones": [
                clic("button:has-text('Registrar manual')", "Pulso Registrar manual"),
                teclea(f"{DLG} app-partner-document-select input", "Pinturas", "elijo el proveedor"),
                clic("mat-option:has-text('Pinturas Germiva')", "pinturas"),
                marca(campo_id("f-days"), "quince días", 2500),
                teclea("#f-ncf", NCF8, "Copio el NCF"),
                teclea("#f-issue", "19/11/2026", "la fecha de emisión"),
                clic(tid("mode-lines"), "paso a por líneas"),
                teclea(f"{DLG} input[formcontrolname='description'] >> nth=0", "Pintura acrílica blanca galón", "escribo la línea"),
                teclea(f"{DLG} input[formcontrolname='quantity'] >> nth=0", "12", "doce galones"),
                teclea(f"{DLG} input[formcontrolname='unitPrice'] >> nth=0", "890", "ochocientos noventa"),
                clic(f"{DLG} mat-select[formcontrolname='taxRateCode'] >> nth=0", "abro la lista"),
                clic("mat-option:has-text('ITBIS 18%')", "dieciocho por ciento"),
            ],
        },
        {
            "id": "02-marcar", "capitulo": "Marcar la línea", "rotulo": "Por recibir",
            "ruta": "Compras › Facturas Recibidas › Registrar manual",
            "narracion": "Debajo de la línea está el interruptor mercancía por recibir. Lo enciendo: la línea deja de pedir cuenta de gasto, y su costo va a mercancía por recibir, como dice el asiento de la derecha. Pulso Dar entrada. El sistema registra la factura y abre la recepción de la pintura. El aviso confirma la factura, y acepto.",
            "acciones": [
                clic(f"{DLG} mat-slide-toggle.line-goods-toggle >> nth=0", "Lo enciendo"),
                marca(f"{DLG} .entry-rail .journal", "como dice el asiento", 4500, cursor=False),
                clic(tid("submit-entry"), "Pulso Dar entrada"),
                marca(ALERTA, "El aviso confirma", 3000, cursor=False),
                clic(f"{ALERTA} button:has-text('Aceptar')", "y acepto"),
            ],
        },
        {
            "id": "03-recepcion", "capitulo": "La recepción en borrador", "rotulo": "La recepción",
            "ruta": "Compras › Recepciones", "navegar": "/purchases/receipts", "al_decir_navegar": "Recepciones",
            "narracion": "Al dar entrada, el sistema abrió la recepción. Voy a Recepciones, y ahí está, en borrador, de Pinturas Germiva. Cuando llegue la pintura, quien recibe en el almacén la abre, liga la línea a su producto, cuenta lo que llegó y la procesa. Recién entonces sube el inventario. Y no hace falta cotejar la factura otra vez: ya está registrada.",
            "acciones": [
                marca(fila("Pinturas Germiva") + " td:nth-child(1)", "ahí está", 3500),
                marca(fila("Pinturas Germiva") + " td:has-text('Borrador')", "en borrador", 3000),
                cartel("En el almacén", "Liga cada línea a su producto, cuenta lo recibido y procesa: ahí sube el inventario.", "Cuando llegue", 8000),
            ],
        },
    ],
}

# ───────────────────────── 09 · Comprobante de Compras (proveedor informal) ─────────────────────────
FACTURAS = {**SESION, "navegar": "/purchases/invoices", "esperar": "button:has-text('Nueva Factura')"}
TIPO = "mat-form-field:has(mat-label:has-text('Tipo de comprobante')) mat-select"
CAT606 = "mat-form-field:has(mat-label:has-text('Categoría 606')) mat-select"
ORIGEN = "input[placeholder*='Elige la caja o el banco'], mat-form-field:has(mat-label:has-text('Cuenta de origen')) input"
EXITO = "mat-dialog-container:has(button:has-text('Aceptar'))"
LIBRE = [clic("button:has(mat-icon:text-is('more_vert')) >> nth=0", "abro más acciones"),
         clic(".mat-mdc-menu-panel button:has-text('libre')", "formulario libre")]
VIDEOS["compras-facturas-09-proveedor-informal"] = {
    "titulo": "Compras · Entrada de facturas 9: comprar a un proveedor informal",
    "descripcion": "Noveno video de la serie de entrada de facturas de compra en Germiva ERP. Cuando el proveedor no está inscrito en el RNC, el comprobante lo emite tu empresa: el Comprobante de Compras (B11 o E41). Lo registramos en el formulario estándar, con la retención que propone el sistema y el pago desde la caja.",
    "_comentario": "Serie Compras · Entrada de facturas (nov. 2026), video 9. Estado A. Ramón Germiva Almonte (cédula 00113055503, contribuyente informal). Servicio «Flete y acarreo de mercancía» (exento), 1 × 8,500; «Proponer retenciones» aplica el ISR del catálogo (1,275.00) → neto 7,225.00, pagado al contado desde Caja general. La empresa sembrada no tiene certificado digital: el tipo propuesto es B11 (E41 sale «sin certificado digital»).",
    "sesion": FACTURAS, "setup": preparar("A"),
    "aprenderas": ["Cuándo corresponde el Comprobante de Compras (B11/E41)", "Registrar la compra en «Nueva Factura» con un servicio del catálogo", "Proponer las retenciones del proveedor informal", "Pagar el neto desde la caja"],
    "errores_comunes": ["Usar el Comprobante de Compras con un proveedor formal: él debe darte su crédito fiscal", "Emitirlo sin las retenciones: el formulario lo avisa", "Pagarle al proveedor el total: se le paga el neto; lo retenido es de la DGII"],
    "pasos": [
        {
            "id": "01-cabecera", "capitulo": "Proveedor informal y comprobante", "rotulo": "Proveedor informal",
            "ruta": "Compras › Facturas › Nueva",
            "narracion": "Le contratamos un flete a Ramón, un camionero que no está inscrito en el RNC. Él no puede darnos un comprobante fiscal, así que lo emite nuestra empresa: el comprobante de compras. En la pantalla de Facturas de compra, pulso Nueva Factura, y recojo el panel para ver mejor. Busco el proveedor: escribo Ramón y lo elijo; su ficha lo marca como contribuyente informal, con su cédula. El tipo de comprobante ya propone el de compras, el B11; si tu empresa factura electrónico, es el E41. No hay campo para el NCF: lo pone tu secuencia al emitir. Y la categoría 606: abro la lista y elijo gastos por trabajos, suministros y servicios.",
            "acciones": [
                clic("button:has-text('Nueva Factura')", "pulso Nueva Factura"),
                clic("button.panel-collapse", "recojo el panel"),
                teclea("app-partner-document-select input", "Ramón", "escribo Ramón"),
                clic("mat-option:has-text('Ramón Germiva')", "lo elijo"),
                marca("app-partner-document-select", "contribuyente informal", 3500),
                marca(f"mat-form-field:has(mat-label:has-text('Tipo de comprobante'))", "ya propone", 5000),
                clic(CAT606, "abro la lista"),
                clic("mat-option:has-text('02 -')", "gastos por trabajos"),
            ],
        },
        {
            "id": "02-linea-retencion", "capitulo": "La línea y las retenciones", "rotulo": "Retenciones",
            "ruta": "Compras › Facturas › Nueva",
            "narracion": "En las líneas busco el servicio en el catálogo: escribo flete y lo elijo. La cantidad queda en uno, y en precio escribo ocho mil quinientos. Enseguida aparece un aviso: al proveedor informal le retienes el ITBIS facturado y, en servicios, el ISR. Pulso Proponer retenciones, y el sistema aplica las del catálogo. En el resumen aparece la retención del ISR, y el total a pagar baja al neto: siete mil doscientos veinticinco. Las tasas, confírmalas con tu contador.",
            "acciones": [
                teclea("input[placeholder*='Escriba para buscar']", "Flete", "escribo flete"),
                clic("mat-option:has-text('Flete y acarreo')", "lo elijo"),
                teclea("input[formcontrolname='price']:visible", "8500", "en precio escribo"),
                marca(".voucher-retention-notice", "aparece un aviso", 5500),
                clic("button:has-text('Proponer retenciones')", "Pulso Proponer retenciones"),
                marca(".mat-mdc-snack-bar-container", "el sistema aplica", 2500, cursor=False),
                marca("app-retention-perception-column", "la retención del ISR", 3000),
                marca("app-document-payable-total", "el total a pagar", 4500),
            ],
        },
        {
            "id": "03-pagar", "capitulo": "Pagar desde la caja", "rotulo": "Guardar y pagar",
            "ruta": "Compras › Facturas › Nueva",
            "narracion": "Abajo está el pago. La condición es contado, y el panel ya trae el monto a pagar, que es el neto, en efectivo. Falta decir de dónde sale el dinero: en cuenta de origen escribo caja; la lista se filtra sola, bajo con la flecha en la lista y elijo la caja general. Pulso Guardar y pagar. El sistema emite el comprobante con el NCF de la secuencia, hace el asiento y registra la salida de caja. El aviso lo confirma, y acepto. Recuerda: lo retenido no se le paga al proveedor; se le debe a la DGII y sale en tu declaración.",
            "acciones": [
                marca("mat-form-field:has(mat-label:has-text('Monto a pagar'))", "el monto a pagar", 4000),
                teclea(ORIGEN, "Caja", "escribo caja"),
                {"esperar_ms": 600},
                tecla("ArrowDown", "bajo"),
                tecla("ArrowDown", "en la lista"),
                tecla("Enter", "elijo la caja"),
                clic("button:has-text('Guardar y pagar') >> nth=0", "Pulso Guardar y pagar"),
                marca(EXITO, "El aviso lo confirma", 2500, cursor=False),
                clic(f"{EXITO} button:has-text('Aceptar')", "y acepto"),
                cartel("Retenciones", "Al proveedor le pagas el neto; lo retenido se le debe a la DGII.", "Recuerda", 7000),
            ],
        },
    ],
}

# ───────────────────────── 10 · Gastos menores ─────────────────────────
VIDEOS["compras-facturas-10-gastos-menores"] = {
    "titulo": "Compras · Entrada de facturas 10: gastos menores",
    "descripcion": "Décimo video de la serie de entrada de facturas de compra en Germiva ERP. Los gastos pequeños sin proveedor identificado se registran con el comprobante de Gastos Menores (B13 o E43) en el formulario libre: conceptos escritos a mano, sin ITBIS, pagados desde la caja.",
    "_comentario": "Serie Compras · Entrada de facturas (nov. 2026), video 10. Estado A. Formulario libre, B13, sin proveedor (Proveedor Genérico interno, marcado por preparar.mjs hasta que la instantánea traiga el seeder corregido). Líneas exentas: Parqueo para la mensajería (servicio) 300 y Agua y café para la oficina (bien) 850 = 1,150, pagado de Caja general.",
    "sesion": FACTURAS, "setup": preparar("A"),
    "aprenderas": ["Cuándo se usa el comprobante de Gastos Menores (B13/E43)", "Cambiar al formulario libre y escribir conceptos sin catálogo", "Por qué las líneas van exentas", "Pagar el gasto desde la caja"],
    "errores_comunes": ["Ponerle ITBIS a un gasto menor: se registra exento", "Usarlo para una compra de un proveedor con RNC: él debe darte su comprobante", "Agregar descuentos o retenciones: el gasto menor no los admite"],
    "pasos": [
        {
            "id": "01-libre", "capitulo": "Formulario libre y tipo", "rotulo": "Gastos menores",
            "ruta": "Compras › Facturas › Nueva compra",
            "narracion": "Para los gastos pequeños sin un proveedor identificado, como el parqueo o el agua de la oficina, existe el comprobante de gastos menores: el B13, o el E43 si facturas electrónico. Pulso Nueva Factura y recojo el panel. Esta vez uso el formulario libre, donde escribo los conceptos sin catálogo: abro más acciones y elijo cambiar a formulario libre. En tipo de comprobante elijo gastos menores. No hace falta proveedor: la compra queda a nombre del proveedor genérico de la empresa.",
            "acciones": [
                clic("button:has-text('Nueva Factura')", "Pulso Nueva Factura"),
                clic("button.panel-collapse", "recojo el panel"),
                *LIBRE,
                clic(TIPO, "En tipo de comprobante"),
                clic("mat-option:has-text('B13')", "elijo gastos menores"),
                marca("mat-form-field:has(input[placeholder*='Busque por nombre'])", "No hace falta proveedor", 5000),
            ],
        },
        {
            "id": "02-conceptos", "capitulo": "Los conceptos", "rotulo": "Conceptos",
            "ruta": "Compras › Facturas › Nueva compra",
            "narracion": "Pulso Agregar línea y escribo el primer concepto: parqueo para la mensajería. Es un servicio: en tipo elijo servicio. El precio, trescientos pesos. Los gastos menores van sin ITBIS, así que en la tasa elijo exento. Agrego otra línea: agua y café para la oficina, ochocientos cincuenta, y su tasa, exento también. Debajo se ve la cuenta contable que se usará; si quieres otra, la cambias por línea.",
            "acciones": [
                clic("button:has-text('Agregar línea')", "Pulso Agregar línea"),
                teclea("input[formcontrolname='productName'] >> nth=0", "Parqueo para la mensajería", "el primer concepto"),
                clic("mat-select[formcontrolname='goodOrServiceIndicator'] >> nth=0", "en tipo"),
                clic("mat-option:has-text('Servicio')", "elijo servicio"),
                teclea("input[formcontrolname='price']:visible >> nth=0", "300", "trescientos pesos"),
                clic("mat-select[formcontrolname='taxId'] >> nth=0", "en la tasa"),
                clic("mat-option:has-text('Exento')", "elijo exento"),
                clic("button:has-text('Agregar línea')", "Agrego otra línea"),
                teclea("input[formcontrolname='productName'] >> nth=1", "Agua y café para la oficina", "agua y café"),
                teclea("input[formcontrolname='price']:visible >> nth=1", "850", "ochocientos cincuenta"),
                clic("mat-select[formcontrolname='taxId'] >> nth=1", "y su tasa"),
                clic("mat-option:has-text('Exento')", "exento también"),
                marca("text=Cuenta contable:", "la cuenta contable", 4500),
            ],
        },
        {
            "id": "03-pagar", "capitulo": "Pagar desde la caja", "rotulo": "Guardar y pagar",
            "ruta": "Compras › Facturas › Nueva compra",
            "narracion": "En el pago, el gasto sale de la caja: el monto ya es el total, mil ciento cincuenta, en efectivo. En cuenta de origen escribo caja; la lista se filtra sola, bajo con la flecha en la lista y elijo la caja general. Pulso Guardar y pagar. El sistema emite el comprobante de gastos menores con su NCF y registra la salida de caja. El aviso lo confirma, y acepto. Recuerda: el gasto menor no lleva ITBIS, ni descuentos, ni retenciones.",
            "acciones": [
                marca("mat-form-field:has(mat-label:has-text('Monto a pagar'))", "el monto ya es el total", 4000),
                teclea(ORIGEN, "Caja", "escribo caja"),
                {"esperar_ms": 600},
                tecla("ArrowDown", "bajo"),
                tecla("ArrowDown", "en la lista"),
                tecla("Enter", "elijo la caja"),
                clic("button:has-text('Guardar y pagar') >> nth=0", "Pulso Guardar y pagar"),
                marca(EXITO, "El aviso lo confirma", 2500, cursor=False),
                clic(f"{EXITO} button:has-text('Aceptar')", "y acepto"),
                cartel("Gastos menores", "Sin ITBIS, sin descuentos y sin retenciones.", "Recuerda", 6500),
            ],
        },
    ],
}

# ───────────────────────── 11 · Pagos al exterior ─────────────────────────
VIDEOS["compras-facturas-11-pagos-al-exterior"] = {
    "titulo": "Compras · Entrada de facturas 11: pagos al exterior",
    "descripcion": "Último video de la serie de entrada de facturas de compra en Germiva ERP. Un servicio que te factura un proveedor del exterior se registra con el comprobante de Pagos al Exterior (B17 o E47): en dólares, con la tasa del día, exento de ITBIS y con la retención del ISR que exige.",
    "_comentario": "Serie Compras · Entrada de facturas (nov. 2026), video 11. Estado A (USD activo, tasa 60.50 del día). Formulario libre, B17, Germiva Cloud Hosting LLC (documento extranjero US-88-1305550). Línea «Hosting del sistema, noviembre», servicio exento, US$120. «Retención a todas»: ISR Remesas al Exterior 27 % (US$32.40). Crédito con vencimiento 20/12/2026, «Guardar y emitir».",
    "sesion": FACTURAS, "setup": preparar("A"),
    "aprenderas": ["Cuándo se usa el comprobante de Pagos al Exterior (B17/E47)", "Registrar la compra en dólares con la tasa del día", "Aplicar la retención del ISR obligatoria", "Emitir la compra a crédito"],
    "errores_comunes": ["Ponerle ITBIS: las líneas van exentas", "Emitirlo sin la retención del ISR: el comprobante la exige en todas las líneas", "Registrar en pesos una factura en dólares sin su tasa"],
    "pasos": [
        {
            "id": "01-cabecera", "capitulo": "Proveedor del exterior y moneda", "rotulo": "Pagos al exterior",
            "ruta": "Compras › Facturas › Nueva compra",
            "narracion": "El hosting del sistema nos lo factura una empresa de Estados Unidos. Un proveedor del exterior no te da comprobante dominicano, así que tu empresa emite el de pagos al exterior: el B17, o el E47 en electrónico. Pulso Nueva Factura, recojo el panel, abro más acciones y paso al formulario libre. En tipo de comprobante elijo pagos al exterior. Busco el proveedor por su nombre: Germiva Cloud Hosting, que se identifica con su documento extranjero. La factura viene en dólares: arriba, en la moneda, abro la lista y elijo dólar estadounidense, y el sistema toma la tasa del día.",
            "acciones": [
                clic("button:has-text('Nueva Factura')", "Pulso Nueva Factura"),
                clic("button.panel-collapse", "recojo el panel"),
                clic("button:has(mat-icon:text-is('more_vert')) >> nth=0", "abro más acciones"),
                clic(".mat-mdc-menu-panel button:has-text('libre')", "paso al formulario libre"),
                clic(TIPO, "En tipo de comprobante"),
                clic("mat-option:has-text('B17')", "elijo pagos al exterior"),
                teclea("input[placeholder*='Busque por nombre']", "Cloud", "Busco el proveedor"),
                clic("mat-option:has-text('Germiva Cloud')", "Germiva Cloud Hosting"),
                clic("button:has-text('DOP')", "en la moneda"),
                clic("mat-form-field:has(mat-label:has-text('Moneda')) mat-select >> nth=-1", "abro la lista"),
                clic("mat-option:has-text('USD')", "elijo dólar estadounidense"),
                tecla("Escape", "y el sistema"),
                marca("button:has-text('USD')", "la tasa del día", 3500),
            ],
        },
        {
            "id": "02-linea-retencion", "capitulo": "La línea y la retención del ISR", "rotulo": "Retención del ISR",
            "ruta": "Compras › Facturas › Nueva compra",
            "narracion": "Pulso Agregar línea y escribo el concepto: hosting del sistema, noviembre. Aquí no hace falta un producto del catálogo: el concepto se escribe tal como viene en la factura. Es un servicio, así que en la columna tipo elijo servicio. El precio: ciento veinte dólares. Y va exento de ITBIS: en la columna tasa elijo exento. Ahora lo que este comprobante exige: la retención del ISR en todas las líneas. Pulso Retención a todas. En el tipo de retención de ISR elijo remesas al exterior, y el sistema propone su tasa: veintisiete por ciento. Aplico, y el aviso confirma la retención en todas las líneas.",
            "acciones": [
                clic("button:has-text('Agregar línea')", "Pulso Agregar línea"),
                teclea("input[formcontrolname='productName'] >> nth=0", "Hosting del sistema, noviembre", "escribo el concepto"),
                clic("mat-select[formcontrolname='goodOrServiceIndicator'] >> nth=0", "columna tipo"),
                clic("mat-option:has-text('Servicio')", "elijo servicio"),
                teclea("input[formcontrolname='price']:visible >> nth=0", "120", "El precio"),
                clic("mat-select[formcontrolname='taxId'] >> nth=0", "columna tasa"),
                clic("mat-option:has-text('Exento')", "elijo exento"),
                clic("button:has-text('Retención a todas')", "Pulso Retención a todas"),
                clic(f"{DLG} mat-select[formcontrolname='isrTaxRetentionTypeId']", "tipo de retención"),
                clic("mat-option:has-text('Remesas al Exterior')", "remesas al exterior"),
                marca(f"{DLG} mat-form-field:has(input[formcontrolname='isrWithholdingRate'])", "veintisiete por ciento", 3000),
                clic(f"{DLG} button:has-text('Aplicar')", "Aplico"),
                marca(".mat-mdc-snack-bar-container", "el aviso confirma", 2500, cursor=False),
            ],
        },
        {
            "id": "03-emitir", "capitulo": "A crédito y emitir", "rotulo": "Guardar y emitir",
            "ruta": "Compras › Facturas › Nueva compra",
            "narracion": "Este proveedor nos da un mes para pagar. En condición de pago abro la lista y elijo crédito, y en vencimiento escribo el veinte de diciembre. El resumen muestra la retención del ISR, y el total a pagar, el neto, en dólares. Pulso Guardar y emitir, y confirmo: la compra toma su NCF de la secuencia. El aviso confirma que se creó y se emitió, y acepto. Con esto ya conoces todas las formas de dar entrada a una factura de compra en Germiva.",
            "acciones": [
                clic("mat-form-field:has(mat-label:has-text('Condición de pago')) input", "abro la lista"),
                clic("mat-option:has-text('Crédito')", "elijo crédito"),
                teclea("mat-form-field:has(mat-label:has-text('Vencimiento')) input", "20/12/2026", "en vencimiento escribo"),
                marca("app-retention-perception-column, app-document-payable-total", "El resumen muestra", 3500),
                marca("app-document-payable-total", "el total a pagar", 3500),
                clic("button:has-text('Guardar y emitir') >> nth=0", "Pulso Guardar y emitir"),
                clic("mat-dialog-container button:has-text('Emitir') >> nth=-1", "y confirmo"),
                marca(EXITO, "El aviso confirma", 2500, cursor=False),
                clic(f"{EXITO} button:has-text('Aceptar')", "y acepto"),
                cartel("Serie completa", "Buzón: lo que emite el proveedor · Nueva Factura: lo que emite tu empresa · Recepción: la mercancía ya recibida.", "Con esto", 8000),
            ],
        },
    ],
}

if __name__ == "__main__":
    solo = sys.argv[1:]
    for nombre, v in VIDEOS.items():
        if solo and not any(s in nombre for s in solo):
            continue
        guion = {**COMUN, **v}
        (RAIZ / "guiones" / f"{nombre}.json").write_text(json.dumps(guion, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        pal = sum(len(p["narracion"].split()) for p in v["pasos"])
        print(f"{nombre}: {len(v['pasos'])} pasos, {pal} palabras (~{pal/2.9/60:.1f} min)")
