# Convenciones comunes de los guiones de la serie «Seguridad» (orquestador, 2026-09-27)

Todos los autores las siguen, para que los 21 videos suenen y se vean como una sola serie.

## Archivo y nombre
- `guiones/seguridad-<NN>-<slug>.json` (p. ej. `seguridad-00-introduccion.json`, `seguridad-08d-alcance.json`).
- `titulo`: «Seguridad · <tema>»; para los casos: «Con y sin permiso · <tema>».
- `_comentario`: estado de partida (E0/E2a/E6c), qué escribe en BD, usuarios que entran, decisiones y AVISOS justificados.

## Cabecera fija (copiar igual)
```json
"base_url": "http://localhost:4200",
"sesion": {"usuario": "rosa.almanzar", "clave": "Demo2026!", "sel_entrar": "button.auth-primary-btn"},
"voz": {"id": "es-DO-RamonaNeural", "velocidad": "+15%"},
"musica": {"archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -32, "ducking": true, "fade_s": 2},
"loudnorm": {"lufs": -14, "tp": -1.5},
"marca_video": {"entrada_s": 3, "cierre_s": 3},
"rotulo_paso": {"segundos": 3.5},
"privacidad": {"permitidos": ["germiva", "1305550", "Las Palmas", "rosa", "almanzar", "ana", "mejia", "mejía", "jose", "josé", "cabrera", "carlos", "pimentel", "pedro", "nunez", "núñez", "marta", "guzman", "guzmán", "hector", "héctor", "vargas", "luisa", "feliz", "sonia", "reyes", "Zona Este", "Villa Mella", "809-555-0188", "germiva.demo"]}
```
El usuario de `sesion` es quien entra al empezar el video (ver plan). Cada paso lleva `capitulo` (título de capítulo de YouTube) y `rotulo` breve.

## Cambio de usuario EN CÁMARA (casos con/sin permiso)
Menú del usuario `button.topbar-user` → `.user-item-list:has-text('Cerrar sesión')` → pantalla de acceso → escribir
usuario y clave → `button.auth-primary-btn`. El login tarda 6–8 s: la voz lo cubre («Entro ahora como Ana, la
vendedora…») con una marca SIN `al_decir` sobre la pantalla que aparece. Nunca navegar a mano a `/auth/...` sin
narrarlo. El paso que cambia de usuario abre con la insignia del usuario que ENTRA.
**Ensayo T3 (2026-09-27):** el botón dice «Iniciar sesión» (no «Entrar») y mientras entra muestra spinner + «Entrando…».
En local el login tarda 5–11 s: receta usada en 08a–08h → clic con `al_decir` «pulso Iniciar», marca
`button.auth-primary-btn:has-text('Entrando')` (3000 ms, `cursor: false`) anclada a «Entrando» ≈2 s después, marca SIN
`al_decir` sobre `aside.sidebar`, y ≈10–12 s de voz entre «Entrando» y la primera acción de la pantalla nueva
(«Ya dentro, abro…»). El panel del menú sigue contraído tras cerrar sesión (localStorage) si se entra por `navegar`.

## Insignias, carteles, diagramas (motor nuevo, ver GRABACION.md «Insignia, cartel y diagrama»)
- Cada paso de un contraste lleva `"insignia": {"tipo": "con"|"sin", "texto": "Con permiso · Ana (Vendedor)"}`;
  pasos informativos de la consola pueden llevar `"tipo": "info"` («Administradora · Rosa») o nada.
- `cartel` tipo `consejo`/`cuidado`: 1–2 por video como máximo, frase corta (≤ 18 palabras), cubierto por la voz.
  Temas obligatorios en la serie: mínimo privilegio, guardar el secreto de la API (se muestra una sola vez),
  revisar la auditoría, no compartir usuarios, desactivar en vez de borrar.
- `diagrama`: `conceptos-seguridad` (00), `acceso-efectivo` (05 y/o 08f), `alcance-propios-todos` (08d),
  `estado-documento` (08e). Sus textos deben CASAR con los datos reales del canon E0 (lee los html en
  `marca/diagramas/` y `seeds/seguridad/README.md`); si no casan, corrige el html y avísalo en el informe.

## Verdades del sistema (NO afirmar lo contrario)
- No hay «filtros por estado del documento» en los permisos; los filtros del editor son Todos/Concedidos/Heredados/Sin conceder.
- Los equipos NO dan permisos: sirven para el alcance «Equipo». Acceso efectivo = roles de la persona + lo heredado del rol padre.
- El alcance aplica a los permisos de «Ver» y se decide por quién CREÓ el registro. Fuera del alcance, abrir por número da aviso.
- Un cambio de permisos vale al instante en el servidor; el menú se refresca al recargar/volver a entrar
  (verificar en el ensayo tras la ronda 2 de correcciones: puede refrescar solo).
- «Clientes» en el catálogo de permisos es el recurso «Socios».

## Selectores y tiempos
Solo de `guiones/_SELECTORES-SEGURIDAD.md` (verificados con count()==1). Tiempos medidos ahí (alta de usuario,
credenciales ≈3,5 s: marca de relleno + resultado SIN `al_decir`, R9/R10/R16/R25).
OJO: está en curso una ronda 2 de correcciones (HALLAZGOS-SEGURIDAD-VIDEO.md D-S1…D-S13): textos de Resumen/
Auditoría pasarán a «Cambió permisos», nombres de registro legibles en singular, actor con nombre y apellido,
títulos de la documentación con acento, «Guardando…» en botones. Escribe la narración para el comportamiento
CORREGIDO y marca en `_comentario` los pasos que dependan de él (se re-verifican en el ensayo).

## Puertas
Antes de entregar: `node seeds/_puertas/revisar.mjs <guion>` sin ERROR y `.venv\Scripts\python.exe tut.py verificar <guion>`
con 0 errores (ambos sin apps). NO ensayes ni grabes (lo hace el operador, uno a la vez).
NO edites `_COBERTURA-SEGURIDAD.md` (lo editan varios): escribe `_COBERTURA-AUTOR-<A|B|C>.md` con «punto → guion/paso»
y el orquestador lo fusiona. Informe por video en `_INFORME-AUTOR-<guion>.md` (decisiones, avisos, dependencias).
