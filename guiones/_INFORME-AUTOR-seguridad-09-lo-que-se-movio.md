# Informe AUTOR A · seguridad-09-lo-que-se-movio

**Estado**: E0 · entra rosa.almanzar · escribe la visibilidad del menú de Rosa (la oculta y la restablece: termina igual). La contraseña se llena y NO se envía.

## Pasos
1. `01-contrasena-en-mi-perfil`: menú del usuario › Mi perfil → tarjeta Seguridad: contraseña actual, nueva y confirmación; «Actualizar contraseña» señalado sin pulsar; cuenta bloqueada en voz.
2. `02-visibilidad-del-menu` (cartel cuidado): Preferencias › Visibilidad del menú → candado de Inicio → apagar Compras → Guardar Cambios → «Cambios Guardados» → el riel sin Compras → Restablecer Todo → confirmación → «Menús Restablecidos» → Compras vuelve.
3. `03-perfil-consultorio`: `navegar` /my-company/perfil-consultorio → vuelve a /home sin aviso (se VE); insignia info «Solo en RegiSalud» + cartel con la ruta de RegiSalud.
4. `04-enlaces-viejos` (caso práctico): `navegar` /security/settings → Mi perfil; resumen.

## Decisiones
- **Perfil del Consultorio**: no se inventa pantalla ni se graba RegiSalud. Se enseña lo que pasa de verdad en el ERP (vuelve al inicio) y un cartel; el motor no tiene cartel «info» (solo consejo|cuidado), así que va un «consejo» titulado «En RegiSalud» + insignia info. Texto: «menú Configuración › Perfil del Consultorio (parte de Mi Empresa)» (F-222).
- **Orden**: el enlace viejo va al final saliendo de /home; pedido desde /profile, Angular no recargaría la vista y no se vería nada.
- Duración 2:22: dentro de 1:30–4:10; el tema no da para más sin relleno.

## Dependencias de la ronda 2
- Ninguna.

## A comprobar en el ensayo
- Que salir de /profile con la contraseña escrita no abra un aviso de «salir sin guardar».
- Candado de la fila «Inicio» del árbol (selector derivado de la cadena verificada de «Compras»; la exploración contó 3 candados).
- «Desplegar» choca con el FAB en su sitio inicial (y=624); el motor la centra antes del clic.

## Puertas (sin apps, 2026-09-27)
- `node seeds/_puertas/revisar.mjs seguridad-09-lo-que-se-movio` → **0 ERROR**, 1 AVISO (primer paso sin `button.panel-collapse`: no existe en /home, /security/* ni /profile; _SELECTORES §0). Duración prevista de los pasos: **2:22** (+6 s de entrada y cierre de marca).
- `.venv\Scripts\python.exe tut.py verificar seguridad-09-lo-que-se-movio` → **0 errores, 0 avisos**.
- No se ensayó ni se grabó (lo hace el operador).
