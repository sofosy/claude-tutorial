# Revisión semántica — Cajas 05, 06, 07 (REVISOR, 2026-09-23)

Los tres videos ya pasaron la puerta mecánica (`veredicto.mjs` → PUBLICABLE, 0 REGRABAR) y
la hoja de fotogramas. Esta revisión es la parte semántica: SRT leído completo como novato,
más 8-14 fotogramas por video extraídos con `ffmpeg` en el instante exacto de cada afirmación
verificable de la voz (cifras, estados, nombres de botón, atribuciones), comparados contra la
pantalla. Se citan los avisos del informe que son falsos positivos conocidos (ver skill
`germiva-video`, sección "Falsos positivos del informe") y no se repiten como hallazgo.

---

## cajas-05-cerrar-caja — VEREDICTO: PUBLICABLE

Presentación: abre nombrando la pantalla («Esta es Mi caja, la pantalla donde la cajera
trabaja su turno») y define cada término la primera vez (arqueo: «contar el dinero que hay de
verdad y compararlo con lo esperado»; tolerancia: «el margen que la empresa acepta»). Sin
relleno vacío ni sustantivos pelados; ortografía y acentos correctos en las 61 líneas del SRT.

### Hallazgos BLOQUEANTES
- Ninguno en el contenido del video. Cifras verificadas por fotograma, todas coinciden con la
  voz: fondo inicial RD$5,000 (t=21s), cobros RD$0 / entradas RD$2,000 (t=25s), salidas
  RD$6,500 (t=32s), transf. recibidas RD$3,000, efectivo esperado RD$3,500 (t=45s), diálogo
  «Conteo de cierre requerido» (t=55s), monto recibido 3,480 / diferencia −20 / «Dentro de
  ±RD$50.00» (t=115s, t=122s), Resumen de totales 3,500 → 3,480 → −20 (t=148s), aviso verde de
  tolerancia (t=155s), «No tienes una sesión activa» al cierre (t=190s).
- **youtube-video.txt — capítulos: solo 1** («00:00 Cajas · Cierra tu caja con el conteo de
  cierre»). El requisito es ≥3 y el video tiene 3 tareas claras con tiempos de arranque exactos
  en `informe-video.md` (01-cerrar-caja 0.0s, 02-ingresar-montos 67.2s, 03-registrar-conteo
  136.0s). Cambiar a:
  ```
  00:00  Mi caja y el desglose del efectivo
  01:07  Conteo de cierre: ingresar montos
  02:16  Confirmar cuadre y registrar
  ```
  Evidencia: `salida/cajas-05-cerrar-caja/youtube-video.txt` línea 8, contra
  `informe-video.md` líneas de cabecera de cada paso.

### Mejoras opcionales
- «0 transacciones» bajo Monto esperado (H-04) queda visible sin narrar en el fotograma de
  t=115s; el guion ya lo evita a propósito (comentario del guion). No requiere cambio, solo
  queda anotado por si se reutiliza el plano en otro video.

### Checklist youtube-video.txt
- capítulos: 1 (NO cumple, ver arriba)
- descripción en español: sí
- nombres internos/localhost: ninguno

---

## cajas-06-cuadre-y-desbloqueo — VEREDICTO: PUBLICABLE

Presentación correcta de las tres pantallas («Esta es Por aprobar, la bandeja de la
supervisora de caja»; «Ahora, un arqueo sorpresa: contar sin avisar el dinero de una caja que
sigue abierta»; «Por último, desbloquear una caja»). Los tres avisos del informe (83.4s / 73.8s
/ 48.0s) son el falso positivo conocido «alerta señalada milisegundos antes de que la sonda la
detectara» — confirmado, no es hallazgo.

### Hallazgos BLOQUEANTES
- Ninguno en el contenido. Fotogramas verificados: cifras del cuadre REC-2026-00007 (esperaba
  3,500 / contó 3,480 / diferencia −20, t=22s y t=26s) coinciden con el «Detalle del cuadre de
  caja» (t=39s, t=44s); «Dentro de tolerancia» badge visible cuando la voz dice «aquí, sí»
  (t=44s); el diálogo genérico «Confirmación / ¿Estás seguro que deseas APROBAR…?» (H-06) se
  muestra tal cual sin que la voz lea su texto exacto — coincide con lo previsto en el guion
  (t=79s); arqueo sorpresa: Caja Mostrador 2 / cajero luis.batista, total esperado en caja
  RD$3,050 (t=143s), monto recibido 3050 y «Sin diferencia» (t=149s) — coincide con «tres mil
  cincuenta pesos» y «como coincide, no hay diferencia que justificar»; desbloqueo: diálogo
  «BLOQUEADO POR Sistema» (H-13) aparece en pantalla (t=194s) pero la voz solo dice «la razón y
  la fecha», nunca atribuye el bloqueo a una persona ni al sistema — no hay afirmación falsa;
  casilla «Resetear contador» viene marcada en pantalla, igual que dice la voz («que viene
  marcada»); al final, filtro «Todas» muestra la caja «Cerrada» (t=227s), igual que «ahora
  Cerrada y lista para abrirse».
- **youtube-video.txt — capítulos: solo 1**. Mismo defecto que el video 05. El informe da los
  tres arranques: 01-aprobar-cuadre 0.0s, 02-arqueo-sorpresa 87.5s, 03-desbloquear 167.9s.
  Cambiar a:
  ```
  00:00  Aprobar un cuadre pendiente
  01:27  Arqueo sorpresa a una caja abierta
  02:48  Desbloquear una caja
  ```
  Evidencia: `salida/cajas-06-cuadre-y-desbloqueo/youtube-video.txt` línea 8.

### Mejoras opcionales
- Ninguna adicional a la de capítulos.

### Checklist youtube-video.txt
- capítulos: 1 (NO cumple, ver arriba)
- descripción en español: sí
- nombres internos/localhost: ninguno

---

## cajas-07-historial-y-analisis — VEREDICTO: PUBLICABLE

Presentación correcta («Este video es para consultar lo que ya pasó… donde cada tarjeta es una
caja de la ferretería»; «Ahora Análisis, la pantalla de números del módulo»). Sin avisos en el
informe (0 alertas sin explicar).

### Hallazgos BLOQUEANTES
- Ninguno en el contenido. Fotogramas verificados: fila de sesión cerrada de Yohanna con ojo,
  lápiz y candado (t=31s); Movimientos con «Autorizado por: carmen.rosario» / «yohanna.peralta»
  visibles (H-02) pero la voz solo dice «la transferencia recibida y la salida aprobada… con su
  monto y su estado», sin nombrar a nadie — no hay atribución falsa (t=46s); Cuadres con
  REC-2026-00007 «Confirmado» e ícono rojo de anular (t=57s, t=60s), igual que «el de hoy ya
  sale Confirmado» y «el ícono rojo… sirve para anular»; hero de Análisis con «1 CUADROS
  PENDIENTES» naranja (t=92s); **Período = «Este mes»** (t=101s) coincide EXACTO con la voz
  («El Período viene en Este mes») — el hallazgo H-10 del plan original (que preveía «Hoy» por
  error) quedó corregido en este guion, sin discrepancia; «7/7 CERRADAS CUADRADAS» (t=109s)
  coincide con «cuántas de las cerradas quedaron cuadradas»; alerta de saldo bajo con tooltip
  exacto «está por debajo del umbral mínimo configurado (RD$1,000.00)» y estado «Resuelta»
  (t=145s) coincide con la voz; auditoría con columnas Fecha/Acción/Entidad/Descripción/
  Usuario/IP y filtros Acción/Tipo de entidad/Usuario/Fecha (t=160s, t=178s) coinciden con «el
  tipo de cambio, la descripción y el usuario» y «por acción, por tipo de entidad, por usuario o
  por fechas»; la IP de auditoría muestra **192.168.1.25** en los fotogramas muestreados (no
  «::1») — la sustitución de privacidad funcionó en los instantes comprobados.
- **youtube-video.txt — capítulos: solo 1**. Mismo defecto. Arranques del informe:
  01-historial-de-una-caja 0.0s, 02-analisis 66.9s, 03-alertas-auditoria 134.3s. Cambiar a:
  ```
  00:00  Historial de sesiones, movimientos y cuadres de una caja
  01:07  Análisis: reporte diario, cuadres y rendimiento
  02:14  Alertas y auditoría
  ```
  Evidencia: `salida/cajas-07-historial-y-analisis/youtube-video.txt` línea 8.

### Mejoras opcionales
- El ícono «candado» (reabrir sesión, H-12) se marca activo (t=31s) sobre una sesión que YA
  tiene cuadre confirmado (REC-2026-00007), justo cuando la voz explica la regla restrictiva
  («el sistema solo lo permite… si todavía no tiene cuadre»). El guion, a propósito, no lo pulsa
  y no afirma que esta fila en particular se pueda reabrir, así que no es una afirmación falsa —
  pero un espectador atento podría pensar que el botón habilitado contradice la regla que acaba
  de escuchar. Sugerencia opcional para una futura regrabación: añadir medio segundo de voz
  aclarando que el botón puede verse activo aunque el sistema lo rechace («el botón se ve igual,
  pero si ya hay cuadre el sistema no te deja»), o remarcar la fila SIN cuadre en vez de la de
  hoy. No bloquea publicación.
- El guion documenta que la IP «::1» puede aparecer unos cientos de ms antes de la sustitución
  de privacidad (nota del propio guion); no se detectó en los fotogramas muestreados, pero si
  `tut auditar --video` la marca, es un hallazgo de motor conocido, no del guion.

### Checklist youtube-video.txt
- capítulos: 1 (NO cumple, ver arriba)
- descripción en español: sí
- nombres internos/localhost: ninguno (IP mostrada en pantalla es la sustituida 192.168.1.25 en
  los instantes verificados)

---

## Resumen para publicar

Los tres videos son **PUBLICABLES en contenido**: cero afirmaciones falsas, cero marcas
apuntando a lo contrario de lo que dice la voz, cero datos reales o «QA-*», cero defecto
conocido del ERP enseñado como si fuera correcto. El único bloqueante real y repetido en los
tres es de **empaquetado, no de grabación**: `youtube-video.txt` sale con un solo capítulo
(«00:00 <título completo>») en vez de los ≥3 que pide la regla; no hace falta regrabar nada,
solo regenerar o editar a mano el bloque de capítulos con los tiempos de arranque de cada paso
que ya trae `informe-video.md` (listados arriba, por video).
