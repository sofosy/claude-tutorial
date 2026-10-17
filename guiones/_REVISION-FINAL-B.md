# Revisión final B — Seguridad 03 · 04a · 04b · 04c (2026-09-28)

Revisor: REVISOR-FINAL (solo lectura). Fuente: fotogramas en
`germiva/qa-seguridad-revision-final-2026-09-28/<guion>/` (+ extras `x-*.jpg` / `y-stack-*.jpg`
extraídos con ffmpeg del video bueno), `salida/<guion>/video.srt` e `informe-video.md`.

Contexto: los cuatro videos se grabaron el 2026-09-27 (21:28–22:34), **antes** del commit de motor
`e1810d6` (2026-09-28 00:44, «no desplazar lo que ya se ve; listas internas con scroll mínimo sin
quedar bajo sticky», G-14/G-19). Los avisos de `informe-video.md` son todos del tipo «toast no se
señaló» → falsos positivos conocidos (SKILL, «Falsos positivos del informe»); no se listan.

Datos: solo ficticios (Distribuidora Las Palmas, RNC 130555036, @germiva.demo, Rosa/Ana/José/Carlos/
Pedro/Marta/Héctor/Luisa/Sonia, Julio en 04b, IP 192.168.1.25). Sin datos reales en ningún video.

| Video | Veredicto |
|---|---|
| seguridad-03-herencia | **CORREGIR** (menor: guion + 1 ERP) |
| seguridad-04a-personas | **OK** (1 observación ERP cosmética) |
| seguridad-04b-alta-y-edicion | **CORREGIR** (menor: guion) |
| seguridad-04c-equipos | **CORREGIR → REGRABAR** (guion + motor) |

---

## seguridad-03-herencia — CORREGIR

### 03-1 · 03:42–03:45 · paso `05-titulares` · tipo **ERP + guion**
- Fotogramas: `qa-seguridad-revision-final-2026-09-28/seguridad-03-herencia/x-03m42.6s-vacio-falso.jpg`,
  `.../y-stack-0342-vacio.jpg`, `.../y-stack-0343-panel.jpg`.
- Qué se ve: tras el clic en Ana (titular), la vista Personas sale con esqueleto y el panel derecho
  dice «Esta persona no está en la lista actual.» [Cerrar] durante ~1–2 s, mientras la voz dice
  «la consola me lleva a su ficha». Un novato lee un error.
- Propuesta ERP: mientras la lista de Personas carga, el panel de detalle debe mostrar esqueleto,
  no el mensaje de «no está en la lista» (misma familia que G-6, vacío falso).
- Propuesta guion (si no se arregla el ERP antes): tras el clic, `esperar` a que el nombre de Ana
  aparezca en el panel antes de la frase «la consola me lleva a su ficha».

### 03-2 · 03:22–03:23 · paso `05-titulares` · tipo **guion**
- Fotograma: `.../seguridad-03-herencia/093-03m23.52s.jpg`.
- Qué se ve: la marca del enlace «3 personas tienen este rol» (durante_ms 4000) sigue dibujada como
  una caja vacía después de que la pantalla cambió a Personas.
- Propuesta: bajar `durante_ms` a ~2000 o anclar la marca antes para que se apague antes del clic.

Resto OK: chip/leyenda de heredado, Cotizaciones heredado, Crear Rol, «Operación completada»,
exclusión + barra de guardar, Eliminar rol (diálogo + aviso), cartel «Cuidado», titulares
(José/Ana/Héctor), Historial «Inventario · Productos», guion rojo «–» → verde, cierre con logo.

---

## seguridad-04a-personas — OK

### 04a-obs · 03:18 · paso de Auditoría/filtro · tipo **ERP** (cosmético, no bloquea)
- Fotograma: `.../seguridad-04a-personas/071-03m18.14s.jpg`.
- El chip del filtro Persona muestra «ana.mejia» (usuario) en lugar de «Ana Mejía»; la voz dice
  «ya filtrada por Ana», así que se entiende. Propuesta: que el chip muestre el nombre visible.

Resto OK: todas las marcas caen en su elemento; IP 192.168.1.25, «Chrome · Windows», cartel
«Consejo» final.

---

## seguridad-04b-alta-y-edicion — CORREGIR

### 04b-1 · 02:26 · paso `02-editar-y-contrasena` · tipo **guion**
- Fotograma: `.../seguridad-04b-alta-y-edicion/067-02m26.18s.jpg`.
- La marca del campo Contraseña («la anterior», durante_ms 4500) sigue dibujada a medias detrás del
  diálogo «Operación completada».
- Propuesta: `durante_ms` ≤ 2500, o anclar la marca antes de «Pulso Actualizar».

### 04b-2 · 03:11–03:15 · paso `03-asignar-rol` · tipo **guion**
- Fotograma: `.../seguridad-04b-alta-y-edicion/088-03m13.75s.jpg`.
- La voz dice «En tu propia ficha, este bloque no trae el enlace, sino un aviso: nadie puede cambiar
  sus propios roles» mientras en pantalla está la ficha de Julio con la marca sobre «ROLES»; el aviso
  nunca se ve. Voz y pantalla no coinciden.
- Propuesta: reformular en condicional sin marca («Si abres tu propia ficha, en lugar del enlace
  verás un aviso: nadie puede cambiar sus propios roles») o quitar la marca sobre ROLES en esa frase.

### 04b-3 (opcional) · 00:16–01:36 · paso `01-alta` · tipo **motor/guion** (cosmético)
- Fotograma: `.../seguridad-04b-alta-y-edicion/008-00m16.39s.jpg`.
- La insignia «Administradora · Rosa» se superpone a la cabecera del diálogo Crear Usuario (no tapa
  el título). Propuesta: ocultar la insignia mientras hay diálogo abierto o moverla de esquina.

Resto OK: alta de Julio Santana (julio.santana@germiva.demo), «Creando usuario…», «Operación
completada», Asignar roles «Se agrega: Almacén», «Roles actualizados», Desactivar/Activar con sus
estados de carga, Inactiva/Pendiente, Eliminar con cartel «Consejo», «Usuario eliminado»,
«Mostrando 1–9 de 9».

---

## seguridad-04c-equipos — CORREGIR → REGRABAR

### 04c-1 · 00:25–00:29 · paso `01-que-es-un-equipo` · tipo **guion**
- Fotogramas: `.../seguridad-04c-equipos/010-00m26.90s.jpg`, `.../011-00m29.89s.jpg`.
- Voz: «La primera, Ana Mejía; y el segundo, José Cabrera», pero la lista muestra José arriba y Ana
  abajo; la marca cae en la 2.ª fila mientras dice «la primera».
- Propuesta: «Arriba, José Cabrera; y debajo, Ana Mejía» (o invertir el orden de las anclas).

### 04c-2 · 01:47–01:53 (y 01:58–02:01) · paso `03-agregar-miembros` · tipo **motor** (pre-e1810d6)
- Fotogramas: `.../seguridad-04c-equipos/042-01m49.90s.jpg`, `.../043-01m52.76s.jpg`,
  `.../x-111.8.jpg`, `.../045-01m58.47s.jpg`, `.../047-02m01.61s.jpg`.
- Al marcar casillas la lista interna se desplaza: la cabecera PERSONA desaparece bajo la barra
  «2 seleccionadas» y la fila de Carlos Pimentel (marcado) queda cortada arriba (solo se lee
  «carlos.pimentel@germiva.demo» a medias), justo cuando la voz dice «Marco a Carlos… y a Héctor».
  En 02:01 el menú «Zona Norte / Zona Este» se abre encima de la fila cortada.
- Propuesta: **regrabar con el motor `e1810d6`** (scroll mínimo de lista interna sin quedar bajo el
  sticky). Si reaparece, marcar a Carlos y Héctor con la lista filtrada o anclar el scroll a la fila.

### 04c-3 · 00:23.96 · paso `01-que-es-un-equipo` · tipo **guion/motor** (menor)
- Fotograma: `.../seguridad-04c-equipos/008-00m23.96s.jpg`.
- La marca del título «Zona Este · 2» es mucho más ancha que el texto (abarca la barra entera).
  Propuesta: apuntar la marca al texto del título, no al contenedor de la barra.

### 04c-obs · 03:39 · paso `05-sin-equipos` · tipo **motor** (menor, se va con la regrabación)
- Fotograma: `.../seguridad-04c-equipos/092-03m39.05s.jpg`.
- Para marcar a Ana la lista interna se desplaza y la cabecera PERSONA y la fila de Pedro quedan
  cortadas arriba. No confunde (voz y marca coinciden), pero es el mismo patrón que 04c-2.

Resto OK: toast «Personas agregadas a «Zona Norte»», correo con «· Zona Norte», riel «2 personas»,
Quitar del equipo + «Persona quitada…», «1 persona» (singular correcto), Editar Equipo con marca
(G-13 resuelto), «Operación completada», Eliminar equipo con nombre en la confirmación, «Equipo
eliminado exitosamente», riel «Sin equipos todavía.», botón «+», cierre en «Roles y permisos».
