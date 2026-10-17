# Informe del autor · seguridad-05-acceso-efectivo (AUTOR B, 2026-09-27)

- **Estado de partida:** E0. **Escribe:** nada. **Graba:** rosa.almanzar.
- **Duración predicha:** 2:31 (+6 s). 4 pasos: lámina (44 s) · Carlos (33 s) · José (29 s) · Ana, Luisa y caso (44 s).
- **Puertas:** 0 ERROR · 1 AVISO · `tut verificar` 0 errores.

## Comprobación del diagrama contra E0 (`_resultados-v05.json`, `seeds/seguridad/README.md`)
- `acceso-efectivo.html` (ya corregido el 09-27 para la verdad 2): Carlos, Vendedor sénior hijo de Vendedor. Padre: Clientes·Ver y Productos·Ver. Directos: Cotizaciones·Aprobar y Facturas·Crear. Equipo Zona Este (Ana, José) tachado, «no suma». **Los 4 permisos casan con E0.**
- **CORREGIDO:** el rótulo del resultado decía «La unión de todos sus permisos» y listaba solo 4. Carlos tiene **11** (ficha: Productos 1/42 · Clientes y Proveedores 1/37 · Facturación 2/79 · Cotizaciones 7/19). Ahora dice «11 en total; aquí, 4 de ejemplo», y la voz dice «en la lámina van cuatro de ejemplo; en su ficha vamos a ver los once». El cambio queda anotado en el comentario del html.
- Cifras que dice la voz, todas de E0: Carlos 11 (Cotizaciones 7 = Ver/Crear/Editar + Aprobar/Rechazar/Aceptar/Convertir; Facturación 2) · José 10 (Productos 5, Inventario 1, Clientes 1, Cotizaciones 3) · Ana 5 · Luisa 0 («Sin ningún rol: inicia sesión pero no ve ningún módulo.», «Ningún permiso concedido.»).

## Decisiones
- La voz dice «vale desde la siguiente operación» (A-022). No promete que el menú cambie sin volver a entrar (D-S9).
- Caso práctico: Luisa «no ve nada» → su ficha lo explica → «+ Asignar rol» (señalado).

## Avisos justificados
- Primer paso sin `button.panel-collapse`: el paso 01 es la lámina y `/security/*` no tiene panel.

## Dependencias de la ronda 2
- Ninguna. Otros autores que usen `acceso-efectivo` (08f) verán el rótulo nuevo.
