from comun import *
g = base_p("Proyectos · Aprobar el presupuesto, línea base y revisiones",
  "Cómo se envía a aprobación el presupuesto de un proyecto en Germiva, quién puede aprobarlo, qué es la línea base, cómo crear una revisión, comparar versiones y definir los niveles de aprobación por monto.",
  "Video 04 de la serie Proyectos. setup: seeds/proyectos/preparar.sh por-aprobar (presupuesto completo en borrador, preparado por el administrador; Laura Méndez es la otra supervisora). El video cambia de usuario en cámara.",
  "/projects", "button[aria-label='Abrir proyecto']", "por-aprobar",
  ["Enviar el presupuesto a aprobación", "Por qué lo aprueba otra persona", "Qué son la línea base y el presupuesto vigente",
   "Crear una revisión y comparar versiones"],
  ["Querer aprobar el presupuesto que uno mismo preparó", "Editar una versión aprobada: se crea una revisión",
   "Enviar a aprobación con cambios sin guardar"])
ABRIR = [clic("button[aria-label='Abrir proyecto']", "abro el proyecto"),
         clic("a.ws-tab:has-text('Presupuesto')", "pestaña Presupuesto"),
         clic("button[aria-label='Ver presupuesto']", "Ver presupuesto")]
pasos = [
 paso("01-enviar", "Enviar a aprobación", "Enviar a aprobación", "Proyectos › Cartera › PRJ › Presupuesto",
  "Borrador → En aprobación",
  """Un presupuesto en borrador todavía no controla nada: primero hay que aprobarlo. Recojo el menú, abro el proyecto, voy a
  su pestaña Presupuesto, y lo abro con Ver presupuesto. Arriba se ven los pasos de la versión: borrador, en aprobación,
  aprobada y vigente. El presupuesto ya está completo: cinco millones de costo, y seis millones seiscientos mil de precio.
  Bajo hasta el final de las partidas, y pulso Enviar a aprobación. El sistema pide confirmar; confirmo. La versión pasa a
  En aprobación y ya no se puede editar. Pero yo no puedo aprobarla: quien prepara o envía un presupuesto no lo aprueba.
  Lo tiene que hacer otra persona con ese permiso.""",
  [clic("button.panel-collapse", "Recojo el menú"), *ABRIR,
   res("ol.version-bar__steps", "los pasos de la versión", 5000),
   res(".budget-figs .gm-fig >> nth=0", "cinco millones de costo", 2500),
   res(".budget-figs .gm-fig:has-text('Precio antes de impuestos')", "seis millones seiscientos", 3000),
   res("table.tree tr:has-text('Total del presupuesto') td >> nth=0", "Bajo hasta el final", 2000),
   clic("button:has-text('Enviar a aprobación')", "pulso Enviar a aprobación"),
   res("mat-dialog-container", "El sistema pide confirmar", 1500),
   clic("mat-dialog-container button.confirm-button", "confirmo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("ol.version-bar__steps", "ya no se puede editar", 4000),
   res("button.topbar-user", "Lo tiene que hacer otra persona", 3500, True)]),
 paso("02-aprobar", "Aprobar", "Aprueba otra persona", "Proyectos › Cartera › PRJ › Presupuesto",
  "Quien prepara no aprueba",
  """Salgo, para que entre Laura Méndez, la otra supervisora de la empresa. Abro el menú del usuario, y cierro sesión. En el
  acceso entro como Laura: escribo su usuario. Después, en el campo de la contraseña, escribo su clave. Con el usuario y la
  clave ya escritos, pulso el botón Iniciar sesión.""",
  [clic("button.topbar-user", "Abro el menú del usuario"),
   clic(".mat-mdc-menu-panel :text('Cerrar sesión')", "cierro sesión"),
   esc("input[formcontrolname='username']", "laura.mendez", "escribo su usuario"),
   esc("input[formcontrolname='password']", "Demo2026!", "escribo su clave"),
   clic("button.auth-primary-btn", "pulso el botón Iniciar")]),
 paso("03-aprobar", "Aprobar", "Decisión de aprobación", "Proyectos › Cartera › PRJ › Presupuesto",
  "Aprobado: línea base y presupuesto vigente",
  """Ya con la sesión de Laura, en la cartera de Proyectos abro el proyecto, voy a su pestaña Presupuesto, y entro con Ver
  presupuesto. Al final de la versión está la Decisión de aprobación, con el nivel que le toca. En Observaciones escribo
  una nota: Revisado contra la cotización. La nota es opcional al aprobar, y obligatoria si se rechaza. Pulso Aprobar
  nivel uno. El sistema pide confirmar; confirmo, y el aviso lo confirma. La versión queda aprobada y congelada: es la
  línea base del proyecto, y también el presupuesto vigente, contra el que se controlarán las compras, las horas y las
  facturas.""",
  [*ABRIR,
   res("app-budget-approval", "la Decisión de aprobación", 4000),
   esc("app-budget-approval textarea", "Revisado contra la cotización.", "En Observaciones escribo"),
   clic("app-budget-approval button:has-text('Aprobar nivel 1')", "Pulso Aprobar\n  nivel uno".replace("\n  ", " ")),
   res("mat-dialog-container", "El sistema pide confirmar", 1500),
   clic("mat-dialog-container button.confirm-button", "confirmo, y el aviso"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("ol.version-bar__steps", "queda aprobada y congelada", 5000),
   res("nav.ws-tabs", "contra el que se controlarán", 4500)],
  navegar="/projects"),
 paso("04-revision", "Revisiones y versiones", "Crear revisión", "Proyectos › Cartera › PRJ › Presupuesto",
  "Una versión aprobada no se edita: se revisa",
  """Una versión aprobada no se edita. Si los costos cambian, se crea una revisión. Abajo, en Nueva revisión, escribo el
  motivo: Ajuste del precio del acero. Con el motivo escrito, pulso Crear revisión. Nace la versión dos, en borrador, con
  todas las partidas copiadas. Ahí se corrigen costos y cantidades; el precio pactado con el cliente no cambia en una
  revisión interna: para eso están las órdenes de cambio. Mientras la versión dos no se apruebe, la uno sigue vigente. Y el
  selector Comparar con muestra, partida por partida, la diferencia entre dos versiones.""",
  [res("table.tree tr:has-text('Total del presupuesto') td >> nth=0", "se crea una revisión", 2000),
   esc("app-budget-approval input, input[placeholder*='revisión'], mat-form-field:has-text('Motivo de la revisión') input", "Ajuste del precio del acero", "escribo el\n  motivo".replace("\n  ", " ")),
   clic("button:has-text('Crear revisión')", "pulso Crear revisión"),
   res("section.version-bar mat-form-field:has-text('Versión') >> nth=0", "Nace la versión dos", 5000),
   res(".budget-figs .gm-fig:has-text('Precio antes de impuestos')", "el precio pactado", 6000),
   res("section.version-bar mat-form-field:has-text('Comparar con')", "selector Comparar con", 5500)]),
 paso("05-niveles", "Niveles de aprobación", "Configuración de presupuestos", "Proyectos › Configuración de presupuestos",
  "Hasta tres niveles, según el monto",
  """Quién aprueba se define en Proyectos, Configuración de presupuestos. Abajo están los niveles de aprobación por monto:
  de uno a tres, cada uno con su límite y con el permiso que lo aprueba. Un presupuesto pequeño lo firma el primer nivel;
  uno grande necesita, en orden, la firma de cada nivel. Con el presupuesto aprobado, el proyecto ya puede controlar lo que
  se compra.""",
  [res("h1, .page-title, app-breadcrumb >> nth=0", "Configuración de presupuestos", 3000),
   res(":text('Niveles de aprobación por monto') >> nth=0", "los niveles de aprobación", 4000),
   res("button:has-text('Agregar nivel')", "de uno a tres", 5000, True),
   res(":text('Niveles de aprobación por monto') >> nth=0", "Un presupuesto pequeño", 6000)],
  navegar="/projects/settings"),
]
guardar("proyectos-04-aprobar-presupuesto", g, pasos)
