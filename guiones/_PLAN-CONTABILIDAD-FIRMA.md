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

Ramas: `feature/contabilidad-catalogo-firma-clientes` en Germiva-api y germiva-website;
`claude/cool-johnson-q9dpzp` aquí. Cada tarea terminada sale en su propio commit, y
este plan se actualiza en el mismo commit.

## Tareas

| # | Tarea | Estado |
|---|-------|--------|
| 1 | Validar contra la copia de PROD lo unido en el lote 2 (migraciones, historial de transferencias, sugerencias de conciliación, centros de costo, búsqueda de períodos) y borrar la copia (`down.sh --all`) | Hecho |
| 2 | Investigar en el código y el manual cómo funciona el catálogo de la firma para sus clientes (dónde se fija el predeterminado, qué pasa al crear un cliente, cambiar el catálogo de un cliente, plantilla propia visible solo a sus clientes) | Hecho |
| 2b | Investigar multimoneda: monedas y tasa del día, diferencia cambiaria realizada y no realizada (configuración y cuentas), revaluación, estados en USD y en DOP; qué cubren ya los videos 01–27 | En curso |
| 2c | Investigar retenciones de ISR e ITBIS y la carta de retención: configuración, compras, ventas (las que nos hacen), asientos, 606/IR-17/IT-1, emisión de cartas; qué cubren ya los videos | En curso |
| 3 | Definir la lista de videos de la tanda (numeración 28 en adelante) y los datos de partida (firma + clientes) | Por hacer |
| 4 | Corregir los defectos que aparezcan (API y web), con pruebas, en las ramas `feature/contabilidad-catalogo-firma-clientes` | Por hacer |
| 5 | Semilla: estados nuevos en `seeds/contabilidad/preparar.py` para la firma y sus clientes | Por hacer |
| 6 | Guionar, revisar, ensayar y grabar cada video (un commit por video) | Por hacer |
| 7 | Manual de Contabilidad y de la Cuenta, catálogo de videos, textos para YouTube | Por hacer |
| 8 | REU: fichas que la tanda toque o deje abiertas | Por hacer |
| 9 | Validación final contra PROD si el cambio toca migraciones o contabilidad; `down.sh --all` y verificación vacía | Por hacer |
| 10 | PR a master/main con CI en verde | Por hacer |

## Videos

### Bloque A · El catálogo de la firma y sus clientes (borrador)

| # | Video | Qué enseña | Estado |
|---|-------|-----------|--------|
| 28 | La firma fija el catálogo de sus clientes | Mi Cartera › Mi firma › «Catálogo de cuentas de sus clientes» › «Plantilla por defecto» › «Guardar plantilla»; los clientes actuales no cambian; en cada alta se puede elegir otra | Por hacer |
| 29 | La plantilla propia de la firma | Desde el catálogo de la firma (o de un cliente ya trabajado): «Crear plantilla desde mi catálogo» con alcance «Mi firma contable»; quién la ve; ponerla por defecto | Por hacer |
| 30 | Dar de alta un cliente con su catálogo | Nuevo cliente › «Para un cliente» › «Dar de alta a un cliente nuevo» › «Catálogo de cuentas» (viene la de la firma, se puede elegir otra) › el cliente nace con catálogo propio y la marca «Origen» | Por hacer |
| 31 | Cambiar el catálogo de un cliente | Cliente sin asientos (catálogo propio, tras el arreglo F1) y cliente invitado con catálogo compartido que adopta la plantilla de la firma; quién puede hacerlo | Por hacer |
| 32 | Cambio de catálogo con asientos | El asistente de correspondencia: qué va a pasar, cuenta por cuenta, fecha de corte, asiento de reclasificación | Por hacer |
| 33 | Mantener las plantillas | Plantillas incompletas, importar una plantilla desde archivo, eliminar una plantilla de la firma | Por hacer |

### Bloque B · Empresas con más de una moneda

Se define al terminar la tarea 2b (qué ya cubren 03 Bancos, 06 Revaluación, 10 Mapeo,
22 Transferencias y los informes).

### Bloque C · Retenciones de ISR e ITBIS y la carta de retención

Se define al terminar la tarea 2c.

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
| F1 | Los clientes que crea la firma nacen con catálogo propio y después NO se les puede cambiar de plantilla, ni siquiera sin asientos (`assertSharedCatalog`) | Arreglar: permitir el cambio libre en catálogo propio mientras no haya asientos | En curso (API escrito, falta probar) |
| F2 | Una plantilla de la firma ya usada no se puede eliminar: cuenta también a los clientes con catálogo propio, que ya no dependen de ella, y el mensaje pide «cámbielas de catálogo», imposible para ellos | Arreglar | Por hacer |
| F3 | Eliminar una plantilla deja colgado el catálogo por defecto de la firma (borrado suave: el `ON DELETE SET NULL` no corre) y la próxima alta falla | Arreglar | Por hacer |
| F4 | Crear empresa por `CreateCompanyDto.chartTemplate` acepta plantillas de OTRA firma y plantillas incompletas | Arreglar | Por hacer |
| F5 | El alcance «Mi firma contable» solo lo esconde la web: el API deja crear plantillas de firma a cualquiera | Arreglar | Por hacer |
| F6 | En la empresa de la firma, sus propias plantillas salen como «De mi contador» | Arreglar | Por hacer |
| F7 | La plantilla de firma es de un USUARIO (`owner_user_id`), no de la firma: si ese contador sale de la firma, la plantilla deja de poder elegirse | REU | Por hacer |
| F8 | Dos tablas de pertenencia distintas para la misma pregunta (`user_companies` al elegir, `user_company_roles` al ver) | Revisar y alinear | Por hacer |
| F9 | El acceso «Contabilidad e Impuestos» (rol Contador) no puede cambiar el catálogo de un cliente (le falta `ACCOUNTING_INTEGRATION_CONFIGURE`) | REU | Por hacer |
| F10 | Las empresas que nacen de una solicitud de certificación y las «Para mi firma» no reciben la plantilla de la firma ni catálogo propio | REU | Por hacer |
| F11 | Sin plantilla por defecto en la firma, el alta guarda `chart_template_id = NULL` en vez de la del sistema (ver H1) | Arreglar (altas nuevas) + REU (saneo de las 16 de PROD) | Por hacer |
| F12 | «Crear plantilla desde mi catálogo» con catálogo compartido ignora los nombres propios de la empresa y copia cuentas ocultas | Arreglar | Por hacer |
| F13 | Una plantilla incompleta no se puede completar en el sitio (no hay edición de roles) | REU | Por hacer |
| F14 | Reusar el código de una plantilla eliminada da un error genérico de duplicado | Arreglar | Por hacer |
| F15 | El cambio con asientos no es atómico (la plantilla nueva y el asiento se confirman antes del paso 3) y no reapunta referencias ni resiembra cuentas por impuesto | Verificar y arreglar | Por hacer |
| F16 | Errata «o dela de alta» en el diálogo de Nuevo cliente | Arreglar | Por hacer |
| F17 | Tú y usted mezclados en Plantillas de Catálogo, el asistente y mensajes del API | Arreglar en las pantallas de la tanda | Por hacer |
| F18 | Manual desfasado: CAT-01 (nombres viejos de plantillas), CAT-13/OBJ-22 (ruta del alta), OBJ-22 (cambio para clientes con catálogo propio), CTD-06 (falta el campo «Catálogo de cuentas») | Arreglar | Por hacer |
| F19 | El video 09 dice que una plantilla «Solo esta empresa» sirve «de base en otra empresa», y el diálogo promete lo mismo: solo es cierto para las de firma | Arreglar el texto y regrabar el 09 | Por hacer |

- **PROD, contexto:** 20 firmas aprobadas, ninguna con catálogo por defecto
  (`default_chart_template_id`); solo existen las 3 plantillas del sistema (ninguna
  propia de una firma); 125 empresas usan GERMIVA_BASE, 5 RD_AMPLIADO y 1 RD_UNIFICADO;
  3 tienen catálogo propio (`chart_mode = OWN`).
