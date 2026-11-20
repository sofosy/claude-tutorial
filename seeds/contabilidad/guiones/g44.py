from comun import *
g = base("Contabilidad · Variaciones: presupuesto contra lo ejecutado",
  "Cómo leer en Germiva las variaciones de un presupuesto contra lo real: el resumen, el análisis por cuenta y centro, cómo se clasifica cada variación, cómo explicar una desviación y el reporte en PDF y Excel.",
  "Video 44 de la serie Contabilidad. setup: preparar.sh variaciones (PRES-2026-11 aprobado con siete renglones; noviembre contabilizado: ventas +8.33 %, mantenimiento +16.67 %, servicios +20 %, fletes −20 %).",
  "/accounting/budget-variance/resumen", ".budget-item",
  "seeds/contabilidad/preparar.sh variaciones",
  ["Leer el resumen de variaciones de los presupuestos aprobados", "Entender cuándo una variación es favorable o desfavorable",
   "Explicar una variación fuera de tolerancia", "Sacar el reporte en PDF o Excel"],
  ["Esperar variaciones de un borrador: el resumen solo considera presupuestos aprobados",
   "Leer todo exceso como malo: vender más de lo presupuestado es favorable",
   "Dejar sin explicar una variación desfavorable: sigue en las alertas"])
T = "tr:has-text('%s')"
pasos = [
 paso("01-resumen", "El resumen", "Variaciones Presupuestarias", "Contabilidad › Presupuestos › Variaciones",
  "Presupuestado contra ejecutado, de un vistazo",
  """Con un presupuesto aprobado, Variaciones lo compara con lo real. Recojo el menú. Arriba, el resumen de todos los
  presupuestos aprobados: los ingresos ejecutados contra los presupuestados, y lo mismo para costos y gastos. Lo real se lee
  del Mayor al abrir la pantalla; no hay que recalcular nada. Debajo, cada presupuesto con su resultado neto: el de noviembre
  va trescientos sesenta por ciento por encima, a favor. Aun así lleva una marca roja, porque tiene cuentas de gasto que se
  pasaron. Esas cuentas están en Alertas por explicar: el mantenimiento y los servicios públicos.""",
  [clic("button.panel-collapse", "Recojo el menú"),
   res(".summary-strip", "Arriba, el resumen", 8000),
   res(".budget-item >> nth=0", "cada presupuesto con su resultado", 7000),
   res(".budget-item >> nth=0 >> .health-indicator", "lleva una marca roja", 5000),
   res("mat-card:has-text('Alertas por explicar'), .card:has-text('Alertas por explicar')", "Alertas por explicar", 5000)]),
 paso("02-analisis", "El análisis", "Análisis del presupuesto", "Contabilidad › Presupuestos › Variaciones › Análisis",
  "Cada cuenta y centro, con su variación y su estado",
  """Abro el presupuesto de noviembre con un clic. Este es su Análisis. Arriba, los totales por tipo de cuenta: ingresos,
  costos y gastos, y el resultado neto. Y abajo, el detalle de cada línea, con su centro de costo. La variación es lo
  ejecutado menos lo presupuestado, y el estado depende de su tamaño: hasta cinco por ciento está dentro de tolerancia;
  después viene menor, significativa, y crítica desde veinticinco. Pero el sentido importa. En Ventas se ejecutó más de lo
  presupuestado, y como es un ingreso, eso es favorable: sale en verde. En Mantenimiento también se ejecutó más, pero es
  un gasto: variación significativa, desfavorable. El filtro Por explicar deja solo las que piden una explicación.""",
  [clic(".budget-item >> nth=0", "con un clic"),
   res("table.totals-by-type tr >> nth=-1", "los totales por tipo", 5000),
   res(T % "6.01.01.01" + " td >> nth=1", "con su centro de costo", 3500),
   res(T % "5.01.01.01" + " .status-pill", "dentro de tolerancia", 6500),
   res(T % "4.01.01" + " .status-pill", "eso es favorable", 5500),
   res(T % "6.03.19" + " .status-pill", "variación significativa", 4500),
   clic("mat-button-toggle[value='pending'] button", "El filtro Por explicar")]),
 paso("03-explicar", "Explicar una variación", "Explicar variación", "Contabilidad › Presupuestos › Variaciones › Análisis",
  "Explicación y acción correctiva",
  """Una variación desfavorable fuera de tolerancia se explica. En la fila de Mantenimiento pulso el botón de explicar.
  El diálogo muestra las cifras. En Explicación escribo el motivo: hubo una reparación no prevista del montacargas.
  La explicación es obligatoria; la acción correctiva es opcional, pero conviene. Escribo qué se hará: contratar
  mantenimiento preventivo mensual. Con la explicación y la acción escritas, pulso Guardar, y el aviso lo confirma. La variación explicada sale de las alertas, y su
  explicación se conserva: solo vuelve a pedirse si la variación empeora de categoría.""",
  [clic(T % "6.03.19" + " button", "pulso el botón de explicar"),
   res("mat-dialog-container", "El diálogo muestra", 2000),
   esc("textarea[formcontrolname='reviewNotes']", "Reparación no prevista del montacargas.", "En Explicación escribo"),
   esc("textarea[formcontrolname='recommendedActions']", "Contratar mantenimiento preventivo mensual.", "Escribo qué se hará"),
   clic("mat-dialog-container button:has-text('Guardar')", "pulso Guardar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("mat-button-toggle[value='pending']", "sale de las alertas", 5000)]),
 paso("04-reporte", "El reporte", "Reporte de Variaciones", "Contabilidad › Presupuestos › Variaciones › Reporte",
  "Imprimir · PDF · Excel",
  """Para presentarlo, pulso Ver reporte. El Reporte de Variaciones agrupa las líneas en desfavorables, favorables y sin
  variación, con un resumen ejecutivo arriba, y al final lista las explicaciones registradas con su acción correctiva.
  Arriba a la derecha se imprime, o se exporta a PDF o a Excel, que trae tres hojas: resumen, variaciones y por período.
  Y cuando el período termine, cerrar el presupuesto deja estas cifras fijas, como historial.""",
  [clic("button:has-text('Ver reporte')", "pulso Ver reporte"),
   res("h1.report-title", "El Reporte de Variaciones", 3500),
   res(":text('Variaciones Desfavorables') >> nth=0", "desfavorables, favorables", 5000),
   res(":text('Explicaciones y acciones correctivas') >> nth=0", "lista las explicaciones", 5000),
   res("button:has-text('PDF')", "o se exporta a PDF", 2500, True),
   res("button:has-text('Excel')", "o a Excel", 5000, True)]),
]
guardar("contabilidad-44-variaciones", g, pasos)
