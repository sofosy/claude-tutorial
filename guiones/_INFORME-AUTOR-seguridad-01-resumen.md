# Informe AUTOR A · seguridad-01-resumen

**Estado**: E0 restaurado JUSTO antes · entra rosa.almanzar · no escribe en BD.

## Pasos
1. `01-cifras`: las cinco cifras, clic en «Sin ningún rol» → Personas › Sin rol (Luisa) → pestaña Resumen.
2. `02-requiere-atencion`: los cuatro asuntos con su enlace; «Configurar →» → Roles › Mensajero (Vacío) + cartel cuidado; vuelta; «Nada pendiente» en voz.
3. `03-actividad-reciente`: columnas, tiempo relativo (sin leer ninguno, R13), etiquetas, «Ver bitácora», clic en la fila «Cambió permisos» → Auditoría con el evento abierto.
4. `04-caso-practico`: revisión semanal: cifras → asunto de Héctor «Revisar →» → Personas › Nunca entraron con su panel (Pendiente).

## Decisiones
- `mapa_fijo` «::1» → «192.168.1.25» (la columna IP).
- El asunto «nunca inició sesión» se narra con el texto corregido («Comprueba su correo o desactiva…»), sin «reenviar invitación» (D-08).
- Filas marcadas por texto estable: «Acceso» (la primera = Rosa), «Pedro», «Marta» (casan con usuario o con nombre tras D-S7).

## Dependencias de la ronda 2 (BLOQUEANTE para el paso 03)
- **D-S6**: el selector `.sec-ov__row:has-text('Cambió permisos')` solo existe cuando el Resumen deje de mostrar «Actualizó · Roles #79». Si la ronda 2 no llega: selector `.sec-ov__row:has-text('Roles #79')` y voz «una fila Actualizó sobre el rol Almacén».
- **D-S7**: la voz dice «los permisos del rol Almacén»; vale con «Rol #79» o con el nombre.

## A comprobar en el ensayo
- La fila del cambio está 8.ª–9.ª, bajo el pliegue del scroll interno (266 px): la marca debe caer entera tras el desplazamiento del motor.
- Las filas en y 598–694 rozan el FAB por la derecha: mirar fotograma de las marcas de fila.

## Puertas (sin apps, 2026-09-27)
- `node seeds/_puertas/revisar.mjs seguridad-01-resumen` → **0 ERROR**, 1 AVISO (primer paso sin `button.panel-collapse`: no existe en /home, /security/* ni /profile; _SELECTORES §0). Duración prevista de los pasos: **3:10** (+6 s de entrada y cierre de marca).
- `.venv\Scripts\python.exe tut.py verificar seguridad-01-resumen` → **0 errores, 0 avisos**.
- No se ensayó ni se grabó (lo hace el operador).
