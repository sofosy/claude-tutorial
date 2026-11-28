"""Hospitalización · Facturar los cargos del ingreso (RegiSalud), 2026-11.

  python3 seeds/clinica/guiones_hospitalizacion.py   → escribe guiones/hosp-01-facturar-cargos.json

Decisión DP-075 punto 2 (2026-11-28): los cargos aprobados de un ingreso se facturan con «Facturar cargos», en la
pestaña Cuenta del paciente, antes o después del alta. Estado previo: `node seeds/clinica/ars.mjs restaurar H`
(hosp.mjs H: Daniel Polanco ingresado, hemograma y electrocardiograma aprobados, sonografía pendiente).
"""
from comun import guion

R = lambda texto, ms=3500, **k: {"resaltar": texto, "durante_ms": ms, **k}  # noqa: E731
ALERTA = "mat-dialog-container:has(app-custom-alert-dialog)"
SONO = "tr:has-text('Sonografía abdominal')"


def hosp_01():
    pasos = [
        {
            "id": "01-aprobar", "capitulo": "Aprobar los cargos", "rotulo": "Cargos del ingreso",
            "navegar": "/hospitalization/charges", "ruta": "Hospitalización › Cargos",
            "texto_pantalla": "Lo que se le hace al paciente ingresado entra como cargo pendiente",
            "narracion": (
                "Durante un ingreso, cada servicio que recibe el paciente entra como un cargo: laboratorios, "
                "estudios, medicamentos, la habitación. Están en Hospitalización, Cargos. Daniel tiene tres: el "
                "hemograma y el electrocardiograma ya aprobados, y una sonografía pendiente. Un cargo pendiente no "
                "se factura hasta que alguien lo revisa y lo aprueba. En su fila pulso Aprobar, y confirmo. El "
                "aviso dice que quedó aprobado; lo cierro."
            ),
            "acciones": [
                R("tr:has-text('Hemograma completo')", 3000, al_decir="Están en Hospitalización"),
                R(f"{SONO} td >> nth=-2", 3500, al_decir="una sonografía pendiente"),
                {"click": f"{SONO} button:has(mat-icon:text('check_circle'))", "al_decir": "En su fila pulso Aprobar"},
                {"click": f"{ALERTA} button:has-text('Aprobar')", "al_decir": "y confirmo"},
                R(ALERTA, 1800, al_decir="dice que quedó aprobado", cursor=False),
                {"click": "button:has-text('Entendido')", "al_decir": "lo cierro"},
            ],
        },
        {
            "id": "02-facturar", "capitulo": "Facturar cargos", "rotulo": "Facturar cargos",
            "navegar": "/patients/554?tab=cuenta", "al_decir_navegar": "En la ficha",
            "ruta": "Pacientes › ficha › Cuenta › Cargos del ingreso",
            "texto_pantalla": "Una factura con los cargos aprobados que aún no se han facturado",
            "narracion": (
                "Ahora los facturamos. En la ficha de Daniel, pestaña Cuenta, están los cargos del ingreso con su estado y el acumulado. "
                "Los tres están aprobados. Pulso Facturar cargos. El sistema arma una sola factura con los cargos "
                "aprobados que aún no tienen factura, y el aviso dice cuántos entraron. Se puede facturar antes o "
                "después del alta, y las veces que haga falta: un cargo facturado no vuelve a entrar. Pulso Abrir la "
                "factura."
            ),
            "acciones": [
                R(":text('Cargos del ingreso') >> xpath=..", 3500, al_decir="están los cargos"),
                R(".acc__total", 3000, al_decir="y el acumulado"),
                {"click": "button:has-text('Facturar cargos')", "al_decir": "Pulso Facturar cargos"},
                R(ALERTA, 5000, al_decir="y el aviso dice", cursor=False),
                {"click": "button:has-text('Abrir la factura')", "al_decir": "Pulso Abrir la"},
            ],
        },
        {
            "id": "03-factura", "capitulo": "La factura del ingreso", "rotulo": "La factura",
            "ruta": "Ventas › Facturas › Factura del ingreso",
            "texto_pantalla": "En borrador: se revisa, se emite y se cobra como cualquier factura",
            "narracion": (
                "La factura queda en borrador, a nombre de Daniel, con una línea por servicio y el número del "
                "ingreso en las notas. Lo que tiene el mismo servicio y el mismo precio, como la habitación de cada "
                "día, va en una sola línea. Desde aquí se revisa, se emite y se cobra como cualquier factura. Si "
                "algún cargo tuviera cobertura de la ARS, el sistema no lo factura aquí: se factura desde la "
                "autorización del paciente, como vimos en la serie de seguros."
            ),
            "acciones": [
                R(":text('Borrador') >> nth=0", 2500, al_decir="queda en borrador"),
                R(":text('Líneas del documento') >> xpath=ancestor::*[3]", 4000, al_decir="una línea por servicio"),
                R(".invoice-total-block", 3000, al_decir="se emite y se cobra"),
            ],
        },
    ]
    return guion(
        "hosp-01-facturar-cargos", "Hospitalización · Facturar los cargos del ingreso",
        "Hospitalización en RegiSalud: aprobar los cargos del ingreso y facturarlos con «Facturar cargos» desde la "
        "pestaña Cuenta del paciente, antes o después del alta, sin facturar dos veces el mismo cargo.",
        pasos, comentario="Estado: ars.mjs restaurar H (hosp.mjs H).", portada_s=4,
    )


if __name__ == "__main__":
    print(hosp_01())
