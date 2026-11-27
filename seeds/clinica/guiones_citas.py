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
                {"escribir": {"sel": "input[formcontrolname='price']", "texto": "2000"}, "al_decir": "En precio particular"},
                R("mat-checkbox:has-text('Pide autorización')", 4500, al_decir="Pide autorización"),
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
                "todavía no existe, y elijo crearlo desde aquí mismo."
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
            ],
        },
        {
            "id": "04-consultorio", "capitulo": "Crear el consultorio", "rotulo": "Nuevo consultorio",
            "texto_pantalla": "Consultorio · código, nombre y ubicación",
            "narracion": (
                "Se abre la ficha del consultorio con el nombre que escribí. Le pongo un código corto: consultorio "
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
                "de inicio, las diez. Después la hora fin, las doce. El último campo es solo para el equipo: escribo el "
                "motivo, reunión médica, para que todos sepan por qué no hay citas. El aviso de abajo confirma qué se va a bloquear. Con todo listo, pulso "
                "Bloquear, y el sistema avisa que el horario quedó bloqueado. En esas horas no se ofrece ninguna cita, ni en recepción ni por internet. Ojo: un bloqueo no cancela "
                "las citas que ya estaban dadas; esas se reprograman. El bloqueo queda en la lista, y desde ahí se "
                "puede quitar."
            ),
            "acciones": [
                R(f"{SCH} .block-section, {SCH} h3:has-text('Bloqueos de agenda')", 3000, al_decir="los bloqueos de agenda"),
                {"click": "button:has-text('Nuevo bloqueo')", "al_decir": "Pulso Nuevo bloqueo"},
                R("mat-form-field:has-text('Hasta') >> nth=0", 3000, al_decir="la fecha hasta"),
                {"click": "mat-select:near(:text('Hora inicio')) >> nth=0", "al_decir": "la hora de inicio"},
                {"click": "mat-option:has-text('10:00 a. m.')", "al_decir": "las diez"},
                {"click": "mat-form-field:has-text('Hora fin') mat-select", "al_decir": "la hora fin"},
                {"click": "mat-option:has-text('12:00 p. m.')", "al_decir": "las doce"},
                {"escribir": {"sel": "input[placeholder*='Motivo'], mat-form-field:has-text('Motivo del bloqueo') input",
                              "texto": "Reunión médica"}, "al_decir": "escribo el"},
                R("mat-icon:text('info') >> xpath=.. >> nth=-1", 3500, al_decir="El aviso de abajo", cursor=False),
                {"click": "button:has-text('Bloquear')", "al_decir": "pulso Bloquear"},
                R("mat-snack-bar-container", 2500, al_decir="quedó bloqueado", cursor=False),
                R(f"{SCH} .exc-row", 4000, al_decir="queda en la lista"),
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
                R("app-staff-schedule-list, .content-block table, .schedule-board", 4000, al_decir="a todos los médicos", cursor=False),
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


if __name__ == "__main__":
    for f in (citas_01,):
        print(f())
