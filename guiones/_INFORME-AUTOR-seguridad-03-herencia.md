# Informe AUTOR A · seguridad-03-herencia

**Estado**: E0 · entra rosa.almanzar · crea «Vendedor en práctica», le excluye «Cotizaciones · Crear» y lo elimina (queda E0 + bitácora).

## Pasos
1. `01-rol-hijo`: Vendedor sénior: chip «Hereda de Vendedor», meta «heredados», leyenda, directo frente a heredado en Cotizaciones, filtro Heredados → Todos, el chip abre el padre, vuelta.
2. `02-crear-hijo`: Nuevo › Rol «Vendedor en práctica» + interruptor + Rol padre «Vendedor» (opciones «… Sistema»), aviso de sincronía, sin ciclos (voz), éxito.
3. `03-excluir` (cartel consejo): Crear heredado → Excluido de la herencia → Guardar cambios → toast; recálculo al cambiar el padre (voz, F-165).
4. `04-eliminar-rol` (cartel cuidado): Más acciones › Eliminar rol → confirmación → toast; casos que lo impiden, en voz.
5. `05-titulares` (caso práctico): Vendedor → enlace «3 personas tienen este rol» → José, Ana, Héctor («Nunca») → clic en Ana → su panel.
6. `06-historial` (caso práctico): `navegar` /security/roles?rol=77 → Historial → «Cambió permisos» con antes/después; permiso de auditoría en voz; resumen.

## Decisiones
- **Orden distinto del plan**: se elimina el rol de prueba ANTES de titulares e historial (el riel queda limpio y el cierre es un caso real).
- En el historial solo se señala «Cambió permisos»; la entrada «Creó» con campos crudos (D-S7) ni se marca ni se lee.
- Errores de eliminar (titulares / rol padre) en voz + cartel; se verificaron en la exploración (A4), no se provocan.

## Duración
- 3:59,5 de pasos + 6 s de marca = **≈ 4:05**, al borde de 4:10. Si la voz real sale más lenta (< 2,9 p/s), recortar la frase de F-154/F-155 del paso 05.

## Dependencias de la ronda 2
- D-S7 («por rosa.almanzar» → nombre): la voz dice «quién lo hizo», sin leerlo.

## A comprobar en el ensayo
- El clic en la fila de Ana (`app-role-holders .rh__row`) navega a Personas con su panel.
- Tras eliminar, la consola abre Mensajero (primer rol).

## Puertas (sin apps, 2026-09-27)
- `node seeds/_puertas/revisar.mjs seguridad-03-herencia` → **0 ERROR**, 1 AVISO (primer paso sin `button.panel-collapse`: no existe en /home, /security/* ni /profile; _SELECTORES §0). Duración prevista de los pasos: **4:00** (+6 s de entrada y cierre de marca).
- `.venv\Scripts\python.exe tut.py verificar seguridad-03-herencia` → **0 errores, 0 avisos**.
- No se ensayó ni se grabó (lo hace el operador).
