from comun import *
g = base_p("Proyectos · Crear el presupuesto del proyecto: fases y partidas",
  "Cómo crear en Germiva el presupuesto de un proyecto, organizarlo en fases y partidas, y dar a cada partida su categoría de costo, su cuenta, su unidad, su cantidad y su costo unitario.",
  "Video 02 de la serie Proyectos. setup: seeds/proyectos/preparar.sh con-proyecto (proyecto Nave industrial Haina creado, sin presupuesto).",
  "/projects", "button[aria-label='Abrir proyecto']", "con-proyecto",
  ["Crear el presupuesto de un proyecto", "Organizarlo en fases y partidas",
   "Completar categoría, cuenta, unidad, cantidad y costo de una partida", "Guardar el borrador"],
  ["Crear las partidas sueltas, fuera de su fase", "Dejar una partida sin categoría o sin cuenta: no se puede enviar a aprobación",
   "Elegir «Solo costos» cuando también se quiere el precio al cliente"])
T = "table.tree "
pasos = [
 paso("01-nuevo", "Nuevo presupuesto", "Presupuestos de proyecto", "Proyectos › Cartera › PRJ › Presupuesto",
  "Nombre · moneda · tipo de presupuesto",
  """El presupuesto del proyecto dice cuánto va a costar la obra, partida por partida, y a qué precio se le vende al
  cliente. Recojo el menú, y abro el proyecto desde la cartera. Voy a su pestaña Presupuesto. Todavía no tiene ninguno:
  pulso Nuevo presupuesto. En el nombre escribo Presupuesto de obra. La moneda es el peso, con tasa uno. Y en el tipo hay
  dos opciones: Solo costos, para controlar el gasto, o Costos y precio al cliente, que además calcula el precio de venta
  y el ITBIS. Dejo esta última, y pulso Crear presupuesto. El aviso lo confirma.""",
  [clic("button.panel-collapse", "Recojo el menú"),
   clic("button[aria-label='Abrir proyecto']", "abro el proyecto"),
   clic("a.ws-tab:has-text('Presupuesto')", "pestaña Presupuesto"),
   clic("button:has-text('Nuevo presupuesto')", "pulso Nuevo presupuesto"),
   esc("input[formcontrolname='name']", "Presupuesto de obra", "En el nombre escribo"),
   res("mat-form-field:has(mat-select[formcontrolname='budgetType'])", "en el tipo hay", 9000),
   clic("button:has-text('Crear presupuesto')", "pulso Crear presupuesto"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
 paso("02-fase", "Fases y partidas", "Estructura y partidas", "Proyectos › Cartera › PRJ › Presupuesto",
  "Una fase agrupa partidas",
  """El presupuesto se arma como un árbol: fases, capítulos y partidas. Abajo, en Estructura y partidas, pulso Agregar
  fase. Le pongo nombre: Cimentación. La fase solo agrupa; los costos van en sus partidas. Con la fase creada, abro su
  menú de tres puntos, y elijo Agregar partida, para que quede dentro de la fase. En el nombre de la partida escribo
  Excavación y relleno. Cada partida recibe su código, cero uno punto cero uno, que la identifica en compras, horas y
  facturas.""",
  [res("#structure-title", "en Estructura y partidas", 2500),
   clic("button:has-text('Agregar fase')", "pulso Agregar\n  fase".replace("\n  ", " ")),
   esc(T + "input[aria-label='Fase 01']", "Cimentación", "Le pongo nombre"),
   clic("button[aria-label^='Más acciones de Cimentación']", "abro su\n  menú".replace("\n  ", " ")),
   clic(".mat-mdc-menu-panel button:has-text('Agregar partida')", "elijo Agregar partida"),
   esc(T + "input[aria-label='Partida 01.01']", "Excavación y relleno", "En el nombre de la partida escribo"),
   res(T + "tr:has(input[aria-label='Partida 01.01']) td >> nth=0", "Cada partida recibe su código", 6000)]),
 paso("03-partida", "Los datos de la partida", "Categoría, cuenta, unidad, cantidad y costo", "Proyectos › Cartera › PRJ › Presupuesto",
  "Cantidad × costo unitario = costo directo",
  """Ahora los datos de la partida. En Categoría de costo abro la lista, y elijo Subcontratos, porque la excavación la
  hará un subcontratista. En Cuenta de costo escribo Costos de obra, la cuenta donde se contabilizará su gasto. Aparece
  en la lista, y la elijo. En Unidad escribo Metro, para buscar la unidad de medida. De la lista elijo Metro Cúbico. En
  Cantidad anoto quinientos. Son los metros cúbicos que hay que mover. Y en Costo unitario anoto ochocientos pesos por
  metro, el precio que cotizó el subcontratista. Arriba, el costo directo se calcula solo: cuatrocientos mil pesos. Pulso Guardar presupuesto, y el aviso lo confirma. Las
  demás partidas se agregan igual; y si el presupuesto es grande, se llena la plantilla de Excel y se importa.""",
  [clic(T + "mat-select[aria-label='Categoría de costo']", "En Categoría de costo abro"),
   clic("mat-option:has-text('Subcontratos')", "elijo Subcontratos"),
   esc(T + "input[placeholder='Buscar cuenta']", "Costos de obra", "En Cuenta de costo escribo"),
   clic("mat-option:has-text('Costos de obra')", "y la elijo"),
   esc(T + "input[placeholder='m², m³, horas…']", "Metro", "En Unidad escribo Metro"),
   clic("mat-option:has-text('Metro Cúbico')", "De la lista elijo"),
   esc(T + "input[aria-label='Cantidad']", "500", "Cantidad anoto quinientos"),
   esc(T + "input[aria-label='Costo unitario']", "800", "anoto ochocientos"),
   res(".budget-figs .gm-fig >> nth=0", "el costo directo se calcula", 4000),
   clic("button:has-text('Guardar presupuesto')", "Pulso Guardar presupuesto"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("button:has-text('Excel / plantilla')", "la plantilla de Excel", 3000, True),
   res("button:has-text('Importar Excel')", "y se importa", 2500, True)]),
]
guardar("proyectos-02-crear-presupuesto", g, pasos)
