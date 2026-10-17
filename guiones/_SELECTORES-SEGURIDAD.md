# Selectores probados · serie «Seguridad» (exploración en vivo, 2026-09-27)

Operador-exploración. Front estático de `fix/security-video-findings` (:4200), API `dist` (:3001), empresa 50,
estado **E0** (y E2a / E6c donde se indica). Playwright headless **1280×720, dsf 1.5**, login real por formulario.
Todo selector marcado ✔ se comprobó con `count()==1` y visible en la pantalla indicada (volcado `selectores_probados`).

- Volcados (DOM útil, botones con `sel_casa`, `mat-label`, `formcontrolname`, clases `.gm-*/.sec-*/.rpe*`, `aria-label`,
  estados vacíos, elementos fijos, choque con el FAB, texto visible): `guiones/exploracion-seguridad/<id>.json`
  + `_resultados-<escenario>.json` (toasts, tiempos, HTTP, filas de BD).
- Capturas con el mismo nombre: `germiva/qa-seguridad-exploracion-2026-09-27/<id>.png`.
- Defectos y verificación de la rama: `germiva/HALLAZGOS-SEGURIDAD-VIDEO.md` (D-S1…D-S13).
- Un selector con `:has-text()` casa por SUBCADENA: «Activas» casa también «Inactivas», «Vendedor» casa «Vendedor sénior»,
  «Clientes» casa «Segmentos de Clientes». Por eso se usan `:has(:text-is('…'))` y `:not(:has-text('sénior'))`.

---

## 0. Global

| Qué | Selector | Nota |
|---|---|---|
| Usuario / clave / Entrar | `input[formcontrolname='username']` · `input[formcontrolname='password']` · `button.auth-primary-btn` | Sin reCAPTCHA visible. Lleva a `/home` en **5,9–8,1 s** (clic → networkidle). Sin modales (R18 OK), sin aviso TRIAL |
| Menú del usuario | `button.topbar-user` ✔ → `.user-item-list:has-text('Mi perfil')` ✔ · `.user-item-list:has-text('Cerrar sesión')` ✔ | Menú: «Mi perfil · Mi Espacio · Bandeja de entrada · Cerrar sesión» |
| Riel: módulo con flyout | `aside.sidebar button.rail-item[aria-label='Ventas']` ✔ → `aside.sidebar a:has-text('Cotizaciones')` ✔ / `a:has-text('Clientes')` ✔ | El flyout «VENTAS» de Ana: Clientes, Cotizaciones |
| Riel: módulo de una opción | `aside.sidebar a.rail-item[aria-label='Inventario']` ✔ (Ana: `href=/inventory/product/list`) · `a.rail-item[href='/security']` ✔ | Un solo destino = enlace directo, sin flyout |
| Contraer panel | `button.panel-collapse` ✔ (aria «Contraer el panel») | Existe en Ventas/Inventario/Cotizaciones. **No existe en `/security/*` ni en `/home`** |
| FAB del asistente | `.chatbot-fab` ✔ (aria «Abrir a Germi») caja **[1200,640,56,56]** | Tapa: extremo derecho de «Guardar cambios» de la barra de guardado, «Página siguiente»/«Última página» de las listas, la 5.ª fila de acciones de Productos |
| Toast | `.mat-mdc-snack-bar-container` | 2,5 s (OK) / 5–6 s (Cerrar). Los guards y las acciones de consola usan toast |
| Diálogo | `mat-dialog-container` | Altas/ediciones (usuario, rol, equipo) y confirmaciones; «Acceso Denegado» (403 con «permiso») también es diálogo, botón «Entendido» |

**Riel de Rosa (Admin):** 17 módulos; «Seguridad» (`a.rail-item[href='/security']`) cae en **y=716 (fuera de 720)**.
Hacer `scroll_into_view` del riel (queda en y=563) o entrar por URL. Para Marta está en y=243, para Ana/Pedro no existe.
**Rieles por usuario (E0):** Ana = Inicio, Ventas, Inventario, Calendario, Configuración · Pedro = Inicio, Inventario,
Calendario, Configuración · Marta = Inicio, Ventas, Inventario, Calendario, Seguridad, Configuración.

---

## 1. Consola (00, 01) — `/security`

El menú lleva a `/security` y aterriza en la **primera pestaña concedida** (Rosa/Marta → `resumen`).

| Qué | Selector ✔ | Texto exacto |
|---|---|---|
| Título / subtítulo | `.gm-sheet__title h1` / `.gm-sheet__title-row` | «Seguridad» / «Quién entra, qué puede hacer y qué cambió.» |
| Buscador | `.security-console__search input` | placeholder y aria «**Buscar persona o rol**» (ya no «…o permiso»). Enter: en Roles filtra el riel (`?q=`), en otra pestaña va a Personas `?q=` |
| Nuevo | `.gm-sheet__actions button:has-text('Nuevo')` → `.mat-mdc-menu-panel button:has-text('Usuario'|'Rol'|'Equipo'|'Integración de API')` | Marta no lo tiene (count 0) |
| Pestañas | `.gm-sheet__tabs a[mat-tab-link]:has-text('Resumen'|'Personas'|'Roles y permisos'|'Integraciones'|'Auditoría')` | Conteos E0: Personas 9 · Roles y permisos 12 · Integraciones 1 |
| Franja sin permiso | `.console-denied` | «No tiene permiso para ver «Integraciones». Solicite el acceso al administrador de la empresa.» (el breadcrumb queda en «Seguridad / Resumen») |

### Resumen — `/security/resumen`
| Qué | Selector ✔ | Texto E0 |
|---|---|---|
| Cifras | `.gm-sheet-fig:has-text('Personas con acceso'|'Administradores'|'Sin ningún rol'|'Credenciales de API'|'Cambios en 7 días')` | 9 «8 activas en 30 días» · 1 «Acceso total a la empresa» · 1 «Entran y no ven ningún módulo» (punto ámbar) · 1 «1 sin uso en 60 días» · 649 «73 de seguridad» (sube con cada toma) |
| Asuntos | `.sec-ov__issue:has-text('sin ningún rol'|'credencial'|'nunca'|'rol sin permisos')`; CTA `… .sec-ov__cta` | «4 asuntos»: «1 persona sin ningún rol / Inician sesión pero no ven ningún módulo. / Luisa Féliz / Asignar rol →» · «1 credencial de API sin uso / Sin llamadas en 60 días. Revócala si ya no se usa. / Tienda en línea anterior / Revisar →» · «1 persona nunca inició sesión / **Comprueba su correo o desactiva la cuenta si ya no la usa.** / Héctor Vargas / **Revisar →**» (abre Personas › Nunca entraron con el panel de Héctor) · «1 rol sin permisos / Asignarlos no da acceso a nada. / Mensajero / Configurar →» (→ `roles?rol=81`) |
| Actividad | `.sec-ov__link` («Ver bitácora →»), filas `.sec-ov__row`, scroll `.gm-sheet-pane .gm-sheet-scroll` | Cabecera CUÁNDO · QUIÉN · ACCIÓN · REGISTRO · IP; «Actualizado hace un momento» |
| Fila del cambio sembrado | `.sec-ov__row:has-text('Roles #79')` ✔ | Dice **«Actualizó · Roles #79»** (no «Cambió permisos», D-S6). Es la 8.ª–9.ª fila, **y=790**, dentro de un scroll interno de 266 px visibles → desplazar el panel antes de señalarla. Abre `/security/auditoria?evento=310792` con el detalle |

---

## 2. Roles y permisos (02a, 02b, 03) — `/security/roles[?rol=id]`

IDs E0: Vendedor 77 · Vendedor sénior 78 · Almacén 79 · Auditor 80 · Mensajero 81 · Admin 1 · Contador 4.
Riel E0 (orden real): «De la empresa»: Mensajero [Vacío] 1 · Auditor (solo lectura) 1 · Almacén 2 · Vendedor 3 · ↳ Vendedor sénior 1;
«Del sistema» (candado): Empleado 0 · Recursos Humanos 0 · Compras 0 · Contador 0 · Supervisor de Caja 0 · Cajero 0 · Admin 1.

| Qué | Selector ✔ | Nota / texto |
|---|---|---|
| Buscar rol | `.sec-roles__search input` | «Buscar rol…» |
| Rol en el riel | `.gm-rail-btn:has-text('Vendedor'):not(:has-text('sénior'))`, `.gm-rail-btn:has-text('Vendedor sénior')`, `…'Mensajero'`, `…'Contador'`, `…'Admin'` | Insignia vacío: `.gm-rail-btn:has-text('Mensajero') .gm-badge--warning` |
| Cabecera | `.sec-roles__h2`; chip `.sec-roles__chip` («Hereda de Vendedor», abre el padre); titulares `.sec-roles__head :text('personas tienen este rol')` | Sénior: «Vendedor con experiencia: aprueba cotizaciones y las convierte en factura · 1 persona tiene este rol» |
| Acciones | `.sec-roles__actions button:has-text('Duplicar')` · `…:has-text('Editar')` · `.sec-roles__actions button[aria-label='Más acciones']` → `.mat-mdc-menu-panel button:has-text('Eliminar rol')` | Rol del sistema: solo «Duplicar». Marta: ninguno |
| Subvistas | `.sec-roles__views button:has-text('Permisos'|'Personas'|'Historial')` | «Personas 2», etc. |
| Aviso sistema | `.rpe__readonly` | «lock «Contador» es un rol del sistema: se ve aquí para saber qué concede. Duplícalo para tener una copia de tu empresa y ajustarla.» (109 acciones `[disabled]`) |
| Módulo | `.rpe__module:has-text('Cotizaciones'|'Productos'|'Clientes y Proveedores')` | Al abrir un rol se muestra el PRIMER módulo con algo concedido (Vendedor → Clientes y Proveedores). Los recursos de otro módulo no están en el DOM hasta pulsar el módulo |
| Filtros de estado | `[aria-label='Filtrar por estado'] button:has-text('Todos'|'Concedidos'|'Heredados'|'Sin conceder')` | |
| Buscar permiso | `.rpe__search input` | «factur» → «Resultados de «factur»» / «156 permisos en todo el catálogo»; con «ver» sale `.rpe :text('Se muestran los primeros 60')` |
| Recurso | `.rpe__resource:has(.rpe__resource-name:text-is('Cotizaciones'))` (tras pulsar el módulo) · `…'Productos'` · `…'Socios'` · `…'Facturas'` (en búsqueda) | «Clientes» NO es un recurso: en «Clientes y Proveedores» el recurso es **«Socios»** |
| Acción | `<recurso> .rpe__act:text-is('Ver')` ✔ o `get_by_role('button', name='Ver', exact=True)` dentro del recurso | Clases de estado `rpe__act--direct|--inherited|--excluded|--none` (+`--changed`). Tooltip 400 ms: «Sin conceder · PARTNER_CREATE», «Heredado del rol padre · PARTNER_CREATE», «Concedido · PRODUCT_DELETE» |
| Alcance | `.rpe__scope-seg[aria-label='Alcance de Ver en Cotizaciones'] button:has-text('Equipo')` ✔ | Solo existe en la acción «Ver» concedida |
| Barra de guardado | `.gm-sheet-savebar` ✔, `… button:has-text('Guardar cambios')` ✔, `… button:has-text('Descartar')` | «1 cambio sin guardar · afectan a 2 personas». Fija abajo: **tapa el segmentado de alcance del último recurso** y el FAB tapa el borde derecho de «Guardar cambios» (clic en el centro funciona) |
| Cambios sin guardar | `mat-dialog-container button:has-text('Seguir editando'|'Descartar cambios')` | «Cambios sin guardar / Hay 2 cambios de permisos sin guardar. Si continúas, se descartan.» |
| Titulares | `app-role-holders` (filas `app-role-holders .rh__row`, 1 cabecera + n) | Vendedor: José «Hace 30 min», Ana, Héctor «Nunca»; Mensajero muestra a Sonia (inactiva) |
| Historial | `app-role-history` | «Cambió permisos · rosa.almanzar · Hace 38 min · Cotizaciones · Cotizaciones — → Ver (Propios), Crear, Editar …». El alta sale como «Creó» con campos crudos `id/name/active/canEdit` (D-S7): no mostrarla |

**Nombres reales del editor (P-13):** Cotizaciones: Ver · Crear · Editar · Eliminar · Aprobar · Rechazar · «Convertir Cotización a Orden» · «Convertir Cotización a Factura Directamente» · «Aceptar Cotización» · «Liquidar Cotización». Productos (módulo «Productos», sección «Compras e inventario»): Ver · Crear · Editar · Eliminar · Importar · Exportar. «Clientes · Crear» = módulo «Clientes y Proveedores» › recurso «Socios» › «Crear» (`PARTNER_CREATE`). `INVENTORY_VIEW` = módulo «Inventario».

### Diálogos de rol
| Diálogo | Selectores ✔ | Textos |
|---|---|---|
| Duplicar (antes «Clonar») | `[formcontrolname='name']`, `[formcontrolname='description']`, `button:has-text('Duplicar')`, `button:has-text('Cancelar')` (todos bajo `mat-dialog-container`) | Título «**Duplicar rol**»; «Se creará un nuevo rol copiando los permisos, la herencia y las exclusiones de Contador.»; éxito «Operación completada / El rol ha sido duplicado correctamente con sus permisos, herencia y exclusiones.» [Aceptar] |
| Crear | `name`, `description`, `mat-dialog-container mat-slide-toggle`, `[formcontrolname='parentRole']`, `button:has-text('Crear')` | «Crear Rol»; interruptor «Heredar permisos de otro rol»; opciones del padre: roles de la empresa + «Empleado Sistema», «Admin Sistema»…; aviso «Este rol heredará automáticamente los permisos de Vendedor y se mantendrá sincronizado con sus cambios. Podrás excluir permisos individuales desde el detalle del rol.»; nombre repetido → diálogo «Error / Ya existe un rol con este nombre en la empresa» [Entendido]; cancelar con cambios → «Guardar Cambios / ¿Estás seguro que deseas salir sin guardar los cambios?» [Cancelar · Sí, salir] |
| Eliminar | `button:has-text('Eliminar')` | «Eliminar rol / ¿Está seguro de que desea eliminar el rol "Vendedor en práctica"? Esta acción no se puede deshacer.» → toast «Rol eliminado exitosamente». Con titulares: toast 422 «Este rol está asignado a 2 personas. Quítaselo antes de eliminarlo.»; con hijos: «No se puede eliminar el rol porque otros roles heredan de él: Vendedor sénior» |

---

## 3. Personas (04a, 04b, 04c, 05) — `/security/personas`

| Qué | Selector ✔ | Texto |
|---|---|---|
| Vistas | `.gm-rail-btn:has(:text-is('Todas'|'Activas'|'Sin rol'|'Nunca entraron'|'Inactivas'))` | Conteos 9 · 8 · 1 · 1 · 1. URL `?vista=activas|sin-rol|nunca|inactivas` |
| Equipos | `.gm-rail-btn:has(:text-is('Zona Este'))` (→ `?equipo=1`), `button[aria-label='Nuevo equipo']` | |
| Buscar / Rol | `input[aria-label='Buscar persona']` · `button:has-text('Rol'):has(mat-icon:text-is('filter_list'))` → `.mat-mdc-menu-panel button:has-text('Almacén')` | Menú: «Todos los roles», Mensajero, Auditor (solo lectura), Almacén, Vendedor sénior, Vendedor, Empleado, … Admin. Vacío: «No se encontraron resultados para los filtros seleccionados» |
| Filas | `.sec-people__row:has-text('Ana Mejía')`, nombre `.sec-people__who:has-text('Ana Mejía')`, casilla `input[aria-label='Seleccionar Carlos Pimentel']` | Orden E0: Sonia, Luisa, Marta, Pedro, Carlos, José, Ana, Héctor, Rosa… «Mostrando 1–9 de 9» (`.sec-people :text('Mostrando')`) |
| Panel | `aside[aria-label='Detalle de la persona']`; `button[aria-label='Cerrar panel']`; `.sec-people__buttons button:has-text('Editar'|'Cambiar contraseña')`; `.sec-people__buttons button[aria-label='Más acciones']`; `.sec-people__role`; `.sec-people__assign-roles`; `aside[aria-label='Detalle de la persona'] button:has-text('Ver los')` | Ana: «Activa · Zona Este · Último ingreso: hace …», «Vendedor · De la empresa», «PERMISOS EFECTIVOS 5 / 1160 · La unión de sus roles, por módulo contratado.» Productos 1/42 · Clientes y Proveedores 1/37 · Cotizaciones 3/19 · «Ver los 34 módulos»; «ÚLTIMOS INGRESOS … · **Cliente de API** · ::1» (D-S13). Más acciones: Desactivar · Ver su actividad · Eliminar |
| Propio | `.sec-people__hint:has-text('No puedes cambiar')` | «No puedes cambiar tus propios roles: pide a otro administrador que lo haga.» (`.sec-people__hint` a secas casa 2) |
| Masivas | `.sec-people__bulk`, `… button:has-text('Agregar a equipo'|'Quitar del equipo'|'Limpiar')` | Toasts «Personas agregadas a «Zona Norte» exitosamente», «Persona quitada de «Zona Norte» exitosamente» (0,3 s) |
| Equipo abierto | `button:has-text('Editar equipo')`, `button[aria-label='Eliminar equipo']` | «Eliminar equipo / ¿Está seguro de que desea eliminar el equipo "Zona Norte"? …» → «Equipo eliminado exitosamente», vuelve a `/security/personas` |

Acceso efectivo (05): Carlos «Vendedor sénior · Hereda de Vendedor» 11/1160 · José «Almacén + Vendedor» 10/1160 · Luisa «Sin ningún rol: inicia sesión pero no ve ningún módulo.» 0/1160 «Ningún permiso concedido.» · Héctor «Pendiente · Último ingreso: nunca» · Sonia «Inactiva», Mensajero, 0/1160.

### Diálogos de persona
| Diálogo | Selectores ✔ (bajo `mat-dialog-container`) | Textos / tiempos |
|---|---|---|
| Asignar roles | `app-role-multi-select mat-select` → `.rms-panel input` + `.rms-panel mat-option:has-text('Almacén')` (cerrar con Escape); chip `button[aria-label='Eliminar Vendedor']`; `.person-roles__line--add` / `--remove`; `button:has-text('Guardar')` | Título «Asignar roles», subtítulo el nombre, campo «Roles en esta empresa», hint «Lo que puede hacer es la unión de los permisos de todos sus roles.», «1 rol(es) asignado(s)», «Limpiar todo». Diff «Se agrega: Almacén» / «Se quita: Vendedor». Sin roles: «Debe conservar al menos un rol: …». Toast «Roles actualizados exitosamente» (0,45 s) |
| Crear Usuario | `[formcontrolname='name'|'lastName'|'email'|'username'|'whatsappPhone'|'password'|'confirmPassword']`, `app-role-multi-select mat-select`, radios `mat-radio-button` (nth 0 = Activo), `button:has-text('Guardar')` | El cuerpo **hace scroll** (632/514 px): «Estado» queda bajo el pliegue. «Operación completada / El usuario ha sido creado correctamente.» tras **7,7–8,2 s** con botones deshabilitados. Correo existente: «Este correo ya está registrado. Se vinculará…»; eliminado: «Este correo pertenece a un usuario eliminado. Se restaurará…». «Verificando correo...» no se llegó a ver (dura < 300 ms) |
| Editar / Cambiar contraseña | casilla `mat-checkbox:has-text('Cambiar la contraseña')`, `[formcontrolname='password']`, `button:has-text('Actualizar')` | En edición hay **una sola** contraseña (sin confirmar). Roles en edición: hint «Agregue o quite roles. Debe conservar al menos uno.». Éxito en 3,6 s |
| Desactivar / Eliminar | `.mat-mdc-menu-panel button:has-text('Desactivar'|'Activar'|'Eliminar')` → `button:has-text('Desactivar'|'Eliminar')` | «Desactivar usuario / ¿Desactivar a "Julio Santana"? No podrá iniciar sesión hasta que se active de nuevo.» → «Usuario desactivado exitosamente» (3,4 s); «Usuario activado exitosamente» (3,3 s, sin confirmación); «Eliminar usuario / ¿Está seguro … Esta acción no se puede deshacer.» → «Usuario eliminado exitosamente» (6,3 s) |
| Nuevo/Editar Equipo | `[formcontrolname='name'|'description']`, `button:has-text('Guardar'|'Actualizar')` | «Operación completada / El equipo ha sido creado|actualizado correctamente.» |

---

## 4. Integraciones (06a, 06b, 06c) — `/security/integraciones`

| Qué | Selector ✔ | Texto |
|---|---|---|
| Barra | `button:has-text('Documentación de la API')`, `button:has-text('Nueva credencial')` | «Credenciales de API» |
| Fila | `.sec-api__row:has-text('Tienda en línea anterior')` | «Creada el Sáb, 30 may · Sincronizaba pedidos de la tienda web (ya no se usa)» · `gv_live_0e9d2d31` · «Jue, 9 jul, 10:10» · «Sin uso». Pie: «Cada credencial tiene sus propios permisos: cambiar los de una no toca los de otra.» / «Rotar un secreto invalida el anterior de inmediato.» |
| Nueva integración | `[formcontrolname='integrationName'|'integrationDescription']`, `input[placeholder='192.168.1.1']`, `button:has-text('Generar credenciales')` | Ver texto completo en `_resultados-v06a.json` (`dlg_nueva`) |
| Franja del secreto | `.sec-api__secret`, `… button:has-text('Mostrar'|'Copiar secreto'|'API Key')`, `… button[aria-label='Cerrar aviso']` | Aparece **≈3,5 s** después de «Generar credenciales» (esperar el selector). «Credencial «Programa del contador» lista. / Copia el secreto ahora: no se vuelve a mostrar.» Toast «Secreto copiado» (con permiso de portapapeles en el contexto) |
| Panel | `.sec-api__permissions` («Editar permisos» / «Ver permisos»), `.sec-api__buttons button:has-text('Rotar secreto')`, `.sec-api__buttons button[aria-label='Más acciones']`, `button[aria-label='Cerrar panel']` | «Activa · 0 llamadas en total · Sin restricción de IP», «PERMISOS 5 / Usa los permisos de la plantilla…», Facturación 3/79 «Facturas: Ver, Crear · Facturas de Compra: Crear», Facturación Electrónica 2/44, Compras 1/38, «OPERACIONES EN 7 DÍAS 0». Más acciones: «Desactivar/Activar», «Revocar y eliminar» |
| Rotar / Desactivar / Revocar | `mat-dialog-container button:has-text('Rotar secreto'|'Eliminar')` | «Rotar secreto / ¿Rotar el secreto de "Programa del contador"? El actual deja de funcionar de inmediato…» → vuelve la franja (3,5 s). «Integración desactivada|activada exitosamente» (3,4 s). «Revocar credencial / ¿Está seguro de que desea eliminar la integración "Tienda en línea anterior"? …» → «Integración eliminada exitosamente» (3,4 s) |
| Página de permisos | `input[placeholder='Nombre o código...']`, `mat-checkbox:has-text('PURCHASE_INVOICE_CREATE') input`, `button:has-text('Volver a Integraciones')` | Casilla «Registrar Facturas de Compra / PURCHASE_INVOICE_CREATE» (hay 2 casillas con ese código: se listan en Facturación y en Compras). Guarda al instante: toast «Permiso quitado exitosamente» / «Permiso concedido exitosamente» (≈1,9 s). «Volver…» está al pie, **y≈12 800 px** |
| Documentación | `/security/api-docs` → `/security/api-docs/referencia-endpoints` | Menú: Referencia de Endpoints · Códigos y Respuestas · Registro de Cambios · POST Login · … · GET Estado de Suscripción (títulos internos sin acento, D-S10) |

---

## 5. Auditoría (07) — `/security/auditoria`

| Qué | Selector ✔ | Texto |
|---|---|---|
| Período | `button:has(mat-icon:text-is('calendar_today'))` → `.mat-mdc-menu-panel :text('Últimos 30 días')` | Hoy · Últimos 7 días · Últimos 30 días · Este mes · Todo el historial |
| Persona / Registro / IP | `input[aria-label='Filtrar por persona'|'Filtrar por registro'|'Filtrar por IP']` | **No recargan la lista al escribir (D-S5)**. En el guion llegar ya filtrado con `navegar` (SPA): `/security/auditoria?persona=ana.mejia&registro=auth` → «5 eventos» ✔ |
| Acción | `button:has(mat-icon:text-is('filter_list'))` → `.mat-mdc-menu-panel :text-is('Creó')` | El menú **no se cierra** al marcar (Escape). Botón pasa a «Acción: Creó, Cambió estado» |
| Limpiar | `button:has-text('Limpiar')` | |
| Filas / total | `.sec-audit__row:has-text('Cambió permisos')` | «677 eventos» (E0 + la toma); grupo «Hoy · domingo, 27 de septiembre»; HORA · QUIÉN · ACCIÓN · REGISTRO · IP |
| Detalle | `aside[aria-label='Detalle del evento']`, `button[aria-label='Cerrar detalle']`, `.sec-audit__change`, `.sec-audit__link:has-text('Historial del registro')`, `.sec-audit__link:has-text('Ver a')` | «Cambió permisos / Domingo, 27 de septiembre de 2026, 11:10 / Roles #79 / por rosa.almanzar / QUÉ CAMBIÓ / Productos · Productos / Ver, Crear, Editar, Importar → Ver, Crear, Editar, Importar, Exportar / SOLICITUD IP ::1 · Origen Cliente de API · Evento PERMISSIONS_CHANGED». Historial → `?registro=roles&registroId=79&periodo=todo` (3 eventos). «Ver a rosa.almanzar →» → `/security/personas?q=rosa.almanzar` |
| Más | `button:has-text('Cargar eventos anteriores')` | 50 por página, al pie |

---

## 6. Otros módulos (08a–08g)

| Pantalla | Selectores ✔ | Por usuario |
|---|---|---|
| `/sales/quotes` | `button:has-text('Crear Cotización')`; fila `tr:has-text('Colmado La Esquina')`; `tr:has-text('…') button:has(mat-icon:text-is('more_vert'))` | Columnas N° · Cliente · Estado · Emisión · Vencimiento · Subtotal · ITBIS · Descuento · Total · Acciones (**sin columna de creador ni vendedor**, tampoco en «Configurar Columnas»). Pie `.mat-mdc-paginator-range-label`: Carlos/Marta «1 – 8 de 8», Ana «1 – 3 de 3», Ana con Equipo «1 – 5 de 5». Ana: «Más acciones» de la fila = «Duplicar»; Marta: sin «Crear Cotización» ni «Duplicar» |
| `/sales/quotes/:n` | pasos `.step-content:has-text('Aprobada'|'Cancelada')` ✔; `button[aria-label='Más acciones']` ✔ → `.mat-mdc-menu-panel button:has-text('Convertir a factura')` ✔ | **Al abrir sale el modal «Acceso Denegado — "Configuración Empresa"» (D-S1)**. Ana: título «Editar Cotización 2 · Borrador», Guardar; «Aprobada» `cursor:not-allowed`, clic sin efecto ni aviso; «Cancelada» `pointer`. Marta: «Cotización 2 · Borrador», sin Guardar, 0 campos editables, todos los pasos `not-allowed`. Carlos Q1: «Aprobada» → «Aprobar cotización / ¿Está seguro de que desea aprobar la cotización "1"? Dejará de ser editable.» [Cancelar · Aprobar] → «Éxito / Estado actualizado correctamente» [Aceptar]. Q6 (Aprobada): Convertir a factura · Versiones e historial · Duplicar. Q7 (Borrador): Versiones e historial · Duplicar (**desaparece**) |
| `/inventory/product/list` | `button:has-text('Nuevo Producto'|'Alta por foto'|'Importar / Exportar')`; fila `tr:has-text('Machete de 22')`; acciones en línea `tr:has-text('Machete de 22') button[aria-label='Abrir'|'Duplicar'|'Desactivar'|'Eliminar']` | **No hay ⋮ en la fila**: son iconos. Rosa: Abrir, Duplicar, Desactivar, Eliminar. Pedro: Abrir, Duplicar, Desactivar. Ana: Abrir (sin Nuevo ni Importar/Exportar). **Pedro y Ana: modal «Acceso Denegado — "Impuestos"» y fotos rotas (D-S2)**. «Importar / Exportar» abre un DIÁLOGO «Importar / Exportar productos» con pestañas `mat-dialog-container :text-is('Importar'|'Exportar')`; en Exportar: «Exportar Excel» / «Exportar CSV» → descarga `productos_export.xlsx` en 0,15 s, sin diálogo nativo |
| `/sales/partners` | `button:has-text('Nuevo Cliente')` | Aparece para Carlos solo con `PARTNER_CREATE` (heredado de Vendedor) y desaparece al excluirlo en Sénior |
| `/profile` | `[formcontrolname='password'|'new_password'|'confirm_new_password']`, `button:has-text('Actualizar contraseña')`, `button[aria-label='Desplegar']`, `button:has-text('Guardar Cambios'|'Restablecer Todo')`, toggle `app-menu-visibility-config .menu-node.level-0:has(> .node-row .node-title:text-is('Compras')) > .node-row mat-slide-toggle` ✔ | Tarjeta «Seguridad / Cambie su contraseña de acceso» al pie (y≈880). «Cambios Guardados / La configuración de visibilidad del menú se ha guardado correctamente.» (0,25 s) → Compras sale del riel sin recargar. «¿Restablecer Todo? / Se mostrarán todos los menús ocultos. ¿Desea continuar?» [Cancelar · Sí, restablecer] → «Menús Restablecidos / Todos los menús han sido restablecidos y son visibles nuevamente.». 3 candados «no se puede ocultar». También sale «Mi Firma Digital … formularios clínicos» |

Rutas viejas: `/security/settings` y `/security/menu-visibility` → `/profile` (sin aviso); `/my-company/perfil-consultorio` → `/home` sin aviso;
`/security/role/77` → `/security/roles?rol=77` (D-12 corregido).

---

## 7. Trampas y tiempos

1. **Modales «Acceso Denegado» en pantallas con permiso (D-S1, D-S2, D-S3):** cotizaciones, productos y la página de permisos de la credencial los abren al cargar para roles no admin. Mientras no se corrija, el guion no puede grabar 08b/08c/08e/08g limpio (o el sembrado da `COMPANY_CONFIG_VIEW`, `TAX_VIEW`, `MEDIA_VIEW`, `MODULE_VIEW` a los roles demo y la voz no lo menciona).
2. **Toast vs diálogo:** guards de ruta, acciones de consola y roles → toast (0,3–0,5 s tras el clic). Altas/ediciones de usuario, rol y equipo, aprobar cotización, visibilidad del menú → diálogo con «Aceptar». 403 con la palabra «permiso» → diálogo «Acceso Denegado» [Entendido]. 403 de alcance (sin «permiso») → nada (D-S4).
3. **Tiempos:** login 6–8 s; alta de usuario 8 s; desactivar/activar/eliminar usuario 3–6 s; credencial generar/rotar/pausar/revocar ≈3,5 s; permisos de rol y equipos 0,3–0,45 s; casilla de credencial ≈1,9 s; exportar 0,15 s.
4. **Fuera del pliegue a 1280×720:** «Seguridad» del riel de Rosa (y=716); la fila «Roles #79» del Resumen (y=790, scroll interno); el asunto «rol sin permisos» (y=750); «Estado» en Crear Usuario; tarjeta «Seguridad» de Mi perfil (y≈880); «Volver a Integraciones» (y≈12 800); casillas de Carlos (y=605) y Héctor (y=829) en Personas.
5. **Sticky/fijos:** topbar 60 px y riel 60 px fijos; `.gm-sheet-savebar` fija al pie del editor (tapa el último recurso); `.chatbot-fab` en [1200,640,56,56].
6. **Actividad reciente E0 (D-S13):** siete «Acceso» sembrados + el de la toma encima del cambio de permisos; los «Hace N min» cambian a «Hoy HH:MM» con el tiempo. Los ingresos sembrados dicen «Cliente de API».
7. **Cambio de usuario:** cada login revoca la sesión previa del mismo usuario; `tweak`/`dev/login` de Rosa revoca su sesión de UI.
8. **Subcadenas:** ver la nota del encabezado (Activas/Inactivas, Vendedor/sénior, Clientes/Segmentos de Clientes, Aprobada).

---

## 8. Respuestas a las «Preguntas abiertas» de `_SERIE-SEGURIDAD.md` §11

1. **Restaurar la bitácora:** sí. `restaurar.mjs E0` borra por `company_id` + marca de agua (0,8–0,9 s, «23 tablas, conteos iguales al canon»); se usó ≈30 veces hoy sin fallo. Pero el canon ya trae 7 ingresos por encima del cambio sembrado (ver trampa 6): en 01-03 hay que desplazar el panel y buscar «Actualizó · Roles #79», o re-sembrar el cambio de permisos DESPUÉS de los ingresos.
2. **Menú tras un cambio de permisos:** la sesión abierta NO cambia el menú. Al pulsar la entrada vieja abre la pantalla y sale «Acceso Denegado — "Productos"». Con **F5** el riel ya se actualiza (desaparece Inventario), pero si se estaba en esa ruta sale otra vez el modal (D-S9). Volviendo a entrar: riel sin Inventario y la URL da el toast «No tienes permiso para ver «Productos»…». La voz «al volver a entrar ya no lo ve» es cierta. El **alcance** (08d) se aplica en la siguiente petición: Ana ve 5 con solo recargar.
3. **D-01:** corregido (ver A1): «+ Asignar rol» abre «Asignar roles» y «Editar» trae el selector. 04b-03 se puede grabar.
4. **Login en cámara:** sin reCAPTCHA; `button.auth-primary-btn`; aterriza en `/home`; sin «Configuración incompleta» ni aviso TRIAL; 6–8 s del clic a la pantalla cargada (+1 s la página de acceso).
5. **Motor y otro origen:** no. `_navegar` hace `base + ruta` (`grabar.py:1007`): una URL absoluta queda `http://localhost:4200http://…`. Servir la lámina bajo el mismo origen (ruta del servidor estático) o añadir soporte de URL absoluta; al volver con `navegar` relativo desde otro origen hace `goto` completo y la sesión se conserva (está en el almacenamiento del origen :4200).
6. **Stepper:** «Aprobada» se VE para Ana (no desaparece), `cursor: not-allowed`, el clic no hace nada ni avisa. «Cancelada» se llama así y está disponible para Ana. Marta: formulario de solo lectura (sin Guardar, 0 campos editables, pasos bloqueados). Todo detrás del modal de D-S1.
7. **«Convertir a factura»:** en Q7 (Borrador) **desaparece** del menú; en Q6 (Aprobada) aparece para Carlos. No se probó sin `INVOICE_CREATE`.
8. **Cifras del Resumen:** sí a las tres: Héctor en NEVER_LOGGED_IN («Revisar →» abre su panel), Mensajero cuenta como rol sin permisos aunque Sonia esté inactiva, la credencial retrocedida sale «sin uso». Cifras: 9 · 1 · 1 · 1 («1 sin uso en 60 días») · 649/73.
9. **Luisa sin rol:** existe en E0 (0/1160). Por la UI no se puede dejar a alguien sin rol: «Asignar roles» exige al menos uno («Debe conservar al menos un rol…»).
10. **Alcance tras el cambio:** Ana ve **5** tras el cambio a «Equipo» con solo recargar (no hace falta volver a entrar). La lista **no tiene columna de creador ni de vendedor** (ni en «Configurar Columnas»): se enseña con el pie «1 – 8 de 8 / 1 – 3 de 3 / 1 – 5 de 5» y los clientes.
11. **Barra de guardado:** cuenta SOLO titulares directos. Vendedor → «afectan a 3 personas» (Ana, José, Héctor; Carlos por herencia NO cuenta); Sénior → «1 persona»; Almacén → «2 personas».
12. **`/my-company` para Pedro:** toast «No tienes permiso para ver «Mi Empresa». Solicita el acceso al administrador de tu empresa.». OJO: ahora `/sales/quotes` también avisa («…«Cotizaciones»…»), así que el contraste «sin aviso / con aviso» de 08a-03 ya no existe: el paso debe decir que en ambos casos vuelve al inicio con aviso.
13. **Etiquetas:** ver §2 «Nombres reales del editor». Clientes · Crear = «Clientes y Proveedores › Socios › Crear» (`PARTNER_CREATE`).
14. **Exportar productos:** «Importar / Exportar» abre un diálogo con pestañas; «Exportar Excel» descarga al instante (`productos_export.xlsx`), sin diálogo nativo en Playwright. En la grabación basta con señalar el botón o pulsarlo (no tapa la toma).

## 9. Diferencias con el plan que obligan a reescribir pasos

- 02a-03: el diálogo ya es «**Duplicar rol**» / botón «Duplicar» / «…duplicado correctamente…»: la aclaración «duplicar y clonar son lo mismo» sobra.
- 00-03 / 01: el buscador dice «Buscar persona o rol»; el asunto «nunca inició sesión» dice «Comprueba su correo o desactiva la cuenta si ya no la usa.» y su CTA es «Revisar →».
- 01-03: la fila es «Actualizó · Roles #79» (no «Cambió permisos») y está bajo el pliegue.
- 02b-02 / 08f: «Clientes · Ver/Crear» → recurso «**Socios**» del módulo «Clientes y Proveedores». «Cobros» no es un módulo del riel (hay «Venta a Crédito», «Facturación»…).
- 04b-02: el diálogo de edición tiene una sola contraseña.
- 07-02: escribir en Persona/Registro/IP no filtra hasta recargar (D-S5).
- 07-03: el detalle dice «Productos · Productos» y «por rosa.almanzar» (no «Rosa Almánzar»).
- 08a-03: las dos URL avisan con toast.
- 08c-03/04: no hay ⋮: las acciones son iconos en la fila (`button[aria-label='Eliminar']`).
- 08b, 08c, 08e, 08g: bloqueados por D-S1/D-S2 hasta corregir o ampliar los roles demo.
