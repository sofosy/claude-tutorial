# BRIEF — Serie «Cajas» (7 videos) · contrato común de los autores · 2026-09-23

Lee en este orden: skill `germiva-video` (`germiva/.claude/skills/germiva-video/SKILL.md`, reglas
R0–R30 y «Falsos positivos»), `GRABACION.md`, `_SERIE-CAJAS.md` (qué va en cada video),
`_SELECTORES-CAJAS.md` (selectores VERIFICADOS en el DOM vivo — la única fuente de selectores),
`exploracion-cajas/` (capturas + json por pantalla), `_DATOS-CAJAS.md` §0 y `seeds/cajas/README.md`
(estados S0…S6), `_HALLAZGOS-CAJAS.md` (no se enseña ningún defecto como si fuera correcto).

## Cambios sobre `_SERIE-CAJAS.md` (decididos)
- Empresa demo **43 «Ferretería El Progreso»**, no la 29. Usuarios: `admin.progreso`,
  `yohanna.peralta`, `luis.batista`, `carmen.rosario`, clave `Demo2026!`.
- **Video 2 lleva un paso 04 «Configurar la impresora»** (pedido expreso del usuario), grabado por
  `admin.progreso` partiendo de **S2i** (sesión del admin abierta en Caja Principal, así aparece el
  ⋮ «Ajustes de este equipo» de Mi caja). Como el paso 04 parte de otro estado, el video 2 se graba
  en DOS tandas: pasos 01–03 desde S0 (`tut.py video`), luego `restaurar S2i` y
  `tut.py grabar <guion> --paso 04` + `montar-video` — por eso el paso 04 debe ser AUTOSUFICIENTE
  (su propio `navegar` y frase de apertura, R23e). Contenido: qué es la estación y por qué la
  impresora se configura en el equipo que la tiene conectada; «Imprimir recibo al facturar» y
  «Abrir gaveta al facturar»; «Detectar» (WebUSB) se SEÑALA y se explica, NUNCA se pulsa (abre el
  selector nativo); Vendor ID `0483`, Product ID `070b`, Tipo de conexión «USB Directo (WebUSB)»
  (explicar las otras tres en una frase); «Guardar» → toast «Impresora configurada exitosamente».
  La voz dice que configurar la impresora lo hace un administrador (H-01: la cajera ve el menú pero
  no puede guardar — NO se muestra ese error; es hallazgo).
- NO existe `button.panel-collapse` en Cajas: el menú es un riel fijo. Ningún guion lo usa;
  `revisar.mjs` avisará de su ausencia en el paso 01 → ignorar ese AVISO, justificado.
- Ajustes medidos: arqueo sorpresa por **3,050**; la alerta de saldo bajo del video 7 sale
  **Resuelta**; el período por defecto de Análisis es «Este mes»; aprobar desde el detalle del
  cuadre pide una segunda confirmación; «Continuar» de Generar cuadre choca con el FAB del chatbot
  (desplazar / marcar otra cosa); «Siguiente»/«Registrar conteo» y la cola de cuadres caen bajo el
  pliegue (el motor centra solo antes de cada acción; no hace falta `desplazar`, pero verifícalo en
  el ensayo).

## Cabecera obligatoria de cada guion (`guiones/cajas-0N-<slug>.json`)
```jsonc
{
  "titulo": "Cajas · <título corto>",
  "base_url": "http://localhost:4200",
  "sesion": { "usuario": "<rol>", "clave": "Demo2026!", "sel_entrar": "button.auth-primary-btn" },
  "voz": { "id": "es-DO-RamonaNeural", "velocidad": "+15%" },
  "musica": { "archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -26, "ducking": true, "fade_s": 2 },
  "privacidad": { "permitidos": ["germiva", "1305550", "progreso", "yohanna", "peralta", "luis.batista", "batista", "carmen", "rosario", "admin.progreso", "santiago", "mostrador"] },
  "aprenderas": [ … ], "errores_comunes": [ … ],
  "pasos": [ … ]
}
```
Comprueba en `tutorial/privacidad.py` (perfil estricto) que ningún dato demo en pantalla se
sustituya por otro (la voz lo nombra y el subtítulo debe casar); si algo más hay que permitir
(p. ej. montos, MOV-00009, REC-2026-…), añádelo a `permitidos` del guion.

## Estilo (resumen del skill, no negociable)
- Español dominicano, tuteo, acentos correctos; etiquetas de la UI entre comillas «» tal cual.
- Cada pantalla se presenta primero para un novato (qué es, qué es cada fila/tarjeta, para qué).
- UN paso = UNA tarea, 40–80 s; video 2:00–4:10. Nada de portada ni cierre.
- R0: nunca >10 s sin que la pantalla cambie → marca lo que la voz nombra, o recorta.
- R2: cada `al_decir` UNA vez en su paso; 2–3 s de habla entre un tecleo y la siguiente ancla.
- R9/R10/R25: toasts (3,5 s) se marcan SIN `al_decir`, justo después del clic que los provoca,
  `durante_ms` 3000–3500, `"cursor": false`; diálogos de confirmación: marca propia.
- R1/R24: NUNCA `esperar` en un paso que cambia de pantalla.
- R5b: marca celdas `td:nth-child(N)`, no filas ni tablas enteras. R11: nada sobre el FAB.
- Siglas (ITBIS, MOV, REC, TRF…) se explican la primera vez; la fonética va en `pronunciacion`, no
  en la narración.
- Las cifras que dice la voz tienen que ser las que muestra la pantalla en ese estado (míralas en
  `exploracion-cajas/*.json`).

## Ciclo de cada autor (en este orden, sin saltarse nada)
1. Escribe el guion. `.venv/Scripts/python.exe tut.py verificar <guion>` → 0 errores.
2. `node seeds/_puertas/revisar.mjs <guion>` → 0 ERROR (AVISOS justificados en `_comentario`).
3. ENSAYO (escribe en la base, usa navegador) bajo cerrojo: crea
   `seeds/_puertas/NAVEGADOR.lock` en modo exclusivo (`fs.openSync(p,'wx')` / `open(p,'x')`) con
   contenido `ENSAYO <guion>` desde un proceso que siga vivo — o, más simple, un script propio
   que tome el cerrojo, haga `node seeds/cajas/restaurar.mjs <S de partida>` →
   `.venv/Scripts/python.exe seeds/_puertas/ensayar.py <guion>` → `restaurar <S de partida>` y
   suelte el cerrojo SOLO si su contenido es el suyo. Si el cerrojo existe, espera (sondea cada
   20 s). El log del ensayo DEBE tener líneas `── paso` (R28). 0 FALLOS y revisa las capturas de
   `salida/<guion>/ensayo/`.
4. Itera hasta pasar las tres puertas. NO GRABES: la grabación la hace el orquestador en serie.
5. Entrega: guion + `_INFORME-AUTOR-<guion>.md` corto (estado de partida, qué escribe, AVISOS
   justificados, dudas).

Máquina: 15,7 GB con ~9 en reposo. Un navegador a la vez (cerrojo). Nada de builds, tests,
ng serve ni reiniciar apps (API en :3001, front estático en :4200 ya arriba). No toques
`tutorial/*.py`, `seeds/_puertas/*` ni `seeds/cajas/*` (si una herramienta falla, repórtalo).
No corrijas el ERP.
