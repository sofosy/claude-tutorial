# Cobertura · AUTOR C (videos 07 y 08a–08g) — para fusionar en `_COBERTURA-SEGURIDAD.md`

AUTOR C · 2026-09-27. Formato: **punto → guion/paso** (estado). Guiones en `guiones/`:
`seguridad-07-auditoria`, `seguridad-08a-vista`, `seguridad-08b-crear-editar-anular`,
`seguridad-08c-exportar-eliminar`, `seguridad-08d-alcance`, `seguridad-08e-aprobar-y-estado`,
`seguridad-08f-herencia`, `seguridad-08g-cambio-en-vivo`. «pantalla» = marca o acción en cámara; «voz» = solo
narración o cartel. Los pasos del plan cambiaron de id: se da el id REAL.

## Front (F-###)

| Punto | Guion / paso | Estado | Nota |
|---|---|---|---|
| F-002 Entrada del menú Seguridad | 08a/04-con-seguridad | pantalla | Marta la pulsa |
| F-007 Historial por la ruta vieja | — | no se enseña | ruta vieja; se enseña «Historial del registro» (07/04) |
| F-014 Permiso de cada pestaña | 08a/04 · 08a/05 | pantalla | 4 pestañas para Marta, sin Integraciones |
| F-015 Aviso de pestaña denegada | 08a/05-sin-integraciones | pantalla | `.console-denied` |
| F-017 Botón «Nuevo» | 08a/04 | pantalla | ausente para Marta (marca `.gm-sheet__actions`) |
| F-023 Etiquetas de acción | 07/01-la-bitacora | pantalla + voz | colores dichos en voz |
| F-025 Origen legible | 07/03-detalle-del-evento · 08g/05-el-rastro | pantalla + voz | sin afirmar cuál sale |
| F-146 Ciclo al pulsar | 08f/04-excluir-en-el-hijo · 08g/02-quitar-y-guardar · 08f/02 | pantalla | heredado → excluido; concedido → sin conceder |
| F-147 Alcance (segmentado) | 08d/06-cambiar-a-equipo | pantalla | Propios → Equipo |
| F-148 Barra de guardado | 08d/06 · 08f/02 · 08f/04 · 08g/02 | pantalla | «afectan a 3 / 1 personas» |
| F-156 Entradas del historial del rol | — | no se enseña aquí | el rastro de 08g se enseña en Auditoría (07/08g) |
| F-197 Período | 07/02-filtros · 07/03 | pantalla | 30 días; Todo el historial |
| F-198 Persona | 07/02-filtros | pantalla | usuario de Ana (dep. D-S5) |
| F-199 Acciones (multi) | 07/02-filtros | pantalla | «Creó»; menú abierto + Escape |
| F-200 Registro | 07/02-filtros | pantalla + voz | `quotes`, nombre interno explicado |
| F-201 IP | 07/02-filtros | pantalla | `10.9.9.9` → vacío (antes era solo voz) |
| F-202 Limpiar | 07/02-filtros | pantalla | |
| F-203 Total | 07/01 · 07/04 | pantalla | |
| F-204 Agrupación por día | 07/01-la-bitacora | pantalla | la voz no dice la fecha (R13) |
| F-205 Fila de evento | 07/01-la-bitacora | pantalla | Hora · Quién · Acción · Registro · IP |
| F-206 Nombre legible del registro | 07/01 · 07/03 | voz | no se lee la etiqueta (D-S7 en corrección) |
| F-207 Vacío filtrado | 07/02-filtros | pantalla | carga/error no se provocan |
| F-208 Cargar eventos anteriores | 07/04 | voz | |
| F-209 Detalle del evento | 07/03 · 08g/05 | pantalla | |
| F-210 Qué cambió (antes → después) | 07/03 · 08g/05 | pantalla | Almacén (+Exportar) · Vendedor (Ver → —) |
| F-211 Solicitud (origen) | 07/03 · 08g/05 | pantalla | IP (mapa_fijo → 192.168.1.25), Origen, evento, solicitud |
| F-212 Historial del registro | 07/04 | pantalla | |
| F-213 Ver a {persona} | 07/04 | pantalla | |
| F-214 Evento fuera del filtro | 07/04 | voz | |
| F-215 Llegadas ya filtradas | 07/04 | pantalla | Historial y «Ver a» llegan filtrados |
| F-225 USER_VIEW | 08a/04 | pantalla | Marta ve Resumen/Personas |
| F-227 USER_CREATE | 08a/04 | pantalla | sin «Nuevo» |
| F-228 / F-229 / F-230 / F-231 USER_EDIT, USER_DELETE, TEAM_* | — | no se enseña (tiempo) | verificado en v08a-09 (panel de Ana para Marta sin Editar ni «+» de equipo); la voz lo resume: «no crea ni edita nada» |
| F-232 ROLE_VIEW | 08a/04 | pantalla | |
| F-233 ROLE_CREATE | 08a/04 | pantalla + voz | sin «Duplicar» |
| F-234 ROLE_EDIT | 08a/04 | pantalla | casillas en gris (`.rpe__act[disabled]`) |
| F-235 ROLE_DELETE | 08a/04 | pantalla | cabecera sin ⋮ (se marca la cabecera; la voz nombra Duplicar y Editar) |
| F-236 AUDIT_LOG_READ | 08g/05-el-rastro | pantalla | Marta abre Auditoría |
| F-237 INTEGRATION_USER_VIEW | 08a/05 | pantalla | |
| F-243 Pestaña no permitida por dirección | 08a/05 | pantalla | |
| F-245 Sin ninguna pestaña | 08a/05 | voz | |
| F-250 Menú lateral | 08a/01 · 08a/02 · 08g/03 | pantalla | Ventas aparece/desaparece; Inventario desaparece tras el cambio |
| F-251 Guard por dirección | 08a/03 · 08g/04 | pantalla | toast «No tienes permiso para ver «…»» (ya no es «sin aviso») |
| F-252 Guard con toast (otras rutas) | 08a/03 | voz | el contraste con `/my-company` ya no existe: las dos avisan igual |
| F-253 Botones de listas dinámicas | 08b/03 · 08c/02 · 08c/06 | pantalla | desaparecen, no se ponen en gris |
| F-254 Cotizaciones: lista | 08b/01 · 08b/03 | pantalla | Crear Cotización + Duplicar |
| F-255 Cotizaciones: formulario (Convertir a factura) | 08e/04 · 08e/05 | pantalla | aparece en Aprobada, desaparece en Borrador |
| F-256 Stepper | 08e/02 · 08e/03 · 08b/02 · 08b/04 | pantalla | Aprobada (QUOTE_APPROVE) y Cancelada (QUOTE_UPDATE) |
| F-257 Productos: lista | 08c/01–06 · 08g/01 | pantalla | Importar/Exportar y Eliminar |
| F-258 Alcance en el front | 08d/03-propios | pantalla + voz | «no hay rótulo: se nota en lo que falta» |
| F-259 VISTA | 08a (todo) | pantalla | |
| F-260 ACCIÓN | 08b · 08c · 08e/02–03 | pantalla | |
| F-261 ALCANCE | 08d (todo) | pantalla | 8 · 3 · 5 |
| F-262 ESTADO | 08e/01 · 08e/04–05 | pantalla | |

## API (A-###)

| Punto | Guion / paso | Estado | Nota |
|---|---|---|---|
| A-006 Recálculo de la herencia | 08f/03-llega-al-hijo | pantalla | heredado en Vendedor sénior y en el acceso efectivo de Carlos |
| A-008 Exclusiones | 08f/04 · 08f/05 | pantalla | |
| A-015 Cómo se resuelve Equipo | 08d/06 · 08d/07 | pantalla | Ana + José = 5 |
| A-016 Filtra por quién creó | 08d/01–03 | pantalla + voz | |
| A-017 Detalle por número | 08d/04-ajena-por-numero | pantalla | CAMBIA respecto al plan: el API ya responde 403 al abrir por número (A6); la UI lo mostrará tras D-S4 |
| A-018 / A-056 No hay filtros por estado | 08e/05 | voz | «esto no se configura en el rol» |
| A-020 Un equipo no da permisos | 08f/01 (diagrama fase 3) · 08f/05 (cartel) · 08d/07 (cartel) | pantalla + voz | |
| A-022 Cálculo en cada petición | 08g/02 (cartel) · 08g/03 | voz | «el servidor revisa el permiso en cada operación» |
| A-048 Filtros de la bitácora | 07/02 | pantalla | |
| A-049 Historial de un registro | 07/04 | pantalla | |
| A-050 Qué guarda cada evento | 07/03 | pantalla | |
| A-055 Qué respeta «Propios» | 08d | pantalla | listado y detalle por número |
| A-057 Casos con/sin demostrables | 08a–08g | pantalla | |
| A-058 Antes/después legible | 07/03 · 08g/05 | pantalla | |
| A-059 «Rol asignado», «Permisos del rol» | — | no se enseña | no aparecen en los eventos que se abren |
| A-060 Cómo verlo | 07 · 08g/05 | pantalla | |
| A-066 Caché de roles y alcance | 08d/07 | INFERIDO — no se enseña | Ana vuelve a entrar tras el cambio |
| A-074 Filtro Registro por palabras | 07/04 | no se enseña (defecto) | se usa «Historial del registro» (coincidencia exacta) |

## Puntos del plan que NO se cubren (con motivo)

- **08b/03 — `/sales/quotes/create` por dirección con Marta**: se omite; hoy el aviso nombra «Cotizaciones»,
  que Marta SÍ puede ver (D-S8, no está en la ronda 2).
- **08f/03 y 08f/05 del plan — «Nuevo Cliente» en la pantalla de Carlos**: se sustituye por su acceso efectivo
  (mismo punto CON/SIN en la ficha de Personas) para no pasar de 4:10; verificado en r08f.
- **08a/04 — botones de la ficha de persona para Marta** (Editar, Cambiar contraseña, «+» de equipo): no se
  visita el panel (tiempo); resumido en voz.
- **08c del plan — «⋮» de la fila de Productos**: no existe; las acciones son iconos (se enseñan así).
