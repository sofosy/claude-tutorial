from comun import *
g = base("Contabilidad · Centros de costo: crear, jerarquía y ejecución",
  "Cómo crear en Germiva un centro de costo con su centro padre, su responsable y su presupuesto, leer la jerarquía con los centros agrupadores, ver la ejecución presupuestaria de un centro y por qué un centro con movimientos se inactiva en lugar de eliminarse.",
  "Video 26 de la serie Contabilidad (regrabado 2026-11 con jerarquía, responsable y ejecución). setup: preparar.sh centros-costo (CC-ADM predeterminado, CC-VEN agrupador con Santo Domingo y Santiago, CC-OPS con 300,000 de presupuesto y 180,000 ejecutados).",
  "/accounting/configuracion/centros-costo", "button:has-text('Crear Centro de Costo')",
  "seeds/contabilidad/preparar.sh centros-costo",
  ["Crear un centro de costo con padre, responsable y presupuesto", "Leer la jerarquía y los centros agrupadores",
   "Ver la ejecución presupuestaria de un centro", "Inactivar un centro en lugar de eliminarlo"],
  ["Imputar gastos a un centro agrupador: solo suma los de sus subcentros", "Repetir un código: cada centro tiene el suyo",
   "Intentar eliminar un centro con movimientos: se inactiva"])
F = "tr.mat-mdc-row:has-text('%s')"
pasos = [
 paso("01-lista", "Los centros de costo", "Centros de Costo", "Contabilidad › Configuración Contable › Centros de Costo",
  "Áreas a las que se imputan ingresos y gastos",
  """Un centro de costo es un área de la empresa a la que se imputan ingresos y gastos: una sucursal, un departamento.
  Sirve para saber cuánto gana y cuánto gasta cada área. Recojo el menú. Cada fila es un centro, con su código, su nombre,
  el tipo, de qué centro depende, su presupuesto, el responsable y el estado. Administración lleva la marca Predeterminado:
  es el centro que reciben los ingresos y gastos que se registran sin centro.""",
  [res(F % "CC-ADM" + " td >> nth=1", "un área de la empresa", 3500),
   clic("button.panel-collapse", "Recojo el menú"),
   res(F % "CC-OPS" + " td >> nth=1", "Cada fila es un centro", 4500),
   res(F % "CC-VEN-SD" + " td >> nth=3", "de qué centro depende", 2500),
   res(F % "CC-ADM" + " .gm-badge:has-text('Predeterminado')", "lleva la marca Predeterminado", 5000)]),
 paso("02-crear", "Crear un centro", "Nuevo Centro de Costo", "Contabilidad › Centros de Costo › Nuevo",
  "Código · nombre · tipo · depende de · responsable · presupuesto",
  """Voy a agregar el área de logística. Pulso Crear Centro de Costo. Escribo el código, CC-LOG, que no se puede repetir
  en la empresa. Luego escribo el nombre: Logística. Con el código y el nombre escritos, miro el tipo: costo, ingresos, utilidad o inversión;
  lo dejo en Costo. En Depende de abro la lista, y elijo Operaciones: así Logística queda como subcentro suyo.
  En Responsable escribo Gabriela, para buscar a la empleada a cargo. Aparece en la lista, y la elijo.
  Por último el presupuesto del área: ciento veinte mil pesos. Guardo, y el aviso lo confirma.""",
  [clic("button:has-text('Crear Centro de Costo')", "Pulso Crear Centro de Costo"),
   esc("input[formcontrolname='code']", "CC-LOG", "Escribo el código"),
   esc("input[formcontrolname='name']", "Logística", "Luego escribo el nombre"),
   res("mat-form-field:has(mat-select[formcontrolname='type'])", "miro el tipo", 4000),
   clic("mat-select[formcontrolname='parent']", "abro la lista"),
   clic("mat-option:has-text('CC-OPS')", "elijo Operaciones"),
   esc("app-custom-select[formcontrolname='responsibleEmployee'] input", "Gabriela", "escribo Gabriela"),
   clic("mat-option:has-text('Gabriela Torres')", "y la elijo"),
   esc("input[formcontrolname='budgetAmount']", "120000", "Por último el presupuesto"),
   clic("button:has-text('Guardar')", "Guardo"),
   res(".mat-mdc-snack-bar-container", "el aviso lo confirma", 2500)]),
 paso("03-jerarquia", "La jerarquía", "Ver Jerarquía", "Contabilidad › Configuración Contable › Centros de Costo",
  "Centros, subcentros y agrupadores",
  """Para ver cómo quedó, pulso Ver Jerarquía. Es el árbol completo: Logística aparece dentro de Operaciones, y las dos
  sucursales dentro de Ventas. Ventas lleva la marca Agrupador: no recibe movimientos propios, solo suma los de sus
  subcentros. En los informes, un centro padre siempre acumula lo de sus hijos. Cierro.""",
  [clic("button:has-text('Ver Jerarquía')", "pulso Ver Jerarquía"),
   res("mat-dialog-container .cc-tree", "Es el árbol completo", 5000),
   res("mat-dialog-container .cc-node:has-text('CC-VEN') .gm-badge >> nth=0", "lleva la marca Agrupador", 6500),
   clic("mat-dialog-container button:has-text('Cerrar')", "Cierro")]),
 paso("04-ficha", "La ficha del centro", "Ejecución presupuestaria", "Contabilidad › Centros de Costo › CC-OPS",
  "Presupuesto, ejecutado, disponible y utilización",
  """Ahora abro Operaciones con el lápiz de su fila. Arriba, el botón Inactivar: un centro inactivo deja de ofrecerse en los
  documentos, sin perder su historial. El interruptor Permite registro directo es el que se apaga en los centros
  agrupadores. Y abajo, la ejecución presupuestaria: de trescientos mil pesos de presupuesto, Operaciones lleva ejecutados
  ciento ochenta mil, el sesenta por ciento, contando el gasto contabilizado del centro y de sus subcentros.""",
  [clic(F % "CC-OPS" + " button[aria-label='Editar']", "con el lápiz de su fila"),
   res("button:has-text('Inactivar')", "el botón Inactivar", 4500),
   res("mat-slide-toggle[formcontrolname='allowsDirectPosting']", "El interruptor", 4500),
   res(".cc-usage", "la ejecución presupuestaria", 9000)]),
 paso("05-eliminar", "Inactivar, no eliminar", "Eliminar un centro con movimientos", "Contabilidad › Configuración Contable › Centros de Costo",
  "Un centro con movimientos no se elimina: se inactiva",
  """Vuelvo a la lista de centros. ¿Y si quiero borrar Operaciones? En su fila pulso Eliminar. El sistema pide confirmar, porque no se puede deshacer; confirmo.
  Y no lo permite, y explica por qué: Operaciones tiene subcentros. Tampoco se elimina un centro que ya tiene
  movimientos, o que es el predeterminado: lo correcto es inactivarlo. Solo se borra un centro que nunca se usó.
  Con los centros creados, el siguiente paso es usarlos en los documentos.""",
  [clic(F % "CC-OPS" + " button[aria-label='Eliminar']", "pulso Eliminar"),
   clic("mat-dialog-container button.confirm-button", "porque no se puede deshacer; confirmo"),
   res(".mat-mdc-snack-bar-container, mat-dialog-container", "y explica por qué", 6000),
   res(F % "CC-OPS" + " td >> nth=6", "lo correcto es inactivarlo", 4000),
   res("button:has-text('Crear Centro de Costo')", "Con los centros creados", 3500)],
  navegar="/accounting/configuracion/centros-costo"),
]
guardar("contabilidad-26-centros-costo", g, pasos)
