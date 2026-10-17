# python seeds/citas/guiones.py  →  guiones/citas-0N-*.json
# Serie «Citas» de RegiSalud (08/10/2026): clínica demo «Centro Médico Los Prados» (empresa 31).
# Un solo lugar para la configuración común; cada parte declara sus pasos. Ver seeds/citas/restaurar.mjs.
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

COMUN = {
    "base_url": "http://localhost:4310",
    "zona_horaria": "America/Santo_Domingo",
    "sesion": {
        "tipo": "api",
        "url": "http://localhost:3001/api/auth/dev/login",
        "cuerpo": {"username": "admin.losprados@regisalud.test", "password": "admin"},
        "clave": "aut",
        "extra": {"__v": 2},
        "navegar": "/home",
    },
    "marca": {
        "nombre": "RegiSalud",
        "logo": "marca/regisalud.png",
        "simbolo": "marca/regisalud-simbolo.png",
        "linea": "RegiSalud · Tutorial",
    },
    "url_publica": "https://regisalud.com",
    "voz": {"id": "es-DO-RamonaNeural", "velocidad": "+12%"},
    "musica": {"archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -32, "ducking": True, "fade_s": 2},
    "loudnorm": {"lufs": -14, "tp": -1.5},
    "marca_video": {"entrada_s": 3, "cierre_s": 3},
    "rotulo_paso": {"segundos": 3.5},
    "css_global": ["app-chatbot-widget{display:none!important}", ".chatbot-fab{display:none!important}"],
    "pronunciacion": {"RegiSalud": "Regisalud", "ARS": "a-erre-ese"},
    "privacidad": {
        "permitidos": [
            "regisalud", "Los Prados", "losprados", "los-prados", "402-0555", "correo.test", "131456789",
            "Carmen Peña", "Ana Pérez", "Jorge Medina", "Marta Reyes", "Pablo Santos", "Elías Tavárez", "Luis Gómez",
            "Rosa Elena", "Martínez", "Juan Carlos", "Batista", "Carolina", "Méndez", "Miguel Ángel", "Rosario",
            "Paola", "Jiménez", "Rafael Antonio", "Núñez", "Yesenia", "Castillo", "Héctor Manuel", "Vargas",
            "Laura Patricia", "Santana", "Daniel Alberto", "Polanco", "Mariela", "Guzmán", "Francisco Javier",
            "Cabrera", "Altagracia", "Peralta", "Mateo", "Valeria", "Natalia", "Ramírez", "Gabriela", "Fernández",
            "809-555", "829-555", "849-555", "Consultorio",
        ],
        "mapa_fijo": {"localhost:3001": "api.regisalud.com", "localhost:4310": "regisalud.com"},
    },
}

# Selectores que se repiten
RAIL = "nav.module-rail [aria-label='{}']"
DLG = "mat-dialog-container"
TAB_AGENDA = "button.tab:has-text('Agenda')"
SEG_DISP = ".gm-seg button:has-text('Disponibilidad')"
SEG_CITAS = ".gm-seg button:has-text('Citas')"
HORARIO = "app-doctor-schedule-tab"


def click(sel, palabra, **kw):
    return {"click": sel, "al_decir": palabra, **kw}


def marca(sel, palabra, ms=4500, **kw):
    return {"resaltar": sel, "durante_ms": ms, "al_decir": palabra, **kw}


def escribir(sel, texto, palabra):
    return {"escribir": {"sel": sel, "texto": texto}, "al_decir": palabra}


def guion(nombre, titulo, descripcion, setup, aprenderas, errores, pasos, comentario=""):
    g = {"titulo": titulo, "descripcion": descripcion, "_comentario": comentario, **COMUN,
         "setup": {"tipo": "shell", "cmd": f"node seeds/citas/restaurar.mjs {setup}"},
         "aprenderas": aprenderas, "errores_comunes": errores, "pasos": pasos}
    destino = RAIZ / "guiones" / f"{nombre}.json"
    destino.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    print("escrito", destino.name, "·", len(pasos), "pasos")


# ── PARTE 1 · Los servicios del centro (tipos de cita) ─────────────────────────────────────────────
guion(
    "citas-01-servicios",
    "Citas · Parte 1: los servicios del centro",
    "Primera parte de la serie de Citas de RegiSalud: dónde se configuran los servicios que ofrece el centro "
    "(los tipos de cita), qué significa cada columna, y cómo se crea uno nuevo: código, nombre, descripción, "
    "duración y pacientes por turno, precio y servicio facturable, color e ícono, reserva en línea, "
    "telemedicina y autorización del seguro. Termina con los días no laborables del centro.",
    "A",
    [
        "Encontrar los servicios del centro en Configuración › Recursos y Ajustes › Tipos de cita",
        "Crear un servicio con su duración, su precio y su color en el calendario",
        "Decidir si el servicio se reserva por internet, si admite teleconsulta y si la ARS debe autorizarlo",
        "Saber qué días no se ofrecen citas en todo el centro",
    ],
    [
        "Crear el servicio y esperar que ya salga en el portal: falta asignarlo a un médico con su horario (parte 2)",
        "Apagar «Permite agendamiento online» y luego no encontrarlo en el portal de reservas",
        "Usar la duración del servicio como horario: los turnos reales los da el horario de cada médico",
    ],
    [
        {
            "id": "01-donde",
            "capitulo": "Dónde están los servicios",
            "rotulo": "Los servicios del centro",
            "ruta": "Configuración › Recursos y Ajustes › Tipos de cita",
            "texto_pantalla": "Tipos de cita · los servicios que ofrece el centro",
            "narracion": (
                "En esta serie vemos el módulo de citas completo, desde los servicios hasta la atención del "
                "paciente. Empezamos por los servicios. Entro a Configuración, en el menú de la izquierda, "
                "y abro Recursos y Ajustes. Recojo el panel para ganar espacio. A la izquierda están los recursos "
                "del centro; elijo Tipos de cita. Un tipo de cita es un servicio que el centro ofrece: una consulta "
                "general, un control, una evaluación del cardiólogo. Cada fila es uno, con su código y su nombre. "
                "La columna de color es como se pinta en el calendario, y la siguiente dice cuánto dura. Reserva "
                "online indica si el paciente lo puede pedir por internet: la urgencia dice que no, porque una "
                "urgencia no se agenda."
            ),
            "acciones": [
                click(RAIL.format("Configuración"), "Entro a Configuración"),
                click(".panel-item:has-text('Recursos y Ajustes')", "abro Recursos"),
                click("button.panel-collapse", "Recojo el panel"),
                click(".nav-item:has-text('Tipos de Cita')", "elijo Tipos"),
                marca("table tbody tr:has-text('CONSULTA-GENERAL') td:nth-child(2)", "Cada fila", 4000),
                marca("table thead th:nth-child(3)", "columna de color", 3500),
                marca("table thead th:nth-child(4)", "cuánto dura", 3500),
                marca("table tbody tr:has-text('URGENCIA') td:nth-child(5)", "la urgencia", 5000),
            ],
        },
        {
            "id": "02-nuevo",
            "capitulo": "Crear un servicio",
            "rotulo": "Nuevo tipo de cita",
            "ruta": "Recursos y Ajustes › Tipos de cita › Nuevo",
            "texto_pantalla": "Código, nombre y descripción · lo que el paciente lee en el portal",
            "narracion": (
                "El centro va a empezar a atender niños, así que creo el servicio de pediatría. Pulso Nuevo tipo "
                "de cita, arriba a la derecha de la tabla. El código es una clave corta, sin espacios: escribo "
                "consulta pediátrica, con un guion en medio y sin tildes, porque es una clave interna. Ahora el "
                "nombre, que es lo que leen la recepción y el "
                "paciente. En la descripción digo para quién es: el paciente la ve en el portal antes de reservar. "
                "Más abajo están los valores iniciales: la duración, treinta minutos, y los pacientes por turno, "
                "uno. Son el punto de partida: los turnos que de verdad se ofrecen salen del horario de cada "
                "médico. El orden de visualización decide en qué lugar sale en las listas."
            ),
            "acciones": [
                click("button:has-text('Nuevo Tipo de Cita')", "Pulso Nuevo"),
                {"resaltar": "mat-dialog-container", "durante_ms": 3000, "cursor": False},
                escribir(f"{DLG} input[formcontrolname='code']", "CONSULTA-PEDIATRICA", "escribo"),
                escribir(f"{DLG} input[formcontrolname='name']", "Consulta pediátrica", "Ahora el nombre"),
                escribir(f"{DLG} textarea[formcontrolname='description']",
                         "Control de niño sano y consulta de enfermedad para menores de 18 años.",
                         "En la descripción"),
                marca(f"{DLG} input[formcontrolname='defaultDurationMinutes']", "la duración", 3500),
                marca(f"{DLG} input[formcontrolname='maxPatientsPerSlot']", "pacientes por turno", 3500),
                marca(f"{DLG} input[formcontrolname='displayOrder']", "orden de visualización", 4000),
            ],
        },
        {
            "id": "03-precio-opciones",
            "capitulo": "Precio, color y opciones",
            "rotulo": "Precio y opciones",
            "ruta": "Recursos y Ajustes › Tipos de cita › Nuevo",
            "texto_pantalla": "Precio base · reserva en línea · teleconsulta · autorización del seguro",
            "narracion": (
                "Sigo más abajo, con el dinero. El precio base es la tarifa del paciente particular: dos mil "
                "pesos. Debajo, el servicio "
                "facturable es el artículo con el que se cobra; si lo dejo vacío, al cobrar se crea solo, con "
                "este nombre y este precio. En apariencia está el color del calendario y el ícono: escribo "
                "child care, el de un bebé, que es el que verá el paciente en el portal. Y las opciones. Permite "
                "agendamiento online deja que el paciente lo reserve por internet: lo dejo encendido. Permite "
                "telemedicina es la modalidad: si la enciendo, la cita se puede dar por videollamada; esta "
                "consulta es presencial. Requiere autorización previa del seguro obliga a tener la aprobación de "
                "la aseguradora de salud del paciente antes de atender. La casilla Activo queda marcada. Con todo "
                "listo, pulso Crear. El aviso confirma que el tipo de cita se creó, y el servicio aparece en la "
                "lista con su color y su duración."
            ),
            "acciones": [
                escribir(f"{DLG} input[formcontrolname='basePrice']", "2000", "El precio base"),
                marca(f"{DLG} app-custom-select, {DLG} mat-form-field:has(mat-label:has-text('Servicio facturable'))",
                      "servicio facturable", 5000),
                marca(f"{DLG} input[formcontrolname='color']", "color del calendario", 3000),
                escribir(f"{DLG} input[formcontrolname='icon']", "child_care", "escribo child"),
                marca(f"{DLG} mat-slide-toggle[formcontrolname='allowOnlineBooking']", "agendamiento online", 4500),
                marca(f"{DLG} mat-slide-toggle[formcontrolname='allowTelemedicine']", "telemedicina es", 5000),
                marca(f"{DLG} mat-checkbox[formcontrolname='requiresAuthorization']", "autorización previa", 5000),
                marca(f"{DLG} mat-checkbox[formcontrolname='active']", "La casilla Activo", 2500),
                click(f"{DLG} button:has-text('Crear')", "pulso Crear"),
                {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3000, "cursor": False},
                marca("table tbody tr:has-text('CONSULTA-PEDIATRICA') td:nth-child(2)", "aparece en la", 5000),
            ],
        },
        {
            "id": "04-no-laborables",
            "capitulo": "Días no laborables",
            "rotulo": "Días no laborables",
            "ruta": "Recursos y Ajustes › Días no laborables",
            "texto_pantalla": "Feriados y cierres · ese día no se ofrecen citas en el centro",
            "narracion": (
                "Antes de pasar a los médicos, un ajuste que afecta a todos. En Días no laborables están los "
                "feriados del país y los cierres del propio centro. Cada fila es un día, con su tipo y su alcance: "
                "global, para todo el país, o solo de esta empresa. La columna pagado es para la nómina. Un día de "
                "esta lista no ofrece citas en el "
                "portal ni en la agenda. Si el centro cierra por algo propio, como un inventario o el aniversario, "
                "se agrega aquí con Nuevo día no laborable. En la próxima parte le damos el servicio de pediatría "
                "a un médico, con sus días y sus horas."
            ),
            "acciones": [
                click(".nav-item:has-text('Días No Laborables')", "En Días no"),
                marca("table tbody tr:first-child td:nth-child(2)", "Cada fila", 3500),
                marca("table thead th:nth-child(3)", "su tipo", 2500),
                marca("table thead th:nth-child(4)", "su alcance", 4000),
                marca("table thead th:nth-child(5)", "pagado es", 3000),
                marca("table tbody tr:first-child td:nth-child(1)", "no ofrece citas", 3500),
                marca("button:has-text('Nuevo día no laborable')", "Nuevo día no laborable", 4500),
            ],
        },
    ],
    comentario="Estado A: servicios base sin «Consulta pediátrica»; el video la crea (queda como el estado P).",
)

# ── PARTE 2 · El médico: servicio, horario, enlace y bloqueos ─────────────────────────────────────
guion(
    "citas-02-medico-horario",
    "Citas · Parte 2: el médico, su horario y su enlace",
    "Segunda parte de la serie de Citas de RegiSalud: cómo se le asigna un servicio a un médico desde su ficha "
    "(Médicos › Agenda › Disponibilidad), el enlace de reservas que se genera para ese médico y ese servicio, "
    "el horario de atención por día con la duración de cada turno, los pacientes por turno y el consultorio "
    "(creado desde el mismo campo), las opciones de reserva en línea, los bloqueos de agenda por vacaciones o "
    "ausencias, y el resumen de horarios de todos los médicos.",
    "P",
    [
        "Habilitar un servicio para un médico y entender el enlace de reservas que se genera",
        "Configurar el horario de atención de varios días de una vez, con turnos, capacidad y consultorio",
        "Crear un consultorio sin salir del horario",
        "Bloquear horas o días del médico para que no se ofrezcan citas",
        "Ver el horario de todos los médicos en una sola pantalla",
    ],
    [
        "Crear el servicio y no darle horario: el médico no aparece en el portal hasta que tiene una franja visible",
        "Desmarcar «Visible para pacientes en el link de reservas»: la franja sirve en recepción pero no en internet",
        "Cargar las vacaciones como un horario nuevo en vez de un bloqueo",
    ],
    [
        {
            "id": "01-ficha",
            "capitulo": "La agenda del médico",
            "rotulo": "La agenda del médico",
            "ruta": "Médicos › Luis Gómez › Agenda › Disponibilidad",
            "texto_pantalla": "Disponibilidad · qué servicios ofrece el médico, cuándo y dónde",
            "narracion": (
                "El servicio de pediatría ya existe, pero ningún médico lo ofrece. Eso se hace en la ficha del "
                "médico. Entro a Médicos, en el menú de la izquierda. A la izquierda está la lista de médicos del "
                "centro; abro al doctor Luis Gómez, pediatra, y recojo la lista para ganar espacio. En la pestaña "
                "Agenda hay dos vistas: Citas, que son las que ya tiene, y Disponibilidad, que es cuándo atiende. "
                "Abro Disponibilidad. El aviso de arriba resume el orden: primero se habilita el servicio, y "
                "después se le pone el horario. Este médico todavía no ofrece ninguno."
            ),
            "acciones": [
                click(RAIL.format("Médicos"), "Entro a Médicos"),
                click("button.dsel__row:has-text('Luis Gómez')", "abro al doctor"),
                click("button.dsel__collapse", "recojo la lista"),
                click(TAB_AGENDA, "la pestaña Agenda"),
                marca(SEG_CITAS, "Citas, que son", 3000),
                click(SEG_DISP, "Abro Disponibilidad"),
                marca(".ag-tab__hint", "El aviso", 5500),
                marca("button:has-text('Ofrecer el primer tipo de cita')", "no ofrece ninguno", 3500),
            ],
        },
        {
            "id": "02-ofrecer",
            "capitulo": "Habilitar el servicio y su enlace",
            "rotulo": "Ofrecer el servicio",
            "ruta": "Médicos › Luis Gómez › Disponibilidad › Ofrecer un tipo de cita",
            "texto_pantalla": "Un enlace de reservas por médico y servicio",
            "narracion": (
                "Como no tiene ninguno, el botón dice ofrecer el primer tipo de cita. Lo pulso. En la ventana "
                "elijo el servicio: consulta pediátrica. "
                "Debajo se ve su duración y su precio. Pulso Habilitar para este médico. Al habilitarlo, el "
                "sistema crea su enlace de reservas: una dirección propia de este médico y este servicio, que se "
                "puede mandar por WhatsApp o poner en redes. El título y la descripción son los que se ven al "
                "compartirlo, con la vista previa a la derecha, y el mensaje de invitación se copia junto con el "
                "enlace con este botón. Por ahora cierro la ventana, porque falta lo más importante: el horario."
            ),
            "acciones": [
                click("button:has-text('Ofrecer el primer tipo de cita')", "Lo pulso"),
                click(f"{DLG} app-custom-select input", "elijo el servicio"),
                click("mat-option:has-text('Consulta pediátrica')", "consulta pediátrica"),
                marca(f"{DLG} .ctx-type-meta, {DLG} .type-meta, {DLG} app-custom-select", "su duración", 3500),
                click(f"{DLG} button:has-text('Habilitar para este médico')", "Pulso Habilitar"),
                marca(f"{DLG} .copybar, {DLG} .urlbar", "una dirección propia", 5000, cursor=False),
                marca(f"{DLG} input[formcontrolname='title']", "El título", 3500),
                marca(f"{DLG} button:has-text('Copiar mensaje + link')", "con este botón", 3500),
                click(f"{DLG} button:has-text('Cerrar')", "cierro la ventana"),
            ],
        },
        {
            "id": "03-horario",
            "capitulo": "El horario de atención",
            "rotulo": "Horario de atención",
            "ruta": "Médicos › Luis Gómez › Disponibilidad › Horario de atención",
            "texto_pantalla": "Una franja: inicio, fin, duración del turno, pacientes y consultorio",
            "narracion": (
                "Ahora el horario. Cada día de la semana sale en una fila, y el doctor no atiende ninguno todavía. "
                "Pulso Agregar en el lunes. Una franja es un bloque de horas que se divide en turnos: de ocho a "
                "doce, con turnos de treinta minutos, que vienen del servicio, y un paciente por turno. El "
                "consultorio es la sala donde atiende. Escribo el nombre de uno que aún no existe, y elijo "
                "crearlo desde aquí mismo."
            ),
            "acciones": [
                marca(f"{HORARIO} .day-line:has-text('Lunes') .day-line__label", "Cada día", 3500),
                click("button.add-franja >> nth=0", "Pulso Agregar"),
                marca(f"{HORARIO} mat-select[formcontrolname='startTime']", "de ocho", 3000),
                marca(f"{HORARIO} mat-select[formcontrolname='slotDurationMinutes']", "turnos de treinta", 3500),
                marca(f"{HORARIO} input[formcontrolname='maxClientsPerSlot']", "un paciente", 3000),
                escribir(f"{HORARIO} app-custom-select[formcontrolname='consultorioId'] input", "Consultorio Pediátrico",
                         "Escribo el nombre"),
                click("mat-option.cs-create", "elijo crearlo"),
            ],
        },
        {
            "id": "04-consultorio",
            "capitulo": "Crear el consultorio",
            "rotulo": "Nuevo consultorio",
            "ruta": "Disponibilidad › Horario › Nuevo consultorio",
            "texto_pantalla": "El consultorio · la sala o sede donde se atiende",
            "narracion": (
                "Se abre la ficha del consultorio, con el nombre que ya escribí. Le pongo un código corto: "
                "consultorio pediatría. Los datos de ubicación son opcionales: la dirección, el teléfono, el "
                "edificio y el piso. Sirven cuando el centro tiene varias sedes, porque el paciente los ve en su "
                "confirmación. Pulso Guardar, y el consultorio queda elegido en la franja."
            ),
            "acciones": [
                marca(f"{DLG} input[formcontrolname='name']", "con el nombre", 3500, cursor=False),
                escribir(f"{DLG} input[formcontrolname='code']", "CONS-PED", "un código corto"),
                marca(f"{DLG} input[formcontrolname='address']", "la dirección", 3500),
                click(f"{DLG} button:has-text('Guardar')", "Pulso Guardar"),
                marca(f"{HORARIO} app-custom-select[formcontrolname='consultorioId']", "queda elegido", 4000),
            ],
        },
        {
            "id": "05-dias-opciones",
            "capitulo": "Varios días y opciones de reserva",
            "rotulo": "Días y opciones",
            "ruta": "Médicos › Luis Gómez › Disponibilidad › Horario de atención",
            "texto_pantalla": "Aplicar a varios días · visible en el enlace · reservas para hoy · exclusivo",
            "narracion": (
                "Para no repetir lo mismo cinco veces, en Aplicar a marco el martes. Marco también el miércoles. "
                "Después el jueves. Y por último el viernes. Abajo están las opciones de reserva. Visible para pacientes en el link de reservas hace "
                "que estos turnos se ofrezcan por internet; si se desmarca, solo la recepción los puede usar. "
                "Permitir reservas para hoy deja reservar el mismo día. Y horario exclusivo para este tipo de "
                "cita aparta estas horas solo para pediatría. Pulso Agregar: se crean las cinco franjas, y cada "
                "día muestra su horario, su consultorio y cuántos turnos tiene."
            ),
            "acciones": [
                click(f"{HORARIO} button.day-chip:has-text('Mar')", "el martes"),
                click(f"{HORARIO} button.day-chip:has-text('Mié')", "el miércoles"),
                click(f"{HORARIO} button.day-chip:has-text('Jue')", "el jueves"),
                click(f"{HORARIO} button.day-chip:has-text('Vie')", "el viernes"),
                marca(f"{HORARIO} mat-checkbox[formcontrolname='allowOnlineBooking']", "Visible para", 5500),
                marca(f"{HORARIO} mat-checkbox[formcontrolname='allowSameDayBooking']", "el mismo día", 3500),
                marca(f"{HORARIO} mat-checkbox[formcontrolname='strictMode']", "horario exclusivo", 4000),
                click(f"{HORARIO} button[type='submit']", "Pulso Agregar"),
                marca(".mat-mdc-snack-bar-container", "cinco franjas", 3000, cursor=False),
            ],
        },
        {
            "id": "06-bloqueo",
            "capitulo": "Bloqueos de agenda",
            "rotulo": "Bloquear horas",
            "ruta": "Médicos › Luis Gómez › Disponibilidad › Bloqueos de agenda",
            "texto_pantalla": "Bloqueo · vacaciones o ausencias: en ese tiempo no se ofrecen citas",
            "narracion": (
                "Más abajo están los bloqueos de agenda. Un bloqueo no cambia el horario: aparta un tiempo en el "
                "que el médico no está, por vacaciones o por una ausencia de unas horas. Pulso Nuevo bloqueo. Por "
                "defecto toma el día completo de hoy. Si es solo un rato, elijo la hora de inicio: las diez. "
                "Después la hora final: las doce. El último campo es solo para el equipo: escribo el motivo, "
                "reunión médica. "
                "El aviso de abajo confirma qué se va a bloquear. Pulso Bloquear: el sistema avisa que el horario "
                "quedó bloqueado, y el bloqueo "
                "aparece en la lista; en esas horas no se ofrece ninguna cita, ni en recepción ni en internet."
            ),
            "acciones": [
                marca(f"{HORARIO} section.exc-panel", "los bloqueos de agenda", 3500),
                click("button:has-text('Nuevo bloqueo')", "Pulso Nuevo bloqueo"),
                click(f"{HORARIO} mat-form-field:has(mat-label:has-text('Hora inicio')) mat-select", "la hora de inicio"),
                click("mat-option:has-text('10:00 a. m.')", "las diez"),
                click(f"{HORARIO} mat-form-field:has(mat-label:has-text('Hora fin')) mat-select", "la hora final"),
                click("mat-option:has-text('12:00 p. m.')", "las doce"),
                escribir(f"{HORARIO} mat-form-field:has(mat-label:has-text('Motivo del bloqueo')) input",
                         "Reunión médica", "escribo el motivo"),
                click(f"{HORARIO} .exc-form__foot button:has-text('Bloquear')", "Pulso Bloquear"),
                {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3000, "cursor": False},
                marca(f"{HORARIO} .exc-row:has-text('Reunión médica')", "aparece en la lista", 5000),
            ],
        },
        {
            "id": "07-resumen",
            "capitulo": "El horario de todos los médicos",
            "rotulo": "Horarios de atención",
            "ruta": "Configuración › Recursos y Ajustes › Horarios de atención",
            "texto_pantalla": "Horarios de atención · la semana de todos los médicos",
            "narracion": (
                "Para ver el horario de todos a la vez, vuelvo a Configuración y entro a Recursos y Ajustes. "
                "Recojo el panel y abro Horarios de atención. Cada fila es un médico con sus días de atención, y cada recuadro una "
                "franja con su duración y su consultorio. Aquí está el doctor Luis Gómez con lo que acabamos de "
                "configurar. Con el servicio, el médico y el horario listos, en la próxima parte el paciente "
                "reserva desde internet."
            ),
            "acciones": [
                click(RAIL.format("Configuración"), "vuelvo a Configuración"),
                click(".panel-item:has-text('Recursos y Ajustes')", "entro a Recursos"),
                click("button.panel-collapse", "Recojo el panel"),
                click(".nav-item:has-text('Horarios de Atención')", "abro Horarios"),
                marca("table.sch__grid tbody tr:first-child th.sch__staff", "Cada fila", 3500),
                marca("table.sch__grid tbody tr:has-text('Luis Gómez') th.sch__staff", "Aquí está", 5000),
            ],
        },
    ],
    comentario="Estado P: «Consulta pediátrica» existe y Luis Gómez no la ofrece. Termina como el estado B "
               "(más el bloqueo de hoy 10-12).",
)

# ── PARTE 3 · El portal de reservas: lo que ve el paciente ─────────────────────────────────────────
CAL_DIA = ".mat-calendar-body-cell:not(.mat-calendar-body-disabled)"
guion(
    "citas-03-portal-paciente",
    "Citas · Parte 3: el paciente reserva por internet",
    "Tercera parte de la serie de Citas de RegiSalud: los dos modos de la agenda en línea (simple, un enlace por "
    "médico y servicio; avanzado, el portal del centro), cómo se activa el portal en Configuración › Preferencias "
    "› Operación, y la reserva completa vista desde fuera, como la hace el paciente: elige el servicio, después el "
    "médico, la fecha y la hora, deja sus datos y recibe el número de su cita.",
    "B",
    [
        "Elegir entre el modo simple (un enlace por médico) y el avanzado (el portal del centro)",
        "Publicar el portal de reservas y copiar su enlace",
        "Recorrer la reserva del paciente: servicio, médico, fecha y hora, datos y confirmación",
        "Saber qué recibe el paciente al reservar y cómo cancela si no puede asistir",
    ],
    [
        "Elegir el modo avanzado y no pulsar Guardar: el enlace del portal no abre hasta guardar",
        "Esperar en el portal un médico sin horario visible en el enlace: solo salen los que tienen turnos en línea",
        "Compartir el enlace de un médico cuando se quería que el paciente eligiera entre varios: para eso es el portal",
    ],
    [
        {
            "id": "01-modo",
            "capitulo": "Simple o avanzado",
            "rotulo": "Modo de la agenda en línea",
            "ruta": "Configuración › Preferencias › Operación › Citas Médicas",
            "texto_pantalla": "Simple: un enlace por médico · Avanzado: el portal de todo el centro",
            "narracion": (
                "Hay dos formas de recibir citas por internet, y se eligen en la configuración. Entro a "
                "Configuración, en el menú, y abro Preferencias. Después recojo el panel para ganar espacio, y "
                "abro la pestaña Operación. En el bloque "
                "Citas Médicas, los minutos antes para recordatorio dicen con cuánta anticipación le llega al "
                "paciente el recordatorio por correo. Al lado está el modo de la agenda en línea; abro la lista. "
                "En el modo simple, cada médico comparte su propio enlace, el que vimos en la parte anterior. En "
                "el modo avanzado, el centro tiene un portal: el paciente entra a una sola dirección y elige el "
                "servicio, el médico y la hora. Elijo el avanzado. Aparece la dirección del portal, con su botón "
                "para copiarla. Como dice la nota, hay que guardar para publicarlo: pulso Guardar, abajo. Sale el "
                "aviso de configuración guardada, y lo acepto."
            ),
            "acciones": [
                click(RAIL.format("Configuración"), "Entro a Configuración"),
                click(".panel-item:has-text('Preferencias')", "abro Preferencias"),
                click("button.panel-collapse", "Recojo el panel"),
                click("[role=tab]:has-text('Operación')", "la pestaña Operación"),
                marca("mat-form-field:has(mat-label:has-text('Minutos antes para recordatorio'))",
                      "minutos antes para recordatorio", 5500),
                click("mat-select[formcontrolname='agendaMode']", "abro la lista"),
                marca("mat-option:has-text('Simple')", "En el modo simple", 5500, cursor=False),
                marca("mat-option:has-text('Avanzado')", "el modo avanzado", 6000, cursor=False),
                click("mat-option:has-text('Avanzado')", "Elijo el avanzado"),
                marca("a[href*='book/centro']", "su botón para", 4500),
                click(".settings-actions button:has-text('Guardar')", "pulso Guardar"),
                {"resaltar": "mat-dialog-container", "durante_ms": 3000, "cursor": False},
                click("mat-dialog-container button:has-text('Aceptar')", "lo acepto"),
            ],
        },
        {
            "id": "02-portal",
            "capitulo": "El portal: elegir el servicio",
            "rotulo": "Paso 1 · el servicio",
            "ruta": "regisalud.com/book/centro/los-prados",
            "texto_pantalla": "El portal del centro · el paciente empieza por el servicio",
            "navegar": "/book/centro/los-prados",
            "al_decir_navegar": "abro el portal",
            "narracion": (
                "Ahora me pongo en el lugar del paciente: abro el portal con ese enlace, como lo haría desde su "
                "teléfono. Arriba está el nombre del centro y los tres pasos de la reserva: servicio, médico, "
                "fecha y hora. Cada tarjeta es un servicio, con su descripción, su duración y cuántos médicos lo "
                "ofrecen. Aquí está la consulta pediátrica que configuramos, con el doctor Luis Gómez. Este "
                "paciente necesita una consulta general, así que la elige."
            ),
            "acciones": [
                marca("app-clinic-portal h1", "el nombre del centro", 3000),
                marca("app-clinic-portal .steps, app-clinic-portal .portal-steps, app-clinic-portal .stepper",
                      "los tres pasos", 4000),
                marca("button.service-card:has-text('Consulta general')", "Cada tarjeta", 4500),
                marca("button.service-card:has-text('Consulta pediátrica')", "Aquí está la consulta", 4500),
                click("button.service-card:has-text('Consulta general')", "la elige"),
            ],
        },
        {
            "id": "03-medico",
            "capitulo": "Elegir el médico",
            "rotulo": "Paso 2 · el médico",
            "ruta": "regisalud.com/book/centro/los-prados",
            "texto_pantalla": "Los médicos que ofrecen ese servicio",
            "narracion": (
                "El segundo paso muestra los médicos que ofrecen ese servicio, con su especialidad. Si se "
                "equivocó, cambiar servicio lo lleva de vuelta. Elige a la doctora Ana Pérez y pulsa ver "
                "horarios. Entra a la página de reservas de la doctora: la misma que se abre con su enlace en el "
                "modo simple. Arriba se ve el servicio, la doctora con su especialidad, la descripción y el precio."
            ),
            "acciones": [
                marca("button.doctor-card:has-text('Jorge Medina')", "ofrecen ese servicio", 4000),
                marca("button:has-text('Cambiar servicio')", "cambiar servicio", 3500),
                click("button.doctor-card:has-text('Ana Pérez')", "ver horarios"),
                marca("app-booking-page h1", "Arriba se ve", 5000, cursor=False),
            ],
        },
        {
            "id": "04-horario",
            "capitulo": "Fecha y hora",
            "rotulo": "Paso 3 · fecha y hora",
            "ruta": "regisalud.com/book/ana-perez/consulta-general",
            "texto_pantalla": "Solo se pueden elegir los días con turnos libres",
            "narracion": (
                "Debajo está el calendario. Los días apagados no se pueden elegir: ya pasaron, la doctora no "
                "atiende, o no le quedan turnos. El paciente toca uno de los próximos días, y a la derecha "
                "aparecen los turnos libres de ese día, cada uno con su hora de inicio, de fin y su duración. "
                "Elige el de las nueve de la mañana, y pulsa siguiente."
            ),
            "acciones": [
                marca("mat-calendar", "el calendario", 4500),
                click(f"{CAL_DIA} >> nth=1", "toca uno de"),
                marca("button.slot-button >> nth=0", "aparecen los turnos", 5000),
                click("button.slot-button:has-text('09:00 a. m.hasta')", "el de las nueve"),
                click("button.next-button", "pulsa siguiente"),
            ],
        },
        {
            "id": "05-datos",
            "capitulo": "Sus datos y la confirmación",
            "rotulo": "Confirmar la reserva",
            "ruta": "regisalud.com/book/ana-perez/consulta-general/confirm",
            "texto_pantalla": "Nombre y correo · el sistema crea la cita y le da su número",
            "narracion": (
                "Arriba queda el resumen de lo que eligió: doctora, consultorio, duración, fecha y hora. Abajo "
                "pone sus datos: el nombre completo, Gabriela Fernández, tal como quiere que aparezca. Después el "
                "correo electrónico, que es donde le llega la confirmación de su cita. Y por último el teléfono, "
                "que es opcional pero sirve para el recordatorio. Pulsa confirmar reserva. Listo: la cita quedó creada. La pantalla le da su número "
                "de cita, el médico, el consultorio, la fecha y la hora. Puede agregarla a su calendario de "
                "Google, y si no puede asistir, la cancela desde aquí para liberar el horario. Del lado del "
                "centro, esta cita ya está en la agenda: eso lo vemos en la siguiente parte."
            ),
            "acciones": [
                marca("app-booking-form .summary-details", "el resumen", 5000),
                escribir("input[formcontrolname='bookerName']", "Gabriela Fernández", "el nombre completo"),
                escribir("input[formcontrolname='bookerEmail']", "gabriela.fernandez@correo.test", "el correo electrónico"),
                escribir("input[formcontrolname='bookerPhone']", "809-555-0190", "por último el teléfono"),
                click("button.submit-button", "Pulsa confirmar"),
                marca("app-booking-confirmation :text('No. de Cita')", "su número", 5000, cursor=False),
                marca(".gcal-button", "calendario de", 3500),
                marca(".cancel-button", "la cancela desde aquí", 4500),
            ],
        },
    ],
    comentario="Estado B: Luis Gómez ya ofrece pediatría; agenda en modo SIMPLE. El video pasa a AVANZADO y reserva "
               "una consulta general con Ana Pérez a nombre de Gabriela Fernández.",
)

# ── PARTE 4 · Ver todas las citas: calendario y Agenda del Centro ──────────────────────────────────
FILTRO = "app-agenda-filters mat-select[formcontrolname='{}']"
VISTA = "button:has(mat-icon:text-is('{}'))"
guion(
    "citas-04-calendario-agenda",
    "Citas · Parte 4: todas las citas del centro",
    "Cuarta parte de la serie de Citas de RegiSalud: cómo se ven todas las citas desde dentro. El calendario con "
    "sus vistas de mes, semana, día y lista, los colores por estado, la disponibilidad, los filtros por médico, "
    "servicio y estado, y el panel de cada cita; la Agenda del Centro, con una columna por médico o una lista por "
    "período; y la agenda propia de cada médico en su ficha.",
    "C",
    [
        "Leer el calendario: vistas, colores por estado, disponibilidad y el detalle de una cita",
        "Filtrar las citas por médico, servicio, consultorio, estado o paciente",
        "Ver el día de todos los médicos lado a lado en la Agenda del Centro",
        "Revisar un período completo agrupado por día, con canceladas o sin ellas",
        "Encontrar la agenda de un solo médico en su ficha",
    ],
    [
        "Buscar una cita cancelada sin encender «Mostrar canceladas» o sin elegir ese estado en el filtro",
        "Olvidar un filtro puesto y pensar que faltan citas: «Limpiar» los quita todos",
        "Tomar la disponibilidad en verde como citas: son horas libres del médico",
    ],
    [
        {
            "id": "01-calendario",
            "capitulo": "El calendario",
            "rotulo": "El calendario",
            "ruta": "Calendario",
            "texto_pantalla": "Cada bloque es una cita: hora y paciente, con el color de su estado",
            "narracion": (
                "Ahora vemos las citas desde dentro del centro. Entro a Calendario, en el menú de la izquierda. "
                "Abre en el mes actual, con el día de hoy marcado. Cada bloque es una cita, con su hora y el "
                "paciente, y el color dice en qué estado está: programada, confirmada, en espera, atendida o "
                "cancelada. Cuando un día tiene muchas, el enlace de más las despliega. Arriba se cambia de mes "
                "con las flechas, y Hoy vuelve al día actual. Estos botones cambian la vista: mes, semana, día y "
                "lista. Paso a la semana."
            ),
            "acciones": [
                click(RAIL.format("Calendario"), "Entro a Calendario"),
                marca(".fc-day-today", "el día de hoy", 3500),
                marca(".fc-day-today .fc-event >> nth=0", "Cada bloque", 4500),
                marca(".fc-day-today .fc-daygrid-more-link", "el enlace de más", 3500),
                marca("button[aria-label='Siguiente'], button:has(mat-icon:text-is('chevron_right')) >> nth=0",
                      "con las flechas", 3000),
                marca("button:has-text('Hoy') >> nth=0", "y Hoy vuelve", 2500),
                marca(VISTA.format("view_week") + " >> xpath=..", "Estos botones", 4000),
                click(VISTA.format("view_week"), "Paso a la semana"),
            ],
        },
        {
            "id": "02-filtros",
            "capitulo": "Filtrar y ver una cita",
            "rotulo": "Filtros y detalle",
            "ruta": "Calendario › Semana",
            "texto_pantalla": "Filtros: médicos, especialidad, servicio, consultorio, estado y búsqueda",
            "narracion": (
                "Con todos los médicos juntos, la semana se llena. Para eso están los filtros de esta fila. En "
                "Médicos elijo a la doctora Ana Pérez, y el calendario muestra solo sus citas. Al encender "
                "Disponibilidad, se pintan en verde las horas en que la doctora atiende y todavía tiene turnos "
                "libres. En la semana, las citas de una misma hora se agrupan en un bloque. Abro el de las ocho: a "
                "la derecha se listan sus citas, y toco la de Juan Carlos Batista. Sale su panel, con el paciente, "
                "el médico, el motivo, el consultorio y los botones para verla, editarla, reprogramarla o cambiar "
                "su estado. Los demás "
                "filtros funcionan igual: especialidad, servicio, consultorio y estado. Limpiar los quita todos."
            ),
            "acciones": [
                marca("app-agenda-filters", "los filtros de esta fila", 4000),
                click(FILTRO.format("staffIds"), "En Médicos"),
                click("mat-option:has-text('Ana Pérez')", "la doctora Ana"),
                {"presionar": {"tecla": "Escape"}, "al_decir": "muestra solo"},
                click("mat-slide-toggle:has-text('Disponibilidad') button", "encender Disponibilidad"),
                click(".fc-timegrid-event:has-text('08:00') >> nth=0", "Abro el de las ocho"),
                click(".hour-group-item:has-text('Juan Carlos Batista')", "toco la de"),
                marca(".detail-actions", "los botones para verla", 5500),
                marca(FILTRO.format("appointmentTypeCatalogId"), "especialidad, servicio", 3500),
                click("button:has-text('Limpiar')", "Limpiar los quita"),
            ],
        },
        {
            "id": "03-lista",
            "capitulo": "La vista de lista y la búsqueda",
            "rotulo": "Lista y búsqueda",
            "ruta": "Calendario › Lista",
            "texto_pantalla": "Lista: cada fila es una cita, con su hora, el paciente y el médico",
            "narracion": (
                "Vuelvo a los botones de vista y elijo la de lista. Es la más cómoda para recepción: cada fila es una cita, con su hora, el "
                "paciente y el médico, agrupadas por día. Para encontrar a alguien uso la búsqueda: escribo "
                "Natalia, y la lista se filtra mientras escribo. Aparece su cita con la doctora Ana Pérez: es la que la paciente reservó por internet, "
                "desde el portal. La reserva en línea no necesita que nadie la cargue: llega sola a la agenda."
            ),
            "acciones": [
                click(VISTA.format("view_list"), "elijo la de lista"),
                marca(".fc-list-event >> nth=0", "cada fila es", 4000),
                escribir("app-agenda-filters input[formcontrolname='searchTerm']", "Natalia", "escribo Natalia"),
                marca(".fc-list-event:has-text('Natalia')", "Aparece su cita", 6000),
            ],
        },
        {
            "id": "04-centro",
            "capitulo": "La Agenda del Centro",
            "rotulo": "Agenda del Centro",
            "ruta": "Calendario › Agenda del Centro",
            "texto_pantalla": "Una columna por médico · el día de todo el centro en una pantalla",
            "narracion": (
                "Para ver el día de todo el centro, pulso Agenda del Centro, arriba. Aquí cada columna es un "
                "médico, con cuántas citas tiene, y cada tarjeta es una cita, con la hora, el paciente, su estado "
                "y el servicio. Con las flechas y el botón Hoy se cambia de día. Solo médicos con citas esconde "
                "las columnas vacías, y mostrar canceladas añade las que se cancelaron, que normalmente se "
                "ocultan para no estorbar: aparece la de Mariela Guzmán. El más de cada columna agenda una cita "
                "nueva con ese médico."
            ),
            "acciones": [
                click("button:has-text('Agenda del Centro')", "pulso Agenda"),
                marca("app-center-agenda .col >> nth=0", "cada columna es", 4500),
                marca("app-center-agenda .apt >> nth=0", "cada tarjeta", 4500),
                marca("app-center-agenda button[aria-label='Día siguiente']", "Con las flechas", 3000),
                click("mat-slide-toggle:has-text('Solo médicos con citas') button", "Solo médicos con citas"),
                click("mat-slide-toggle:has-text('Mostrar canceladas') button", "mostrar canceladas"),
                marca("app-center-agenda .apt:has-text('Mariela Guzmán')", "aparece la de", 4500),
                marca("app-center-agenda button[aria-label='Nueva cita para este médico'] >> nth=0",
                      "El más de", 4000),
            ],
        },
        {
            "id": "05-periodo",
            "capitulo": "Las citas de un período",
            "rotulo": "Por período",
            "ruta": "Calendario › Agenda del Centro › Por período",
            "texto_pantalla": "Por período: todas las citas de varios días, agrupadas por día",
            "narracion": (
                "Arriba a la derecha está la otra vista, por período. Muestra todas las citas de un rango de "
                "fechas, por defecto una semana, agrupadas por día. Cada fila es una cita: la hora, el médico, el "
                "paciente, el servicio y el estado. Los mismos filtros sirven aquí: abro el filtro de Servicio, y "
                "en la lista elijo evaluación cardiológica. Quedan solo las citas del cardiólogo. Al tocar cualquier fila se abre el detalle "
                "de la cita."
            ),
            "acciones": [
                click("app-center-agenda button:has-text('Por período')", "la otra vista"),
                marca("app-center-agenda mat-date-range-input, app-center-agenda mat-form-field:has(mat-label:has-text('Período'))",
                      "un rango de", 4000),
                marca("app-center-agenda .row-apt >> nth=0", "Cada fila es", 5000),
                click(FILTRO.format("appointmentTypeCatalogId"), "abro el filtro"),
                click("mat-option:has-text('Evaluación cardiológica')", "elijo evaluación"),
                marca("app-center-agenda .row-apt >> nth=0", "Quedan solo", 4500),
            ],
        },
        {
            "id": "06-medico",
            "capitulo": "La agenda de un médico",
            "rotulo": "Agenda del médico",
            "ruta": "Médicos › Ana Pérez › Agenda › Citas",
            "texto_pantalla": "La agenda propia del médico: su semana y su lista de citas",
            "narracion": (
                "Y cada médico tiene su propia agenda en su ficha. Entro a Médicos y abro a la doctora Ana Pérez. "
                "En la pestaña Agenda, la vista Citas muestra su semana, con cuántas citas tiene cada día, y debajo "
                "la lista, con la hora, el paciente, el servicio y el consultorio. Desde el botón Estado de cada "
                "cita se confirma, se registra la llegada o se marca que no asistió. En la próxima parte agendamos "
                "una cita y la atendemos de principio a fin."
            ),
            "acciones": [
                click(RAIL.format("Médicos"), "Entro a Médicos"),
                click("button.dsel__row:has-text('Ana Pérez')", "abro a la doctora"),
                click(TAB_AGENDA, "En la pestaña"),
                marca(".ag-tab__week",
                      "muestra su semana", 4500),
                marca("app-doctor-appointments-tab button:has-text('Estado') >> nth=0", "Desde el botón Estado", 5000),
            ],
        },
    ],
    comentario="Estado C: modo avanzado, agenda llena (hoy en todos los estados) y la reserva en línea de Natalia "
               "Ramírez con Ana Pérez.",
)

# ── PARTE 5 · Agendar y atender una cita ───────────────────────────────────────────────────────────
guion(
    "citas-05-agendar-atender",
    "Citas · Parte 5: agendar, confirmar y atender",
    "Quinta parte de la serie de Citas de RegiSalud: la cita de punta a punta desde recepción. Agendar una cita "
    "nueva (paciente, médico, servicio, motivo, prioridad, turno, cobertura, recordatorios por WhatsApp y correo), "
    "confirmarla, registrar la llegada del paciente, verlo en la Operación del Día y llamarlo a consulta, "
    "reprogramar una cita a otro turno y cancelar otra con su motivo.",
    "C",
    [
        "Agendar una cita eligiendo el turno libre del médico y los recordatorios del paciente",
        "Confirmar la cita y registrar la llegada del paciente",
        "Seguir al paciente en la Operación del Día y llamarlo a consulta",
        "Reprogramar una cita a otro día u hora sin perder su historia",
        "Cancelar una cita dejando el motivo para los informes",
    ],
    [
        "Elegir el turno antes del servicio: los turnos dependen del servicio y del horario del médico",
        "Editar la hora de una cita en vez de reprogramarla: reprogramar avisa al paciente y deja el rastro",
        "Cancelar cuando el paciente simplemente no vino: para eso está «Marcar no asistió»",
    ],
    [
        {
            "id": "01-nueva",
            "capitulo": "Agendar una cita",
            "rotulo": "Nueva cita",
            "ruta": "Calendario › Nueva cita",
            "texto_pantalla": "Paciente, médico y servicio · después el turno",
            "narracion": (
                "Una paciente llama para pedir cita. Entro al calendario, en el menú de la izquierda, y pulso Nueva "
                "cita. Primero el paciente: "
                "escribo Laura, y cuando aparece en la lista, la elijo. Debajo sale su ficha, con la edad, la "
                "cédula y el teléfono. Ahora el médico: escribo Jorge, y en la lista que se abre elijo al doctor "
                "Jorge Medina. Con el médico elegido, el tipo de "
                "cita ofrece solo los servicios que él da: elijo consulta general. Debajo se resumen su duración, "
                "la modalidad y la tarifa. El motivo de la consulta es lo que necesita atender la paciente: elijo "
                "chequeo general en la lista."
            ),
            "acciones": [
                click(RAIL.format("Calendario"), "Entro al calendario"),
                click("button:has-text('Nueva Cita')", "pulso Nueva"),
                escribir(f"{DLG} input[formcontrolname='patientSearch']", "Laura", "escribo Laura"),
                click("mat-option:has-text('Laura Patricia')", "la elijo"),
                marca(f"{DLG} .patient-card, {DLG} .pc, {DLG} :text('Cédula 402-0555009-9')", "su ficha", 3500),
                escribir(f"{DLG} input[formcontrolname='doctorSearch']", "Jorge", "escribo Jorge"),
                click("mat-option:has-text('Jorge Medina')", "elijo al doctor"),
                click(f"{DLG} mat-select[formcontrolname='appointmentTypeCatalogId']", "el tipo de cita"),
                click("mat-option:has-text('Consulta general')", "elijo consulta general"),
                marca(f"{DLG} :text('TIPO DE CITA') >> xpath=..", "se resumen su duración", 4000),
                click(f"{DLG} app-custom-select[formcontrolname='reasonForVisit'] input", "El motivo de la consulta"),
                click("mat-option:has-text('Chequeo General')", "elijo chequeo"),
            ],
        },
        {
            "id": "02-turno",
            "capitulo": "El turno y los recordatorios",
            "rotulo": "Turno y recordatorios",
            "ruta": "Calendario › Nueva cita",
            "texto_pantalla": "Turnos libres del médico · cobertura · recordatorios por WhatsApp y correo",
            "narracion": (
                "La prioridad se queda en normal. Más abajo, en Cuándo, está la semana del doctor: cada día dice "
                "cuántos turnos libres le quedan. Toco el primer día disponible, y aparecen sus turnos. Elijo uno "
                "de la tarde. El consultorio se llena solo, desde el horario del médico. A la derecha está la "
                "cobertura: la paciente paga directo, así que paga la tarifa completa. Los recordatorios salen "
                "por WhatsApp un día antes y por correo una hora antes; se pueden quitar o agregar otros. En cómo "
                "se agendó marco que fue por teléfono, y como la paciente ya la confirmó, marco esa casilla. "
                "Pulso Agendar cita, y la cita queda creada."
            ),
            "acciones": [
                marca(f"{DLG} button:has-text('Normal')", "La prioridad", 2500),
                marca(f"{DLG} .apt-days", "la semana del doctor", 4000),
                click(f"{DLG} button.apt-day:not(.is-dead) >> nth=0", "el primer día disponible"),
                click(f"{DLG} button.apt-slot:has-text('16:00')", "Elijo uno"),
                marca(f"{DLG} :text('Consultorio del turno') >> xpath=..", "El consultorio se llena", 3500),
                marca(f"{DLG} mat-select[formcontrolname='patientInsuranceId']", "la cobertura", 4000),
                marca(f"{DLG} :text('Recordatorios') >> xpath=../..", "Los recordatorios salen", 6000),
                click(f"{DLG} mat-select[formcontrolname='source']", "en cómo se agendó"),
                click("mat-option:has-text('Teléfono')", "por teléfono"),
                click(f"{DLG} mat-checkbox[formcontrolname='isConfirmed']", "marco esa casilla"),
                click(f"{DLG} button:has-text('Agendar cita')", "Pulso Agendar"),
                {"resaltar": ".mat-mdc-snack-bar-container, .custom-alert-dialog-panel mat-dialog-container",
                 "durante_ms": 3500, "cursor": False},
            ],
        },
        {
            "id": "03-confirmar-llegada",
            "capitulo": "Confirmar y registrar la llegada",
            "rotulo": "Confirmar y llegada",
            "ruta": "Calendario › Lista › Panel de la cita",
            "texto_pantalla": "Programada → Confirmada → En espera",
            "narracion": (
                "Ahora una cita de hoy que sigue programada: la de Yesenia Castillo. En la vista de lista toco su fila, "
                "y a la derecha sale su panel. El botón Estado muestra solo los pasos que tocan: confirmar, "
                "registrar la llegada o marcar que no asistió. Confirmo: el sistema pregunta, y digo que sí. El "
                "panel se cierra y la cita ya sale en verde, confirmada. Cuando la paciente llega a recepción, la "
                "abro otra vez, y en el menú Estado registro su llegada. Acepto el aviso. La cita pasa a en espera "
                "y la paciente recibe un turno en la cola de la sala."
            ),
            "acciones": [
                click(VISTA.format("view_list"), "En la vista de lista"),
                click(".fc-list-event:has-text('Yesenia Castillo')", "toco su fila"),
                click("button.status-menu-trigger", "El botón Estado"),
                marca(".mat-mdc-menu-panel", "solo los pasos", 4000, cursor=False),
                click(".mat-mdc-menu-item:has-text('Confirmar')", "Confirmo"),
                {"resaltar": ".custom-alert-dialog-panel mat-dialog-container", "durante_ms": 2500, "cursor": False},
                click(f"{DLG} button:has-text('Sí, confirmar')", "digo que sí"),
                {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3000, "cursor": False},
                marca(".fc-list-event:has-text('Yesenia Castillo') .fc-list-event-dot", "sale en verde", 3500),
                click(".fc-list-event:has-text('Yesenia Castillo')", "la abro otra vez"),
                click("button.status-menu-trigger", "en el menú Estado"),
                click(".mat-mdc-menu-item:has-text('Registrar llegada')", "registro su llegada"),
                click(f"{DLG} button:has-text('Sí, registrar')", "Acepto el aviso"),
                {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3500, "cursor": False},
            ],
        },
        {
            "id": "04-operacion",
            "capitulo": "La Operación del Día",
            "rotulo": "Operación del Día",
            "ruta": "Operación del Día",
            "texto_pantalla": "Citado → Llegó → En cola → En consulta → Cerrado",
            "narracion": (
                "Lo que pasa con los pacientes de hoy se sigue en la Operación del Día. Arriba están las etapas, "
                "con cuántos pacientes hay en cada una: en consulta, en cola, citados y cerrados. Cada fila es un "
                "paciente, con su turno, el consultorio y el médico. Abro a Yesenia Castillo: su recorrido de hoy "
                "dice que fue citada, llegó y está en cola. Cuando el médico está listo, pulso Llamar. El sistema "
                "avisa que la paciente fue llamada, y el turno sale en la pantalla de la sala; acepto el aviso. La "
                "ficha dice a qué hora se llamó. Cuando entra al consultorio, pulso Iniciar atención, y otra vez "
                "acepto. Ahora sí está en consulta. Al terminar, el médico la cierra desde la historia clínica, "
                "con su nota firmada."
            ),
            "acciones": [
                click(RAIL.format("Operación del Día"), "en la Operación del Día"),
                marca(".op-rail__item >> nth=1", "las etapas", 4500),
                marca("button.op-tbl__r >> nth=0", "Cada fila es", 4000),
                click("button.op-tbl__r:has-text('Yesenia Castillo')", "Abro a Yesenia"),
                marca(":text('Recorrido de hoy') >> xpath=..", "su recorrido", 5000),
                click("button:has-text('Llamar')", "pulso Llamar"),
                {"resaltar": ".custom-alert-dialog-panel mat-dialog-container", "durante_ms": 3500, "cursor": False},
                click(f"{DLG} button:has-text('Aceptar')", "acepto el aviso"),
                marca(":text('Falta iniciar la atención') >> xpath=..", "a qué hora se llamó", 3500, cursor=False),
                click("button:has-text('Iniciar atención')", "pulso Iniciar"),
                {"resaltar": ".custom-alert-dialog-panel mat-dialog-container", "durante_ms": 2500, "cursor": False},
                click(f"{DLG} button:has-text('Aceptar')", "otra vez acepto"),
                marca("button:has-text('Finalizar atención')", "Ahora sí está", 3500),
                marca("button:has-text('Historia clínica')", "desde la historia", 4000),
            ],
        },
        {
            "id": "05-reprogramar",
            "capitulo": "Reprogramar una cita",
            "rotulo": "Reprogramar",
            "ruta": "Agenda del Centro › Detalle de la cita › Reprogramar",
            "texto_pantalla": "Reprogramar crea la cita nueva y avisa al paciente",
            "narracion": (
                "Otro paciente, Francisco Javier Cabrera, pide moverse de hora. Vuelvo al calendario y entro a la "
                "Agenda del Centro. En la columna del doctor Jorge Medina está su cita, y la abro: se ve el "
                "detalle completo. Toco el botón Reprogramar. Arriba queda la cita actual, y debajo la "
                "semana del médico con los cupos de cada día. Elijo el primer día con cupos y el turno de las "
                "cinco. Escribo el motivo: el paciente pidió otra hora. Con todo listo, pulso Reprogramar al pie: "
                "se crea la cita nueva, "
                "la anterior queda como reprogramada para la historia, y al paciente le llega un correo."
            ),
            "acciones": [
                click(RAIL.format("Calendario"), "Vuelvo al calendario"),
                click("button:has-text('Agenda del Centro')", "entro a la"),
                click("app-center-agenda .apt:has-text('Francisco Javier')", "y la abro"),
                click("button:has-text('Reprogramar')", "Toco el botón"),
                marca(f"{DLG} :text('Cita actual') >> xpath=..", "la cita actual", 3500),
                click(f"{DLG} button.day:not(.off) >> nth=0", "el primer día con cupos"),
                click(f"{DLG} button.slot:has-text('17:00')", "el turno de las"),
                escribir(f"{DLG} textarea", "El paciente pidió otra hora.", "Escribo el motivo"),
                click(f"{DLG} .mat-mdc-dialog-actions button:has-text('Reprogramar'), {DLG} button.mat-mdc-unelevated-button:has-text('Reprogramar')",
                      "Reprogramar al pie"),
                {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3500, "cursor": False},
            ],
        },
        {
            "id": "06-cancelar",
            "capitulo": "Cancelar una cita",
            "rotulo": "Cancelar",
            "ruta": "Agenda del Centro › Detalle de la cita › Cancelar",
            "texto_pantalla": "Cancelar con motivo · el hueco queda libre para otro paciente",
            "narracion": (
                "Y si un paciente avisa que no vendrá, la cita se cancela. Vuelvo al calendario, entro otra vez a la "
                "Agenda del Centro, y en la columna de la doctora Ana Pérez abro la de Rafael Antonio Núñez. Pulso Cancelar cita. El sistema pregunta con el número y la hora, y pide "
                "el motivo: solicitud del paciente. Ese motivo queda en la cita y en el informe de cancelaciones. "
                "Las notas son opcionales, para el equipo. Ahora sí, pulso Cancelar la cita. La cita queda "
                "cancelada, el turno queda libre para otro paciente y los recordatorios se anulan. Si el paciente "
                "simplemente no vino, no se cancela: se marca que no asistió, desde el botón Estado. Con esto "
                "cerramos la serie de citas."
            ),
            "acciones": [
                click(RAIL.format("Calendario"), "Vuelvo al calendario"),
                click("button:has-text('Agenda del Centro')", "entro otra vez"),
                click("app-center-agenda .apt:has-text('Rafael Antonio') >> nth=0", "abro la de Rafael"),
                click("button:has-text('Cancelar cita')", "Pulso Cancelar cita"),
                marca(f"{DLG} mat-select", "solicitud del paciente", 4500),
                marca(f"{DLG} textarea", "Las notas son", 2500),
                click(f"{DLG} button:has-text('Cancelar la cita')", "pulso Cancelar la cita"),
                {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3500, "cursor": False},
                marca(":text-is('Cancelada') >> nth=0", "queda cancelada", 5000, cursor=False),
                marca(":text('Rafael Antonio Núñez') >> nth=0", "no se cancela", 6000, cursor=False),
            ],
        },
    ],
    comentario="Estado C. Laura Patricia Santana con Jorge Medina (primer día con cupos, 16:00); confirma y registra "
               "la llegada de Yesenia Castillo (Ana, 11:00 de hoy); la llama en la Operación del Día; reprograma a "
               "Francisco Javier Cabrera (Jorge 15:00) y cancela a Rafael Antonio Núñez (Ana 10:30).",
)
