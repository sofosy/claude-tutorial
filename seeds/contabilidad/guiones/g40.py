from comun import *
g = base("Contabilidad · El centro de costo en un asiento: por línea, repartido y obligatorio",
  "Cómo asignar en Germiva un centro de costo a cada línea de un asiento, repartir un gasto entre varios centros por porcentaje y hacer que una cuenta exija centro de costo.",
  "Video 40 de la serie Contabilidad. setup: preparar.sh centros-documentos (árbol de centros con Logística, sin movimientos).",
  "/accounting/registro/diario", "button:has-text('Crear Asiento')",
  "seeds/contabilidad/preparar.sh centros-documentos",
  ["Asignar un centro de costo a una línea del asiento", "Repartir un gasto entre varios centros por porcentaje",
   "Qué pasa con las líneas sin centro", "Hacer que una cuenta exija centro de costo"],
  ["Poner centro a la línea del banco o la caja: el centro va en ingresos y gastos", "Un reparto que no suma 100 %: no se puede aplicar",
   "Elegir un centro agrupador: no recibe movimientos"])
L = ".table-row >> nth=%d >> "
pasos = [
 paso("01-linea", "Centro por línea", "Centro de costo en la línea", "Contabilidad › Diario y Mayor › Nuevo asiento",
  "Cada línea de gasto lleva su centro",
  """Los centros de costo se asignan al registrar cada operación. En Diario y Mayor recojo el menú, y pulso Crear Asiento.
  Voy a registrar dos gastos de noviembre. Escribo la descripción del asiento. Con la descripción lista, bajo a las líneas y
  agrego la primera línea. En la cuenta busco Fletes, la cuenta de gastos de envío. Aparece en la lista; la elijo, y en el
  débito anoto veinte mil pesos. Al elegir una cuenta de gasto, el centro se llena solo con el predeterminado de la empresa,
  Administración. Pero este flete es de Logística: en Centro de Costo escribo Log, para buscarlo por su código o su nombre.
  Aparece en la lista, y elijo Logística. Así el gasto queda imputado a ese centro.""",
  [clic("button.panel-collapse", "recojo el menú"),
   clic("button:has-text('Crear Asiento')", "pulso Crear Asiento"),
   esc("textarea[formcontrolname='description']", "Gastos de noviembre", "Escribo la descripción"),
   clic("button.add-line-button", "agrego la primera línea"),
   esc(L % 0 + "input[placeholder='Buscar cuenta...']", "Fletes", "En la cuenta busco"),
   clic("mat-option:has-text('6.03.10')", "la elijo, y en el"),
   esc(L % 0 + "input[formcontrolname='debitAmount']", "20000", "anoto veinte mil pesos"),
   res(L % 0 + "input[placeholder='Centro de costo...']", "el centro se llena solo", 4500),
   esc(L % 0 + "input[placeholder='Centro de costo...']", "Log", "escribo Log"),
   clic("mat-option:has-text('CC-LOG')", "y elijo Logística"),
   res(L % 0 + ".line-number", "Así el gasto queda", 3500)]),
 paso("02-reparto", "Repartir entre centros", "Repartir entre centros", "Contabilidad › Diario y Mayor › Nuevo asiento",
  "Un gasto compartido se reparte por porcentaje",
  """El segundo gasto es el alquiler del local de ventas, que comparten las dos sucursales. Agrego la segunda línea, y en su
  cuenta busco Arrend, de arrendamientos. Aparece en la lista; la elijo, y en el débito anoto treinta mil pesos. Como el gasto
  es de dos centros, en lugar de elegir uno solo pulso el botón de repartir, al lado del centro. En el primer centro abro la
  lista, y elijo Ventas Santo Domingo. En su porcentaje anoto sesenta. A Santo Domingo le toca más porque ocupa más espacio.
  Pulso Agregar centro. En la fila nueva abro la lista, y elijo Ventas Santiago. Y en su porcentaje anoto el cuarenta
  restante. El reparto tiene que sumar cien por ciento, y el total lo confirma. Aplico. La línea dice Repartido en dos
  centros: al guardar se divide en una línea por centro.""",
  [res(L % 0 + "input[formcontrolname='debitAmount']", "El segundo gasto", 2500),
   clic("button.add-line-button", "Agrego la segunda línea"),
   esc(L % 1 + "input[placeholder='Buscar cuenta...']", "Arrend", "cuenta busco Arrend"),
   clic("mat-option:has-text('6.03.02')", "la elijo, y en el"),
   esc(L % 1 + "input[formcontrolname='debitAmount']", "30000", "anoto treinta mil pesos"),
   clic("button[aria-label='Repartir la línea 2 entre varios centros']", "pulso el botón de repartir"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   clic("mat-dialog-container mat-select[formcontrolname='costCenter'] >> nth=0", "En el primer centro abro"),
   clic("mat-option:has-text('CC-VEN-SD')", "elijo Ventas Santo Domingo"),
   esc("mat-dialog-container input[formcontrolname='percentage'] >> nth=0", "60", "anoto sesenta"),
   clic("mat-dialog-container button:has-text('Agregar centro')", "Pulso Agregar centro"),
   clic("mat-dialog-container mat-select[formcontrolname='costCenter'] >> nth=1", "En la fila nueva abro"),
   clic("mat-option:has-text('CC-VEN-STI')", "elijo Ventas Santiago"),
   esc("mat-dialog-container input[formcontrolname='percentage'] >> nth=1", "40", "anoto el cuarenta"),
   res("mat-dialog-container :text('Total:') >> nth=0", "el total lo confirma", 2000),
   clic("mat-dialog-container button:has-text('Aplicar')", "Aplico"),
   res(L % 1 + "button:has-text('Repartido en 2 centros')", "La línea dice Repartido", 5000)]),
 paso("03-guardar", "Guardar el asiento", "Líneas sin centro", "Contabilidad › Diario y Mayor › Nuevo asiento",
  "La caja y el banco no llevan centro",
  """Falta la contrapartida. Agrego la tercera línea, y en su cuenta busco la caja general, de donde salió el dinero.
  Aparece en la lista; la elijo, y en el crédito anoto los cincuenta mil pesos del total. Fíjate en que esta línea
  queda sin centro, y es lo correcto: la caja, los bancos y las cuentas por cobrar o por pagar son cuentas de balance, y el
  centro de costo solo aplica a ingresos y gastos. Guardo el asiento, y el aviso lo confirma.""",
  [clic("button.add-line-button", "Agrego la tercera línea"),
   esc(L % 2 + "input[placeholder='Buscar cuenta...']", "Caja gen", "busco la caja general"),
   clic("mat-option:has-text('1.01.01.01.02')", "la elijo, y en el"),
   esc(L % 2 + "input[formcontrolname='creditAmount']", "50000", "anoto los cincuenta mil"),
   res(L % 2 + "input[placeholder='Centro de costo...']", "queda sin centro", 7000),
   clic("button:has-text('Guardar')", "Guardo el asiento"),
   res(".mat-mdc-snack-bar-container", "el aviso lo confirma", 2500)]),
 paso("04-exige", "Cuentas que exigen centro", "Exige centro de costo", "Contabilidad › Configuración Contable › Plan de Cuentas",
  "Una cuenta puede exigir centro de costo",
  """Hay cuentas que nunca deberían quedar sin centro, como los fletes. Eso se configura en el Plan de Cuentas. En el
  buscador escribo Fletes, y el catálogo se filtra mientras escribo. Ahí está la cuenta; la abro con el ojo, Ver detalles.
  Abajo, entre las opciones de la cuenta, marco la casilla Exige centro de costo, y el aviso confirma que quedó
  guardada. Desde ahora, toda línea a esta cuenta, venga de una factura, de la nómina o de un asiento, debe quedar con un
  centro: el elegido, el de su proyecto o el predeterminado de la empresa. Si no queda ninguno, el sistema rechaza el
  documento y dice qué línea hay que corregir.""",
  [res("h4.page-title, :text('Plan de Cuentas') >> nth=0", "Eso se configura", 3000),
   esc("input[placeholder='Código, nombre o descripción']", "Fletes", "escribo Fletes"),
   clic(".tree-node-content:has(.node-code:text-is('6.03.10')) button[aria-label='Ver detalles']", "la abro con el ojo"),
   clic("mat-checkbox:has-text('Exige centro de costo') label", "marco la casilla"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3000, "cursor": False},
   res("p.field-note:has-text('Toda línea a esta cuenta')", "toda línea a esta cuenta", 9000),
   res("p.field-note:has-text('Toda línea a esta cuenta')", "Si no queda ninguno", 4500)],
  navegar="/accounting/configuracion/plan-cuentas"),
]
guardar("contabilidad-40-centro-en-asiento", g, pasos)
