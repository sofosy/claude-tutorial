# Informe AUTOR A · seguridad-02b-editor-permisos

**Estado**: **E2a** · entra rosa.almanzar · escribe los permisos de «Cobrador» (un guardado por lote).

## Pasos
1. `01-modulos-y-leyenda` (insignia info «Permiso = recurso + acción»): Vendedor; secciones, solo lo contratado, primer módulo con algo, n/total, módulo Cotizaciones, título, leyenda, recurso y acciones.
2. `02-conceder`: Cobrador (Vacío) → Clientes y Proveedores → **Socios** · Ver (ciclo concedido / sin conceder / concedido) → «Conceder todo» en Estado de Cuenta → barra de cambios.
3. `03-alcance`: segmentado de «Ver en Socios»: Todos / Equipo / Propios → Propios; cartel consejo (se decide por quién CREÓ); solo en permisos de ver.
4. `04-buscar-permiso`: «factur» → Resultados en todo el catálogo → Facturas · Ver; tope de 60 y vacío en voz; borrar búsqueda.
5. `05-guardar-o-descartar` (cartel cuidado): clic en «Contador externo» → «Cambios sin guardar» → Seguir editando → «Descartar» señalado → Guardar cambios → toast → filtro Concedidos; cierre del caso.

## Decisiones
- «Clientes» = recurso «Socios» (_SELECTORES §2). «Cobros» no es módulo: se usa «Conceder todo» en «Estado de Cuenta».
- `:text-is('Ver')` solo casa la acción SIN conceder (la concedida lleva el icono «check» dentro); el segundo clic del ciclo usa `.rpe__act--direct`.
- La voz no lee el número de cambios de la barra (serán 4) ni el de personas más allá de «a ninguna».
- Los filtros se presentan como estado del PERMISO, «no por el estado de un documento» (verdad 1).

## Dependencias de la ronda 2
- Solo el texto «Guardando…» del botón (no se nombra).

## A comprobar en el ensayo
- Al borrar la búsqueda, el editor vuelve a «Clientes y Proveedores» (el paso 05 depende de ello para que Concedidos enseñe Socios y Estado de Cuenta).
- El FAB tapa el borde derecho de «Guardar cambios»: el clic cae en el centro (x≈1141).
- «Facturas» en los resultados está en y≈1135 del scroll interno: el motor lo centra.
- Los ids de Cobrador/Contador externo en E2a no se usan (todo se abre desde el riel).

## Puertas (sin apps, 2026-09-27)
- `node seeds/_puertas/revisar.mjs seguridad-02b-editor-permisos` → **0 ERROR**, 1 AVISO (primer paso sin `button.panel-collapse`: no existe en /home, /security/* ni /profile; _SELECTORES §0). Duración prevista de los pasos: **3:51** (+6 s de entrada y cierre de marca).
- `.venv\Scripts\python.exe tut.py verificar seguridad-02b-editor-permisos` → **0 errores, 0 avisos**.
- No se ensayó ni se grabó (lo hace el operador).
