# Informe de autor · seguridad-08e-aprobar-y-estado («Con y sin permiso · Aprobar y el estado del documento»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion (sin ensayo).
- **Entran en cámara:** `carlos.pimentel` (sesion) → `ana.mejia` → `carlos.pimentel`.
- **Estado de partida: E0** (`quote_requires_approval = 1`). `restaurar.mjs E0` antes y después.
- **Duración prevista:** 3:02 (+6 s) · 01 30 s · 02 33 s · 03 43 s · 04 37 s · 05 40 s.

## Qué escribe cada toma

| Paso | Escribe |
|---|---|
| 02 | cotización 1 (Q1, de Ana, Constructora Mirador): Borrador → Aprobada (`quotes`, `quote_approvals`, `quote_versions`, `audit_logs`) |
| 03 | nada (el clic en «Aprobada» de Ana no hace nada, verificado: Q2 sigue en estado 1) |
| 04–05 | nada: «Convertir a factura» solo se señala; los menús se cierran con Escape |

Lo deshace `restaurar E0`.

## Contrastes

| Punto | CON | SIN |
|---|---|---|
| Paso «Aprobada» del stepper (permiso Aprobar) | 02 Carlos en Q1 → «Aprobar cotización» [Aprobar] → «Éxito / Estado actualizado correctamente» [Aceptar] | 03 Ana en su Q2: el paso se ve, `cursor: not-allowed`, el clic no hace nada |
| «Más acciones» del formulario (estado) | 04 Carlos en Q6 Aprobada: Convertir a factura · Versiones e historial · Duplicar | 05 el MISMO Carlos en Q7 Borrador: Versiones e historial · Duplicar (desaparece) |

Reglas usadas, sin inventar (F-255, F-256, _SELECTORES §6): «Aprobada» exige QUOTE_APPROVE con aprobación
exigida; «Convertir a factura» exige QUOTE_CONVERT_DIRECTLY_TO_INVOICE y estado Aprobada o Aceptada. La voz dice
que esa regla NO se configura en el rol (A-018: no hay filtros por estado). Entre documentos se entra siempre
desde la lista (R21). Cartel cuidado en 05; resumen práctico al final.

## Diagrama `estado-documento`

Ya estaba corregido (cotización Borrador → Aprobada, «Convertir a factura» bloqueado/permitido). Se cambió la
hoja «COT-1042» por «COT 1» para casar con E0 (Q1 es la que Carlos aprueba).

## Dependencias de la ronda 2

- **D-S1**: hoy, al abrir cualquier cotización, salta «Acceso Denegado — Configuración Empresa» (Carlos y
  Ana). Escrito para el comportamiento CORREGIDO.

## A verificar en el ensayo

- El clic crudo sobre `.step-content:has-text('Aprobada')`: en la exploración Playwright avisó que
  `.step-wrapper.chevron-wrapper` intercepta el puntero. Si no abre la confirmación, usar
  `.step-wrapper:has(.step-content:has-text('Aprobada'))`.
- La marca del éxito `mat-dialog-container:has-text('Estado actualizado')` (sin `al_decir`, tarda 1,4–4,3 s).

## Puertas

- `revisar.mjs` → 0 ERROR · 1 AVISO (primer paso sin panel-collapse: es la lámina sobre `/home`).
- `tut.py verificar` → 0 errores, 0 avisos.
