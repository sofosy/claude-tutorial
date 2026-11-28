"""Citas y turnos · Parte 6: la configuración de la agenda (RegiSalud), 2026-11.

  python3 seeds/clinica/guiones_citas_config.py   → escribe guiones/citas-06-configuracion.json

Pedido del usuario: la serie de Citas debe incluir la configuración y cómo el paciente se agenda solo según
el horario configurado. Las partes 1 (médico y horario) y 2 (reserva por internet) ya lo muestran en detalle;
esta parte reúne los ajustes generales de la agenda y cierra en el enlace que usa el paciente.

Estado previo: cualquiera con los médicos y horarios de la serie de Citas (citas.mjs C).
"""
from comun import guion

R = lambda texto, ms=3500, **k: {"resaltar": texto, "durante_ms": ms, **k}  # noqa: E731
CITAS = ":text('Citas Médicas') >> xpath=ancestor::*[2]"


def citas_06():
    pasos = [
        {
            "id": "01-recordatorios", "capitulo": "Recordatorios de las citas", "rotulo": "Configuración de la agenda",
            "navegar": "/company/preferences", "ruta": "Configuración › Preferencias › Operación › Citas Médicas",
            "texto_pantalla": "Los ajustes generales de la agenda del centro",
            "narracion": (
                "En este video vemos los ajustes generales de la agenda. Los horarios de cada médico ya los vimos "
                "en la parte uno. Los ajustes del centro están en Configuración, Preferencias, pestaña Operación. "
                "Ahí está la sección Citas Médicas. Al paciente le llega un recordatorio veinticuatro horas antes de "
                "su cita, y un segundo recordatorio: aquí se dice cuántos minutos antes sale. Lo cambio a dos horas: "
                "ciento veinte minutos."
            ),
            "acciones": [
                {"click": "[role=tab]:has-text('Operación')", "al_decir": "pestaña Operación"},
                R(":text('Citas Médicas')", 2500, al_decir="la sección Citas Médicas"),
                R("mat-form-field:has([formcontrolname='appointmentReminderMinutesBefore'])", 3500,
                  al_decir="un segundo recordatorio"),
                {"escribir": {"sel": "input[formcontrolname='appointmentReminderMinutesBefore']", "texto": "120"},
                 "al_decir": "Lo cambio a dos horas"},
            ],
        },
        {
            "id": "02-enlace", "capitulo": "El enlace de reservas del centro", "rotulo": "Enlace de reservas",
            "ruta": "Configuración › Preferencias › Operación › Citas Médicas",
            "texto_pantalla": "Un solo enlace para todo el centro",
            "narracion": (
                "Al lado está el enlace de reservas del centro. Es uno solo para todos los médicos, y dice cuántos "
                "se pueden reservar en línea. Un médico aparece en el enlace cuando su consulta está marcada para "
                "reserva en línea y tiene franjas visibles para pacientes, como vimos en la parte uno. Copiar enlace "
                "lo deja listo para pegarlo en WhatsApp, en las redes o en la página web del centro."
            ),
            "acciones": [
                R("app-center-booking-link", 4000, al_decir="el enlace de reservas del centro"),
                R(":text('reservables en línea')", 3500, al_decir="dice cuántos"),
                {"click": "button:has-text('Copiar enlace')", "al_decir": "Copiar enlace"},
            ],
        },
        {
            "id": "03-whatsapp", "capitulo": "Avisos por WhatsApp", "rotulo": "Avisos por WhatsApp",
            "ruta": "Configuración › Preferencias › Operación › Avisos por WhatsApp",
            "texto_pantalla": "Confirmación, recordatorio, reprogramación y cancelación por WhatsApp",
            "narracion": (
                "Los avisos de la cita salen siempre por correo. Si el centro conectó su WhatsApp en WhatsApp e IA, "
                "este interruptor los manda también por WhatsApp: la confirmación, el recordatorio, la "
                "reprogramación y la cancelación, cada uno con su plantilla aprobada. El sistema ya trae las "
                "plantillas redactadas. Termino con Guardar."
            ),
            "acciones": [
                R(":text('Avisos por WhatsApp')", 2500, al_decir="Los avisos de la cita"),
                R("mat-slide-toggle[formcontrolname='appointmentWhatsappEnabled']", 4500, al_decir="este interruptor"),
                {"click": "button:has(mat-icon:text('save')):has-text('Guardar')", "al_decir": "Termino con Guardar"},
            ],
        },
        {
            "id": "04-portal", "capitulo": "Las reservas del portal", "rotulo": "Portal del paciente",
            "navegar": "/agenda/configurar-portal-paciente", "al_decir_navegar": "En el Calendario",
            "ruta": "Calendario › Configurar portal del paciente",
            "texto_pantalla": "Con reservas del portal, el paciente entra con su correo",
            "narracion": (
                "Lo guardado queda para todos. En el Calendario, Configurar portal del paciente decide cómo "
                "reserva el paciente. Con Permitir reservas desde el portal encendido, entra con su correo y un "
                "código, y si el sistema lo reconoce, la cita se crea sola. Apagado, solo deja sus datos y la "
                "recepción vincula la reserva."
            ),
            "acciones": [
                R("mat-slide-toggle:has-text('Permitir acceso al portal')", 2500, al_decir="decide cómo"),
                R("mat-slide-toggle:has-text('Permitir reservas desde el portal')", 5000, al_decir="Con Permitir reservas"),
                R("button:has-text('Guardar configuración')", 2500, al_decir="la recepción vincula"),
            ],
        },
        {
            "id": "05-paciente", "capitulo": "Lo que ve el paciente", "rotulo": "El paciente se agenda",
            "navegar": "/book/centro/los-prados", "al_decir_navegar": "veamos el otro lado",
            "ruta": "Enlace de reservas del centro (lo que ve el paciente)",
            "texto_pantalla": "Especialidad, médico y hora: solo lo que los horarios permiten",
            "narracion": (
                "Para terminar, veamos el otro lado. Y así lo ve el paciente cuando abre el enlace: primero elige la "
                "especialidad, por ejemplo medicina general, y salen sus médicos con los próximos turnos libres, "
                "sacados de los horarios que configuramos, sin bloqueos ni horas ocupadas. Toca una hora y la "
                "reserva sigue: entra con su correo y confirma. Ese paso a paso está en la parte dos. Con esto "
                "termina la serie de citas y turnos."
            ),
            "acciones": [
                R(":text('Elige la especialidad')", 1800, al_decir="cuando abre el enlace"),
                {"click": ":text('Medicina General')", "al_decir": "por ejemplo medicina general"},
                R(":text('Próximos turnos') >> nth=0", 4000, al_decir="los próximos turnos"),
                R(":text('Próximos turnos') >> xpath=.. >> button >> nth=0", 3000, al_decir="Toca una hora"),
                R(":text('Correo y acceso')", 3000, al_decir="entra con su correo"),
            ],
        },
    ]
    return guion(
        "citas-06-configuracion", "Citas y turnos · Parte 6: la configuración de la agenda",
        "Sexta parte de la serie de Citas y turnos de RegiSalud: los ajustes generales de la agenda (recordatorios, "
        "enlace de reservas del centro, avisos por WhatsApp y reservas del portal) y cómo el paciente se agenda "
        "solo desde el enlace, según los horarios configurados.",
        pasos, comentario="Estado: citas.mjs C (médicos con horario y consulta reservable).", portada_s=4,
    )


if __name__ == "__main__":
    print(citas_06())
