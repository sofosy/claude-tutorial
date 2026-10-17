# Informe del autor · seguridad-06c-caso-integracion (AUTOR B, 2026-09-27)

- **Estado de partida:** **E6c**. «Programa del contador», id 7957, lleva la plantilla sin «Registrar compras» y sin «Productos · Ver». **Escribe:** 1 login de integración y 3 consultas (`api_call_count`/`last_api_call`), y concede «Productos · Ver» (paso 04). **Restaurar E6c después.** **Graba:** rosa.almanzar (su sesión solo se usa en el paso 04).
- **Duración predicha:** 2:23 (+6 s). 5 pasos: el programa (38 s) · consulta permitida (27 s) · consulta no permitida (27 s) · conceder en el ERP (29 s) · repetir (22 s).
- **Puertas:** 0 ERROR · 1 AVISO · `tut verificar` 0 errores.

## La lámina `marca/demo-integracion/index.html`
- Página autocontenida (sin recursos externos) titulada «Programa del contador». Una franja de prueba dice «Página de prueba: simula el programa del contador…» y la voz lo declara igual.
- Flujo real contra el API local: «Conectar» → `POST /api/auth/integration/login {apiKey, apiSecret}` → token (sessionStorage) · «Consultar facturas emitidas» → `GET /api/v1/invoices/sales` (200 en E6c: F1 y F2 emitidas + F3 borrador, ruta confirmada en `_ensuciar.mjs` y el README) · «Consultar productos» → `GET /api/v1/product` (403 en E6c).
- El 403 se pinta con el código, «Rechazado» y la frase del API sin «(PRODUCT_VIEW)». El código técnico sale aparte, en pequeño («Código técnico del permiso: …»), y la voz no lo lee.
- **CORS:** `Germiva-api/src/main.ts:55` crea la app con `cors: true`. Eso acepta cualquier origen y la cabecera `Authorization`, y el `fetch` de :4200 a :3001 pasa. Base del API: `http://localhost:3001/api` (se puede cambiar con `apiBase` en el JSON).
- **Sin secretos en el repo:** la clave y el secreto se leen de `./credencial.local.json`. Está en `marca/demo-integracion/.gitignore` y se genera con `marca/demo-integracion/preparar.mjs` desde `seeds/seguridad/credencial.json`, que ya está en `.gitignore`.
- **Mismo origen:** el motor no navega a otro origen. El guion lleva `rutas_locales` (`**/demo-integracion/*` → `marca/demo-integracion/`) para la GRABACIÓN y `spa: false`: cada `navegar` es una carga completa, y volver al ERP recarga Angular (≈3–5 s, cubierto por la voz). La página guarda el token en sessionStorage, así que en el paso 05 sigue «Conectado».
- La página NO se ha abierto en un navegador (regla del encargo). Solo se comprobó la sintaxis de su JS. El ensayo confirma su aspecto a 1280×720 y los selectores `#btn-conectar`, `#estado-conexion`, `#btn-facturas`, `#btn-productos`, `#res-*` `.res-codigo/.res-resumen/.res-mensaje/.filas`.

## Instrucciones para el operador
1. `node seeds/seguridad/restaurar.mjs E6c` (siempre, sobre todo si 06b ya se grabó: 06b rota el secreto).
2. `node marca/demo-integracion/preparar.mjs --estatico` (desde `claude-tutorial/`). Escribe `marca/demo-integracion/credencial.local.json` y copia `index.html` + el JSON a `fe-estatico-seguridad/browser/demo-integracion/`. **Esa copia hace falta para el ENSAYO** (`ensayar.py` no aplica `rutas_locales`); la grabación funciona con o sin ella.
3. Comprobar a mano que abre `http://localhost:4200/demo-integracion/index.html` (con `index.html` explícito: el servidor estático manda las carpetas al index del SPA).
4. Ensayo → `restaurar.mjs E6c` → grabación → `restaurar.mjs E6c`.
5. Al terminar la serie, borrar `credencial.local.json` de las dos carpetas.

## Decisiones
- En el ERP (paso 04) el permiso se busca por su código. Quedan 3 casillas parecidas y se elige excluyendo `SUPPLIER_PRODUCT_VIEW` y `ORDER_PRODUCT_VIEW` (volcado a5-04). La voz no lee el código.
- La voz explica «200» y «403» en palabras llanas («permitido» y «rechazado»).

## Avisos justificados
- Primer paso sin `button.panel-collapse`: la lámina no tiene menú.
