# Ensayo · serie «Seguridad» · tanda 1 (OPERADOR-ENSAYO, 2026-09-27)

Guiones: 00, 01, 02a, 02b, 03 y 09. Apps: API `dist` en :3001 y front estático en :4200 (no se reiniciaron). Un
solo navegador headless 1280×720 (dsf 1.5). Todo corrió bajo `seeds/_puertas/NAVEGADOR.lock` («ENSAYANDO <guion>
<pid>»), tomado con `wx` desde el proceso vivo que lanzaba el ensayo y borrado solo cuando seguía siendo suyo. Antes
y después de cada ensayo y de cada sonda se restauró el estado (E0, o E2a en 02b). Al terminar quedó **E0**.
Capturas en `germiva/qa-seguridad-ensayos-2026-09-27/<guion>/`. Los logs llevan líneas `──` de paso (R28).

## Resultado

| Guion | Estado | Pasos | Acciones | Fallos 1.ª pasada → final | revisar | verificar | Duración estimada |
|---|---|---|---|---|---|---|---|
| 00-introduccion | E0 | 4 | 40 | 7 (herramienta) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:05 + 6 s ≈ **3:11** |
| 01-resumen | E0 | 4 | 38 | 1 → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:17 + 6 s ≈ **3:24** |
| 02a-roles | E0 → E2a | 4 | 44 | **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:17 + 6 s ≈ **3:23** |
| 02b-editor-permisos | E2a | 5 | 48 | 0 (1 afirmación falsa en la voz) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 3:51 + 6 s ≈ **3:57** |
| 03-herencia | E0 | 6 | 66 | 0 (1 afirmación falsa en la voz) → **0** | 0 ERROR · 1 AVISO | 0 · 0 | 4:00 + 6 s ≈ **4:06** (al borde de 4:10) |
| 09-lo-que-se-movio | E0 | 5 | 41 | **0** | 0 ERROR · 1 AVISO | 0 · 0 | 2:47 + 6 s ≈ **2:53** |

En los seis el AVISO es el mismo, ya justificado: el primer paso no pulsa `button.panel-collapse`, porque ese botón
no existe en /home, /security/* ni /profile.

## Fallos y correcciones

### Herramienta: `ensayar.py` no ejecutaba la capa (E-5)
En la primera pasada de 00 salieron 7 «acción desconocida», en `diagrama_fase` 2–6 y en dos `cartel`. Se amplió
`seeds/_puertas/ensayar.py` para que haga lo mismo que el motor (`g._insignia`, `g._cartel`, `g._abrir_diagrama`,
`g._fase_diagrama`, `g._cerrar_diagrama`). Además de ejecutarlos, comprueba en el shadow root `#__tut_ui`:

- que la insignia se ve y trae su texto;
- que el cartel se ve y trae su texto;
- que la lámina está abierta y que cada fase `data-fase=N` existe y se revela.

La lámina se cierra al acabar el paso, igual que en el motor. Con eso quedan confirmados en los seis guiones todas
las insignias, los 8 carteles y el diagrama `conceptos-seguridad` con sus fases 2–6. La captura
`00/02-seis-conceptos.png` muestra la lámina completa, con la tarjeta 04 «propios, equipo o todos».

### 01-resumen · paso 03 (1 FALLO)
`.sec-ov__row:has-text('Pedro')` no existe. Tras el re-canon r2, la Actividad reciente tiene esto:

- «Hace un momento · Acceso» (la toma);
- «Hace 3 h · Cambió permisos · Rol #79»;
- «Creó · Permiso de rol #11034», «Actualizó · Usuario #7951» y varios «Acceso».

Todo lo sembrado sale como «Hace 3 h» y no hay filas de Pedro. Cambios:

- La voz decía «hace un momento, hace unos minutos, y después la hora del día», pero `relativeTime()` da
  «Hace N min», «Hace N h», «Hoy/Ayer hh:mm» y día. Ahora dice «hace un momento, hace unos minutos o unas horas, y
  lo más viejo con el día y la hora». La marca va sobre `.sec-ov__row:has-text('Creó') .sec-ov__when`, con
  «unas horas».
- La marca de «etiqueta de color» estaba sobre la fila de Marta, que queda debajo del pliegue. Pasa a
  `.sec-ov__row:has-text('Creó') .gm-badge`.
- «Más abajo hay una fila Cambió permisos» pasa a «Justo debajo de mi entrada…», porque es la 2.ª fila.
- «los permisos del rol Almacén» pasa a «los permisos de un rol»: la pantalla dice «Rol #79», no «Almacén».
- D-S6 verificado: la fila dice «Cambió permisos · Rol #79», y el clic abre Auditoría con el evento y el panel
  «Detalle del evento».

### 02b-editor-permisos · paso 01 (afirmación falsa, E-1)
La voz decía «al abrir un rol el editor enseña el primer módulo donde ya concede algo». En la pantalla, en cambio,
el editor conserva el módulo que estaba abierto: `firstGrantedModule` solo actúa sin módulo previo, y la consola
abre antes Mensajero en General. La frase ahora es «al cambiar de rol, el editor se queda en el módulo que tenías
abierto».

### 03-herencia · paso 01 (afirmación falsa, E-1)
«El título del módulo lo confirma: uno de sus permisos viene heredado» sonaba mientras la pantalla decía «Módulo
General · 0 de 109 permisos · 0 heredados de Vendedor» (`03-senior-al-abrir.png`). Ahora la frase y su marca
(`.rpe__toolbar-title`) van después de «abro Cotizaciones», y la voz dice «siete permisos, y dos de ellos
heredados de Vendedor», que es lo que enseña el título («7 de 19 permisos · 2 heredados de Vendedor»).

## Puntos «a verificar» confirmados

- **00**: la primera fila «Acceso» de Auditoría es el ingreso de Rosa en la toma: «14:43 Rosa Almánzar · Acceso ·
  Sesión #7943», con 9 filas «Acceso». El candado del riel se centra y sale entero.
- **01**: la fila del cambio es la 2.ª (y≈501 de 720) y sale entera. No hay filas de marca bajo el FAB. «Nunca
  entraron · 1»: Héctor, Pendiente, con el panel «Último ingreso: nunca».
- **02a**:
  - Mensajero abre primero.
  - Historial de Contador: `app-role-history .gm-sheet-state` existe (el selector se sacó del código y aquí se
    confirmó).
  - «Duplicar rol» y «Operación completada» salen a ≤0,3 s (marca sin ancla, R10).
  - Contador externo queda abierto y editable. Cobrador sale con Vacío.
- **02b**:
  - Al borrar la búsqueda vuelve Clientes y Proveedores.
  - «Concedidos» enseña solo Socios (Ver · Propios) y Estado de Cuenta (Ver, PDF).
  - Facturación marca «1/79». La barra decía «4 cambios».
  - El clic en «Guardar cambios» funciona a pesar del FAB.
- **03**:
  - Crear queda «Excluido de la herencia».
  - Tras eliminar el rol se abre Mensajero.
  - La fila de Ana en «Personas del rol» lleva a su ficha.
  - El Historial de Vendedor abre con «Cambió permisos», que muestra Cotizaciones de «—» a «Ver (Propios), Crear,
    Editar».
- **09**:
  - Al salir de /profile con la contraseña escrita no sale ningún aviso.
  - El candado de «Inicio» se marca entero.
  - «Desplegar» se centra y el FAB no lo tapa.
  - Al ocultar Compras, el riel pierde «Compras» al instante: Ventas queda seguido de Inventario, comprobado con
    una sonda.
  - `/security/audit/entity-name/roles/entity-id/79` lleva a Auditoría con el filtro «roles», «Todo el historial»
    y «3 eventos»: Creó y dos «Cambió permisos», de Rosa Almánzar.
  - `/security/settings` lleva a Mi perfil.

## Tiempos medidos (R16/R25)

Ninguna operación de estos seis guiones es lenta:

| Operación | Tiempo |
|---|---|
| Duplicar rol, crear rol, «Cambios guardados», «Menús restablecidos», «¿Restablecer todo?» | ≤ 0,3 s tras la pausa de 0,4 s (menos de 0,7 s desde el clic) |
| Guardado por lote del editor y «Rol eliminado» (toast) | ≤ 0,3 s tras la pausa |
| Cambio de pestaña o de rol | < 1,2 s de clic a pantalla lista |
| Login con formulario (MySQL local, N-4) | 8,9–15,8 s |

El login ocurre fuera de cámara (`sesion`), antes del primer paso, así que no afecta al video. Como ningún guion
cambia de usuario en cámara, no hizo falta ajustar ninguna marca ni frase de relleno. Los tramos sin cambio que
predice `revisar.mjs` quedan en todos por debajo de 10 s.

## Pendiente para el orquestador

- **E0 · N-5 / E-3**: en 01-03 el panel del evento sembrado muestra «Productos · Productos» durante la marca de 6 s.
  La voz no lo lee. No se tocó.
- **E-4**: añadir `user_menu_visibility` (empresa 50) a `seeds/seguridad/_estado.mjs` y volver a fijar el estado,
  o dejarlo documentado como ahora en el `_comentario` de 09.
- **03** dura ≈ 4:06: si la voz real sale más lenta de 2,9 palabras/s, recortar la frase de F-154/F-155 del paso 05
  (lo propone el autor).
- El cambio de `seeds/_puertas/ensayar.py` está en el repo `claude-tutorial`, sin commitear.
