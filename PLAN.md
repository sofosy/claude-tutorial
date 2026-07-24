# Plan: Generador de video tutoriales para ERP

Herramienta que convierte pantallas de un sistema web en video tutoriales narrados,
con contexto de negocio y sin exponer datos privados.

---

## 1. Principio rector

**El video enseña a hacer la tarea. El contexto de negocio entra donde cambia una
decisión, no como relleno.**

Hay dos formas de fallar, y la segunda es menos obvia.

Un tutorial robótico no enseña nada porque solo dicta movimientos:

> "Haz click en el botón azul. Escribe el RFC. Presiona Guardar."

Pero un tutorial que solo teoriza tampoco sirve, porque el usuario termina el video
entendiendo el proceso y sin saber operarlo:

> "El RFC es la llave con la que el SAT reconoce a quien recibe el comprobante, y
> si queda mal capturado el cliente no puede deducir."

Lo que buscamos es la instrucción como columna vertebral, con el porqué encima
cuando el campo implica una decisión con consecuencias:

> "En **RFC del cliente** capturamos el RFC del receptor: `DBA980412H23`. Al salir
> del campo el sistema lo busca en el padrón y completa la razón social solo. Si no
> la completa, ese cliente no está dado de alta y hay que registrarlo antes de
> seguir."

La instrucción es siempre concreta —qué campo, qué valor, qué pasa después—. El
contexto de negocio aparece cuando hay algo que decidir o algo que se puede
romper, y se calla cuando el campo es evidente.

Esa mezcla no sale de un mejor prompt. Sale de que el sistema **investigue la
pantalla antes de narrarla**: qué modelo la respalda, qué valida cada campo, qué
efecto tiene guardar. Sin eso, el generador no tiene manera de saber cuáles son los
dos campos que ameritan explicación y cuáles son los diez que no. Por eso la
investigación es una etapa propia (§4) y no un paso más del guion.

---

## 2. Arquitectura: tres etapas desacopladas

```
┌─ ETAPA A ─ INVESTIGACIÓN ──────────────── (Claude, interactiva) ─┐
│  Explora la vista con Chrome MCP + lee el código si existe        │
│  Produce:  fichas/<vista>.json   ← hechos verificados             │
└───────────────────────────────────────────────────────────────────┘
                              ↓
┌─ ETAPA B ─ GUION ──────────────────────── (Claude, interactiva) ─┐
│  Convierte fichas en narrativa de negocio + pasos de captura      │
│  Produce:  guiones/<tutorial>.json   ← prosa + selectores         │
└───────────────────────────────────────────────────────────────────┘
                              ↓
┌─ ETAPA C ─ RENDER ─────────────────── (CLI determinista, sin IA) ─┐
│  Playwright → Pillow → edge-tts → ffmpeg                          │
│  Produce:  salida/<tutorial>/final.mp4 + paquete de publicación   │
└───────────────────────────────────────────────────────────────────┘
```

**Por qué desacopladas.** Cada etapa se re-ejecuta sola:

| Cambió... | Re-corres solo |
|---|---|
| La redacción de una narración | Etapa C, paso `narrar` + `montar` |
| El diseño de una pantalla | Etapa C completa (guion sigue válido) |
| Un campo nuevo en el formulario | Etapa A de esa vista, luego B y C |
| La voz o el idioma | Etapa C, paso `narrar` + `montar` |

Si todo fuera un solo proceso monolítico, corregir una coma en la narración
costaría recapturar y re-renderizar el video entero. Con esto cuesta 20 segundos.

---

## 3. Los dos modos de acceso

El requisito es que funcione **con** el código (para sembrar datos) y **sin** él
(solo navegando). Se resuelve con un bloque `setup` opcional por paso:

```json
"setup": { "tipo": "shell", "cmd": "npm run seed:factura-demo" }
"setup": { "tipo": "sql",   "archivo": "seeds/cliente-demo.sql" }
"setup": { "tipo": "http",  "metodo": "POST", "url": "/api/clientes", "body": {...} }
```

- **Con `setup`** (modo caja blanca): el CLI lo ejecuta antes de capturar. Sirve
  para dejar el ERP en el estado exacto que el paso necesita — un cliente que
  existe, un inventario con stock, una factura previa.
- **Sin `setup`** (modo caja negra): el paso es pura navegación. Un guion sin
  ningún `setup` corre contra **cualquier URL**, sin acceso al repositorio.

Mismo motor. La capacidad extra es *opt-in*, no un requisito.

**Sesión y login.** Playwright se engancha por CDP a un Chrome ya abierto
(`connect_over_cdp`), heredando tu sesión iniciada. No se automatizan credenciales
ni se guardan en ningún archivo. Alternativa para CI: `storage_state.json` generado
una vez a mano y excluido de git.

---

## 4. Etapa A — Investigación de vistas

Produce una **ficha**: el conjunto de hechos verificados sobre una pantalla. Es la
materia prima de la narración, y existe separada para que la prosa nunca invente.

### Inventario y cobertura: que no falte ninguna vista

Antes de investigar vista por vista, la Etapa A **recorre el menú completo y
enumera todo** en `fichas/mapa.json`: cada entrada de menú, cada submenú, cada
acceso rápido y cada pantalla alcanzable desde ellos.

Sin ese inventario, "cubrir todas las vistas" es una intención que nadie puede
comprobar: se documenta lo que uno recuerda y las pantallas secundarias se quedan
fuera sin que nadie lo note. Con él, la cobertura es verificable:

```
tut cobertura            # lista las vistas del mapa sin ficha o sin paso en un guion
```

El comando falla si alguna vista del mapa no está cubierta. Es lo que convierte
"están todas" en un hecho comprobable en vez de una promesa.

### Ubicación: dónde vive cada pantalla

Cada ficha registra **todas** las formas de llegar a la vista, no solo la que usó
quien la investigó:

```json
"ubicacion": {
  "ruta_menu": ["Facturación", "Listado de comprobantes"],
  "accesos": [
    { "desde": "Menú lateral", "como": "Facturación" },
    { "desde": "Panel de inicio", "como": "Acceso rápido «Nueva factura»" },
    { "desde": "Ficha del cliente", "como": "Pestaña «Facturas»" }
  ]
}
```

Una función que vive en tres lugares se enseña en los tres, porque el usuario
llega desde donde ya está trabajando, no desde donde el tutorial supone.

### Fuentes que se cruzan

| Fuente | Qué aporta | Disponible en |
|---|---|---|
| DOM en vivo (Chrome MCP) | labels, tipos, `required`, opciones de select, placeholders, textos de ayuda, mensajes de validación | siempre |
| Código del ERP | modelo/tabla, validaciones de servidor, reglas de negocio, relaciones, permisos, efectos secundarios | modo caja blanca |
| Interacción exploratoria | qué pasa al enviar vacío, qué errores dispara, qué cambia en pantalla | siempre |

### Esquema de ficha

```json
{
  "vista": "facturacion/nueva",
  "titulo_ui": "Nueva factura",
  "proposito": "Emitir un CFDI de ingreso a un cliente registrado.",
  "contexto_negocio": "Es el paso donde una venta ya cerrada se vuelve un documento fiscal. Ocurre después de confirmar el pedido y antes del cobro.",
  "quien_la_usa": ["Facturación", "Ventas (solo lectura)"],
  "precondiciones": ["El cliente debe existir con RFC válido", "Debe haber folio disponible en la serie"],
  "campos": [
    {
      "selector": "#cliente_rfc",
      "etiqueta": "RFC del cliente",
      "tipo": "text",
      "obligatorio": true,
      "que_es": "Registro Federal de Contribuyentes del receptor.",
      "por_que_importa": "Identifica fiscalmente a quien recibe el CFDI. Si es incorrecto el cliente no puede deducir el gasto.",
      "reglas": ["12 o 13 caracteres", "se valida contra el catálogo del SAT", "se autocompleta si el cliente ya existe"],
      "valor_demo": "XAXX010101000",
      "sensible": false,
      "origen": ["dom", "modelos/factura.py:L44"]
    }
  ],
  "acciones": [
    {
      "selector": "#btn-timbrar",
      "etiqueta": "Timbrar",
      "efecto": "Envía el CFDI al PAC, obtiene el UUID fiscal y descuenta inventario.",
      "irreversible": true
    }
  ],
  "rutas_alternativas": [
    {
      "para": "Crear una factura",
      "principal": "Botón «Nueva factura» en el listado",
      "alternativa": "Acción «Duplicar» en una fila del listado",
      "cuando_conviene": "Cuando se factura lo mismo cada mes: copia cliente y conceptos."
    }
  ],
  "efectos_al_guardar": ["Se genera UUID fiscal", "Se descuenta inventario", "Se crea póliza contable"],
  "errores_comunes": ["RFC con espacios", "Serie sin folios disponibles"]
}
```

`origen` es deliberado: cada afirmación apunta a de dónde salió. Si un campo dice
`"origen": ["inferido"]`, es señal de que hay que revisarlo antes de narrarlo.
**Sin origen verificable, el dato no entra al guion.**

### Cómo se genera

Claude navega la vista, toma el snapshot del DOM (que trae selectores y
coordenadas exactas), busca en el código el modelo correspondiente, y llena la
ficha. El resultado es un JSON editable: donde Claude se equivoque o le falte
contexto de negocio que solo tú sabes, lo corriges a mano una vez y queda fijo.

---

## 5. Ofuscación de datos privados

### La decisión de diseño: sustituir, no tapar

Lo obvio es difuminar o poner barras negras sobre los datos sensibles. Es mala
idea por dos razones: el video queda feo y lleno de manchas, y la narración se
vuelve imposible ("aquí va el nombre del cliente, que no te puedo decir").

El enfoque de esta herramienta es **sustituir el dato real por uno falso realista
inyectado en el DOM antes de tomar la captura**. La pantalla se ve completa,
natural y legible; simplemente dice `María Fernanda Ruiz` en vez del nombre del
cliente real. La narración puede leer el valor en voz alta sin problema, porque
es un valor inventado.

### Consistencia: mismo dato real → mismo dato falso, siempre

Crítico y fácil de arruinar. Si el mismo cliente aparece en cinco pantallas del
tutorial y en cada una se le inventa un nombre distinto, el video se vuelve
incoherente. La sustitución es **determinista por hash con semilla**:

```
falso = catalogo[ tipo ][ hash(semilla + valor_real) % len(catalogo[tipo]) ]
```

Mismo valor real → mismo falso en todos los frames y en toda la narración. La
semilla vive en el guion, no en el código.

### Reglas de detección, en orden de confianza

1. **Por selector explícito** — `{"sel": "#cliente_nombre", "tipo": "nombre"}`.
   La más confiable. Se declara en la ficha (`"sensible": true`).
2. **Por semántica de campo** — nombre del input, label o `autocomplete`
   (`email`, `tel`, `rfc`, `curp`, `iban`, `direccion`).
3. **Por patrón en el texto** — regex para RFC, CURP, CLABE, email, teléfono,
   tarjeta, IMSS. Se aplica a todo el texto visible, incluyendo tablas y PDFs
   embebidos, que es donde más se escapan los datos.
4. **Red de seguridad** — regiones declaradas como `zona_privada` en el guion
   (ej. el panel lateral con la lista real de clientes) se difuminan completas
   sin intentar clasificar nada.

### Verificación obligatoria antes de publicar

La sustitución automática no es garantía. El CLI incluye:

```
tut auditar <tutorial>    # OCR sobre cada frame final + regex de patrones sensibles
                          # Falla el build si detecta algo que parezca dato real
```

Corre sobre las imágenes **ya renderizadas**, no sobre el DOM — así detecta lo que
se coló por canvas, imágenes, PDFs o tooltips que la sustitución de DOM no alcanzó.
Y una segunda pasada sobre el texto de la narración, por si un valor real llegó al
guion. **Ningún tutorial se da por terminado sin pasar `auditar`.**

Perfiles: `estricto` (todo lo dudoso se sustituye), `moderado` (solo reglas 1-3),
`ninguno` (para datos ya demo). El default es `estricto`.

---

## 6. Etapa B — El guion: narrativa de negocio

### Separación hechos / prosa

La ficha guarda hechos. El guion guarda la prosa que los cuenta. Están separados
para que reescribir la narración no obligue a re-investigar nada, y para que la
prosa sea auditable contra los hechos que dice representar.

### Estructura narrativa de cada tutorial

```
1. APERTURA (30-45 s, sin captura o con pantalla de título)
   Qué problema de negocio resuelve este módulo.
   Dónde encaja en el proceso completo de la empresa.
   Quién lo usa y con qué frecuencia.
   Qué vas a lograr al terminar el video.

2. POR CADA VISTA
   a) UBICACIÓN (paso obligatorio): dónde vive la pantalla. Se marca
      la entrada del menú con subrayado, se muestra la ruta completa
      en pantalla, y si hay más de un acceso se marcan todos.
   b) Para qué existe esta pantalla y cuándo llegas a ella.
   c) Recorrido de campos: qué se captura, con qué valor y qué pasa
      después. Los campos triviales (un "Notas" opcional) se mencionan
      en grupo, no uno por uno.
   d) La acción y su consecuencia real en el negocio.

3. CIERRE
   Qué cambió en el sistema como resultado.
   Qué sigue en el proceso.
   Los dos o tres errores más comunes y cómo evitarlos.
```

### Reglas de estilo, explícitas en el generador

**Obligatorio:**
- **Cada paso dice qué hacer, en qué campo y con qué valor.** La instrucción es la
  columna vertebral; nunca se sustituye por teoría.
- Los elementos se nombran por su **etiqueta visible** ("el campo *Uso de CFDI*",
  "el botón *Timbrar factura*"), que es lo que el usuario ve y busca.
- Se dice **qué pasa después** de cada acción: qué se autocompleta, qué se
  recalcula, a qué pantalla te lleva.
- Primera persona plural: "capturamos", "seleccionamos", "confirmamos".
- Los valores de ejemplo se dicen en voz alta (ya son datos falsos, §5).
- El porqué se agrega **solo cuando el campo implica una decisión o tiene
  consecuencia si se equivoca** — y entonces se dice cuál es esa consecuencia.

**Prohibido:**
- Describir la interfaz por su apariencia: "el botón azul", "el ícono de la
  esquina". Si el ERP cambia de tema, la narración queda mintiendo. Para eso están
  las marcas visuales.
- Narrar uno por uno los campos evidentes. Los triviales se agrupan: "el resto de
  los campos son datos de contacto opcionales".
- Teorizar sin instrucción. Si un párrafo no dice qué hacer ni qué decidir, sobra.

### Una captura por campo

Cada campo o componente recibe **su propia captura, con una sola marca**. Marcar
cinco campos numerados en un mismo frame reparte la atención: el usuario no sabe
cuál está mirando mientras escucha, y la pantalla se ve saturada de recuadros.

En el guion se escribe con un bloque `campos`, que el cargador expande a un paso
por campo heredando navegación, ruta y setup:

```json
{
  "id": "02-datos-fiscales",
  "navegar": "/facturas/nueva",
  "campos": [
    { "sel": "#cliente_rfc", "narracion": "Empezamos por «RFC del cliente»…" },
    { "sel": "#uso_cfdi",    "narracion": "En «Uso de CFDI» elegimos G01…" }
  ]
}
```

Las marcas múltiples en un mismo frame quedan reservadas para lo que sí es
comparativo: mostrar dos accesos a la misma función, o dar el mapa general de una
vista antes de entrar al detalle.

**Primero el mapa, después el detalle.** Todo bloque `campos` abre con una toma de
la pantalla completa, sin zoom, declarada en el bloque `vista`. Encadenar
acercamientos sin haber mostrado el conjunto desorienta: el usuario ve campos
ampliados sin saber en qué parte de la pantalla están ni cuánto falta. El zoom
sobre un campo se queda en 1.45 por la misma razón — más cerrado y el campo pierde
todo su entorno.

### Anunciar los cambios de pantalla

Cuando una acción lleva a otra vista, la narración **dice a dónde llegaste**. No
como instrucción mecánica ("el botón te envió a otra pantalla"), sino nombrando el
destino y por qué estás ahí:

> "«Siguiente» nos deja en el segundo bloque del asistente, Datos de Empresa."
> "Germiva te lleva a la pantalla de verificación y manda un código al correo."

Y el paso siguiente abre con la vista completa del destino. Un tutorial donde la
pantalla cambia sin avisar obliga al usuario a reconstruir por su cuenta qué pasó,
y es donde más se pierde el hilo.

### Rutas alternativas

Cuando hay más de una forma de lograr lo mismo, el tutorial **enseña una como
camino principal y menciona la otra con el criterio para elegirla**. No se listan
todas las variantes disponibles — eso convierte el tutorial en documentación de
referencia y satura al que apenas está aprendiendo.

> "Creamos la factura con el botón **Nueva factura**. También puedes partir de una
> existente con **Duplicar**, que copia cliente y conceptos: conviene cuando
> facturas lo mismo cada mes."

Esto obliga a que la Etapa A las busque activamente, porque no se ven solas en el
DOM del formulario. La investigación debe cazar: atajos de teclado, accesos desde
otros módulos, acciones de fila en los listados, duplicar/plantilla, carga masiva
frente a captura individual, y menús contextuales. Van al campo
`rutas_alternativas` de la ficha, y el guion decide cuáles narrar.

### Esquema de guion

```json
{
  "tutorial": "facturacion-emitir-cfdi",
  "titulo": "Cómo emitir una factura",
  "voz": { "id": "es-MX-DaliaNeural", "velocidad": "-8%", "tono": "+0Hz" },
  "base_url": "http://localhost:3000",
  "privacidad": { "perfil": "estricto", "semilla": "germiva-2026" },
  "apertura": {
    "fondo": "titulo",
    "narracion": "La facturación es el punto donde una venta cerrada se convierte..."
  },
  "pasos": [
    {
      "id": "03-datos-fiscales",
      "ficha": "facturacion/nueva",
      "setup": { "tipo": "shell", "cmd": "npm run seed:cliente-demo" },
      "navegar": "/facturas/nueva",
      "acciones": [
        { "escribir": { "sel": "#cliente_rfc", "texto": "XAXX010101000" } }
      ],
      "esperar": "#datos-fiscales.cargado",
      "resaltar": [
        { "sel": "#cliente_rfc", "estilo": "caja", "color": "ambar", "etiqueta": "1" },
        { "sel": "#uso_cfdi",   "estilo": "caja", "color": "ambar", "etiqueta": "2" }
      ],
      "kenburns": { "hacia": "#datos-fiscales", "zoom": 1.35 },
      "narracion": "Estos dos campos deciden si la factura le sirve al cliente..."
    }
  ],
  "cierre": { "narracion": "Con el timbrado, el inventario ya se descontó..." }
}
```

---

## 7. Etapa C — Render

### C1. Captura (Playwright)

Por cada paso: ejecuta `setup` → navega → ejecuta acciones → espera condición →
**aplica sustitución de datos privados** → captura PNG a 2x → extrae el
`bounding_box` real de cada elemento a resaltar.

Los bounding boxes vienen del navegador, no de que Claude adivine dónde está el
botón. Es la razón por la que las marcas caen exactas.

Salida: `frames/03-datos-fiscales.png` + `frames/03-datos-fiscales.json` (cajas).

### C2. Anotación (Pillow)

Dibuja sobre el PNG usando las cajas del paso anterior:

- **Caja** — rectángulo redondeado, borde de 3px, esquinas suaves.
- **Subrayado** — línea gruesa bajo el elemento. Para entradas de menú y enlaces,
  donde un recuadro compite con el resaltado propio de la navegación.
- **Foco** — oscurece todo menos la zona marcada. El más efectivo para dirigir la
  atención en pantallas densas de ERP.
- **Flecha** — desde un margen libre hacia el elemento.
- **Numeración** — círculos `1`, `2`, `3` para secuencias dentro de un mismo frame.
- **Chip de ruta** — la ruta de navegación completa (`Menú lateral › Facturación ›
  Nueva factura`) en una etiqueta fija. Es lo que permite que un usuario que cayó
  al video por la mitad sepa dónde está parado.
- **Barra inferior** — el texto clave del paso, sobre franja semitransparente.

El chip de ruta y la barra se dibujan en una **capa aparte del tamaño final del
video**, no sobre el frame: si se pintaran encima, el zoom de C4 se los comería.

Paleta de un solo acento (ámbar sobre gris) para no competir con los colores
propios del ERP.

### C3. Narración (edge-tts)

Un archivo de audio por paso. Voz neuronal `es-MX-DaliaNeural`, velocidad -8%
(la narración técnica se entiende mejor un poco más lenta).

La duración del audio es la que **manda sobre la duración del clip**, no al revés.
Nunca se corta una frase por un tiempo fijo.

La capa de voz queda tras una interfaz de una sola función, para poder cambiar a
ElevenLabs u otro motor tocando un archivo. Edge-TTS usa un endpoint no oficial de
Microsoft y requiere internet; el aislamiento es el seguro contra eso.

### C4. Montaje (ffmpeg)

Por paso: imagen anotada + audio → clip con Ken Burns (`zoompan`) hacia el
elemento resaltado.

**Nota técnica que ahorra dolor:** `zoompan` produce zoom con temblor visible si se
aplica directo. Se resuelve renderizando a 2x y escalando abajo al final. Va
resuelto desde la primera versión, no como parche.

Luego: concatenación de clips + transiciones de 300ms + música de fondo opcional a
volumen bajo + subtítulos `.srt` generados del mismo texto de narración (gratis,
ya lo tenemos escrito, y hace el tutorial accesible).

Salida: `salida/<tutorial>/final.mp4` + `final.srt`.

---

## 8. Paquete de publicación (YouTube)

Cada tutorial produce, además del MP4, un paquete listo para subir. **No requiere
generar texto nuevo**: la narración ya está escrita en el guion y las duraciones ya
se calcularon en C3, así que los capítulos con timestamps salen exactos y sin costo.

### Qué se genera

```
salida/<tutorial>/publicacion/
├── titulo.txt          ≤100 caracteres
├── descripcion.txt     listo para pegar en YouTube
├── capitulos.txt       timestamps
├── tags.txt            palabras clave separadas por coma
├── transcripcion.md    narración completa, legible
├── final.srt           subtítulos (de C4)
└── miniatura.png       1280×720
```

### Estructura de `descripcion.txt`

```
[Resumen de negocio — 2 o 3 frases, tomadas de la apertura del guion:
 qué problema resuelve el módulo y para quién.]

⏱️ CAPÍTULOS
00:00  Introducción: por qué facturamos desde el ERP
00:38  Precondiciones: el cliente debe existir
01:24  Datos fiscales: RFC y uso de CFDI
...

📋 QUÉ APRENDERÁS
• Emitir un CFDI de ingreso a un cliente registrado
• Elegir correctamente el uso de CFDI
• Qué se descuenta del inventario al timbrar

⚠️ ERRORES COMUNES
• RFC capturado con espacios
• Serie sin folios disponibles

—
[Transcripción completa, para SEO y accesibilidad]
```

Los bloques no se inventan: "Qué aprenderás" sale de los `proposito` de las fichas,
"Errores comunes" del campo `errores_comunes`, y la transcripción de las
narraciones concatenadas. Todo trazable al mismo material verificado.

### Capítulos: agrupación, no un paso = un capítulo

YouTube exige que el primero sea `00:00`, que haya al menos 3, y que cada uno dure
**mínimo 10 segundos**. Muchos pasos narran 6-8 segundos, así que mapear paso a
capítulo produciría un archivo que YouTube rechaza en silencio.

Solución: el guion lleva un campo `capitulo` por paso, y los pasos consecutivos que
comparten el mismo se fusionan en un capítulo único.

```json
{ "id": "03-datos-fiscales", "capitulo": "Datos fiscales del receptor", ... }
{ "id": "04-uso-cfdi",       "capitulo": "Datos fiscales del receptor", ... }
```

El generador valida las tres reglas y avisa si un capítulo queda corto, en vez de
producir un archivo que falla al pegarlo.

### Miniatura

Se toma el frame más representativo (por defecto el del paso marcado
`"portada": true`), se le aplica un oscurecido y se le sobreimprime el título en
tipografía grande. Pillow, mismo estilo visual que las anotaciones.

### La descripción también pasa por la auditoría de privacidad

Es el punto por donde más fácil se escapa un dato: la transcripción va completa en
la descripción, y una descripción de YouTube es **pública e indexable por Google**.
`tut auditar` corre las mismas regex sobre `descripcion.txt` y `transcripcion.md`,
no solo sobre los frames.

---

## 9. Estructura del proyecto

```
germiva-tutorial/
├── PLAN.md                   este documento
├── tut.py                    CLI
├── tutorial/
│   ├── investigar.py         soporte para etapa A
│   ├── capturar.py           Playwright + sustitución de datos
│   ├── privacidad.py         detección, sustitución determinista, auditoría
│   ├── anotar.py             Pillow
│   ├── narrar.py             edge-tts (interfaz de un solo punto de cambio)
│   ├── montar.py             ffmpeg
│   ├── publicar.py           título, descripción, capítulos, tags, miniatura
│   └── catalogos/            nombres, RFCs, direcciones falsas para sustituir
├── fichas/mapa.json          inventario de vistas y accesos (etapa A)
├── fichas/<vista>.json       hechos verificados (etapa A)
├── guiones/<tutorial>.json   narrativa + pasos (etapa B)
├── seeds/                    scripts de datos previos (modo caja blanca)
└── salida/<tutorial>/
    ├── frames/  audio/  clips/
    ├── final.mp4  final.srt
    ├── publicacion/          paquete para YouTube
    └── auditoria.txt         resultado del chequeo de privacidad
```

## 10. CLI

```bash
tut mapa <url>                           # → fichas/mapa.json (inventario de vistas)
tut investigar <url> [--codigo <ruta>]   # → fichas/<vista>.json
tut guion <ficha...>                     # → guiones/<tutorial>.json (borrador)
tut cobertura                            # vistas del mapa sin ficha o sin narrar

tut capturar <tutorial>                  # etapa C1
tut anotar   <tutorial>                  # C2
tut narrar   <tutorial>                  # C3
tut montar   <tutorial>                  # C4
tut publicar <tutorial>                  # paquete YouTube (§8)
tut build    <tutorial>                  # C1→C4 + publicar + auditar
tut auditar  <tutorial>                  # privacidad: OCR en frames + regex en textos

tut build <tutorial> --paso 03           # rehace un solo paso
tut preview <tutorial> --paso 03         # abre el frame anotado, sin video
```

---

## 11. Implementación por fases

**Estado al 24/07/2026**

| Fase | Estado |
|---|---|
| 1 · Esqueleto del render | implementada y verificada |
| 2 · Privacidad | implementada: sustitución determinista, 4 reglas de detección, `tut auditar` con OCR |
| 3 · Inventario e investigación | `tut mapa` y `tut cobertura` implementados; las fichas son la etapa interactiva (§4) |
| 4 · Narrativa | reglas de estilo aplicadas; el guion se escribe a mano contra las fichas |
| 5 · Paquete de publicación | implementada: `youtube.txt` con capítulos + `miniatura.png` |
| 6 · Pulido | disolvencias y subtítulos hechos; faltan música e intro de marca |


Cada fase con un criterio de terminado verificable — no "quedó bien", sino algo
que se comprueba corriéndolo.

### Fase 1 — Esqueleto del render (C1→C4)
Un guion de ejemplo de 3 pasos contra un sitio público cualquiera.
**Verificable:** `tut build ejemplo` produce un `final.mp4` reproducible, con voz
en español, marcas encima de los elementos correctos y zoom sin temblor.

### Fase 2 — Privacidad
Sustitución determinista + detección por selector, semántica y regex + `tut auditar`.
**Verificable:** un guion con datos reales sembrados produce un video donde el OCR
de los frames no encuentra ni un solo dato original, y el mismo cliente aparece con
el mismo nombre falso en los 3 pasos.

### Fase 3 — Inventario e investigación de vistas
Etapa A contra tu ERP: `tut mapa` recorre el menú y enumera todas las vistas;
`tut investigar` produce las fichas con campos, reglas, ubicación y contexto.
**Verificable:** `tut cobertura` no reporta ninguna vista sin ficha, y tú lees la
ficha de una vista real y confirmas que sus campos, sus accesos y su contexto de
negocio son correctos (cada dato con `origen` rastreable).

### Fase 4 — Narrativa
Generación de guion desde fichas con las reglas de estilo de §6.
**Verificable:** escuchas el tutorial completo de un módulo real y no aparece ni
una sola frase del tipo "haz click en el botón".

### Fase 5 — Paquete de publicación
Título, descripción, capítulos, tags, transcripción y miniatura (§8).
**Verificable:** pegas `capitulos.txt` en un video de YouTube y los capítulos
aparecen correctamente (los tres requisitos: primero en `00:00`, mínimo 3, mínimo
10 s cada uno), y `tut auditar` no encuentra datos sensibles en `descripcion.txt`.

### Fase 6 — Pulido
Transiciones, música, subtítulos estilizados, pantalla de título e intro/outro de marca.

---

## 12. Riesgos y cómo se manejan

| Riesgo | Manejo |
|---|---|
| Edge-TTS deja de funcionar (endpoint no oficial) | Capa de voz aislada tras una interfaz; cambiar de motor toca un archivo |
| Un dato privado se escapa al video | `tut auditar` con OCR sobre frames finales, obligatorio antes de publicar |
| Un dato privado se escapa a la descripción pública de YouTube | La misma auditoría corre sobre `descripcion.txt` y `transcripcion.md`, que son indexables por Google |
| Claude inventa reglas de negocio en la ficha | Campo `origen` por dato; lo `inferido` se revisa a mano antes de narrar |
| El ERP cambia y los selectores se rompen | Falla ruidosa en captura indicando el paso y selector; se re-corre solo ese paso |
| Videos que envejecen mal | El costo de regenerar es bajo por diseño; la separación en etapas es justamente esto |

---

## 13. Dependencias

Ya disponibles: `ffmpeg`, `python3`, `Pillow 12.1.1`, MCP de Chrome DevTools.

Por instalar (en venv local): `edge-tts`, `playwright` (+ Chromium ~150 MB),
`pytesseract` + `tesseract` (solo para `tut auditar`).
