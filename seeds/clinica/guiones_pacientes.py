"""Serie «Pacientes» (RegiSalud), 2026-11.

  python3 seeds/clinica/guiones_pacientes.py      → escribe guiones/pacientes-0N-*.json

Estado previo de cada video: `node seeds/clinica/pacientes.mjs` (y `citas.mjs C` para que haya citas).
"""
from comun import guion

R = lambda texto, ms=3500, **k: {"resaltar": texto, "durante_ms": ms, **k}  # noqa: E731


def pacientes_01():
    pasos = [
        {
            "id": "01-consola", "capitulo": "La consola de Pacientes", "rotulo": "Pacientes",
            "navegar": "/home", "ruta": "Pacientes",
            "texto_pantalla": "Pacientes · la lista y la ficha en una sola pantalla",
            "narracion": (
                "En esta serie vemos los pacientes: su registro, su ficha y su acceso al portal. Entro a Pacientes, "
                "en el menú de la izquierda. Arriba dice cuántos pacientes tiene el centro. A la izquierda está la "
                "lista, y la ficha del paciente que elijo se abre aquí mismo, sin perder la búsqueda. Buscar "
                "paciente encuentra por nombre, cédula o número de expediente, y tolera pequeñas faltas de "
                "ortografía. El filtro de estado muestra los activos, los inactivos o todos. El engranaje abre los "
                "ajustes del módulo, y Ocultar la lista deja todo el ancho a la ficha."
            ),
            "acciones": [
                {"click": "a.rail-item[aria-label='Pacientes']", "al_decir": "Entro a Pacientes"},
                R("h1, .page-title, :text('pacientes registrados')", 3000, al_decir="cuántos pacientes"),
                R(".sel__order >> xpath=ancestor::*[2]", 3500, al_decir="está la lista"),
                {"escribir": {"sel": ".pc__search input", "texto": "Rosa"}, "al_decir": "Buscar paciente encuentra"},
                R(".pc__filter", 3000, al_decir="El filtro de estado"),
                R("button.pc__settings", 2500, al_decir="El engranaje"),
                R("button.pc__list-toggle", 2500, al_decir="Ocultar la lista"),
            ],
        },
        {
            "id": "02-documento", "capitulo": "Nuevo paciente: el documento", "rotulo": "Nuevo paciente",
            "ruta": "Pacientes › Nuevo paciente",
            "texto_pantalla": "Tipo de documento · cédula, pasaporte, extranjero o sin documento",
            "narracion": (
                "Llega una paciente nueva. La forma más común de registrarla es aquí, con Nuevo paciente. También "
                "puede registrarse sola, con un enlace de registro, o nacer de una reserva por internet. Pulso "
                "Nuevo paciente. Empiezo por el tipo de documento: cédula, pasaporte, documento extranjero o sin "
                "documento. Dejo cédula y escribo el número, sin guiones, y paso al campo siguiente. Al terminar, el "
                "sistema avisa enseguida que ese documento ya pertenece a otra "
                "paciente, con su nombre y su expediente: no se registran dos personas con el mismo documento. Me "
                "equivoqué de número, así que pulso Cambiar Documento y escribo el correcto."
            ),
            "acciones": [
                R("button.pc__new", 3500, al_decir="Llega una paciente nueva"),
                R("button.pc__settings", 3000, al_decir="con un enlace de registro"),
                {"click": "button.pc__new", "al_decir": "Pulso Nuevo paciente"},
                R("mat-form-field:has([formcontrolname='documentType'])", 4000, al_decir="el tipo de documento"),
                {"escribir": {"sel": "input[formcontrolname='documentNumber']", "texto": "40205550011"},
                 "al_decir": "escribo el número"},
                R("mat-dialog-container", 6000, al_decir="El sistema avisa", cursor=False),
                {"click": "mat-dialog-container button:has-text('Cambiar Documento')", "al_decir": "pulso Cambiar Documento"},
                {"escribir": {"sel": "input[formcontrolname='documentNumber']", "texto": "40205550177"},
                 "al_decir": "escribo el correcto"},
            ],
        },
        {
            "id": "03-datos", "capitulo": "Nombre, nacimiento y contacto", "rotulo": "Datos básicos",
            "ruta": "Pacientes › Nuevo paciente › Información básica",
            "texto_pantalla": "Nombre, apellidos, fecha de nacimiento, género y contacto",
            "narracion": (
                "Ahora el nombre, tal como aparece en su cédula: Sofía, con su tilde. Después el primer apellido, "
                "que es Ramírez. El segundo apellido es opcional, pero lo pongo igual: Castro, el de su madre. Ahora la fecha de "
                "nacimiento, que es importante porque "
                "con ella el sistema calcula la edad y sabe si es menor de edad. Abro el género y elijo femenino. "
                "Después abro el estado civil y elijo soltera. En contacto personal va su teléfono móvil, que es el de los "
                "recordatorios por WhatsApp, y su correo, donde le llegan las confirmaciones de sus citas."
            ),
            "acciones": [
                {"escribir": {"sel": "input[formcontrolname='name']", "texto": "Sofía"}, "al_decir": "tal como aparece"},
                {"escribir": {"sel": "input[formcontrolname='firstLastName']", "texto": "Ramírez"}, "al_decir": "Después el primer apellido"},
                {"escribir": {"sel": "input[formcontrolname='secondLastName']", "texto": "Castro"}, "al_decir": "lo pongo igual"},
                {"escribir": {"sel": "input[formcontrolname='birthDate']", "texto": "15/03/1990"}, "al_decir": "Ahora la fecha"},
                {"click": "mat-select[formcontrolname='gender']", "al_decir": "Abro el género"},
                {"click": "mat-option:has-text('Femenino')", "al_decir": "elijo femenino"},
                {"click": "mat-select[formcontrolname='maritalStatus']", "al_decir": "abro el estado civil"},
                {"click": "mat-option:has-text('Soltero')", "al_decir": "elijo soltera"},
                {"escribir": {"sel": "input[formcontrolname='personalMobilePhone']", "texto": "8095550170"},
                 "al_decir": "su teléfono móvil"},
                {"escribir": {"sel": "input[formcontrolname='personalEmail']", "texto": "sofia.ramirez@correo.test"},
                 "al_decir": "y su correo"},
            ],
        },
        {
            "id": "04-guardar", "capitulo": "El resto de la ficha y guardar", "rotulo": "Crear paciente",
            "ruta": "Pacientes › Nuevo paciente › Crear Paciente",
            "texto_pantalla": "Secciones opcionales · portal del paciente · Crear Paciente",
            "narracion": (
                "Más abajo están las demás secciones: seguro de salud, datos sociodemográficos, sangre, "
                "discapacidad, información social y contactos. Se llenan si el centro las pide; cuáles se ven y "
                "cuáles son obligatorias se decide en los ajustes del módulo. Si la paciente trae seguro, aquí se "
                "registra su afiliación a la ARS. Al final, la casilla del portal del paciente le envía un código "
                "para que entre a ver sus citas y resultados; la vemos en otro video. Pulso Crear Paciente. El aviso "
                "confirma que se creó, y la ficha se abre con su número de expediente, que el sistema asigna solo y que la identifica en "
                "todo lo que se le haga."
            ),
            "acciones": [
                R(".section-title:has-text('Seguro de salud')", 3500, al_decir="Más abajo"),
                R(".section-title:has-text('Contactos y referencias')", 3500, al_decir="y contactos"),
                R(".section-title:has-text('Seguro de salud')", 3500, al_decir="Si la paciente trae seguro"),
                R(".section-title:has-text('Portal del paciente'), h2:has-text('Portal del paciente')", 4000, al_decir="la casilla del portal"),
                {"click": "button:has-text('Crear Paciente')", "al_decir": "Pulso Crear Paciente"},
                R("mat-snack-bar-container", 2500, al_decir="El aviso", cursor=False),
                R(":text('EXP-2026')", 4000, al_decir="número de expediente"),
            ],
        },

        {
            "id": "05-menor", "capitulo": "Registrar a un menor", "rotulo": "Paciente menor",
            "ruta": "Pacientes › Nuevo paciente (menor de edad)",
            "texto_pantalla": "Menor de edad · sin documento propio, con su representante",
            "narracion": (
                "Un niño no tiene cédula, y el sistema lo maneja distinto. Juan Carlos Batista trae a su hijo "
                "Mateo. Pulso Nuevo paciente otra vez. Escribo el nombre del niño: Mateo, así, sin más. Y después su apellido, "
                "el mismo del padre: Batista. Antes del documento va la fecha de nacimiento, porque es la que dice que es menor de "
                "edad. Ahora en tipo de documento aparece la "
                "opción Menor de Edad, que no pide número. La elijo."
            ),
            "acciones": [
                {"click": "button.pc__new", "al_decir": "Pulso Nuevo paciente"},
                {"escribir": {"sel": "input[formcontrolname='name']", "texto": "Mateo"}, "al_decir": "Escribo el nombre del niño"},
                {"escribir": {"sel": "input[formcontrolname='firstLastName']", "texto": "Batista"}, "al_decir": "Después su apellido"},
                {"escribir": {"sel": "input[formcontrolname='birthDate']", "texto": "11/02/2019"}, "al_decir": "Antes del documento"},
                {"click": "mat-select[formcontrolname='documentType']", "al_decir": "en tipo de documento"},
                R("mat-option:has-text('Menor de Edad')", 2500, al_decir="la opción Menor de Edad", cursor=False),
                {"click": "mat-option:has-text('Menor de Edad')", "al_decir": "La elijo"},
            ],
        },
        {
            "id": "06-representante", "capitulo": "El representante legal", "rotulo": "Representante legal",
            "ruta": "Pacientes › Nuevo paciente › Contactos y referencias",
            "texto_pantalla": "Un menor necesita representante legal: nombre, relación y teléfono",
            "narracion": (
                "Un paciente menor de dieciocho años necesita un representante legal, y el formulario ya agregó "
                "ese contacto en Contactos y referencias. Escribo el nombre del padre: Juan Carlos Batista, completo, como en su cédula. "
                "Después su teléfono principal, que es a donde se llama por el niño. La relación queda como tutor legal; también puede ser padre o madre. Si el "
                "representante ya es paciente del centro, se puede indicar su ficha. Pulso Crear Paciente: el aviso "
                "lo confirma, y Mateo queda registrado con su expediente y su edad. Al cumplir dieciocho años deja de figurar como "
                "menor solo, porque la edad sale siempre de la fecha de nacimiento."
            ),
            "acciones": [
                R(".section-title:has-text('Contactos y referencias')", 3500, al_decir="representante legal"),
                {"escribir": {"sel": "mat-form-field:has-text('Nombre del contacto') input >> nth=-1",
                              "texto": "Juan Carlos Batista"}, "al_decir": "Escribo el nombre del padre"},
                {"escribir": {"sel": "mat-form-field:has-text('Teléfono principal') input >> nth=-1",
                              "texto": "8095550122"}, "al_decir": "Después su teléfono"},
                R("mat-form-field:has-text('Parentesco') >> nth=-1", 3500, al_decir="La relación"),
                {"click": "button:has-text('Crear Paciente')", "al_decir": "Pulso Crear Paciente"},
                R("mat-snack-bar-container", 2500, al_decir="lo confirma, y", cursor=False),
                R(":text('años') >> nth=0", 4000, al_decir="su expediente y su edad"),
            ],
        },
    ]
    return guion(
        "pacientes-01-registrar", "Pacientes · Parte 1: registrar un paciente (adulto y menor)",
        "Primera parte de la serie de Pacientes de RegiSalud: la consola de Pacientes (búsqueda, estado, ajustes), "
        "registrar un paciente adulto con su documento (y el aviso de documento ya registrado), sus datos y su "
        "contacto, las secciones que pide el centro, el número de expediente, y registrar a un menor con su "
        "representante legal.",
        pasos, comentario="Estado: pacientes.mjs (sin Sofía Ramírez).", portada_s=4,
    )


if __name__ == "__main__":
    for f in (pacientes_01,):
        print(f())
