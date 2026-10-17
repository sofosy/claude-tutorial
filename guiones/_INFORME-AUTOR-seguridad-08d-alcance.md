# Informe de autor · seguridad-08d-alcance («Con y sin permiso · El alcance: propios, equipo y todos»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion (sin ensayo).
- **Entran en cámara:** `carlos.pimentel` (sesion) → `ana.mejia` → `rosa.almanzar` → `ana.mejia`.
- **Estado de partida: E0.** `restaurar.mjs E0` antes y después.
- **Duración prevista:** 3:51 (+6 s) · 01 40 s · 02 34 s · 03 36 s · 04 28 s · 05 26 s · 06 26 s · 07 44 s.

## Qué escribe cada toma

| Paso | Escribe |
|---|---|
| 06 | rol Vendedor (77): alcance de «Cotizaciones · Ver» Propios → Equipo (`role_permissions` + `audit_logs` PERMISSIONS_CHANGED) |
| resto | solo eventos de acceso (y el 403 del paso 04, que no escribe) |

Lo deshace `restaurar E0`.

## Contraste sobre el MISMO listado de Cotizaciones

| Alcance | Quién | Pie de la lista (E0 verificado) |
|---|---|---|
| Todos | 02 Carlos | 1 – 8 de 8 |
| Propios | 03 Ana | 1 – 3 de 3 |
| Equipo (Zona Este) | 07 Ana, tras el cambio de Rosa | 1 – 5 de 5 |

La lista no tiene columna de creador (ni en «Configurar Columnas»): la voz dice de quién es cada cotización y
se marca la celda N° («COT n»). 04: Ana, en «Propios», abre por número la cotización 4 (de José) →
403 «Tu rol solo te permite ver y trabajar las cotizaciones que creaste tú. Pide acceso a tu administrador si
necesitas este documento.» (API verificado, A6). Se hace ANTES del cambio a Equipo (con Equipo, la 4 sí es
visible). Carteles: consejo en 03 («Propios es lo que la persona creó…») y en 07 («Un equipo no da
permisos…»). Resumen práctico al final de 07.

## Diagrama corregido: `marca/diagramas/alcance-propios-todos.html`

Antes: 6 documentos ilustrativos «COT-1042…», 2 fases (6 de 6 / 2 de 6). Ahora casa con E0: COT 8…COT 1 en el
orden de la lista real, autores Rosa (8), Carlos (7, 6), José (5, 4), Ana (3, 2, 1); fase 2 «Solo los
propios» 3 de 8; **fase 3 nueva** «Equipo · Zona Este» 5 de 8 (vuelven las de José). Se actualizó la cuenta
de fases en `GRABACION.md` («(3)»). No se ha visto renderizado (sin navegador): revisar la lámina en el ensayo.

## Dependencias de la ronda 2

- **D-S4**: hoy el 403 de alcance NO se ve (la vista vuelve muda a la lista). Escrito para el comportamiento
  CORREGIDO: se marca la unión `.mat-mdc-snack-bar-container, mat-dialog-container` SIN `al_decir` y
  `click_opcional` del primer botón del diálogo (si es toast, no hace nada). Ajustar al ver su forma real.

## A verificar en el ensayo

- `tr:has-text('COT n') td:nth-child(1)` (celda N°) y el clic de `Equipo` en el segmentado.
- Que tras el 403 la pantalla quede en la lista (así fue en A6).

## Puertas

- `revisar.mjs` → 0 ERROR · 6 AVISO (5 del paginador en zona FAB, justificados; primer paso sin
  panel-collapse: es la lámina sobre `/home`).
- `tut.py verificar` → 0 errores, 0 avisos.
