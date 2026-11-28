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


def pacientes_02():
    pasos = [
        {
            "id": "01-cabecera", "capitulo": "La ficha: cabecera y pestañas", "rotulo": "La ficha del paciente",
            "navegar": "/patients", "ruta": "Pacientes › Rosa Elena Martínez",
            "texto_pantalla": "La ficha · cabecera, acciones y pestañas",
            "narracion": (
                "En esta parte vemos la ficha del paciente: todo lo que el centro sabe de él, en un solo lugar. Estoy "
                "en Pacientes. En la lista, abro la ficha de Rosa Elena Martínez. Arriba está la cabecera: su nombre, si está activa, su "
                "expediente, la edad, la cédula y el teléfono, con atajos para llamar, escribir por WhatsApp o por "
                "correo. A la derecha, Agendar cita abre el formulario de la cita con la paciente ya puesta, y "
                "Nueva evolución empieza una nota clínica. Debajo están las pestañas: el resumen, la historia "
                "clínica, la ficha con sus datos, la agenda con sus citas, la cuenta con sus facturas y saldo, y "
                "el ingreso si la hospitalizan. En la fila de plantillas están los formularios clínicos que el "
                "centro usa, como el consentimiento informado."
            ),
            "acciones": [
                {"click": "button:has-text('Rosa Elena')", "al_decir": "abro la ficha"},
                R(".ph, app-patient-header", 5000, al_decir="la cabecera", cursor=False),
                R("button:has-text('Agendar cita')", 3000, al_decir="Agendar cita abre"),
                R("button:has-text('Nueva evolución')", 2500, al_decir="Nueva evolución"),
                R("button.tab:has-text('Resumen') >> xpath=..", 6000, al_decir="las pestañas"),
                R(":text('Consentimiento Informado') >> nth=0", 3000, al_decir="la fila de plantillas"),
            ],
        },
        {
            "id": "02-alergia", "capitulo": "Alergias, medicación y alertas", "rotulo": "Alergias y alertas",
            "ruta": "Pacientes › ficha › Resumen › Alergias",
            "texto_pantalla": "Alergias, medicación habitual y alertas médicas",
            "narracion": (
                "El resumen muestra la situación clínica, las últimas evoluciones, los consentimientos y, a la "
                "derecha, lo que nadie debe pasar por alto: alertas médicas, alergias y medicación activa. La "
                "paciente es alérgica a la penicilina, así que en alergias pulso Agregar, y se abre la ventana. En "
                "alérgeno escribo el nombre: penicilina, como lo dice la paciente. Ahora abro el tipo, y en la lista elijo medicamento. "
                "Después abro la severidad, y elijo severa, porque le cuesta respirar. En reacción escribo lo que "
                "le pasa: ronchas y falta de aire. Las fechas y las notas son opcionales. Con eso, pulso el botón "
                "Agregar. La alergia queda en la lista y, por ser grave, también "
                "en la cabecera, a la vista de quien abra la ficha. La medicación habitual y las alertas médicas "
                "se registran igual, con su botón Agregar. Las escribe el personal médico; recepción solo las ve."
            ),
            "acciones": [
                R(":text('Situación clínica')", 3000, al_decir="la situación clínica"),
                R(":text('Alertas médicas') >> xpath=..", 3500, al_decir="lo que nadie debe pasar"),
                {"click": "button:has-text('Agregar') >> nth=1", "al_decir": "en alergias pulso Agregar"},
                R("mat-dialog-container", 1500, al_decir="se abre la ventana", cursor=False),
                {"escribir": {"sel": "mat-dialog-container input[formcontrolname='allergen']", "texto": "Penicilina"},
                 "al_decir": "escribo el nombre: penicilina"},
                {"click": "mat-dialog-container mat-select[formcontrolname='allergyType']", "al_decir": "abro el tipo"},
                {"click": "mat-option:has-text('Medicamento')", "al_decir": "elijo medicamento"},
                {"click": "mat-dialog-container mat-select[formcontrolname='severity']", "al_decir": "abro la severidad"},
                {"click": "mat-option:has-text('Severa')", "al_decir": "elijo severa"},
                {"escribir": {"sel": "mat-dialog-container [formcontrolname='reaction']", "texto": "Ronchas y falta de aire"},
                 "al_decir": "En reacción escribo"},
                {"click": "mat-dialog-container button:has-text('Agregar')", "al_decir": "pulso el botón Agregar"},
                R("mat-snack-bar-container", 2500, al_decir="queda en la lista", cursor=False),
                R(":text('Penicilina') >> nth=0", 3000, al_decir="por ser grave"),
                R(":text('Medicación activa') >> xpath=..", 3500, al_decir="La medicación habitual"),
            ],
        },
        {
            "id": "03-archivos", "capitulo": "Datos, archivos y estado", "rotulo": "Ficha y archivos",
            "ruta": "Pacientes › ficha › Ficha",
            "texto_pantalla": "Ficha · datos editables, archivos del paciente y estado",
            "narracion": (
                "Terminado el resumen, ahora paso a la pestaña Ficha, que tiene los mismos datos del registro, editables, y se guardan con Guardar. Más "
                "abajo están los archivos del paciente: aquí se suben sus estudios, informes o documentos. Pulso "
                "Agregar archivo y elijo el PDF de su hemograma. Escribo el nombre con el que se va a buscar: "
                "hemograma. La fecha es la del estudio; la dejo en hoy. Pulso Subir. El archivo queda en la lista, guardado en la nube y no en el equipo, para "
                "descargarlo, editarlo o eliminarlo. Al final está el estado del paciente: si se desmarca Paciente "
                "activo, deja de salir al agendar, pero conserva toda su historia; un paciente con actividad no se "
                "borra, se inactiva."
            ),
            "acciones": [
                {"click": "button.tab:has-text('Ficha')", "al_decir": "paso a la pestaña Ficha"},
                R(".section-title:has-text('Información básica')", 3500, al_decir="los mismos datos"),
                R(".section-title:has-text('Archivos del paciente')", 3500, al_decir="los archivos del paciente"),
                {"click": "button:has-text('Agregar archivo')", "al_decir": "Pulso Agregar archivo"},
                {"subir": {"sel": "app-patient-file-section input[type='file']", "archivo": "seeds/clinica/archivos/hemograma-rosa-elena.pdf",
                           "ancla": "app-patient-file-section .drop-text"}, "al_decir": "elijo el PDF"},
                {"escribir": {"sel": "app-patient-file-section input[formcontrolname='name']", "texto": "Hemograma"},
                 "al_decir": "Escribo el nombre"},
                R("app-patient-file-section input[formcontrolname='date']", 2500, al_decir="La fecha es"),
                {"click": "app-patient-file-section button:has-text('Subir'), app-patient-file-section button:has-text('Guardar')",
                 "al_decir": "Pulso Subir"},
                R("mat-snack-bar-container", 2500, al_decir="El archivo queda", cursor=False),
                R("app-patient-file-section :text('Hemograma') >> nth=0", 3000, al_decir="guardado en la nube"),
                R(".section-title:has-text('Estado del paciente')", 4500, al_decir="el estado del paciente"),
            ],
        },
    ]
    return guion(
        "pacientes-02-ficha", "Pacientes · Parte 2: la ficha del paciente",
        "Segunda parte de la serie de Pacientes de RegiSalud: la cabecera de la ficha y sus atajos, las pestañas, "
        "registrar una alergia (y dónde van la medicación y las alertas médicas), subir un archivo del paciente y "
        "el estado activo o inactivo.",
        pasos, comentario="Estado: pacientes.mjs (Rosa Elena sin alergias ni archivos).", portada_s=4,
    )


def pacientes_03():
    I = "mat-form-field:has-text('{}') input"
    pasos = [
        {
            "id": "01-campos", "capitulo": "Qué campos pide la ficha", "rotulo": "Campos de la ficha",
            "navegar": "/patients", "ruta": "Pacientes › Ajustes › Campos de la ficha",
            "texto_pantalla": "Campos de la ficha · requerido, visible u oculto",
            "narracion": (
                "Cada centro decide qué le pide a sus pacientes. En Pacientes, el engranaje abre los ajustes del "
                "módulo, con dos pestañas. En Campos de la ficha está cada campo, sección por sección. En "
                "visibilidad se elige si es requerido, visible u oculto: un campo requerido se exige al registrar "
                "desde la pantalla y desde el enlace, y uno oculto desaparece del formulario. También se le puede "
                "cambiar la etiqueta, poner un texto de ayuda y moverlo de orden con las flechas. Toda una sección "
                "se oculta con su propia visibilidad. Aplicar perfil carga una configuración de fábrica, y los "
                "cambios se guardan con Guardar."
            ),
            "acciones": [
                {"click": "button.pc__settings", "al_decir": "el engranaje abre"},
                R("a:has-text('Campos de la ficha')", 3000, al_decir="dos pestañas"),
                R("mat-form-field.visibility-select >> nth=1", 4500, al_decir="En visibilidad"),
                R("mat-form-field.label-input >> nth=1", 3000, al_decir="cambiar la etiqueta"),
                R("mat-form-field.help-input >> nth=1", 2500, al_decir="un texto de ayuda"),
                R("button:has(mat-icon:text('arrow_downward')) >> nth=1", 2500, al_decir="con las flechas"),
                R("mat-form-field.section-visibility-select >> nth=0", 3000, al_decir="Toda una sección"),
                R("button:has-text('Aplicar perfil')", 3000, al_decir="Aplicar perfil"),
            ],
        },
        {
            "id": "02-enlace", "capitulo": "Generar un enlace de registro", "rotulo": "Enlace de registro",
            "ruta": "Pacientes › Ajustes › Enlaces de registro",
            "texto_pantalla": "Enlace de registro · el paciente llena su ficha desde el teléfono",
            "narracion": (
                "La otra pestaña son los enlaces de registro: el paciente llena sus datos desde su teléfono, antes "
                "de llegar, y recepción no tiene que escribirlos. Pulso Generar enlace. Hay dos tipos: el temporal vence a los "
                "siete días o en la fecha que elija; el permanente no vence y sirve para publicarlo en la página "
                "del centro. Lo dejo temporal y escribo el nombre del paciente, Tomás Polanco, para reconocer el "
                "enlace en la lista. Pulso Generar enlace. El sistema lo copia al portapapeles: se lo mando al "
                "paciente por WhatsApp o por correo, porque el sistema no lo envía."
            ),
            "acciones": [
                {"click": "a:has-text('Enlaces de registro')", "al_decir": "los enlaces de registro"},
                {"click": "button:has-text('Generar enlace')", "al_decir": "antes de llegar, y recepción"},
                R("mat-dialog-container mat-form-field:has([formcontrolname='linkType'])", 4500, al_decir="Hay dos tipos", cursor=False),
                {"escribir": {"sel": "mat-dialog-container input[formcontrolname='patientName']", "texto": "Tomás Polanco"},
                 "al_decir": "escribo el nombre del paciente"},
                {"click": "mat-dialog-container button:has-text('Generar enlace')", "al_decir": "Pulso Generar enlace. El sistema"},
                R("mat-dialog-container", 4000, al_decir="lo copia al portapapeles", cursor=False),
                {"click": "mat-dialog-container button:has-text('Entendido')", "al_decir": "porque el sistema no lo envía"},
            ],
        },
        {
            "id": "03-paciente", "capitulo": "El paciente llena su registro", "rotulo": "Registro del paciente",
            "setup": {"tipo": "shell", "cmd": "node seeds/clinica/ultimo-enlace.mjs", "guardar_en": "token"},
            "navegar": "/intake/{{token}}", "al_decir_navegar": "abre el enlace",
            "ruta": "Enlace de registro (lo que ve el paciente)",
            "texto_pantalla": "Registro del paciente · sus datos, en pasos",
            "narracion": (
                "Ahora me pongo en el lugar del paciente, que abre el enlace en su teléfono. El formulario va por "
                "pasos. Arriba puede entrar a su portal si ya tiene cuenta; no hace falta para registrarse. Escribe "
                "su nombre: Tomás, como en su cédula. Ahora su primer apellido, que es Polanco. En tipo de documento "
                "abre la lista y elige cédula, que es su documento. Ahora escribe su número, sin guiones ni espacios. Y por último, su "
                "fecha de nacimiento, con el día primero y después el mes. Con eso, pulsa Siguiente. Este paso tiene sus datos sociales, y es opcional, así que sigue. El "
                "siguiente es su información médica, como el tipo de sangre; sigue. Luego viene la dirección; "
                "sigue. Después sus contactos; sigue. La información de discapacidad; sigue. Los datos sociales y "
                "administrativos; sigue. Y llega al último paso."
            ),
            "acciones": [
                R(":text('Paso 1 de')", 3000, al_decir="va por pasos"),
                R("button:has-text('Ingresar al portal')", 3000, al_decir="entrar a su portal"),
                {"escribir": {"sel": I.format("Nombre") + " >> nth=0", "texto": "Tomás"}, "al_decir": "Escribe su nombre"},
                {"escribir": {"sel": I.format("Primer apellido"), "texto": "Polanco"}, "al_decir": "Ahora su primer apellido"},
                {"click": "mat-form-field:has-text('Tipo de documento') mat-select", "al_decir": "abre la lista"},
                {"click": "mat-option:has-text('Cédula')", "al_decir": "elige cédula"},
                {"escribir": {"sel": I.format("Número de documento"), "texto": "40205550188"}, "al_decir": "Ahora escribe su número"},
                {"escribir": {"sel": I.format("Fecha de nacimiento"), "texto": "20/06/1987"}, "al_decir": "su fecha de nacimiento"},
                {"click": "button:has-text('Siguiente')", "al_decir": "Con eso, pulsa Siguiente"},
                {"click": "button:has-text('Siguiente')", "al_decir": "opcional, así que sigue"},
                {"click": "button:has-text('Siguiente')", "al_decir": "tipo de sangre; sigue"},
                {"click": "button:has-text('Siguiente')", "al_decir": "la dirección; sigue"},
                {"click": "button:has-text('Siguiente')", "al_decir": "sus contactos; sigue"},
                {"click": "button:has-text('Siguiente')", "al_decir": "discapacidad; sigue"},
                {"click": "button:has-text('Siguiente')", "al_decir": "administrativos; sigue"},
            ],
        },
        {
            "id": "04-enviar", "capitulo": "Enviar el registro", "rotulo": "Enviar el registro",
            "ruta": "Enlace de registro › Enviar Formulario",
            "texto_pantalla": "Enviar · el sistema comprueba el documento",
            "narracion": (
                "En el último paso pulsa Enviar Formulario. El sistema comprueba que no sea un robot y que el "
                "documento no esté ya registrado en el centro, sin decir de quién es. El registro quedó hecho, y "
                "si dejó su correo le llega la confirmación."
            ),
            "acciones": [
                {"click": "button:has-text('Enviar Formulario')", "al_decir": "pulsa Enviar Formulario"},
                R("mat-card, .success, .result, main", 4000, al_decir="El registro quedó hecho", cursor=False),
            ],
        },
        {
            "id": "05-ficha", "capitulo": "La ficha nueva en el centro", "rotulo": "La ficha nueva",
            "navegar": "/patients",
            "ruta": "Pacientes",
            "texto_pantalla": "La ficha nace con su número de expediente",
            "narracion": (
                "De vuelta en el centro, Tomás Polanco ya aparece en Pacientes, con su número de expediente, listo "
                "para agendarle. La marca Incompleta avisa que le faltan datos que la ficha pide; recepción los "
                "completa cuando llegue. Si el documento ya existía, el registro se rechaza y el paciente ve que debe "
                "comunicarse con el centro."
            ),
            "acciones": [
                R("button:has-text('Tomás')", 4000, al_decir="ya aparece en Pacientes"),
                R(":text('Incompleta') >> nth=0", 3500, al_decir="La marca Incompleta"),
            ],
        },
    ]
    return guion(
        "pacientes-03-campos-y-enlaces", "Pacientes · Parte 3: campos de la ficha y enlaces de registro",
        "Tercera parte de la serie de Pacientes de RegiSalud: qué campos pide la ficha (requerido, visible u "
        "oculto), generar un enlace de registro temporal o permanente y cómo el paciente llena su registro desde "
        "el teléfono.",
        pasos, comentario="Estado: pacientes.mjs (sin enlaces ni Tomás Polanco).", portada_s=4,
    )


def pacientes_04():
    correo = "rosa.martinez@correo.test"
    PS = "app-portal-staff"
    pasos = [
        {
            "id": "01-config", "capitulo": "Configurar el portal del paciente", "rotulo": "Portal del paciente",
            "navegar": "/agenda/calendar", "ruta": "Calendario › Configurar portal del paciente",
            "texto_pantalla": "Portal del paciente · acceso, citas, reservas y resultados",
            "narracion": (
                "El portal del paciente es la página donde el paciente entra con su correo para ver sus citas y "
                "los resultados que el centro le publica. No da acceso a ninguna pantalla del centro ni a su "
                "historia clínica. Se configura desde el Calendario, con Configurar portal del paciente. Permitir "
                "acceso deja entrar a los pacientes. Mostrar citas les enseña sus citas, y permitir reservas les "
                "deja agendar desde el portal. Los resultados vienen apagados: los enciendo, porque vamos a "
                "publicar un análisis. Si el centro tiene WhatsApp conectado, los códigos de acceso también pueden "
                "ir por ahí. Pulso Guardar configuración, y el aviso confirma que quedó guardada."
            ),
            "acciones": [
                R("button:has-text('Configurar portal del paciente')", 3500, al_decir="la página donde el paciente"),
                R("button:has-text('Reservas sin ficha')", 3000, al_decir="No da acceso"),
                {"click": "button:has-text('Configurar portal del paciente')", "al_decir": "Configurar portal del paciente. Permitir"},
                R("mat-slide-toggle:has-text('Permitir acceso al portal')", 3000, al_decir="acceso deja entrar"),
                R("mat-slide-toggle:has-text('Mostrar citas')", 2500, al_decir="Mostrar citas"),
                R("mat-slide-toggle:has-text('Permitir reservas')", 2500, al_decir="permitir reservas"),
                {"click": "mat-slide-toggle:has-text('Mostrar resultados publicados') button", "al_decir": "los enciendo"},
                R("mat-form-field:has-text('Plantilla de códigos')", 3500, al_decir="WhatsApp conectado"),
                {"click": "button:has-text('Guardar configuración')", "al_decir": "Pulso Guardar configuración"},
                R(":text('Configuración guardada')", 2500, al_decir="quedó guardada", cursor=False),
            ],
        },
        {
            "id": "02-acceso", "capitulo": "Dar acceso a un paciente", "rotulo": "Autorizar un acceso",
            "navegar": "/patients", "ruta": "Pacientes › ficha › Gestionar acceso al portal",
            "texto_pantalla": "Autorizar un acceso · titular o representante, y qué puede ver",
            "narracion": (
                "Cualquier paciente puede crear su cuenta al reservar por internet. Pero el centro también le da "
                "acceso desde su ficha. Abro a Rosa Elena Martínez y paso a la pestaña Ficha. Más abajo está "
                "Gestionar acceso al portal. El tipo de acceso es paciente titular, ella misma; para un niño se "
                "autoriza a su representante. El canal es el correo, y escribo el suyo. Marco lo que podrá ver: "
                "citas, formularios y resultados publicados. Por último, confirmo que verifiqué su identidad y su correo, y "
                "pulso Guardar y enviar código. Le llega un código para entrar."
            ),
            "acciones": [
                {"click": "button:has-text('Rosa Elena')", "al_decir": "Abro a Rosa Elena"},
                {"click": "button.tab:has-text('Ficha')", "al_decir": "la pestaña Ficha"},
                R(f"{PS} h3:has-text('Autorizar')", 3000, al_decir="Gestionar acceso al portal"),
                R(f"{PS} mat-form-field:has-text('Tipo de acceso')", 4000, al_decir="El tipo de acceso"),
                {"escribir": {"sel": f"{PS} mat-form-field:has-text('Correo de quien') input", "texto": correo},
                 "al_decir": "escribo el suyo"},
                {"click": f"{PS} mat-checkbox:has-text('Resultados publicados')", "al_decir": "resultados publicados"},
                {"click": f"{PS} mat-checkbox.check", "al_decir": "confirmo que verifiqué"},
                {"click": f"{PS} button:has-text('Guardar y enviar código')", "al_decir": "pulso Guardar y enviar código"},
                R(":text('Acceso guardado')", 3500, al_decir="Le llega un código", cursor=False),
            ],
        },
        {
            "id": "03-resultado", "capitulo": "Publicar un resultado", "rotulo": "Publicar un resultado",
            "ruta": "Pacientes › ficha › Resultados para el portal",
            "texto_pantalla": "Resultados para el portal · un PDF que el paciente descarga",
            "narracion": (
                "Justo debajo están los resultados para el portal. Escribo el título que verá la paciente: "
                "hemograma completo, tal como lo entregó el laboratorio. Ahora pulso Seleccionar PDF y elijo el archivo del laboratorio. Pulso Publicar para "
                "este paciente. El resultado queda en la lista, y desde aquí se puede retirar. Publicarlo no lo "
                "agrega a los archivos de la ficha: son cosas distintas."
            ),
            "acciones": [
                {"escribir": {"sel": f"{PS} mat-form-field:has-text('Título del resultado') input", "texto": "Hemograma completo"},
                 "al_decir": "Escribo el título"},
                {"subir": {"sel": f"{PS} input[type='file']", "archivo": "seeds/clinica/archivos/resultado-hemograma.pdf",
                           "ancla": f"{PS} button:has-text('Seleccionar PDF')"}, "al_decir": "Ahora pulso Seleccionar PDF"},
                {"click": f"{PS} button:has-text('Publicar para este paciente')", "al_decir": "Pulso Publicar"},
                R(f"{PS} button:has-text('Retirar')", 3500, al_decir="se puede retirar"),
            ],
        },
        {
            "id": "04-entrar", "capitulo": "El paciente entra a su portal", "rotulo": "Entrar al portal",
            "navegar": "/portal-paciente/los-prados", "al_decir_navegar": "entra al portal",
            "ruta": "Portal del paciente (lo que ve el paciente)",
            "texto_pantalla": "Portal del paciente · correo y código de seis dígitos",
            "narracion": (
                "Ahora la paciente entra al portal, desde el enlace del correo o desde el enlace de reservas del "
                "centro. Pulsa Ingresar al portal. Escribe su correo, el mismo que le dio al centro, y después pulsa "
                "Continuar. Le llega un código de seis dígitos, que vence en "
                "treinta minutos."
            ),
            "acciones": [
                {"click": "button:has-text('Ingresar al portal')", "al_decir": "Pulsa Ingresar al portal"},
                {"escribir": {"sel": "#portal-email", "texto": correo}, "al_decir": "Escribe su correo"},
                {"click": "button.btn--primary:has-text('Continuar')", "al_decir": "después pulsa Continuar"},
            ],
        },
        {
            "id": "05-portal", "capitulo": "Sus citas y sus resultados", "rotulo": "Citas y resultados",
            "setup": {"tipo": "shell", "cmd": f"node seeds/clinica/codigo-portal.mjs {correo}", "guardar_en": "codigo"},
            "ruta": "Portal del paciente › Citas y resultados",
            "texto_pantalla": "Sus citas y los resultados publicados",
            "narracion": (
                "Revisa su correo y copia el código. Lo escribe aquí, son seis números, y después pulsa Verificar código. Ya "
                "está dentro. Ve sus citas con su fecha y su estado, "
                "y debajo los resultados que el centro le publicó, que puede descargar en PDF. El portal muestra "
                "las citas, pero no las cancela: para eso usa el enlace de su reserva o llama al centro. En Gestionar "
                "personas autorizadas puede darle acceso a un familiar. Y desde Agendar una cita reserva otra. La sesión "
                "dura ocho horas. Con esto termina la serie de pacientes."
            ),
            "acciones": [
                {"escribir": {"sel": "#portal-code", "texto": "{{codigo}}"}, "al_decir": "Lo escribe aquí"},
                {"click": "button:has-text('Verificar código')", "al_decir": "después pulsa Verificar código"},
                R(":text('Citas') >> nth=0", 3500, al_decir="Ve sus citas"),
                R(":text('Hemograma completo') >> nth=0", 4000, al_decir="los resultados que el centro"),
                R("button:has-text('Descargar PDF'), a:has-text('Descargar PDF')", 3000, al_decir="descargar en PDF"),
                R(":text('Citas') >> nth=0", 3000, al_decir="no las cancela"),
                R(":text('Gestionar personas autorizadas')", 3000, al_decir="Gestionar personas"),
                R(":text('Agendar una cita')", 2500, al_decir="Agendar una cita reserva"),
                R("button:has-text('Cerrar sesión')", 3000, al_decir="La sesión"),
            ],
        },
    ]
    return guion(
        "pacientes-04-portal", "Pacientes · Parte 4: el portal del paciente",
        "Cuarta parte de la serie de Pacientes de RegiSalud: configurar el portal del paciente, dar acceso a un "
        "paciente desde su ficha, publicarle un resultado en PDF y cómo entra con su correo y un código para ver "
        "sus citas y sus resultados.",
        pasos, comentario="Estado: pacientes.mjs (portal sin accesos, resultados apagados) + citas.mjs C.", portada_s=4,
    )


if __name__ == "__main__":
    for f in (pacientes_01, pacientes_02, pacientes_03, pacientes_04):
        print(f())
