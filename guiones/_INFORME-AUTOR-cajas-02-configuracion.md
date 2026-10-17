# Informe de autor · cajas-02-configuracion (Video 2 «Denominaciones, políticas e impresora»)

- **Graba:** `admin.progreso`, en DOS tandas:
  1. pasos 01–03 desde **S0** (`tut.py video`, restaurar S0 antes y después);
  2. `restaurar S2i` → `tut.py grabar cajas-02-configuracion --paso 04` → `montar-video` → `restaurar S0`.
- **Duración prevista:** 3:48 · 01-denominaciones 50 s · 02-politicas-fondo-tolerancia 55 s ·
  03-politicas-aprobaciones-cuadre 55 s · 04-impresora 68 s.
- **Escribe:** 01 denominación «Veinte» (20, BILL, orden 7, DOP) con `company_id=43` (verificado en BD);
  03 umbrales 1,000 / 60,000 en `cashier_config`; 04 impresora de Caja Principal (id 49):
  `0483` / `070b` / `USB`, `auto_print_receipt=1`, `auto_open_drawer=0` (verificado en BD).
- **Estado final de 01–03 frente a S1:** `cashier_config` es IDÉNTICO a S1 en las 18 columnas de
  política (5000 · — · — · AMOUNT · 50 · 1 · 3 · 720 · 5000 · 10000 · 1 · 1 · 1 · 24 · 0 · 0 · 1000 ·
  60000). La única diferencia es la denominación «Veinte», como se esperaba.

## Puertas
1. `tut.py verificar` → 0 errores, 0 avisos.
2. `revisar.mjs` → 0 ERROR · 1 AVISO (justificado: primer paso sin `button.panel-collapse`, que no
   existe en Cajas).
3. Ensayo bajo `NAVEGADOR.lock`: 01–03 desde S0 → 39 acciones OK, 0 fallos, 0 CORTADO; 04 desde S2i
   → 12 acciones OK, 0 fallos (log con líneas `── paso`). Capturas en `salida/cajas-02-configuracion/ensayo/`.

## Notas
- En el paso 03 dos marcas salían CORTADAS (el motor centra el campo contra la ventana 0..720 y el
  panel lateral tiene pie fijo). Se resuelve con dos `presionar` invisibles de tecla inocua
  (`Shift` en el umbral bajo, `End` en la casilla de conteo ciego): Playwright enfoca y desplaza el
  campo antes de que se marque. No cambian datos.
- «Detectar» solo se señala (no se pulsa). La voz dice que la impresora la configura un
  administrador (H-01 no se muestra).
- Privacidad: el input `nameCount` («Veinte») cae en la regla «nombre» del perfil estricto; se añadió
  «veinte» a `permitidos`. Pronunciación en `pronunciacion`: USB, ID, IP, 0483, 070b.

## Dudas
- Ninguna bloqueante.
