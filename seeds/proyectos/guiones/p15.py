from comun import *
g = base_p("Proyectos · Mis horas: cómo registra el empleado su semana",
  "Cómo llena un empleado su hoja de tiempo en Germiva: copiar la semana anterior, anotar las horas de cada día, ver lo planificado y enviar la semana a aprobación.",
  "Video 15 de la serie Proyectos. setup: seeds/proyectos/preparar.sh mis-horas (Juan Pérez Germiva, albañil, con usuario propio, la hoja de la semana pasada y 40 h planificadas esta semana). La sesión del video es la de Juan.",
  "/projects/timesheets/mine", "button:has-text('Copiar semana anterior')", "mis-horas",
  ["Entrar a Mis horas con tu propio usuario", "Copiar los renglones de la semana anterior",
   "Anotar las horas de cada día", "Enviar la semana a aprobación"],
  ["Esperar a fin de mes para llenar las horas", "Olvidar enviar la hoja: en borrador no llega al supervisor",
   "Querer editar una hoja ya enviada sin retirarla primero"])
g["sesion"]["cuerpo"] = {"username": "juan.perez", "password": "Demo2026!"}
D = "mat-dialog-container "
pasos = [
 paso("01-copiar", "Mi hoja de la semana", "Mis horas", "Proyectos › Mis horas",
  "Cada empleado registra su propia semana",
  """Las horas de un proyecto las puede registrar el encargado, o cada empleado por su cuenta. Juan, albañil de la obra,
  entra con su usuario a Proyectos, Mis horas. Arriba ve su nombre y su puesto. Esta semana todavía está vacía. En vez de
  armarla desde cero, pulso Copiar semana anterior. El diálogo lo explica: crea la hoja con los mismos renglones de la
  semana pasada, con su proyecto, su partida y su tipo de hora. Confirmo con el botón Copiar. La hoja aparece con el renglón de Zapatas.
  Y debajo de su nombre, el sistema le recuerda lo planificado para él: cuarenta horas esta semana.""",
  [res("button.topbar-user", "o cada empleado por su cuenta", 3500),
   res("section.content h2 >> nth=0", "Arriba ve su nombre", 3000),
   res("button:has-text('Copiar semana anterior')", "En vez de", 2500, True),
   clic("button:has-text('Copiar semana anterior')", "pulso Copiar semana anterior"),
   res("mat-dialog-container", "El diálogo lo explica", 6000),
   clic(D + "button:has-text('Copiar') >> nth=-1", "Confirmo con el botón"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("table tbody tr >> nth=0 >> td >> nth=2", "con el renglón de Zapatas", 3000),
   res("table tbody tr >> nth=0 >> td >> nth=0", "le recuerda lo planificado", 4500)]),
 paso("02-enviar", "Anotar y enviar", "Enviar a aprobación", "Proyectos › Mis horas",
  "Las horas se envían por semana",
  """Ahora anota lo trabajado. El lunes, ocho horas, la jornada completa en las zapatas. El martes, otras ocho horas en la
  misma partida de la obra. Y el miércoles, ocho más, con el vaciado ya terminado. La fila suma las horas de la semana.
  Aparece la barra de cambios sin guardar: pulso Guardar borrador, y el aviso lo confirma. Mientras esté en borrador,
  la hoja se puede seguir llenando día a día. Al terminar la semana, abro el menú de la hoja, y elijo Enviar a aprobación.
  El sistema pide confirmar, y confirmo. Desde aquí la hoja no se edita; si hay un error, se retira desde el mismo menú.
  El supervisor la recibe en Horas por aprobar, y al aprobarla, su costo entra al proyecto.""",
  [esc("input.cin.cell >> nth=0", "8", "El lunes, ocho horas"),
   esc("input.cin.cell >> nth=1", "8", "El martes, otras ocho"),
   esc("input.cin.cell >> nth=2", "8", "Y el miércoles"),
   res("tr:has-text('Total de la semana') td >> nth=0", "La fila suma", 2500),
   clic("button:has-text('Guardar borrador')", "pulso Guardar borrador"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("table tbody tr >> nth=0 >> td >> nth=-2", "Mientras esté en borrador", 3500),
   clic("button[aria-label^='Acciones de la hoja']", "abro el menú de la hoja"),
   clic(".mat-mdc-menu-panel button:has-text('Enviar a aprobación')", "elijo Enviar a aprobación"),
   res("mat-dialog-container >> nth=0", "El sistema pide confirmar", 2500),
   clic("mat-dialog-container button.confirm-button, mat-dialog-container button:has-text('Enviar')", "y confirmo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("table tbody tr >> nth=0 >> td >> nth=-2", "El supervisor la recibe", 4500)]),
]
guardar("proyectos-15-mis-horas", g, pasos)
