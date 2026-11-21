from comun import *
g = base_p("Contabilidad · Las obras dentro del presupuesto contable: incorporar los presupuestos de proyecto",
  "Cómo llevar el presupuesto de cada proyecto al presupuesto contable de la empresa en Germiva: el botón Presupuestos de proyecto, el cuadre proyecto contra contable y los renglones que se incorporan por cuenta, centro de costo y mes.",
  "Video 46 de la serie Contabilidad. setup: seeds/proyectos/preparar.sh consolidar (la obra Nave industrial Haina con su presupuesto aprobado, de noviembre a abril, y el presupuesto contable anual 2026 en borrador con los gastos fijos).",
  "/accounting/budgets/list", "tr.mat-mdc-row:has-text('PRES-2026')", "consolidar",
  ["Incorporar los presupuestos de proyecto al presupuesto contable", "Leer el cuadre proyecto contra contable",
   "Reconocer los renglones incorporados", "Qué hacer cuando el presupuesto de la obra cambia"],
  ["Copiar a mano el presupuesto de la obra en el presupuesto contable",
   "Querer editar los renglones incorporados: se actualizan volviendo a incorporar",
   "Esperar el total de la obra en un solo año: solo entra lo que cae en el ejercicio"])
D = "mat-dialog-container "
pasos = [
 paso("01-incorporar", "Incorporar las obras", "Presupuestos de proyecto", "Contabilidad › Presupuestos › PRES-2026",
  "El presupuesto de cada obra entra al presupuesto contable",
  """La empresa tiene su presupuesto anual, y cada obra tiene el suyo. Para que el presupuesto contable incluya las obras
  no se copian a mano: se incorporan. En Presupuestos, abro el anual con Ver detalles. Por ahora solo tiene los gastos
  fijos. Arriba, pulso Presupuestos de proyecto. El diálogo lista cada proyecto con presupuesto vigente: la nave de Haina,
  con cinco millones y medio de pesos. De ese total, en este ejercicio cae un millón ochocientos treinta y tres mil:
  noviembre y diciembre, según el cronograma de sus partidas. El resto es del año próximo. La diferencia sale en rojo,
  porque todavía no se ha incorporado. Pulso Incorporar presupuestos de proyecto. La diferencia queda en cero, y el estado
  pasa a Cuadrado. Cierro el diálogo.""",
  [res("tr.mat-mdc-row:has-text('PRES-2026') td >> nth=1", "La empresa tiene su presupuesto", 3500),
   clic("tr.mat-mdc-row:has-text('PRES-2026') button[aria-label='Ver detalles']", "con Ver detalles"),
   clic("button:has-text('Presupuestos de proyecto')", "pulso Presupuestos de proyecto"),
   res(D + "table.recon tbody td >> nth=1", "la nave de Haina", 4000),
   res(D + "table.recon tbody td >> nth=2", "en este ejercicio cae", 6500),
   res(D + "table.recon tbody td >> nth=4", "La diferencia sale en rojo", 4000),
   clic(D + "button:has-text('Incorporar')", "Pulso Incorporar presupuestos"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2000, "cursor": False},
   res(D + "table.recon tbody td >> nth=6", "y el estado", 3000),
   clic(D + "button:has-text('Cerrar')", "Cierro el diálogo")]),
 paso("02-renglones", "Los renglones incorporados", "Cuenta × centro × mes", "Contabilidad › Presupuestos › PRES-2026",
  "Un renglón por cuenta, centro de costo y mes",
  """En las líneas del presupuesto aparecen los renglones nuevos. Llevan la cuenta Costos de obra, el centro de costo del
  proyecto, y un renglón por cada mes. Tienen el ícono de proyecto, y su monto no se edita aquí. Si el presupuesto de la
  obra cambia, por ejemplo con una orden de cambio, se vuelve a incorporar con el mismo botón. Abajo, el total de costos y
  gastos ya incluye la obra. Así las variaciones de la empresa, y el control de cada obra, salen de las mismas cifras.""",
  [res("div.table-row:has(mat-icon.project-origin) >> nth=0 >> div.table-cell >> nth=0", "Llevan la cuenta Costos de obra", 3000),
   res("div.table-row:has(mat-icon.project-origin) >> nth=0 >> div.table-cell >> nth=1", "el centro de costo del", 3000),
   res("div.table-row:has(mat-icon.project-origin) >> nth=1 >> div.table-cell >> nth=2", "y un renglón por cada mes", 3000),
   res("div.table-row:has(mat-icon.project-origin) >> nth=0 >> div.table-cell >> nth=3", "y su monto no se edita", 4000),
   res("button:has-text('Presupuestos de proyecto')", "se vuelve a incorporar", 4500, True),
   res(":text('Costos y gastos') >> nth=0", "el total de costos y", 5000),
   res("button:has-text('Ver variaciones')", "Así las variaciones", 5000)]),
]
guardar("contabilidad-46-presupuestos-de-proyecto", g, pasos)
