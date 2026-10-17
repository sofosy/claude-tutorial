# Informe del autor — `cajas-08-cobro-factura` · «Cobrar una factura con pago combinado» (2026-09-23)

## Quién graba y por qué
**`admin.progreso`**, con SU sesión abierta en Caja Principal. La cajera no sirve hoy: al abrir cualquier
factura le sale «Acceso Denegado — Ver Historial de Versiones de Facturas» (H-16). La historia no cambia:
el cobro entra a la caja abierta de quien cobra (`cashier-session-access.service.ts:157-192`).

## Estado de partida: **S8**
S1 + **plan 15** en la suscripción de la empresa 43 + factura **1000000001** de CONTADO en **BORRADOR**
(B01, «Constructora Los Pinos», 10 × cemento a 450 + 20 × varilla a 150 = 7,500 + ITBIS 1,350 =
**RD$8,850.00**) + sesión del admin en Caja Principal con fondo 5,000.
- Preparar: `node seeds/cajas/preparar-s8.mjs` → `node seeds/cajas/fijar.mjs S8` → `node seeds/cajas/plan-s8.mjs off`.
- Entre tomas: `node seeds/cajas/restaurar.mjs S8` (deja el plan 15).
- **Después de ensayar o grabar el video 8: `node seeds/cajas/plan-s8.mjs off`**. S0…S6 no guardan la
  suscripción, así que no devuelven el plan 2 por sí solos. Con el plan 15 cambia el riel de los tres roles.
  El ensayo (`ensayo-v8.mjs`) ya lo hace; `grabar-serie.sh` no.
- Por qué el plan 15: con el plan 2 abrir la factura lanza «Módulo No Disponible» (H-17). El 15 es el plan que se
  pidió al crear la demo (`_DATOS` §0.1).
- Por qué un borrador de contado y no una factura emitida: en el listado, una factura emitida solo ofrece
  «Ver Detalles», que es de solo lectura y no tiene cobro (H-20). «Cobros › Registrar cobro» dice «Pago directo
  (sin caja)», que es falso (H-21). El borrador se abre con el lápiz «Editar» y se cobra con «Guardar y
  Cobrar»; el NCF se asigna al cobrar.
- Probado: `restaurar S8` ×2 después de cobrar (API y UI), S1→S8, S8→S0 (factura, productos y pagos a 0;
  plan 2).

## Qué escribe la toma
Factura → PAGADA con NCF B0100000001. Recibo RCP-2026-000001 con 2 líneas: efectivo 5,000 y tarjeta Visa ••••4821
(autorización 738214, ficticios). Además: CxC, asientos, `cash_counts` (5,000 / 3,850), secuencias y auditoría.
Todo lo cubre `_estado.mjs`, ampliado solo con tablas nuevas: products, prices, price_history, product_history,
invoices, invoice_details, invoice_tax_group, invoice_versions, entity_versions, accounts_receivable,
ar_payment_history, payment_applications, payments, payment_details, payment_changes, ncf,
customer_timeline_events (en S0…S6 la 43 tiene 0 filas en todas), `secuentials` y `subscriptions` (solo-update).
Abrir «Cuadre» y pulsar «Volver» no escribe nada (medido).
Maestro que persiste y no se restaura: el cliente «Constructora Los Pinos» (RNC ficticio 130555079).

## Guion
4 pasos: 01 Tu caja y la factura · 02 Cobrar con pago combinado · 03 La factura pagada · 04 Cómo se refleja
en la caja. Duración prevista **3:48** (más 6 s de marca). Las cifras de la voz son las de pantalla:
- Mi caja antes: esperado 5,000.
- Pago: 5,000 + 3,850; «Falta» 3,850 y luego 0.
- Factura: pagado 8,850, pendiente 0.
- Mi caja después: cobros en efectivo 5,000 y esperado 10,000.
- Cuadre: «Cobros del turno» 8,850, Efectivo 10,000, Tarjeta 3,850.

Siglas explicadas la primera vez: NCF, DGII, ITBIS y B01, con su fonética en `pronunciacion`. El diálogo
«Cobro procesado» tarda unos 6 s: se marca sin ancla y se cierra con «Aceptar».

## Puertas
- `tut.py verificar`: **0 errores, 0 avisos**.
- `revisar.mjs`: **0 ERROR, 1 AVISO justificado**. El paso 01 no contrae el menú porque arranca en Cajas (riel
  fijo, sin panel). El panel de Ventas se contrae en el paso 02 (`button.panel-collapse`).
- Ensayo bajo `NAVEGADOR.lock` con restauración antes y después (`seeds/cajas/ensayo-v8.mjs`, 2 corridas):
  **4 pasos, 51 acciones OK, 0 fallos**, todas «visible=entero». Log con líneas `── paso` en
  `salida/cajas-08-cobro-factura/ensayo/ensayo.log`.
- Capturas del ensayo revisadas:
  - La 02 sale en blanco: la página se recarga al pulsar «Aceptar». El paso 03 abre con una frase de relleno
    («Al aceptar, la factura se vuelve a cargar…»).
  - Riesgo de la toma: si la recarga tarda más de 2 s, la primera marca del paso 03 llega tarde. Mirar ese
    punto en el veredicto.

## AVISOS y cosas que la voz no enseña como correctas
- La columna ESTADO vacía de la pestaña «Pagos» (H-18) no se señala.
- El «Este dato es requerido» rojo que queda después del último método (H-19) se nombra en la voz: «el formulario
  de arriba se vacía, listo para otro método, pero ya no hace falta».
- «Total esperado en caja» 13,850 (H-22) no se nombra.
- La franja naranja «Facturación electrónica deshabilitada» de la factura es informativa y fija. No es un aviso
  emergente y no se comenta.

## Hallazgos nuevos
Van al final de `_HALLAZGOS-CAJAS.md`, del H-16 al H-22. Los que bloqueaban el video: H-16, H-17, H-20 y H-21.

## Archivos
- `guiones/cajas-08-cobro-factura.json`
- `guiones/_INVENTARIO-COBRO-FACTURA.md`
- `guiones/_DATOS-CAJAS.md`: fila S8.
- `guiones/_HALLAZGOS-CAJAS.md`
- `seeds/cajas/`:
  - Scripts nuevos: `preparar-s8.mjs`, `plan-s8.mjs`, `ensayo-v8.mjs`, `con-cerrojo.mjs`, `explorar_v8*.py`.
  - `_estado.mjs` ampliado.
  - `estados/S8.sql` y `estados/S8.json`.
- `guiones/exploracion-cajas/v8*-*`.
