# Informe de autor · seguridad-08b-crear-editar-anular («Con y sin permiso · Crear, editar y anular»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion (sin ensayo).
- **Entran en cámara:** `ana.mejia` (sesion) → `marta.guzman`.
- **Estado de partida: E0.** `restaurar.mjs E0` antes y después.
- **Duración prevista:** 2:45 (+6 s) · 01 44 s · 02 39 s · 03 45 s · 04 37 s.

## Qué escribe cada toma

| Paso | Escribe |
|---|---|
| 02 | cotización 2 (Q2, Colmado La Esquina): cantidad de la 1.ª línea «Bombillo LED 9 W» 12 → 15 y lo que genere el guardado (`quotes`, `quote_details`, `quote_versions`, `audit_logs`) |
| resto | solo eventos de acceso |

Q2 NO se cancela: el paso «Cancelada» solo se señala (Q2 sigue en Borrador para 08e). Todo lo deshace
`restaurar E0`.

## Contrastes

| Punto | CON (Ana) | SIN (Marta) |
|---|---|---|
| Lista de Cotizaciones | «Crear Cotización» y «Más acciones › Duplicar» | no existen (desaparecen, no se ponen en gris); solo el ojo |
| La MISMA Q2 | «Editar Cotización», Guardar, paso «Cancelada» pulsable (QUOTE_UPDATE) | «Cotización», solo «Volver», pasos bloqueados |

## Dependencias de la ronda 2

- **D-S1**: hoy, al abrir cualquier cotización, salta «Acceso Denegado — Configuración Empresa» (Ana y
  Marta). Escrito para el comportamiento CORREGIDO (sin modal).

## A verificar en el ensayo (no explorado)

- `input[formcontrolname='quantity']` (el primero = primera línea; hay 2).
- Qué muestra el guardado: se marca `.mat-mdc-snack-bar-container, mat-dialog-container` SIN `al_decir` y
  `click_opcional` de «Aceptar». Si sale otro diálogo (p. ej. de versión), añadir su marca y su botón.

## Decisiones

- No se usa `/sales/quotes/create` con Marta: hoy avisa «No tienes permiso para ver «Cotizaciones»» (D-S8:
  nombra lo que SÍ puede ver; no está en la lista de la ronda 2).
- No se abre el formulario nuevo para cancelarlo (evita el diálogo de salir con cambios); se señala el botón.
- Queda en 2:45 (el plan estimaba 3:40): el contenido del plan está completo; no se rellenó.

## Puertas

- `revisar.mjs` → 0 ERROR · 4 AVISO (pie del formulario y paginador en zona FAB: falsos positivos conocidos).
- `tut.py verificar` → 0 errores, 0 avisos.
