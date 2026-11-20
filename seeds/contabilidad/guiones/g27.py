from comun import *
g = base("Contabilidad · Presupuestos: crear por cuenta y centro, aprobar y cerrar",
  "Cómo crear en Germiva un presupuesto por cuenta contable, centro de costo y mes, aprobarlo para compararlo contra lo real, y qué significan reabrir, cerrar, cancelar y eliminar.",
  "Video 27 de la serie Contabilidad (regrabado 2026-11 con centro de costo por línea, real en vivo y ciclo de vida). setup: preparar.sh presupuestos (árbol de centros y noviembre contabilizado: ventas 650,000, mantenimiento de Operaciones 35,000).",
  "/accounting/budgets/list", "button:has-text('Nuevo Presupuesto')",
  "seeds/contabilidad/preparar.sh presupuestos",
  ["Crear un presupuesto por cuenta, centro de costo y mes", "Aprobarlo y ver lo real junto a lo presupuestado",
   "Reabrir, cerrar, cancelar y eliminar un presupuesto", "Leer los estados en el listado"],
  ["Presupuestar una cuenta de grupo: solo se presupuestan cuentas de movimiento",
   "Repetir la misma cuenta, centro y período en dos líneas",
   "Querer editar un presupuesto aprobado: primero se reabre"])
L = ".table-row >> nth=%d >> "
pasos = [
 paso("01-crear", "Crear el presupuesto", "Nuevo Presupuesto", "Contabilidad › Presupuestos › Nuevo",
  "Código · nombre · tipo · fechas",
  """Un presupuesto fija cuánto se espera vender y gastar en cada cuenta, para compararlo después con lo real. Recojo el
  menú, y pulso Nuevo Presupuesto. Escribo el código, PRES-2026-11, que no se puede repetir en la empresa. Después va el
  nombre, para reconocerlo en la lista: Operativo de noviembre. Con el código y el nombre escritos, en Tipo de Presupuesto
  abro la lista, y de las opciones elijo Mensual. Siguen las fechas: en Fecha de Inicio escribo el primero de noviembre de
  dos mil veintiséis. Y en Fecha de Fin, el treinta de noviembre del mismo año: un solo mes. El período contable es
  opcional; si se deja vacío, se usa el ejercicio de la fecha de inicio.""",
  [clic("button.panel-collapse", "Recojo el menú"),
   clic("button:has-text('Nuevo Presupuesto')", "pulso Nuevo Presupuesto"),
   esc("input[formcontrolname='code']", "PRES-2026-11", "Escribo el código"),
   esc("input[formcontrolname='name']", "Operativo de noviembre", "Después va el nombre"),
   clic("mat-select[formcontrolname='type']", "abro la lista"),
   clic("mat-option:has-text('Mensual')", "elijo Mensual"),
   esc("input[formcontrolname='startDate']", "01/11/2026", "en Fecha de Inicio escribo"),
   esc("input[formcontrolname='endDate']", "30/11/2026", "Y en Fecha de Fin"),
   res("app-autocomplete:has-text('Período contable'), mat-form-field:has-text('Período contable')", "El período contable es opcional", 5000)]),
 paso("02-lineas", "Las líneas", "Líneas del Presupuesto", "Contabilidad › Presupuestos › Nuevo",
  "Una línea por cuenta, centro de costo y período",
  """Ahora las líneas: una por cuenta, centro de costo y período. Pulso Agregar línea. En la cuenta escribo Ventas, para
  buscar la cuenta de ingresos. Aparece en la lista, y elijo la cuatro cero uno cero uno. En Centro de Costo escribo Ventas
  otra vez, ahora para buscar el centro. De la lista elijo el centro Ventas, el que agrupa a las dos sucursales: una línea
  en un centro padre cubre también a sus subcentros. En el período abro la lista, y elijo Noviembre. Y en el monto anoto
  seiscientos mil pesos, lo que se espera vender. Agrego otra línea, para un gasto. En su cuenta escribo Manten, de
  mantenimiento. Aparece en la lista, y la elijo. En su centro escribo Opera, de Operaciones. Aparece, y lo elijo. Abro su
  período, y elijo también Noviembre. Y en su monto anoto treinta mil pesos. Abajo, los totales separan ingresos, costos y
  gastos, y el resultado neto esperado. Guardo, y el aviso lo confirma.""",
  [clic("button.add-btn", "Pulso Agregar línea"),
   esc(L % 0 + "input[placeholder='Buscar cuenta...']", "Ventas", "En la cuenta escribo Ventas"),
   clic("mat-option:has-text('4.01.01')", "elijo la cuatro cero uno"),
   esc(L % 0 + "input[placeholder='Centro de costo...']", "Ventas", "escribo Ventas\n  otra vez".replace("\n  "," ")),
   clic("mat-option:has-text('CC-VEN - Ventas')", "De la lista elijo el centro"),
   clic(L % 0 + "mat-select[formcontrolname='period']", "En el período abro"),
   clic("mat-option:has-text('Noviembre')", "y elijo Noviembre"),
   esc("app-money-input[formcontrolname='budgetAmount'] >> nth=0 >> input", "600000", "anoto seiscientos mil"),
   clic("button.add-btn", "Agrego otra línea"),
   esc(L % 1 + "input[placeholder='Buscar cuenta...']", "Manten", "En su cuenta escribo Manten"),
   clic("mat-option:has-text('6.03.19')", "y la elijo"),
   esc(L % 1 + "input[placeholder='Centro de costo...']", "Opera", "escribo Opera"),
   clic("mat-option:has-text('CC-OPS')", "y lo elijo"),
   clic(L % 1 + "mat-select[formcontrolname='period']", "Abro su período"),
   clic("mat-option:has-text('Noviembre')", "elijo también Noviembre"),
   esc("app-money-input[formcontrolname='budgetAmount'] >> nth=1 >> input", "30000", "anoto treinta mil"),
   res("div.totals-table", "Abajo, los totales", 5500),
   clic("button:has-text('Guardar')", "Guardo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
]
guardar("contabilidad-27-presupuestos", g, pasos)
