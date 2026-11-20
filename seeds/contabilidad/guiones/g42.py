from comun import *
g = base("Contabilidad · Distribución de costos indirectos entre centros",
  "Cómo repartir en Germiva los gastos indirectos de un centro, como el alquiler y los servicios de la oficina, entre los centros que los consumen: crear la regla, ver la vista previa, contabilizar la distribución y anularla desde el historial.",
  "Video 42 de la serie Contabilidad. setup: preparar.sh distribucion (árbol de centros; noviembre con 60,000 de alquiler y 24,000 de servicios en Administración).",
  "/accounting/distribucion-costos/reglas", "button:has-text('Crear Regla')",
  "seeds/contabilidad/preparar.sh distribucion",
  ["Crear una regla de distribución con emisores, cuentas y receptores", "Revisar la vista previa antes de contabilizar",
   "Contabilizar la distribución de un período", "Anular una distribución desde el historial"],
  ["Receptores que no suman 100 %: la regla no se guarda", "Usar el mismo centro como emisor y receptor",
   "Distribuir un período cerrado: solo se ejecuta en períodos abiertos"])
R = "div[formarrayname='receivers'] "
pasos = [
 paso("01-regla", "La regla de distribución", "Reglas de Distribución", "Contabilidad › Distribución de Costos › Reglas",
  "Qué se reparte, de qué centro y entre cuáles",
  """Hay gastos que paga un centro pero consumen varios: el alquiler y la luz de la oficina, por ejemplo, se cargan a
  Administración, aunque los usan Ventas y Operaciones. La Distribución de Costos los reparte con una regla. Recojo el menú,
  y pulso Crear Regla. Escribo el código, DIST-ADM, que identifica la regla y no se repite en la empresa. Después va el nombre, que dice
  qué reparte: Gastos de administración. Con el código y el nombre escritos, bajo a Qué se distribuye. En Centros emisores
  abro la lista, marco Administración, que es el centro que tiene el gasto, y con la tecla Escape cierro la lista.
  El porcentaje a distribuir queda en cien: se reparte todo el saldo.""",
  [res("app-console-tabs, [role=tablist] >> nth=0", "La Distribución de Costos", 3500),
   clic("button.panel-collapse", "Recojo el menú"),
   clic("button:has-text('Crear Regla')", "pulso Crear Regla"),
   esc("input[formcontrolname='code']", "DIST-ADM", "Escribo el código"),
   esc("input[formcontrolname='name']", "Gastos de administración", "Después va el nombre"),
   clic("mat-select[formcontrolname='senders']", "abro la lista"),
   clic("mat-option:has-text('CC-ADM')", "marco Administración"),
   {"presionar": {"tecla": "Escape"}, "al_decir": "cierro la lista"},
   res("mat-form-field:has(input[formcontrolname='allocationPercentage'])", "El porcentaje a distribuir", 4000)]),
 paso("02-cuentas-receptores", "Cuentas y receptores", "Cuentas y centros receptores", "Contabilidad › Distribución de Costos › Nueva regla",
  "Rango de cuentas · base de reparto · receptores",
  """Ahora, qué cuentas se reparten. En Desde la cuenta escribo el código de arrendamientos, seis punto cero tres punto cero
  dos. Y en Hasta la cuenta, el de servicios públicos, que termina en cero tres. Así la regla toma solo esas dos cuentas.
  En Cómo se reparte dejo la base en porcentaje fijo; las otras bases reparten según un indicador de cada mes, como los
  metros cuadrados, o según los empleados activos de cada centro. Faltan los receptores. En el primero abro la lista, y
  elijo Ventas Santo Domingo. En su porcentaje anoto cincuenta: le toca la mitad, porque es la sucursal que más espacio
  ocupa. Pulso Agregar receptor. En la fila nueva abro la lista, y elijo Ventas Santiago. En su porcentaje anoto treinta,
  que es su parte de la oficina. Vuelvo a pulsar Agregar receptor para el último. Abro su lista, y elijo Operaciones.
  Y en su porcentaje anoto el veinte restante. Los tres porcentajes tienen que sumar cien, y el total lo confirma.
  Guardo la regla, y el aviso lo confirma.""",
  [esc("input[formcontrolname='fromCode']", "6.03.02", "En Desde la cuenta escribo"),
   esc("input[formcontrolname='toCode']", "6.03.03", "Y en Hasta la cuenta"),
   res("mat-form-field:has(mat-select[formcontrolname='basis'])", "dejo la base en porcentaje fijo", 9000),
   clic(R + "mat-select[formcontrolname='costCenter'] >> nth=0", "En el primero abro"),
   clic("mat-option:has-text('CC-VEN-SD')", "elijo Ventas Santo Domingo"),
   esc(R + "input[formcontrolname='percentage'] >> nth=0", "50", "anoto cincuenta"),
   clic("button:has-text('Agregar receptor')", "Pulso Agregar receptor"),
   clic(R + "mat-select[formcontrolname='costCenter'] >> nth=1", "En la fila nueva abro"),
   clic("mat-option:has-text('CC-VEN-STI')", "elijo Ventas Santiago"),
   esc(R + "input[formcontrolname='percentage'] >> nth=1", "30", "anoto treinta"),
   clic("button:has-text('Agregar receptor')", "Vuelvo a pulsar Agregar"),
   clic(R + "mat-select[formcontrolname='costCenter'] >> nth=2", "Abro su lista"),
   clic("mat-option:has-text('CC-OPS')", "elijo Operaciones"),
   esc(R + "input[formcontrolname='percentage'] >> nth=2", "20", "anoto el veinte"),
   res(":text('Total:') >> nth=0", "el total lo confirma", 2500),
   clic("button:has-text('Guardar')", "Guardo la regla"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
 paso("03-ejecutar", "Ejecutar la distribución", "Vista previa y contabilizar", "Contabilidad › Distribución de Costos › Ejecutar",
  "Vista previa · contabilizar",
  """La regla solo define el reparto; el movimiento se hace al ejecutarla, una vez por período. Paso a la pestaña Ejecutar.
  En Período contable abro la lista, y elijo Noviembre de dos mil veintiséis. Sin elegir reglas, se ejecutan todas las
  activas. Pulso Vista previa, que calcula sin registrar nada. La regla sale Lista para contabilizar, con ochenta y cuatro
  mil pesos: el alquiler y los servicios de noviembre. Debajo está el detalle. En Receptores, cuánto recibe cada
  centro: cuarenta y dos mil Santo Domingo, veinticinco mil doscientos Santiago y dieciséis mil ochocientos Operaciones.
  Y debajo, el asiento que se va a registrar: sale de Administración y entra a cada receptor, en las mismas cuentas.
  Todo cuadra, así que pulso Contabilizar. El sistema avisa que registrará un asiento por regla; confirmo. Tras un momento, el
  sistema informa que la distribución quedó contabilizada, con su asiento. Acepto el aviso.""",
  [clic("app-console-tabs :text('Ejecutar'), [role=tab]:has-text('Ejecutar')", "Paso a la pestaña Ejecutar"),
   clic("mat-form-field:has-text('Período contable') mat-select", "abro la lista"),
   clic("mat-option:has-text('Noviembre 2026')", "elijo Noviembre"),
   clic("button:has-text('Vista previa')", "Pulso Vista previa"),
   res(".rule-head >> nth=0", "La regla sale Lista", 5500),
   res("table.lines >> nth=0", "En Receptores", 9000),
   res("table.lines >> nth=1", "el asiento que se va a registrar", 7000),
   clic("button:has-text('Contabilizar')", "pulso Contabilizar"),
   res("mat-dialog-container", "El sistema avisa", 2500),
   clic("mat-dialog-container button:has-text('Contabilizar')", "confirmo"),
   res("mat-dialog-container", "quedó contabilizada", 2000),
   clic("mat-dialog-container button:has-text('Aceptar')", "Acepto el aviso")],
  navegar="/accounting/distribucion-costos/reglas"),
 paso("04-historial", "Historial y anulación", "Historial", "Contabilidad › Distribución de Costos › Historial",
  "Cada ejecución con su asiento · anular",
  """Cada ejecución queda en el Historial: el período, la regla, lo distribuido, sus receptores y el asiento que generó,
  que se abre desde su fila. Desde ese momento, los informes por centro muestran a Ventas y a Operaciones con su parte del
  alquiler, y a Administración sin ese gasto. Si algo salió mal, Anular registra el asiento de reverso en el mismo
  período, pide un motivo y deja la distribución como anulada, lista para ejecutarse de nuevo. Con varias reglas
  encadenadas, se anulan de la última a la primera.""",
  [res("tr.mat-mdc-row >> nth=0 >> td >> nth=2", "lo distribuido", 3000),
   res("tr.mat-mdc-row >> nth=0 >> td >> nth=4", "el asiento que generó", 4000),
   res("tr.mat-mdc-row >> nth=0 >> td >> nth=5", "los informes por centro", 6000),
   res("tr.mat-mdc-row >> nth=0 >> button[aria-label='Anular']", "Anular registra", 7000, True),
   res("tr.mat-mdc-row >> nth=0 >> td >> nth=6", "Con varias reglas", 4000)],
  navegar="/accounting/distribucion-costos/historial"),
]
guardar("contabilidad-42-distribucion-costos", g, pasos)
