from comun import *
g = base_p("Proyectos · Cerrar el proyecto: compromisos abiertos, finiquito y cierre del presupuesto",
  "Cómo cerrar un proyecto en Germiva: pasarlo a Completado resolviendo los compromisos abiertos, cerrar el contrato de venta con su finiquito y cerrar el presupuesto para que no reciba más costos.",
  "Video 13 de la serie Proyectos. setup: seeds/proyectos/preparar.sh cierre (obra en ejecución con una orden de acero de 450,000 sin facturar y el contrato de venta registrado). Entre el paso 1 y el 2, preparar.py resolver-compromiso anula esa orden por el API.",
  "/projects/17", "mat-select[formcontrolname='status']", "cierre",
  ["Pasar el proyecto a Completado", "Qué son los compromisos abiertos y cómo resolverlos",
   "Cerrar el contrato de venta con su finiquito", "Cerrar el presupuesto del proyecto"],
  ["Forzar el cierre con órdenes de compra todavía abiertas",
   "Dejar el presupuesto abierto: la obra sigue recibiendo costos",
   "Cerrar el contrato antes de facturar la última cubicación"])
D = "mat-dialog-container "
EST = "mat-select[formcontrolname='status']"
pasos = [
 paso("01-compromisos", "Completar el proyecto", "Completar el proyecto", "Proyectos › Cartera › PRJ › Resumen",
  "El sistema revisa lo que sigue abierto",
  """Una obra no termina con la última factura: hay que cerrarla en el sistema, para que nadie le siga cargando costos. El
  cierre tiene tres partes: el proyecto, el contrato y el presupuesto. Empiezo en el Resumen. Abro el campo Estado, y elijo
  Completado. Abajo, pulso Actualizar. El sistema se detiene: el proyecto tiene compromisos abiertos. Hay cuatrocientos
  cincuenta mil pesos en órdenes de compra sin facturar. Podría continuar de todos modos, pero lo abierto quedaría sin
  resolver. Pulso Cancelar. Lo correcto es resolver cada compromiso: recibir y facturar la orden, o anularla si ya no
  va.""",
  [res("header.ws-header h1", "El\n  cierre tiene tres partes".replace("\n  ", " "), 3500),
   clic(EST, "Abro el campo Estado"),
   clic("mat-option:has-text('Completado')", "y elijo\n  Completado".replace("\n  ", " ")),
   clic("button:has-text('Actualizar')", "pulso Actualizar"),
   res("mat-dialog-container", "El sistema se detiene", 4000),
   res(D + "app-project-closure-blockers", "Hay cuatrocientos", 5000),
   res(D + "button:has-text('Continuar de todos modos')", "Podría continuar", 4500),
   clic(D + "button:has-text('Cancelar')", "Pulso Cancelar"),
   res("a.ws-tab:has-text('Control')", "Lo correcto es resolver", 5000)]),
 paso("02-completado", "Completar el proyecto", "Sin compromisos abiertos", "Proyectos › Cartera › PRJ › Resumen",
  "Con todo resuelto, el proyecto se completa",
  """La orden de acero ya no iba, y se anuló en Compras. Ahora sí. De nuevo en el Resumen, abro el campo Estado, y elijo
  Completado. Pulso Actualizar. Esta vez el sistema lo acepta, y confirma que el proyecto se guardó. Pulso Aceptar. La
  cabecera ya muestra el proyecto como Completado.""",
  [clic(EST, "abro el campo Estado"),
   clic("mat-option:has-text('Completado')", "y elijo\n  Completado".replace("\n  ", " ")),
   clic("button:has-text('Actualizar')", "Pulso Actualizar"),
   res("mat-dialog-container", "Esta vez el sistema", 3500),
   clic(D + "button:has-text('Aceptar')", "Pulso Aceptar"),
   res("header.ws-header h1", "La\n  cabecera ya muestra".replace("\n  ", " "), 3500)],
  navegar="/projects/17", setup={"tipo": "shell", "cmd": "python3 seeds/proyectos/preparar.py resolver-compromiso"}),
 paso("03-contrato", "Cerrar el contrato", "Finiquito del contrato", "Proyectos › Cartera › PRJ › Facturación",
  "Después del cierre no se factura nada más",
  """Segundo, el contrato de venta. En la pestaña Facturación, recojo el menú, y bajo a Cierre del contrato. El botón
  Finiquito genera el documento que liquida el contrato: lo facturado, el anticipo y el fondo de reparo. Pulso Cerrar
  contrato. En las notas escribo Obra recibida conforme. Con la nota ya escrita, confirmo con el botón Cerrar contrato.
  Desde ahora no se factura nada más de este contrato; solo el fondo de reparo se sigue liberando. Y si se cerró por
  error, el botón Reabrir lo devuelve.""",
  [clic("button.panel-collapse", "recojo el menú"),
   res("#billing-closing-title", "bajo a Cierre del contrato", 2500),
   res("button:has-text('Finiquito')", "El botón\n  Finiquito".replace("\n  ", " "), 6000, True),
   clic("section.ps-panel:has(#billing-closing-title) button:has-text('Cerrar contrato')", "Pulso Cerrar\n  contrato".replace("\n  ", " ")),
   esc(D + "textarea[formcontrolname='notes']", "Obra recibida conforme", "En las notas escribo"),
   clic(D + "button:has-text('Cerrar contrato')", "confirmo con el botón"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("section.ps-panel:has(#billing-closing-title) p >> nth=0", "Desde ahora no se factura", 5000),
   res("button:has-text('Reabrir')", "el botón Reabrir", 3500, True)],
  navegar="/projects/17/facturacion"),
 paso("04-presupuesto", "Cerrar el presupuesto", "Cerrar el presupuesto", "Proyectos › Cartera › PRJ › Presupuesto",
  "Solo lectura: la obra ya no recibe costos",
  """Y tercero, el presupuesto del proyecto, que es donde se cargan todos los costos de la obra. Arriba, pulso Cerrar presupuesto. El sistema recuerda la regla: solo se cierra con el
  proyecto completado y sin compromisos abiertos. En el motivo escribo Obra terminada y entregada. Con el motivo ya
  anotado, pulso el botón Cerrar presupuesto. El presupuesto queda cerrado, en solo lectura, y deja de aceptar
  imputaciones: ninguna compra, hora ni gasto se puede cargar ya a esta obra. Así el costo final queda fijo, listo para
  compararlo con lo presupuestado. Proyecto, contrato y presupuesto: con los tres cerrados, la obra está terminada también
  en los libros.""",
  [res("header.ws-header h1", "que es donde se cargan", 3000),
   clic("button:has-text('Cerrar presupuesto')", "pulso Cerrar presupuesto"),
   res("mat-dialog-container", "El sistema recuerda la regla", 5000),
   esc(D + "textarea", "Obra terminada y entregada", "En el motivo escribo"),
   clic(D + "button:has-text('Cerrar presupuesto')", "pulso el botón Cerrar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res(":text('Este presupuesto está cerrado') >> nth=0", "El presupuesto queda cerrado", 6000),
   res("a.ws-tab:has-text('Control')", "Así el costo final", 5000),
   res(":text('Este presupuesto está cerrado') >> nth=0", "Proyecto, contrato y presupuesto", 5000)],
  navegar="/projects/17/presupuesto/2"),
]
guardar("proyectos-13-cerrar-el-proyecto", g, pasos)
