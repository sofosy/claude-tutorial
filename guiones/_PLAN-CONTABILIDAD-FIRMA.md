# Plan · Tanda «Catálogo de la firma», «Multimoneda» y «Retenciones» (serie Contabilidad)

Pedido del usuario (2026-10-18): los videos de Contabilidad no explican cómo una firma
contable establece el catálogo de cuentas por defecto de los clientes que crea, ni las
posibilidades que se le dan:

- la firma cambia el catálogo de un cliente suyo;
- la firma crea un catálogo propio como plantilla, disponible solo para sus clientes;
- la firma lo pone por defecto al crear sus clientes;
- y las demás combinaciones que el sistema permita (ver la investigación).

Segundo pedido (2026-10-18, mismo día): aclarar todo el proceso de las empresas que
trabajan con más de una moneda: cómo se configura la diferencia cambiaria y sus cuentas,
y cómo se ven los estados de una operación multimoneda en USD y en DOP. Antes de
guionar se valida lo que ya cubren los videos 01–27 y se agrega solo el complemento, en
orden lógico.

Tercer pedido (2026-10-18): videos sobre las retenciones de ISR e ITBIS y la carta de
retención, investigando bien el tema en el repo.

Además, con `DUMP_URL_PROD` ya configurada, se valida contra la copia de PROD lo que se
unió en el lote 2 (api#1563, web#1409).

Ramas y repos:
- **claude-tutorial** (`claude/cool-johnson-q9dpzp`): este plan, guiones, semillas y videos.
- **Germiva-api** y **germiva-website**: `feature/contabilidad-catalogo-firma-clientes` para el
  bloque A ([api#1569](https://github.com/sofosy/Germiva-api/pull/1569),
  [web#1416](https://github.com/sofosy/germiva-website/pull/1416)); los arreglos de
  multimoneda y de retenciones van en ramas propias (`fix/contabilidad-multimoneda`:
  [api#1575](https://github.com/sofosy/Germiva-api/pull/1575), [web#1419](https://github.com/sofosy/germiva-website/pull/1419);
  `fix/fiscal-retenciones`: [api#1574](https://github.com/sofosy/Germiva-api/pull/1574),
  [web#1418](https://github.com/sofosy/germiva-website/pull/1418)) para que cada PR se revise solo.
- Cada tarea terminada sale en su propio commit, y este plan se actualiza en el mismo commit.

**Regla de datos (pedido del usuario):** los videos usan SOLO datos y escenarios creados
para el tutorial (base sembrada + `seeds/contabilidad/preparar.py`, nombres «Germiva»,
RNC 130555xxx). La copia de PROD sirve únicamente para validar cambios y se borra al
terminar; nunca aparece en un video.

## Tareas

| # | Tarea | Estado |
|---|-------|--------|
| 1 | Validar contra la copia de PROD lo unido en el lote 2 (migraciones, historial de transferencias, sugerencias de conciliación, centros de costo, búsqueda de períodos) y borrar la copia (`down.sh --all`) | Hecho |
| 2 | Investigar en el código y el manual cómo funciona el catálogo de la firma para sus clientes (dónde se fija el predeterminado, qué pasa al crear un cliente, cambiar el catálogo de un cliente, plantilla propia visible solo a sus clientes) | Hecho |
| 2b | Investigar multimoneda: monedas y tasa del día, diferencia cambiaria realizada y no realizada (configuración y cuentas), revaluación, estados en USD y en DOP; qué cubren ya los videos 01–27 | Hecho |
| 2c | Investigar retenciones de ISR e ITBIS y la carta de retención: configuración, compras, ventas (las que nos hacen), asientos, 606/IR-17/IT-1, emisión de cartas; qué cubren ya los videos | Hecho |
| 3 | Definir la lista de videos de la tanda (numeración 28 en adelante) y los datos de partida (firma + clientes) | Por hacer |
| 4 | Corregir los defectos que aparezcan (API y web), con pruebas | Hecho: firma (api#1569, web#1416), multimoneda (api#1575, web#1419), retenciones (api#1574, web#1418) |
| 5 | Semilla: estados nuevos en `seeds/contabilidad/preparar.py` (firma, firma-plantilla, firma-alta, firma-cambio, firma-asistente; luego multimoneda y retenciones) | En curso: los de la firma, hechos |
| 6 | Guionar, revisar, ensayar y grabar cada video (un commit por video) | En curso: 28–33 guionados; 28–30 a regrabar (ritmo); 31–33 ensayados |
| 7 | Manual de Contabilidad y de la Cuenta, catálogo de videos, textos para YouTube | En curso: manual y definición de la experta hechos (api#1569); faltan catálogo de videos y textos de YouTube |
| 8 | REU: fichas que la tanda toque o deje abiertas | Hecho: DP-124 a DP-138 (DP-135 a DP-138 renumeradas por choque con comisiones), DP-016, DP-005 y DP-002 al día |
| 9 | Validación final contra PROD si el cambio toca migraciones o contabilidad; `down.sh --all` y verificación vacía | Por hacer |
| 10 | PR a master/main con CI en verde | Hecho para los arreglos: los 6 PR unidos a master con CI en verde (2026-10-18). Pruebas completas del API sobre la unión: 10 991 en verde; 7 fallos, todos de archivos que ya fallan en master o que pasan solos. Falta el PR de los videos (claude-tutorial) al final |

## Videos

### Bloque A · El catálogo de la firma y sus clientes (borrador)

| # | Video | Qué enseña | Estado |
|---|-------|-----------|--------|
| 28 | La firma fija el catálogo de sus clientes | Mi Cartera › Mi firma › «Catálogo de cuentas de sus clientes» › «Plantilla por defecto» › «Guardar plantilla»; los clientes actuales no cambian; en cada alta se puede elegir otra | Grabando |
| 29 | La plantilla propia de la firma | Desde el catálogo de la firma (o de un cliente ya trabajado): «Crear plantilla desde mi catálogo» con alcance «Mi firma contable»; quién la ve; ponerla por defecto | Grabando |
| 30 | Dar de alta un cliente con su catálogo | Nuevo cliente › «Para un cliente» › «Dar de alta a un cliente nuevo» › «Catálogo de cuentas» (viene la de la firma, se puede elegir otra) › el cliente nace con catálogo propio y la marca «Origen» | Grabando |
| 31 | Cambiar el catálogo de un cliente | Cliente sin asientos (catálogo propio, tras el arreglo F1) y cliente invitado con catálogo compartido que adopta la plantilla de la firma; quién puede hacerlo | Por hacer |
| 32 | Cambio de catálogo con asientos | El asistente de correspondencia: qué va a pasar, cuenta por cuenta, fecha de corte, asiento de reclasificación | Por hacer |
| 33 | Mantener las plantillas | Plantillas incompletas, importar una plantilla desde archivo, eliminar una plantilla de la firma | Por hacer |

### Bloque B · Empresas con más de una moneda (borrador)

Qué ya existe: el **06 Revaluación** es el único video multimoneda (corre la revaluación de
cierre y explica el asiento). El 08 menciona la casilla «Monetaria» (con una promesa que el
sistema no cumple, ver M4) y el 22 dice que una transferencia exige la misma moneda. Nada
enseña a registrar la tasa, configurar las cuentas de diferencia cambiaria ni operar en USD.

Orden lógico (el 06 queda como pieza de cierre entre el 37 y el 38):

| # | Video | Qué enseña | Estado |
|---|-------|-----------|--------|
| 34 | Monedas y tasa del día | «Monedas disponibles»: moneda local (DOP, fija) y moneda por defecto; registrar la tasa del día; el aviso «Falta la tasa del día»; «Histórico de Tasas»; qué tasa toma cada documento | Por hacer |
| 35 | Las cuentas de diferencia cambiaria | Orden en que se buscan: por moneda (NET/GROSS) › cuentas generales › roles «Multimoneda» del mapeo; las cuentas que trae cada plantilla; qué pasa si faltan | Por hacer |
| 36 | Vender y cobrar en dólares | Cuenta bancaria en USD, factura en USD a 58.75, cobro a 59.50: el asiento con la ganancia cambiaria realizada (DR Banco 59,500 / CR CxC 58,750 / CR Ganancia 750) | Por hacer |
| 37 | Comprar y pagar en dólares | Factura de proveedor en USD y pago a otra tasa: la pérdida cambiaria; anticipo a proveedor en USD | Por hacer |
| 06 | (existente) Revaluación de cierre | Se mantiene; el 38 lo complementa | Hecho |
| 38 | La revaluación por dentro | Abrir el asiento de revaluación (CxC, CxP y bancos), el asiento «-POST» de lo cobrado después del corte y anular una revaluación | Por hacer |
| 39 | Ver la operación en USD y en DOP | Qué muestra cada pantalla: la factura (USD y su equivalente), cartera y antigüedad por moneda, estado de cuenta del cliente y del proveedor por moneda, saldo del banco en USD, y los estados financieros siempre en DOP (tasa histórica + revaluación) | Por hacer |

### Bloque C · Retenciones de ISR e ITBIS y la carta de retención (borrador)

Qué ya existe: nada. Ningún video toca las retenciones ni la carta (el «demo-contadores»
solo nombra el IR-17 de pasada) y ninguna semilla las crea. Los arreglos van en
`fix/fiscal-retenciones`.

| # | Video | Qué enseña | Estado |
|---|-------|-----------|--------|
| 40 | Las retenciones en Germiva | Las que practicas a tus proveedores y las que te hacen tus clientes; la consola «Retenciones e Impuestos»; «Tipos de Retención» y su historial de tasas (Ley 30-26: manda la fecha del comprobante) | Por hacer |
| 41 | Las cuentas de las retenciones | Mapeo «Retención ITBIS/ISR por pagar» y «… a favor», cuentas por tipo, qué pasa si falta una | Por hacer |
| 42 | Comprar a una persona física | Servicio de una PF (E31/B01): ITBIS 100 % e ISR 15 % sugeridos, el modal por línea, el neto a pagar y el asiento | Por hacer |
| 43 | Comprar a una empresa y el Comprobante de Compras | ITBIS 30 % de servicios a una sociedad, los avisos de la matriz por comprobante, E41 a un informal con «Proponer retenciones» | Por hacer |
| 44 | Corregir una retención | «Corregir retenciones» en una compra ya registrada, y las retenciones del Buzón | Por hacer |
| 45 | Pagar y declarar | Pagar al neto; el 606 (fecha de pago, ITBIS retenido, tipo y monto de ISR); el IR-17 y la sección A del IT-1 | Por hacer |
| 46 | Las retenciones que te hacen tus clientes | En la factura, al cobrar («Retenciones del cliente») o en «Retenciones recibidas»; el asiento «a favor»; el 607 y el IT-1; nunca registrar la misma dos veces | Por hacer |
| 47 | Preparar la carta de retención | Firma, sello y membrete en Mi Empresa; «Firma y destinatario» | Por hacer |
| 48 | Emitir las cartas de retención | Mes o año completo, estados de cada proveedor, vista previa, emitir y «Emitir pendientes»; recorrido del PDF | Por hacer |
| 49 | Enviar, anular y reemitir | Envío por correo, anular con motivo, «desactualizada» → reemitir; el bloqueo al reversar un pago certificado | Por hacer |

## Validación contra PROD (lote 2) — 2026-10-18

Copia anonimizada de PROD cargada con `up.sh --source prod`: todas las migraciones
pasaron. Probado por el API con un usuario de las empresas 69 (la de más asientos) y 40
(la de más cuentas bancarias):

- `GET /v1/bank-account-transfers`: 200 (PROD no tiene transferencias entre cuentas).
- `GET /v1/cost-centers/hierarchy` y `/active`: 200, solo los centros de la empresa.
- Búsqueda de períodos con varias palabras: «Diciembre 2026» trae solo ese período,
  «2026» los doce del año, «fiscal 2026» solo el período fiscal de la 69.
- Flujo de efectivo y balanza de comprobación de 2025: 200.
- `GET /v1/bank-reconciliation`: 200. Las sugerencias con asientos no se pudieron
  ejercitar: PROD no tiene conciliaciones.

Copia borrada con `down.sh --all`; `docker ps -a | grep germiva-dev` salió vacío.

## Hallazgos

- **H1 (PROD):** 16 empresas tienen `chart_template_id` vacío (75–80, 90, 94, 99,
  102–104, 109, 124, 127, 134); 10 de ellas tienen un vínculo ACTIVO con una firma. Hoy
  ven el catálogo de la plantilla marcada por defecto (GERMIVA_BASE), porque el sistema
  cae a ella cuando falta, pero si la plantilla por defecto cambiara, cambiarían de
  catálogo sin que nadie lo decida. Por confirmar en la investigación: el alta de
  clientes desde la firma guarda `chartTemplateId ?? null`.
- **Investigación del catálogo de la firma (tarea 2).** Decisión por hallazgo: *Arreglar*
  (en esta tanda, con pruebas) o *REU* (decisión de negocio).

| # | Hallazgo | Decisión | Estado |
|---|----------|----------|--------|
| F1 | Los clientes que crea la firma nacen con catálogo propio y después NO se les puede cambiar de plantilla, ni siquiera sin asientos (`assertSharedCatalog`) | Arreglar: permitir el cambio libre en catálogo propio mientras no haya asientos | Hecho (api#1569, web#1416) |
| F2 | Una plantilla de la firma ya usada no se puede eliminar: cuenta también a los clientes con catálogo propio, que ya no dependen de ella, y el mensaje pide «cámbielas de catálogo», imposible para ellos | Arreglar | Hecho (api#1569) |
| F3 | Eliminar una plantilla deja colgado el catálogo por defecto de la firma (borrado suave: el `ON DELETE SET NULL` no corre) y la próxima alta falla | Arreglar | Hecho (api#1569) |
| F4 | Crear empresa por `CreateCompanyDto.chartTemplate` acepta plantillas de OTRA firma y plantillas incompletas | Arreglar | Hecho (api#1569) |
| F5 | El alcance «Mi firma contable» solo lo esconde la web: el API deja crear plantillas de firma a cualquiera | Arreglar | Hecho (api#1569) |
| F6 | En la empresa de la firma, sus propias plantillas salen como «De mi contador» | Arreglar | Hecho (web#1416) |
| F7 | La plantilla de firma es de un USUARIO (`owner_user_id`), no de la firma: si ese contador sale de la firma, la plantilla deja de poder elegirse | REU | Por hacer |
| F8 | Dos tablas de pertenencia distintas para la misma pregunta (`user_companies` al elegir, `user_company_roles` al ver) | Revisado: no es una inconsistencia (una pregunta es «¿es miembro de la firma?», la otra «¿está vinculado a esta empresa?») | No aplica |
| F9 | El acceso «Contabilidad e Impuestos» (rol Contador) no puede cambiar el catálogo de un cliente (le falta `ACCOUNTING_INTEGRATION_CONFIGURE`) | REU | Por hacer |
| F10 | Las empresas que nacen de una solicitud de certificación y las «Para mi firma» no reciben la plantilla de la firma ni catálogo propio | REU | Por hacer |
| F11 | Sin plantilla por defecto en la firma, el alta guarda `chart_template_id = NULL` en vez de la del sistema (ver H1) | Arreglar (altas nuevas) + REU (saneo de las 16 de PROD) | Hecho en altas nuevas (api#1569); saneo de PROD al REU |
| F12 | «Crear plantilla desde mi catálogo» con catálogo compartido ignora los nombres propios de la empresa y copia cuentas ocultas | Arreglar | Hecho (api#1569) |
| F13 | Una plantilla incompleta no se puede completar en el sitio (no hay edición de roles) | REU | Por hacer |
| F14 | Reusar el código de una plantilla eliminada da un error genérico de duplicado | Arreglar | Hecho (api#1569) |
| F15 | El cambio con asientos no es atómico (la plantilla nueva y el asiento se confirman antes del paso 3) y no reapunta referencias ni resiembra cuentas por impuesto | Verificar y arreglar | Hecho el reapunte y el resembrado (api#1569); la atomicidad del asiento queda anotada |
| F16 | Errata «o dela de alta» en el diálogo de Nuevo cliente | Arreglar | Hecho (web#1416) |
| F17 | Tú y usted mezclados en Plantillas de Catálogo, el asistente y mensajes del API | Arreglar en las pantallas de la tanda | Hecho en Plantillas, asistente, catálogo y Nuevo cliente (web#1416) |
| F18 | Manual desfasado: CAT-01 (nombres viejos de plantillas), CAT-13/OBJ-22 (ruta del alta), OBJ-22 (cambio para clientes con catálogo propio), CTD-06 (falta el campo «Catálogo de cuentas») | Arreglar | Por hacer |
| F20 | Al dar de alta (o invitar) a un cliente, la Cartera lo listaba pero «Clientes activos» seguía en 0 hasta 5 minutos: el caché del resumen no se invalidaba nunca | Arreglar | Hecho (api#1569) |
| F19 | El video 09 dice que una plantilla «Solo esta empresa» sirve «de base en otra empresa», y el diálogo promete lo mismo: solo es cierto para las de firma | Arreglar el texto y regrabar el 09 | Hecho el texto (web#1416); falta regrabar el 09 |

- **Investigación multimoneda (tarea 2b).** Los arreglos van en `fix/contabilidad-multimoneda`.

| # | Hallazgo | Decisión | Estado |
|---|----------|----------|--------|
| M1 | Vista 360: la tarjeta de un banco en USD suma líneas USD y DOP (y borradores) y luego multiplica por la tasa de hoy; «Total bancos» no cuadra con el efectivo | Arreglar | Hecho (api#1575, web#1419) |
| M2 | El estado de cuenta del proveedor mezcla monedas con el total rotulado «RD$»; la búsqueda del proveedor no filtra por empresa | Arreglar | Hecho (api#1575, web#1419) |
| M3 | Conciliación: comisiones e intereses de una cuenta en USD se contabilizan como pesos, sin convertir; las sugerencias comparan USD contra DOP | Arreglar | Hecho (api#1575, web#1419) |
| M4 | La casilla «Monetaria» promete revaluar cualquier cuenta y solo excluye bancos (préstamos y caja en USD no se revalúan) | Corregir el texto + REU (revaluar cuentas monetarias) | Hecho el texto (api#1575, web#1419); revaluar otras cuentas → REU |
| M5 | Mensajes que mandan a registrar la tasa en «Histórico de Tasas», que es de solo lectura; ninguna pantalla registra una tasa con fecha pasada | Arreglar mensajes + evaluar fecha en el registro | Hecho (api#1575, web#1419) |
| M6 | «Configuración multi-moneda»: ayuda falsa («el asiento queda desbalanceado»), errores de carga tragados, permiso del menú | Arreglar | Hecho (api#1575, web#1419) |
| M7 | Las cuentas generales de diferencia cambiaria se guardan sin validar empresa, catálogo ni que admitan movimiento | Arreglar | Hecho (api#1575, web#1419) |
| M8 | `getRate` sin empresa lee tasas de todas; el GET de revaluaciones sin guardia de empresa; se acepta tasa 0 | Arreglar | Hecho (api#1575, web#1419) |
| M9 | Inglés en asientos y pantallas: «Pago CASH», «AccountReceivable#123», «Default», «NET/GROSS», «Posteada» | Arreglar | Hecho (api#1575, web#1419) |
| M10 | Diálogos de pago con `'DOP'` fijo en vez de la moneda local de la empresa | Arreglar si es local | Hecho (api#1575, web#1419) |
| M11 | Una revaluación sin saldos queda «Posteada» y bloquea esa fecha; sin cuentas configuradas, falla aunque no haya saldos | Arreglar | Hecho (api#1575, web#1419) |
| M12 | Diario y Mayor: las filas muestran el importe en USD y los totales en DOP, sin columna de moneda | Arreglar | Hecho (api#1575, web#1419) |
| M13 | Sin asiento manual en USD en pantalla, sin anticipos de cliente en USD, sin compra de dólares (transferencia entre monedas) | REU (funcionalidad nueva) | Por hacer |

- **Investigación de retenciones (tarea 2c).** Los arreglos van en `fix/fiscal-retenciones`.

| # | Hallazgo | Decisión | Estado |
|---|----------|----------|--------|
| G1 | La carta dice que lo retenido se declaró en el IR-17/IT-1 del mes del PAGO, pero el IR-17 y el IT-1 de Germiva lo ponen en el mes de la FACTURA | REU (decide el contador) | Por hacer |
| G2 | «Monto pagado» de la carta ignora ISC, otros impuestos y propina | Arreglar | Hecho (api#1574, web#1418) |
| G3 | Reimprimir una carta no da el mismo documento: logo, membrete, firma y sello se leen al descargar | Arreglar | Hecho (api#1574, web#1418) |
| G4 | El código de verificación no se puede consultar en ninguna parte | REU (funcionalidad nueva) | Por hacer |
| G5 | Cambios que no marcan la carta (solo el tipo en «Corregir retenciones», cambiar la fecha del pago); la reemisión no es atómica | Arreglar | Hecho (api#1574, web#1418) |
| G6 | Probable: las retenciones de una compra estándar caen también en «Retenciones recibidas» | Verificar y arreglar | Hecho (api#1574, web#1418) |
| G7 | Sin período abierto, la retención de la compra se omite en silencio | Arreglar | Hecho (api#1574, web#1418) |
| G8 | 606, casilla 17: el código 4 (rentas presuntas) nunca se usa | REU (decide el contador) | Por hacer |
| G9 | Cualquier empresa puede editar o eliminar un tipo de retención del catálogo global | Arreglar | Hecho (api#1574, web#1418) |
| G10 | «Firma y destinatario» visible con solo ver (guardar da 403); «Retenciones practicadas» pide un permiso distinto al del API | Arreglar | Hecho (api#1574, web#1418) |
| G11 | La retención al cobrar acepta montos negativos | Arreglar | Hecho (api#1574, web#1418) |
| G12 | Código sin uso: `retention-operations`, «Agente Fiscal», el formulario de retención por proveedor (sin pantalla), el viejo «generar certificado» | REU (limpieza) | Por hacer |
| G13 | NG 02-2026 (sin ITBIS 30 % a quien factura con e-CF) no está aplicada; la matriz corre en modo aviso | REU (ya pendiente) | Por hacer |
| G14 | Tú y usted en un mismo mensaje («Indique … Selecciona …») | Arreglar | Hecho (api#1574, web#1418) |
| G15 | Inglés que llega al usuario («Invoice … not found», estado «applied») | Arreglar | Hecho (api#1574, web#1418) |
| G16 | Textos erróneos («no puede ser negativa», «Retención sobre el ISR del documento», ejemplo 18 en Swagger) | Arreglar | Hecho (api#1574, web#1418) |
| G17 | Nombres desfasados («Contabilidad › Fiscal», «Archivos de marca», «certificado» vs «carta», cita a DP-096) | Arreglar | Hecho (api#1574, web#1418) |
| G18 | El manual fiscal no tiene la carta de retención; compras manda a buscarla allí | Arreglar | Hecho (api#1574, web#1418) |

- **PROD, contexto:** 20 firmas aprobadas, ninguna con catálogo por defecto
  (`default_chart_template_id`); solo existen las 3 plantillas del sistema (ninguna
  propia de una firma); 125 empresas usan GERMIVA_BASE, 5 RD_AMPLIADO y 1 RD_UNIFICADO;
  3 tienen catálogo propio (`chart_mode = OWN`).
- **Motor de grabación:** la sesión del login se volvía a inyectar en cada carga completa de la
  página, así que cambiar de empresa dentro de un video (que recarga la app) volvía a la empresa
  del login. Ahora se inyecta una sola vez por pestaña (`tutorial/capturar.py`).
- **Retenciones, pendientes que dejó el arreglo:** las compras emitidas antes de G6 pueden tener
  filas en `tax_withholdings` (`TW-<factura>-ITBIS|ISR`) que inflan el IR-2 y «Retenciones
  recibidas» (saneo → REU); las cartas ya emitidas con ISC, propina o percepciones saldrán
  «desactualizadas» porque su «Monto pagado» estaba mal.
- **Multimoneda, decisiones que dejó el arreglo:** `allowPaymentCurrencyOverride` se guarda y
  nadie lo lee (quitar o implementar); la Vista 360 muestra el valor en libros en DOP, no a la tasa
  de hoy; una cuenta bancaria en USD sin cuenta contable se valora a la tasa de la última
  revaluación; la pantalla no registra una tasa con fecha pasada; la revaluación rotula «Ganancia
  DOP» / RD$ fijo. → REU.
- **Entorno:** `ng serve` (≈6 GB) cayó dos veces por falta de memoria con agentes trabajando en
  paralelo. Para grabar se sirve la compilación estática del frontend (poca RAM); se recompila
  cuando cambia el código de la web.
- **Entorno de grabación sobre master** (2026-10-18): API y web en `master` con los tres bloques de
  arreglos; la base de partida de los videos (`contabilidad-base.sql.gz`) se regeneró con las
  migraciones nuevas de master.

