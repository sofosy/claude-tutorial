# Puertas de calidad de los videos (`seeds/_puertas/`)

Herramientas Node sin dependencias (solo `node:fs`/`node:path`). Se corren
desde la raíz de `claude-tutorial`. `seeds/` está en `.gitignore`: esta
carpeta NO viaja con el repo — cópiala o recréala al clonar.

| Cuándo | Comando | Sale con 1 si… |
|---|---|---|
| Antes de grabar | `node seeds/_puertas/revisar.mjs <modulo\|ruta.json> [...] [--wps=3.0] [--audio]` | hay algún ERROR |
| Antes de grabar (app arriba; ESCRIBE en la BD) | `.venv/Scripts/python.exe seeds/_puertas/ensayar.py <modulo\|ruta.json> [--paso ID] [--headed] [--salida DIR]` | hay fallos (1) · 0 pasos / login fallido (2) |
| Después de montar | `node seeds/_puertas/veredicto.mjs <modulo> [...]` | algún video queda en REGRABAR |
| Para arreglar R0 | `node seeds/_puertas/huecos.mjs <modulo> [seg=10]` | — |

## revisar.mjs — el guion (`guiones/<modulo>.json`)

Predice la línea de tiempo de cada paso: la voz a 3,0 palabras/s (`--audio`
usa los tiempos reales de `salida/<modulo>/audio/*.json` si ya existen) y el
anclaje de `al_decir` igual que `grabar.py` (busca desde el reloj actual,
aplica el mapa `PRONUNCIACION` que lee de `narrar.py`, descuenta 1,0 s de
viaje del cursor en clics y 0,25 s en marcas, tecleo a 45 ms/letra).

- **ERROR**: R0 (> 10 s sin cambios en pantalla, medido sobre el video entero,
  también a través del corte entre pasos); `al_decir` ausente, repetido o ya
  gastado; R2 (ancla antes de fin de tecleo + 2 s); `resaltar` sobre algo que
  el mismo paso ya pulsó; `esperar_ms` delante de una acción con `al_decir`;
  `esperar` en paso con `navegar` o clic de guardar/crear/abrir (R1/R24);
  R5b (`resaltar` sobre `table`/`tbody` entera).
- **AVISO**: sigla sin explicar la primera vez; paso > 120 s; video fuera de
  1:30–4:10; primer paso sin `button.panel-collapse`; marca sobre fila `tr`;
  dos marcas a la vez; clic/marca en la zona del `.chatbot-fab`; `esperar`
  con clics no críticos; acciones que terminan después de la voz.

## veredicto.mjs — lo grabado (`salida/<modulo>/`)

PUBLICABLE o REGRABAR con la lista de FALLOS: línea ERROR del informe o error
del segmento; clic a más de ±0,9 s de su palabra; tramo > 10 s sin eventos
(clic, tecleo, marca durante su `durante_ms`, navegación, alerta nueva);
alerta sin `resaltar` sobre el diálogo en ≤ 8 s; elemento CORTADO;
`video.mp4` más viejo que los segmentos.

Descarta (y lista aparte) los falsos positivos conocidos: CORTADO sobre fila
`tr` o sobre `footer.form-layout-footer`; alerta señalada hasta 1,5 s ANTES
de que la sonda la detecte; el mismo diálogo (mismas primeras palabras)
reportado varias veces mientras se opera dentro, o que sigue abierto desde el
paso anterior.

## huecos.mjs

Tramos de imagen quieta sobre los segmentos grabados (umbral en segundos, 10
por defecto), con el texto del subtítulo (`video.srt`) que suena en cada uno:
ahí va la marca nueva o el `durante_ms` estirado.
