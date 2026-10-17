# Ensayo · serie «Seguridad» · tanda 2 (OPERADOR-ENSAYO, 2026-09-27)

Guiones: 04a, 04b, 04c, 05, 06a, 06b y 06c. Apps: API `dist` :3001 y front estático :4200, sin reiniciar. Un solo
navegador headless 1280×720 (dsf 1.5). Cada ensayo y cada sonda corrieron bajo `seeds/_puertas/NAVEGADOR.lock`
(«ENSAYANDO <guion> <pid>»). El cerrojo se tomó con `wx` desde el proceso node vivo que lanzaba el ensayo, y solo se
borró si el contenido seguía siendo el suyo. Antes y después de cada corrida se restauró el estado de partida: E0, o
E6c + `node marca/demo-integracion/preparar.mjs --estatico` en 06b/06c. Al terminar quedó **E0**. Los logs llevan
líneas `──` de paso (R28) y están en `germiva/qa-seguridad-ensayos-2026-09-27/<guion>/ensayo-*.log`, junto a las capturas.

## Resultado

| Guion | Estado | Pasos | Acciones (ensayo) | Fallos 1.ª → final | revisar | verificar | Duración estimada |
|---|---|---|---|---|---|---|---|
| 04a-personas | E0 | 5 | 48 | 17 (1 raíz) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:40 + 6 s ≈ **3:46** |
| 04b-alta-y-edicion | E0 | 5 | 63 | 0 (tiempos) → **0** | 0 ERROR · 2 AVISO | 0 · 0 | 3:58 + 6 s ≈ **4:04** |
| 04c-equipos | E0 | 5 | 52 | 0 (afirmación falsa) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:21 + 6 s ≈ **3:27** |
| 05-acceso-efectivo | E0 | 4 | 30 | **0** | 0 ERROR · 1 AVISO | 0 · 0 | 2:33 + 6 s ≈ **2:39** |
| 06a-credenciales | E0 | 5 | 42 | 0 (1 marca pegada arriba) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:43 + 6 s ≈ **3:49** |
| 06b-rotar-pausar-revocar | E6c | 4 | 39 | 0 (1 CORTADO + tiempos) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 2:36 + 6 s ≈ **2:42** |
| 06c-caso-integracion | E6c | 5 | 35 | 0 (1 marca pegada arriba) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 2:23 + 6 s ≈ **2:29** |

Avisos que quedan, todos justificados:

- En los siete: el primer paso no pulsa `button.panel-collapse`, porque no existe en `/security/*` ni en la lámina.
- 04b, segundo aviso: «dos marcas a la vez» en 05-eliminar. Es un artefacto de la predicción: la marca del toast va sin
  ancla y el motor la pinta cuando el toast existe, 4–11 s después y no a los 0,4 s.

## Fallos y correcciones

### 04a-personas
- **Filtro Rol (raíz de 17 fallos en cascada):** tras elegir un rol, el botón deja de decir «Rol» y pasa a decir
  «Almacén». Ya no casaba `button:has-text('Rol'):has(…)`, el menú no se abría y el resto del guion quedó tapado.
  Los dos clics usan ahora `.sec-people button:has(mat-icon:text-is('filter_list'))` (count 1).
- La marca sobre `.mat-mdc-menu-panel` salía CORTADO: el panel mide 477 px y va de y=243 a 720. Pasa a
  `…button:has-text('Mensajero')`, y la voz dice «arriba los de la empresa, como Mensajero, y debajo los del sistema».
- **D-S13 corregido en la ficha:** «Últimos ingresos» dice «Hace 4 h · Chrome · Windows». Se quitó la frase «Aquí dice
  Cliente de API…» (falsa) y el ancla pasa a «Chrome en Windows».
- **Ver su actividad:** la fila de arriba es «11:07 · Ana Mejía · Actualizó · Precio #797». El «Acceso» de Ana está
  en y≈2043, abajo del todo. La marca pasa a `.sec-audit__row >> nth=0` y la voz dice «Arriba está lo más reciente:
  aquí, que actualizó un precio». D-S7 queda confirmado: los registros se leen «Precio», «Historial de precios» y
  «Versión de cotización».

### 04b-alta-y-edicion (tiempos, R16/R25)
- **Alta:** el diálogo tarda 6,4–8 s en el ensayo y hasta 11 s según la ronda 2. Ahora va así:
  - marca sin demora sobre `button:has-text('Creando usuario')`, que confirma el indicador de D-S12;
  - relleno «Fíjate en el usuario» a los +4 s;
  - marca del diálogo anclada a «Mientras tanto» (+10,4 s). Si el diálogo aún no existe, el motor espera hasta 15 s,
    así que nunca queda más de 8 s sin marca.
  - «Pulso Aceptar» a los +18 s.

  La voz ya no dice «los botones quedan en espera»: dice «El botón dice Creando usuario».
- **Eliminar:** tarda 4,6 s en la sonda aislada, 6,7–9,2 s en los ensayos y más de 11 s si se elimina justo después
  de crear. Mientras dura, el panel muestra «Eliminando…» (`.sec-people__busy`), que ahora se marca. La voz se alargó y
  «otra vez nueve» cae a +14,5 s del clic.
- Se quitó la frase «Tampoco puedes dar permisos que tú no tienes, ni dejar a alguien sin roles.», que no estaba
  verificada y dejaba el video en 4:09.
- Todos los demás selectores del informe existen: `.sec-people__card-name`, `.sec-people__block-title >> nth=0`,
  `.person-roles__line--add` y `mat-dialog-container:has-text('Operación completada')` con el formulario detrás.
  Tras activar, la fila de la lista vuelve a «Activa».

### 04c-equipos (afirmación falsa → E-6)
- El riel de Equipos **no muestra el número de miembros**: `.gm-rail-count` sale vacío. Se quitaron dos frases:
  - «cada uno con su número de miembros» pasa a «esta empresa tiene uno solo»;
  - «en el riel Zona Norte ya tiene dos» pasa a «en la lista Carlos ya lleva Zona Norte al lado de su correo; Héctor
    también», con la marca sobre `.sec-people__who:has-text('Carlos Pimentel') .gm-sheet-meta`.
- Se confirmaron `.sec-people__teams-label`, `.sec-people__title`, `.sec-people__none` («Sin equipos todavía»), los
  toasts «agregadas / quitada / eliminado» y los dos diálogos de eliminar.

### 05-acceso-efectivo
Sin cambios.

- La lámina `acceso-efectivo` abre y revela las fases 2, 3 y 4, con «11 en total; aquí, 4 de ejemplo».
- En la ficha, el orden de los roles de José es Almacén → Vendedor, que es el orden que dice la voz.
- Carlos tiene 7/19 en Cotizaciones y 2/79 en Facturación. Luisa sale «Sin ningún rol» y «Ningún permiso concedido».

### 06a-credenciales
- `.page-title`, en la página de permisos, está en y=80, pegado al borde superior, y no se puede centrar (R5b: llega
  1,5 s tarde). Se cambió por `mat-card.info-card` (la tarjeta con el prefijo y los permisos activos), anclada a
  «los datos de la credencial».
- La franja del secreto aparece a los 3,1 s. Después de desmarcar «Registrar Facturas de Compra», el panel dice
  **4** y Compras desaparece, que es justo lo que dice la voz. Al volver con «Volver a Integraciones» el panel sigue
  abierto.

### 06b-rotar-pausar-revocar
- **Documentación de la API (E-7):** la página se pinta debajo de la barra superior y del riel. Por eso el `h1` salía
  CORTADO (y=24..68). La marca pasa al primer bloque de código, `.api-docs-content pre >> nth=0` («POST
  /api/auth/integration/login»), que es lo que la voz describe como «cómo entra un programa». La barra lateral sigue
  cortada por la izquierda. Es un defecto del ERP y la voz no lo lee.
- **Tiempos:** desactivar tarda 4,1–5,4 s, activar 3,2–3,6 s y revocar 3,1–4,1 s. Se añadió voz de relleno para que
  «dice Inactiva» caiga a +8,4 s del clic, «otra vez Activa» a +5 s y «queda una sola» a +6 s.
- El Resumen, después de revocar, dice «3 asuntos» y ninguno es de credenciales. Confirmado.

### 06c-caso-integracion
- `.page-title` pasa a `mat-card.info-card`, igual que en 06a.
- **La lámina, confirmada en el navegador:**
  - `#btn-conectar` responde «Conectado · Germiva entregó un pase válido por 24 horas».
  - Las facturas dan **200 · Permitido** y «Germiva entregó 3 facturas»: B0100000001 Constructora Mirador Emitida,
    B0200000001 Consumidor Final Emitida y 1000000003 Ferretería Doña Luz Borrador.
  - Los productos dan **403 · Rechazado**. El mensaje se lee bien: «No tienes el permiso requerido para acceder a este
    recurso: «Productos». Solicita acceso a tu administrador.», seguido de «Germiva no entregó ningún dato.». El
    código técnico va aparte y en pequeño.
  - Después de conceder, sale **200** y «Germiva entregó 25 productos». La cifra «veinticinco» de la voz es cierta.
  - La sesión de la lámina sobrevive a la vuelta al ERP y sigue «Conectado».
- De las tres casillas «PRODUCT_VIEW», el selector de exclusión elige la correcta. El toast dice «Permiso concedido
  exitosamente».

## Tiempos medidos (para la grabación)

| Operación | Tiempo |
|---|---|
| Login (sesión, fuera de cámara) | 7,4–8,7 s |
| Alta de usuario (clic → «Operación completada») | 6,4–8 s en el ensayo (hasta 11 s según la ronda 2) |
| Editar / cambiar contraseña | ≈3 s |
| Desactivar / activar usuario | 3,7–4,1 s / 1,4–3,7 s |
| Eliminar usuario | 4,6–9,2 s, y más de 11 s justo después de crear |
| Generar / rotar secreto | 3,1–3,7 s |
| Desactivar / activar / revocar credencial | 3,5–5,4 s / 3,2–3,6 s / 3,1–4,1 s |
| Casilla de permiso de la credencial | ≈1,3 s |
| Equipos (crear, agregar, quitar, eliminar) | ≤ 0,3 s |

## Defectos del ERP anotados (HALLAZGOS-SEGURIDAD-VIDEO.md › Ensayos › Tanda 2)

- **E-6:** en el riel de Equipos falta el número de miembros.
- **E-7:** la Documentación de la API queda debajo de la barra superior y del riel.
- **E-8:** en «Permisos de Integración», el título va pegado al breadcrumb y las etiquetas de módulo están en inglés
  («COMPANY»).
- **E-9:** tiempos de usuarios y credenciales con MySQL local (N-4).

## Herramientas usadas (scratchpad, fuera del repo)
- `ens.mjs`: cerrojo → restaurar → `ensayar.py --salida <qa>` → restaurar → soltar el cerrojo si es suyo.
- `sonda.py` / `sonda.mjs`: con la misma sesión y las mismas funciones del motor (`ensayar._una`), ejecuta acciones,
  cuenta selectores, evalúa JS y captura. Va bajo el mismo cerrojo y restaura.

## Pendiente para el orquestador
- 04b dura ≈4:04. Si la voz real sale más lenta de 2,9 palabras/s, recortar en 01 la aclaración del WhatsApp o la del
  correo que ya existe.
- 06c: borrar `marca/demo-integracion/credencial.local.json` y su copia en `fe-estatico-seguridad/browser/demo-integracion/`
  al cerrar la serie.
- La API Key completa (`gv_live_…`) se ve en la franja de 06a y 06b. Cambia en cada toma. Si el revisor la quiere
  tapada, añadirla a `privacidad.mapa_fijo` después de grabar.
