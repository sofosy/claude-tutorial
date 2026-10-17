# Informe AUTOR A · seguridad-00-introduccion

**Estado**: E0 · entra rosa.almanzar · no escribe en BD.

## Pasos
1. `01-bienvenida` (/home): para quién es la serie, empresa demo (chip de la empresa), tarjeta Seguridad y candado del riel (F-001; F-002 en voz).
2. `02-seis-conceptos`: lámina `conceptos-seguridad`, fases 2–6 en su palabra + cartel consejo «Da los permisos a los roles…».
3. `03-la-consola`: clic en el candado → Resumen; título, pestañas con conteos, cartel cuidado «Cada pestaña exige su permiso», buscador, menú Nuevo (abre y cierra con Escape).
4. `04-recorrido` (caso práctico): se sigue a Ana por Personas → Roles → Integraciones → Auditoría → Resumen y se resume la serie.

## Decisiones
- **Diagrama corregido**: `marca/diagramas/conceptos-seguridad.html`, tarjeta 04 «Alcance»: decía «los propios o todos»; ahora dice «propios, equipo o todos» y lleva el chip «Equipo». La tarjeta 05 ya decía «No da permisos».
- El recorrido de las cinco pestañas es a la vez el caso práctico (seguir a Ana), para no alargar.
- El buscador se describe como en la app real: personas; en Roles y permisos, roles (_SELECTORES §1), no «permiso».
- Las marcas de recapitulación sobre pestañas ya pulsadas usan `.console-tabs a:has-text(…)` (la misma nav) para no chocar con la regla «marca sobre algo ya pulsado»: las pestañas siguen en pantalla.

## Dependencias de la ronda 2
- Ninguna fuerte. La fila de Auditoría se busca por «Acceso» (no cambia con D-S7).

## A comprobar en el ensayo
- Que la primera fila «Acceso» de Auditoría sea el ingreso de Rosa de la toma.
- El candado de Rosa cae en y=716: el motor lo desplaza (scroll del riel).

## Puertas (sin apps, 2026-09-27)
- `node seeds/_puertas/revisar.mjs seguridad-00-introduccion` → **0 ERROR**, 1 AVISO (primer paso sin `button.panel-collapse`: no existe en /home, /security/* ni /profile; _SELECTORES §0). Duración prevista de los pasos: **3:05** (+6 s de entrada y cierre de marca).
- `.venv\Scripts\python.exe tut.py verificar seguridad-00-introduccion` → **0 errores, 0 avisos**.
- No se ensayó ni se grabó (lo hace el operador).
