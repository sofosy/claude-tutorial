from comun import *
g = base_p("Proyectos · Planificación de recursos: quién está disponible y quién está sobreasignado",
  "Cómo planificar a tu gente por semana en Germiva: la capacidad de cada empleado según su horario, vacaciones y feriados, las horas asignadas a cada proyecto y el aviso de semana sobreasignada.",
  "Video 14 de la serie Proyectos. setup: seeds/proyectos/preparar.sh horas (la obra con su presupuesto aprobado y dos empleados de obra, Juan Pérez Germiva y Ramón Díaz Germiva).",
  "/projects/resource-plan", "app-custom-select input", "horas",
  ["Leer la capacidad semanal de cada empleado", "Asignar horas de un proyecto por semana",
   "Detectar y corregir una semana sobreasignada", "Ver solo a la gente de un proyecto"],
  ["Planificar sin elegir el proyecto: las casillas no aparecen",
   "Asignar más horas que la capacidad de la semana",
   "Confundir lo planificado con el costo: el costo llega con las horas aprobadas"])
JUAN = "input[aria-label^='Horas del proyecto para Juan'] >> nth="
RAMON = "input[aria-label^='Horas del proyecto para Ramón'] >> nth="
pasos = [
 paso("01-capacidad", "Capacidad y asignaciones", "Planificación de recursos", "Proyectos › Planificación de recursos",
  "Asignado / capacidad, por empleado y semana",
  """Antes de que empiece la semana conviene saber quién está disponible. En Proyectos, Planificación de recursos, cada
  fila es un empleado, y cada columna una semana. Las dos cifras son horas asignadas sobre capacidad. La capacidad sale del
  horario laboral de la persona, menos sus vacaciones, permisos y días feriados. En Buscar empleado escribo Germiva, para
  quedarme solo con la cuadrilla de la obra, que lleva ese apellido en los datos de ejemplo. Quedan Juan y Ramón. Para
  asignar horas hay que elegir el proyecto. En Proyecto a planificar escribo Nave, y espero a que el sistema busque entre
  los proyectos activos. Aparece la nave de Haina, y la elijo. Ahora cada semana tiene su casilla.""",
  [res("table thead th >> nth=1", "cada\n  fila es un empleado".replace("\n  ", " "), 4000),
   res("table tbody tr >> nth=0 >> td >> nth=1", "Las dos cifras son", 4000),
   res("table tbody tr >> nth=0 >> td >> nth=4", "menos sus vacaciones", 3500),
   esc("mat-form-field:has(mat-label:has-text('Buscar empleado')) input", "Germiva", "escribo Germiva"),
   res("table tbody tr >> nth=1 >> td >> nth=0", "Quedan Juan y Ramón", 2500),
   esc("app-custom-select input", "Nave", "escribo Nave"),
   clic("mat-option:has-text('Nave industrial')", "y la elijo"),
   res(JUAN + "0", "Ahora cada semana", 3000)]),
 paso("02-asignar", "Asignar y equilibrar", "Semana sobreasignada", "Proyectos › Planificación de recursos",
  "En rojo, la semana que supera la capacidad",
  """A Juan le planifico cuarenta horas esta semana, que es lo normal de un albañil en la obra. La barra azul muestra cuánto
  de su capacidad queda ocupado. Para la semana siguiente le anoto sesenta, porque toca vaciar las zapatas completas. La
  casilla se pone en rojo, y arriba sale el aviso: una semana sobreasignada. Sesenta horas superan las cincuenta de su
  capacidad. Lo corrijo: a Juan le dejo cincuenta, que es el máximo que su horario permite esa semana. Y las diez que
  faltan se las asigno a Ramón, el ayudante, que tenía la semana libre. El aviso desaparece. Con el botón Solo los de este
  proyecto, la lista se queda con la gente planificada en la obra. Esto es un plan: no genera costo. El costo llega
  después, cuando las horas se registran y se aprueban.""",
  [esc(JUAN + "0", "40", "le planifico cuarenta"),
   res("table tbody tr >> nth=0 >> td >> nth=1", "La barra azul", 3000),
   esc(JUAN + "1", "60", "le anoto sesenta"),
   {"presionar": {"tecla": "Tab"}, "al_decir": "La\n  casilla se pone".replace("\n  ", " ")},
   res(":text('sobreasignada en esta página') >> nth=0", "arriba sale el aviso", 4500),
   esc(JUAN + "1", "50", "le dejo cincuenta"),
   esc(RAMON + "1", "10", "se las asigno a Ramón"),
   {"presionar": {"tecla": "Tab"}, "al_decir": "El aviso desaparece"},
   clic("button:has-text('Solo los de este proyecto')", "Con el botón Solo"),
   res("table tbody tr >> nth=0 >> td >> nth=0", "Esto es un plan", 3000),
   res("table tbody tr >> nth=1 >> td >> nth=0", "cuando las horas se registran", 3500)]),
]
guardar("proyectos-14-planificacion-de-recursos", g, pasos)
