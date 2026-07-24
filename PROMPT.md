# Cómo trabajar esto con Claude Code

La herramienta hace el render. Lo que aporta Claude es **investigar la pantalla y
escribir el guion**: qué hace cada campo, qué se rompe si te equivocas, y en qué
orden contarlo. Eso no sale de un guion escrito a ciegas.

## Prompt de ejemplo — tutorial nuevo

> Quiero un tutorial de **[módulo]** de mi ERP.
>
> - La app corre en `http://localhost:4200` y el código está en `[ruta]`.
> - Entra con el usuario `[usuario]`; si pide código de verificación, sácalo de la
>   base (`config.local.json` tiene el acceso).
>
> Antes de escribir el guion, **recorre el módulo y dime qué encontraste**: las
> vistas, los campos de cada una, cuáles son obligatorios y qué reglas de negocio
> aplican. Si algo no lo puedes verificar en el DOM o en el código, márcalo como
> inferido en vez de darlo por hecho — no quiero que el video afirme cosas que
> nadie comprobó.
>
> Después arma `guiones/[modulo].json` siguiendo el estilo del que ya existe:
> una captura por campo, vista completa antes del detalle, y el porqué solo donde
> el campo implica una decisión o tiene consecuencia si se equivoca.
>
> Compila, revisa algunos fotogramas para confirmar que las marcas caen sobre los
> elementos correctos, corre `tut auditar` y muéstrame el resultado.

## Por qué está redactado así

**"Recorre el módulo y dime qué encontraste"** — separa investigar de narrar. Si
pides el guion directamente, el modelo rellena los huecos con lo que suena
razonable, y en un ERP lo razonable suele estar mal.

**"Márcalo como inferido"** — te da dónde revisar. Un tutorial que afirma reglas
fiscales inventadas es peor que no tener tutorial.

**"Revisa algunos fotogramas"** — sin eso, el modelo reporta que compiló, no que
quedó bien. La diferencia aparece rápido: marcas fuera de sitio, texto tapado,
acercamientos que recortan justo lo que señalan.

## Otros prompts útiles

**Corregir una redacción** (barato, no re-captura nada):

> En el paso `03-empresa-2` la narración suena telegráfica. Amplíala explicando
> por qué el nombre legal debe coincidir con la DGII. Re-narra y re-monta.

**Ver qué falta por documentar:**

> Corre `tut mapa` sobre el ERP y luego `tut cobertura`. Dime qué vistas no
> aparecen en ningún tutorial y propón en qué orden grabarlas.

**Auditar antes de publicar:**

> Corre `tut auditar` sobre todos los tutoriales y muéstrame cada hallazgo con el
> frame donde aparece. Si algo es un dato real, dime qué regla de privacidad
> habría que agregar para que la sustitución lo cubra.

## Lo que conviene revisar tú

- **Las reglas de negocio del guion.** Claude las saca del DOM y del código; el
  contexto de por qué el negocio funciona así lo tienes tú.
- **El resultado de `tut auditar`.** Es la última barrera antes de publicar.
- **La primera compilación completa.** El ritmo y el tono se ajustan rápido, pero
  hay que escucharlos.
