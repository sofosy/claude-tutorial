# Informe de autor · cajas-01-tablero (Video 1 «El tablero y tus cajas»)

- **Graba:** `admin.progreso` · **estado de partida:** S0 (restaurar S0 antes y después).
- **Duración prevista:** 3:13 (revisar.mjs a 3 p/s) · pasos 01-tablero 73 s · 02-nueva-caja 63 s · 03-panel-configuracion 56 s.
- **Escribe:** caja `CAJA-03` «Caja Mostrador 3» (Área de ventas — piso 2, Efectivo+Tarjeta+Transferencia,
  límites 1,000 / 60,000). Verificado en BD tras el ensayo (id nuevo, `acceptTransfer=1`,
  `min_cash_limit=1000`, `max_cash_limit=60000`). El paso 03 depende de esa caja: no se regraba solo
  sin rehacer el 02.

## Puertas
1. `tut.py verificar` → 0 errores, 0 avisos.
2. `revisar.mjs` → 0 ERROR · 1 AVISO (justificado: «primer paso sin `button.panel-collapse`»: en
   Cajas el menú es un riel fijo, el botón no existe; lo dice el brief).
3. Ensayo bajo `NAVEGADOR.lock` (restaurar S0 → ensayar → restaurar S0) → 3 pasos, 45 acciones OK,
   0 fallos, todo «visible=entero». Log con líneas `── paso`. Capturas en `salida/cajas-01-tablero/ensayo/`.

## Notas
- Primer ensayo: 9 fallos en el paso 03 por un selector de `_SELECTORES-CAJAS.md` que no existe:
  `.settings-sheet` (solo existe `.settings-sheet__header`). Corregido a `app-cashier-settings-sheet`.
  Ojo el resto de autores: un `presionar Escape` tras un menú que no se abrió cierra el panel entero.
- El menú de tres puntos de la tarjeta y el de la fila se cierran con `presionar Escape`.
- Privacidad: el input `name` («Caja Mostrador 3») cae en la regla «nombre» del perfil estricto;
  lo salva «mostrador» en `permitidos`.

## Dudas
- Ninguna bloqueante. La voz dice «Luis Batista» (la tarjeta muestra `luis.batista`): subtítulo y
  pantalla casan en lo esencial.
