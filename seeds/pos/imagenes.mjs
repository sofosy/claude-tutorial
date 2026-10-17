// node seeds/pos/imagenes.mjs [--esperar]
// Pone la foto de cada producto del catálogo (imagenes/<slug>.jpg) como imagen PRINCIPAL, igual que la
// pestaña «Imágenes» de la ficha del producto: POST v1/media/upload (multipart `file`) y luego
// POST v1/product/:id/media { media: [{ media, isPrimary: true, sortOrder: 1 }] }.
// Idempotente: si el producto ya tiene como principal una foto con ese nombre, no la vuelve a subir.
// «Varilla corrugada» (slug null) queda sin foto a propósito (mosaico de iniciales en el POS).
//   --esperar → espera a imagenes/manifest.json (señal de fin de la descarga), sondeando cada 30 s, hasta 25 min.
// Verifica al final GET v1/media/view/:id?size=small (la miniatura que pide el POS) con admin.progreso.
import fs from 'node:fs';
import path from 'node:path';
import { api, sql, log, login, API, EMPRESA } from '../cajas/_lib.mjs';
import { AQUI } from './_estado.mjs';

const ADMIN = 'admin.progreso';
const DIR = path.join(AQUI, 'imagenes');
const MANIFEST = path.join(DIR, 'manifest.json');
const uno = s => sql(s)[0]?.[0];
const catalogo = JSON.parse(fs.readFileSync(path.join(AQUI, 'catalogo.json'), 'utf8')).productos;

if (process.argv.includes('--esperar')) {
  const t0 = Date.now();
  while (!fs.existsSync(MANIFEST)) {
    if (Date.now() - t0 > 25 * 60000) { console.error('✗ 25 min sin manifest.json'); process.exit(3); }
    log('esperando imagenes/manifest.json …');
    await new Promise(r => setTimeout(r, 30000));
  }
}
const token = await login(ADMIN);
let fallos = 0;
for (const p of catalogo) {
  const pid = +uno(`SELECT id FROM products WHERE company_id=${EMPRESA} AND code='${p.sku}' AND deleted_at IS NULL LIMIT 1`);
  if (!p.slug) { log(`${p.sku} sin foto a propósito`); continue; }
  const archivo = path.join(DIR, `${p.slug}.jpg`);
  if (!fs.existsSync(archivo)) { fallos++; console.log(`  ✗ ${p.sku} falta ${p.slug}.jpg`); continue; }
  const ya = uno(`SELECT m.id FROM product_media pm JOIN media m ON m.id=pm.media_id WHERE pm.product_id=${pid} AND pm.isPrimary=1
    AND pm.deleted_at IS NULL AND m.originalName='${p.slug}.jpg' AND pm.company_id=${EMPRESA} LIMIT 1`);
  if (ya) continue;
  const fd = new FormData();
  fd.append('file', new Blob([fs.readFileSync(archivo)], { type: 'image/jpeg' }), `${p.slug}.jpg`);
  const r = await fetch(`${API}/v1/media/upload`, { method: 'POST', headers: { Authorization: `Bearer ${token}` }, body: fd });
  const txt = await r.text();
  if (!r.ok) { fallos++; console.log(`  ✗ ${p.sku} upload ${r.status}: ${txt.slice(0, 200)}`); continue; }
  const media = JSON.parse(txt);
  const mediaId = media.id ?? media.data?.id;
  await api(ADMIN, 'POST', `v1/product/${pid}/media`, { media: [{ media: +mediaId, isPrimary: true, sortOrder: 1 }] });
  log(`${p.sku} ← ${p.slug}.jpg (media ${mediaId})`);
}

// Verificación: la miniatura que descarga el POS
for (const p of catalogo.filter(x => x.slug)) {
  const [mid, orig] = sql(`SELECT m.id, m.originalName FROM products pr JOIN product_media pm ON pm.product_id=pr.id AND pm.isPrimary=1 AND pm.deleted_at IS NULL
    JOIN media m ON m.id=pm.media_id WHERE pr.company_id=${EMPRESA} AND pr.code='${p.sku}' LIMIT 1`)[0] ?? [];
  if (!mid) { fallos++; console.log(`  ✗ ${p.sku} sin imagen principal en la BD`); continue; }
  const r = await fetch(`${API}/v1/media/view/${mid}?size=small`, { headers: { Authorization: `Bearer ${token}` } });
  const bytes = (await r.arrayBuffer()).byteLength;
  const ok = r.ok && /^image\//.test(r.headers.get('content-type') ?? '') && bytes > 500;
  if (!ok) fallos++;
  console.log(`  ${ok ? '✓' : '✗'} ${p.sku} media ${mid} (${orig}) → ${r.status} ${r.headers.get('content-type')} ${bytes} B`);
}
log(fallos ? `✗ ${fallos} fallo(s)` : '✓ imágenes listas');
process.exit(fallos ? 1 : 0);
