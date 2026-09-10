# claude-tutorial

Generador de video tutoriales para aplicaciones web. Toma una app real, la
recorre paso a paso, marca los componentes de los que habla, narra con voz
sintética y entrega un MP4 listo para YouTube — con subtítulos, capítulos y
descripción.

Está pensado para documentar un ERP, pero funciona contra cualquier sitio web.

```
guion.json ──> [1] Playwright ──> capturas + coordenadas reales de cada elemento
           ──> [2] Pillow     ──> recuadros, subrayados, cursor, barra de texto
           ──> [3] edge-tts   ──> narración en español
           ──> [4] ffmpeg     ──> acercamientos, disolvencias ──> final.mp4
```

## Qué lo diferencia de una grabación de pantalla

- **Las marcas caen exactas.** Las coordenadas las reporta el navegador, no se
  estiman: si el diseño cambia, la marca sigue sobre el elemento correcto.
- **Se regenera.** Cambió una pantalla o una frase: se re-corre el paso, no se
  regraba el video entero.
- **Sustituye los datos privados** por otros inventados, de forma determinista, y
  audita el resultado con OCR sobre los frames finales.
- **La duración la manda el audio**, nunca un tiempo fijo, así que jamás se corta
  una frase a la mitad.

## Instalación

```bash
python3 -m venv .venv
./.venv/bin/pip install edge-tts playwright pillow pytesseract
./.venv/bin/playwright install chromium
brew install ffmpeg tesseract      # macOS

cp config.ejemplo.json config.local.json   # y ajusta las rutas de tu máquina
```

### En Windows

```powershell
python -m venv .venv
.\.venv\Scripts\pip install edge-tts playwright pillow pytesseract
.\.venv\Scripts\python -m playwright install chromium chromium-headless-shell
winget install Gyan.FFmpeg          # ffmpeg y ffprobe, sin administrador
```

Dos cosas que no salen solas:

- **`chromium-headless-shell`** hay que pedirlo aparte. El motor lanza el
  navegador en modo headless, y sin ese binario la captura muere en el primer
  paso aunque `playwright install chromium` haya terminado bien.
- **Tesseract** (la auditoría OCR) solo se distribuye como instalador que exige
  administrador. Si no lo tienes, extrae el instalador en tu perfil y declara la
  ruta del binario en `config.local.json` → `"tesseract"`; el motor la usa sin
  necesidad de que esté en el PATH:

  ```powershell
  # 7-Zip portátil, extraído del MSI (no requiere administrador)
  curl -o 7z.msi https://www.7-zip.org/a/7z2301-x64.msi
  msiexec /a 7z.msi TARGETDIR="$env:LOCALAPPDATA\7zip-portable" /qn
  # y con él, Tesseract
  curl -o tess.exe https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe
  & "$env:LOCALAPPDATA\7zip-portable\Files\7-Zip\7z.exe" x tess.exe -o"$env:LOCALAPPDATA\Tesseract-OCR"
  ```

`ffmpeg` recién instalado no está en el PATH de las consolas ya abiertas: abre
una nueva antes de `tut narrar` o `tut montar`.

## Uso

**Modo de grabación en vivo** (recomendado — ver [`GRABACION.md`](GRABACION.md)):
la pantalla se graba mientras el guion se ejecuta, con cursor, clics y tecleo
reales, y la voz sincronizada palabra por palabra.

```bash
./.venv/bin/python tut.py verificar ejemplo         # cada clic y cada vista se explican (exit 0)
./.venv/bin/python tut.py video ejemplo             # voz → grabar → montar → informe-video.md
./.venv/bin/python tut.py video ejemplo --paso 05   # regrabar solo un grupo
./.venv/bin/python tut.py auditar ejemplo --video   # OCR sobre el video final
open salida/ejemplo/video.mp4
```

El guion lo escribe una sesión (Opus/Sonnet) y otra lo rectifica con
`informe-video.md` + `revision/clics.png`; el skill `germiva-video` del
workspace describe los dos roles y las reglas de un guion grabado en vivo.

Modo fijo original (una foto por paso con Ken Burns):

```bash
./.venv/bin/python tut.py build ejemplo     # captura, anota, narra y monta
./.venv/bin/python tut.py auditar ejemplo   # revisa que no se filtren datos reales
open salida/ejemplo/final.mp4
```

Etapas sueltas, para iterar sin rehacer todo:

```bash
tut capturar <tutorial> [--paso 03]   # navega y captura
tut anotar   <tutorial>               # marcas, cursor y textos
tut narrar   <tutorial>               # voz
tut montar   <tutorial>               # video + subtítulos + youtube.txt
tut mapa     <tutorial>               # inventario de vistas de la app
tut cobertura                         # vistas que ningún guion narra todavía
```

Corregir una redacción cuesta `narrar` + `montar`. Cambiar el diseño de una
pantalla cuesta re-capturar ese paso. Esa es la razón de que las etapas estén
separadas.

## Configuración

| Archivo | Qué contiene | ¿Se versiona? |
|---|---|---|
| `config.json` | Marca, voz, dominio público, privacidad, etiquetas | sí |
| `config.local.json` | Rutas de tu máquina (`tesseract`, cliente de MySQL), acceso a la base, credenciales de demo | **no** |
| `guiones/<nombre>.json` | El tutorial concreto | sí |

Se fusionan en ese orden, y el guion gana. Todo lo compartido vive en
`config.json` para que **todos los tutoriales salgan iguales** sin repetirlo.

Un ejemplo de lo que resuelve esa separación: los videos se graban contra
`localhost` pero se publican para clientes, así que `url_publica` reescribe la
barra de direcciones al dominio real. El video enseña la dirección a la que el
usuario tiene que llegar, no la de tu máquina.

## Anatomía de un guion

```json
{
  "titulo": "Cómo registrarse",
  "pasos": [
    {
      "id": "01-formulario",
      "capitulo": "Datos del representante",
      "navegar": "/authentication/signup",
      "ruta": "Registro › Representante Legal",
      "vista": { "narracion": "Este es el formulario…" },
      "campos": [
        {
          "sel": "input[formcontrolname='email']",
          "acciones": [{ "escribir": { "sel": "input[formcontrolname='email']",
                                       "texto": "{{correo_demo}}" } }],
          "texto_pantalla": "Correo · será tu usuario para entrar",
          "narracion": "«Correo» es el campo crítico…"
        }
      ]
    }
  ]
}
```

- `vista` antepone una toma de la pantalla completa: primero el mapa, después el
  detalle.
- `campos` genera **una captura por campo**, con una sola marca cada una. Marcar
  cinco campos a la vez reparte la atención.
- `{{variable}}` se resuelve desde `config.local.json` o desde una consulta SQL.

### Dejar el sistema listo antes de capturar

```json
"setup": { "tipo": "shell", "cmd": ".venv/bin/python seeds/limpiar_demo.py" }
"setup": { "tipo": "sql", "query": "SELECT codigo FROM users WHERE …",
           "guardar_en": "codigo" }
```

El resultado de una consulta se usa después como `{{codigo}}`. Es lo que permite
grabar un flujo con código de verificación por correo sin depender de que el
correo llegue.

`navegar` también admite `{{variable}}`. El número de un documento lo genera la
aplicación al crearlo, así que no se puede escribir en el guion; con `setup: sql`
el paso lo consulta y salta directo a él:

```json
"setup":   { "tipo": "sql", "guardar_en": "cotizacion",
             "query": "SELECT numero FROM quotes WHERE referencia='TUT-01'" },
"navegar": "/sales/quotes/edit/{{cotizacion}}"
```

Poner ese `setup` en **cada** paso que use la variable es lo que hace que
`tut capturar <tutorial> --paso 12` funcione por sí solo, sin depender de que
antes se haya corrido el paso que la definió. Es la diferencia entre rehacer una
toma en diez segundos o volver a capturar el video entero.

Un guion **sin** ningún `setup` corre contra cualquier URL, sin acceso al código
de la aplicación.

### Avisos que tapan la primera pantalla

Un ERP suele recibirte con un modal de notificaciones o una franja de aviso, y si
no se despachan salen en todos los fotogramas. Se cierran una sola vez, al
entrar, con las mismas acciones del guion:

```json
"sesion": { "usuario": "…", "clave": "…",
            "acciones": [{ "click_opcional": "mat-dialog-container button:has-text('Cerrar')" }] }
```

`click_opcional` no falla si el aviso no apareció.

## Privacidad

El perfil `estricto` sustituye datos sensibles por otros inventados **antes** de
la captura. Se sustituye en vez de difuminar: la pantalla queda completa y
legible, y la narración puede leer los valores en voz alta porque son falsos.

La sustitución es determinista por hash con semilla, así que el mismo cliente
conserva el mismo nombre inventado en todas las pantallas y en el audio. Los
valores generados llevan marcas convencionales de ficción (rango `555`, dominio
`ejemplo.com`) para que la auditoría distinga lo inventado de lo real.

```bash
tut auditar <tutorial>   # OCR sobre los frames finales + regex sobre los textos
```

Corre sobre las **imágenes renderizadas**, no sobre el DOM: así detecta lo que se
cuela por canvas, PDFs incrustados o tooltips. Revisa también la descripción de
YouTube, que es pública e indexable. Sale con código de error si encuentra algo.

## Salida

```
salida/<tutorial>/
├── final.mp4        1920×1080, con subtítulos quemados en el .srt aparte
├── final.srt
├── youtube.txt      título, descripción, capítulos con timestamps y transcripción
├── miniatura.png    1280×720
├── auditoria.txt    resultado del chequeo de privacidad
└── privacidad.json  mapa real → inventado, para mantener la coherencia
```

## Documentación

- [`PLAN.md`](PLAN.md) — el diseño completo y por qué cada decisión es como es.
- [`PROMPT.md`](PROMPT.md) — cómo pedirle a Claude Code que arme un tutorial nuevo.
