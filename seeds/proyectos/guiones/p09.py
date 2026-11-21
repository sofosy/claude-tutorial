from comun import *
g = base_p("Proyectos · Subcontratos y retención de garantía",
  "Cómo registrar en Germiva el subcontrato de un proyecto, imputarle las facturas del subcontratista, retenerle un porcentaje de garantía en cada una y liberar esa retención cuando el trabajo se recibe conforme.",
  "Video 09 de la serie Proyectos. setup: seeds/proyectos/preparar.sh subcontrato (presupuesto aprobado; proveedor Movimientos de Tierra Germiva y su factura B0100000321 de 200,000 en borrador para la partida Excavación).",
  "/projects/17/subcontratos", "button:has-text('Registrar subcontrato')", "subcontrato",
  ["Registrar un subcontrato con su retención de garantía", "Imputar la factura del subcontratista al subcontrato",
   "Ver lo facturado, lo retenido y lo que falta por facturar", "Liberar la retención de garantía"],
  ["Pagarle al subcontratista el total de la factura: la garantía queda retenida",
   "Registrar la factura sin elegir el subcontrato: no retiene nada",
   "Querer liberar la retención de una factura sin emitir"])
D = "mat-dialog-container "
pasos = [
 paso("01-registrar", "Registrar el subcontrato", "Registrar subcontrato", "Proyectos › Cartera › PRJ › Subcontratos",
  "Proveedor · alcance · monto · retención de garantía",
  """Parte de la obra la hacen subcontratistas, y a cada uno se le suele retener una garantía hasta recibir su trabajo.
  Eso se lleva en la pestaña Subcontratos del proyecto. Recojo el menú, y pulso Registrar subcontrato. En Proveedor escribo
  Movimientos, para buscar al subcontratista de la excavación. Aparece en la lista, y lo elijo. En Alcance del
  subcontrato escribo qué va a hacer: Excavación y relleno. Con el alcance escrito, en Monto pactado anoto cuatrocientos mil
  pesos, sin ITBIS. La Retención de garantía viene en cinco por ciento: de cada factura suya se retendrá ese porcentaje.
  Pulso Guardar, y el aviso lo confirma. El subcontrato recibe su número, y su ficha se abre abajo.""",
  [res("a.ws-tab:has-text('Subcontratos')", "en la pestaña Subcontratos", 2500),
   clic("button.panel-collapse", "Recojo el menú"),
   clic("button:has-text('Registrar subcontrato')", "pulso Registrar subcontrato"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   esc(D + "app-custom-select[formcontrolname='supplier'] input", "Movimientos", "escribo\n  Movimientos".replace("\n  ", " ")),
   clic("mat-option:has-text('Movimientos de Tierra')", "y lo elijo"),
   esc(D + "input[formcontrolname='description']", "Excavación y relleno", "escribo qué va a hacer"),
   esc(D + "input[formcontrolname='originalAmount']", "400000", "en Monto pactado anoto"),
   res(D + "mat-form-field:has(input[formcontrolname='retentionPercentage'])", "La Retención de garantía", 6000),
   clic(D + "button:has-text('Guardar')", "Pulso Guardar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("table[aria-label='Subcontratos del proyecto'] tbody tr >> nth=0 >> td >> nth=0", "recibe su número", 4000)]),
 paso("02-factura", "La factura del subcontratista", "Subcontrato en la factura de compra", "Compras › Facturas › Editar compra",
  "La factura se imputa al subcontrato y retiene la garantía",
  """Ahora su primera factura, que ya está en Compras, en borrador. La abro con el lápiz. El formulario carga sus datos: el
  proveedor, el proyecto y la partida. Como el proveedor tiene un subcontrato vigente en este proyecto, aparece el campo
  Subcontrato. Abro la lista, y elijo el que acabo de registrar. Debajo, el sistema estima la retención de garantía: el
  cinco por ciento de los doscientos mil pesos de la factura, diez mil pesos. Pulso Guardar y emitir. El sistema pide
  confirmar la emisión, y confirmo. La factura queda emitida: la cuenta por pagar se parte en dos, lo que se le paga
  ahora, y la retención de garantía, que no se propone para pago hasta liberarla.""",
  [res("tr.mat-mdc-row:has-text('Borrador') td >> nth=2", "ya está en Compras", 3500),
   clic("tr.mat-mdc-row:has-text('Borrador') button[aria-label='Editar']", "La abro con el lápiz"),
   res("app-project-picker", "el proyecto y la partida", 3500),
   res("app-invoice-subcontract-field", "aparece el campo", 3000),
   clic("app-invoice-subcontract-field mat-select", "Abro la lista"),
   clic("mat-option:has-text('Excavación')", "elijo el que acabo"),
   res("app-invoice-subcontract-field mat-hint, app-invoice-subcontract-field .mat-mdc-form-field-hint", "estima la retención", 6500),
   clic("button:has-text('Guardar y emitir')", "Pulso Guardar y emitir"),
   res("mat-dialog-container", "El sistema pide", 2000),
   clic("mat-dialog-container button.confirm-button", "y confirmo"),
   res("mat-dialog-container, .mat-mdc-snack-bar-container", "se parte en dos", 3500),
   {"click_opcional": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "hasta liberarla"}],
  navegar="/purchases/invoices/list"),
 paso("03-liberar", "Liberar la retención", "Liberar retención de garantía", "Proyectos › Cartera › PRJ › Subcontratos",
  "Facturado, retenido y por liberar",
  """De vuelta en la pestaña Subcontratos del proyecto, la fila ya muestra lo facturado, lo que falta por facturar del
  subcontrato, y lo retenido por liberar: diez mil pesos. En su ficha, cada factura aparece con su neto, lo retenido y lo
  liberado. Cuando el trabajo se recibe conforme, se libera la garantía. Pulso Liberar retención. El diálogo propone la
  factura y el monto retenido; se puede liberar todo o una parte. Lo dejo completo, y pulso Liberar. El aviso lo confirma.
  El sistema registra el asiento que pasa la garantía a la cuenta por pagar corriente, y desde ese momento ya se propone
  para pago. Si fue un error, la liberación se puede reversar desde su lista.""",
  [res("table[aria-label='Subcontratos del proyecto'] tbody tr >> nth=0 >> td >> nth=4", "lo facturado", 3000),
   res("table[aria-label='Subcontratos del proyecto'] tbody tr >> nth=0 >> td >> nth=7", "lo retenido por liberar", 4000),
   res("#subcontract-detail-title", "En su ficha", 5000),
   clic("button:has-text('Liberar retención')", "Pulso Liberar retención"),
   res("mat-dialog-container", "El diálogo propone", 5500),
   clic("mat-dialog-container button:has-text('Liberar')", "completo, y pulso"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res(":text('Liberaciones') >> nth=0", "registra el asiento", 6000),
   res("button:has-text('Reversar')", "se puede reversar", 4000, True)],
  navegar="/projects/17/subcontratos"),
]
guardar("proyectos-09-subcontratos", g, pasos)
