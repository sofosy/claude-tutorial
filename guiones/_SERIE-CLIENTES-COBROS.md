# Serie «Clientes» (7 videos) y «Cobros» (7 videos) · plan · 2026-10-23

Fuente de los hechos: lectura del código de `germiva-website` y `Germiva-api` (rama `master`, API `fb521b9`)
y de `docs/base-conocimiento/ventas/07`, `09`, `docs/qa/QA-CLIENTES-*`, `docs/qa/QA-COBRO-VARIAS-FACTURAS-DEV.md`.
Todo lo que la voz afirme se comprueba en la pantalla viva durante el ensayo. Lo no comprobado se marca **[I]**.

## Clientes (`clientes-NN-*.json`, estado de partida `seeds/clientes/preparar.sh <estado>`)

| # | Video | Qué enseña | Escenarios |
|---|---|---|---|
| 01 | `01-pantalla` | La pantalla Ventas › Clientes: qué es un cliente, columnas (Cuenta / sucursal, Razón social, Zona, Vendedor asignado, Nombre, Documento, Categoría, Etiquetas), buscar por nombre o RNC, filtros Zona/Categoría/Etiqueta, Estado de Cuenta | listado |
| 02 | `02-empresa-con-rnc` | Alta de una empresa con RNC: consulta al padrón DGII, razón social vs nombre comercial, Categoría, Actúa como, Tipo de cliente, lista de precios, Tipo de NCF por defecto, guardar y aviso de la dirección de facturación | RNC en padrón |
| 03 | `03-contactos-y-direcciones` | Pestañas Contactos y Direcciones (aparecen al guardar): agregar contacto y dirección de facturación, por qué importa (E46 / IR-2) | contactos, direcciones |
| 04 | `04-persona-extranjero-informal` | Persona con cédula, contribuyente informal, documento extranjero, Consumidor Final (no se crea ni se archiva), cliente + proveedor en una ficha, bloqueo de duplicado | casos especiales |
| 05 | `05-mismo-rnc-sucursales` | **Varias cuentas con el mismo RNC**: cuándo sí (sucursales con cartera, vendedor, zona y precios propios) y cuándo no (duplicado por error); 2.ª y 3.ª cuenta; aviso «Este RNC ya tiene N cuentas»; razón social compartida; código de cuenta C-000001; nombre comercial único; lo que queda bloqueado; «Corregir identidad fiscal compartida» | RNC compartido |
| 06 | `06-sucursales-en-documentos` | Lo mismo en el día a día: elegir la sucursal en una factura, «Crear otra sucursal con este RNC» desde la factura, la factura imprime código · nombre comercial + razón social + RNC, cada cuenta con su estado de cuenta (los cobros no se cruzan entre sucursales) | factura, estado de cuenta |
| 07 | `07-archivar-e-importar` | Archivar y restaurar, Ver archivados; Importar / Exportar con `codigo_cuenta` y `razon_social` | archivar, masivo |

## Cobros (`cobros-NN-*.json`, estado `seeds/cobros/preparar.sh <estado>`)

| # | Video | Qué enseña | Escenarios |
|---|---|---|---|
| 01 | `01-pantalla` | Ventas › Cobros: Recibo, Fecha, N° Factura, Cliente, Monto, Estado (Vigente/Anulado), Método; filtros Tipo/Cliente; los dos botones; el detalle del cobro | listado |
| 02 | `02-cobrar-una-factura` | Registrar cobro de UNA factura: transferencia total; abono parcial (la factura queda parcialmente pagada); efectivo con vuelto | total, parcial, efectivo |
| 03 | `03-pago-combinado` | Pago combinado (efectivo + tarjeta en un recibo): cuándo ocurre; tope de siete pagos por factura | varios métodos |
| 04 | `04-retenciones` | El cliente retiene ITBIS/ISR: se cobra el efectivo y la retención salda el resto; el aviso de retención ya declarada en la factura | retención |
| 05 | `05-varias-facturas` | **Un solo pago que salda varias facturas**: cuándo ocurre; Cobrar varias facturas, cliente, datos del pago, Sugerir reparto (más antiguo primero), completas y parcial, Recibido / Aplicado / Por ubicar, confirmar, recibo, detalle | liquidación base |
| 06 | `06-varias-facturas-variantes` | Otras configuraciones de la liquidación: repartir a mano según el recibo del cliente, dejar una factura sin tocar, con retenciones y descuento por pronto pago, cheque / depósito / efectivo / tarjeta, rechazos (sobra o falta dinero, supera saldo), cobro duplicado, **casa matriz que paga por sucursales** (no mezcla cuentas: una liquidación por cuenta) | variantes y errores |
| 07 | `07-corregir-y-reversar` | Reversar un cobro (motivo, el recibo no se edita), Corregir reparto de una liquidación, candado de anular una factura cobrada junto con otras | reverso, corrección |

Anticipos (registrar y aplicar a factura) quedan para una serie aparte: no se pidieron y tienen sus propias reglas.

## Reglas de la serie
- Voz `es-DO-EmilioNeural` (edge-tts; no hay clave de ElevenLabs en esta máquina). Las series anteriores usan ElevenLabs: el timbre cambia.
- Datos de demo con «Germiva» y RNC `130555xxx`, como la serie Vendedores.
- Un video no se publica si `revisar.mjs` o `veredicto.mjs` dan error.
