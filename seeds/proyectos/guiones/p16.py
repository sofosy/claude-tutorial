from comun import *
g = base_p("Proyectos · Importar el presupuesto desde Excel",
  "Cómo cargar el presupuesto de un proyecto desde una hoja de Excel en Germiva: descargar la plantilla, importar el archivo, revisar la vista previa con sus errores y confirmar la importación.",
  "Video 16 de la serie Proyectos. setup: seeds/proyectos/preparar.sh importar (el proyecto con su presupuesto en borrador y vacío). Sube seeds/proyectos/presupuesto-nave.xlsx (3 fases, 6 partidas, indirectos 10 % y utilidad 20 %).",
  "/projects/17/presupuesto/2", "button:has-text('Importar Excel')", "importar",
  ["Descargar la plantilla de Excel del presupuesto", "Importar el archivo y leer la vista previa",
   "Confirmar la importación", "Exportar el presupuesto para trabajarlo fuera"],
  ["Importar sobre un borrador ya armado sin saber que lo reemplaza",
   "Confirmar con errores sin corregir el archivo",
   "Querer importar sobre una versión aprobada: se hace en una revisión en borrador"])
IMP = "section.ps-panel:has(#import-title) "
pasos = [
 paso("01-importar", "Importar desde Excel", "Importar Excel", "Proyectos › Cartera › PRJ › Presupuesto",
  "La plantilla, el archivo y la vista previa",
  """Si el presupuesto ya existe en una hoja de cálculo, no hay que digitarlo partida por partida. En el presupuesto en
  borrador, recojo el menú. El botón Excel, plantilla, descarga el formato: una fila por fase o por partida, con su código,
  su unidad, su cantidad y su costo unitario. Con el archivo ya lleno, pulso Importar Excel, y elijo el archivo de la nave.
  El sistema todavía no lo aplica: primero muestra una vista previa. Nueve filas, y cero errores. Si una unidad o una
  cuenta no existiera, aquí saldría la fila exacta, con su mensaje. Y avisa que se reemplazará la estructura del borrador.
  Pulso Confirmar importación, y el aviso lo confirma.""",
  [res("header.ws-header h1", "no hay que digitarlo", 3000),
   clic("button.panel-collapse", "recojo el menú"),
   res("button:has-text('Excel / plantilla')", "El botón Excel", 6500, True),
   {"subir": {"sel": "input[type=file]", "archivo": "seeds/proyectos/presupuesto-nave.xlsx",
              "ancla": "button:has-text('Importar Excel')"}, "al_decir": "pulso Importar Excel"},
   res("#import-title", "primero muestra una vista previa", 3000),
   res(IMP + ".ps-head span.ps-muted", "Nueve filas", 6500),
   res(IMP + ".import p >> nth=0", "Y avisa que se reemplazará", 3500),
   clic(IMP + "button:has-text('Confirmar importación')", "Pulso Confirmar importación"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3000, "cursor": False}]),
 paso("02-resultado", "El presupuesto importado", "Presupuesto listo", "Proyectos › Cartera › PRJ › Presupuesto",
  "Fases, partidas y porcentajes, tal como venían en el archivo",
  """El presupuesto queda armado. Arriba, el costo directo de cinco millones de pesos, con los indirectos y la utilidad que
  traía el archivo en su hoja de configuración. Abajo, las tres fases con sus partidas, sus cantidades y sus costos. Desde
  aquí se sigue igual que siempre: se ajusta lo que haga falta, y se envía a aprobación. Y funciona en los dos sentidos:
  el mismo botón de Excel exporta el presupuesto, para trabajarlo fuera, y volver a importarlo mientras siga en
  borrador.""",
  [res(".budget-figs .gm-fig >> nth=0", "el costo directo", 3500),
   res(".budget-figs .gm-fig >> nth=3", "y la utilidad", 3500),
   res("table.tree tr.is-phase >> nth=0 >> td >> nth=1", "las tres fases", 3000),
   res("table.tree tbody tr >> nth=1 >> td >> nth=1", "sus cantidades y sus costos", 3500),
   res(":text('En aprobación') >> nth=0", "y se envía a aprobación", 3500),
   res("button:has-text('Excel / plantilla')", "el mismo botón de Excel", 5000, True)]),
]
guardar("proyectos-16-importar-desde-excel", g, pasos)
