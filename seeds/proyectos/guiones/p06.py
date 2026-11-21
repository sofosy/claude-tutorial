from comun import *
g = base_p("Proyectos · Órdenes de cambio: adicionales, deductivas y firma del cliente",
  "Cómo registrar en Germiva una orden de cambio cuando el cliente modifica el alcance, el precio o el plazo de un proyecto: crearla, enviarla a aprobación, aprobarla y ver cómo cambia el contrato y el presupuesto vigente.",
  "Video 06 de la serie Proyectos. setup: seeds/proyectos/preparar.sh cambios (presupuesto aprobado; orden deductiva OCB-001 «Luminarias que suple el cliente» enviada por Laura, por −30,000 de costo y −39,600 de precio).",
  "/projects/17/cambios", "table.orders", "cambios",
  ["Crear una orden de cambio adicional sobre una partida", "Enviarla a aprobación y aprobar la de otra persona",
   "Ver el contrato original, los cambios y el contrato vigente", "Cuándo exigir la firma del cliente"],
  ["Cambiar el precio con una revisión interna: el precio pactado solo cambia con una orden de cambio",
   "Querer anular una orden aprobada: se revierte con una deductiva",
   "Aprobar sin la referencia del cliente cuando el proyecto exige su firma"])
D = "mat-dialog-container "
pasos = [
 paso("01-cambios", "La pestaña Cambios", "Órdenes de cambio", "Proyectos › Cartera › PRJ › Cambios",
  "Contrato original · cambios · contrato vigente",
  """En una obra, el cliente casi siempre pide cambios: más metros, otro acabado, un plazo distinto. Cada cambio se
  registra como una orden de cambio. Se llevan en la pestaña Cambios del proyecto. Recojo el menú. Arriba, el
  contrato original: seis millones seiscientos mil pesos; los cambios aprobados; y el contrato vigente, que es la suma
  de los dos. A la derecha, lo que está en aprobación, y cómo quedaría el contrato si se aprueba. Y abajo, la lista de
  órdenes: hay una en aprobación, que preparó Laura.""",
  [res("header.ws-header h1", "el cliente casi siempre", 3500),
   res("a.ws-tab:has-text('Cambios')", "en la pestaña Cambios", 2500),
   clic("button.panel-collapse", "Recojo el menú"),
   res(".gm-fig:has-text('Contrato original'), :text('Contrato original') >> nth=0", "el\n  contrato original".replace("\n  ", " "), 3500),
   res(":text('Contrato vigente') >> nth=0", "y el contrato vigente", 4000),
   res(":text('Contrato si se aprueban') >> nth=0", "cómo quedaría el contrato", 4000),
   res("table.orders tbody tr >> nth=0 >> td >> nth=1", "hay una en aprobación", 4000)]),
 paso("02-nueva", "Nueva orden de cambio", "Nueva orden de cambio", "Proyectos › Cartera › PRJ › Cambios",
  "Tipo · título · origen · plazo · partidas que cambian",
  """Registro un cambio nuevo: el cliente quiere doscientos metros más de piso. Pulso Nueva orden de cambio. El tipo ya dice
  Adicional, porque aumenta el contrato; Deductivo lo reduce, y Sin costo solo cambia el plazo. En Título escribo
  Ampliación del piso industrial. Con el título de la orden ya escrito, en Plazo anoto cinco: son los días que el cambio agrega a la
  entrega. En Referencia del cliente escribo el documento donde lo pidió: Carta del 18 de noviembre. Ahora las
  partidas que cambian. Pulso Partida existente. En el buscador escribo Piso, para buscar la partida. Aparece en la
  lista, y la elijo. En Cantidad anoto doscientos, los metros cuadrados adicionales que pidió el cliente. En Costo anoto ciento cuarenta mil pesos, lo
  que cuesta hacerlos. Y en Precio anoto ciento ochenta y cuatro mil ochocientos, lo que se le cobra al cliente. Pulso
  Guardar, y el aviso lo confirma.""",
  [clic("button:has-text('Nueva orden de cambio')", "Pulso Nueva orden de cambio"),
   res(D + "app-segmented-control[formcontrolname='changeType']", "El tipo ya dice", 6500),
   esc(D + "input[formcontrolname='title']", "Ampliación del piso industrial", "En Título escribo"),
   esc(D + "input[formcontrolname='scheduleDays']", "5", "en Plazo anoto cinco"),
   esc(D + "input[formcontrolname='clientReference']", "Carta del 18 de noviembre", "Referencia del cliente escribo"),
   clic(D + "button:has-text('Partida existente')", "Pulso Partida existente"),
   esc(D + "input[aria-label='Partida de la línea 1']", "Piso", "escribo Piso"),
   clic("mat-option:has-text('03.01')", "y la elijo"),
   esc(D + "input[formcontrolname='quantity']", "200", "En Cantidad anoto doscientos"),
   esc(D + "input[formcontrolname='costAmount']", "140000", "En Costo anoto"),
   esc(D + "input[formcontrolname='priceAmount']", "184800", "en Precio anoto"),
   clic(D + "button:has-text('Guardar')", "Pulso\n  Guardar".replace("\n  ", " ")),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
 paso("03-enviar", "Enviar a aprobación", "Detalle de la orden", "Proyectos › Cartera › PRJ › Cambios › OCB-002",
  "Partidas, recorrido y soporte",
  """La orden queda en borrador, con su número. La abro con un clic en el número. El detalle muestra la partida que cambia y
  el efecto de la orden: ciento cuarenta mil más de costo, y ciento ochenta y cuatro mil ochocientos más de precio.
  En Recorrido se ve por dónde va; y en Soporte se adjunta la carta firmada por el cliente. Pulso Enviar a aprobación. El
  sistema pide confirmar; confirmo. Igual que el presupuesto, una orden de cambio la aprueba otra persona, no quien la
  preparó.""",
  [clic("table.orders tr:has-text('OCB-002') button.link", "con un clic en el número"),
   res("#change-order-detail table >> nth=0", "la partida que cambia", 7000),
   res("#change-order-detail :text('Recorrido') >> nth=0", "En Recorrido", 2500),
   res("#change-order-detail button:has-text('Adjuntar')", "en Soporte se adjunta", 3500, True),
   clic("#change-order-detail button:has-text('Enviar a aprobación')", "Pulso Enviar a aprobación"),
   res("mat-dialog-container", "El\n  sistema pide confirmar".replace("\n  ", " "), 1500),
   clic("mat-dialog-container button.confirm-button, mat-dialog-container button:has-text('Enviar')", "confirmo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("table.orders tr:has-text('OCB-002') td >> nth=7", "la aprueba otra persona", 4500)]),
 paso("04-aprobar", "Aprobar", "Aprobar orden de cambio", "Proyectos › Cartera › PRJ › Cambios › OCB-001",
  "Al aprobarse, cambia el contrato y el presupuesto vigente",
  """La que sí puedo aprobar es la de Laura: el cliente decidió comprar él mismo las luminarias. La abro. Es deductiva:
  baja treinta mil de costo, y treinta y nueve mil seiscientos de precio. Pulso Aprobar. El sistema avisa que, al
  aprobarla, se suma al presupuesto vigente y al contrato del proyecto; confirmo, y el aviso lo confirma. Arriba, las
  cifras cambiaron: el contrato vigente bajó a seis millones quinientos sesenta mil cuatrocientos pesos. Una orden
  aprobada ya no se anula: si hay que deshacerla, se registra otra en sentido contrario. Y si el proyecto debe exigir la
  firma del cliente antes de aprobar, se activa en el control de su presupuesto.""",
  [clic("table.orders tr:has-text('OCB-001') button.link", "La abro"),
   res("#change-order-detail table >> nth=0", "Es deductiva", 6000),
   clic("#change-order-detail button:has-text('Aprobar')", "Pulso Aprobar"),
   res("mat-dialog-container", "El sistema avisa", 5500),
   clic("mat-dialog-container button:has-text('Aprobar')", "confirmo, y el aviso"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res(":text('Contrato vigente') >> nth=0", "el contrato vigente bajó", 6000),
   res("table.orders tr:has-text('OCB-001') td >> nth=7", "ya no se anula", 6000),
   res("a.ws-tab:has-text('Presupuesto')", "se activa en el control", 4000)]),
]
guardar("proyectos-06-ordenes-de-cambio", g, pasos)
