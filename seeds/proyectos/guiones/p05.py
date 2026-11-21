from comun import *
g = base_p("Proyectos · Control del presupuesto: comprometido, real y disponible por partida",
  "Cómo sigue Germiva el presupuesto de un proyecto en ejecución: lo comprometido en órdenes, lo real contabilizado y lo disponible de cada partida, cómo se imputa un documento a una partida, qué pasa cuando se excede y cómo trasladar presupuesto entre partidas.",
  "Video 05 de la serie Proyectos. setup: seeds/proyectos/preparar.sh control (presupuesto aprobado; compra contabilizada de 250,000 en Excavación; orden de compra aprobada de acero por 450,000 en Estructura metálica).",
  "/projects/17/control", "table.control-table", "control",
  ["Leer vigente, comprometido, real y disponible por partida", "Imputar un documento a un proyecto y a una partida",
   "Qué pasa cuando un documento excede la partida", "Trasladar presupuesto entre partidas"],
  ["Registrar gastos del proyecto sin partida: no aparecen en su control",
   "Creer que una orden aprobada no cuenta: ya es compromiso", "Trasladar más de lo disponible en la partida de origen"],
  )
C = "table.control-table "
L = ".table-row >> nth=%d >> "
pasos = [
 paso("01-control", "La pestaña Control", "Presupuesto contra real", "Proyectos › Cartera › PRJ › Control",
  "Vigente − comprometido − real = disponible",
  """Con el presupuesto aprobado, el proyecto tiene una pestaña nueva: Control. Recojo el menú. Cada partida muestra cuatro cifras. Vigente es su presupuesto actual, con los indirectos incluidos.
  Comprometido, lo que ya está pedido en órdenes de compra aprobadas: aquí, cuatrocientos cincuenta mil pesos de acero
  para la estructura. Real, lo que ya llegó a la contabilidad: doscientos cincuenta mil de excavación. Y Disponible, lo
  que queda por gastar. Si pulso una partida, abajo salen sus compromisos abiertos y sus costos reales, con la factura
  y el asiento de cada uno. Y el interruptor Ver desglose agrega lo reservado por requisiciones y el material que está
  en el almacén de la obra.""",
  [res("a.ws-tab:has-text('Control')", "una pestaña nueva", 2500),
   clic("button.panel-collapse", "Recojo el menú"),
   res(C + "thead", "muestra cuatro cifras", 3000),
   res(C + "tr:has-text('02.01') td >> nth=2", "cuatrocientos cincuenta mil", 5000),
   res(C + "tr:has-text('01.01') td >> nth=3", "doscientos cincuenta mil de excavación", 3500),
   res(C + "tr:has-text('01.01') td >> nth=4", "Y Disponible", 3000),
   clic(C + "tr:has-text('01.01') button.line-link", "Si pulso una partida"),
   res(":text('Costos reales') >> nth=0", "sus costos reales", 5000),
   res(":text('Ver desglose') >> nth=0", "el interruptor Ver desglose", 6000, True)]),
 paso("02-imputar", "Imputar un documento", "Proyecto y partida en el documento", "Compras › Facturas › Editar compra",
  "El proyecto y la partida viajan con el documento",
  """¿Cómo llega un gasto a su partida? Cada documento lleva el proyecto y la partida: la requisición, la orden de compra,
  la factura, la salida de inventario y el asiento. Esta es una factura de compra en borrador, del subcontratista de la
  excavación. La abro con el lápiz. El formulario carga sus datos: el proveedor, el comprobante, las fechas y sus líneas. En la cabecera está el Proyecto, la nave de Haina. Y en la línea, la columna Partida
  dice a cuál de sus partidas va el gasto: Excavación y relleno. Debajo de las líneas aparece el aviso del control. La
  partida tiene ciento noventa mil pesos disponibles, y esta factura pide doscientos mil: se excede en diez mil.
  Lo que pasa después depende de la política del presupuesto. Con Avisar, que es la de este proyecto, se puede
  continuar y el excedente queda registrado. Pedir aprobación exige que otra persona apruebe el sobregiro. Y Bloquear
  no deja guardar el documento. La política se elige en el presupuesto del proyecto, y se puede cambiar con la obra en
  marcha.""",
  [res("tr.mat-mdc-row:has-text('Borrador') td >> nth=2", "Esta es una factura de compra", 4500),
   clic("tr.mat-mdc-row:has-text('Borrador') button[aria-label='Editar']", "La abro con el lápiz"),
   res("app-project-picker", "En la cabecera está el Proyecto", 3500),
   res("[data-col='partida'] >> nth=1", "la columna Partida", 6000),
   res("app-project-budget-control-notice", "aparece el aviso del control", 12000),
   res("app-project-budget-control-notice", "Con Avisar", 6000),
   res("button:has-text('Guardar y emitir')", "Pedir aprobación exige", 4500),
   res("app-project-picker", "La política se elige", 5000)],
  navegar="/purchases/invoices/list"),
 paso("03-traslado", "Trasladar entre partidas", "Trasladar entre partidas", "Proyectos › Cartera › PRJ › Control",
  "Mover presupuesto sin cambiar el total del proyecto",
  """Cuando a una partida le falta y a otra le sobra, se hace un traslado. Vuelvo a la pestaña Control del proyecto, y
  pulso Trasladar entre partidas. En Sale de abro la lista, y elijo Piso industrial, que todavía no ha gastado. En
  Entra a abro la otra lista, y elijo Excavación y relleno. En Monto anoto cincuenta mil pesos, lo que le falta a la excavación con algo de holgura. Y en Motivo escribo por
  qué: Mayor volumen de excavación. El motivo es obligatorio, porque queda en el historial. Pulso Guardar, y el aviso confirma la solicitud. El traslado no se aplica de inmediato:
  queda Por aprobar en la vista Traslados, hasta que otra persona lo apruebe. El total del proyecto no cambia; solo se
  mueve entre partidas.""",
  [clic("button:has-text('Trasladar entre partidas')", "pulso Trasladar entre partidas"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   clic("mat-dialog-container mat-select[formcontrolname='fromLineKey']", "En Sale de abro"),
   clic("mat-option:has-text('03.01')", "elijo Piso industrial"),
   clic("mat-dialog-container mat-select[formcontrolname='toLineKey']", "abro la otra lista"),
   clic("mat-option:has-text('01.01')", "elijo Excavación y relleno"),
   esc("mat-dialog-container input[formcontrolname='amount']", "50000", "En Monto anoto"),
   esc("mat-dialog-container textarea[formcontrolname='reason']", "Mayor volumen de excavación", "en Motivo escribo"),
   clic("mat-dialog-container button:has-text('Guardar')", "Pulso Guardar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   clic("div.view-switch button:has-text('Traslados')", "en la vista Traslados"),
   res("tr:has-text('Por aprobar') >> nth=0 >> td >> nth=-2", "hasta que otra persona", 5000)],
  navegar="/projects/17/control"),
]
guardar("proyectos-05-control", g, pasos)
