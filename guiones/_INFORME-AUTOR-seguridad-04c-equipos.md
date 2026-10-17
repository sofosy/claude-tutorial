# Informe del autor · seguridad-04c-equipos (AUTOR B, 2026-09-27)

- **Estado de partida:** E0 («Zona Este» con Ana y José). **Escribe:** el equipo «Zona Norte». Lo crea, le agrega a Carlos y a Héctor, quita a Héctor, cambia la descripción y lo elimina. **Restaurar E0 después.** **Graba:** rosa.almanzar.
- **Duración predicha:** 2:49 (+6 s). 4 pasos: qué es (44 s) · crear (35 s) · agregar miembros (34 s) · quitar/editar/eliminar + caso (56 s).
- **Puertas:** 0 ERROR · 1 AVISO · `tut verificar` 0 errores.

## Decisiones
- Verdad 2 de la serie: un equipo NO da permisos, solo sirve para el alcance «Equipo». Lo dicen la voz y el cartel de cuidado del paso 01, y lo repite el caso práctico del paso 04.
- El ítem «Nuevo › Equipo» solo se nombra. Se usa el «+» del riel (F-020).
- Las casillas de Carlos y de Héctor quedan bajo el pliegue del scroll interno. El motor las centra.
- Toasts (0,3 s) marcados sin `al_decir` y con selector por su texto: «agregadas», «quitada», «eliminado».

## Avisos justificados
- Primer paso sin `button.panel-collapse` (no existe en `/security/*`).

## No cubierto
- F-052 «Sin equipos»: la demo siempre tiene «Zona Este».
- F-226 (`TEAM_VIEW`): qué ve quien no lo tiene no está verificado, y no se afirma nada.

## Selectores que el ensayo debe confirmar
`.sec-people__teams-label`, `.sec-people__title`, `.sec-people__who:has-text('José Cabrera') .gm-sheet-meta`,
`mat-dialog-container:has-text('actualizado correctamente')`, `mat-dialog-container:has-text('Eliminar equipo')`.
