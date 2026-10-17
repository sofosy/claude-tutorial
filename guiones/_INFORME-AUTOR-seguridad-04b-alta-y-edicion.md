# Informe del autor · seguridad-04b-alta-y-edicion (AUTOR B, 2026-09-27)

- **Estado de partida:** E0. **Escribe:** crea a Julio Santana (`julio.santana`, Vendedor), le cambia la clave, le agrega Almacén, lo desactiva, lo activa y lo elimina. Además deja eventos en la bitácora. **Restaurar E0 antes y después.** **Graba:** rosa.almanzar.
- **Duración predicha:** 3:59 (+6 s). Está cerca del tope de 4:10. 5 pasos: alta (≈90 s) · cambiar contraseña (35 s) · asignar rol (49 s) · desactivar/activar (37 s) · eliminar + caso (32 s).
- **Puertas:** 0 ERROR · 1 AVISO · `tut verificar` 0 errores.

## Decisiones
- Alta de 7,7–8,2 s (R16/R25). A +4 s del clic se pone una marca de relleno sobre el campo «Nombre de usuario». La marca del diálogo «Operación completada» va anclada ≈9,5 s después del clic (el motor espera hasta 15 s a que aparezca).
- Los toasts de desactivar, activar, eliminar y roles se marcan sin `al_decir`, justo después del clic (R9). Cada uno usa un selector distinto por su texto (R20). Los tres clics en «Más acciones» también usan selectores distintos.
- Radio «Activo»: `mat-radio-button >> nth=0`, porque «Activo» casa también con «Inactivo». Opción «Vendedor»: `:not(:has-text('sénior'))`.
- D-01 está verificado como corregido (a1-02…05). «+ Asignar rol» se graba con el diff «Se agrega: Almacén».
- Carteles: «cada persona con su propio usuario» (no compartir usuarios) y «desactivar en vez de eliminar». Los dos son temas obligatorios. «Nadie cambia sus propios roles» va solo en voz, con una marca sobre el bloque Roles (máximo 2 carteles).
- La clave nueva de Julio es «Santana2026!». No importa, porque se elimina en el mismo video.

## Avisos justificados
- Primer paso sin `button.panel-collapse`: no existe en `/security/*`.

## Dependencias de la ronda 2
- D-S12 («Guardando…» en los botones). La voz dice «los botones quedan en espera», sin nombrar el texto. En el ensayo hay que medir de nuevo el tiempo del alta.

## Selectores que el ensayo debe confirmar
`mat-dialog-container:has-text('Operación completada')` (con dos diálogos abiertos, R20), `.sec-people__card-name`, `.sec-people__block-title >> nth=0`,
`.sec-people__row:has-text('Julio Santana') .gm-status` (hay que ver si la lista se refresca tras activar), `mat-dialog-container .person-roles__line--add`.
