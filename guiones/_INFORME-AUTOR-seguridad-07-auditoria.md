# Informe de autor · seguridad-07-auditoria («Seguridad · La auditoría»)

- **Autor:** AUTOR C · 2026-09-27. Solo guion: no se ensayó ni grabó (sin apps).
- **Graba:** `rosa.almanzar` (sesion), un solo usuario. **Estado de partida: E0** →
  `node seeds/seguridad/restaurar.mjs E0` antes y después de cada ensayo y cada toma.
- **Duración prevista:** 3:47 (+6 s de entrada/cierre) · 01-la-bitacora 59 s · 02-filtros 54 s ·
  03-detalle-del-evento 55 s · 04-historial-y-persona 60 s.

## Qué escribe cada toma (para que `restaurar E0` lo deshaga)

| Paso | Escribe en BD |
|---|---|
| 01–04 | nada propio; solo el acceso de la sesión de Rosa en `audit_logs` (lo borra `restaurar E0`, que restaura `audit_logs` por empresa y marca de agua) |

Tecleo sin guardado: Persona `ana.mejia`, Registro `quotes`, IP `10.9.9.9` (solo filtros, van a la URL).

## Guion

- 01 entra con `navegar /security/resumen` (el enlace «Seguridad» del riel de Rosa cae en y=716) y pulsa
  la pestaña Auditoría en cámara; presenta el total, los grupos por día y las columnas Hora · Quién ·
  Acción (colores) · Registro · IP.
- 02 Período → «Últimos 30 días»; Persona = usuario de Ana; Acción → «Creó» (el menú no se cierra: Escape);
  Registro `quotes` (la voz explica que es el nombre interno, F-200); IP `10.9.9.9` → vacío «No se
  encontraron resultados…»; «Limpiar».
- 03 Período → «Todo el historial» (así la fila sembrada sale aunque se grabe >7 días después); fila
  «Cambió permisos» (Almacén: Ver, Crear, Editar, Importar → + Exportar); fecha, registro, quién, antes
  tachado / después resaltado, Solicitud (IP, Origen, evento, número de solicitud). Cartel consejo.
- 04 «Historial del registro →» (Creó + 2 Cambió permisos del rol 79) → vuelve a abrir el cambio →
  «Ver a …» → Personas filtrada por Rosa. En voz: «Cargar eventos anteriores» y «El evento no está entre
  los resultados…». Resumen práctico + cartel consejo (tema obligatorio «revisar la auditoría»).

## Dependencias de la ronda 2 (re-verificar en el ensayo)

- **D-S5**: 02 escribe en Persona/Registro/IP y espera que la lista se filtre AL ESCRIBIR. Hoy solo filtra
  al recargar: sin la corrección, 02 no se puede grabar.
- **D-S6/D-S7**: la fila se busca por «Cambió permisos»; la voz dice «quién lo hizo: Rosa» y «el enlace Ver
  a Rosa» (vale con usuario o con nombre) y NO lee la etiqueta del registro («Roles #79» hoy).
- **D-S7 y el filtro Persona**: se teclea el usuario `ana.mejia` (verificado por URL `persona=ana.mejia`).
  Si tras D-S7 el filtro comparara el nombre visible, cambiar el texto a «Ana Mejía».
- **D-S11/D-S13**: la voz dice «en Productos» (no «Inventario») y describe el Origen sin afirmar cuál sale
  («un navegador con su sistema o un programa conectado por API»); el evento sembrado dice «Cliente de API».

## A verificar en el ensayo

- `.sec-audit :text('No se encontraron resultados')` (el vacío filtrado no se pudo ver por D-S5).
- `.gm-sheet-meta:has-text('eventos')` (hay 4 `.gm-sheet-meta`; se toma el primero con «eventos»).
- Fecha de grabación: el paso 02 necesita los eventos de Ana del 27-09 dentro de «Últimos 30 días»:
  grabar antes del 2026-10-27 (o re-sembrar).

## Puertas

- `revisar.mjs` → 0 ERROR · 1 AVISO (justificado: no existe `button.panel-collapse` en `/security/*`).
- `tut.py verificar` → 0 errores, 0 avisos.
