from comun import *
g = base_p("Proyectos · Crear un proyecto y conocer su espacio de trabajo",
  "Cómo crear un proyecto en Germiva con su cliente, su gerente, su equipo, su centro de costo y su almacén de obra, recorrer las pestañas de su espacio de trabajo y registrar sus tareas.",
  "Video 01 de la serie Proyectos. setup: seeds/proyectos/preparar.sh inicio (Constructora Germiva Demo; cliente Industrias Germiva del Caribe, centro CC-NAVE, Laura Méndez como segunda usuaria).",
  "/projects", "button:has-text('Nuevo proyecto')", "inicio",
  ["Crear un proyecto con cliente, gerente y equipo", "Conectarlo a un centro de costo y a un almacén de obra",
   "Recorrer las pestañas del proyecto", "Registrar las tareas del proyecto"],
  ["Dejar el proyecto sin centro de costo: sus gastos caen en el predeterminado",
   "Buscar Control o Avance antes de aprobar el presupuesto: aparecen después",
   "Escribir el presupuesto a mano en la ficha: se calcula desde el presupuesto del proyecto"])
pasos = [
 paso("01-cartera", "La cartera", "Cartera de proyectos", "Proyectos › Proyectos",
  "Todos los proyectos, con su avance y su salud",
  """Un proyecto reúne todo lo de una obra o un contrato: su presupuesto, sus compras, sus horas y su facturación. Esta es
  la Cartera de proyectos, en el menú Proyectos. Recojo el menú. Arriba resume los proyectos activos, lo comprometido y los
  que están en riesgo; y abajo lista cada proyecto con su estado, su avance y sus indicadores. Todavía no hay ninguno:
  voy a crear el primero con el botón Nuevo proyecto.""",
  [res("section.pf-figures", "Arriba resume", 5500),
   clic("button.panel-collapse", "Recojo el menú"),
   res("thead >> nth=0", "abajo lista cada proyecto", 5000),
   clic("button:has-text('Nuevo proyecto')", "con el botón Nuevo proyecto")]),
 paso("02-datos", "Los datos del proyecto", "Crear Proyecto", "Proyectos › Proyectos › Nuevo",
  "Nombre · fechas · cliente · gerente · equipo",
  """Empiezo por el nombre: Nave industrial Haina. El código lo asigna el sistema, y el estado empieza en Planificación.
  Después van las fechas. En Fecha de inicio escribo el dos de noviembre de dos mil veintiséis. Y en Fecha de fin, el treinta
  de abril del año siguiente. El presupuesto, el costo real y el avance no se escriben aquí: se calculan solos desde el
  presupuesto del proyecto. Sigo con las relaciones. En Cliente escribo Industrias, para buscar al dueño de la obra.
  Aparece en la lista, y lo elijo. En Gerente de proyecto escribo Admin, para buscar al responsable. Aparece, y lo elijo:
  el gerente ve todo el proyecto. En Miembros del equipo abro la lista, marco a Laura Méndez, y cierro la lista. Solo el
  gerente, el equipo y quien tenga permiso para ver todos pueden abrir el proyecto.""",
  [esc("input[formcontrolname='name']", "Nave industrial Haina", "Empiezo por el nombre"),
   res("mat-form-field:has(mat-select[formcontrolname='status'])", "el estado empieza", 2500),
   esc("input[formcontrolname='startDate']", "02/11/2026", "En Fecha de inicio escribo"),
   esc("input[formcontrolname='endDate']", "30/04/2027", "Y en Fecha de fin"),
   res("app-project-derived-figures", "no se escriben aquí", 5500),
   esc("app-custom-select[formcontrolname='partner'] input", "Industrias", "En Cliente escribo Industrias"),
   clic("mat-option:has-text('Industrias Germiva')", "y lo elijo"),
   esc("app-custom-select[formcontrolname='projectManager'] input", "Admin", "escribo Admin"),
   clic("mat-option:has-text('Administrador')", "Aparece, y lo elijo"),
   clic("mat-select[formcontrolname='teamMembers']", "abro la lista"),
   clic("mat-option:has-text('Laura')", "marco a Laura"),
   {"presionar": {"tecla": "Escape"}, "al_decir": "cierro la lista"}]),
 paso("03-contabilidad", "Centro de costo y almacén", "Contabilidad y almacén", "Proyectos › Proyectos › Nuevo",
  "El proyecto conectado a la contabilidad y al inventario",
  """La última sección conecta el proyecto con la contabilidad y con el inventario. En Centro de costo abro la lista, y
  elijo Obra Nave Haina: los ingresos y gastos del proyecto que no traigan un centro propio irán a ese. En Almacén de obra
  escribo Sur, para buscar el almacén. Aparece, y lo elijo: lo que se compre para el proyecto entrará por omisión a ese
  almacén. Pulso Guardar. El sistema confirma que el proyecto quedó creado, y acepto.""",
  [clic("app-cost-center-field mat-select", "En Centro de costo abro"),
   clic("mat-option:has-text('CC-NAVE')", "elijo Obra Nave Haina"),
   esc("app-custom-select[formcontrolname='warehouse'] input", "Sur", "escribo Sur"),
   clic("mat-option:has-text('Almacén Sur')", "Aparece, y lo elijo"),
   clic(".project-actions button:has-text('Guardar')", "Pulso Guardar"),
   res("mat-dialog-container", "El sistema confirma", 2500),
   clic("mat-dialog-container button", "y acepto")]),
 paso("04-espacio", "El espacio de trabajo", "Las pestañas del proyecto", "Proyectos › Cartera › PRJ",
  "Cada pestaña es una parte del proyecto",
  """Este es el espacio de trabajo del proyecto. Arriba, su nombre, el estado, el cliente, el gerente y las fechas. Y debajo,
  las pestañas, una por cada parte de la obra. Resumen muestra el tablero y la ficha que acabo de llenar. Presupuesto, el
  desglose de costos y precios. Facturación, el contrato con el cliente y sus facturas. Subcontratos, lo pactado con cada
  subcontratista. Horas, la mano de obra de la semana. Y Tareas, el trabajo por hacer. Cuando el presupuesto esté aprobado
  aparecerán tres pestañas más: Control, Avance y Cambios.""",
  [res("header.ws-header", "Arriba, su nombre", 5000),
   res("a.ws-tab:has-text('Resumen')", "Resumen muestra", 3500),
   res("a.ws-tab:has-text('Presupuesto')", "Presupuesto, el", 3000),
   res("a.ws-tab:has-text('Facturación')", "Facturación, el contrato", 3500),
   res("a.ws-tab:has-text('Subcontratos')", "Subcontratos, lo pactado", 3000),
   res("a.ws-tab:has-text('Horas')", "Horas, la mano", 3000),
   res("a.ws-tab:has-text('Tareas')", "Y Tareas", 2500),
   res("nav.ws-tabs", "aparecerán tres pestañas", 5000)]),
 paso("05-tareas", "Las tareas", "Tareas del proyecto", "Proyectos › Cartera › PRJ › Tareas",
  "Responsable, fecha límite y dependencias",
  """Abro la pestaña Tareas, y pulso Nueva tarea. En Nombre escribo la primera: Permiso de construcción. Con el nombre
  escrito, en Responsable abro la lista, y elijo a Laura Méndez. La tarea también lleva estado, prioridad, fecha límite,
  horas estimadas, y las tareas de las que depende. Guardo, y el aviso lo confirma. La tarea queda en la lista del
  proyecto, y más adelante se puede vincular a una partida del presupuesto. Con el proyecto creado, el siguiente paso es
  su presupuesto.""",
  [clic("a.ws-tab:has-text('Tareas')", "Abro la pestaña Tareas"),
   clic("button:has-text('Nueva tarea')", "pulso Nueva tarea"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   esc("mat-dialog-container input[formcontrolname='name']", "Permiso de construcción", "En Nombre escribo"),
   clic("mat-dialog-container [formcontrolname='assignedUser']", "en Responsable abro"),
   clic("mat-option:has-text('Laura')", "elijo a Laura"),
   res("mat-dialog-container .task-grid", "La tarea también lleva", 5500),
   clic("mat-dialog-container button:has-text('Guardar')", "Guardo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("tr:has-text('Permiso de construcción')", "La tarea queda en la lista", 4500),
   res("a.ws-tab:has-text('Presupuesto')", "el siguiente paso", 3000)]),
]
guardar("proyectos-01-crear-proyecto", g, pasos)
