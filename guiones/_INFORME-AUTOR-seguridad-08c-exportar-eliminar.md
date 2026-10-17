# Informe de autor · seguridad-08c-exportar-eliminar («Con y sin permiso · Exportar y eliminar»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion (sin ensayo).
- **Entran en cámara:** `pedro.nunez` (sesion) → `ana.mejia` → `rosa.almanzar` → `pedro.nunez`.
- **Estado de partida: E0.** `restaurar.mjs E0` antes y después.
- **Duración prevista:** 3:00 (+6 s) · 01 38 s · 02 43 s · 03 25 s · 04 19 s · 05 23 s · 06 34 s.

## Qué escribe cada toma

Nada en BD (solo eventos de acceso, y el de exportación si el API lo registra). «Exportar Excel» descarga
`productos_export.xlsx` en 0,15 s sin diálogo nativo; «Eliminar» solo se señala.

## Contrastes

| Punto | CON | SIN |
|---|---|---|
| «Importar / Exportar» de Productos | 01 Pedro (Almacén: PRODUCT_EXPORT): abre el diálogo y exporta | 02 Ana: el botón no está; en la fila solo el lápiz «Abrir» |
| Papelera «Eliminar» de la fila «Machete de 22 pulgadas» | 04 Rosa (Admin) | 06 Pedro: Abrir, Duplicar, Desactivar, sin Eliminar |

Los pasos 03 y 05 SOLO cambian de usuario (el login deja en `/home`); el paso siguiente entra con `navegar
/inventory/product/list` porque para Rosa y Pedro «Inventario» abre un panel con varias opciones (no hay
selector verificado de «Productos» dentro). Para Ana es enlace directo y se pulsa en cámara (y no tiene panel
que contraer).

## Dependencias de la ronda 2

- **D-S2**: hoy la lista de Productos abre «Acceso Denegado — Impuestos» y rompe las fotos para Pedro y Ana.
  Escrito para el comportamiento CORREGIDO.

## Observación (no se dice en voz)

- Ana ve «Alta por foto» (F-257 lo liga a PRODUCT_VIEW) aunque no tiene PRODUCT_CREATE. La voz solo afirma
  que no aparece «Importar / Exportar». Posible hallazgo para el orquestador.

## Puertas

- `revisar.mjs` → 0 ERROR · 0 AVISO. `tut.py verificar` → 0 errores, 0 avisos.
