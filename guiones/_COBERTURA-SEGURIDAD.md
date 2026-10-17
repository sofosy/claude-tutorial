# Cobertura — serie «Seguridad» (Germiva ERP)

Autor: AUTOR-PLAN · 2026-09-27. Fusión 2026-09-27 de `_COBERTURA-AUTOR-A.md` (00, 01, 02a, 02b, 03, 09),
`_COBERTURA-AUTOR-B.md` (04a, 04b, 04c, 05, 06a, 06b, 06c) y `_COBERTURA-AUTOR-C.md` (07, 08a–08g) sobre
este archivo. Plan: `_SERIE-SEGURIDAD.md`. Fuentes: `_INVENTARIO-SEGURIDAD-FE.md` (F-001…F-274) e
`_INVENTARIO-SEGURIDAD-API.md` (A-001…A-076). Cada `Video / paso` de un punto **guionizado** es un id real,
verificado contra el `seguridad-XX-*.json` correspondiente (no contra el plan). La columna **Minuto** queda
vacía. Se llena después de grabar, con el `informe-video.md` y el SRT de cada video.

## Resumen de la fusión

| | Total | **Guionizado** | Pantalla | Voz | No se provoca | No aplica | Técnico | Defecto | INFERIDO | **SIN CUBRIR** |
|---|---|---|---|---|---|---|---|---|---|---|
| Front F-### | 274 | **236** | 204 | 32 | 12 | 4 | 18 | 4 | 0 | **0** |
| API A-### | 76 | **50** | 37 | 13 | 0 | 2 | 13 | 8 | 3 | **0** |
| **Total** | **350** | **286** | **241** | **45** | **12** | **6** | **31** | **12** | **3** | **0** |

Cobertura de lo **visible para el usuario** (total − técnico − no aplica): Front 236 de 252 = **93.7 %** ·
API 50 de 61 = **82.0 %** · conjunto 286 de 313 = **91.4 %**. Lo que queda fuera son 12 estados de carga o
fallo que no se provocan, 12 defectos que el plan esquiva a propósito y 3 comportamientos INFERIDOS sin
confirmar en código. **SIN CUBRIR: 0.**

**SIN CUBRIR → cerrados por el AUTOR D (2026-09-27)** (11 Front + 1 API; detalle en
`_INFORME-AUTOR-seguridad-08h-administrar-la-seguridad.md`):
- F-226, F-228, F-229, F-230, F-231, F-238, F-239, F-240 → video nuevo `seguridad-08h-administrar-la-seguridad`
  (Rosa con permiso / Marta sin, sobre el mismo panel de persona, el mismo equipo y la misma credencial)
- F-052 → 04c/05-sin-equipos · F-157 → 02a/02-rol-del-sistema · F-007 → 09/03b-historial-viejo ·
  A-059 → 07/03-detalle-del-evento
- Selectores sacados del código y no de un volcado (se confirman en el ensayo): vacío de equipos, historial
  vacío, barra de selección y cabecera de equipo de Marta, celda Registro #11034, recurso de «Acceso API».

## Cómo leer la tabla

- **Video / paso**: `<video>/<id de paso>` REAL del guion grabable (por ejemplo `02b/03-alcance`, verificado
  en `seguridad-02b-editor-permisos.json`). Cuando hay varios, el primero es donde se ENSEÑA y los demás
  donde se vuelve a ver.
- **Estado**:
  - *guionizado* → confirmado en un guion real, se ve en pantalla (marca o acción).
  - *guionizado (voz)* → confirmado en un guion real, solo en narración o cartel, sin pantalla propia.
  - **SIN CUBRIR** → el plan lo daba por enseñable y ningún autor lo guionizó; el motivo va en la última
    columna (del `_COBERTURA-AUTOR-*` o del `_INFORME-AUTOR-*` correspondiente, o «sin motivo» si no consta).
  - *no se provoca* → estado de carga o de fallo (esqueletos, error de red, enlace roto). Existe, pero
    provocarlo en cámara sería inventar una falla.
  - *no aplica* → no existe para el administrador de una empresa cliente del ERP (empresa principal,
    RegiSalud o pantalla estrecha).
  - *técnico interno — no visible, no se enseña* → modelo de datos, endpoints, selectores, estado del front.
  - *no se enseña (defecto / en corrección)* → defecto del inventario (D-## / A-069…A-076). El plan lo esquiva
    sin afirmar lo contrario.
  - *INFERIDO — no se enseña* → comportamiento no confirmado en código.

Los siete tipos de caso con/sin del pedido: VISTA 08a · ACCIÓN 08b, 08c y 08e · ALCANCE 08d · ESTADO 08e ·
HERENCIA Y EQUIPOS 08f (+05) · CAMBIO EN VIVO 08g · INTEGRACIÓN 06c.

## Front (F-###)

| ID | Qué | Video / paso | Minuto | Estado | Motivo / nota |
|---|---|---|---|---|---|
| F-001 | Entrada del menú lateral | 00/03-la-consola |  | guionizado |  |
| F-002 | Permiso para ver la entrada del menú | 00/03-la-consola · 08a/04-con-seguridad |  | guionizado |  |
| F-003 | Ruta raíz | 00/03-la-consola · 01/01-cifras |  | guionizado | autor A: el candado aterriza en Resumen (en pantalla, no solo mencionado) |
| F-004 | Ruta de la consola | — | | técnico interno — no visible, no se enseña | ids internos de la URL; el usuario navega por pestañas |
| F-005 | Rutas heredadas (redirigen) | 09/04-enlaces-viejos |  | guionizado (voz) | se demuestra con /security/settings; el resto se nombra |
| F-006 | Alias de pestaña en la URL | — | | técnico interno — no visible, no se enseña | alias de URL sin efecto visible |
| F-007 | Historial de un registro (ruta vieja) | 09/03b-historial-viejo |  | guionizado | autor D: se navega a la ruta vieja y se ve la Auditoría filtrada por el registro (Almacén, 3 eventos); redirección SPA a confirmar en el ensayo |
| F-008 | Rutas que salieron del módulo | 09/04-enlaces-viejos · 09/03-perfil-consultorio |  | guionizado |  |
| F-009 | Rutas con página propia | 06a/05-sus-permisos · 06b/04-documentacion |  | guionizado |  |
| F-010 | Sin guard de ruta | — | | técnico interno — no visible, no se enseña | sin guard de ruta; su efecto (franja) se ve en 08a/05 |
| F-011 | Hoja única | 00/03-la-consola |  | guionizado |  |
| F-012 | Barra de pestañas | 00/03-la-consola |  | guionizado |  |
| F-013 | Conteos en las pestañas | 00/03-la-consola |  | guionizado |  |
| F-014 | Permiso de cada pestaña | 00/03-la-consola · 08a/04 · 08a/05 |  | guionizado |  |
| F-015 | Aviso de pestaña denegada por URL | 08a/05-sin-integraciones |  | guionizado |  |
| F-016 | Buscador global de la cabecera | 00/03-la-consola |  | guionizado | solo búsqueda de personas (D-11: no busca permisos) |
| F-017 | Botón «Nuevo» (menú) | 00/03-la-consola · 08a/04 (ausente para Marta) |  | guionizado |  |
| F-018 | Nuevo › Usuario | 04b/01-crear-usuario |  | guionizado |  |
| F-019 | Nuevo › Rol | 02a/04-crear-rol · 03/02-crear-hijo |  | guionizado |  |
| F-020 | Nuevo › Equipo | 04c/02-crear-equipo |  | guionizado (voz) | se usa el «+» del rail; el ítem de «Nuevo» se nombra |
| F-021 | Nuevo › Integración de API | 06a/02-crear-credencial |  | guionizado (voz) | se usa «Nueva credencial»; el ítem de «Nuevo» se nombra |
| F-022 | Estado compartido | — | | técnico interno — no visible, no se enseña | estado compartido del front |
| F-023 | Etiquetas de acción (compartidas) | 01/03-actividad-reciente · 07/01-la-bitacora |  | guionizado |  |
| F-024 | Formato de tiempo relativo | 01/03-actividad-reciente |  | guionizado (voz) | autor A: la voz no lee ningún «Hace N min» (R13); no queda marca propia en pantalla |
| F-025 | Origen legible del user-agent | 04a/03-ficha-de-la-persona · 07/03-detalle-del-evento |  | guionizado |  |
| F-026 | Estado de carga | — | | no se provoca | esqueleto de carga, dura milisegundos |
| F-027 | Estado de error | — | | no se provoca | error de red; no se provoca en video |
| F-028 | Cifra «Personas con acceso» | 01/01-cifras |  | guionizado |  |
| F-029 | Cifra «Administradores» | 01/01-cifras |  | guionizado |  |
| F-030 | Cifra «Sin ningún rol» | 01/01-cifras |  | guionizado |  |
| F-031 | Cifra «Credenciales de API» | 01/01-cifras |  | guionizado |  |
| F-032 | Cifra «Cambios en 7 días» | 01/01-cifras |  | guionizado |  |
| F-033 | Bloque «Requiere atención» | 01/02-requiere-atencion |  | guionizado |  |
| F-034 | Asunto USERS_WITHOUT_ROLE | 01/02-requiere-atencion |  | guionizado |  |
| F-035 | Asunto STALE_API_CREDENTIAL | 01/02-requiere-atencion · 06b/03-revocar |  | guionizado |  |
| F-036 | Asunto NEVER_LOGGED_IN | 01/02-requiere-atencion |  | guionizado | no decir «reenviar invitación» (D-08: no existe) |
| F-037 | Asunto EMPTY_ROLE | 01/02-requiere-atencion |  | guionizado |  |
| F-038 | Atención vacía | 01/02-requiere-atencion |  | guionizado (voz) | la demo tiene asuntos a propósito |
| F-039 | Bloque «Actividad reciente» | 01/03-actividad-reciente |  | guionizado |  |
| F-040 | Fila de actividad | 01/03-actividad-reciente |  | guionizado | la parte ≤767 px no aplica (video 1280) |
| F-041 | Actividad vacía | 01/03-actividad-reciente |  | guionizado (voz) |  |
| F-042 | Rótulo «Vistas» | 04a/01-vistas |  | guionizado |  |
| F-043 | Vista «Todas» | 04a/01-vistas |  | guionizado |  |
| F-044 | Vista «Activas» | 04a/01-vistas |  | guionizado |  |
| F-045 | Vista «Sin rol» | 04a/01-vistas · 01/01-cifras |  | guionizado |  |
| F-046 | Vista «Nunca entraron» | 04a/01-vistas |  | guionizado |  |
| F-047 | Vista «Inactivas» | 04a/01-vistas |  | guionizado |  |
| F-048 | Conteos del rail | 04a/01-vistas |  | guionizado |  |
| F-049 | Rótulo «Equipos» | 04c/01-que-es-un-equipo |  | guionizado |  |
| F-050 | Botón «+» Nuevo equipo | 04c/02-crear-equipo |  | guionizado |  |
| F-051 | Lista de equipos | 04c/01-que-es-un-equipo |  | guionizado |  |
| F-052 | Sin equipos | 04c/05-sin-equipos |  | guionizado | autor D: al final se elimina también «Zona Este» para enseñar «Sin equipos todavía.» (restaurar E0 la devuelve); selector del código, a confirmar en el ensayo |
| F-053 | Título de la lista | 04a/01-vistas |  | guionizado |  |
| F-054 | Buscador | 04a/02-buscar-y-filtrar |  | guionizado |  |
| F-055 | Filtro «Rol» | 04a/02-buscar-y-filtrar |  | guionizado |  |
| F-056 | Botón «Editar equipo» | 04c/04-quitar-editar-eliminar |  | guionizado |  |
| F-057 | Botón eliminar equipo | 04c/04-quitar-editar-eliminar |  | guionizado |  |
| F-058 | Confirmación de eliminar equipo | 04c/04-quitar-editar-eliminar |  | guionizado |  |
| F-059 | Éxito / error al eliminar equipo | 04c/04-quitar-editar-eliminar |  | guionizado | el error no se provoca |
| F-060 | Columnas | 04a/01-vistas |  | guionizado |  |
| F-061 | Estado de la persona | 04a/01-vistas · 04b/04-desactivar-activar |  | guionizado |  |
| F-062 | Casilla «Seleccionar todas» | 04c/03-agregar-miembros |  | guionizado |  |
| F-063 | Casilla por fila | 04c/03-agregar-miembros |  | guionizado |  |
| F-064 | Carga | — | | no se provoca | esqueleto de carga |
| F-065 | Error | — | | no se provoca | error de red |
| F-066 | Vacío | 04a/02-buscar-y-filtrar |  | guionizado (voz) |  |
| F-067 | Paginación | 04a/01-vistas |  | guionizado | la demo tiene 9 personas: una sola página |
| F-068 | Barra de selección | 04c/03-agregar-miembros |  | guionizado |  |
| F-069 | «Agregar a equipo» | 04c/03-agregar-miembros |  | guionizado |  |
| F-070 | Éxito / error al agregar | 04c/03-agregar-miembros |  | guionizado |  |
| F-071 | «Quitar del equipo» | 04c/04-quitar-editar-eliminar |  | guionizado |  |
| F-072 | Éxito / error al quitar | 04c/04-quitar-editar-eliminar |  | guionizado |  |
| F-073 | «Limpiar» | 04c/03-agregar-miembros |  | guionizado |  |
| F-074 | Abrir el panel | 04a/03-ficha-de-la-persona |  | guionizado |  |
| F-075 | Cabecera del panel | 04a/03-ficha-de-la-persona |  | guionizado |  |
| F-076 | Botón «Editar» | 04b/02-editar-y-contrasena |  | guionizado |  |
| F-077 | Botón «Cambiar contraseña» | 04b/02-editar-y-contrasena |  | guionizado |  |
| F-078 | Menú «Más acciones» | 04a/04-su-actividad · 04b/04 |  | guionizado |  |
| F-079 | Más acciones › Desactivar / Activar | 04b/04-desactivar-activar |  | guionizado |  |
| F-080 | Éxito / error de activar | 04b/04-desactivar-activar |  | guionizado |  |
| F-081 | Más acciones › Ver su actividad | 04a/04-su-actividad |  | guionizado | D-06: Marta (sin editar) no lo ve; se graba con Rosa |
| F-082 | Más acciones › Eliminar | 04b/05-eliminar |  | guionizado |  |
| F-083 | Éxito / error al eliminar | 04b/05-eliminar |  | guionizado |  |
| F-084 | Bloque «Roles» | 04a/03-ficha-de-la-persona · 05/02 · 05/04 |  | guionizado |  |
| F-085 | Enlace «+ Asignar rol» | 04b/03-asignar-rol |  | guionizado | D-01 corregido (autor B): el enlace «+ Asignar rol» aparece con normalidad |
| F-086 | Bloque «Permisos efectivos» | 04a/03-ficha-de-la-persona · 05/02–04 |  | guionizado |  |
| F-087 | «Ver los N módulos» | 04a/03-ficha-de-la-persona |  | guionizado |  |
| F-088 | Bloque «Últimos ingresos» | 04a/03-ficha-de-la-persona · 04a/05-caso-nunca-entro |  | guionizado |  |
| F-089 | Carga del panel | — | | no se provoca | esqueleto de carga |
| F-090 | Persona no encontrada | — | | no se provoca | solo con un enlace a una persona ajena a la lista |
| F-091 | Error al abrir para editar | — | | no se provoca | error de red |
| F-092 | «Nuevo Equipo» | 04c/02-crear-equipo |  | guionizado |  |
| F-093 | «Editar Equipo» | 04c/04-quitar-editar-eliminar |  | guionizado |  |
| F-094 | Éxito del equipo | 04c/02-crear-equipo |  | guionizado |  |
| F-095 | Error del equipo | — | | no se provoca | error del API; no se provoca |
| F-096 | Salir con cambios (equipo) | 04c/04-quitar-editar-eliminar |  | guionizado (voz) |  |
| F-097 | Miembros | 04c/02-crear-equipo |  | guionizado (voz) |  |
| F-098 | Título | 04b/01-crear-usuario |  | guionizado |  |
| F-099 | Nombre(s) | 04b/01-crear-usuario |  | guionizado |  |
| F-100 | Apellido(s) | 04b/01-crear-usuario |  | guionizado |  |
| F-101 | Correo Electrónico | 04b/01-crear-usuario |  | guionizado |  |
| F-102 | Aviso de correo existente | 04b/01-crear-usuario |  | guionizado (voz) |  |
| F-103 | Aviso de correo eliminado | 04b/01-crear-usuario |  | guionizado (voz) |  |
| F-104 | Nombre de Usuario | 04b/01-crear-usuario |  | guionizado |  |
| F-105 | WhatsApp | 04b/01-crear-usuario |  | guionizado |  |
| F-106 | Contraseña (alta) | 04b/01-crear-usuario |  | guionizado |  |
| F-107 | Cambiar contraseña (edición) | 04b/02-editar-y-contrasena |  | guionizado |  |
| F-108 | Bloqueo de contraseña | — | | no aplica | solo la empresa principal (Sofosy); el admin de una empresa cliente no lo ve |
| F-109 | Roles (solo en alta) | 04b/01-crear-usuario |  | guionizado |  |
| F-110 | Aviso de médicos (solo en clínica) | — | | no aplica | solo modo clínica (RegiSalud) |
| F-111 | Estado | 04b/01-crear-usuario |  | guionizado |  |
| F-112 | Éxito del usuario | 04b/01-crear-usuario |  | guionizado |  |
| F-113 | Error del usuario | 04b/01-crear-usuario |  | guionizado (voz) | usuario o correo repetido: se menciona |
| F-114 | Salir con cambios (usuario) | 04b/02-editar-y-contrasena |  | guionizado (voz) | autor B: movido desde el paso 05 (eliminar) al paso 02 (editar) |
| F-115 | No hay botón «Nuevo usuario» en la pestaña | 04b/01-crear-usuario |  | guionizado (voz) |  |
| F-116 | Buscador de roles | 02a/01-lista-de-roles |  | guionizado |  |
| F-117 | Grupo «De la empresa» | 02a/01-lista-de-roles · 03/01-rol-hijo |  | guionizado |  |
| F-118 | Insignia «Vacío» | 02a/01 · 02a/04 · 01/02 |  | guionizado |  |
| F-119 | Conteo de titulares | 02a/01-lista-de-roles |  | guionizado |  |
| F-120 | Grupo «Del sistema» | 02a/01-lista-de-roles |  | guionizado |  |
| F-121 | Rail vacío | 02a/01-lista-de-roles |  | guionizado (voz) |  |
| F-122 | Carga del rail | — | | no se provoca | esqueleto de carga |
| F-123 | Selección inicial | 02a/01-lista-de-roles |  | guionizado |  |
| F-124 | Sin rol elegido | — | | no se provoca | la consola siempre abre un rol; no se alcanza sin forzar |
| F-125 | Nombre | 02a/02-rol-del-sistema |  | guionizado |  |
| F-126 | Chip «Hereda de {padre}» | 03/01-rol-hijo |  | guionizado |  |
| F-127 | Insignias | 02a/02-rol-del-sistema |  | guionizado |  |
| F-128 | Descripción y titulares | 03/05-titulares |  | guionizado |  |
| F-129 | Botón «Duplicar» | 02a/03-duplicar |  | guionizado |  |
| F-130 | Botón «Editar» | 02a/02-rol-del-sistema |  | guionizado | se enseña presente (rol de empresa) y ausente (sistema); no se edita el nombre de ningún rol |
| F-131 | «Más acciones» › «Eliminar rol» | 03/05-eliminar-rol |  | guionizado |  |
| F-132 | Confirmación de eliminar rol | 03/05-eliminar-rol |  | guionizado |  |
| F-133 | Éxito / error al eliminar rol | 03/05-eliminar-rol |  | guionizado |  |
| F-134 | Subvistas | 03/05-titulares · 03/06-historial |  | guionizado |  |
| F-135 | Cambios sin guardar | 02b/05-guardar-o-descartar |  | guionizado |  |
| F-136 | Rail «Módulos» | 02b/01-modulos-y-leyenda |  | guionizado |  |
| F-137 | Módulo inicial | 02b/01-modulos-y-leyenda |  | guionizado (voz) | autor A: solo se nombra, sin marca propia |
| F-138 | Título del módulo | 02b/01 · 03/01-rol-hijo |  | guionizado |  |
| F-139 | Filtros por estado del PERMISO | 02b/05 · 03/01-rol-hijo |  | guionizado | son estados del PERMISO, nunca «estado del documento» |
| F-140 | Búsqueda en todo el catálogo | 02b/04-buscar-permiso |  | guionizado |  |
| F-141 | Tope de la búsqueda | 02b/04-buscar-permiso |  | guionizado (voz) |  |
| F-142 | Leyenda | 02b/01 · 03/01 |  | guionizado |  |
| F-143 | Aviso de rol del sistema (solo lectura) | 02a/02-rol-del-sistema |  | guionizado |  |
| F-144 | Recurso | 02b/02-conceder |  | guionizado |  |
| F-145 | Acciones del recurso | 02b/02-conceder · 03/01 |  | guionizado |  |
| F-146 | Ciclo al pulsar | 02b/02-conceder · 03/03-excluir · 08f/02-conceder-en-el-padre · 08f/04-excluir-en-el-hijo · 08g/02-quitar-y-guardar |  | guionizado |  |
| F-147 | Alcance | 02b/03-alcance · 08d/06-cambiar-a-equipo |  | guionizado |  |
| F-148 | Barra de guardado por lote | 02b/02-conceder · 02b/05-guardar-o-descartar · 03/03-excluir · 08d/06-cambiar-a-equipo · 08f/02-conceder-en-el-padre · 08f/04-excluir-en-el-hijo · 08g/02-quitar-y-guardar |  | guionizado |  |
| F-149 | Éxito / error al guardar permisos | 02b/05-guardar-o-descartar |  | guionizado |  |
| F-150 | Vacío / error / carga del editor | 02b/04-buscar-permiso |  | guionizado (voz) | solo el vacío de búsqueda; carga y error no se provocan |
| F-151 | Pantalla estrecha | — | | no aplica | ancho ≤991 px; el video es 1280 |
| F-152 | Tabla de titulares | 03/05-titulares |  | guionizado |  |
| F-153 | Abrir una persona | 03/05-titulares |  | guionizado |  |
| F-154 | Más de 50 | 03/05-titulares |  | guionizado (voz) | la demo no pasa de 50 |
| F-155 | Vacío | 03/05-titulares |  | guionizado (voz) |  |
| F-156 | Entradas | 03/06-historial · 08g/05-el-rastro (voz) |  | guionizado |  |
| F-157 | Vacío | 02a/02-rol-del-sistema |  | guionizado | autor D: Historial de Contador (rol del sistema, sin eventos de la empresa en E0) → «No se encontraron registros»; selector del código, a confirmar en el ensayo |
| F-158 | Títulos y botón | 02a/03-duplicar · 02a/04-crear-rol |  | guionizado | voz aclara Duplicar = Clonar (D-07) |
| F-159 | Aviso de clonado | 02a/03-duplicar |  | guionizado |  |
| F-160 | Nombre | 02a/03-duplicar |  | guionizado |  |
| F-161 | Descripción | 02a/04-crear-rol |  | guionizado |  |
| F-162 | Herencia: interruptor | 03/02-crear-hijo |  | guionizado |  |
| F-163 | Herencia: elegir el padre | 03/02-crear-hijo |  | guionizado |  |
| F-164 | Aviso de herencia | 03/02-crear-hijo |  | guionizado |  |
| F-165 | Aviso al cambiar el padre (edición) | 03/03-excluir |  | guionizado (voz) |  |
| F-166 | Éxito del rol | 02a/03 · 02a/04 · 03/02 |  | guionizado |  |
| F-167 | Error del rol | 02a/04-crear-rol |  | guionizado (voz) |  |
| F-168 | Salir con cambios (rol) | 02a/04-crear-rol |  | guionizado (voz) |  |
| F-169 | Barra superior | 06a/01 · 06b/04 |  | guionizado |  |
| F-170 | Diálogo «Nueva integración» | 06a/02-crear-credencial |  | guionizado |  |
| F-171 | Campos del alta | 06a/02-crear-credencial |  | guionizado |  |
| F-172 | Restricciones (opcional) | 06a/02-crear-credencial |  | guionizado |  |
| F-173 | IP permitida | 06a/02-crear-credencial |  | guionizado | se señala; no se llena |
| F-174 | Endpoint permitido | 06a/02-crear-credencial |  | guionizado | se señala; no se llena |
| F-175 | Botones del alta | 06a/02-crear-credencial |  | guionizado |  |
| F-176 | Franja del secreto (una sola vez) | 06a/03-guardar-el-secreto · 06b/01 |  | guionizado |  |
| F-177 | Aviso al copiar | 06a/03-guardar-el-secreto |  | guionizado |  |
| F-178 | Tabla de credenciales | 06a/01-que-es-una-credencial |  | guionizado |  |
| F-179 | Carga, error y vacío de la lista | — | | no se provoca | carga/error; el vacío no se da (hay credenciales) |
| F-180 | Notas al pie | 06a/01-que-es-una-credencial |  | guionizado |  |
| F-181 | Panel de la credencial | 06a/04-panel |  | guionizado |  |
| F-182 | Botón «Editar permisos» | 06a/05-sus-permisos · 06c/04 |  | guionizado | D-05: se graba solo con Rosa |
| F-183 | Botón «Rotar secreto» | 06b/01-rotar-secreto |  | guionizado |  |
| F-184 | «Más acciones» › Desactivar / Activar | 06b/02-desactivar-activar |  | guionizado |  |
| F-185 | «Más acciones» › Revocar y eliminar | 06b/03-revocar |  | guionizado |  |
| F-186 | Bloque «Permisos» del panel | 06a/04-panel |  | guionizado |  |
| F-187 | Bloque «Operaciones en 7 días» | 06a/04-panel |  | guionizado |  |
| F-188 | Credencial inexistente | — | | no se provoca | enlace a una credencial borrada |
| F-189 | Cabecera | 06a/05-sus-permisos |  | guionizado |  |
| F-190 | Tarjeta de datos | 06a/05-sus-permisos |  | guionizado (voz) | autor B: sin marca propia; selector no verificado |
| F-191 | Permisos por módulo | 06a/05-sus-permisos · 06c/04 |  | guionizado |  |
| F-192 | Mensajes de la página | 06a/05-sus-permisos · 06c/04-conceder |  | guionizado | autor B: SI hay toasts («Permiso quitado/concedido exitosamente»); el plan asumía que no |
| F-193 | Volver | 06a/05-sus-permisos |  | guionizado |  |
| F-194 | Dónde está | 06b/04-documentacion |  | guionizado |  |
| F-195 | Barra lateral | 06b/04-documentacion |  | guionizado | D-09: labels sin acento si no se corrige |
| F-196 | Contenido | 06b/04-documentacion |  | guionizado | «Documento no encontrado» no se provoca |
| F-197 | Filtro Período | 07/01-la-bitacora · 07/02-filtros · 07/03-detalle-del-evento |  | guionizado |  |
| F-198 | Filtro Persona | 07/02-filtros |  | guionizado |  |
| F-199 | Filtro Acciones | 07/02-filtros |  | guionizado |  |
| F-200 | Filtro Registro | 07/02-filtros |  | guionizado |  |
| F-201 | Filtro IP | 07/02-filtros |  | guionizado | autor C: se muestra en pantalla (10.9.9.9 → vacío); antes se preveía solo en voz |
| F-202 | «Limpiar» | 07/02-filtros |  | guionizado |  |
| F-203 | Total | 07/01-la-bitacora |  | guionizado |  |
| F-204 | Agrupación por día | 07/01-la-bitacora |  | guionizado |  |
| F-205 | Fila de evento | 07/01-la-bitacora |  | guionizado |  |
| F-206 | Nombre legible del registro | 07/01-la-bitacora |  | guionizado (voz) | autor C: no se lee la etiqueta (D-S7 en corrección) |
| F-207 | Carga, error y vacío | 07/02-filtros |  | guionizado | autor C: el vacío filtrado SÍ se muestra en pantalla; carga/error siguen sin provocarse |
| F-208 | «Cargar eventos anteriores» | 07/04-historial-y-persona |  | guionizado (voz) |  |
| F-209 | Detalle del evento | 07/03-detalle-del-evento · 08g/05-el-rastro |  | guionizado |  |
| F-210 | «Qué cambió» (antes → después) | 07/03-detalle-del-evento · 08g/05-el-rastro |  | guionizado |  |
| F-211 | «Solicitud» (origen) | 07/03-detalle-del-evento · 08g/05-el-rastro |  | guionizado |  |
| F-212 | «Historial del registro →» | 07/04-historial-y-persona |  | guionizado |  |
| F-213 | «Ver a {persona} →» | 07/04-historial-y-persona |  | guionizado |  |
| F-214 | Evento fuera del filtro | 07/04-historial-y-persona |  | guionizado (voz) |  |
| F-215 | Llegadas ya filtradas | 01/03-actividad-reciente · 01/04-caso-practico · 04a/04-su-actividad · 06c/04-conceder · 07/04-historial-y-persona |  | guionizado |  |
| F-216 | Cómo llegar a Mi perfil | 09/01-contrasena-en-mi-perfil |  | guionizado |  |
| F-217 | Cambio de contraseña | 09/01-contrasena-en-mi-perfil |  | guionizado | se llena y no se envía |
| F-218 | Cuenta con la clave bloqueada | 09/01-contrasena-en-mi-perfil |  | guionizado (voz) |  |
| F-219 | Visibilidad del menú | 09/02-visibilidad-del-menu |  | guionizado |  |
| F-220 | Contenido de Visibilidad del menú | 09/02-visibilidad-del-menu |  | guionizado |  |
| F-221 | Mensajes de Visibilidad del menú | 09/02-visibilidad-del-menu |  | guionizado |  |
| F-222 | Perfil del Consultorio | 09/03-perfil-consultorio (tarjeta) |  | guionizado | autor A: pantalla + voz; se navega a la ruta y se ve que vuelve al inicio |
| F-223 | Textos del Perfil del Consultorio | 09/03-perfil-consultorio (tarjeta) |  | no aplica | pantalla de RegiSalud; no existe en el ERP |
| F-224 | Relevancia para una serie del ERP | 09/03-perfil-consultorio (tarjeta) |  | guionizado (voz) |  |
| F-225 | USER_VIEW | 08a/04-con-seguridad · 00/03 |  | guionizado |  |
| F-226 | TEAM_VIEW | 08h/06-sin-equipos · 08h/02-con-equipos |  | guionizado | autor D: en pantalla, Marta ve Zona Este y sus miembros solo con ver; el lado «sin» va en voz, verificado en código (html:19; ningún usuario demo tiene USER_VIEW sin TEAM_VIEW, D-04) |
| F-227 | USER_CREATE | 08a/04-con-seguridad |  | guionizado | Marta sin «Nuevo» |
| F-228 | USER_EDIT | 08h/01-con-personas · 08h/05-sin-personas |  | guionizado | autor D: mismo panel de Ana: Rosa con Editar, Cambiar contraseña, «+ Asignar rol» y Desactivar; Marta sin ellos (v08a-09) |
| F-229 | USER_DELETE | 08h/01-con-personas · 08h/05-sin-personas |  | guionizado | autor D: «Eliminar» en el ⋮ de Rosa; el ⋮ de Marta solo trae «Ver su actividad» (hasPersonMenu por AUDIT_LOG_READ) |
| F-230 | TEAM_CREATE / TEAM_EDIT / TEAM_DELETE | 08h/02-con-equipos · 08h/06-sin-equipos |  | guionizado | autor D: «+» Nuevo equipo, «Editar equipo» y papelera con Rosa; ausentes con Marta (v08a-09 para el «+»; el resto verificado en código, a confirmar en el ensayo) |
| F-231 | TEAM_MANAGE_MEMBERS | 08h/02-con-equipos · 08h/06-sin-equipos |  | guionizado | autor D: la barra de selección de Rosa trae Agregar/Quitar; la de Marta solo «Limpiar» (código html:82, a confirmar en el ensayo) |
| F-232 | ROLE_VIEW | 08a/04-con-seguridad |  | guionizado |  |
| F-233 | ROLE_CREATE | 08a/04-con-seguridad |  | guionizado | sin «Duplicar» |
| F-234 | ROLE_EDIT | 08a/04-con-seguridad |  | guionizado | acciones en gris |
| F-235 | ROLE_DELETE | 08a/04-con-seguridad |  | guionizado |  |
| F-236 | AUDIT_LOG_READ | 03/06-historial (voz) · 08g/05-el-rastro |  | guionizado |  |
| F-237 | INTEGRATION_USER_VIEW | 08a/05-sin-integraciones |  | guionizado |  |
| F-238 | INTEGRATION_USER_CREATE | 08h/03-con-credenciales · 08h/07-sin-credenciales |  | guionizado | autor D: Rosa concede solo «Ver» al Auditor en 08h/04 (E0 no lo tiene: se dice en voz); Marta ve la lista sin «Nueva credencial» (a5-06 vs a5-01) |
| F-239 | INTEGRATION_USER_EDIT | 08h/03-con-credenciales · 08h/07-sin-credenciales |  | guionizado | autor D: sin «Rotar secreto» ni Desactivar; el botón pasa de «Editar permisos» a «Ver permisos» (a5-06). «Ver permisos» no se pulsa (D-S3/D-05) |
| F-240 | INTEGRATION_USER_DELETE | 08h/03-con-credenciales · 08h/07-sin-credenciales |  | guionizado | autor D: «Revocar y eliminar» en el ⋮ de Rosa; Marta no tiene ⋮ (a5-06) |
| F-241 | Sin permiso de front | — | | no se enseña (defecto / en corrección) | D-05: «Editar permisos» sin control de permiso; no se muestra a quien no debe |
| F-242 | PERMISSION_VIEW, AUDIT_VIEW | — | | no se enseña (defecto / en corrección) | D-03: permisos que solo encienden el menú; ningún usuario demo los tiene sueltos |
| F-243 | Tiene alguna pestaña pero no la pedida (p. ej. /security/auditoria sin AUDIT_LO… | 08a/05-sin-integraciones |  | guionizado |  |
| F-244 | Entra por el menú («Seguridad» → /security/resumen) sin USER_VIEW | — | | no se enseña (defecto / en corrección) | D-02: ningún usuario demo entra sin USER_VIEW a la consola |
| F-245 | No tiene ninguno de los permisos de pestaña | 08a/05-sin-integraciones |  | guionizado (voz) | caso «sin ninguna pestaña» solo en voz |
| F-246 | Pide ?nuevo=1 sin el permiso de alta | — | | técnico interno — no visible, no se enseña | ?nuevo=1 sin permiso no produce nada visible |
| F-247 | Pide /security/integration-user/:id/permissions sin permisos | — | | no se enseña (defecto / en corrección) | D-05 (INFERIDO); no se graba |
| F-248 | Pide /my-company/perfil-consultorio sin COMPANY_UPDATE o en el ERP | 09/03-perfil-consultorio |  | guionizado (voz) |  |
| F-249 | Servicio de permisos | — | | técnico interno — no visible, no se enseña | servicio del front |
| F-250 | Menú lateral | 08a/01-con-ventas · 08a/02-sin-ventas-menu · 08g/03-despues |  | guionizado |  |
| F-251 | Guard por data.permissions (URL directa) | 08a/03-sin-ventas-url · 08g/04-por-direccion |  | guionizado | autor C: toast «No tienes permiso para ver «…»»; ya no es «sin aviso» como preveía el plan |
| F-252 | Guard canActivateRouteByPermissionsFn (otras rutas) | 08a/03-sin-ventas-url |  | guionizado (voz) | autor C: el contraste con /my-company ya no existe; las dos rutas avisan igual (toast) |
| F-253 | Botones de listas dinámicas | 08b/03-sin-crear · 08c/02-sin-exportar · 08c/06-sin-eliminar |  | guionizado |  |
| F-254 | Cotizaciones: lista | 08b/01-con-crear · 08b/03-sin-crear |  | guionizado |  |
| F-255 | Cotizaciones: formulario | 08e/04-con-estado-aprobada · 08e/05-sin-estado-borrador |  | guionizado |  |
| F-256 | Cotizaciones: estados (stepper) | 08e/02 · 08e/03 · 08b/02 · 08b/04 |  | guionizado |  |
| F-257 | Productos: lista | 08c/01-con-exportar … 08c/06-sin-eliminar · 08g/01-antes |  | guionizado |  |
| F-258 | Alcance en el front | 08d/03-propios |  | guionizado |  |
| F-259 | VISTA | 08a/01-con-ventas (todo el video) |  | guionizado |  |
| F-260 | ACCIÓN | 08b/01-con-crear (todo 08b y 08c) |  | guionizado |  |
| F-261 | ALCANCE | 08d/01-que-es-el-alcance (todo el video) |  | guionizado | confirmado por A-016: filtra por creador |
| F-262 | ESTADO | 08e/01-permiso-y-estado (todo el video) |  | guionizado |  |
| F-263 | Pestañas de la consola | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-264 | Aviso de pestaña denegada | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-265 | Buscador global | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-266 | Menú Nuevo | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-267 | Cifras del Resumen | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-268 | Personas | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-269 | Roles | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-270 | Editor | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-271 | Integraciones | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-272 | Auditoría | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-273 | Diálogos | — | | técnico interno — no visible, no se enseña | selector para el guionista |
| F-274 | Nota | — | | técnico interno — no visible, no se enseña | selector para el guionista |

## API (A-###)

| ID | Qué | Video / paso | Minuto | Estado | Motivo / nota |
|---|---|---|---|---|---|
| A-001 | Tabla roles | — | | técnico interno — no visible, no se enseña | modelo de datos |
| A-002 | Rol de empresa vs rol del sistema | 02a/02-rol-del-sistema |  | guionizado |  |
| A-003 | Visibilidad de roles por empresa | 02a/01-lista-de-roles |  | guionizado (voz) | roles ocultos (Referidor, fuera del plan) se nombran; el 404 no |
| A-004 | Crear / clonar | 02a/03-duplicar · 02a/04-crear-rol |  | guionizado |  |
| A-005 | Modelo | 03/01-rol-hijo · 05/01 |  | guionizado |  |
| A-006 | Recálculo | 03/01-rol-hijo (voz) · 03/02-crear-hijo (voz) · 08f/03-llega-al-hijo |  | guionizado |  |
| A-007 | Profundidad y ciclos | 03/02-crear-hijo |  | guionizado (voz) | los mensajes de ciclo no se provocan; la lista ya excluye descendientes |
| A-008 | Exclusiones | 03/03-excluir · 08f/04 |  | guionizado |  |
| A-009 | Borrar un rol padre | 03/05-eliminar-rol |  | guionizado (voz) | cartel «cuidado»; no se provoca el 422 |
| A-010 | Tabla permission | 00/02-seis-conceptos |  | guionizado (voz) | solo el concepto; la tabla es interna |
| A-011 | Recurso / acción NO son columnas | 02b/01-modulos-y-leyenda |  | guionizado |  |
| A-012 | Secciones del editor | 02b/01-modulos-y-leyenda |  | guionizado |  |
| A-013 | Qué se ofrece | 02b/01 · 05/04 |  | guionizado (voz) |  |
| A-014 | Dónde se guarda | 02b/03-alcance |  | guionizado |  |
| A-015 | Cómo se resuelve | 08d/06-cambiar-a-equipo · 08d/07-equipo |  | guionizado |  |
| A-016 | Dónde se APLICA de verdad | 08d/03-propios |  | guionizado | confirmado por autor C (08d/01–03): el filtro es por quién creó el registro |
| A-017 | Límite práctico decisivo para el video | 02b/03-alcance (voz, límite) · 08d/04-ajena-por-numero |  | guionizado | CAMBIA respecto al plan (autor C): el API ya responde 403 al abrir por número; la UI lo mostrará tras D-S4 |
| A-018 | NO EXISTEN en el API. | 08e/01 · 08e/05 |  | guionizado (voz) | se dice que no es un filtro del rol |
| A-019 | Tablas | 04c |  | guionizado |  |
| A-020 | Un equipo NO da permisos. | 04c/01 · 05/04 · 08f/05 |  | guionizado |  |
| A-021 | Endpoints | — | | técnico interno — no visible, no se enseña | endpoints |
| A-022 | Cálculo en el guard | 05/04-equipo-no-suma (voz) · 06c/05-repetir · 08g/02-quitar-y-guardar (voz) |  | guionizado | autor B: la misma consulta pasa de 403 a 200 en pantalla (06c/05) |
| A-023 | Plan | 05/04-equipo-no-suma |  | guionizado (voz) |  |
| A-024 | Panel de persona | 04a/03 · 05/02–04 |  | guionizado |  |
| A-025 | Personas | 04a/01-vistas |  | guionizado |  |
| A-026 | Historial de ingresos = bitácora | 04a/03-ficha-de-la-persona |  | guionizado |  |
| A-027 | Listado de personas | 04a/01 · 04a/02 |  | guionizado |  |
| A-028 | GET /api/v1/security/overview | 01/01-cifras |  | guionizado |  |
| A-029 | «Requiere atención» | 01/02-requiere-atencion |  | guionizado |  |
| A-030 | Actividad reciente | 01/03-actividad-reciente |  | guionizado |  |
| A-031 | CRUD | 02a/04-crear-rol |  | guionizado (voz) | solo el aviso de nombre repetido; el resto es técnico |
| A-032 | GET /api/role/:id/permission-matrix | — | | técnico interno — no visible, no se enseña | endpoint de la matriz (lo pinta 02b) |
| A-033 | PATCH /api/role/:id/permissions | 02b/05-guardar-o-descartar |  | guionizado (voz) | un solo guardado = una sola operación; los errores no se provocan |
| A-034 | Endpoints antiguos conservados | — | | técnico interno — no visible, no se enseña | endpoints antiguos, sin UI |
| A-035 | Titulares del rol | 03/04-titulares-e-historial |  | guionizado |  |
| A-036 | Historial del rol | 03/04-titulares-e-historial |  | guionizado |  |
| A-037 | Catálogo de permisos | — | | técnico interno — no visible, no se enseña | catálogo de permisos |
| A-038 | Endpoints | 04b |  | guionizado |  |
| A-039 | Reglas de asignación de roles | 04b/03-asignar-rol |  | guionizado (voz) | cartel y voz; los errores no se provocan |
| A-040 | Acciones masivas | 04c/03-agregar-miembros | | técnico interno — no visible, no se enseña | el front itera uno a uno; invisible |
| A-041 | Endpoints | — | | técnico interno — no visible, no se enseña | endpoints (los usa la UI de 06a/06b) |
| A-042 | Creación y secreto | 06a/02 · 06a/03 |  | guionizado |  |
| A-043 | Permisos por módulo de la credencial | 06a/05-sus-permisos |  | guionizado (voz) | autor B: la voz explica que los permisos propios se conceden al primer cambio |
| A-044 | Resumen / actividad 7 días | 06a/04-panel |  | guionizado | las consultas no cuentan como operaciones |
| A-045 | Rotación y revocación | 06b/01 · 06b/02 |  | guionizado |  |
| A-046 | Swagger | — | | no aplica | Swagger solo en NODE_ENV=local; no existe para el cliente |
| A-047 | Documentación de producto | 06b/04-documentacion |  | guionizado |  |
| A-048 | GET /api/v1/audit-logs | 07/02-filtros |  | guionizado |  |
| A-049 | Historial de un registro | 07/04-historial-y-persona |  | guionizado |  |
| A-050 | Qué guarda cada evento | 07/03-detalle-del-evento |  | guionizado |  |
| A-051 | Dos vías | 06c/01-el-programa |  | guionizado (voz) | se usa la vía token; las cabeceras se nombran |
| A-052 | Respuesta cuando NO tiene el permiso | 06c/03-consulta-no-permitida |  | guionizado |  |
| A-053 | Ejemplo grabable (empresa 43, credencial recién creada con la plantilla) | 06c | | técnico interno — no visible, no se enseña | receta de la lámina (preparación) |
| A-054 | Códigos (BD local) | 08b · 08c · 08e | | técnico interno — no visible, no se enseña | tabla de códigos para preparar roles |
| A-055 | Alcance «Propios» — qué lo respeta DE VERDAD | 08d/02-todos · 08d/03-propios · 08d/04-ajena-por-numero |  | guionizado |  |
| A-056 | Filtros de ESTADO | 08e/05 |  | guionizado (voz) | igual que A-018 |
| A-057 | Casos con/sin permiso demostrables de verdad en la app | 06c/02-consulta-permitida · 06c/03-consulta-no-permitida |  | guionizado | caso demostrable de verdad; el resto de la fila (08a–08e) es contraste con/sin, no un paso único |
| A-058 | Sí, con antes/después legible | 07/03 · 08g/04 |  | guionizado |  |
| A-059 | Además | 07/03-detalle-del-evento |  | guionizado | autor D: se marca la celda Registro de la fila «Creó · permiso de rol #11034», bajo el «Cambió permisos» sembrado; la voz no lee la etiqueta (D-S7 en corrección) |
| A-060 | Cómo verlo | 07/01-la-bitacora · 07/04-historial-y-persona · 03/05-titulares · 03/06-historial · 08g/05-el-rastro |  | guionizado |  |
| A-061 | #1336 NO trae migraciones | — | | técnico interno — no visible, no se enseña | estado de esquema |
| A-062 | Migraciones pendientes en germiva local | — | | técnico interno — no visible, no se enseña | migraciones pendientes |
| A-063 | Alta de empresa y usuarios | — | | técnico interno — no visible, no se enseña | receta de alta (sembrar.mjs) |
| A-064 | Empresa demo 43 hoy | — | | no aplica | empresa 43 descartada: se crea «Distribuidora Las Palmas» |
| A-065 | Propios en GET /v1/product (INFERIDO) | — | | INFERIDO — no se enseña | la serie no usa el alcance en Productos |
| A-066 | Caché de roles y alcance (INFERIDO) | 08d/07-equipo |  | INFERIDO — no se enseña | se vuelve a entrar tras el cambio; pregunta abierta 10 |
| A-067 | Front no revisado por el autor API | — | | técnico interno — no visible, no se enseña | resuelto por el inventario FE |
| A-068 | Cupo de usuarios del plan | — | | INFERIDO — no se enseña | cupo de usuarios del plan; no se enseña |
| A-069 | Borrar un rol no quita el acceso | — | | no se enseña (defecto / en corrección) | borrar rol con titulares; en 03/05 se borra un rol SIN titulares |
| A-070 | Escalada por isAdminRole | — | | no se enseña (defecto / en corrección) | escalada por isAdminRole; no se enseña |
| A-071 | «Propios» solo filtra listados | — | | no se enseña (defecto / en corrección) | el video no promete que «Propios» limite abrir o editar |
| A-072 | Nombres poco claros en el 403 | 06c/03 | | no se enseña (defecto / en corrección) | se usa Productos (nombre claro) en vez de «Facturas Socios» |
| A-073 | EMPTY_ROLE con LIMIT 20 | — | | no se enseña (defecto / en corrección) | tope 20 en roles vacíos; la demo tiene 1 |
| A-074 | Filtro entityName=roles mezcla registros | 07/04 | | no se enseña (defecto / en corrección) | se usa «Historial del registro» (coincidencia exacta) |
| A-075 | PERMISSIONS_CHANGED solo en guardado en lote | 06a/05 | | no se enseña (defecto / en corrección) | no se promete antes/después para permisos de credenciales |
| A-076 | Rol huérfano, equipos borrados, purchases con INVOICE_VIEW | — | | no se enseña (defecto / en corrección) | rol huérfano al borrar credencial; no se enseña |

## Defectos del inventario FE (D-##) y cómo los trata la serie

| D | Efecto en la serie |
|---|---|
| D-01 | 04b/03 depende del arreglo en `fix/security-video-findings` (pregunta abierta 3). Si no llega, el rol se enseña solo al crear (04b/01) |
| D-02 | Ningún usuario demo entra a la consola sin USER_VIEW (Marta lo tiene) |
| D-03 | Nadie de la demo tiene PERMISSION_VIEW ni AUDIT_VIEW sueltos |
| D-04 | Nadie tiene TEAM_VIEW sin USER_VIEW |
| D-05 | «Editar permisos» de una credencial solo lo pulsa Rosa (06a/05, 06c/04) |
| D-06 | «Ver su actividad» se graba con Rosa (04a/04); la auditora usa la pestaña Auditoría (08g/04) |
| D-07 | La voz aclara que «Duplicar» abre «Clonar Rol» (02a/03) |
| D-08 | El asunto «nunca inició sesión» no se describe como «reenviar invitación» (01/02) |
| D-09 | 06b/04 no marca ni lee las etiquetas sin acento, si siguen así |
| D-10 | 06a/05 muestra la página tal cual; la voz dice «Integraciones» |
| D-11 | El buscador global solo se usa para personas (00/03) |
| D-12 | No se usan enlaces `/security/role/:id` |
| D-13 | La voz nombra cada aviso por su forma (diálogo o toast) |
| D-14 | Los errores de las subvistas del rol no se provocan |
