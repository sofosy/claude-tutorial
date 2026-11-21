from comun import *
g = base_p("Proyectos · Avance físico, valor ganado, flujo de caja y rentabilidad",
  "Cómo registrar en Germiva el avance físico de las partidas de un proyecto y leer con él el valor ganado (CPI, SPI y estimado al terminar), el flujo de caja, la rentabilidad y el informe de estado del proyecto.",
  "Video 11 de la serie Proyectos. setup: seeds/proyectos/preparar.sh avance (presupuesto vigente 5,500,000; costo real 250,000 en Excavación; 450,000 comprometidos en Estructura; sin avance registrado).",
  "/projects/17/avance?seccion=avance", "button:has-text('Registrar avance')", "avance",
  ["Registrar el avance físico de una partida", "Leer el valor ganado: CPI, SPI y estimado al terminar",
   "Ver el flujo de caja y la rentabilidad del proyecto", "Descargar o enviar el informe de estado"],
  ["Juzgar el proyecto solo por lo gastado: sin avance no hay valor ganado",
   "Confundir CPI con SPI: uno mide el costo y el otro el plazo",
   "Bajar un avance sin motivo: el sistema lo pide"])
D = "mat-dialog-container "
S = "nav.subnav button:has-text('%s')"
pasos = [
 paso("01-avance", "Avance físico", "Registrar avance", "Proyectos › Cartera › PRJ › Avance",
  "Cuánto de cada partida está hecho",
  """Saber cuánto se ha gastado no basta: hay que saber cuánto se ha avanzado. Eso se registra en la pestaña Avance, en
  Avance físico. Recojo el menú. La tabla lista las partidas, todavía sin avance. Arriba de ella está el botón Registrar: lo pulso. La excavación va
  en sesenta por ciento. En su fila cambio la medición a porcentaje. Y en el acumulado anoto sesenta: siempre se escribe
  el total acumulado a la fecha de corte, no lo del período. Pulso Registrar avance, abajo, y el aviso lo confirma. La
  partida muestra su sesenta por ciento, con origen manual. El avance también puede venir de las cubicaciones o de las
  tareas, según la fuente que se configure.""",
  [res(S % "Avance físico", "en\n  Avance físico".replace("\n  ", " "), 2500),
   clic("button.panel-collapse", "Recojo el menú"),
   clic("button:has-text('Registrar avance')", "lo pulso"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   clic(D + "tr:has-text('01.01') button[aria-label='Porcentaje']", "cambio la medición"),
   esc(D + "tr:has-text('01.01') input", "60", "en el acumulado anoto"),
   clic(D + "button:has-text('Registrar avance')", "Pulso Registrar avance, abajo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("tr:has-text('01.01') td >> nth=2", "muestra su sesenta", 4000),
   res("button:has-text('Configuración')", "según la fuente", 4000, True)]),
 paso("02-valor-ganado", "Valor ganado", "Valor ganado", "Proyectos › Cartera › PRJ › Avance › Valor ganado",
  "Planificado, ganado y real",
  """Con el avance, paso a Valor ganado. Compara tres cifras. El valor planificado: lo que debía estar hecho a la fecha,
  según el cronograma. El valor ganado: lo que realmente se hizo, a precio de presupuesto: doscientos sesenta y cuatro mil
  pesos. Y el costo real: lo que costó hacerlo, doscientos cincuenta mil. De ahí salen dos indicadores. El CPI mide el
  costo: uno punto cero seis significa que cada peso gastado rindió un peso con seis centavos; por encima de uno, se gasta
  menos de lo previsto. El SPI mide el plazo: cero punto cuarenta y cinco dice que la obra va atrasada respecto al plan.
  Y el estimado al terminar proyecta el costo final si se mantiene este rendimiento: cinco millones doscientos ocho mil
  pesos, dentro del presupuesto.""",
  [clic(S % "Valor ganado", "paso a Valor ganado"),
   res(":text('Valor planificado') >> nth=0", "El valor planificado", 5000),
   res(":text('ejecutado') >> nth=0", "El valor ganado: lo que", 6000),
   res(":text('Costo real') >> nth=0", "Y el costo real", 4000),
   res(":text('Rendimiento del costo') >> nth=0", "El CPI mide", 10000),
   res(":text('Rendimiento del plazo') >> nth=0", "El SPI mide", 7000),
   res(":text('Estimado al terminar') >> nth=0", "el estimado al terminar", 8000)]),
 paso("03-flujo", "Flujo de caja y rentabilidad", "Flujo de caja", "Proyectos › Cartera › PRJ › Avance › Flujo de caja",
  "Cuándo entra y cuándo sale el dinero",
  """La siguiente sección es el Flujo de caja, que pone esas cifras en el calendario: lo real hasta la fecha de corte, y después lo proyectado. Las
  entradas son los cobros al cliente; las salidas, los pagos, los compromisos y lo que falta por gastar. El saldo más bajo
  avisa cuánto dinero habrá que poner, y en qué mes. Y Rentabilidad resume el negocio: el contrato y lo facturado; el
  costo real, lo comprometido y el estimado al terminar; y el margen presupuestado frente al margen proyectado al
  terminar, que hoy es veintiuno por ciento.""",
  [clic(S % "Flujo de caja", "es el Flujo de caja"),
   res(":text('Entradas') >> nth=0", "Las\n  entradas son".replace("\n  ", " "), 4000),
   res(":text('Saldo más bajo') >> nth=0", "El saldo más bajo", 5000),
   clic(S % "Rentabilidad", "Y Rentabilidad resume"),
   res(":text('Contrato vigente') >> nth=0", "el contrato y lo facturado", 3000),
   res(":text('Estimado al terminar') >> nth=0", "el estimado al terminar", 3000),
   res(":text('Proyectado al terminar') >> nth=0", "al margen proyectado", 5000)]),
 paso("04-estado", "El informe de estado", "Estado del proyecto", "Proyectos › Cartera › PRJ › Avance",
  "PDF, Excel o envío al gerente",
  """Todo esto se entrega con el botón Estado del proyecto: descarga el informe en PDF o en Excel, o lo envía ahora al
  gerente y a quienes se indiquen. En Configuración se programa para que salga solo, cada lunes o cada primero de mes, y
  se eligen el método del estimado y los umbrales de alerta del CPI y el SPI. Y en la Cartera, esos mismos indicadores
  aparecen como semáforos, para ver de un vistazo qué proyecto necesita atención.""",
  [clic("button:has-text('Estado del proyecto')", "Estado del proyecto"),
   res(".mat-mdc-menu-panel", "descarga el informe", 6000),
   {"presionar": {"tecla": "Escape"}, "al_decir": "En Configuración"},
   res("button:has-text('Configuración')", "se programa para que", 6000, True),
   res("a:has-text('Cartera') >> nth=0", "en la Cartera", 6000, True)]),
]
guardar("proyectos-11-avance-y-valor-ganado", g, pasos)
