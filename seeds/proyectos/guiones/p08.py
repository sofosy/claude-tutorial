from comun import *
g = base_p("Proyectos · Cubicaciones: medir el avance, facturarlo y el fondo de reparo",
  "Cómo facturar un proyecto por avance en Germiva: crear la cubicación del período midiendo cada partida, enviarla y aprobarla, generar su factura con la amortización del anticipo y el fondo de reparo retenido, y liberar el fondo al final.",
  "Video 08 de la serie Proyectos. setup: seeds/proyectos/preparar.sh cubicacion (contrato por avance de 6,600,000 con anticipo 20 %, amortización 20 % y fondo de reparo 5 %; anticipo facturado y emitido; Laura Méndez aprueba y factura: el video cambia de usuario en cámara).",
  "/projects/17/facturacion", "button:has-text('Nueva cubicación')", "cubicacion",
  ["Crear la cubicación de un período", "Medir cada partida por cantidad o por porcentaje",
   "Aprobar la cubicación y generar su factura", "Qué es el fondo de reparo y cómo se libera"],
  ["Abrir una cubicación nueva sin facturar la anterior: solo hay una abierta a la vez",
   "Olvidar que la factura descuenta la amortización del anticipo",
   "Querer liberar el fondo de reparo de una factura en borrador"])
D = "mat-dialog-container "
pasos = [
 paso("01-medir", "Nueva cubicación", "Nueva cubicación", "Proyectos › Cartera › PRJ › Facturación",
  "Lo ejecutado en el período, partida por partida",
  """Una cubicación es la medición de lo que se ejecutó en un período, y es lo que se le factura al cliente. En la pestaña
  Facturación, recojo el menú, y bajo a Cubicaciones. Pulso Nueva cubicación. La tabla trae las partidas del presupuesto,
  con lo contratado y lo medido antes. La excavación se terminó completa: en su fila pulso el botón Completar. Queda en
  cien por ciento, con su monto. De las zapatas va la mitad. En su fila cambio la medición a porcentaje, con el botón
  de porcentaje. Y en Este período anoto cincuenta, por la mitad de las zapatas ya vaciadas. El sistema calcula la cantidad y el monto con el precio de la
  partida. Abajo suma el avance del período. Pulso Guardar, y el aviso lo confirma.""",
  [clic("button.panel-collapse", "recojo el menú"),
   res("#billing-progress-title", "bajo a Cubicaciones", 2500),
   clic("button:has-text('Nueva cubicación')", "Pulso Nueva cubicación"),
   res(D + "table thead", "La tabla trae las partidas", 4500),
   clic(D + "button[aria-label='Completar 01.01']", "pulso el botón Completar"),
   res(D + "tr:has-text('01.01') td >> nth=-1", "con su monto", 2500),
   clic(D + "tr:has-text('01.02') button[aria-label='Porcentaje del período']", "cambio la medición"),
   esc(D + "input[aria-label^='Ejecutado este período en 01.02']", "50", "anoto cincuenta"),
   res(D + "tr:has-text('01.02') td >> nth=-1", "calcula la cantidad y el monto", 4500),
   clic(D + "button:has-text('Guardar')", "Pulso Guardar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
 paso("02-aprobar", "De la cubicación a la factura", "Enviar y aprobar", "Proyectos › Cartera › PRJ › Facturación › CUB-000001",
  "Avance − amortización = base · fondo de reparo retenido",
  """La cubicación queda en borrador. La abro con un clic en su número. A la derecha, el sistema explica cómo se convierte en
  factura. El avance medido del período es un millón tres mil doscientos pesos. De ahí se descuenta la amortización del
  anticipo, el veinte por ciento. Lo que queda es la base de la factura, y el ITBIS se calcula sobre el diez por ciento de
  esa base. Al final, el fondo de reparo: el cinco por ciento del avance, que el cliente retiene y no paga todavía.
  Con las cifras revisadas, pulso Enviar a aprobación, y confirmo. Como en el presupuesto, quien envía una cubicación no la
  aprueba: lo hace otro supervisor.""",
  [clic("table[aria-label='Cubicaciones del proyecto'] button.link", "con un clic en su número"),
   res("#progress-billing-detail :text('De la cubicación a la factura') >> nth=0", "el sistema explica", 4000),
   res("#progress-billing-detail :text('Avance medido del período') >> nth=-1", "El avance medido", 4500),
   res("#progress-billing-detail :text('Amortización del anticipo') >> nth=0", "la amortización del", 4500),
   res("#progress-billing-detail :text('Base de la factura') >> nth=0", "la base de la factura", 6000),
   res("#progress-billing-detail :text('Fondo de reparo retenido') >> nth=0", "el fondo de reparo", 6500),
   clic("#progress-billing-detail button:has-text('Enviar a aprobación')", "pulso Enviar a aprobación"),
   clic("mat-dialog-container button.confirm-button, mat-dialog-container button:has-text('Enviar')", "y confirmo"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False},
   res("table[aria-label='Cubicaciones del proyecto'] tbody tr >> nth=0 >> td >> nth=4", "quien envía una cubicación", 4500)]),
 paso("03-laura", "Aprobar", "Aprueba otra persona", "Acceso",
  "Entra la otra supervisora",
  """Entra entonces Laura Méndez, la otra supervisora. Abro el menú del usuario, y cierro sesión. En el acceso escribo su
  usuario. Después, en el campo de la contraseña, escribo su clave. Con el usuario y la clave ya escritos, pulso el botón
  Iniciar sesión. El sistema le recuerda un dato pendiente de la empresa, que no afecta a los proyectos; pulso Más
  tarde.""",
  [clic("button.topbar-user", "Abro el menú del usuario"),
   clic(".mat-mdc-menu-panel :text('Cerrar sesión')", "cierro sesión"),
   esc("input[formcontrolname='username']", "laura.mendez", "escribo su\n  usuario".replace("\n  ", " ")),
   esc("input[formcontrolname='password']", "Demo2026!", "escribo su clave"),
   clic("button.auth-primary-btn", "pulso el botón"),
   res("mat-dialog-container", "El sistema le recuerda", 3000),
   clic("mat-dialog-container button:has-text('Más tarde')", "pulso Más\n  tarde".replace("\n  ", " "))]),
 paso("04-facturar", "Facturar la cubicación", "Facturar", "Proyectos › Cartera › PRJ › Facturación › CUB-000001",
  "La factura sale en borrador en Ventas",
  """Ya como Laura, vuelvo a la pestaña Facturación del proyecto, y abro la cubicación con un clic en su número. Está en
  aprobación. Pulso Aprobar, y en el diálogo confirmo con Aprobar. Con la cubicación aprobada aparece el botón Facturar.
  Lo pulso. La vista previa repite las cifras: la base, el ITBIS, el
  total de la factura, y lo que queda por cobrar ahora, sin el fondo de reparo. Pulso Generar factura. La factura se crea
  en borrador en Ventas, con la amortización como descuento, y allí se emite con su comprobante. En la tabla Facturas del
  proyecto quedan las dos: la del anticipo y la de esta cubicación, con su bruto, su amortización y el fondo por
  liberar.""",
  [clic("table[aria-label='Cubicaciones del proyecto'] button.link", "con un clic en su número"),
   clic("#progress-billing-detail button:has-text('Aprobar')", "Pulso Aprobar"),
   clic("mat-dialog-container button:has-text('Aprobar')", "confirmo con Aprobar"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2000, "cursor": False},
   clic("#progress-billing-detail button:has-text('Facturar')", "Lo pulso"),
   res("mat-dialog-container", "La vista previa repite", 8000),
   clic("mat-dialog-container button:has-text('Generar factura')", "Pulso Generar factura"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 3500, "cursor": False},
   res("#billing-documents-title", "En la tabla Facturas del", 3000),
   res("section:has(#billing-documents-title) tbody tr >> nth=0 >> td >> nth=0", "la de esta cubicación", 6000)],
  navegar="/projects/17/facturacion"),
 paso("05-fondo", "El fondo de reparo", "Fondo de reparo", "Proyectos › Cartera › PRJ › Facturación",
  "Lo retenido se libera al recibir la obra",
  """Queda el fondo de reparo. Lo retenido en cada factura se acumula en una cuenta por cobrar propia, aparte de la del
  cliente. Cuando la obra se recibe sin defectos, se pulsa Liberar fondo: se elige la factura emitida, el monto y la fecha,
  y el sistema pasa ese valor a la cuenta por cobrar normal, para cobrarlo como cualquier factura. Mientras las facturas
  estén en borrador, el fondo no se puede liberar: primero se emiten en Ventas. Así se factura toda la obra: una
  cubicación por período, hasta completar el contrato.""",
  [res("#billing-retention-title", "Queda el fondo de reparo", 5000),
   res("button:has-text('Liberar fondo')", "se pulsa Liberar fondo", 7000, True),
   res("#billing-retention-title", "Mientras las facturas", 6000),
   res("#billing-progress-title", "una\n  cubicación por período".replace("\n  ", " "), 4000)]),
]
guardar("proyectos-08-cubicaciones", g, pasos)
