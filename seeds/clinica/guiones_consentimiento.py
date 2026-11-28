"""Video «Consentimiento informado» (RegiSalud), 2026-11.

  python3 seeds/clinica/guiones_consentimiento.py   → escribe guiones/consentimiento-01-*.json

Estado previo: `node seeds/clinica/consentimiento.mjs` (Rosa sin registros clínicos).
Se graba con la sesión de la doctora Ana Pérez: el documento toma su nombre y su exequátur, y la firma
del registro es suya. `window.open` se redirige a la misma pestaña para que la grabación siga a la
página de firma del paciente.
"""
import json

from comun import RAIZ, guion

R = lambda texto, ms=3500, **k: {"resaltar": texto, "durante_ms": ms, **k}  # noqa: E731
ANA = json.loads((RAIZ / "guiones" / "clinica-ana.json").read_text(encoding="utf-8"))
HUECO = ".ck-editor__editable p:has-text('_____') >> nth=0"
PANEL = "app-consent-request-panel"


def llenar(texto, al_decir):
    """Triple clic selecciona la línea en blanco entera; lo que se teclea la reemplaza."""
    return [{"click": HUECO, "veces": 3, "al_decir": al_decir}, {"teclear": texto}]


def consentimiento_01():
    pasos = [
        {
            "id": "01-nuevo", "capitulo": "Un consentimiento nuevo", "rotulo": "Consentimiento informado",
            "navegar": "/patients", "ruta": "Pacientes › ficha › Consentimiento Informado General",
            "texto_pantalla": "El consentimiento se redacta en la ficha del paciente",
            "narracion": (
                "En este video la doctora Ana Pérez prepara el consentimiento de un procedimiento, la paciente lo "
                "firma y queda la constancia en su expediente. Abro a Rosa Elena Martínez. En la ficha, debajo de "
                "Plantillas, está Consentimiento Informado General: viene asignado a todos los médicos, y el "
                "centro puede crear los suyos en las plantillas clínicas. Lo abro y pulso Nueva. El documento ya "
                "trae los datos de la paciente, su cédula, y el nombre y el exequátur de la doctora."
            ),
            "acciones": [
                {"click": "button:has-text('Rosa Elena')", "al_decir": "Abro a Rosa Elena"},
                R("button.tab:has-text('Consentimiento Informado General')", 4000, al_decir="debajo de Plantillas"),
                {"click": "button.tab:has-text('Consentimiento Informado General')", "al_decir": "Lo abro"},
                {"click": "button:has(mat-icon:text('add_circle'))", "al_decir": "pulso Nueva"},
                R(".ck-editor__editable p:has-text('Yo, Rosa Elena')", 3500, al_decir="los datos de la paciente"),
                R(".ck-editor__editable p:has-text('exequátur')", 3000, al_decir="el exequátur"),
            ],
        },
        {
            "id": "02-llenar", "capitulo": "Procedimiento, riesgos y alternativas", "rotulo": "Llenar los espacios",
            "ruta": "Pacientes › ficha › Consentimiento › Redacción",
            "texto_pantalla": "Las líneas en blanco son lo que la doctora explica a la paciente",
            "narracion": (
                "Lo que falta son las líneas en blanco, y se llenan con palabras que la paciente entienda. Primero "
                "el procedimiento: drenaje de un absceso en el brazo derecho, tal como se lo dije a ella. En la línea de abajo, cómo se hace: "
                "con anestesia local, en el mismo consultorio. Después, los riesgos que le expliqué en la consulta, "
                "los frecuentes y también los suyos propios. En la otra línea, lo que puede quedarle después, que es una "
                "pequeña cicatriz. Por último, las alternativas razonables, incluida la de no hacer nada. Un "
                "consentimiento con huecos sin llenar no se puede enviar a firmar."
            ),
            "acciones": [
                *llenar("Drenaje de un absceso en el brazo derecho,", "el procedimiento: drenaje"),
                *llenar("con anestesia local.", "En la línea de abajo"),
                *llenar("Dolor, sangrado leve o infección.", "los riesgos que le expliqué"),
                *llenar("Una pequeña cicatriz en la zona.", "En la otra línea"),
                *llenar("Tratamiento con antibióticos, o no hacer nada.", "las alternativas razonables"),
            ],
        },
        {
            "id": "03-completar", "capitulo": "Completar y elegir cómo firma", "rotulo": "Completar",
            "ruta": "Pacientes › ficha › Consentimiento › Aceptación del paciente",
            "texto_pantalla": "En el consultorio o por correo",
            "narracion": (
                "Debajo del documento, la aceptación del paciente espera a que el registro esté completo. El botón Guardar "
                "solo lo deja en borrador. Ahora pulso Completar. El aviso lo confirma, y se abre la aceptación del paciente. Hay dos "
                "formas de firmar. Por correo, a la paciente le llega un enlace personal y firma desde su casa: "
                "eliges cuántos días vale y se le recuerda antes de vencer. Mientras no firme, el enlace se puede "
                "reenviar o cancelar. Pero lo más común es que firme aquí mismo, así que elijo En el consultorio. "
                "Antes de abrir el documento, pedirá los últimos cuatro dígitos de su cédula."
            ),
            "acciones": [
                R("button:has(mat-icon:text('check_circle'))", 2500, al_decir="Debajo del documento"),
                R("button:has(mat-icon:text('save'))", 1500, al_decir="El botón Guardar"),
                {"click": "button:has-text('Completar')", "al_decir": "Ahora pulso Completar"},
                R(".mat-mdc-snack-bar-label, simple-snack-bar", 1800, al_decir="El aviso lo confirma", cursor=False),
                R(PANEL, 3000, al_decir="se abre la aceptación"),
                {"click": f"{PANEL} [role=radio]:has-text('Por correo')", "al_decir": "Por correo, a la paciente"},
                R(f"{PANEL} mat-form-field:has-text('Vigencia del enlace')", 3500, al_decir="cuántos días vale"),
                {"click": f"{PANEL} [role=radio]:has-text('En el consultorio')", "al_decir": "elijo En el consultorio"},
                R(f"{PANEL} :text('Identidad: últimos 4 dígitos')", 3500, al_decir="los últimos cuatro dígitos"),
            ],
        },
        {
            "id": "04-identidad", "capitulo": "La paciente confirma que es ella", "rotulo": "Identidad",
            "ruta": "Página de firma (lo que ve la paciente)",
            "texto_pantalla": "Últimos 4 dígitos de la cédula · enlace personal",
            "narracion": (
                "Ahora es el turno de la paciente. Pulso Abrir para firmar y le paso la pantalla, o la tableta. Se abre la "
                "página de firma, con el nombre del centro arriba. Esta es su página: "
                "no ve nada del sistema, solo su documento. Escribe los últimos cuatro dígitos de su cédula y "
                "pulsa Continuar."
            ),
            "acciones": [
                {"click": f"{PANEL} button:has-text('Abrir para firmar')", "al_decir": "Pulso Abrir para firmar"},
                R(".pc__lead", 3000, al_decir="Esta es su página"),
                {"escribir": {"sel": "input[formcontrolname='answer']", "texto": "0011"}, "al_decir": "Escribe los últimos"},
                {"click": "button:has-text('Continuar')", "al_decir": "pulsa Continuar"},
            ],
        },
        {
            "id": "05-firma", "capitulo": "Leer, declarar y firmar", "rotulo": "La firma",
            "ruta": "Página de firma › Lectura › Firma",
            "texto_pantalla": "Lo lee hasta el final, marca cada declaración y firma con el dedo",
            "narracion": (
                "En la pantalla siguiente está el documento. Primero lo lee completo: el botón para seguir solo se activa al llegar al final. Si no está de "
                "acuerdo, lo dice aquí y queda registrado. Pulsa Continuar. Ahora marca cada declaración, solo si "
                "es cierta: que lo leyó completo, que pudo hacer sus preguntas, que sabe que puede revocarlo, y "
                "que autoriza el procedimiento. Firma como paciente; si fuera un menor, firmaría "
                "su representante. Su nombre ya está puesto. Dibuja su firma con el dedo; si no le gusta, la limpia y "
                "vuelve a empezar. Cuando está conforme, pulsa Aceptar y firmar."
            ),
            "acciones": [
                {"click": ".pc__doc", "al_decir": "lo lee completo"},
                {"presionar": {"tecla": "End"}, "al_decir": "al llegar al final"},
                R("button:has-text('No estoy de acuerdo')", 2500, al_decir="Si no está de"),
                {"click": "button:has-text('Continuar')", "al_decir": "Pulsa Continuar"},
                {"click": "mat-checkbox >> nth=0", "al_decir": "que lo leyó completo"},
                {"click": "mat-checkbox >> nth=1", "al_decir": "pudo hacer sus"},
                {"click": "mat-checkbox >> nth=2", "al_decir": "que puede revocarlo"},
                {"click": "mat-checkbox >> nth=3", "al_decir": "que autoriza el"},
                R("mat-radio-group, :text('Firmo como')", 3000, al_decir="Firma como paciente"),
                R("input[formcontrolname='signerName']", 2000, al_decir="Su nombre"),
                {"firmar": "canvas", "al_decir": "Dibuja su firma"},
                {"click": "button:has-text('Aceptar y firmar')", "al_decir": "pulsa Aceptar y firmar"},
            ],
        },
        {
            "id": "06-listo", "capitulo": "La constancia", "rotulo": "Consentimiento aceptado",
            "ruta": "Página de firma › Listo",
            "texto_pantalla": "Código de verificación y copia firmada",
            "narracion": (
                "Listo. La firma queda con fecha y hora, y con un código de verificación. La paciente puede "
                "descargar su copia firmada aquí mismo, o pedirla impresa en el centro. Y si cambia de opinión, puede "
                "revocarlo antes del procedimiento."
            ),
            "acciones": [
                R(":text('Consentimiento aceptado')", 2500, al_decir="Listo"),
                R(":text('Código de verificación') >> xpath=..", 2000, al_decir="un código de verificación"),
                R("button:has-text('Descargar mi consentimiento'), a:has-text('Descargar mi consentimiento')", 3000,
                  al_decir="descargar su copia"),
                R(":text('Puede revocar este consentimiento')", 3000, al_decir="si cambia de opinión"),
            ],
        },
        {
            "id": "07-expediente", "capitulo": "En el expediente", "rotulo": "En el expediente",
            "navegar": "/patients/545?tab=tpl-576", "al_decir_navegar": "recupera su pantalla",
            "ruta": "Pacientes › ficha › Consentimiento › Aceptado",
            "texto_pantalla": "Aceptado · constancia, bitácora y firma de la doctora",
            "narracion": (
                "La doctora recupera su pantalla y vuelve a la ficha de Rosa, en la pestaña del consentimiento. Mientras "
                "carga, fíjate en algo: la paciente nunca vio el resto del sistema, solo su documento. En el "
                "historial está el registro que acabamos de preparar, con su número. Lo abro. Dice Aceptado, cuándo "
                "lo abrió y cuándo firmó, por qué canal y quién firmó. Ver constancia descarga el documento con la "
                "evidencia, y Revocar registra que la paciente se arrepintió. Debajo, la bitácora guarda cada "
                "paso. El texto aceptado queda congelado. Por último firmo yo el registro: pulso Firmar. Me pide "
                "mi contraseña, para confirmar que soy yo quien firma. La escribo. Nadie más puede firmar por mí. Ahora confirmo con Firmar. Queda "
                "cerrado, y solo se corrige por enmienda."
            ),
            "acciones": [
                R("tr:has-text('RC-2026-00001')", 3000, al_decir="En el historial"),
                {"click": "tr:has-text('RC-2026-00001') button", "al_decir": "Lo abro"},
                R(f"{PANEL} .cp__status, {PANEL} :text('Aceptado') >> nth=0", 2500, al_decir="Dice Aceptado", cursor=False),
                R(f"{PANEL} dl, {PANEL} :text('Canal')", 2000, al_decir="por qué canal"),
                R(f"{PANEL} button:has-text('Ver constancia')", 2500, al_decir="Ver constancia"),
                R(f"{PANEL} button:has-text('Revocar')", 2500, al_decir="Revocar registra"),
                R(f"{PANEL} :text('Bitácora')", 3000, al_decir="la bitácora"),
                {"click": "button:has(mat-icon:text('draw'))", "al_decir": "pulso Firmar"},
                R("mat-dialog-container", 2500, al_decir="Me pide", cursor=False),
                {"escribir": {"sel": "mat-dialog-container input[type='password']", "texto": "AnaPerez2026!"},
                 "al_decir": "La escribo"},
                {"click": "mat-dialog-container button:has-text('Firmar')", "al_decir": "confirmo con Firmar"},
            ],
        },
        {
            "id": "08-resumen", "capitulo": "Los consentimientos de la paciente", "rotulo": "Resumen",
            "ruta": "Pacientes › ficha › Resumen › Consentimientos",
            "texto_pantalla": "Todos sus consentimientos y su estado, en el Resumen",
            "narracion": (
                "Una última cosa. En el Resumen de la ficha, el bloque de consentimientos reúne todos los de la paciente con su "
                "estado: sin enviar, enviado, aceptado o revocado. Así, antes del procedimiento, cualquiera ve si "
                "ya firmó. Con esto termina el video de consentimiento informado."
            ),
            "acciones": [
                {"click": "button.tab:has-text('Resumen')", "al_decir": "En el Resumen"},
                R("app-patient-consents-block", 5000, al_decir="el bloque de consentimientos"),
                R("app-patient-consents-block :text('Aceptado') >> nth=0", 3500, al_decir="si ya firmó"),
            ],
        },
    ]
    return guion(
        "consentimiento-01-firma", "Consentimiento informado: redactar, firmar y archivar",
        "Cómo se prepara un consentimiento informado en RegiSalud: la doctora llena el procedimiento, los riesgos "
        "y las alternativas, la paciente confirma su identidad, lo lee, declara y firma con el dedo en el "
        "consultorio (o desde un enlace por correo), y el registro queda aceptado, con constancia, bitácora y la "
        "firma de la doctora.",
        pasos, comentario="Estado: consentimiento.mjs. Sesión: Ana Pérez.", portada_s=4,
        sesion=ANA["sesion"], js_global=ANA["js_global"],
    )


if __name__ == "__main__":
    print(consentimiento_01())
