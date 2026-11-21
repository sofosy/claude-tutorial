from comun import *
g = base("Contabilidad · El centro de costo en compras, nómina, activos y almacenes",
  "Cómo asignar en Germiva un centro de costo a cada línea de una factura de compra, repartir una línea entre centros, y dónde se define el centro que usan la nómina, los activos fijos y los almacenes.",
  "Video 41 de la serie Contabilidad. setup: preparar.sh centros-compras (árbol de centros y compra B01 en borrador de Servicios Germiva del Cibao con dos servicios).",
  "/purchases/invoices/list", "tr.mat-mdc-row:has-text('Cibao')",
  "seeds/contabilidad/preparar.sh centros-compras",
  ["Asignar un centro de costo a cada línea de una compra", "Repartir una línea de compra entre centros",
   "De dónde sale el centro de la nómina", "El centro de un activo fijo y de un almacén"],
  ["Esperar centro en el ITBIS o en la cuenta por pagar: solo el gasto lo lleva",
   "Dejar al departamento sin centro: su nómina cae en el predeterminado",
   "Repartir con porcentajes que no suman 100 %"])
D = "mat-dialog-container "
pasos = [
 paso("01-linea", "Centro por línea de compra", "Centro de costo de la línea", "Compras › Facturas › Editar compra",
  "Cada línea de la compra lleva su centro",
  """En las compras, el centro de costo va en cada línea de la factura. Recojo el menú. Este borrador es de un proveedor de
  servicios, con dos gastos distintos. Lo abro con el lápiz de su fila. La primera línea es el mantenimiento de los
  montacargas, un gasto de Operaciones. Despliego la línea con la flecha de la derecha. Entre sus datos está Centro de
  costo: abro la lista, y elijo Operaciones. Si lo dejara vacío, el gasto iría al centro predeterminado de la empresa.""",
  [clic("button.panel-collapse", "Recojo el menú"),
   res("tr.mat-mdc-row:has-text('Cibao') td >> nth=2", "Este borrador es de un proveedor", 4000),
   clic("tr.mat-mdc-row:has-text('Cibao') button[aria-label='Editar']", "con el lápiz de su fila"),
   clic("button:has(mat-icon:text-is('expand_more')) >> nth=0", "Despliego la línea"),
   clic("app-line-cost-center-select mat-select >> nth=0", "abro la lista"),
   clic("mat-option:has-text('CC-OPS')", "elijo Operaciones"),
   res("span.line-cost-center-hint >> nth=0", "Si lo dejara vacío", 4500)]),
 paso("02-reparto", "Repartir una línea", "Repartir entre centros", "Compras › Facturas › Editar compra",
  "Una línea de compra repartida por porcentaje",
  """La segunda línea es la publicidad en radio, que sirve a las dos sucursales de ventas. La despliego también, y esta vez
  pulso Repartir entre centros. En el primer centro abro la lista, y elijo Ventas Santo Domingo. En su porcentaje anoto
  cincuenta. La campaña es la misma para las dos sucursales, así que va a partes iguales. Pulso Agregar centro. En la fila
  nueva abro la lista, y elijo Ventas Santiago. En su porcentaje anoto el otro cincuenta. Con el total en cien por
  ciento, aplico. En la tabla, cada línea muestra ya su centro o su reparto. Guardo el borrador, y espero un momento mientras el sistema registra la factura. El sistema confirma
  que la compra quedó actualizada, y acepto. Cuando la factura se emita, cada gasto irá a su centro; el ITBIS y la cuenta
  por pagar al proveedor van sin centro.""",
  [clic("button:has(mat-icon:text-is('expand_more')) >> nth=0", "La despliego también"),
   clic("button:has-text('Repartir entre centros') >> nth=-1", "pulso Repartir entre centros"),
   {"resaltar": "mat-dialog-container", "durante_ms": 1500, "cursor": False},
   clic(D + "mat-select[formcontrolname='costCenter'] >> nth=0", "En el primer centro abro"),
   clic("mat-option:has-text('CC-VEN-SD')", "elijo Ventas Santo Domingo"),
   esc(D + "input[formcontrolname='percentage'] >> nth=0", "50", "anoto cincuenta"),
   clic(D + "button:has-text('Agregar centro')", "Pulso Agregar centro"),
   clic(D + "mat-select[formcontrolname='costCenter'] >> nth=1", "En la fila nueva abro"),
   clic("mat-option:has-text('CC-VEN-STI')", "elijo Ventas Santiago"),
   esc(D + "input[formcontrolname='percentage'] >> nth=1", "50", "anoto el otro cincuenta"),
   clic(D + "button:has-text('Aplicar')", "aplico"),
   res("span.line-cost-center-hint >> nth=1", "cada línea muestra ya", 3500),
   clic("button:has-text('Guardar borrador')", "Guardo el borrador"),
   res("mat-dialog-container:has-text('Operación completada')", "El sistema confirma", 2500),
   clic("mat-dialog-container button:has-text('Aceptar')", "y acepto"),
   res("span.line-cost-center-hint >> nth=0", "cada gasto irá a su centro", 3500),
   res(":text('Impuestos') >> nth=0", "el ITBIS y la cuenta por pagar", 4000)]),
 paso("03-nomina", "Nómina", "El centro del departamento", "Recursos Humanos › Configuración › Departamentos",
  "La nómina usa el centro del departamento",
  """El gasto de nómina no se digita línea a línea: toma el centro del departamento de cada empleado. En la configuración de
  Recursos Humanos, en Departamentos, abro Logística, uno de los departamentos que vienen con el sistema, con un clic en su
  fila. Estos departamentos no se editan, pero sí aceptan un centro de costo propio de tu empresa. En Centro de costo
  escribo Log, y espero a que el sistema busque entre los centros activos de la empresa. Aparece Logística, y lo elijo.
  Pulso Guardar centro de costo, y el aviso lo confirma. Desde ahora el sueldo, los aportes y las provisiones de su gente
  se imputan a ese centro. Y si un empleado debe ir a otro centro, se le pone uno propio en su ficha.""",
  [res("mat-dialog-container >> nth=0", "En la configuración", 2500),
   res("tr.mat-mdc-row:has-text('Logística') td >> nth=1", "en Departamentos", 1800),
   clic("tr.mat-mdc-row:has-text('Logística') td >> nth=0", "con un clic en su"),
   res("mat-dialog-container >> nth=-1 >> p.gm-dialog-note >> nth=0", "Estos departamentos no se editan", 5000),
   esc("mat-dialog-container >> nth=-1 >> app-autocomplete >> nth=-1 >> input", "Log", "escribo Log"),
   clic("mat-option:has-text('CC-LOG')", "y lo elijo"),
   clic("mat-dialog-container >> nth=-1 >> button:has-text('Guardar centro de costo')", "Pulso Guardar centro de costo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("tr.mat-mdc-row:has-text('Logística') td >> nth=2", "Desde ahora el sueldo", 4500),
   res("tr.mat-mdc-row:has-text('Despacho') td >> nth=0", "Y si un empleado", 3500)],
  navegar="/employee/inicio?config=departamentos"),
 paso("04-almacen", "Almacenes y activos fijos", "Centro por omisión del almacén", "Inventario › Almacenes › Almacén Sur",
  "El almacén tiene su centro por omisión",
  """Lo mismo pasa en Inventario. En la ficha de cada almacén está el Centro de costo por omisión: lo usan sus ajustes,
  sus salidas y sus consumos cuando el movimiento no trae otro centro.""",
  [res("app-cost-center-field", "Centro de costo por omisión", 8000)],
  navegar="/inventory/warehouse/1"),
 paso("05-activo", "Almacenes y activos fijos", "Centro del activo fijo", "Contabilidad › Activos Fijos › Nuevo",
  "La depreciación va al centro del activo",
  """Y en Activos Fijos, al registrar un activo, el campo Centro de Costo decide a dónde van su depreciación de cada mes,
  su baja y su venta. Así, cada gasto llega a su centro sin tener que acordarse de digitarlo.""",
  [res("mat-form-field:has(mat-select[formcontrolname='costCenter'])", "el campo Centro de Costo", 8000)],
  navegar="/accounting/fixed-assets/create"),
]
guardar("contabilidad-41-centro-en-compras", g, pasos)
