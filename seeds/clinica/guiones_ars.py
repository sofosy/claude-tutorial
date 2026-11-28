"""Serie «Seguros de salud (ARS)» (RegiSalud), 2026-11.

  python3 seeds/clinica/guiones_ars.py      → escribe guiones/ars-0N-*.json

Estado previo de cada video: `node seeds/clinica/ars.mjs restaurar <base|B|C|D|E>` (ver ars.mjs).
"""
from comun import guion

R = lambda texto, ms=3500, **k: {"resaltar": texto, "durante_ms": ms, **k}  # noqa: E731
DLG = "mat-dialog-container"


def ars_01():
    pasos = [
        {
            "id": "01-consola", "capitulo": "La consola de Seguros de Salud", "rotulo": "Seguros de Salud",
            "navegar": "/home", "ruta": "Seguros de Salud",
            "texto_pantalla": "Aseguradoras, tarifario, afiliaciones, autorizaciones y reclamaciones",
            "narracion": (
                "En esta serie vemos el ciclo completo con las ARS, las administradoras de riesgos de salud: la aseguradora y su tarifario, la afiliación "
                "del paciente, la autorización, las dos facturas y el cobro a la aseguradora. Entro a Seguros de "
                "Salud, en el menú de la izquierda. Arriba, el resumen dice cuántas aseguradoras hay, cuántas "
                "autorizaciones esperan respuesta y cuánto se les debe cobrar a las ARS. Las pestañas siguen el "
                "ciclo: aseguradoras, tarifario, afiliaciones, autorizaciones y reclamaciones."
            ),
            "acciones": [
                R("a.rail-item[aria-label='Seguros de Salud']", 3000, al_decir="las dos facturas"),
                {"click": "a.rail-item[aria-label='Seguros de Salud']", "al_decir": "Entro a Seguros"},
                R(":text('aseguradoras ·')", 4000, al_decir="el resumen dice"),
                R("a[role=tab]:has-text('Aseguradoras')", 1800, al_decir="las pestañas siguen"),
                R("a[role=tab]:has-text('Tarifario')", 1500, al_decir="tarifario, afiliaciones"),
                R("a[role=tab]:has-text('Reclamaciones')", 2000, al_decir="y reclamaciones"),
            ],
        },
        {
            "id": "02-importar", "capitulo": "Importar las aseguradoras", "rotulo": "Importar del catálogo",
            "ruta": "Seguros de Salud › Aseguradoras › Importar del catálogo",
            "texto_pantalla": "Las ARS dominicanas, con sus planes, desde el catálogo",
            "narracion": (
                "El centro todavía no tiene aseguradoras. Lo más rápido es traerlas del catálogo dominicano, con "
                "sus planes ya cargados; también se puede crear una a mano con Nueva aseguradora. Pulso Importar "
                "del catálogo, y se abre la lista de las ARS del país. Busco Humano, y cuando aparece en la lista con sus ocho planes, la marco con un clic. Ahora borro la búsqueda y escribo "
                "Senasa, que es la otra ARS con la que trabaja el centro; la marco también. La selección se "
                "conserva entre búsquedas. Pulso Importar. El aviso confirma dos aseguradoras y doce planes; pulso "
                "Entendido. Lo importado pasa a ser del centro: se puede renombrar o desactivar sin afectar a "
                "nadie más."
            ),
            "acciones": [
                R("button:has-text('Nueva aseguradora')", 3000, al_decir="crear una a mano"),
                {"click": "button:has-text('Importar del catálogo') >> nth=0", "al_decir": "Pulso Importar del"},
                R(f"{DLG}", 2200, al_decir="se abre la lista", cursor=False),
                {"escribir": {"sel": f"{DLG} input", "texto": "Humano"}, "al_decir": "Busco Humano"},
                {"click": f"{DLG} :text('ARS HUMANO')", "al_decir": "la marco con un clic"},
                {"escribir": {"sel": f"{DLG} input", "texto": "Senasa"}, "al_decir": "escribo Senasa"},
                {"click": f"{DLG} :text('ARS SENASA')", "al_decir": "la marco también"},
                {"click": f"{DLG} button:has-text('Importar')", "al_decir": "Pulso Importar. El"},
                R(f"{DLG}", 2500, al_decir="El aviso confirma", cursor=False),
                {"click": "button:has-text('Entendido')", "al_decir": "Entendido. Lo"},
                R(":text('ARS HUMANO') >> nth=0", 3500, al_decir="pasa a ser del centro"),
            ],
        },
        {
            "id": "03-ficha", "capitulo": "La ficha de la aseguradora", "rotulo": "La ficha de la ARS",
            "ruta": "Seguros de Salud › Aseguradoras › ARS Humano",
            "texto_pantalla": "Planes, convenio y lo que exige para reclamar",
            "narracion": (
                "A la derecha está la ficha de ARS Humano: su registro nacional de contribuyente, el RNC, sus cifras de cobro y, debajo, sus planes. Más abajo, el "
                "convenio y el tarifario, y lo que la ARS exige para reclamar. Aquí avisa que faltan dos datos: sin "
                "el código de prestador y el plazo de presentación, la aseguradora devuelve la remesa. Pulso "
                "Completar."
            ),
            "acciones": [
                R(":text('RNC 102017174')", 2500, al_decir="el RNC"),
                R(":text('PLANES') >> nth=0", 3000, al_decir="debajo, sus planes"),
                R(":text('Faltan datos para poder reclamar')", 4500, al_decir="faltan dos datos"),
                {"click": "button:has-text('Completar')", "al_decir": "Pulso Completar"},
            ],
        },
        {
            "id": "04-completar", "capitulo": "Código de prestador y plazo", "rotulo": "Completar la ARS",
            "ruta": "Seguros de Salud › Aseguradoras › Editar aseguradora",
            "texto_pantalla": "Código de prestador, comprobante y plazo de presentación",
            "narracion": (
                "La ficha trae el RNC, que hace falta para facturarle con crédito fiscal, y el teléfono de "
                "autorizaciones. En facturación y reclamación escribo el código de prestador que la ARS le dio al "
                "centro. El tipo de comprobante lo dejo automático: el sistema elige el que tenga secuencia activa. "
                "Y a la derecha, el plazo de presentación, los días que da la ARS para reclamarle: sesenta. Con eso "
                "basta. Pulso Guardar cambios, y el aviso lo confirma."
            ),
            "acciones": [
                R("mat-form-field:has([formcontrolname='tin'])", 3000, al_decir="trae el RNC"),
                R("mat-form-field:has([formcontrolname='authorizationPhone'])", 2500, al_decir="el teléfono"),
                {"escribir": {"sel": "input[formcontrolname='insurerProviderCode']", "texto": "PSS-10458"},
                 "al_decir": "escribo el código de prestador"},
                R("mat-form-field:has([formcontrolname='ncfType'])", 2500, al_decir="lo dejo automático"),
                {"escribir": {"sel": "input[formcontrolname='insurerClaimDeadlineDays']", "texto": "60"},
                 "al_decir": "los días que da"},
                {"click": "button:has-text('Guardar cambios')", "al_decir": "Pulso Guardar cambios"},
                R("mat-dialog-container:has(app-custom-alert-dialog)", 1800, al_decir="el aviso lo confirma", cursor=False),
                {"click_opcional": "button:has-text('Entendido')", "espera_ms": 5000},
            ],
        },
        {
            "id": "05-tarifa", "capitulo": "El tarifario", "rotulo": "Nueva tarifa",
            "navegar": "/health-insurance/tarifario", "al_decir_navegar": "pasamos al tarifario",
            "ruta": "Seguros de Salud › Tarifario › Nueva tarifa",
            "texto_pantalla": "Por plan y por servicio: lo que cubre la ARS y lo que paga el paciente",
            "narracion": (
                "Con la aseguradora lista, pasamos al tarifario, que es el acuerdo con la ARS: por plan y por servicio, cuánto cubre ella y "
                "cuánto paga el paciente. Pulso Nueva tarifa, y se abre el formulario en blanco. Elijo el plan, ARS Humano Básico. Una tarifa es de un "
                "plan, no de toda la aseguradora. Después elijo el servicio: la consulta de medicina general. Su precio de venta se propone como precio convenido: dos mil "
                "quinientos. La ARS cubre dos mil, y el copago se calcula solo: quinientos, lo que paga el paciente en el mostrador. Ahora escribo el código con "
                "que la ARS identifica el servicio, y marco que exige autorización previa. Guardo."
            ),
            "acciones": [
                {"click": "button:has-text('Nueva tarifa') >> nth=0", "al_decir": "Pulso Nueva tarifa"},
                R(f"{DLG}", 2000, al_decir="el formulario en blanco", cursor=False),
                {"click": f"{DLG} mat-select >> nth=0", "al_decir": "Elijo el plan"},
                {"click": "mat-option:has-text('ARS Humano Basico')", "al_decir": "Humano Básico"},
                {"click": f"{DLG} mat-select >> nth=1", "al_decir": "Después elijo el servicio"},
                {"click": "mat-option:has-text('Consulta de medicina general')", "al_decir": "la consulta de"},
                R(f"{DLG} mat-form-field:has-text('Precio convenido')", 3000, al_decir="se propone como"),
                {"escribir": {"sel": f"{DLG} mat-form-field:has-text('Cubre la aseguradora') input", "texto": "2000"},
                 "al_decir": "La ARS cubre"},
                R(f"{DLG} mat-form-field:has-text('Copago del paciente')", 3000, al_decir="se calcula solo"),
                {"escribir": {"sel": f"{DLG} mat-form-field:has-text('Código de la ARS') input", "texto": "CONS-001"},
                 "al_decir": "Ahora escribo el código"},
                {"click": f"{DLG} mat-slide-toggle button", "al_decir": "marco que exige"},
                {"click": f"{DLG} button:has-text('Guardar')", "al_decir": "guardo"},
            ],
        },
        {
            "id": "06-mas", "capitulo": "Otras formas de cargar el tarifario", "rotulo": "Importar y aprobar",
            "ruta": "Seguros de Salud › Tarifario",
            "texto_pantalla": "Importar / Exportar · Requerir aprobación de las tarifas",
            "narracion": (
                "La tarifa queda en la lista, con lo que cubre la ARS, el copago y que exige autorización. Los "
                "montos se corrigen aquí mismo. Para cargar muchas a la vez está Importar y Exportar, con una "
                "plantilla. Y en el engranaje, Requerir aprobación hace que cada tarifa nueva pase por un "
                "supervisor antes de usarse. En el próximo video afiliamos a una paciente y pedimos su autorización."
            ),
            "acciones": [
                R("tr:has-text('Consulta de medicina general')", 4500, al_decir="queda en la lista"),
                R("button:has-text('Importar / Exportar') >> nth=0", 3500, al_decir="Para cargar muchas"),
                R("button[aria-label='Ajustes del módulo']", 3500, al_decir="en el engranaje"),
            ],
        },
    ]
    return guion(
        "ars-01-aseguradoras-tarifario", "Seguros de salud · Parte 1: aseguradoras y tarifario",
        "Primera parte de la serie de ARS de RegiSalud: la consola de Seguros de Salud, importar las ARS del "
        "catálogo dominicano con sus planes, completar el código de prestador y el plazo de presentación, y "
        "cargar el tarifario: lo que cubre la ARS y el copago del paciente, por plan y por servicio.",
        pasos, comentario="Estado: ars.mjs restaurar base.", portada_s=4,
    )


def ars_02():
    pasos = [
        {
            "id": "01-afiliacion", "capitulo": "La afiliación del paciente", "rotulo": "Nueva afiliación",
            "navegar": "/patients", "ruta": "Pacientes › ficha › ARS › Nueva afiliación",
            "texto_pantalla": "A qué plan pertenece el paciente: aseguradora, plan, póliza y afiliado",
            "narracion": (
                "Rosa Elena Martínez llega con su seguro de ARS Humano. La afiliación se registra en su ficha; "
                "también se puede marcar al crear el paciente, con la casilla de que viene con seguro. Abro a "
                "Rosa en la lista, y en su ficha paso a la pestaña ARS. Pulso Nueva afiliación, y se abre el formulario con su nombre arriba. Primero elijo la aseguradora: ARS Humano. "
                "Con eso se cargan sus planes, y elijo el suyo, que es el Básico. Ahora escribo el número de "
                "póliza, tal como sale en su carnet. Debajo va el número de afiliado, que es el que la ARS pide "
                "en cada autorización. La vigencia empieza hoy, y como es su primera afiliación, queda como la "
                "principal. Todo listo: guardo."
            ),
            "acciones": [
                {"click": "button:has-text('Rosa Elena')", "al_decir": "Abro a"},
                {"click": "button.tab:has-text('ARS')", "al_decir": "la pestaña ARS"},
                {"click": "button:has-text('Nueva afiliación')", "al_decir": "Pulso Nueva afiliación"},
                R(f"{DLG} :text('Rosa Elena Martínez')", 2000, al_decir="con su nombre arriba", cursor=False),
                {"click": f"{DLG} mat-select[formcontrolname='insurerId']", "al_decir": "Primero elijo la aseguradora"},
                {"click": "mat-option:has-text('ARS HUMANO')", "al_decir": "ARS Humano. Con"},
                {"click": f"{DLG} mat-select[formcontrolname='planId']", "al_decir": "se cargan sus planes"},
                {"click": "mat-option:has-text('Basico')", "al_decir": "que es el Básico"},
                {"escribir": {"sel": "input[formcontrolname='policyNumber']", "texto": "HUM-778812"},
                 "al_decir": "Ahora escribo el número"},
                {"escribir": {"sel": "input[formcontrolname='memberNumber']", "texto": "88120455"},
                 "al_decir": "Debajo va el número"},
                R(f"{DLG} mat-form-field:has([formcontrolname='effectiveDate'])", 2500, al_decir="La vigencia empieza hoy"),
                R(f"{DLG} :text('queda como la principal')", 3000, al_decir="queda como la principal"),
                {"click": f"{DLG} button:has-text('Guardar')", "al_decir": "guardo"},
            ],
        },
        {
            "id": "02-autorizacion", "capitulo": "Pedir la autorización", "rotulo": "Nueva autorización",
            "ruta": "Pacientes › ficha › ARS › Nueva autorización",
            "texto_pantalla": "Lo que la ARS acepta cubrir, con los montos del tarifario",
            "narracion": (
                "La afiliación queda arriba, como principal. Ahora la consulta: en el tarifario exige "
                "autorización, así que pulso Nueva autorización. La afiliación ya viene elegida, con el tipo y "
                "la urgencia. Busco el servicio escribiendo consulta, y en la lista aparece con su tarifa; lo elijo. Los montos salen del tarifario: dos mil "
                "quinientos, de los que la ARS cubre dos mil y la paciente paga quinientos. Vienen bloqueados "
                "porque así lo pactó el convenio."
            ),
            "acciones": [
                R(":text('ARS HUMANO · ARS Humano Basico')", 3000, al_decir="La afiliación queda arriba"),
                {"click": "button:has-text('Nueva autorización')", "al_decir": "pulso Nueva autorización"},
                R(":text('No. afiliado')", 3000, al_decir="ya viene elegida"),
                {"escribir": {"sel": "mat-form-field:has-text('Servicio a autorizar') input", "texto": "Consulta"},
                 "al_decir": "Busco el servicio"},
                {"click": "mat-option:has-text('Consulta de medicina general')", "al_decir": "con su tarifa; lo elijo"},
                R(":text('Cubre la aseguradora') >> nth=0", 3500, al_decir="la ARS cubre dos mil"),
                R(":text('Montos del convenio')", 3000, al_decir="Vienen bloqueados"),
            ],
        },
        {
            "id": "03-aprobar", "capitulo": "Registrar la respuesta de la ARS", "rotulo": "Guardar y aprobar",
            "ruta": "Pacientes › ficha › ARS › Nueva autorización › Respuesta de la aseguradora",
            "texto_pantalla": "Código de la ARS, monto aprobado y vigencia",
            "narracion": (
                "La autorización se pide por el canal de la ARS: su portal o su teléfono. Si todavía no responde, "
                "pulso Guardar y queda pendiente. Aquí ya llamé y me dieron el código, así que enciendo Registrar "
                "la aprobación. Escribo el código que dio la ARS, que es el que se reclama después. El monto aprobado "
                "se propone con la cobertura calculada, y la vigencia es de treinta días. Si todo cuadra, pulso "
                "Guardar y Aprobar. El aviso confirma que quedó aprobada con su código. Pulso Entendido, y la "
                "autorización aparece en la lista de Rosa, con su número y su vencimiento."
            ),
            "acciones": [
                R("button:has-text('Guardar borrador') >> xpath=..", 3500, al_decir="Si todavía no responde"),
                {"click": "mat-slide-toggle:has-text('Registrar la aprobación') button", "al_decir": "enciendo Registrar"},
                {"escribir": {"sel": "input[formcontrolname='insurerAuthorizationNumber']", "texto": "AUT-551207"},
                 "al_decir": "Escribo el código"},
                R("mat-form-field:has([formcontrolname='approvedAmount'])", 3000, al_decir="El monto aprobado"),
                R("mat-form-field:has([formcontrolname='validUntil'])", 2500, al_decir="treinta días"),
                {"click": "button:has-text('Guardar y Aprobar')", "al_decir": "pulso Guardar y Aprobar"},
                R("mat-dialog-container:has(app-custom-alert-dialog)", 2500, al_decir="El aviso confirma", cursor=False),
                {"click": "button:has-text('Entendido')", "al_decir": "Pulso Entendido"},
                R(":text('ARS AUT-551207')", 3000, al_decir="aparece en la lista"),
            ],
        },
        {
            "id": "04-bandejas", "capitulo": "Las bandejas de seguimiento", "rotulo": "Autorizaciones y afiliaciones",
            "navegar": "/health-insurance/autorizaciones", "al_decir_navegar": "En Seguros de Salud",
            "ruta": "Seguros de Salud › Autorizaciones · Afiliaciones",
            "texto_pantalla": "Qué contestó la ARS, qué vence y qué ya se puede facturar",
            "narracion": (
                "Todo esto se sigue desde la consola. En Seguros de Salud, la pestaña Autorizaciones es la "
                "bandeja: cuántas esperan respuesta, cuántas vencen y cuántas están aprobadas sin usar. Cada "
                "fila dice su siguiente paso; la de Rosa ya se puede facturar. Ahora paso a la pestaña de al lado. En Afiliaciones, la columna "
                "Cobertura hoy contesta si el seguro cubre hoy, y Verificar lo comprueba. En el próximo video "
                "facturamos la consulta: lo que paga Rosa y lo que se le reclama a la ARS."
            ),
            "acciones": [
                R(":text('APROBADAS SIN USAR') >> xpath=..", 3500, al_decir="cuántas están aprobadas"),
                R("button:has-text('Facturar en el paciente')", 3500, al_decir="ya se puede facturar"),
                {"click": "a[role=tab]:has-text('Afiliaciones')", "al_decir": "En Afiliaciones"},
                R("td:has-text('Cubre')", 3000, al_decir="Cobertura hoy contesta"),
                R("button:has-text('Verificar')", 2500, al_decir="Verificar lo comprueba"),
            ],
        },
    ]
    return guion(
        "ars-02-afiliacion-autorizacion", "Seguros de salud · Parte 2: afiliación y autorización",
        "Segunda parte de la serie de ARS de RegiSalud: registrar la afiliación del paciente en su ficha, pedir "
        "la autorización de un servicio con los montos del tarifario, registrar la aprobación de la ARS y "
        "seguirla desde las bandejas de Autorizaciones y Afiliaciones.",
        pasos, comentario="Estado: ars.mjs restaurar B.", portada_s=4,
    )


def ars_03():
    pasos = [
        {
            "id": "01-dos-facturas", "capitulo": "Dos facturas por un servicio", "rotulo": "Facturar la autorización",
            "navegar": "/patients/545?tab=ars", "ruta": "Pacientes › ficha › ARS › Facturar esta autorización",
            "texto_pantalla": "La paciente paga su copago; lo que cubre la ARS se le factura a ella aparte",
            "narracion": (
                "Un servicio con seguro lleva dos facturas: la de la paciente, solo por lo que ella paga, y la de "
                "la ARS, por lo que cubre, que se hace después en Reclamaciones. Empezamos por la de Rosa. En su "
                "ficha, pestaña ARS, está la autorización aprobada de la consulta. En su menú pulso Facturar esta "
                "autorización. Es la forma más común; también se puede cobrar la consulta desde la cita en la "
                "agenda."
            ),
            "acciones": [
                R("a.rail-item[aria-label='Seguros de Salud']", 2500, al_decir="en Reclamaciones"),
                R(":text('Cobertura del paciente') >> xpath=..", 3000, al_decir="Empezamos por la de Rosa"),
                R(":text('ARS AUT-551207')", 4000, al_decir="está la autorización aprobada"),
                {"click": "button:has(mat-icon:text('more_vert')) >> nth=1", "al_decir": "En su menú"},
                {"click": ".mat-mdc-menu-content button:has-text('Facturar esta autorización')",
                 "al_decir": "pulso Facturar esta"},
                R(":text('Nueva Factura')", 3000, al_decir="Es la forma más común"),
            ],
        },
        {
            "id": "02-factura", "capitulo": "La factura del paciente", "rotulo": "Factura del paciente",
            "ruta": "Ventas › Facturas › Nueva factura (médica)",
            "texto_pantalla": "El servicio completo, menos lo que cubre la ARS: el copago",
            "narracion": (
                "Se abre la factura ya armada. La paciente queda fija mientras se use su cobertura, y el "
                "comprobante es de consumo. Abajo están su aseguradora, su plan y su póliza. La línea trae la "
                "consulta de dos mil quinientos, con lo que cubre la ARS. El resumen lo deja claro: dos mil "
                "quinientos de servicio, menos dos mil de cobertura, y un total a pagar de quinientos."
            ),
            "acciones": [
                R(":text('El paciente no puede cambiarse')", 3500, al_decir="queda fija"),
                R(":text('COBERTURA DEL PACIENTE') >> xpath=..", 3500, al_decir="su aseguradora"),
                R(":text('COBERT. ARS')", 3000, al_decir="con lo que cubre"),
                R("app-document-cost-summary", 3500, al_decir="El resumen lo deja claro"),
                R(".invoice-total-block", 3000, al_decir="un total a pagar"),
            ],
        },
        {
            "id": "03-cobro", "capitulo": "Cobrar el copago", "rotulo": "Guardar y cobrar",
            "ruta": "Ventas › Facturas › Nueva factura › Cobro",
            "texto_pantalla": "Efectivo, tarjeta o transferencia; la factura queda saldada",
            "narracion": (
                "Más abajo está el cobro. Rosa paga en efectivo, así que elijo Efectivo. Me entrega justo quinientos, y pulso Exacto: el monto "
                "recibido es el mismo que se cobra. El aviso de abajo confirma que se cobran quinientos y la "
                "factura queda saldada. Pulso Guardar y cobrar. En ese paso se emite el comprobante y se registra "
                "el cobro, y la factura queda en contabilidad. El aviso dice cobro procesado; pulso Aceptar."
            ),
            "acciones": [
                {"click": "button:has-text('Efectivo')", "al_decir": "elijo Efectivo"},
                {"click": "button:has-text('Exacto')", "al_decir": "pulso Exacto"},
                R(":text('la factura queda')", 3000, al_decir="El aviso de abajo"),
                {"click": "button:has-text('Guardar y cobrar')", "al_decir": "Pulso Guardar y cobrar"},
                R("mat-dialog-container:has(app-custom-alert-dialog)", 1800, al_decir="El aviso dice", cursor=False),
                {"click": "button:has-text('Aceptar')", "al_decir": "pulso Aceptar"},
            ],
        },
        {
            "id": "04-resultado", "capitulo": "La factura pagada", "rotulo": "Factura pagada",
            "ruta": "Ventas › Facturas › Ver factura",
            "texto_pantalla": "Pagada, con su comprobante; la autorización queda utilizada",
            "narracion": (
                "La factura queda pagada, con su número de comprobante. El resumen de pagos dice lo cobrado y que "
                "no queda nada pendiente, y desde aquí se imprime la factura, o también el recibo del pago. La autorización pasa a "
                "utilizada: ya no se puede facturar otra vez. Lo que cubrió la ARS queda en Reclamaciones, por "
                "reclamar. En el próximo video se lo reclamamos y le emitimos su factura."
            ),
            "acciones": [
                R(":text('Pagada') >> nth=0", 3000, al_decir="queda pagada"),
                R(":text('B0200000001')", 2500, al_decir="número de comprobante"),
                R(":text('Resumen de Pagos') >> xpath=..", 3500, al_decir="El resumen de pagos"),
                R("button:has-text('Imprimir') >> nth=0", 2500, al_decir="se imprime"),
                R("button:has-text('Imprimir recibo')", 2500, al_decir="el recibo del pago"),
                R(":text('Cobertura ARS') >> nth=0", 3000, al_decir="Lo que cubrió la ARS"),
            ],
        },
    ]
    return guion(
        "ars-03-factura-paciente", "Seguros de salud · Parte 3: la factura del paciente",
        "Tercera parte de la serie de ARS de RegiSalud: facturar una autorización aprobada, la factura del "
        "paciente por su copago (el servicio completo menos la cobertura de la ARS), cobrarla y cómo queda la "
        "autorización.",
        pasos, comentario="Estado: ars.mjs restaurar C.", portada_s=4,
    )


if __name__ == "__main__":
    for f in (ars_01, ars_02, ars_03):
        print(f())
