from comun import *
g = base_p("Proyectos · Facturar por hitos: el plan de cobros y la factura de cada hito",
  "Cómo cobrar un proyecto por hitos en Germiva: armar el plan de cobros con un porcentaje del contrato por hito, marcar un hito listo para facturar y generar su factura en Ventas. Y cuándo conviene tiempo y materiales.",
  "Video 12 de la serie Proyectos. setup: seeds/proyectos/preparar.sh hitos (proyecto de supervisión con contrato por hitos de 600,000 y dos hitos: 30 % y 40 %).",
  "/projects/17/facturacion", "button:has-text('Nuevo hito')", "hitos",
  ["Armar el plan de cobros de un contrato por hitos", "Marcar un hito listo para facturar",
   "Generar la factura del hito", "Cuándo usar hitos, cubicaciones o tiempo y materiales"],
  ["Dejar el plan de cobros sin llegar al monto del contrato",
   "Facturar el hito por fuera, con una factura suelta en Ventas",
   "Creer que la factura ya quedó emitida: nace en borrador"])
D = "mat-dialog-container "
pasos = [
 paso("01-plan", "El plan de cobros", "Plan de cobros", "Proyectos › Cartera › PRJ › Facturación",
  "Cada hito, un porcentaje del contrato",
  """No todos los proyectos se cobran midiendo avance. Un servicio, como esta supervisión de obra, se cobra por hitos: se
  factura al cumplir cada entrega pactada. En la pestaña Facturación, recojo el menú lateral para ganar espacio, y bajo al plan de cobros por hitos.
  Ya hay dos hitos, del treinta y del cuarenta por ciento del contrato. El aviso lo dice: faltan ciento ochenta mil pesos
  por planificar. Pulso Nuevo hito. En el nombre escribo Entrega final, que es el cierre de este servicio de supervisión. El valor puede ser un porcentaje
  del contrato, o un monto fijo; lo dejo en porcentaje, y anoto treinta, que es justo lo que faltaba. En la condición
  escribo lo que debe cumplirse para cobrarlo: Acta de recepción firmada. Con esos datos completos, pulso Guardar. El
  plan llega a los seiscientos mil pesos del contrato, y el aviso desaparece.""",
  [res("header.ws-header h1", "Un servicio, como esta", 3500),
   clic("button.panel-collapse", "recojo el menú"),
   res("#billing-milestones-title", "bajo al plan de cobros", 2500),
   res("section:has(#billing-milestones-title) tbody tr >> nth=0 >> td >> nth=1", "Ya hay dos hitos", 3500),
   res("section:has(#billing-milestones-title) :text('por planificar') >> nth=0", "El aviso lo dice", 4000),
   clic("button:has-text('Nuevo hito')", "Pulso Nuevo hito"),
   esc(D + "input[formcontrolname='name']", "Entrega final", "En el nombre escribo"),
   res(D + "app-segmented-control", "El valor puede ser", 4500),
   esc(D + "input[formcontrolname='percentage']", "30", "y anoto treinta"),
   esc(D + "textarea[formcontrolname='condition']", "Acta de recepción firmada", "En la condición"),
   clic(D + "button:has-text('Guardar')", "pulso Guardar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("section:has(#billing-milestones-title) tbody tr >> nth=2 >> td >> nth=1", "El\n  plan llega".replace("\n  ", " "), 4500)]),
 paso("02-facturar", "Del hito a la factura", "Facturar un hito", "Proyectos › Cartera › PRJ › Facturación",
  "Listo para facturar → factura en borrador en Ventas",
  """El primer hito ya se cumplió: el cliente firmó los planos. En su fila abro el menú de acciones, y elijo Marcar listo
  para facturar. El sistema pide confirmar; pulso Marcar listo. El hito cambia de estado, y facturación recibe el aviso.
  Ahora la fila muestra el botón Facturar. Lo pulso. La vista previa trae el monto del hito, ciento ochenta mil pesos, el
  ITBIS, y el total de la factura. Si el contrato tuviera anticipo, aquí se descontaría su amortización. Pulso Generar
  factura. La factura nace en borrador en Ventas, con el proyecto en la cabecera; allí se revisa y se emite con su
  comprobante fiscal. El hito queda como Facturado, y abajo, en Facturas del proyecto, aparece la factura con su origen.""",
  [clic("button[aria-label='Más acciones del hito 1']", "abro el menú de acciones"),
   clic(".mat-mdc-menu-panel button:has-text('Marcar listo')", "y elijo Marcar listo"),
   res("mat-dialog-container", "El sistema pide confirmar", 2500),
   clic("mat-dialog-container button:has-text('Marcar listo')", "pulso Marcar listo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("section:has(#billing-milestones-title) tbody tr >> nth=0 >> td >> nth=5", "Ahora la fila muestra", 2500),
   clic("section:has(#billing-milestones-title) button:has-text('Facturar')", "Lo pulso"),
   res(D + ":text('Monto del hito') >> nth=0", "La vista previa trae", 4500),
   res(D + ":text('Total de la factura') >> nth=0", "y el total de la factura", 5000),
   clic(D + "button:has-text('Generar factura')", "Pulso Generar\n  factura".replace("\n  ", " ")),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3500, "cursor": False},
   res("section:has(#billing-milestones-title) tbody tr >> nth=0 >> td >> nth=5", "El hito queda como Facturado", 3500),
   res("section:has(#billing-documents-title) tbody tr >> nth=0 >> td >> nth=0", "aparece la factura", 4500)]),
 paso("03-modos", "Tres formas de facturar", "¿Hitos, avance u horas?", "Proyectos › Cartera › PRJ › Facturación",
  "Hitos · Cubicaciones · Tiempo y materiales",
  """La forma de facturar se elige una sola vez, en el contrato de venta del proyecto. Por hitos, como aquí, para entregas
  pactadas. Por avance, con cubicaciones, para obras que se miden partida por partida. Y por tiempo y materiales, cuando se
  cobra lo trabajado: el sistema propone la factura del período con las horas aprobadas, a su tarifa de venta, y los
  gastos facturables del proyecto. En los tres casos la factura sale de aquí, del proyecto, y por eso el contrato siempre
  sabe cuánto se ha facturado y cuánto falta.""",
  [res("#billing-contract-title", "La forma de facturar", 5000),
   res("#billing-milestones-title", "Por hitos, como aquí", 4500),
   res("#billing-figures-title", "Por avance, con cubicaciones", 6000),
   res("#billing-contract-title", "Y por tiempo y materiales", 7000),
   res("#billing-documents-title", "En los tres casos", 5000),
   res("#billing-figures-title", "el contrato siempre", 4500)]),
]
guardar("proyectos-12-facturar-por-hitos", g, pasos)
