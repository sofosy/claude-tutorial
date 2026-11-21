from comun import *
g = base("Contabilidad · Informes por centro de costo: resultados, acumulado y Libro Mayor",
  "Cómo leer en Germiva el informe Resultados por Centro de Costo, acumularlo en los centros principales, filtrar el Estado de Resultados por un centro y ver en el Libro Mayor los movimientos de un centro.",
  "Video 43 de la serie Contabilidad. setup: preparar.sh resultados-centro (noviembre 2026: ventas 400,000 y 250,000 por sucursal, costos, sueldos, gastos de Operaciones y Logística, e indirectos de Administración ya distribuidos con DIST-ADM).",
  "/accounting/financial-statements/income-statement-by-cost-center", "button:has-text('Generar')",
  "seeds/contabilidad/preparar.sh resultados-centro",
  ["Leer los resultados de cada centro en columnas", "Acumular los subcentros en su centro principal",
   "Filtrar el Estado de Resultados por un centro", "Ver en el Mayor los movimientos de un centro"],
  ["Buscar el filtro de centro en el Balance General: solo los informes de resultados se filtran por centro",
   "Olvidar que un centro padre incluye a sus subcentros", "Leer «Sin centro» como error: son movimientos sin imputar"])
M = "table.cc-matrix "
pasos = [
 paso("01-informe", "Resultados por centro", "Resultados por Centro de Costo", "Contabilidad › Informes Financieros › Resultados por Centro de Costo",
  "Un estado de resultados con una columna por centro",
  """Con los centros en los documentos, este informe responde cuánto ganó cada área. Está en Informes Financieros, y se
  llama Resultados por Centro de Costo. Recojo el menú. En Período contable abro la lista, y elijo Noviembre de dos mil
  veintiséis. Pulso Generar. Es un estado de resultados con una columna por centro. Arriba, los ingresos: cuatrocientos mil
  de Santo Domingo y doscientos cincuenta mil de Santiago. Luego los costos y los gastos de cada uno. En Arrendamientos se
  ve la distribución: el alquiler que pagó Administración ya está repartido entre Operaciones y las dos sucursales. Y al
  pie, la utilidad de cada centro: Santo Domingo ganó setenta y tres mil pesos, y Logística y Operaciones, que solo
  gastan, salen en negativo. La columna Total coincide con el Estado de Resultados de la empresa.""",
  [res("mat-form-field:has-text('Tipo de informe')", "se llama Resultados por Centro", 3500),
   clic("button.panel-collapse", "Recojo el menú"),
   clic("mat-select[formcontrolname='accountingPeriodId']", "abro la lista"),
   clic("mat-option:has-text('Noviembre 2026')", "elijo Noviembre"),
   clic("button:has-text('Generar')", "Pulso Generar"),
   res(M + "thead", "una columna por centro", 4000),
   res(M + "tr:has-text('4.01.01')", "Arriba, los ingresos", 6000),
   res(M + "tr:has-text('6.03.02')", "En Arrendamientos", 9000),
   res(M + "tr.result-row >> nth=-1", "la utilidad de cada centro", 9500),
   res(M + "thead th >> nth=-1", "La columna Total", 4000)]),
 paso("02-acumular", "Acumular y filtrar", "Acumular en los centros principales", "Contabilidad › Informes Financieros › Resultados por Centro de Costo",
  "Los subcentros se suman a su centro principal",
  """Para una vista más resumida, marco Acumular en los centros principales, y vuelvo a pulsar Generar. Ahora cada subcentro
  se suma a su padre: las dos sucursales quedan en Ventas, con ciento diecisiete mil ochocientos de utilidad, y Logística
  queda dentro de Operaciones. El filtro Centro de costo limita el informe a un centro y a los que dependen de él. Y el
  botón Excel exporta la tabla.""",
  [clic("mat-checkbox[formcontrolname='rollUp'] label", "marco Acumular"),
   clic("button:has-text('Generar')", "vuelvo a pulsar Generar"),
   res(M + "thead", "cada subcentro se suma", 4000),
   res(M + "tr.result-row >> nth=-1", "las dos sucursales quedan", 7000),
   res("mat-form-field:has(mat-select[formcontrolname='costCenterId'])", "El filtro Centro de costo", 5500),
   res("button:has-text('Excel')", "el botón Excel", 2500, True)]),
 paso("03-estado", "Estado de Resultados por centro", "Estado de Resultados de un centro", "Contabilidad › Informes Financieros › Estado de Resultados",
  "El mismo informe de siempre, de un solo centro",
  """El Estado de Resultados normal también se puede pedir de un solo centro. En Tipo de informe abro la lista, y elijo
  Estado de Resultados. Elijo el período, Noviembre, igual que antes. Después, en Centro de costo abro la lista, y elijo Ventas Santo Domingo.
  Pulso Generar. Es el estado completo, pero solo de esa sucursal: sus ventas, su costo, sus gastos y su utilidad. Los
  informes de balance no tienen este filtro: la caja, los bancos y las cuentas por cobrar no llevan centro.""",
  [clic("mat-form-field:has-text('Tipo de informe') mat-select", "En Tipo de informe abro"),
   clic("mat-option:has-text('Estado de Resultados')", "elijo Estado de Resultados"),
   clic("mat-select[formcontrolname='accountingPeriodId']", "Elijo el período"),
   clic("mat-option:has-text('Noviembre 2026')", "Noviembre"),
   clic("mat-select[formcontrolname='costCenterId']", "En Centro de costo abro"),
   clic("mat-option:has-text('Ventas Santo Domingo')", "elijo Ventas Santo Domingo"),
   clic("button:has-text('Generar')", "Pulso Generar"),
   res(".net-income-row", "solo de esa sucursal", 6000),
   res("mat-form-field:has(mat-select[formcontrolname='costCenterId'])", "Los informes de balance", 6000)]),
 paso("04-mayor", "El centro en el Mayor", "Libro Mayor por centro", "Contabilidad › Diario y Mayor › Libro Mayor",
  "Los movimientos de un centro, uno por uno",
  """Y para ver el detalle, el Libro Mayor. Tiene el mismo filtro, junto a la cuenta y las fechas: en Centro de costo abro la
  lista, y elijo Logística, el centro que quiero revisar. Con el filtro puesto, pulso Consultar. Quedan solo las cuentas con movimientos de ese centro, y cada movimiento dice a qué centro pertenece.
  Con el módulo de Proyectos, a su lado está el filtro por proyecto, que funciona igual. Así se llega del resultado de un
  centro hasta el asiento que lo explica.""",
  [res("mat-form-field:has(mat-select[formcontrolname='costCenterId'])", "Tiene el mismo filtro", 2500),
   clic("mat-select[formcontrolname='costCenterId']", "en Centro de costo abro"),
   clic("mat-option:has-text('Logística')", "elijo Logística"),
   clic("button:has-text('Consultar')", "pulso Consultar"),
   res("span.account-ref >> nth=0", "cada movimiento dice", 5000),
   res("app-project-picker", "el filtro por proyecto", 5000),
   res("span.account-ref >> nth=0", "hasta el asiento", 3000)],
  navegar="/accounting/registro/mayor"),
]
guardar("contabilidad-43-informes-por-centro", g, pasos)
