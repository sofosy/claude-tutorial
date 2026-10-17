# Informe de autor · seguridad-08a-vista («Con y sin permiso · Ver una pantalla»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion (sin ensayo).
- **Entran en cámara:** `ana.mejia` (sesion) → `pedro.nunez` → `marta.guzman`, con la receta de
  `_CONVENCIONES` (menú del usuario → Cerrar sesión → usuario/clave → Entrar; el login de 6–8 s lo cubren la
  voz y una marca SIN `al_decir` sobre `aside.sidebar`, que no existe en la pantalla de acceso).
- **Estado de partida: E0.** `restaurar.mjs E0` antes y después.
- **Duración prevista:** 3:26 (+6 s) · 01 43 s · 02 45 s · 03 30 s · 04 52 s · 05 36 s.

## Qué escribe cada toma

Nada salvo los eventos de acceso (Ana, Pedro, Marta) en `audit_logs` → `restaurar E0`.

## Contrastes (mismo punto, primero CON y luego SIN)

| Punto | CON | SIN |
|---|---|---|
| Ventas › Cotizaciones en el menú | 01 Ana (lista 1–3 de 3) | 02 Pedro: su menú no tiene Ventas |
| La dirección de Cotizaciones | (Ana entra por el menú) | 03 Pedro: `navegar /sales/quotes` → Inicio + toast «No tienes permiso para ver «Cotizaciones». Solicita el acceso…» (verificado A3/spa-01) |
| Consola Seguridad | 04 Marta: 4 pestañas, sin «Nuevo», rol sin Duplicar/Editar y casillas en gris | 05 Marta: Integraciones por dirección → franja `.console-denied` y debajo su Resumen |

Carteles: consejo (03) «Escribir la dirección no salta el permiso…»; cuidado (05) «Ver no es cambiar…».
Resumen práctico al final de 05.

## Decisiones

- El plan pedía el contraste «sin aviso / con aviso» (`/sales/quotes` vs `/my-company`); ya no existe (las
  dos rutas avisan con toast, _SELECTORES §8.12): se enseña una sola dirección.
- Riel de Pedro: `aside.sidebar .rail-item[aria-label='Inventario']` sin tag (para él Inventario abre panel).

## Dependencias de la ronda 2

Ninguna: lista de Cotizaciones (sin abrir el formulario) y consola verificadas sin modales.

## A verificar en el ensayo

- Que el cierre de sesión conserve la insignia (sessionStorage) o que el motor la re-empuje tras el login.
- `h1:has-text('Ana')` / `h1:has-text('Pedro')` del Inicio («Buenos días, …»).

## Puertas

- `revisar.mjs` → 0 ERROR · 1 AVISO (paginador en zona FAB: el rango está a la izquierda de los botones).
- `tut.py verificar` → 0 errores, 0 avisos.
