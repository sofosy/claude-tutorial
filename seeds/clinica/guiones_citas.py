"""Serie «Citas y turnos» (RegiSalud), regrabada 2026-11 sin tipos de cita.

  python3 seeds/clinica/guiones_citas.py      → escribe guiones/citas-0N-*.json

Estado previo de cada video: ver `seeds/clinica/citas.mjs <estado>`.
"""
from comun import guion

R = lambda texto, ms=3500, **k: {"resaltar": texto, "durante_ms": ms, **k}  # noqa: E731
SCH = "app-doctor-schedule-tab"


def citas_01():
    pasos = [
        {
            "id": "01-medico", "capitulo": "La agenda de un médico", "rotulo": "Disponibilidad del médico",
            "navegar": "/home",
            "texto_pantalla": "Médicos › Agenda › Disponibilidad · la consulta, el horario y los bloqueos",
            "narracion": (
                "En esta serie vemos las citas de principio a fin. Todo empieza por el médico: sin horario, nadie "
                "le puede agendar. Entro a Médicos, en el menú de la izquierda. A la izquierda está la lista de "
                "médicos del centro. Un médico nuevo se registra con Nuevo médico, con su cédula, su exequátur y sus "
                "especialidades; el doctor Luis Gómez, pediatra, ya está registrado, así que lo abro. Recojo la "
                "lista para ganar espacio, y abro la pestaña Agenda. Tiene dos vistas: Citas, las que ya tiene, y "
                "Disponibilidad, que es cuándo y dónde atiende. Abro Disponibilidad. Arriba está el enlace de "
                "reservas del centro: uno solo para todos los médicos. El aviso dice que este doctor todavía no "
                "aparece en él, porque no tiene horario."
            ),
            "acciones": [
                {"click": "a.rail-item[aria-label='Médicos']", "al_decir": "Entro a Médicos"},
                R("button.dsel__new-btn", 3500, al_decir="Nuevo médico"),
                {"click": "button.dsel__row:has-text('Luis Gómez')", "al_decir": "así que lo abro"},
                {"click": "button.dsel__collapse", "al_decir": "Recojo la"},
                {"click": "button.tab:has-text('Agenda')", "al_decir": "la pestaña Agenda"},
                R("button:has-text('Citas') >> nth=0", 2500, al_decir="Citas, las que"),
                {"click": "button:has-text('Disponibilidad')", "al_decir": "Abro Disponibilidad"},
                R("a.center-link__url", 3500, al_decir="enlace de reservas"),
                R(".center-link, app-center-booking-link", 4500, al_decir="El aviso", cursor=False),
            ],
        },
        {
            "id": "02-consulta", "capitulo": "La consulta: precio y autorización", "rotulo": "La consulta",
            "texto_pantalla": "Consulta · precio particular, autorización de la ARS y reserva en línea",
            "narracion": (
                "Debajo está la consulta del médico. Ya no hay tipos de cita: cada médico tiene una sola consulta, "
                "y de aquí salen su precio, su cobro y si la aseguradora de salud, la ARS, exige un permiso previo. En precio particular escribo lo "
                "que paga un paciente sin seguro: dos mil pesos. Es el precio que se cobra y el que ve el paciente "
                "al reservar. Pide autorización de la aseguradora se marca cuando las ARS exigen una autorización "
                "previa para esta consulta: al agendar con seguro, el sistema la pedirá. Este pediatra no la "
                "necesita. Y se puede reservar en el enlace del centro lo deja aparecer en las reservas por "
                "internet. Pulso Guardar, y el aviso de abajo confirma que la consulta quedó guardada."
            ),
            "acciones": [
                R(".consult-price, mat-form-field.consult-price", 2500, al_decir="consulta del médico"),
                R("mat-checkbox:has-text('Pide autorización')", 3000, al_decir="permiso previo"),
                {"escribir": {"sel": "input[formcontrolname='price']", "texto": "2000"}, "al_decir": "En precio particular"},
                R("mat-checkbox:has-text('Pide autorización')", 4500, al_decir="Pide autorización de"),
                R("mat-checkbox:has-text('Se puede reservar')", 3500, al_decir="Y se puede reservar"),
                {"click": "button.consult-save", "al_decir": "Pulso Guardar"},
                R("mat-snack-bar-container", 2500, al_decir="quedó guardada", cursor=False),
            ],
        },
        {
            "id": "03-franja", "capitulo": "El horario de atención", "rotulo": "Horario de atención",
            "texto_pantalla": "Una franja: horas, especialidad, duración del turno, pacientes, modalidad y consultorio",
            "narracion": (
                "Ahora el horario de atención. Cada día de la semana es una fila, y el doctor todavía no atiende "
                "ninguno. Pulso Agregar en el lunes. Una franja es un bloque de horas que se divide en turnos: de "
                "ocho de la mañana a doce. La especialidad es la que atiende en esta franja; sale de las de su "
                "ficha. La duración por turno es la duración de cada cita: treinta minutos. Y pacientes por turno, "
                "uno. La modalidad puede ser presencial o virtual, por videollamada, con su enlace de reunión. Esta "
                "es presencial, así que lleva consultorio: la sala donde atiende. Escribo el nombre de uno que "
                "todavía no existe, y elijo crearlo desde aquí mismo. Se abre la ficha del consultorio, con el nombre "
                "que escribí."
            ),
            "acciones": [
                R(f"{SCH} .day-line:has-text('Lunes')", 2500, al_decir="Cada día"),
                {"click": "button.add-franja >> nth=0", "al_decir": "Pulso Agregar"},
                R(f"{SCH} mat-form-field:has([formcontrolname='startTime'])", 3000, al_decir="de ocho"),
                R(f"{SCH} mat-form-field:has([formcontrolname='specialtyId'])", 3500, al_decir="La especialidad"),
                R(f"{SCH} mat-form-field:has([formcontrolname='slotDurationMinutes'])", 3000, al_decir="La duración por turno"),
                R(f"{SCH} mat-form-field:has([formcontrolname='maxClientsPerSlot'])", 2500, al_decir="pacientes por turno"),
                R(f"{SCH} mat-form-field:has([formcontrolname='allowRemoteService'])", 4000, al_decir="La modalidad"),
                {"escribir": {"sel": f"{SCH} app-custom-select[formcontrolname='consultorioId'] input",
                              "texto": "Consultorio Pediátrico"}, "al_decir": "Escribo el nombre"},
                {"click": "mat-option.cs-create", "al_decir": "elijo crearlo"},
                R("mat-dialog-container", 3000, al_decir="Se abre la ficha", cursor=False),
            ],
        },
        {
            "id": "04-consultorio", "capitulo": "Crear el consultorio", "rotulo": "Nuevo consultorio",
            "texto_pantalla": "Consultorio · código, nombre y ubicación",
            "narracion": (
                "Le pongo un código corto: consultorio "
                "pediatría, en mayúsculas y con un guion en medio, porque es una clave interna. La dirección, el teléfono, el edificio y el piso son opcionales; sirven cuando el centro "
                "tiene varias sedes, porque el paciente ve dónde lo atienden. Pulso Guardar, y el consultorio queda "
                "elegido en la franja. Los consultorios también se manejan en la pestaña Ajustes del médico."
            ),
            "acciones": [
                {"escribir": {"sel": "mat-dialog-container input[formcontrolname='code']", "texto": "CONS-PED"},
                 "al_decir": "un código corto"},
                R("mat-dialog-container mat-form-field:has([formcontrolname='address'])", 3500, al_decir="La dirección"),
                {"click": "mat-dialog-container button:has-text('Guardar')", "al_decir": "Pulso Guardar"},
                R(f"{SCH} app-custom-select[formcontrolname='consultorioId']", 3000, al_decir="queda elegido"),
                R("button.tab:has-text('Ajustes')", 3000, al_decir="pestaña Ajustes"),
            ],
        },
        {
            "id": "05-dias", "capitulo": "Repetir la franja en varios días", "rotulo": "Aplicar a varios días",
            "texto_pantalla": "Aplicar a · la misma franja de lunes a viernes",
            "narracion": (
                "Para no repetir lo mismo cinco veces, en Aplicar a marco el martes. Marco también el miércoles. "
                "Después el jueves. Y por último el viernes. El recuadro azul resume cuántos turnos salen en cada "
                "día. Abajo hay dos opciones de reserva. Visible para pacientes en el enlace de "
                "reservas hace que estas horas se ofrezcan por internet; si se desmarca, solo recepción las puede "
                "usar. Permitir reservas para hoy deja reservar el mismo día. Pulso Agregar franja. El aviso de abajo "
                "confirma que se agregaron las cinco franjas, y cada día muestra ya su horario, su especialidad y su consultorio. Y arriba, el enlace del centro ya dice que el "
                "doctor aparece en las reservas."
            ),
            "acciones": [
                {"click": f"{SCH} button.day-chip:has-text('Mar')", "al_decir": "el martes"},
                {"click": f"{SCH} button.day-chip:has-text('Mié')", "al_decir": "también el miércoles"},
                {"click": f"{SCH} button.day-chip:has-text('Jue')", "al_decir": "Después el jueves"},
                {"click": f"{SCH} button.day-chip:has-text('Vie')", "al_decir": "por último el viernes"},
                R(f"{SCH} .inline-hint", 3000, al_decir="El recuadro azul"),
                R(f"{SCH} mat-checkbox:has-text('Visible para pacientes')", 4500, al_decir="Visible para pacientes"),
                R(f"{SCH} mat-checkbox:has-text('Permitir reservas para hoy')", 3000, al_decir="Permitir reservas para hoy"),
                {"click": f"{SCH} button:has-text('Agregar franja')", "al_decir": "Pulso Agregar franja"},
                R("mat-snack-bar-container", 3000, al_decir="se agregaron", cursor=False),
                R(f"{SCH} .day-line:has-text('Lunes')", 3500, al_decir="cada día muestra"),
                R(".center-link, app-center-booking-link", 3500, al_decir="el enlace del centro ya dice"),
            ],
        },
        {
            "id": "06-bloqueo", "capitulo": "Bloqueos de agenda", "rotulo": "Bloquear unas horas",
            "texto_pantalla": "Bloqueos · vacaciones o una ausencia de unas horas",
            "narracion": (
                "Más abajo están los bloqueos de agenda. Un bloqueo no cambia el horario: aparta un tiempo en que el "
                "médico no está, por vacaciones o por unas horas. Pulso Nuevo bloqueo. Por defecto toma el día "
                "completo de hoy; para varios días se cambia la fecha hasta. Esta vez es solo un rato: elijo la hora "
                "de inicio y marco las diez. Después la hora fin, y marco las doce. El último campo es solo para el equipo: escribo el "
                "motivo, reunión médica, para que todos sepan por qué no hay citas. El aviso de abajo confirma qué se va a bloquear. Con todo listo, pulso "
                "Bloquear, y el sistema avisa que el horario quedó bloqueado. En esas horas no se ofrece ninguna cita, ni en recepción ni por internet. Ojo: un bloqueo no cancela "
                "las citas que ya estaban dadas; esas se reprograman. El bloqueo queda en la lista, y desde ahí se "
                "puede quitar."
            ),
            "acciones": [
                R(f"{SCH} .block-section, {SCH} h3:has-text('Bloqueos de agenda')", 3000, al_decir="los bloqueos de agenda"),
                {"click": "button:has-text('Nuevo bloqueo')", "al_decir": "Pulso Nuevo bloqueo"},
                R("mat-form-field:has-text('Hasta') >> nth=0", 3000, al_decir="la fecha hasta"),
                {"click": "mat-select:near(:text('Hora inicio')) >> nth=0", "al_decir": "Esta vez es solo"},
                {"click": "mat-option:has-text('10:00 a. m.')", "al_decir": "y marco las diez"},
                {"click": "mat-form-field:has-text('Hora fin') mat-select", "al_decir": "Después la"},
                {"click": "mat-option:has-text('12:00 p. m.')", "al_decir": "y marco las doce"},
                {"escribir": {"sel": "input[placeholder*='Motivo'], mat-form-field:has-text('Motivo del bloqueo') input",
                              "texto": "Reunión médica"}, "al_decir": "escribo el"},
                R("mat-icon:text('info') >> xpath=.. >> nth=-1", 3500, al_decir="El aviso de abajo", cursor=False),
                {"click": "button:has-text('Bloquear')", "al_decir": "pulso Bloquear"},
                R("mat-snack-bar-container", 2500, al_decir="quedó bloqueado", cursor=False),
                R(f"{SCH} .exc-row", 4500, al_decir="En esas horas"),
                R(f"{SCH} .day-line:has-text('Lunes')", 3500, al_decir="las citas que ya estaban"),
                R(f"{SCH} .exc-row__del", 3000, al_decir="se puede quitar"),
            ],
        },
        {
            "id": "07-centro", "capitulo": "Los horarios de todos y los feriados", "rotulo": "Recursos y Ajustes",
            "navegar": "/agenda/settings", "al_decir_navegar": "Recursos y Ajustes",
            "texto_pantalla": "Configuración › Recursos y Ajustes · horarios de todos y días no laborables",
            "narracion": (
                "El horario también se puede cargar desde otra pantalla: Configuración, Recursos y Ajustes. Recojo el "
                "panel para ganar espacio. La sección Horarios de Atención muestra a todos los médicos a la vez, con sus franjas, y desde ahí "
                "mismo se agregan. Y en Días No Laborables están los feriados y los cierres del centro: un día de "
                "esa lista no ofrece citas a nadie. En el próximo video el paciente reserva por internet."
            ),
            "acciones": [
                {"click": "button.panel-collapse", "al_decir": "Recojo el"},
                {"click": "button.nav-item:has-text('Horarios de Atención')", "al_decir": "Horarios de Atención"},
                R("table.sch__grid th.sch__staff >> nth=0", 4000, al_decir="a todos los médicos", cursor=False),
                {"click": "button.nav-item:has-text('Días No Laborables')", "al_decir": "Días No Laborables"},
                R("td:has-text('Navidad')", 3000, al_decir="los feriados"),
                R("button:has-text('Nuevo día no laborable')", 3000, al_decir="los cierres del centro"),
            ],
        },
    ]
    return guion(
        "citas-01-medico-horario", "Citas · Parte 1: el médico, su consulta y su horario",
        "Primera parte de la serie de Citas de RegiSalud: la Disponibilidad del médico (Médicos › Agenda), su "
        "consulta (precio particular, autorización de la ARS y reserva en línea), el horario de atención por "
        "franjas con especialidad, duración del turno, pacientes, modalidad y consultorio (creado desde el mismo "
        "campo), la repetición en varios días, los bloqueos de agenda y la vista de Recursos y Ajustes.",
        pasos, comentario="Estado A de citas.mjs: Luis Gómez sin consulta ni horario, sin Consultorio Pediátrico.",
        portada_s=4,
    )


def citas_02():
    correo = "gabriela.fernandez@correo.test"
    pasos = [
        {
            "id": "01-enlace", "capitulo": "El enlace de reservas del centro", "rotulo": "Enlace de reservas",
            "navegar": "/book/centro/los-prados", "al_decir_navegar": "abro el enlace",
            "ruta": "Enlace de reservas del centro (lo que ve el paciente)",
            "texto_pantalla": "Enlace de reservas · especialidad, médico y hora",
            "narracion": (
                "Me pongo en el lugar de la paciente y abro el enlace de reservas del centro, como lo haría desde su "
                "teléfono. Es uno solo para todos los médicos: se copia desde la Disponibilidad de cualquier médico "
                "y se comparte por WhatsApp, en redes o en la página web. Arriba están los pasos de la reserva. "
                "Cada tarjeta es una especialidad, con su médico y su próximo turno. Gabriela necesita una consulta "
                "general, así que elige Medicina General."
            ),
            "acciones": [
                R(".topbar", 3500, al_decir="uno solo"),
                R(".steps", 3500, al_decir="los pasos"),
                R("button.specialty >> nth=0", 3500, al_decir="Cada tarjeta"),
                {"click": "button.specialty:has-text('Medicina General')", "al_decir": "elige Medicina General"},
            ],
        },
        {
            "id": "02-hora", "capitulo": "Elegir médico y hora", "rotulo": "Médico y hora",
            "ruta": "Enlace de reservas › Medicina General",
            "texto_pantalla": "Médicos de la especialidad con sus próximos turnos",
            "narracion": (
                "Salen los médicos de esa especialidad, primero quien atiende antes, con su consultorio y sus "
                "próximos turnos. Tocar una hora ya elige médico y turno, pero ella quiere otro día, así que pulsa "
                "Ver más días y horas en la doctora Ana Pérez. Se abre la semana de la doctora: los días apagados "
                "no tienen cupo. Toca un día, y abajo salen las horas de la mañana. Elige una, y el resumen de "
                "abajo confirma el día y la hora. Pulsa Continuar."
            ),
            "acciones": [
                R("article.card:has-text('Ana Pérez')", 4000, al_decir="Salen los médicos"),
                R("article.card:has-text('Ana Pérez') .slots", 3500, al_decir="Tocar una hora"),
                {"click": "article.card:has-text('Ana Pérez') button.link", "al_decir": "Ver más días"},
                R(".days", 3500, al_decir="los días apagados"),
                {"click": "button.day:not([disabled]) >> nth=1", "al_decir": "Toca un día"},
                {"click": "button.slot >> nth=2", "al_decir": "Elige una"},
                R(".selection", 3000, al_decir="el resumen"),
                {"click": "button.btn--primary:has-text('Continuar')", "al_decir": "Pulsa Continuar"},
            ],
        },
        {
            "id": "03-correo", "capitulo": "Entrar con el correo", "rotulo": "Correo y acceso",
            "ruta": "Enlace de reservas › Correo y acceso",
            "texto_pantalla": "Correo y acceso · un código de seis dígitos",
            "narracion": (
                "A la derecha queda el resumen de la reserva: la doctora, el consultorio, la duración y el precio "
                "particular de su consulta. Para reservar, la paciente entra con su correo: así sus citas quedan en "
                "su portal. Escribe su correo, el mismo donde quiere recibir los avisos de sus citas, y pulsa "
                "Continuar. Le llega un código de seis dígitos."
            ),
            "acciones": [
                R(".summary, aside", 4500, al_decir="el resumen", cursor=False),
                {"escribir": {"sel": "#portal-email", "texto": correo}, "al_decir": "Escribe su correo"},
                {"click": "app-portal-entry button.btn--primary:has-text('Continuar')", "al_decir": "pulsa Continuar"},
            ],
        },
        {
            "id": "04-codigo", "capitulo": "Verificar el código y sus datos", "rotulo": "Código de verificación",
            "ruta": "Enlace de reservas › Código",
            "setup": {"tipo": "shell", "cmd": f"node seeds/clinica/codigo-portal.mjs {correo}", "guardar_en": "codigo"},
            "texto_pantalla": "El código vence en 30 minutos y admite tres intentos",
            "narracion": (
                "El código vence en treinta minutos. Lo copia del correo y lo escribe aquí. Son seis números, y "
                "tiene tres intentos. Ahora pulsa Verificar código. Como es la primera vez que entra, completa su "
                "nombre: Gabriela, tal como quiere que aparezca. Después su primer apellido: Fernández. El segundo apellido es opcional. Pulsa Guardar datos y continuar."
            ),
            "acciones": [
                {"escribir": {"sel": "#portal-code", "texto": "{{codigo}}"}, "al_decir": "lo escribe aquí"},
                {"click": "button:has-text('Verificar código')", "al_decir": "pulsa Verificar código"},
                {"escribir": {"sel": "#portal-names", "texto": "Gabriela"}, "al_decir": "completa su nombre"},
                {"escribir": {"sel": "#portal-first", "texto": "Fernández"}, "al_decir": "su primer apellido"},
                {"click": "button:has-text('Guardar datos y continuar')", "al_decir": "Pulsa Guardar"},
            ],
        },
        {
            "id": "05-confirmar", "capitulo": "Para quién es y confirmar", "rotulo": "Confirmar la cita",
            "ruta": "Enlace de reservas › Paciente › Confirmación",
            "texto_pantalla": "Para mí o para una persona a mi cargo · Confirmar cita",
            "narracion": (
                "Ahora dice para quién es la cita: para ella, o para una persona a su cargo, como un hijo, con su "
                "relación y su fecha de nacimiento. Es para ella. Pulsa Revisar la cita. Revisa el paciente y a qué "
                "correo le llegarán los avisos, y pulsa Confirmar cita. La reserva quedó confirmada, con su número. "
                "Desde aquí la agrega a su calendario, reserva otra o la cancela si no puede ir."
            ),
            "acciones": [
                R("input[name='patient-choice'] >> xpath=ancestor::label[1] >> nth=1", 3500, al_decir="una persona a su cargo"),
                {"click": "input[name='patient-choice'] >> nth=0", "al_decir": "Es para ella"},
                {"click": "button:has-text('Revisar la cita')", "al_decir": "Pulsa Revisar"},
                {"click": "button[type='submit']", "al_decir": "pulsa Confirmar cita"},
                R(":text('Tu reserva quedó confirmada')", 4000, al_decir="quedó confirmada", cursor=False),
            ],
        },
        {
            "id": "06-sin-ficha", "capitulo": "Reservas sin ficha: vincular al paciente", "rotulo": "Reservas sin ficha",
            "navegar": "/agenda/reservas-sin-ficha",
            "ruta": "Calendario › Reservas sin ficha",
            "texto_pantalla": "Reservas sin ficha · verificar la identidad y vincular",
            "narracion": (
                "Ahora la recepción. En el Calendario, Reservas sin ficha. Si el correo de Gabriela estuviera en su "
                "ficha, la cita se habría creado sola. Pero su ficha no lo tiene, así que el centro todavía no sabe "
                "quién es: el turno está apartado, pero no es una cita ni sale en el calendario. Cada reserva tiene "
                "sus acciones. Registrar paciente crea la ficha con los datos de la reserva, si es nueva. Si la "
                "reserva quedó pendiente, Confirmar turno la confirma; esta ya está confirmada. Y Cancelar reserva "
                "libera el horario. Gabriela ya es "
                "paciente, así que pulso Vincular paciente. La busco por su nombre, o por su cédula, y pulso Buscar. "
                "Aparece su ficha; verifico que es ella, pulso Vincular esta ficha. El sistema pregunta "
                "si la vinculo, y confirmo. Ahora sí se crea la "
                "cita, con su médico y su turno: el aviso lo confirma, y a Gabriela le llega la confirmación por "
                "correo."
            ),
            "acciones": [
                R("h2:has-text('Gabriela')", 3500, al_decir="el correo de Gabriela"),
                R("h2:has-text('Gabriela') >> xpath=..", 4000, al_decir="el turno está apartado"),
                R("a:has-text('Registrar paciente')", 3000, al_decir="Registrar paciente"),
                R(".identity .status", 2500, al_decir="Confirmar turno"),
                R("button:has-text('Cancelar reserva')", 2500, al_decir="Cancelar reserva"),
                {"click": "button:has-text('Vincular paciente')", "al_decir": "pulso Vincular paciente"},
                {"escribir": {"sel": "input[name='query']", "texto": "Gabriela"}, "al_decir": "La busco"},
                {"click": "button:has-text('Buscar')", "al_decir": "pulso Buscar"},
                {"click": "button:has-text('Vincular esta ficha')", "al_decir": "pulso Vincular esta ficha"},
                R("mat-dialog-container", 2500, al_decir="El sistema pregunta", cursor=False),
                {"click": "mat-dialog-container button:has-text('Vincular')", "al_decir": "y confirmo"},
                R(":text('Reserva vinculada')", 3500, al_decir="Ahora sí se crea", cursor=False),
            ],
        },
    ]
    return guion(
        "citas-02-reserva-en-linea", "Citas · Parte 2: el paciente reserva por internet",
        "Segunda parte de la serie de Citas de RegiSalud: el enlace único de reservas del centro tal como lo ve el "
        "paciente (especialidad, médico y hora), la entrada con su correo y el código de verificación, para quién "
        "es la cita, la confirmación, y cómo recepción vincula una reserva sin ficha con el paciente.",
        pasos, comentario="Estado B de citas.mjs (sin citas); Gabriela Fernández con ficha sin correo.",
        portada_s=4,
    )


def citas_03():
    pasos = [
        {
            "id": "01-calendario", "capitulo": "El Calendario: todas las citas", "rotulo": "Calendario",
            "navegar": "/home", "ruta": "Calendario",
            "texto_pantalla": "Calendario · mes, semana, día y lista",
            "narracion": (
                "Ahora vemos las citas desde dentro del centro. Entro a Calendario, en el menú de la izquierda. Abre "
                "en el mes actual. Cada bloque es una cita, con su hora y el paciente, y el color dice su estado; "
                "abajo está la leyenda de colores: programada, confirmada, en espera, atendida, cancelada. Con las "
                "flechas se cambia de mes y Hoy vuelve al día actual. Estos botones cambian la vista: mes, semana, "
                "día y lista. Paso a la semana."
            ),
            "acciones": [
                {"click": "a.rail-item[aria-label='Calendario']", "al_decir": "Entro a Calendario"},
                R(".fc-daygrid-event >> nth=0", 3500, al_decir="Cada bloque"),
                R(".calendar-legend", 4500, al_decir="la leyenda"),
                R("button.today-btn", 2500, al_decir="Hoy vuelve"),
                R(".view-toggle-group", 3500, al_decir="Estos botones"),
                {"click": ".view-toggle-btn >> nth=1", "al_decir": "Paso a la semana"},
            ],
        },
        {
            "id": "02-filtros", "capitulo": "Filtrar y ver la disponibilidad", "rotulo": "Filtros",
            "ruta": "Calendario › Semana",
            "texto_pantalla": "Filtros · médico, especialidad, consultorio y estado",
            "narracion": (
                "Con todos los médicos juntos, la semana se llena. Para eso está esta fila de filtros: buscar, "
                "médicos, especialidad, consultorio y estado. Abro Médicos, y en la lista elijo a la doctora Ana "
                "Pérez. Quedan "
                "solo sus citas. Con un solo médico se puede encender Disponibilidad: se pintan en verde las horas "
                "en que atiende y todavía tiene turnos libres. Toco una cita, y a la derecha sale su panel: el "
                "paciente, el médico, el motivo y el consultorio, con los botones para verla, editarla, "
                "reprogramarla, cambiar su estado o cancelarla."
            ),
            "acciones": [
                R(".calendar-filters", 4000, al_decir="esta fila de filtros"),
                {"click": "mat-select[formcontrolname='staffIds']", "al_decir": "Abro Médicos"},
                {"click": "mat-option:has-text('Ana Pérez')", "al_decir": "elijo a la doctora"},
                {"presionar": {"tecla": "Escape"}, "al_decir": "Quedan"},
                {"click": "mat-slide-toggle:has-text('Disponibilidad')", "al_decir": "encender Disponibilidad"},
                {"click": ".fc-timegrid-event >> nth=0", "al_decir": "Toco una cita"},
                R(".appointment-panel, .side-panel, mat-sidenav, aside", 6000, al_decir="sale su panel", cursor=False),
            ],
        },
        {
            "id": "03-lista", "capitulo": "La vista de lista y la búsqueda", "rotulo": "Vista de lista",
            "ruta": "Calendario › Lista",
            "texto_pantalla": "Lista · las citas por día, con búsqueda",
            "narracion": (
                "Ahora otra vista. Paso a la vista de lista, que es la más cómoda para recepción: una fila por "
                "cita, agrupadas por día. Quito el filtro del médico, y para encontrar a alguien uso Buscar: "
                "escribo Carolina, y la lista se filtra mientras escribo. Aparece su cita con la doctora Marta Reyes."
            ),
            "acciones": [
                {"click": ".view-toggle-btn >> nth=3", "al_decir": "la vista de lista"},
                {"click": "mat-select[formcontrolname='staffIds']", "al_decir": "Quito el filtro"},
                {"click": "mat-option:has-text('Ana Pérez')", "al_decir": "del médico"},
                {"presionar": {"tecla": "Escape"}, "al_decir": "para encontrar"},
                {"escribir": {"sel": "input[formcontrolname='searchTerm']", "texto": "Carolina"}, "al_decir": "escribo Carolina"},
                R(".fc-list-event >> nth=0", 3500, al_decir="Aparece su cita"),
            ],
        },
        {
            "id": "04-centro", "capitulo": "La Agenda del Centro", "rotulo": "Agenda del Centro",
            "ruta": "Calendario › Agenda del Centro",
            "texto_pantalla": "Agenda del Centro · una columna por médico",
            "narracion": (
                "Para ver el día de todo el centro, pulso Agenda del Centro. Aquí cada columna es un médico, con cuántas "
                "citas tiene, y cada tarjeta es una cita con su hora, el paciente y su estado. Con la flecha paso "
                "al día siguiente, y el botón Hoy vuelve a hoy. Solo médicos con citas esconde las columnas vacías, "
                "y mostrar canceladas añade las que se cancelaron. El más de cada columna agenda una cita nueva con "
                "ese médico, y al tocar su nombre se abre su panel. La otra vista, por período, lista las citas de "
                "varios días."
            ),
            "acciones": [
                {"click": "button:has-text('Agenda del Centro')", "al_decir": "pulso Agenda del Centro"},
                R(".col >> nth=0", 4000, al_decir="Aquí cada columna"),
                {"click": "button[aria-label='Día siguiente']", "al_decir": "paso al día siguiente"},
                R("button.today-btn", 2500, al_decir="el botón Hoy"),
                R(".toggles mat-slide-toggle:has-text('Solo médicos')", 3000, al_decir="Solo médicos con citas"),
                R(".toggles mat-slide-toggle:has-text('Mostrar canceladas')", 3000, al_decir="mostrar canceladas"),
                R("button.col__add >> nth=0", 3000, al_decir="El más"),
                R(".col__head >> nth=0", 2500, al_decir="su nombre"),
                R("button:has-text('Período'), button:has-text('Periodo')", 3000, al_decir="por período"),
            ],
        },
        {
            "id": "05-medico", "capitulo": "La agenda de cada médico", "rotulo": "Agenda del médico",
            "ruta": "Médicos › Ana Pérez › Agenda › Citas",
            "texto_pantalla": "Agenda del médico · próximas, hoy y anteriores",
            "narracion": (
                "Y cada médico tiene su agenda en su panel. Toco el nombre de la doctora Ana Pérez. En la pestaña "
                "Agenda, la vista Citas muestra su semana y debajo la lista: próximas, las de hoy o las anteriores, "
                "con la hora, el paciente y el consultorio. Desde el botón de estado de cada cita se confirma, se "
                "registra la llegada o se marca que no asistió. En la próxima parte agendamos una cita y la "
                "manejamos de principio a fin."
            ),
            "acciones": [
                {"click": ".col__head:has-text('Ana Pérez')", "al_decir": "Toco el nombre"},
                {"click": "button.tab:has-text('Agenda')", "al_decir": "En la pestaña"},
                R("button:has-text('Próximas')", 3500, al_decir="próximas"),
                R("button:has-text('Estado') >> nth=0", 4000, al_decir="el botón de estado"),
            ],
        },
    ]
    return guion(
        "citas-03-calendario-agenda", "Citas · Parte 3: el calendario y la agenda del centro",
        "Tercera parte de la serie de Citas de RegiSalud: el Calendario con sus vistas (mes, semana, día y lista), "
        "los colores de estado, los filtros por médico, especialidad, consultorio y estado, la disponibilidad de "
        "un médico, el panel de una cita, la búsqueda, la Agenda del Centro por médico y la agenda de cada médico.",
        pasos, comentario="Estado C de citas.mjs.", portada_s=4,
    )


def citas_04():
    F = "app-appointment-form"
    pasos = [
        {
            "id": "01-nueva", "capitulo": "Nueva cita: paciente, motivo y médico", "rotulo": "Nueva cita",
            "navegar": "/agenda/calendar", "ruta": "Calendario › Nueva Cita",
            "texto_pantalla": "Nueva cita · paciente, motivo de la consulta y médico",
            "narracion": (
                "Una paciente llama para pedir cita. La forma más común de agendar es desde el Calendario, con el "
                "botón Nueva Cita. También se agenda desde la ficha del paciente, o con el más de cada médico en la "
                "Agenda del Centro; y el paciente lo hace solo, por el enlace de reservas o por WhatsApp. Pulso "
                "Nueva Cita. Primero el paciente: escribo su nombre, Laura. Cuando aparece en la lista, la elijo. "
                "Debajo sale su ficha, con la edad y la cédula. Ahora el motivo de la consulta: escribo chequeo, y "
                "en la lista que se abre debajo del campo elijo chequeo general. Después el médico: escribo Jorge, que es su nombre, y en la lista "
                "elijo al doctor Jorge Medina. Debajo se ve lo que dice su consulta: la duración del turno, si la "
                "ARS exige autorización y su tarifa."
            ),
            "acciones": [
                R("button:has-text('Nueva Cita')", 3000, al_decir="botón Nueva Cita"),
                R("button:has-text('Agenda del Centro')", 3000, al_decir="Agenda del Centro;"),
                {"click": "button:has-text('Nueva Cita')", "al_decir": "Pulso Nueva Cita"},
                {"escribir": {"sel": "input[formcontrolname='patientSearch']", "texto": "Laura"}, "al_decir": "escribo su nombre"},
                {"click": "mat-option:has-text('Laura Patricia')", "al_decir": "la elijo"},
                R("mat-dialog-container", 1500, al_decir="Debajo sale su ficha", cursor=False),
                {"escribir": {"sel": "app-custom-select.apt-reason input", "texto": "Chequeo"}, "al_decir": "escribo chequeo"},
                {"click": "mat-option:has-text('Chequeo General')", "al_decir": "elijo chequeo general"},
                {"escribir": {"sel": "input[formcontrolname='doctorSearch']", "texto": "Jorge"}, "al_decir": "escribo Jorge"},
                {"click": "mat-option:has-text('Jorge Medina')", "al_decir": "elijo al doctor Jorge"},
                R("mat-dialog-container", 4000, al_decir="lo que dice su consulta", cursor=False),
            ],
        },
        {
            "id": "02-turno", "capitulo": "El turno, la cobertura y los recordatorios", "rotulo": "Turno y cobertura",
            "ruta": "Calendario › Nueva Cita › Cuándo",
            "texto_pantalla": "Cuándo · los huecos libres del horario del médico",
            "narracion": (
                "Más abajo está la semana del doctor: cada día dice cuántos turnos le quedan. Toco el primer día "
                "disponible, y aparecen sus turnos libres. Elijo uno de la tarde. El consultorio sale solo de la "
                "franja del horario. En cobertura, la paciente paga directo, sin seguro, así que paga la tarifa "
                "completa; si tuviera ARS, aquí se elige su afiliación y su autorización. Los recordatorios salen "
                "por WhatsApp un día antes y por correo una hora antes. En cómo se agendó marco por teléfono, y "
                "como ya la confirmó, marco esa casilla."
            ),
            "acciones": [
                R(".apt-days", 3500, al_decir="la semana del doctor"),
                {"click": "button.apt-day:not([disabled]) >> nth=0", "al_decir": "Toco el primer día"},
                {"click": ".apt-slots button >> nth=2", "al_decir": "Elijo uno de la tarde"},
                R(".apt-sec:has-text('Cobertura')", 5000, al_decir="En cobertura"),
                R(".apt-sec:has-text('Recordatorios')", 4000, al_decir="Los recordatorios"),
                {"click": "mat-select[formcontrolname='source']", "al_decir": "En cómo se agendó"},
                {"click": "mat-option:has-text('teléfono')", "al_decir": "marco por teléfono"},
                {"click": "mat-checkbox[formcontrolname='isConfirmed']", "al_decir": "marco esa casilla"},
            ],
        },
        {
            "id": "03-repetir", "capitulo": "Repetir la cita y agendar", "rotulo": "Repetir esta cita",
            "ruta": "Calendario › Nueva Cita › Repetir esta cita",
            "texto_pantalla": "Repetir esta cita · cada N semanas o meses",
            "narracion": (
                "Laura viene a control cada cuatro semanas, así que marco Repetir esta cita. La frecuencia ya dice "
                "cuatro semanas, y en repeticiones pongo tres, contando la primera, para no pedir cada control. Abajo, la nota dice hasta qué "
                "fecha llega la serie. Pulso Agendar cita. Se "
                "agendan las tres citas, cada una con las mismas validaciones que la primera; si alguna cae en un "
                "feriado o en un turno lleno, el sistema avisa cuál quedó fuera para agendarla a mano. La ventana "
                "se cierra y la cita ya sale en el calendario. Al abrirla se ve su visita, primera consulta o "
                "seguimiento, que el sistema decide solo con el historial de la paciente."
            ),
            "acciones": [
                {"click": "mat-checkbox[formcontrolname='isRecurring']", "al_decir": "marco Repetir"},
                R("input[formcontrolname='recurrenceInterval']", 2500, al_decir="La frecuencia"),
                {"escribir": {"sel": "input[formcontrolname='recurrenceCount']", "texto": "3"}, "al_decir": "pongo tres"},
                R(".apt-note", 3500, al_decir="La nota dice"),
                {"click": "button:has-text('Agendar cita')", "al_decir": "Pulso Agendar cita"},
                R("mat-snack-bar-container", 3000, al_decir="cada una con las mismas", cursor=False),
                R(".toolbar-title", 3000, al_decir="feriado o en un turno lleno"),
                R(".calendar-legend", 4000, al_decir="ya sale en el calendario", cursor=False),
            ],
        },
        {
            "id": "04-confirmar", "capitulo": "Confirmar una cita", "rotulo": "Confirmar",
            "navegar": "/agenda/calendar", "ruta": "Calendario › panel de la cita › Estado",
            "texto_pantalla": "Estado · confirmar, registrar la llegada o no asistió",
            "narracion": (
                "Ahora una cita que sigue programada: la de Rosa Elena Martínez. En el Calendario la busco por su "
                "nombre, Rosa. Ahora paso a la vista de lista, y toco su cita. En el panel, el botón de estado muestra solo los pasos que tocan: "
                "confirmar, registrar la llegada o marcar que no asistió. Confirmo, el sistema pregunta, y digo que "
                "sí. La cita queda confirmada, en verde."
            ),
            "acciones": [
                {"escribir": {"sel": "input[formcontrolname='searchTerm']", "texto": "Rosa"}, "al_decir": "la busco por su"},
                {"click": ".view-toggle-btn >> nth=3", "al_decir": "la vista de lista"},
                {"click": ".fc-list-event:has-text('Rosa') >> nth=0", "al_decir": "toco su cita"},
                {"click": "button.status-menu-trigger", "al_decir": "el botón de estado"},
                R(".mat-mdc-menu-panel", 3500, al_decir="confirmar, registrar", cursor=False),
                {"click": "button[mat-menu-item]:has-text('Confirmar')", "al_decir": "Confirmo"},
                R("mat-dialog-container", 2000, al_decir="el sistema pregunta", cursor=False),
                {"click": "mat-dialog-container button:has-text('Sí'), mat-dialog-container button:has-text('Confirmar')", "al_decir": "digo que sí"},
                R("mat-snack-bar-container", 3000, al_decir="queda confirmada", cursor=False),
            ],
        },
        {
            "id": "05-reprogramar", "capitulo": "Reprogramar a otra hora", "rotulo": "Reprogramar",
            "ruta": "Calendario › panel de la cita › Reprogramar",
            "texto_pantalla": "Reprogramar · nuevo horario y motivo",
            "narracion": (
                "Otro paciente, Francisco Javier Cabrera, pide otra hora. Lo busco por su nombre. Su cita es la "
                "semana que viene, así que paso a la semana siguiente, y toco su cita. En el panel, pulso el botón "
                "Reprogramar. Se abre la ventana: arriba queda la cita actual, y debajo la semana del médico con los "
                "cupos de cada día. Elijo el sábado, que tiene cupos, y el último turno de la tarde. Escribo el motivo: el paciente pidió otra "
                "hora, para que quede en la historia. Confirmo con el botón de abajo: se crea la cita nueva, la anterior queda como reprogramada para la "
                "historia, y al paciente le llega un correo con el nuevo horario."
            ),
            "acciones": [
                {"escribir": {"sel": "input[formcontrolname='searchTerm']", "texto": "Francisco"}, "al_decir": "Lo busco por"},
                {"click": "button[mattooltip='Siguiente'], button:has(mat-icon:text('chevron_right')) >> nth=0", "al_decir": "la semana siguiente"},
                {"click": ".fc-list-event:has-text('Francisco') >> nth=0", "al_decir": "toco su cita"},
                {"click": "button:has-text('Reprogramar') >> nth=0", "al_decir": "pulso el botón"},
                R("mat-dialog-container .days", 3500, al_decir="la semana del médico", cursor=False),
                {"click": "mat-dialog-container button.day:not([disabled]) >> nth=0", "al_decir": "Elijo el sábado"},
                {"click": "mat-dialog-container button.slot >> nth=-1", "al_decir": "el último turno"},
                {"escribir": {"sel": "mat-dialog-container textarea", "texto": "El paciente pidió otra hora"}, "al_decir": "Escribo el motivo"},
                {"click": "mat-dialog-container button:has-text('Reprogramar') >> nth=-1", "al_decir": "Confirmo con el botón"},
                R("mat-snack-bar-container", 3500, al_decir="se crea la cita nueva", cursor=False),
                R(".calendar-legend", 3500, al_decir="como reprogramada"),
            ],
        },
        {
            "id": "06-cancelar", "capitulo": "Cancelar o marcar que no asistió", "rotulo": "Cancelar",
            "ruta": "Calendario › panel de la cita › Cancelar",
            "texto_pantalla": "Cancelar · motivo para el informe de cancelaciones",
            "narracion": (
                "Y si un paciente avisa que no vendrá, se cancela. Busco a Rafael Antonio Núñez por su nombre. Toco "
                "su cita, y en el panel pulso el botón rojo. El sistema pide el motivo: solicitud del paciente. Ese "
                "motivo queda en la cita y en el informe de cancelaciones; la nota es opcional, para el equipo. Y "
                "confirmo con Cancelar la cita: el turno queda libre y los recordatorios se anulan. Si el paciente simplemente "
                "no vino, no se cancela: en el botón de estado se marca que no asistió. Y con los filtros de "
                "estado se encuentran las canceladas. En la próxima parte, la llegada del paciente y los turnos."
            ),
            "acciones": [
                {"escribir": {"sel": "input[formcontrolname='searchTerm']", "texto": "Rafael"}, "al_decir": "Busco a Rafael"},
                {"click": ".fc-list-event:has-text('Rafael') >> nth=0", "al_decir": "toco su cita"},
                {"click": "button:has-text('Cancelar Cita') >> nth=0", "al_decir": "el botón rojo"},
                {"click": "mat-dialog-container mat-select", "al_decir": "pide el motivo"},
                {"click": "mat-option:has-text('Solicitud del paciente')", "al_decir": "solicitud del paciente"},
                R("mat-dialog-container", 2500, al_decir="Ese motivo queda", cursor=False),
                R("mat-dialog-container textarea", 2500, al_decir="la nota es opcional"),
                {"click": "mat-dialog-container button:has-text('Cancelar la cita')", "al_decir": "confirmo con Cancelar"},
                R("mat-snack-bar-container", 3000, al_decir="el turno queda libre", cursor=False),
                R("mat-select[formcontrolname='statuses']", 3000, al_decir="los filtros de"),
            ],
        },
    ]
    return guion(
        "citas-04-agendar-y-gestionar", "Citas · Parte 4: agendar, confirmar, reprogramar y cancelar",
        "Cuarta parte de la serie de Citas de RegiSalud: agendar una cita desde el Calendario (y las otras formas "
        "de agendar), el paciente, el motivo, el médico y su consulta, el turno libre, la cobertura, los "
        "recordatorios, repetir la cita cada N semanas, confirmar, reprogramar a otra hora y cancelar con motivo.",
        pasos, comentario="Estado C de citas.mjs.", portada_s=4,
    )


if __name__ == "__main__":
    for f in (citas_01, citas_02, citas_03, citas_04):
        print(f())
