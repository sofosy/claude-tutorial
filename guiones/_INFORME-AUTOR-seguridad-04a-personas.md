# Informe del autor · seguridad-04a-personas (AUTOR B, 2026-09-27)

- **Estado de partida:** E0 (`restaurar.mjs E0`). **Escribe:** nada (solo el ingreso de Rosa). **Graba:** rosa.almanzar.
- **Duración predicha:** 3:43 (+6 s de entrada/cierre). 5 pasos: vistas (63 s) · buscar y filtrar (45 s) · ficha (62 s) · su actividad (22 s) · caso «nunca entró» (27 s).
- **Puertas:** `revisar.mjs` 0 ERROR · 1 AVISO · `tut verificar` 0 errores.

## Decisiones
- Se entra por `/security/resumen` y se pulsa la pestaña «Personas» (Seguridad del riel de Rosa cae en y=716, fuera del cuadro).
- Las vistas se pulsan (Sin rol → Luisa, Nunca entraron → Héctor, Inactivas → Sonia, Todas), no solo se señalan.
- No se nombran colores de estado ni el rojo de «Sin ningún rol»: no están verificados. La voz dice «cada estado lleva su color».
- «Últimos ingresos» del canon dicen «Cliente de API» y «::1» (D-S13). La voz lo explica como datos cargados por un programa. `privacidad.mapa_fijo` cambia «::1» por 192.168.1.25.
- «Ver su actividad» vuelve con la pestaña «Personas»: el motor no tiene acción «atrás».
- Caso práctico final: vista «Nunca entraron» → ficha de Héctor («Pendiente», «Sin ingresos registrados en esta empresa») + cartel de consejo.

## Avisos justificados
- `el primer paso no contrae el menú`: `button.panel-collapse` no existe en `/security/*`.

## Dependencias de la ronda 2
- 04: D-S7 (nombres de registro legibles). La voz no lee ninguna fila salvo «Acceso». En el ensayo hay que confirmar que la primera fila de `?persona=ana.mejia` sigue siendo el «Acceso».
- 03: si la ronda 2 vuelve a sembrar los ingresos con un navegador real, la frase «Aquí dice Cliente de API…» deja de ser cierta y hay que quitarla.

## Selectores que el ensayo debe confirmar (clases vistas en los volcados, sin `count()==1` propio)
`.gm-sheet-row--head`, `.sec-people__row:has-text('Luisa Féliz') .sec-people__norole`, `.sec-people__row:has-text('Héctor Vargas') .gm-status`,
`.sec-people__facts`, `.sec-people__block-head`, `.sec-people__module:has-text('Nómina')` (solo tras «Ver los módulos»),
`.sec-people__login >> nth=0` / `.gm-cell-mono >> nth=0` / `span >> nth=0`, `.sec-audit__row:has-text('Acceso')`, `:text('Sin ingresos registrados')`.
