from comun import *
g = base_p("Proyectos · Facturar por tiempo y materiales: horas aprobadas y gastos refacturables",
  "Cómo facturar un proyecto por tiempo y materiales en Germiva: las horas aprobadas a su tarifa de venta, los gastos del proyecto que marcas refacturables con su recargo, y la factura del período en un clic.",
  "Video 17 de la serie Proyectos. setup: seeds/proyectos/preparar.sh tiempo-materiales (contrato por tiempo y materiales: 900 la hora y 10 % de recargo; 40 h de Juan aprobadas y un alquiler de andamios de 30,000 cargado al proyecto).",
  "/projects/17/facturacion", "#billing-tm-title", "tiempo-materiales",
  ["Cuándo conviene facturar por tiempo y materiales", "Cómo se valoran las horas aprobadas",
   "Marcar un gasto como refacturable, con su recargo", "Generar la factura del período"],
  ["Facturar horas que nadie aprobó: solo entran las aprobadas",
   "Olvidar marcar los gastos refacturables: no se cobran solos",
   "Dejar un puesto sin tarifa de venta: sus horas no se pueden facturar"])
TM = "section.ps-panel:has(#billing-tm-title) "
GASTOS = TM + "table[aria-label='Gastos del proyecto'] "
HORAS = TM + "table[aria-label='Horas por facturar'] "
pasos = [
 paso("01-propuesta", "Tiempo y materiales", "La propuesta del período", "Proyectos › Cartera › PRJ › Facturación",
  "Horas aprobadas × tarifa de venta + gastos refacturables",
  """Hay trabajos que no se cobran por un precio cerrado, sino por lo que se trabajó: horas y gastos. Eso es facturar por
  tiempo y materiales, y se elige en el contrato de venta del proyecto. En la pestaña Facturación, recojo el menú, y bajo
  al panel Tiempo y materiales. El sistema arma solo la propuesta del período. Primero las horas: solo las aprobadas, cada
  día con su empleado y su partida. Juan trabajó cuarenta horas, y cada una se cobra a novecientos pesos, la tarifa de
  venta del contrato. Son treinta y seis mil pesos. Esa tarifa es de venta: no es lo que cuesta Juan, sino lo que se le
  cobra al cliente.""",
  [res("#billing-contract-title", "y se elige en el contrato", 3500),
   clic("button.panel-collapse", "recojo el menú"),
   res("#billing-tm-title", "al panel Tiempo y materiales", 3000),
   res(HORAS + "thead", "Primero las horas", 3500),
   res(HORAS + "tbody tr >> nth=0 >> td >> nth=1", "con su empleado y su partida", 3500),
   res(HORAS + "tbody tr >> nth=0 >> td >> nth=3", "a novecientos pesos", 4000),
   res(TM + "h3 >> nth=0", "Son treinta y seis mil", 3500),
   res(HORAS + "tbody tr >> nth=1 >> td >> nth=3", "Esa tarifa es de venta", 5000)]),
 paso("02-facturar", "Gastos y factura", "Gastos refacturables", "Proyectos › Cartera › PRJ › Facturación",
  "El gasto se cobra con su recargo",
  """Debajo están los gastos del proyecto: las compras que se le cargaron en el período. Aquí hay un alquiler de andamios
  de treinta mil pesos. Ningún gasto se cobra solo: hay que decidirlo. Marco su casilla Refacturable, y el aviso lo
  confirma. El sistema le suma el recargo del contrato, el diez por ciento, y quedan treinta y tres mil pesos a facturar.
  Arriba, el botón ya muestra el total del período: sesenta y nueve mil pesos. Lo pulso. El sistema crea la factura en
  borrador en Ventas, con una línea para la mano de obra y otra para los gastos, y el aviso trae su número. Allí se revisa
  y se emite con su comprobante. La propuesta queda vacía: lo facturado se marca, y no se vuelve a proponer. El próximo
  período se repite igual, con las horas y los gastos nuevos.""",
  [res("section.ps-panel:has(#billing-tm-title) h3 >> nth=1", "Debajo están los gastos", 3500),
   res(GASTOS + "tbody tr >> nth=0 >> td >> nth=1", "un alquiler de andamios", 4000),
   clic(GASTOS + "mat-checkbox input >> nth=0", "Marco su casilla"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res(GASTOS + "tbody tr >> nth=0 >> td >> nth=4", "y quedan treinta y tres mil", 4000),
   res(TM + "button:has-text('Facturar')", "el botón ya muestra", 3500, True),
   clic(TM + "button:has-text('Facturar')", "Lo pulso"),
   res("#billing-tm-title", "El sistema crea la factura", 4500),
   res(".mat-mdc-snack-bar-container", "y el aviso trae su número", 3000),
   res(HORAS + "tbody tr >> nth=0 >> td >> nth=0", "La propuesta queda vacía", 4000),
   res("#billing-documents-title", "El próximo\n  período".replace("\n  ", " "), 4000)]),
]
guardar("proyectos-17-tiempo-y-materiales", g, pasos)
