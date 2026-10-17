# Informe AUTOR A · seguridad-02a-roles

**Estado**: E0 → deja **E2a** (crea «Contador externo» y «Cobrador») · entra rosa.almanzar.

## Pasos
1. `01-lista-de-roles`: qué es un rol; grupos «De la empresa» / «Del sistema», ↳ del hijo, insignia Vacío, conteo de titulares, rol abierto al entrar (Mensajero, con Editar y Más acciones), buscar «vend» y borrar.
2. `02-rol-del-sistema`: Contador: insignia, aviso de solo lectura, acciones en gris, solo «Duplicar»; por qué (A-002) + cartel consejo.
3. `03-duplicar`: «Duplicar rol» → «Contador externo» → «Operación completada» → rol nuevo editable.
4. `04-crear-rol`: Nuevo › Rol → «Cobrador» + descripción; interruptor de herencia solo señalado; éxito; insignia Vacío; errores en voz; resumen (caso práctico: duplicar frente a crear).

## Decisiones
- El diálogo ya es «Duplicar rol»/«Duplicar» (_SELECTORES §9): se quitó la aclaración «duplicar = clonar».
- Diálogos de éxito por panelClass (`.custom-alert-dialog-panel`, R20) y sin `al_decir` (R10), con frase de relleno.
- Nombre repetido y «salir sin guardar» solo en voz (verificados en la exploración, v02a-11/12).

## Dependencias de la ronda 2
- Ninguna.

## A comprobar en el ensayo
- Tras la toma: `restaurar.mjs E0` (E2a ya está fijado por `preparar.mjs E2a`).

## Puertas (sin apps, 2026-09-27)
- `node seeds/_puertas/revisar.mjs seguridad-02a-roles` → **0 ERROR**, 1 AVISO (primer paso sin `button.panel-collapse`: no existe en /home, /security/* ni /profile; _SELECTORES §0). Duración prevista de los pasos: **3:06** (+6 s de entrada y cierre de marca).
- `.venv\Scripts\python.exe tut.py verificar seguridad-02a-roles` → **0 errores, 0 avisos**.
- No se ensayó ni se grabó (lo hace el operador).
