from comun import *
g = base_p("Proyectos · Horas de mano de obra: tarifas, hojas de tiempo y aprobación",
  "Cómo llevar en Germiva la mano de obra de un proyecto: definir la tarifa por puesto, registrar las horas de la semana por partida, enviarlas y aprobarlas para que entren al costo real, y consultar el reporte de horas.",
  "Video 10 de la serie Proyectos. setup: seeds/proyectos/preparar.sh horas (presupuesto aprobado; Juan Pérez, albañil, y Ramón Díaz, ayudante; tarifa del puesto Albañil 250 + 30 %; hoja HT-1 de Juan de la semana del 9 de noviembre enviada, 40 h).",
  "/projects/labor-rates", "button:has-text('Nueva tarifa')", "horas",
  ["Definir la tarifa de mano de obra de un puesto", "Registrar las horas de la semana por partida",
   "Aprobar una hoja de tiempo", "Leer el reporte de horas"],
  ["Registrar horas de un puesto sin tarifa: no se pueden costear", "Aprobar la hoja propia: la aprueba otra persona",
   "Olvidar la partida: las horas no llegan al costo del proyecto"])
D = "mat-dialog-container "
pasos = [
 paso("01-tarifas", "Tarifas de mano de obra", "Tarifas estándar", "Proyectos › Tarifas de mano de obra",
  "Costo de la hora por puesto o por empleado",
  """La mano de obra también es costo del proyecto, y se mide con las horas de cada persona. Recojo el menú. Lo primero es
  la tarifa: cuánto cuesta una hora de cada puesto. El albañil ya tiene la suya: doscientos cincuenta pesos la hora, más
  treinta por ciento de cargas. Agrego la del ayudante: pulso Nueva tarifa. Se abre su formulario, que sirve para un
  puesto o para un empleado. En Puesto escribo Ayudante, para buscarlo entre los puestos de la empresa. Aparece en la
  lista, y lo elijo. En Costo de la hora anoto ciento ochenta pesos. Y en Cargas anoto treinta: es el
  porcentaje de seguridad social y prestaciones que se suma a la hora. Pulso Guardar, y el aviso lo confirma. Si una
  persona gana distinto que su puesto, se le pone una tarifa propia, y esa manda.""",
  [res("app-breadcrumb, .breadcrumb >> nth=0", "se mide con las horas", 3000),
   clic("button.panel-collapse", "Recojo el menú"),
   res("tr:has-text('Albañil') td >> nth=4", "ya tiene la suya", 4500),
   clic("button:has-text('Nueva tarifa')", "pulso Nueva tarifa"),
   {"resaltar": "mat-dialog-container h2", "durante_ms": 1500, "cursor": False},
   esc(D + "app-custom-select[formcontrolname='position'] input", "Ayudante", "En Puesto escribo"),
   clic("mat-option:has-text('Ayudante')", "y lo elijo"),
   esc(D + "input[formcontrolname='baseHourlyCost']", "180", "En Costo de la hora anoto"),
   esc(D + "input[formcontrolname='burdenPercentage']", "30", "en Cargas anoto treinta"),
   clic(D + "button:has-text('Guardar')", "Pulso Guardar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("tr:has-text('Ayudante') td >> nth=0", "una tarifa propia", 4000)]),
 paso("02-registrar", "Registrar las horas", "Hojas de tiempo de la semana", "Proyectos › Cartera › PRJ › Horas",
  "Persona · partida · horas de cada día",
  """Las horas se registran por semana. Cada empleado puede llenar las suyas en Mis horas; y en la pestaña Horas del
  proyecto, el encargado las registra por su cuadrilla. Pulso Agregar persona. Se abre el diálogo del renglón. En
  Empleado escribo Ramón Díaz, para buscar al ayudante entre los empleados activos. Aparece en la lista con su nombre
  completo, y lo elijo. En la partida escribo Excavación, que es donde trabajó esta semana. Aparece en la lista, y la
  elijo. Las horas son normales y facturables, como vienen marcadas; confirmo con el botón Agregar. En la fila de Ramón
  anoto las horas de cada día. El lunes trabajó ocho, la jornada normal de la obra. El martes, otra jornada completa de ocho horas. Y el miércoles,
  ocho más, hasta terminar la excavación. La fila calcula el total de horas, y el costo con la tarifa de su puesto. Debajo
  del total de la semana aparece la barra de cambios sin guardar: pulso Guardar borrador, y el aviso lo confirma. La hoja
  de Ramón queda en borrador. Para enviarla, abro el menú de su fila, y elijo Enviar a aprobación. El sistema pide
  confirmar, porque mientras esté por aprobar no se edita; confirmo.""",
  [res("button:has-text('Agregar persona') >> nth=0", "el encargado las registra", 3000, True),
   clic("button:has-text('Agregar persona') >> nth=0", "Pulso Agregar persona"),
   {"resaltar": "mat-dialog-container h2", "durante_ms": 1500, "cursor": False},
   esc(D + "app-custom-select[formcontrolname='employee'] input", "Ramón Díaz", "Empleado escribo Ramón"),
   clic("mat-option:has-text('Ramón Díaz Germiva')", "completo, y lo elijo"),
   esc(D + "input[aria-label='Partida del renglón']", "Excavación", "En la partida escribo"),
   clic("mat-option:has-text('01.01')", "y la\n  elijo".replace("\n  ", " ")),
   clic(D + "button:has-text('Agregar')", "confirmo con el botón Agregar"),
   esc("input.cin.cell >> nth=0", "8", "El lunes trabajó ocho"),
   esc("input.cin.cell >> nth=1", "8", "El martes, otra jornada"),
   esc("input.cin.cell >> nth=2", "8", "Y el miércoles"),
   res("tr:has-text('Total de la semana') td >> nth=0", "Debajo\n  del total".replace("\n  ", " "), 2500),
   clic("button:has-text('Guardar borrador')", "pulso Guardar borrador"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   clic("button[aria-label^='Acciones de la hoja']", "abro el menú de su fila"),
   clic(".mat-mdc-menu-panel button:has-text('Enviar a aprobación')", "elijo Enviar a aprobación"),
   res("mat-dialog-container", "El sistema pide\n  confirmar".replace("\n  ", " "), 3500),
   clic("mat-dialog-container button.confirm-button, mat-dialog-container button:has-text('Enviar')", "edita; confirmo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}],
  navegar="/projects/17/horas"),
 paso("03-aprobar", "Aprobar las horas", "Horas por aprobar", "Proyectos › Horas por aprobar",
  "Al aprobar, la mano de obra entra al costo real",
  """Las hojas enviadas llegan a Horas por aprobar. Aquí está la de Juan Pérez, el albañil, de la semana anterior: cuarenta
  horas, que a su tarifa cuestan trece mil pesos. La abro con Ver. El detalle muestra cada día, la partida, y los avisos
  de Recursos Humanos, si la persona tenía vacaciones o un permiso. Todo está bien, así que pulso Aprobar, y en el
  diálogo confirmo con Aprobar. El aviso lo dice: la mano de obra entró al costo real de la partida, con su asiento
  contable. Y como siempre, nadie aprueba su propia hoja.""",
  [res("tr:has-text('Juan Pérez') td >> nth=2", "Aquí está la de Juan", 4000),
   res("tr:has-text('Juan Pérez') td >> nth=5", "trece mil pesos", 3000),
   clic("tr:has-text('Juan Pérez') button:has-text('Ver')", "La abro con Ver"),
   res("#timesheet-detail", "El detalle muestra", 7000),
   clic("#timesheet-detail button:has-text('Aprobar')", "pulso Aprobar"),
   clic("mat-dialog-container button:has-text('Aprobar')", "confirmo con Aprobar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3500, "cursor": False}],
  navegar="/projects/timesheets/approvals"),
 paso("04-reporte", "Reporte y planificación", "Reporte de horas", "Proyectos › Reporte de horas",
  "Horas por proyecto, empleado y partida",
  """El Reporte de horas reúne todo. Pulso Consultar. Sale cada empleado con su partida, sus horas y su costo, y arriba
  el resumen: horas facturables, no facturables, y la utilización facturable del equipo. Se exporta a Excel. Y en
  Planificación de recursos, en el mismo menú, se asignan por adelantado las horas de cada persona a cada proyecto, semana
  por semana, para ver quién está sobrecargado. Con las horas aprobadas, el control del proyecto ya incluye su mano de
  obra.""",
  [clic("button:has-text('Consultar')", "Pulso Consultar"),
   res("table tbody tr >> nth=0", "Sale cada empleado", 4000),
   res("dl.utilization", "el resumen", 6000),
   res("button:has-text('Exportar a Excel')", "Se exporta a Excel", 2500, True),
   res("app-breadcrumb, .breadcrumb >> nth=0", "Planificación de recursos", 8000)],
  navegar="/projects/timesheets/report"),
]
guardar("proyectos-10-horas", g, pasos)
