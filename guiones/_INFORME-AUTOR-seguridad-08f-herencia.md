# Informe de autor · seguridad-08f-herencia («Con y sin permiso · La herencia (y por qué el equipo no cuenta)»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion (sin ensayo).
- **Graba:** solo `rosa.almanzar` (sesion). **Estado de partida: E0.** `restaurar.mjs E0` antes y después.
- **Duración prevista:** 2:51 (+6 s) · 01 40 s · 02 37 s · 03 36 s · 04 25 s · 05 34 s.

## Qué escribe cada toma

| Paso | Escribe |
|---|---|
| 02 | rol Vendedor (77): concede «Socios · Crear» (PARTNER_CREATE) → `role_permissions` (+ heredado materializado en Vendedor sénior) + `audit_logs` |
| 04 | rol Vendedor sénior (78): excluye ese permiso heredado → `role_permission_exclusions` + `audit_logs` |

Lo deshace `restaurar E0`.

## Contraste sobre el MISMO punto: el acceso efectivo de Carlos

| | Dónde | Qué se ve |
|---|---|---|
| CON (heredado) | 03 Personas › Carlos | «Vendedor sénior · Hereda de Vendedor»; Permisos efectivos › «Clientes y Proveedores 2/37» (verificado r08f; «12 / 1160») |
| SIN (excluido) | 05 Personas › Carlos | «Clientes y Proveedores 1/37» (E0 = 1/37; A VERIFICAR tras la exclusión) |

Barra de guardado: padre «afectan a 3 personas» (Ana, José, Héctor; Carlos no cuenta aunque herede) · hijo
«afectan a 1 persona» (verificado v08f). En el editor, «Clientes» es el recurso «Socios» del módulo «Clientes y
Proveedores» (la voz lo explica). «Por qué el equipo no cuenta»: fase 3 del diagrama + cartel cuidado en 05.

## Diagrama `acceso-efectivo`

Ya corregido por el plan (el equipo NO suma). Casa con E0: Carlos, Vendedor sénior (Aprobar, Facturas · Crear),
padre Vendedor (Clientes · Ver, Productos · Ver), Zona Este = Ana y José. Sin cambios.

## DESVIACIÓN del plan (avisada)

- El plan hacía entrar a Carlos dos veces a `/sales/partners` para ver aparecer/desaparecer «Nuevo Cliente».
  Con los 3 cambios de usuario el video pasaba de 4:10; el encargo pide comprobarlo «en el acceso efectivo», y
  así se hace (mismo punto, CON y SIN). Lo de «Nuevo Cliente» está verificado en r08f y queda solo en la
  cobertura como no enseñado en cámara. Si se quiere, se puede añadir como video corto aparte.

## Dependencias de la ronda 2

Ninguna (roles, personas y guardado en lote verificados).

## Puertas

- `revisar.mjs` → 0 ERROR · 1 AVISO (sin panel-collapse en `/security/*`; el primer paso es la lámina).
- `tut.py verificar` → 0 errores, 0 avisos.
