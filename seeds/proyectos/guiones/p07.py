from comun import *
g = base_p("Proyectos · El contrato de venta y la factura del anticipo",
  "Cómo registrar en Germiva el contrato de venta de un proyecto: monto, régimen de ITBIS para obras, forma de facturar, anticipo con su amortización y fondo de reparo; y cómo facturar el anticipo.",
  "Video 07 de la serie Proyectos. setup: seeds/proyectos/preparar.sh facturacion (presupuesto aprobado por 6,600,000 de precio; servicio «Construcción de nave industrial» con base presunta de construcción).",
  "/projects/17/facturacion", "button:has-text('Registrar contrato de venta')", "facturacion",
  ["Registrar el contrato de venta del proyecto", "Elegir el régimen de ITBIS de una obra con materiales",
   "Pactar anticipo, amortización y fondo de reparo", "Facturar el anticipo"],
  ["Facturar una obra con materiales con ITBIS sobre el 100 %", "Olvidar la amortización: el anticipo nunca se descontaría",
   "Querer cambiar el régimen después de facturar: queda fijo con la primera factura"])
D = "mat-dialog-container "
pasos = [
 paso("01-contrato", "El contrato de venta", "Registrar contrato de venta", "Proyectos › Cartera › PRJ › Facturación",
  "Cliente, monto, régimen de ITBIS y comprobante",
  """El presupuesto dice cuánto cuesta la obra; el contrato de venta dice cómo se le cobra al cliente. Se registra en la
  pestaña Facturación del proyecto. Recojo el menú, y pulso Registrar contrato de venta. El cliente ya viene del proyecto.
  En Monto del contrato anoto seis millones seiscientos mil pesos, el precio del presupuesto, sin ITBIS. Los días de
  crédito quedan en treinta. Ahora el régimen de ITBIS. Esta es una obra con materiales: marco esa opción. Con ella, el
  ITBIS se calcula sobre el diez por ciento de cada factura, y el resto sale exento, como manda la norma para
  construcción. En Servicio de la factura escribo Construcción, para buscar el servicio con que se arma cada factura.
  Aparece en la lista, y lo elijo. En Tipo de comprobante abro la lista, y elijo la factura de crédito fiscal.""",
  [res("a.ws-tab:has-text('Facturación')", "pestaña Facturación", 2500),
   clic("button.panel-collapse", "Recojo el menú"),
   clic("button:has-text('Registrar contrato de venta')", "pulso Registrar contrato"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   esc(D + "input[formcontrolname='originalAmount']", "6600000", "En Monto del contrato anoto"),
   res(D + "mat-form-field:has(input[formcontrolname='paymentTermDays'])", "Los días de\n  crédito".replace("\n  ", " "), 2500),
   clic(D + "mat-radio-button:has-text('Obra con materiales')", "marco esa opción"),
   res(D + "h3:has-text('ITBIS y comprobante')", "sobre el diez por ciento", 6000),
   esc(D + "app-custom-select[formcontrolname='product'] input", "Construcción", "escribo Construcción"),
   clic("mat-option:has-text('Construcción de nave')", "y lo elijo"),
   clic(D + "mat-select[formcontrolname='ncfType']", "En Tipo de comprobante abro"),
   clic("mat-option:has-text('Crédito Fiscal')", "elijo la factura de crédito fiscal")]),
 paso("02-condiciones", "Cómo se factura", "Avance, anticipo y fondo de reparo", "Proyectos › Cartera › PRJ › Facturación",
  "Por avance · anticipo 20 % · fondo de reparo 5 %",
  """Sigue la forma de facturar. Hay tres: por avance, midiendo lo ejecutado en cada período; por hitos, con un plan de
  cobros; o por tiempo y materiales. Dejo Por avance. En Presupuesto que se cubica abro la lista, y elijo el presupuesto
  de la obra: sus partidas son las que se medirán. Bajo al anticipo. En Anticipo anoto veinte: el cliente adelanta el
  veinte por ciento del contrato. Y en Amortización por factura anoto veinte también: cada factura de avance descontará
  ese porcentaje, hasta devolver el anticipo completo. Por último, el fondo de reparo. Anoto cinco: el cliente retiene el
  cinco por ciento de cada factura como garantía, y lo paga al recibir la obra. Pulso Guardar, y el aviso lo
  confirma.""",
  [res(D + "mat-radio-button:has-text('Por avance')", "Hay tres", 7500),
   clic(D + "mat-select[formcontrolname='budget']", "En Presupuesto que se cubica abro"),
   clic("mat-option:has-text('Presupuesto de obra')", "elijo el presupuesto"),
   esc(D + "input[formcontrolname='advancePercentage']", "20", "En Anticipo anoto veinte"),
   esc(D + "input[formcontrolname='amortizationPercentage']", "20", "anoto veinte también"),
   esc(D + "input[formcontrolname='retentionPercentage']", "5", "Anoto cinco"),
   clic(D + "button:has-text('Guardar')", "Pulso Guardar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
 paso("03-anticipo", "Facturar el anticipo", "Factura del anticipo", "Proyectos › Cartera › PRJ › Facturación",
  "El anticipo se factura aparte, con su ITBIS",
  """Con el contrato guardado, la pestaña muestra el estado de facturación: contrato vigente, facturado, cobrado y por
  facturar. Más abajo está el Anticipo: un millón trescientos veinte mil pesos pactados, todavía sin facturar. Pulso
  Facturar anticipo. El sistema muestra la vista previa: la base, el ITBIS sobre el diez por ciento, y el total de la
  factura. Pulso Generar factura. El aviso dice que la factura quedó creada en borrador: se revisa y se emite en Ventas,
  como cualquier otra. Desde ahí, cada factura de avance irá amortizando este anticipo.""",
  [res("section.ps-panel >> nth=0", "el estado de facturación", 5000),
   res("#billing-advance-title", "Más abajo está el Anticipo", 4500),
   clic("button:has-text('Facturar anticipo')", "Pulso\n  Facturar anticipo".replace("\n  ", " ")),
   res("mat-dialog-container", "la vista previa", 7000),
   clic("mat-dialog-container button:has-text('Generar factura')", "Pulso Generar factura"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3500, "cursor": False},
   res("#billing-advance-title", "cada factura de avance", 4000)]),
]
guardar("proyectos-07-contrato-y-anticipo", g, pasos)
