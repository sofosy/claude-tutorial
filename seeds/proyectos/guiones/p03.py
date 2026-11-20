from comun import *
g = base_p("Proyectos · Análisis de precio unitario, indirectos, utilidad e ITBIS del presupuesto",
  "Cómo desglosar en Germiva el costo de una partida con el análisis de precio unitario, aplicar indirectos y utilidad para llegar al precio del cliente, completar el detalle de la partida y exportar el presupuesto a PDF y Excel.",
  "Video 03 de la serie Proyectos. setup: seeds/proyectos/preparar.sh borrador (presupuesto en borrador con seis partidas; «Zapatas y pedestales» sin costo; indirectos y utilidad en cero).",
  "/projects", "button[aria-label='Abrir proyecto']", "borrador",
  ["Desglosar una partida en materiales y mano de obra", "Aplicar indirectos y utilidad para obtener el precio",
   "Completar fechas, tarea e ITBIS de una partida", "Exportar el presupuesto a PDF y Excel"],
  ["Escribir las cantidades del análisis por el total de la partida: van por unidad",
   "Confundir costo con precio: la utilidad se aplica sobre el costo",
   "Enviar al cliente el PDF interno, que muestra los costos"])
A = "aside.apu-panel "
pasos = [
 paso("01-apu", "Análisis de precio unitario", "Análisis de precio unitario", "Proyectos › Cartera › PRJ › Presupuesto",
  "El costo de una partida, desglosado en recursos",
  """Este presupuesto ya tiene sus seis partidas, pero a Zapatas y pedestales le falta el costo. En lugar de escribirlo, lo
  voy a calcular. Recojo el menú, abro el proyecto, voy a su pestaña Presupuesto, y abro el presupuesto con Ver
  presupuesto. En la fila de Zapatas pulso el botón de Análisis de precio unitario. Se abre un panel a la derecha: aquí se
  desglosa lo que cuesta una sola unidad de la partida, en este caso un metro cúbico. Pulso Agregar recurso. En
  Descripción escribo el primero: Hormigón. El tipo ya dice Material. En Cantidad por unidad anoto uno. Es un metro cúbico
  de hormigón por cada metro cúbico de zapata. Y en Costo unitario anoto seis mil trescientos pesos.""",
  [clic("button.panel-collapse", "Recojo el menú"),
   clic("button[aria-label='Abrir proyecto']", "abro el proyecto"),
   clic("a.ws-tab:has-text('Presupuesto')", "pestaña Presupuesto"),
   clic("button[aria-label='Ver presupuesto']", "abro el presupuesto con Ver"),
   clic("button[aria-label='Análisis de precio unitario de la partida 01.02']", "pulso el botón de Análisis"),
   res(A + ">> nth=0", "Se abre un panel", 6000),
   clic(A + "button:has-text('Agregar recurso')", "Pulso Agregar recurso"),
   esc(A + "mat-form-field:has-text('Descripción') input >> nth=0", "Hormigón", "Descripción escribo"),
   esc(A + "mat-form-field:has-text('Cantidad por unidad') input >> nth=0", "1", "Cantidad por unidad anoto uno"),
   esc(A + "mat-form-field:has-text('Costo unitario') input >> nth=0", "6300", "anoto seis mil trescientos")]),
 paso("02-apu-mo", "Análisis de precio unitario", "Aplicar al borrador", "Proyectos › Cartera › PRJ › Presupuesto",
  "Materiales + mano de obra = costo por unidad",
  """Falta la mano de obra. Agrego otro recurso. En su tipo abro la lista, y elijo Mano de obra. En su descripción
  escribo Cuadrilla de vaciado. Con la descripción lista, en su cantidad por unidad anoto uno también. Y en su costo
  unitario anoto dos mil setecientos pesos, lo que cobra la cuadrilla por metro cúbico. Arriba, el panel suma: el costo
  por unidad es nueve mil pesos, y el de la partida, con sus ochenta metros cúbicos, setecientos veinte mil. Si un
  material se desperdicia, se indica en su porcentaje de desperdicio. Pulso Aplicar al borrador, y el costo pasa a la
  partida. Cierro el panel.""",
  [clic(A + "button:has-text('Agregar recurso')", "Agrego otro recurso"),
   clic(A + "mat-form-field:has-text('Tipo') mat-select >> nth=1", "En su tipo abro"),
   clic("mat-option:has-text('Mano de obra')", "elijo Mano de obra"),
   esc(A + "mat-form-field:has-text('Descripción') input >> nth=1", "Cuadrilla de vaciado", "escribo Cuadrilla"),
   esc(A + "mat-form-field:has-text('Cantidad por unidad') input >> nth=1", "1", "anoto uno también"),
   esc(A + "mat-form-field:has-text('Costo unitario') input >> nth=1", "2700", "anoto dos mil setecientos"),
   res(A + ":text('Costo por unidad') >> nth=0", "el panel suma", 9000),
   res(A + "mat-form-field:has-text('Desperdicio') >> nth=0", "Si un\n  material".replace("\n  ", " "), 4500),
   clic(A + "button:has-text('Aplicar al borrador')", "Pulso Aplicar al borrador"),
   {"click_opcional": "button[aria-label='Cerrar el análisis de precio unitario']", "al_decir": "Cierro el panel"}]),
 paso("03-porcentajes", "Del costo al precio", "Indirectos y utilidad", "Proyectos › Cartera › PRJ › Presupuesto",
  "Costo directo + indirectos + utilidad = precio",
  """Con todas las partidas costeadas, el costo directo de la obra es cinco millones de pesos. Para llegar al precio del
  cliente faltan los porcentajes. En Indirectos anoto diez: son los gastos de la obra que no pertenecen a una partida,
  como la supervisión. Imprevistos lo dejo en cero. Y en Utilidad anoto veinte, la ganancia sobre el costo. Las cifras se
  recalculan al momento: el precio antes de impuestos queda en seis millones seiscientos mil pesos. Abajo, cada partida
  muestra ya su precio, y la última fila da el total. Pulso Guardar presupuesto, y el aviso lo confirma.""",
  [res(".budget-figs .gm-fig >> nth=0", "el costo directo de la obra", 4500),
   esc("label.rate:has-text('Indirectos') input", "10", "En Indirectos anoto diez"),
   res("label.rate:has-text('Imprevistos')", "Imprevistos lo dejo", 2000),
   esc("label.rate:has-text('Utilidad') input", "20", "en Utilidad anoto veinte"),
   res(".budget-figs .gm-fig:has-text('Precio antes de impuestos')", "el precio antes de impuestos", 5000),
   res("table.tree tr:has-text('Total del presupuesto') td >> nth=0", "la última fila", 2500),
   clic("button:has-text('Guardar presupuesto')", "Pulso Guardar presupuesto"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
 paso("04-detalle", "El detalle y la exportación", "Fechas, tarea y detalle", "Proyectos › Cartera › PRJ › Presupuesto",
  "Fechas, tarea, ITBIS · PDF y Excel",
  """Cada partida tiene además su detalle. Abro el menú de la primera, y elijo Fechas, tarea y detalle. Aquí van el inicio
  y el fin previstos de la partida, que arman el cronograma; la tarea del proyecto a la que se vincula; y el ITBIS
  estimado, con base presunta si el contrato la admite. También sus propios porcentajes de indirectos y utilidad, si
  difieren de los generales. Cancelo, y subo a la barra de versión. Con el presupuesto guardado, Excel descarga la
  estructura completa, que también sirve de plantilla para importar. Y PDF genera dos documentos: uno para el cliente,
  solo con precios, y uno interno, con los costos.""",
  [clic("button[aria-label^='Más acciones de Excavación']", "Abro el menú de la primera"),
   clic(".mat-mdc-menu-panel button:has-text('Fechas, tarea y detalle')", "elijo Fechas, tarea"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   res("mat-dialog-container [formcontrolname='plannedStartDate']", "el inicio\n  y el fin".replace("\n  ", " "), 4000),
   res("mat-dialog-container mat-form-field:has-text('Tarea vinculada')", "la tarea del proyecto", 3500),
   res("mat-dialog-container mat-form-field:has-text('ITBIS estimado')", "y el ITBIS\n  estimado".replace("\n  ", " "), 5000),
   res("mat-dialog-container mat-form-field:has-text('Indirectos de esta partida')", "sus propios porcentajes", 5000),
   clic("mat-dialog-container button:has-text('Cancelar')", "Cancelo"),
   res("button:has-text('Excel / plantilla')", "Excel descarga", 6000, True),
   clic("button:has-text('PDF')", "Y PDF genera"),
   res(".mat-mdc-menu-panel", "uno para el cliente", 6000)]),
]
guardar("proyectos-03-precio-unitario", g, pasos)
