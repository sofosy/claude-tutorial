# Modo de grabación en vivo (`tut video`)

El modo original (`tut build`) toma **una foto por paso** y le simula vida con
un acercamiento Ken Burns, un cursor pintado con Pillow y una disolvencia entre
fotos. Se nota: nada se mueve de verdad, un clic no abre nada en cámara y el
usuario no ve el gesto que tiene que imitar.

`tut video` **graba la pantalla mientras el guion se ejecuta**. El cursor
viaja, el botón se pulsa con su onda, el texto se teclea letra a letra, el
menú se despliega, la tabla se recarga — y la voz dice cada cosa en el momento
en que ocurre. Los guiones existentes funcionan sin cambios; solo hay claves
nuevas opcionales para afinar la sincronía.

```
guion.json ──> [C3] edge-tts  ──> voz por paso + tiempo de cada palabra
           ──> [G1] Playwright ──> screencast de Chrome → ffmpeg (maestro, 30 fps)
                                  + capa DOM: cursor, onda de clic, recuadro
                                  + segmentos/<paso>.json (línea de tiempo)
           ──> [G2] ffmpeg     ──> corte por segmento + zoom suave + voz + barras
                                  → video.mp4 · video.srt · youtube-video.txt
```

## Uso

```bash
./.venv/Scripts/python.exe tut.py video <tutorial>            # todo: voz → grabar → montar
./.venv/Scripts/python.exe tut.py video <tutorial> --paso 04  # regrabar solo un grupo
./.venv/Scripts/python.exe tut.py grabar <tutorial>           # solo G1
./.venv/Scripts/python.exe tut.py montar-video <tutorial>     # solo G2
./.venv/Scripts/python.exe tut.py auditar <tutorial> --video  # OCR sobre el video final
```

Salida en `salida/<tutorial>/`:

| Archivo | Qué es |
|---|---|
| `video.mp4` | 1920×1080, 30 fps, voz mezclada en su instante exacto |
| `video.srt` | subtítulos **por frase**, con los tiempos reales de la voz |
| `youtube-video.txt` | título, descripción, capítulos con timestamps, transcripción |
| `miniatura-video.png` | fotograma real del video, oscurecido, con el título |
| `grabacion/master-*.mp4` | el maestro de cada corrida (se cortan de aquí los clips) |
| `grabacion/segmentos/*.json` | por paso: tramo del maestro, eventos, caja marcada, zoom |
| `audio/<paso>.json` | hash de la narración + instante de cada palabra |

## Cómo se logra la sincronía

1. **La voz se genera antes de grabar.** Así se conoce la duración de cada
   narración y el instante de cada palabra (edge-tts los reporta con
   `WordBoundary`).
2. **Cada paso es un segmento del maestro** que arranca cuando arranca su
   narración. Las acciones corren dentro de ese tramo, en tiempo real, y el
   segmento no cierra hasta que la voz terminó (+0,6 s de respiro). Si las
   acciones tardan más que la voz, el segmento se alarga: jamás se corta una
   frase. Si tardan menos, el cursor descansa sobre el elemento.
3. **El reloj del video es el reloj real.** Chrome solo entrega un fotograma
   cuando algo cambia; un hilo «bomba» escribe a ffmpeg el último fotograma
   recibido a 30 fps constantes con su propio reloj. Por construcción, el
   segundo `t` del maestro es el segundo `t` de la grabación, y el montaje
   coloca cada MP3 exactamente en el `inicio` de su segmento.
4. **`al_decir`** dispara una acción en la palabra en que la voz la menciona.
   El motor descuenta el viaje del cursor (~0,8 s), de modo que lo que coincide
   con la palabra es el **clic**, no el arranque del movimiento.

## Cómo se escribe un guion para grabar en vivo: UN paso = UNA tarea

El esquema del modo fijo (`vista` + `campos`: una marca, una frase, diez
segundos, siguiente marca) grabado en vivo sigue siendo una presentación de
diapositivas con cursor. Lo natural es lo que haría una persona grabando su
pantalla: **hacer la tarea de corrido, contar lo que va haciendo y detenerse
solo donde hace falta una aclaración**.

```jsonc
{
  "id": "02-alta",
  "ruta": "Clientes › Nuevo Cliente",
  "texto_pantalla": "Nuevo Cliente · documento, nombre y clasificación",
  "acciones": [
    { "click": "button:has-text('Nuevo Cliente')", "al_decir": "Nuevo Cliente" },
    { "resaltar": "mat-form-field.document-pair__type", "durante_ms": 4500, "al_decir": "Tipo" },
    { "escribir": { "sel": "input[formcontrolname='documentNumber']", "texto": "901234567" },
      "al_decir": "escribo el documento" },
    { "click": "button:has-text('Guardar')", "al_decir": "pulso Guardar" },
    { "resaltar": "mat-dialog-container", "durante_ms": 9000, "cursor": false, "al_decir": "aviso" },
    { "click": "mat-dialog-container button:has-text('Aceptar')", "al_decir": "Aceptar" },
    { "plano_general": true, "al_decir": "cotizar" }
  ],
  "narracion": "Pulso Nuevo Cliente, arriba a la derecha… Empieza por el Tipo de documento… Escribo el documento… Y pulso Guardar. Aparece un aviso que conviene leer… Pulso Aceptar… ya se le puede cotizar."
}
```

- **Cada pantalla se presenta antes de operarla**, para alguien que no conoce
  el sistema: qué es, qué representa cada fila o registro y para qué sirve
  («Esta es la pantalla de Clientes. Un cliente es cualquier persona, empresa
  o aseguradora a la que la clínica le cobra; cada fila es uno»). Nunca
  arrancar con «el listado» o «el formulario» como si ya se supiera qué son.
- Una narración de 30–120 s escrita como la contaría alguien que está
  haciendo la tarea; las acciones van **en el orden en que la voz las
  nombra** y cada una cae en su palabra (`al_decir`).
- `resaltar` dentro de `acciones` es la **aclaración de paso**: el recuadro
  aparece cuando la voz menciona algo, la cámara se acerca, y a los
  `durante_ms` se apaga solo y el plano se abre. No detiene la tarea.
  `"cursor": false` deja el puntero donde estaba (útil sobre un diálogo).
- **Breve.** Se dice lo que se hace y solo las aclaraciones que cambian una
  decisión o evitan un error. 40–80 s por tarea; un tutorial de submódulo
  dura 2–4 minutos. Sin portada ni cierre: el video empieza en la tarea.
- **Sin edición.** El video es la grabación tal cual: navegador a pantalla
  completa, sin zoom, sin barra inferior ni chip de ruta (`"zoom": true` y
  `"capas": true` existen, apagados). Lo que señala es el **cursor**: grande,
  con un halo ámbar que se enciende mientras viaja hacia una acción y pulsa
  al hacer clic; y el recuadro transitorio de `resaltar` para las aclaraciones.
- **Lo que se toca o se señala se ve entero.** Antes de cada clic, tecleo o
  marca el motor desplaza la página con scroll suave hasta dejar el elemento
  en el centro de la franja realmente visible, descontando la cabecera fija
  Y la barra de acciones fija de abajo (el problema clásico: el campo queda
  detrás de «Guardar»). No hace falta `desplazar` en el guion para eso.
- **Toda alerta se explica.** El motor detecta cada diálogo, toast o aviso
  que la app muestre durante el paso (evento `alerta` en el informe). Debe
  cubrirse con un `resaltar` sobre él y una frase que diga qué significa y
  qué hacer; el informe destaca la alerta que quedó sin explicar.
- `plano_general` y `quitar_marca` solo tienen efecto visible con zoom
  activo (el segundo apaga además la marca).
- `vista` + `campos` sigue disponible para pantallas de solo lectura que de
  verdad hay que recorrer elemento a elemento (una tabla de informe), pero
  es la excepción, no la regla.

## Claves nuevas del guion (todas opcionales)

```jsonc
{
  "spa": true,              // navegación interna sin recargar la app (por defecto)
  "ruta_neutra": "/",       // por dónde pasar para «volver» a la misma ruta y limpiar filtros
  "pasos": [{
    "navegar": "/health-insurance/agreements",
    "al_decir_navegar": "listado",         // cambia de pantalla al decir esta palabra
    "acciones": [
      { "click": "mat-select", "al_decir": "Estado" },        // clic al decir «Estado»
      { "click": "mat-option:has-text('Borrador')", "al_decir": "Borrador" },
      { "escribir": { "sel": "input", "texto": "DC-43" }, "al_decir": "código" }
    ],
    "campos": [
      { "sel": ".plan-summary", "al_decir": "plan", "narracion": "…" }  // la marca aparece al decir «plan»
    ]
  }]
}
```

- `al_decir` acepta una palabra, varias seguidas («Nuevo Convenio») o un número
  de segundos. Si la narración no contiene la palabra, avisa y actúa al inicio.
- Sin `al_decir`, la primera acción arranca 0,45 s después de la voz y las
  demás van encadenadas, como antes.
- `esperar_ms` y `pausa_ms` se respetan tal cual. En el modo fijo eran esperas
  «a que la pantalla se asiente antes de la foto»; aquí corren mientras la
  voz habla, así que en general se pueden acortar.

## Música de fondo (opcional)

```jsonc
{
  "musica": {
    "archivo": "marca/musica/elevator-music-mcculloch.mp3",
    "volumen_db": -24,     // atenuación fija antes de mezclar (por defecto -24)
    "ducking": true,       // baja aún más sola cuando hay voz (por defecto true)
    "fade_s": 2            // fundido de entrada y de salida, en segundos (por defecto 2)
  }
}
```

- Va en `config.json` (toda la serie) o en el guion de un tutorial concreto
  (pisa la config, igual que `voz`). **Sin la clave, el montaje queda
  EXACTAMENTE igual que hoy** — no se toca ni un filtro.
- La pista se repite en bucle para cubrir el video completo, con un único
  fundido de entrada al principio y uno de salida al final (no en cada
  clip); el `-24dB` deja la música muy por debajo de la voz (~20 dB medidos
  con `ebur128` en `salida/rrhh-import-export-empleados/`) y con
  `ducking: true` baja más todavía mientras alguien habla, con
  `sidechaincompress` usando la propia voz como disparador.
- Pistas CC0 listas para usar en `marca/musica/` (ver
  `marca/musica/LICENCIAS.md` — origen, autor y licencia de cada una).
- No cambia la duración del video ni la sincronía: cada clip solo recorta
  su tramo de la pista ya preparada, en el mismo instante que le toca dentro
  del video final.
- Con `musica` y ducking, la voz se duplica con `asplit` antes de mezclar:
  una etiqueta de filtro de ffmpeg se consume una sola vez, y usar `[voz]`
  en el `sidechaincompress` y en el `amix` hacía fallar el montaje.

## Acabado profesional (opcional): sonoridad, entrada/cierre de marca, rótulos

Tres claves independientes, en `config.json` (toda la serie) o en el guion
(pisa la config). **Sin ninguna de ellas el montaje es idéntico bit a bit al
de antes** (comprobado: mismo `video.mp4`, `video.srt` y `youtube-video.txt`,
por md5). La miniatura sí cambió a propósito con la identidad 2026 (abajo).

```jsonc
{
  "loudnorm":    { "lufs": -14, "tp": -1.5 },          // norma de YouTube
  "marca_video": { "entrada_s": 3, "cierre_s": 3 },
  "rotulo_paso": { "segundos": 3.5 }
}
```

**`loudnorm`** — normaliza la sonoridad del video ya montado, en dos pasadas:
la primera mide (`loudnorm`, integrado + pico real); la segunda aplica UNA
ganancia lineal. Si la ganancia deja los picos bajo `tp`, se aplica con
`loudnorm … linear=true`; si no cabe (la voz TTS trae picos sueltos: en
`rrhh-import-export-empleados` -19 LUFS con pico -5,9 dBTP, que +5 dB
llevaría a -0,9), en vez de dejar que `loudnorm` caiga a su modo dinámico
(comprime toda la voz) se aplica la misma ganancia con `volume` + un
`alimiter` rápido con compensación de latencia, que solo toca esos picos.
El video se copia (`-c:v copy`); solo se recodifica el audio, con los mismos
parámetros del montaje: la duración no cambia. Resultado medido con
`ebur128`: **-14,0 LUFS, pico -2,0 dBFS**. Corre después de unir, así que
cubre también la entrada y el cierre.

**`marca_video`** — antepone una entrada y añade un cierre, generados con
Pillow (1920×1080, fondo claro, Inter de `marca/fuentes/`) con la identidad
2026 de `germiva/Logos/`: `marca/logo.png` (horizontal: hoja + «Germiva» +
«ERP | Siembra control, cosecha resultados») y `marca/simbolo.png` (solo la
hoja), ambos con fondo transparente sin halo (el blanco del PNG original se
«des-mezcla»; el logo anterior quedó en `marca/_anterior/logo-2026-09.png`).
Paleta del logo: marino `#0B3552` (título), azul `#1273B8` (antetítulo),
teal `#04B19E` («Germiva ERP · Tutorial»), verde `#5BD34E` (línea de acento
y punto del rótulo). `marca.simbolo` en la config cambia el símbolo.

- Entrada: símbolo · antetítulo · título · «Germiva ERP · Tutorial». Si el
  `titulo` del guion es «Módulo · Tema», el módulo sube como antetítulo en
  mayúsculas y el tema queda como título. Aparece desde blanco y vuelve a
  blanco antes de la app.
- Cierre: logo horizontal · `url_publica` (el eslogan ya va en el logo: no
  se repite en texto). Aparece desde blanco y termina en negro.
- La miniatura (con o sin estas claves) usa la misma identidad: velo marino,
  sello del símbolo sobre placa blanca arriba a la izquierda, acento verde.
- Sin voz. Con `musica`, llevan su tramo de la pista (la pista se prepara
  del largo total, entrada y cierre incluidos) subida +3 dB, con una rampa
  de 1 s hacia la narración; sin `musica`, silencio.
- **Sincronía**: `video.srt` se corre `entrada_s`; en `youtube-video.txt`
  el primer capítulo sigue en 00:00 (YouTube lo exige) y absorbe la
  entrada, los demás se corren `entrada_s`. El informe (`informe-video.md`,
  fotogramas de `revision/`) se calcula sobre los pasos sin la entrada
  (`grabacion/cuerpo.mp4`, temporal, se borra al terminar). La miniatura no
  cambia.
- Archivos: `clips-video/_entrada.{png,mp4}` y `clips-video/_cierre.{png,mp4}`.

**`rotulo_paso`** — al empezar cada paso de video (no en tarjetas), una
píldora oscura semitransparente con un punto verde y el título del paso en
Inter Bold, abajo a la izquierda: 54 px de alto (5 % del cuadro), 112 px
del borde izquierdo (pasa la franja de iconos del menú lateral) y 34 px del
inferior, a lo sumo el 40 % del ancho (se trunca con «…»). Entra a 0,35 s y
sale a los `segundos`, con fundidos de opacidad de 0,4 s.

- Texto: la clave opcional `rotulo` del paso; si no, lo que va antes del
  primer « · » de `texto_pantalla` (convención «Pantalla · detalle»). Un
  paso sin ninguna de las dos no lleva rótulo. Pasa por la sustitución de
  privacidad.
- Se pinta después del zoom y de la barra de `capas`: el acercamiento no lo
  mueve ni lo agranda. Con `capas: true` y la barra abajo, se solaparían:
  no combinar las dos cosas.
- Las barras de acciones de la app (botones de diálogo, «Crear…») viven a
  la derecha o al centro; la esquina inferior izquierda solo tiene filas de
  tabla o el pie del menú, y el rótulo dura 3,5 s. Aun así, si un paso
  empieza con algo que hay que ver ahí, dale un `rotulo` corto o quita la
  clave en ese guion.
- La miniatura sale de un cuadro SIN rótulo (tomado del maestro).

## Qué cambia respecto al modo fijo

| | `tut build` (fijo) | `tut video` (grabación) |
|---|---|---|
| Fuente | 1 PNG por paso a 2× | screencast real a 1920×1080 |
| Cursor | dibujado con Pillow | capa DOM animada, con onda de clic |
| Acciones | ocurren fuera de cámara | ocurren en cámara, tecleo incluido |
| Zoom | `zoompan` sobre la foto | `zoompan` sobre el video, con continuidad entre pasos |
| Navegación | `goto` completo | interna al SPA (`pushState` + `popstate`), sin recargar |
| Subtítulos | un bloque por paso | por frase, con tiempos reales de la voz |
| Re-narrar | todo | solo los pasos cuya redacción cambió (hash) |
| Auditoría | frames anotados | fotogramas cada 2 s del video final (`--video`) |
| Privacidad | sustitución antes de la foto | sustitución + `MutationObserver` continuo en la página |

Lo que se conserva: guiones, seeds, `setup` (shell/SQL), sesión, `ocultar`,
`desplazar`, estilos de marca (`caja`, `subrayado`, `foco`), tarjetas de
portada/cierre, paquete de YouTube, privacidad determinista.

## Resolución y legibilidad

El navegador arranca con `--force-device-scale-factor=1.5` y un viewport de
1280×720 al 150 %: la app se comporta como en un portátil normal (media
queries en 1280) y el screencast sale a 1920×1080 físicos con el texto
grande y nítido. Comprobado: el screencast de CDP ignora el
`device_scale_factor` del contexto y captura a resolución CSS; solo esa
bandera del proceso lo cambia.

## Regrabar un solo paso

`tut video <t> --paso 05` narra lo que falte de ese grupo, lo graba en un
maestro nuevo (`master-<fecha>.mp4`) y reescribe solo sus segmentos; el
montaje toma cada segmento del maestro que le corresponde. Los maestros
viejos que ya no referencia ningún segmento se pueden borrar a mano.

## Límites conocidos

- La primera carga de la app sí es completa y sale en cámara (con la voz de
  la portada o del primer paso encima). Las siguientes pantallas se abren por
  navegación interna.
- Un paso que navega Y actúa (`navegar` + `acciones`) necesita una frase de
  entrada antes de la palabra clave, si no la acción llega tarde a la voz.
- La sustitución de datos privados corre al cargar la pantalla y después de
  las acciones; un valor real que aparezca por primera vez en medio de una
  animación puede verse unos cientos de milisegundos antes de sustituirse.
  `tut auditar --video` lo detecta.
- edge-tts necesita internet; el sidecar con el hash evita repetir llamadas.
