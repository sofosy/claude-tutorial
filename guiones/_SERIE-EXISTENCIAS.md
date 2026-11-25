# Serie «Existencias» — cargas masivas de existencias

Ocho videos sobre «Actualizar existencias», la importación de productos con existencia y la recepción de un
contenedor desde Excel, con las reglas del contador: motivo y referencia obligatorios, un solo asiento por carga,
vista previa del asiento, ninguna carga sin asiento con la contabilidad activa, e inventario inicial abierto hasta
«Cerrar inventario inicial».

## Empresa y datos (ficticios)

- Empresa 1 renombrada **Repuestos Germiva, SRL** (RNC 130555050): importadora de repuestos.
- Almacenes **Almacén Central** (`ALM-CENTRAL`, principal) y **Sucursal Santiago** (`SUC-SANTIAGO`), cada uno con su
  «Ubicación Principal». Los almacenes y productos sembrados se borran (suave) en la copia de la serie.
- Proveedores: **Autopartes del Caribe Germiva, SRL** (130555301) y **Repuestos del Cibao Germiva, SRL** (130555302).
- Repuestos con su proveedor habitual (`product_partners`): FA-210 filtro (185), PF-88 pastillas (650), AM-410
  amortiguador (2,300), RD-90 radiador (6,800) → Autopartes del Caribe; BJ-14 bujía (95), CD-305 correa (1,250),
  LF-04 líquido de frenos (240) → Repuestos del Cibao.
- Privacidad: perfil `ninguno` (todos los datos son inventados; la sustitución automática chocaba con el diálogo al
  cambiar de paso). La puerta es `tut auditar --video`. `130585050` está en `permitidos` porque el OCR lee a veces
  el RNC ficticio de la empresa (130555050, en el encabezado) con un 8 en lugar del 5 (comprobado en el video 4).

## Preparación

```bash
# 1. Base sembrada y API/front arriba: Germiva-api/scripts/dev-env/up.sh --web --source seed
node seeds/existencias/preparar.mjs            # renombra la empresa, crea almacenes, proveedores y repuestos
node seeds/existencias/restaurar.mjs --volcar  # guarda el canon en Germiva-api/.dev-env/existencias-canon.sql.gz
python3 seeds/existencias/_guiones.py          # escribe guiones/existencias-*.json
```

`restaurar.mjs <estado>` recarga el canon (≈ 40 s), aplica por el API las cargas del estado y deja en
`seeds/existencias/archivos/` el Excel que sube el video, generado de la plantilla REAL del sistema en ese estado
(así la vista previa lo reconoce como exportado y el conteo compara contra la existencia del momento).

| Estado | Qué deja | Videos |
|---|---|---|
| A | Siete repuestos sin existencia, inventario inicial abierto | 1 |
| B | Inventario inicial del Central (filtros, pastillas, bujías) y de Santiago; faltan correa y amortiguador | 2 |
| C | B + el complemento aplicado y el inventario inicial cerrado | 3, 4, 8 |
| D | B + complemento con 140 amortiguadores (error) y cerrado | 5 |
| E | B (inventario inicial abierto) | 6 |
| F | C + el mapeo «Otros Ingresos por Ajuste de Inventario» apuntando a la agrupadora 4.02.01.02 | 7 |

## Videos

| # | Guion | Situación | Cifras |
|---|---|---|---|
| 1 | `existencias-01-inventario-inicial` | Inventario inicial del Almacén Central | 3 productos, 719,500.00 contra patrimonio de apertura |
| 2 | `existencias-02-mercancia-que-quedo-fuera` | Plantilla «Sin existencia», complemento y «Cerrar inventario inicial» | 167,000.00 |
| 3 | `existencias-03-conteo-fisico` | Conteo de Santiago: sobrante, faltantes y un cero confirmado | +2,500.00 / −8,540.00 |
| 4 | `existencias-04-sobrante` | Sobrante encontrado; los movimientos quedan sin proveedor | 5,270.00 |
| 5 | `existencias-05-correccion` | Corrección de error de registro (140 → 40) | −230,000.00 |
| 6 | `existencias-06-productos-nuevos` | Importación de productos con existencia y proveedor habitual | 251,000.00 |
| 7 | `existencias-07-asiento-no-se-registra` | Asiento bloqueado por cuenta agrupadora, corrección del mapeo y nueva subida | 5,270.00 |
| 8 | `existencias-08-recepcion-contenedor` | Recepción sin orden desde Excel, a nombre del proveedor; historial del producto | 675,600.00 sin ITBIS |

Las cifras cuadran con la «Guía rápida de cargas masivas de existencias»
(`Germiva-api/docs/manuales/actualizacion-masiva-existencias/build-guia-rapida.cjs`).

## Puertas

`node seeds/_puertas/revisar.mjs guiones/existencias-0N-*.json` (0 ERROR) → `ensayar.py` (0 fallos) →
`tut.py video` → `veredicto.mjs` (PUBLICABLE) → revisión de fotogramas → `tut auditar --video`.

Lecciones de la serie:

- Cada «Aplicar» lleva en el mismo paso una frase y una marca sobre el diálogo de progreso; el paso siguiente arranca
  con la marca del resultado (regla «toda alerta se explica en ≤ 8 s»).
- Tras subir un archivo, una marca en `.sbu-context` (encabezado de la vista previa) evita el R0 mientras carga.
- El input de archivo del diálogo está oculto: `subir` con `ancla` en «Elegir archivo y revisar».
