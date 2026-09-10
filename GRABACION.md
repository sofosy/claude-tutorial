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
