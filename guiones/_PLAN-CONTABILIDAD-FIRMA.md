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
| 1 | Validar contra la copia de PROD lo unido en el lote 2 (migraciones, historial de transferencias, sugerencias de conciliación, centros de costo, búsqueda de períodos) y borrar la copia (`down.sh --all`) | En curso |
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

## Hallazgos

Se completa a medida que aparezcan.
