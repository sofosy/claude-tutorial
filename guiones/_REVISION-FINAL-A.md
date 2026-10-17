# Revisión final A · serie «Seguridad» (00, 01, 02a, 02b) · 2026-09-28

Revisor: REVISOR-FINAL-A (solo lectura). Fotogramas en
`qa-seguridad-revision-final-2026-09-28/<guion>/`. **Revisión INCOMPLETA** — detenida a pedido del
usuario; el visor de imágenes falló gran parte de la sesión.

## Estado de avance

| Video | Estado | Veredicto |
|---|---|---|
| seguridad-00-introduccion | Fotogramas NO revisados (solo SRT + informe: sin avisos, desfases ≤0,5 s) | PENDIENTE |
| seguridad-01-resumen | Fotogramas NO revisados (solo SRT) | PENDIENTE |
| seguridad-02a-roles | Revisado ~0:10–0:40 y 1:15–3:46 (falta 0:47–1:10) | OK con menores |
| seguridad-02b-editor-permisos | Revisado casi completo | **CORREGIR (regrabar)** |

Nota operativa: la toma buena del 00 es `salida/seguridad-00-introduccion/video-20260927-2104.mp4`
(el `video.mp4` es la toma vieja de T1; renombrar).

## seguridad-02b-editor-permisos — CORREGIR

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| B1 | 2:12–2:25 | 03-alcance | `045-02m12.86s`, `047`, `048`, `050` | motor | El título «Socios» queda medio tapado bajo la leyenda fija (lista interna desplazada) mientras se marcan Todos/Equipo/Propios | Regrabar paso 03 con motor `e1810d6` |
| B2 | 3:43–3:52 | 05-guardar | `078-03m43.76s`, `080-03m52.10s` | motor | Tras guardar, la fila superior del recurso sale cortada («0/4 Conceder todo» con botones recortados) | Regrabar paso 05 con `e1810d6` |
| B3 | 3:16–3:36 | 04→05 | `067-03m16.37s`, `068`, `073`, `075` | motor/ERP | Al borrar la búsqueda, «Clientes y Proveedores 3 de 33» muestra el cuerpo vacío ~20 s (lista interna quedó desplazada) | Tras borrar, pulsar el módulo o el filtro «Todos» para reposicionar; verificar con `e1810d6` |
| B4 | 3:36–3:41 | 05-guardar | `075-03m36.78s`, `x-03m39.60s` | guion/ERP | La voz nombra «Guardar cambios» pero el botón está bajo el borde (la barra se parte en dos líneas); solo aparece a 3:41 | Marcar/desplazar a `.gm-sheet-savebar button:has-text('Guardar cambios')` al decirlo; ERP: barra en una sola línea |
| B5 | 2:02 | 02-conceder | `042-02m02.71s` | guion/ERP | Barra de cambios marcada sin el botón Guardar visible | Igual que B4 |
| B6 | 0:40–0:42 | 01 | `x-00m40.30s` | guion | Cursor tapa «3/19» mientras la voz dice «tres de diecinueve» | `"cursor": false` en esa marca |
| B7 | 4:05 | 05 | `086-04m05.78s` | guion | Cursor tapa «1/79» de Facturación («ya marca uno») | `"cursor": false` |
| B8 | 1:10 | 01 | `022-01m10.70s` | guion | «Vendedor tiene Ver, Crear y Editar»: la marca cubre solo «Ver» | Marcar la fila de acciones o las tres |
| B9 | 4:10 | 05 | `087-04m10.78s` | guion | Voz «su estado de cuenta», pero Estado de Cuenta quedó con alcance «Todos» | Poner Propios en Estado de Cuenta o cambiar la voz a «el estado de cuenta de todos los clientes» |
| B10 | 2:42 | 03 | `053-02m42.13s` | guion | Tooltip «Concedido · Socios · Ver» tapa el segmento de alcance que se explica | Mover cursor fuera (`cursor:false`) |

## seguridad-02a-roles — OK con menores

| # | mm:ss | Paso | Fotograma | Tipo | Defecto | Propuesta |
|---|---|---|---|---|---|---|
| A1 | 1:28 | 02-rol-del-sistema | `027-01m28.15s` | guion | Fila «Unidades Medida» cortada en el borde inferior al marcar «Ver» en gris | Marcar una acción de una fila más alta |
| A2 | 3:28 / 3:34 | 04-crear-rol | `077-03m28.39s`, `078-03m34.01s` | guion | Marcas sobre título/descripción del rol mientras la voz explica avisos del diálogo (nombre repetido, cerrar sin guardar) que no se ven | Quitar esas marcas o mostrar el aviso real |

## Pendiente para continuar

1. Revisar fotogramas de 00 (usar `video-20260927-2104.mp4`) y 01 completos.
2. Revisar 02a 0:47–1:10.
3. Decidir si 02b se regraba entero (B1–B3 son de motor, previos a `e1810d6`).

---

## Reposición (orquestador, 09-28): hallazgos de 00, 01 y 02a del segundo revisor

Este archivo fue sobrescrito por un revisor anterior que se había detenido. Los hallazgos del revisor que sí vio los
fotogramas de 00/01/02a (y que el AUTOR-CORRECCIÓN-1 ya aplicó, ver «Corrección 09-28» en cada guion) eran:

- **00-introduccion: CORREGIR → REGRABAR.** Motor 2:48 (046): la tabla de Personas se desplaza y oculta la cabecera
  cuando la voz nombra las columnas. Guion 2:54 (049): la voz dice «su rol, Vendedor» con el panel en Mensajero · Vacío.
  Guion 3:10: la marca de la fila de Auditoría sigue dibujada tras volver al Resumen.
- **01-resumen: CORREGIR → REGRABAR.** Motor 1:30 y 1:37: «Requiere atención» se desplaza y corta su cabecera y el
  asunto anterior. ERP 3:17: «Nunca entraron · 0» y «Esta persona no está en la lista actual» ~1,5 s al cargar
  (corregido en ronda 8). Guion 2:19: «lo más viejo con el día y la hora» marcando «Hace 7 h». Guion: el cursor tapa cifras.
- **02a-roles: CORREGIR.** Guion 3:25–3:37: los «dos avisos útiles» se explican marcando título y descripción, sin que
  se vea ningún aviso. Guion 0:41: el cursor tapa el «2» de «Almacén, dos». Motor 1:28 (menor): «Unidades Medida»
  cortada abajo. Marcas mayores que lo nombrado.
- **Textos ERP** (corregidos en ronda 8): «Asignarlos» con un solo rol; «PREFIJO DE LA API KEY»; «Unidades Medida»;
  «Crear Rol» vs «Duplicar rol».
