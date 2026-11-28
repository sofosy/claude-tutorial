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
                {"click": f"{DLG} button:has-text('Guardar')", "al_decir": "Guardo"},
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


if __name__ == "__main__":
    for f in (ars_01,):
        print(f())
