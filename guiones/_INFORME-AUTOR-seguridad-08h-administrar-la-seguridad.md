# Informe del AUTOR D · cobertura 100 % de la serie «Seguridad» (2026-09-27)

Sin apps, sin navegador, sin git. Fuentes: skill `germiva-video`, `GRABACION.md` («Insignia, cartel y diagrama»),
`_CONVENCIONES`, `_SERIE`, `_SELECTORES`, `_INVENTARIO-SEGURIDAD-FE/API`, `_REVISION-SEMANTICA`,
`HALLAZGOS-SEGURIDAD-VIDEO.md`, los volcados de `exploracion-seguridad/`, el canon `seeds/seguridad/estados/E0.sql`
y el código de las ramas `fix/security-video-findings` (front y API), que solo se leyó.

## Resultado

| Guion | Qué cubre | `revisar.mjs` | `tut verificar` | Duración prevista |
|---|---|---|---|---|
| **seguridad-08h-administrar-la-seguridad** (nuevo) | F-226, F-228, F-229, F-230, F-231, F-238, F-239, F-240 (+ F-227) | 0 ERROR · 1 AVISO | 0 · 0 | 3:55.6 |
| seguridad-04c-equipos | F-052 (paso nuevo `05-sin-equipos`) | 0 ERROR · 1 AVISO | 0 · 0 | 3:19.3 (antes 2:50) |
| seguridad-02a-roles | F-157 (en `02-rol-del-sistema`) | 0 ERROR · 1 AVISO | 0 · 0 | 3:17.5 (antes 3:06) |
| seguridad-09-lo-que-se-movio | F-007 (paso nuevo `03b-historial-viejo`) | 0 ERROR · 1 AVISO | 0 · 0 | 2:46.7 (antes 2:22) |
| seguridad-07-auditoria | A-059 (en `03-detalle-del-evento`) | 0 ERROR · 1 AVISO | 0 · 0 | 4:01.2 (antes 3:49; límite 4:10) |

El único AVISO de cada guion es el de siempre: el primer paso no contrae el panel del menú, que no existe en
`/security/*` ni en `/home`. `seguridad-03-herencia` no se tocó: está en 3:59,5 y F-157 no cabía.
`_COBERTURA-SEGURIDAD.md`: se cambiaron las 12 filas y el resumen. Ahora queda **SIN CUBRIR 0**; lo visible
queda Front 93,7 %, API 82,0 % y el conjunto 91,4 %.

## 08h · «Con y sin permiso · Quién puede administrar la seguridad»

El guion arranca en **E0** y entra `rosa.almanzar`. Marta entra una sola vez, en el paso 05.

| Paso | Insignia | Qué se ve |
|---|---|---|
| 01-con-personas | con · Rosa | En el panel de Ana: Editar, Cambiar contraseña, «+ Asignar rol» y el menú ⋮ con Desactivar · Ver su actividad · Eliminar. El menú se cierra con Escape |
| 02-con-equipos | con · Rosa | Zona Este: «+» Nuevo equipo, «Editar equipo» y la papelera. Con la casilla de Ana aparece la barra con Agregar/Quitar, y se cierra con Limpiar |
| 03-con-credenciales | con · Rosa | Nueva credencial. En «Tienda en línea anterior»: Editar permisos, Rotar secreto y el ⋮ con Desactivar · Revocar y eliminar |
| 04-dar-solo-ver | info · Rosa | En Roles › Auditor › Acceso API «0 de 4» se concede **solo «Ver»** y se guarda por lote (toast) |
| 05-sin-personas | sin · Marta | Cambio de usuario en cámara. La consola no tiene «Nuevo». En el MISMO panel de Ana no hay Editar, ni contraseña, ni «+ Asignar rol», y el ⋮ solo trae «Ver su actividad» |
| 06-sin-equipos | sin · Marta | Ve Zona Este y sus miembros. No hay «+», ni «Editar equipo», ni papelera. La barra de selección solo trae «Limpiar» |
| 07-sin-credenciales | sin · Marta | Aparece la pestaña Integraciones, pero sin «Nueva credencial». El botón dice **«Ver permisos»**. No hay Rotar ni ⋮. Cartel **consejo de mínimo privilegio** y resumen |

**Decisión sobre Integraciones:** en E0 Marta no tiene la pestaña. En 04 la voz lo dice («ni siquiera ve la
pestaña Integraciones; esa ausencia ya es una diferencia») con la marca «Acceso API 0/4». Para el contraste de
ACCIÓN, Rosa concede SOLO `INTEGRATION_USER_VIEW` al rol Auditor ANTES de que Marta entre. Así hay un solo
cambio de usuario y Marta no tiene que volver a entrar. **Qué escribe la toma:** `role_permissions` del
Auditor (80) + `audit_logs` PERMISSIONS_CHANGED roles/80 + los accesos. No crea, edita ni borra personas,
equipos ni credenciales. **Hay que correr `restaurar.mjs E0` después.**

**Verificado:**
- En volcados:
  - `v08a-09`: Marta sin Editar ni «+ Asignar rol», con ⋮ y con Zona Este, sin «Nuevo equipo».
  - `v08a-07`: Marta sin «Nuevo».
  - `a5-06` frente a `a5-01`: Marta con INTEGRATION_USER_VIEW tiene «Ver permisos» y no tiene Rotar, ⋮ ni «Nueva credencial».
- En el código del front:
  - `hasPersonMenu = USER_EDIT || USER_DELETE || AUDIT_LOG_READ`, así que el ⋮ de Marta solo trae «Ver su actividad».
  - `canEditTeam`, `canDeleteTeam`, `canManageMembers && teams().length`.
  - `canCreate`, `canEdit` y `canDelete` de Integraciones.

**A confirmar en el ensayo.** Todo va anotado en el `_comentario`, y la voz no lee lo no comprobado:
1. El nombre del recurso de «Acceso API» en el editor. El parser del API da «Usuarios de Integración». El
   selector usa `:has-text('Integración')` y la voz no lo nombra.
2. Que el Auditor muestre «0/4» en Acceso API. La voz dice «cero de cuatro».
3. La barra de guardado dice «afecta a una persona». El Auditor tiene 1 titular.
4. La cabecera de equipo y la barra «solo Limpiar» de Marta. Están verificadas en el código, no en un volcado.

**No se pulsa «Ver permisos» con Marta:** esa página falla hoy (D-S3, modal «Ver Módulos») y no deshabilita
las casillas (D-05).

F-226 (TEAM_VIEW): el lado «con» se ve en pantalla. El lado «sin» solo va en voz («a quien no lo tiene, los
equipos ni le aparecen»). Está verificado en el código (`html:19`), y ningún usuario demo tiene USER_VIEW sin
TEAM_VIEW (D-04).

## Los otros cuatro

- **F-052 · 04c/05-sin-equipos.** Tras borrar Zona Norte, el guion abre Zona Este, la elimina y enseña
  «Sin equipos todavía.» (`.sec-people__none`). Es el ÚLTIMO paso, así que no rompe nada posterior. El caso
  práctico del alcance Equipo se movió de 04 a 05. Restaurar E0 devuelve Zona Este con Ana y José.
- **F-157 · 02a/02.** Se abre el Historial de **Contador**, un rol del sistema, y sale «No se encontraron
  registros». Después se vuelve a Permisos antes de Duplicar. Por qué está vacío: el historial se filtra por
  la empresa (`audit-log.service.ts:105-120`) y E0 solo tiene eventos de los roles 77–81. **Mensajero no
  servía:** tiene 1 evento «Creó».
- **F-007 · 09/03b-historial-viejo.** El guion navega a `/security/audit/entity-name/roles/entity-id/79` y
  llega a la Auditoría filtrada por el registro de Almacén, con el período «todo». Salen **3 eventos**: Creó
  más dos «Cambió permisos», confirmados en E0.sql. El paso 04 sale ahora desde Auditoría, no desde /home.
  Sigue sin estar en /profile, así que la redirección de /security/settings se ve igual.
- **A-059 · 07/03.** Antes de abrir el «Cambió permisos», se marca la celda Registro de la fila de justo
  debajo, «Creó · … #11034»: `role_permissions`, auditado LIGHT, misma hora. Ese evento SÍ está en E0 (id
  11034 en el canon). La etiqueta está en corrección: el build muestra «Permisos por rol», el front actual
  «Permisos del rol» y el API «Permiso de rol». Por eso la voz dice «una fila Creó sobre un permiso de ese
  rol» y no la lee. No aparece «Rol asignado» (`user_company_roles`) cerca en E0, así que no se usó.
