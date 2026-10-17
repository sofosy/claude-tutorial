# Informe del autor · seguridad-06a-credenciales (AUTOR B, 2026-09-27)

- **Estado de partida:** E0. **Escribe:** la credencial «Programa del contador» (usuario de integración + rol propio al quitar «Registrar Facturas de Compra»). **Restaurar E0 después.** **Graba:** rosa.almanzar.
- **Duración predicha:** 3:43 (+6 s). 5 pasos: qué es (46 s) · crear (≈55 s) · el secreto (37 s) · panel (38 s) · sus permisos (46 s).
- **Puertas:** 0 ERROR · 1 AVISO · `tut verificar` 0 errores.

## Decisiones
- La franja del secreto aparece ≈3,5 s después de «Generar credenciales». Su marca va anclada ≈6 s después del clic (R25). Además, la creación abre sola el panel (`?credencial=`), que el paso 04 da por abierto.
- «Mostrar» se señala y NO se pulsa: el secreto no sale en claro en cámara. «Copiar secreto» sí se pulsa: CDK Clipboard funciona sin permiso de portapapeles («Secreto copiado», 0,2 s en la exploración).
- La API Key completa (`gv_live_…`) sí se ve en la franja. Es de la demo local, se borra al restaurar y cambia en cada toma. Si el revisor la quiere tapada, hay que añadir el valor de la toma a `privacidad.mapa_fijo`.
- En la página de permisos se busca por el código. Es lo único que deja solo 2 casillas, la misma en Facturación y en Compras. La voz no lee el código y explica por qué sale dos veces.
- Carteles (2, el máximo de la convención): cuidado «el secreto se ve una sola vez» (03) y consejo de mínimo privilegio (05). «Limitar IP y rutas reduce el daño si se filtra» queda solo en voz (02).
- La voz no promete antes/después en la Auditoría para los permisos de credenciales (A-075).

## Avisos justificados
- Primer paso sin `button.panel-collapse` (no existe en `/security/*`).

## Selectores que el ensayo debe confirmar
`.sec-api__title`, `.sec-api__row:has-text('Tienda en línea anterior') :text('gv_live_0e9d2d31')`, `.sec-api__stale`, `.sec-api__notes`,
`mat-dialog-container .gm-dialog-note`, `mat-dialog-container mat-form-field:has(input[placeholder='/api/v1/invoice'])`, `.sec-api__secret-text`,
`.sec-api__secret .sec-api__value >> nth=0|1`, `.sec-api__card-top`, `.sec-api__facts`, `.sec-api__block-head >> nth=0`,
`.sec-api__module:has(.sec-api__module-name:text-is('Facturación'|'Compras'))`, `.sec-api__bars`, `.page-title`.
Además: que el panel siga abierto al volver con «Volver a Integraciones» (el volcado v06a-11 trae `?credencial=`).
