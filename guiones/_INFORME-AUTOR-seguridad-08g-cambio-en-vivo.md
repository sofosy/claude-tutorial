# Informe de autor · seguridad-08g-cambio-en-vivo («Con y sin permiso · Un cambio en vivo y su rastro en la Auditoría»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion (sin ensayo).
- **Entran en cámara:** `ana.mejia` (sesion) → `rosa.almanzar` → `ana.mejia` → `marta.guzman`.
- **Estado de partida: E0.** `restaurar.mjs E0` antes y después.
- **Duración prevista:** 3:06 (+6 s) · 01 26 s · 02 51 s · 03 33 s · 04 17 s · 05 60 s.

## Qué escribe cada toma

| Paso | Escribe |
|---|---|
| 02 | rol Vendedor (77): quita «Productos · Ver» (PRODUCT_VIEW) con el guardado en lote → `role_permissions` + `audit_logs` PERMISSIONS_CHANGED «Productos · Productos: Ver → —» |
| resto | solo eventos de acceso |

Lo deshace `restaurar E0`.

## Contraste sobre el MISMO punto: Inventario › Productos de Ana

| | Qué se ve |
|---|---|
| CON (01) | «Inventario» en su menú (enlace directo) y la lista 1 – 10 de 25 |
| SIN (03, 04) | «Inventario» ya no está en su menú; por dirección → Inicio + «No tienes permiso para ver «Productos». Solicita el acceso al administrador de tu empresa.» (verificado v08g) |
| Rastro (05) | Marta (AUDIT_LOG_READ) abre «Cambió permisos» en Auditoría: registro, quién, fecha, antes «Ver» → después «—», Solicitud |

## Menú tras el cambio

Con la sesión abierta el menú no cambiaba (D-S9: F5 lo arreglaba). Aquí Ana VUELVE A ENTRAR (el navegador es uno
solo) y la voz lo dice: «el servidor revisa el permiso en cada operación; el menú se arma al entrar; por eso la
hacemos entrar de nuevo». Vale con o sin la corrección de la ronda 2. Cartel cuidado en 02 («Guardar aplica el
cambio a todos los que tienen el rol, desde su siguiente operación»). Resumen práctico al final de 05.

## Dependencias de la ronda 2

- **D-S2**: la lista de Productos de Ana abre hoy «Acceso Denegado — Impuestos» y rompe fotos. Escrito para el
  comportamiento CORREGIDO.
- **D-S6/D-S7**: la fila se busca por «Cambió permisos»; la voz dice «lo hizo Rosa» y no lee la etiqueta del
  registro.

## A verificar en el ensayo

- El clic en `aside.sidebar a.rail-item[href='/security']` de Rosa (y=716: el motor desplaza el riel antes).
- El Origen del evento será el navegador de la grabación (en a7, hecho por la UI: «Chrome · Windows»); la voz
  dice solo «el navegador desde donde se hizo».

## Puertas

- `revisar.mjs` → 0 ERROR · 2 AVISO (paginador en zona FAB; primer paso sin panel-collapse: Ana llega a
  Productos por enlace directo y no tiene panel).
- `tut.py verificar` → 0 errores, 0 avisos.
