# seeds/pos — datos y estado P0 del video «Punto de venta» (/pos)

Empresa demo **43 «Ferretería El Progreso»** (SRL, RNC 130555021, DOP, **sin e-CF**:
`companies.managesElectronicBilling = 0` → el POS emite B02/B01, no E32/E31). Todo toca SOLO filas
`company_id = 43`. Front: módulo `src/app/modules/pos` (commit 703012072 de germiva-website).
Correr desde `claude-tutorial/` con Node ≥ 18 (sin dependencias). Reutiliza `../cajas/_lib.mjs`.

## Uso rápido

```bash
node seeds/pos/restaurar.mjs P0      # ≈ 0,8 s: deja la empresa en el canon limpio del video (verifica conteos)
node seeds/pos/verificar.mjs         # catálogo/descuentos/NCF como los lee el POS (admin.progreso, solo lectura)
node seeds/pos/verificar.mjs --cajera  # ídem + permisos efectivos de yohanna (OJO: su login cierra su sesión del navegador)
```

Recrear desde cero (idempotente, ~1 min): `node seeds/pos/sembrar.mjs --desde-s0` →
`node seeds/pos/imagenes.mjs` → `node seeds/pos/fijar.mjs P0`.

| Archivo | Qué hace |
|---|---|
| `catalogo.json` | 6 categorías y 25 productos (SKU, precio SIN ITBIS, costo, existencia, exento, slug de la foto) |
| `sembrar.mjs [--desde-s0]` | Plan 15, categorías, productos + precio, existencias, clientes, línea de crédito, descuentos, «exigir turno», rol complementario de la cajera. Todo por API con los payloads de los formularios del front. Escribe `ids.json` |
| `imagenes.mjs [--esperar]` | Sube `imagenes/<slug>.jpg` (`POST v1/media/upload`) y la pone como principal (`POST v1/product/:id/media`, `ManageProductMediaDto`), como la pestaña «Imágenes» de la ficha. Verifica `GET v1/media/view/:id?size=small` |
| `verificar.mjs [--cajera]` | Repite la consulta del catálogo del POS y el cálculo de `pos-catalog.service.ts toItem()` (precio con ITBIS, «N en existencia» / «Quedan N» / «Agotado», imagen), el `evaluate-for-invoice` de los descuentos con el consumidor final y el `form-bootstrap` |
| `prueba.mjs [--sin-restaurar]` | Prueba de punta a punta como yohanna: abre turno, venta de contado B02 con 5 %, venta a crédito B01; verifica en BD y restaura P0 |
| `_estado.mjs` | Tablas que fija/restaura P0 = las 41 de Cajas + 22 medidas para el POS (catálogo, existencias, lotes, fotos, clientes, crédito, descuentos, contadores del plan, rol) |
| `fijar.mjs P#` / `restaurar.mjs P#` | Copias de `cajas/fijar.mjs` / `cajas/restaurar.mjs` con la lista de `_estado.mjs`; estados en `estados/P#.sql|json` |
| `_medir.mjs` | Foto de conteo/MAX(id)/MAX(updated_at) de las tablas con `company_id` (y AUTO_INCREMENT de las demás) para medir qué toca un flujo (`--comparar`) |

## Qué hay en P0

- **Plan**: suscripción 42 → plan **15 «Empresarial»** (trae POS, INVOICING, PRODUCTS, **SALES_CREDIT** y
  **SALES_DISCOUNT**; el plan 2 «Emprendedor» no trae los dos últimos → sin «Crédito del cliente» ni
  descuentos, y H-17 al abrir facturas). P0 guarda la fila de `subscriptions`; `cajas/restaurar.mjs S0…S6`
  NO la tocan (volver al plan 2: `node seeds/cajas/plan-s8.mjs off`).
- **Categorías** (`product_types`): Herramientas 35, Electricidad 36, Plomería 37, Pintura 38, Construcción 39, Jardín 40.
- **Productos** 212…236 (`FER-1001`…`FER-6003`, ver `ids.json`), activos, con inventario, sin lote obligatorio,
  ITBIS 18 % (tax 1) salvo *Fertilizante soluble, 500 g* exento (tax 4, codeNumber 4). Precio regular en DOP sin
  ITBIS (`prices`, prioridad 1). Existencias en «Almacén Principal» (ubicación 34) por «Carga inicial de
  existencias» (tipo 17): *Llave ajustable* 3 («Quedan 3»), *Tomacorriente doble* 0 («Agotado»), el resto «N en existencia».
- **Fotos**: 24 productos con imagen principal; *Varilla corrugada 3/8"* sin foto a propósito (iniciales).
- **Clientes**: *Constructora Hermanos Peña* (8034, empresa, RNC ficticio **130555206** con dígito DGII
  válido y ausente del padrón local `taxpayers`, B01 por defecto) con **línea de crédito 3: RD$150,000 a 30
  días, vence 2027-12-31** (solicitud 5 evaluada y aprobada por admin.progreso); *María Fernández* (8035,
  persona, cédula ficticia **40225107313** con dígito verificador válido, B02, sin crédito).
  *Consumidor Final* (7737, interno) intacto. *Constructora Los Pinos* (7740) sigue ahí (serie de Cajas).
- **Descuentos** de toda la factura, porcentuales, sin aprobación, sin aplicación automática (el cajero los
  elige con F6): 15 «Descuento de mostrador 5 %», 16 «Cliente frecuente 10 %».
- **NCF**: rangos de la empresa B01 (528) y B02 (529) 0000000001–0099999999, vencen 2026-12-31, 0 usados.
- **Caja**: `company_configs.require_cashier_session_for_sale = 1` (el POS muestra «Abre tu turno para
  vender»). Caja Principal (49, CAJA-01) **cerrada**, sin conteo por denominaciones
  (`require_denomination_control = 0` → teclado numérico en efectivo), `cashier_config.blind_count = 0`
  («Efectivo esperado en gaveta» visible); es la ÚNICA caja que yohanna puede abrir
  (`GET v1/cashiers?availableForOpening=true` → solo la 49: Mostrador 2 la tiene abierta luis, Santiago
  bloqueada). No existe en el ERP una «asignación» de caja a usuario. Denominaciones DOP: las 10 globales.
- **Usuarios** (clave `Demo2026!`): graba **yohanna.peralta** (roles *Cajero* 2 + *Cajero POS demo* 75 de la
  empresa 43). admin.progreso (Admin) para preparar. luis.batista y carmen.rosario como en Cajas.

## Rol «Cajero POS demo» (75) — por qué existe

El rol de catálogo *Cajero* (2) no trae permisos que el POS usa (hallazgo, ver informe):
`MEDIA_VIEW` (fotos del catálogo → sin él todas las tarjetas salen con iniciales),
`COMPANY_VIEW` (`GET v1/company/43/internal-partner` → sin él el POS no evalúa descuentos para el
consumidor final y el selector solo ofrece «Sin descuento»), `INVOICE_RETURN_CREATE` (botón «Devolución»)
e `INVOICE_RETURN_VIEW` (la ruta de la devolución). Se creó un rol DE LA EMPRESA 43 con esos 4 permisos y
se le sumó a yohanna (`PATCH user/add-role/7646`), sin tocar el rol global *Cajero*.

## Prueba de punta a punta (2026-09-25, repetida 3 veces con resultado idéntico)

`node seeds/pos/prueba.mjs` como yohanna, mismos payloads que `pos-checkout.service.ts`:
- Turno abierto en Caja Principal con 5 × 1,000.
- Contado, consumidor final, B02, descuento 15: Martillo ×2 + Fertilizante soluble ×1 → factura 1000000001
  **PAID**, NCF **B0200000001**, total 1,369.90 (descuento 64.00), recibo RCP-2026-000001 recibido 1,500.00
  cambio 130.10 en ese turno; existencia del martillo 38 → 36.
- Crédito, Constructora Hermanos Peña, B01: Cemento de albañilería ×10 + Varilla ×20 → factura 1000000002 creada y luego
  **EMITTED**, NCF **B0100000001**, total 13,688.00, CxC 13,688.00 vence 2026-10-25; línea 150,000 → usado
  13,688 / disponible 136,312.
- `restaurar.mjs P0` → 0 facturas, 7 sesiones (las de Cajas), existencias iguales al catálogo, Caja Principal cerrada.

## Trampas

- `restaurar.mjs P0` cubre también todas las tablas de Cajas (P0 es superconjunto). Al revés NO:
  `cajas/restaurar.mjs S#` deja huérfanas las filas del POS (existencias, categorías, clientes, descuentos) y el plan 15.
- Los archivos de las fotos quedan en el almacenamiento del API aunque P0 borre filas de `media` nuevas.
- Cada login revoca la sesión previa del MISMO usuario: no correr `verificar.mjs --cajera` ni `prueba.mjs`
  mientras yohanna graba.
- `invoices.payment_due_date` se ve 1 h antes en el cliente mysql (UTC-5 vs RD): es la zona, no un error.
