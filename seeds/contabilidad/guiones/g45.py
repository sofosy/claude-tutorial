from comun import *
g = base("Contabilidad · Control presupuestario: comprometido, disponible y bloqueo",
  "Cómo hacer en Germiva que un presupuesto aprobado controle lo que se gasta: las políticas sin control, avisar y bloquear, la tolerancia, qué es lo comprometido y lo disponible, y cómo se ve el bloqueo al registrar un asiento.",
  "Video 45 de la serie Contabilidad. setup: preparar.sh control (PRES-2026-11 aprobado; fletes de Logística: presupuesto 25,000, real 20,000, orden de compra aprobada por 3,000 → disponible 2,000).",
  "/accounting/budgets/list", "tr.mat-mdc-row:has-text('PRES-2026-11')",
  "seeds/contabilidad/preparar.sh control",
  ["Elegir la política de control de un presupuesto", "Leer lo comprometido y lo disponible de cada línea",
   "Ver el aviso de disponible al registrar un documento", "Qué hacer cuando el presupuesto bloquea"],
  ["Creer que el control aplica en borrador: solo aplica con el presupuesto aprobado",
   "Olvidar lo comprometido: una orden aprobada ya consume disponible",
   "Poner tolerancia cero y bloquear por centavos"])
L = ".table-row >> nth=%d >> "
F = ".table-row >> nth=4 >>"
pasos = [
 paso("01-politica", "La política de control", "Control presupuestario", "Contabilidad › Presupuestos › PRES-2026-11",
  "Sin control · Avisar · Bloquear · Tolerancia",
  """Hasta aquí, el presupuesto solo se compara con lo real. Pero también puede controlar lo que se gasta. Recojo el menú,
  y abro el presupuesto de noviembre con Ver detalles. En Control presupuestario abro la lista. Hay tres políticas. Sin
  control solo compara. Avisar deja pasar el documento que excede, pero deja constancia y notifica al responsable del
  centro. Y Bloquear lo rechaza: elijo Bloquear, la política más estricta de las tres. Al lado, en Tolerancia anoto cinco: un exceso de hasta el cinco por ciento de la
  línea solo avisa, aunque la política bloquee. Como el presupuesto ya está aprobado, no hace falta reabrirlo: pulso Guardar
  control, y el aviso lo confirma.""",
  [clic("button.panel-collapse", "Recojo el menú"),
   clic("tr.mat-mdc-row:has-text('PRES-2026-11') button[aria-label='Ver detalles']", "con Ver detalles"),
   clic("mat-select[formcontrolname='controlPolicy']", "abro la lista"),
   res("mat-option:has-text('Avisar')", "Avisar deja pasar", 5500),
   clic("mat-option:has-text('Bloquear')", "elijo Bloquear"),
   esc("input[formcontrolname='controlTolerancePercentage']", "5", "en Tolerancia anoto cinco"),
   res("mat-form-field:has(input[formcontrolname='controlTolerancePercentage']) mat-hint", "solo avisa, aunque", 4000),
   clic("button:has-text('Guardar control')", "pulso Guardar\n  control".replace("\n  ", " ")),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2500, "cursor": False}]),
 paso("02-disponible", "Comprometido y disponible", "Comprometido y Disponible", "Contabilidad › Presupuestos › PRES-2026-11",
  "Disponible = presupuesto − comprometido − real",
  """El control trabaja con tres cifras por línea. Mira la de fletes, de Logística: veinticinco mil pesos de presupuesto.
  Real: veinte mil, lo ya contabilizado. Comprometido: tres mil, de una orden de compra aprobada que todavía no se ha
  facturado. Y Disponible: lo que queda, dos mil pesos. Lo comprometido cuenta las requisiciones y las órdenes de compra
  aprobadas, y las facturas de compra que aún no se contabilizan. Todo se calcula en el momento.""",
  [res(F + " .table-cell >> nth=3", "veinticinco mil pesos de presupuesto", 3000),
   res(F + " .table-cell >> nth=4", "Real: veinte mil", 3000),
   res(F + " .table-cell >> nth=5", "Comprometido: tres mil", 6000),
   res(F + " .table-cell >> nth=6", "Y Disponible", 4000),
   res(".table-header", "Lo comprometido cuenta", 7000)]),
 paso("03-asiento", "El control en un documento", "Bloqueado por presupuesto", "Contabilidad › Diario y Mayor › Nuevo asiento",
  "El aviso dice disponible, documento y faltante",
  """Veamos el control en acción. En Diario y Mayor pulso Crear Asiento, para registrar otro flete. Escribo la
  descripción del asiento. Con la descripción lista, bajo a las líneas y agrego la primera línea. En la cuenta busco Fletes,
  la misma cuenta del presupuesto. Aparece en la lista; la elijo, y en su débito anoto cuatro mil pesos, el valor del
  flete. En Centro de Costo escribo Log, porque el gasto es de Logística. Aparece en la lista con su código, y lo
  elijo. Ahora la contrapartida: agrego la segunda línea, y en su cuenta busco la caja general, de donde sale el pago.
  Aparece en la lista; la selecciono, y en el crédito anoto los mismos cuatro mil. Al pie aparece el aviso del presupuesto, en rojo: no se podrá contabilizar. Dice la cuenta,
  el centro y el período; el disponible, dos mil; lo que pide este documento, cuatro mil; y el faltante, dos mil. Guardo
  el borrador. Arriba, Contabilizar queda deshabilitado, con el motivo al lado: Bloqueado por presupuesto.""",
  [clic("button:has-text('Crear Asiento')", "pulso Crear Asiento"),
   esc("textarea[formcontrolname='description']", "Flete adicional de noviembre", "Escribo la\n  descripción".replace("\n  ", " ")),
   clic("button.add-line-button", "agrego la primera línea"),
   esc(L % 0 + "input[placeholder='Buscar cuenta...']", "Fletes", "En la cuenta busco"),
   clic("mat-option:has-text('6.03.10')", "la elijo, y en su débito"),
   esc(L % 0 + "input[formcontrolname='debitAmount']", "4000", "anoto cuatro mil pesos"),
   esc(L % 0 + "input[placeholder='Centro de costo...']", "Log", "escribo Log"),
   clic("mat-option:has-text('CC-LOG')", "lo\n  elijo".replace("\n  ", " ")),
   clic("button.add-line-button", "agrego la segunda línea"),
   esc(L % 1 + "input[placeholder='Buscar cuenta...']", "Caja gen", "busco la caja general"),
   clic("mat-option:has-text('1.01.01.01.02')", "la selecciono, y en el"),
   esc(L % 1 + "input[formcontrolname='creditAmount']", "4000", "anoto los mismos"),
   res("app-ledger-budget-notice .note", "el aviso del presupuesto", 5000),
   res("app-ledger-budget-notice li >> nth=0", "Dice la cuenta", 11000),
   clic("button:has-text('Guardar')", "Guardo el borrador"),
   {"resaltar": ".mat-mdc-snack-bar-container", "durante_ms": 2000, "cursor": False},
   res("span.post-blocked-reason", "Bloqueado por presupuesto", 4000)],
  navegar="/accounting/registro/diario"),
 paso("04-compras", "Compras y qué hacer", "El control en Compras", "Compras › Órdenes › COM-2026-000001",
  "Requisición · orden · factura · asiento",
  """El mismo control actúa en Compras: al aprobar una requisición o una orden de compra, y al emitir una factura.
  Esta es la orden de fletes que tenía comprometidos los tres mil pesos: mientras no se facture, sigue consumiendo
  disponible. Cuando el presupuesto bloquea, hay dos salidas: ajustar el documento, o pedir que se modifique el
  presupuesto. Y con la política Avisar, el documento habría pasado, dejando constancia y un aviso en la campanita del
  responsable. Así el presupuesto deja de ser un informe, y pasa a ser un control.""",
  [res(":text('COM-2026-000001') >> nth=0", "Esta es la orden de fletes", 6000),
   res("app-cost-center-field, :text('Centro de costo') >> nth=0", "sigue consumiendo", 4000),
   res(":text('Aprobad') >> nth=0", "hay dos salidas", 7000),
   res("button.mat-mdc-menu-trigger:not(.topbar-user) >> nth=0", "un aviso en la campanita", 5000, True)],
  navegar="/purchases/purchase-orders/view/1"),
]
guardar("contabilidad-45-control-presupuestario", g, pasos)
