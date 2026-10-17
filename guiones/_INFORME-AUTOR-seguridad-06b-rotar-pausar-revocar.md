# Informe del autor · seguridad-06b-rotar-pausar-revocar (AUTOR B, 2026-09-27)

- **Estado de partida:** **E6c** (`restaurar.mjs E6c`). **Escribe:** rota el secreto de «Programa del contador» (el de `credencial.json` deja de valer), la desactiva y la activa, y revoca «Tienda en línea anterior». **Restaurar E6c DESPUÉS**: 06c necesita el secreto vigente. **Graba:** rosa.almanzar.
- **Duración predicha:** 2:28 (+6 s). 4 pasos: rotar (≈45 s) · pausar (30 s) · revocar + Resumen (35 s) · documentación + caso (42 s).
- **Puertas:** 0 ERROR · 1 AVISO · `tut verificar` 0 errores.

## Decisiones
- Rotar y revocar piden confirmación; desactivar y activar no. Tiempos ≈3,4–3,5 s: los toasts se marcan sin `al_decir`. Se usa «Integración activada» para no casar con «desactivada» (R20).
- El paso 03 comprueba en cámara que el asunto «credencial sin uso» desaparece del Resumen («3 asuntos», volcado v06b-08). La antigüedad de la credencial se marca en la celda «Último uso» de la lista, no en el panel.
- Documentación: selectores tomados del código (`api-docs-layout.component.html`), no del DOM vivo: `.api-docs-sidenav button.section-header`, `a.nav-item[href='/security/api-docs/autenticacion']`, `.api-docs-content h1`. Los títulos de los documentos siguen sin acento o en inglés (D-S10): la voz no los lee.
- Carteles: cuidado «rotar corta la integración» y consejo «revoca lo que no se usa» (caso práctico).

## Avisos justificados
- Primer paso sin `button.panel-collapse` (no existe en `/security/*`).

## Dependencias de la ronda 2
- D-S10 (títulos con acento): no cambia la narración.

## No cubierto
- F-239/F-240 (qué ve quien no tiene `INTEGRATION_USER_EDIT/DELETE`): no verificado, no se afirma nada.
