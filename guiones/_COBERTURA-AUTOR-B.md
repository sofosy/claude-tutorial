# Cobertura · AUTOR B (04a, 04b, 04c, 05, 06a, 06b, 06c) — 2026-09-27

Formato: `punto → guion/paso · cómo`. «pantalla» = marca o acción en cámara; «voz» = solo narración o cartel.
Guiones: `seguridad-04a-personas`, `seguridad-04b-alta-y-edicion`, `seguridad-04c-equipos`,
`seguridad-05-acceso-efectivo`, `seguridad-06a-credenciales`, `seguridad-06b-rotar-pausar-revocar`,
`seguridad-06c-caso-integracion`. Para fusionar en `_COBERTURA-SEGURIDAD.md` (lo edita el orquestador).

## Front (F-###)

| Punto | Guion / paso | Cómo |
|---|---|---|
| F-009 Rutas con página propia | 06a/05-sus-permisos · 06b/04-documentacion | pantalla |
| F-018 Nuevo › Usuario | 04b/01-crear-usuario | pantalla |
| F-020 Nuevo › Equipo | 04c/02-crear-equipo | voz (se usa el «+» del riel) |
| F-021 Nuevo › Integración de API | 06a/02-crear-credencial | voz (se usa «Nueva credencial») |
| F-025 Origen legible del user-agent | 04a/03-ficha-de-la-persona | pantalla + voz («Cliente de API»; con navegador «Chrome en Windows») |
| F-035 Asunto STALE_API_CREDENTIAL | 06b/03-revocar | pantalla (Resumen tras revocar: «3 asuntos») |
| F-042…F-048 Rail «Vistas», vistas y conteos | 04a/01-vistas | pantalla (clic en Sin rol, Nunca entraron, Inactivas, Todas) |
| F-049 Rótulo «Equipos» · F-051 Lista de equipos | 04c/01-que-es-un-equipo | pantalla |
| F-050 Botón «+» Nuevo equipo | 04c/02-crear-equipo | pantalla |
| F-053 Título de la lista | 04c/01 (`.sec-people__title` «Zona Este · 2») · 04c/04 | pantalla |
| F-054 Buscador · F-055 Filtro «Rol» | 04a/02-buscar-y-filtrar | pantalla |
| F-056 «Editar equipo» · F-057 eliminar equipo · F-058 confirmación · F-059 éxito | 04c/04-quitar-editar-eliminar | pantalla |
| F-060 Columnas · F-061 Estado de la persona | 04a/01-vistas · 04b/04 | pantalla |
| F-062 «Seleccionar todas» | 04c/03-agregar-miembros | pantalla (señalada, no se pulsa) |
| F-063 Casilla por fila · F-068 barra de selección · F-069 «Agregar a equipo» · F-070 éxito · F-073 «Limpiar» | 04c/03-agregar-miembros | pantalla (Limpiar señalado) |
| F-066 Vacío de la lista | 04a/02-buscar-y-filtrar | voz |
| F-067 Paginación | 04a/01-vistas | pantalla (pie «Mostrando 1–9 de 9») |
| F-071 «Quitar del equipo» · F-072 éxito | 04c/04-quitar-editar-eliminar | pantalla |
| F-074 Abrir el panel · F-075 cabecera | 04a/03 · 05/02–04 | pantalla |
| F-076 «Editar» · F-077 «Cambiar contraseña» | 04b/02-editar-y-contrasena | pantalla (Editar señalado; Cambiar contraseña usado) |
| F-078 «Más acciones» | 04a/04-su-actividad · 04b/04 · 04b/05 | pantalla |
| F-079 Desactivar / Activar · F-080 éxito | 04b/04-desactivar-activar | pantalla |
| F-081 Ver su actividad | 04a/04-su-actividad | pantalla |
| F-082 Eliminar · F-083 éxito | 04b/05-eliminar | pantalla |
| F-084 Bloque «Roles» | 04a/03 · 04b/03 · 05/02–04 | pantalla |
| F-085 «+ Asignar rol» | 04b/03-asignar-rol | pantalla (D-01 verificado corregido) |
| F-086 «Permisos efectivos» · F-087 «Ver los N módulos» | 04a/03 · 05/02–04 | pantalla |
| F-088 «Últimos ingresos» | 04a/03 · 04a/05 («Sin ingresos registrados») | pantalla |
| F-092 «Nuevo Equipo» · F-094 éxito | 04c/02-crear-equipo | pantalla |
| F-093 «Editar Equipo» | 04c/04 | pantalla |
| F-096 Salir con cambios (equipo) | 04c/04 | voz |
| F-097 Miembros fuera del diálogo | 04c/02 | voz |
| F-098…F-101, F-104…F-106, F-109, F-111, F-112 Alta de usuario | 04b/01-crear-usuario | pantalla |
| F-102 correo existente · F-103 correo eliminado · F-113 usuario repetido · F-115 sin «invitar» | 04b/01-crear-usuario | voz |
| F-107 Cambiar contraseña (edición) | 04b/02-editar-y-contrasena | pantalla |
| F-114 Salir con cambios (usuario) | 04b/02-editar-y-contrasena | voz (movido desde 05) |
| F-169 Barra superior de Integraciones | 06a/02 · 06b/04 | pantalla |
| F-170…F-175 Diálogo «Nueva integración» (nota, campos, restricciones, botones) | 06a/02-crear-credencial | pantalla (IP y endpoint señalados, no se llenan) |
| F-176 Franja del secreto | 06a/03-guardar-el-secreto · 06b/01-rotar-secreto | pantalla («Mostrar» señalado, no pulsado) |
| F-177 Aviso al copiar | 06a/03 · 06b/01 | pantalla (toast «Secreto copiado») |
| F-178 Tabla · F-180 Notas al pie | 06a/01-que-es-una-credencial | pantalla |
| F-181 Panel · F-186 «Permisos» · F-187 «Operaciones en 7 días» | 06a/04-panel | pantalla |
| F-182 «Editar permisos» | 06a/05 · 06c/04 | pantalla (solo Rosa, D-05/D-S3) |
| F-183 «Rotar secreto» | 06b/01 | pantalla |
| F-184 Desactivar / Activar | 06b/02 | pantalla |
| F-185 Revocar y eliminar | 06b/03 | pantalla |
| F-189 Cabecera · F-191 permisos por módulo · F-193 Volver | 06a/05-sus-permisos | pantalla |
| F-190 Tarjeta de datos | 06a/05-sus-permisos | voz (sin marca propia: selector no verificado) |
| F-191 Permisos por módulo (conceder) | 06c/04-conceder | pantalla |
| F-192 Mensajes de la página | 06a/05 · 06c/04 | pantalla (toasts «Permiso quitado/concedido exitosamente») |
| F-194 Dónde está · F-195 barra lateral · F-196 contenido | 06b/04-documentacion | pantalla (títulos sin acento D-S10: no se leen) |
| F-215 Llegadas ya filtradas | 04a/04 (Auditoría `?persona=`) · 06c/04 (`?credencial=`) | pantalla |

## API (A-###)

| Punto | Guion / paso | Cómo |
|---|---|---|
| A-005 Herencia por rol padre | 05/01 · 05/02 | pantalla (lámina + ficha de Carlos) |
| A-013 / A-023 Solo lo contratado | 05/04-equipo-no-suma | voz |
| A-019 / A-020 Equipos, no dan permisos | 04c/01 (cartel) · 05/01 (fase 3) · 05/04 | pantalla + voz |
| A-022 Vale desde la siguiente operación | 05/04 · 06c/05 | voz / pantalla (06c: la misma consulta pasa de 403 a 200) |
| A-024 Panel de persona · A-025/A-027 Personas | 04a/01–03 · 05 | pantalla |
| A-026 Ingresos = bitácora | 04a/03 | pantalla (la voz no nombra la bitácora) |
| A-038 Endpoints de usuario | 04b | pantalla (a través de la UI) |
| A-039 Reglas de asignación | 04b/03-asignar-rol | voz |
| A-042 Creación y secreto | 06a/02 · 06a/03 | pantalla |
| A-043 Permisos propios al primer cambio | 06a/05 | voz |
| A-044 Actividad de 7 días | 06a/04 | pantalla + voz (las consultas no cuentan) |
| A-045 Rotación y revocación | 06b/01–03 | pantalla |
| A-047 Documentación de producto | 06b/04 | pantalla |
| A-051 Dos vías de autenticación | 06c/01 | voz (solo la vía token: «pase temporal»; las cabeceras no se nombran) |
| A-052 Respuesta 403 | 06c/03 | pantalla (lámina) |
| A-057 Caso demostrable | 06c | pantalla |

## No cubiertos (con motivo)

- F-052 «Sin equipos»: la demo siempre tiene «Zona Este»; provocarlo exigiría borrarla en cámara.
- F-226 `TEAM_VIEW` (voz en 04c/01 según el plan): qué ve quien no lo tiene no está verificado en la exploración; la voz no lo afirma.
- F-238/F-239/F-240 `INTEGRATION_USER_CREATE/EDIT/DELETE` (voz en 06a/06b según el plan): no verificado qué botones desaparecen sin cada permiso; no se afirma nada.
- F-064/F-065/F-089/F-090/F-091/F-095/F-179/F-188: estados de carga/error, no se provocan (igual que el plan).
- A-040 acciones masivas, A-041 endpoints, A-053 receta: técnicos, sin cambio.
- A-075 (sin evento antes/después para permisos de credenciales): la voz no promete ese evento.
