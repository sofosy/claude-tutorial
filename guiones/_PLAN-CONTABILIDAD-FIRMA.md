# Plan · Tanda «Catálogo de la firma para sus clientes» (serie Contabilidad)

Pedido del usuario (2026-10-18): los videos de Contabilidad no explican cómo una firma
contable establece el catálogo de cuentas por defecto de los clientes que crea, ni las
posibilidades que se le dan:

- la firma cambia el catálogo de un cliente suyo;
- la firma crea un catálogo propio como plantilla, disponible solo para sus clientes;
- la firma lo pone por defecto al crear sus clientes;
- y las demás combinaciones que el sistema permita (ver la investigación).

Además, con `DUMP_URL_PROD` ya configurada, se valida contra la copia de PROD lo que se
unió en el lote 2 (api#1563, web#1409).

Ramas: `feature/contabilidad-catalogo-firma-clientes` en Germiva-api y germiva-website;
`claude/cool-johnson-q9dpzp` aquí. Cada tarea terminada sale en su propio commit, y
este plan se actualiza en el mismo commit.

## Tareas

| # | Tarea | Estado |
|---|-------|--------|
| 1 | Validar contra la copia de PROD lo unido en el lote 2 (migraciones, historial de transferencias, sugerencias de conciliación, centros de costo, búsqueda de períodos) y borrar la copia (`down.sh --all`) | Hecho |
| 2 | Investigar en el código y el manual cómo funciona el catálogo de la firma para sus clientes (dónde se fija el predeterminado, qué pasa al crear un cliente, cambiar el catálogo de un cliente, plantilla propia visible solo a sus clientes) | En curso |
| 3 | Definir la lista de videos de la tanda (numeración 28 en adelante) y los datos de partida (firma + clientes) | Por hacer |
| 4 | Corregir los defectos que aparezcan (API y web), con pruebas, en las ramas `feature/contabilidad-catalogo-firma-clientes` | Por hacer |
| 5 | Semilla: estados nuevos en `seeds/contabilidad/preparar.py` para la firma y sus clientes | Por hacer |
| 6 | Guionar, revisar, ensayar y grabar cada video (un commit por video) | Por hacer |
| 7 | Manual de Contabilidad y de la Cuenta, catálogo de videos, textos para YouTube | Por hacer |
| 8 | REU: fichas que la tanda toque o deje abiertas | Por hacer |
| 9 | Validación final contra PROD si el cambio toca migraciones o contabilidad; `down.sh --all` y verificación vacía | Por hacer |
| 10 | PR a master/main con CI en verde | Por hacer |

## Videos

Se completa al terminar la tarea 3.

| # | Video | Estado |
|---|-------|--------|

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
- **PROD, contexto:** 20 firmas aprobadas, ninguna con catálogo por defecto
  (`default_chart_template_id`); solo existen las 3 plantillas del sistema (ninguna
  propia de una firma); 125 empresas usan GERMIVA_BASE, 5 RD_AMPLIADO y 1 RD_UNIFICADO;
  3 tienen catálogo propio (`chart_mode = OWN`).
