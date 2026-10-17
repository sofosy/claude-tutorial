// Prepara la lámina del video seguridad-06c sin escribir secretos en el repo.
// Uso (desde claude-tutorial/, con E6c ya restaurado):
//   node marca/demo-integracion/preparar.mjs            → marca/demo-integracion/credencial.local.json (grabación, rutas_locales)
//   node marca/demo-integracion/preparar.mjs --estatico → además copia la carpeta a ../fe-estatico-seguridad/browser/demo-integracion/ (ensayo)
// Toma la clave y el secreto de seeds/seguridad/credencial.json (lo escribe preparar.mjs E6c; en .gitignore).
import fs from 'node:fs';
import path from 'node:path';

const raiz = process.cwd();
const origen = path.join(raiz, 'seeds/seguridad/credencial.json');
const aqui = path.join(raiz, 'marca/demo-integracion');
if (!fs.existsSync(origen)) { console.error('Falta seeds/seguridad/credencial.json: corre antes «node seeds/seguridad/preparar.mjs E6c».'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(origen, 'utf8'));
const local = { nombre: c.nombre, apiKey: c.apiKey, apiSecret: c.apiSecret, prefijo: c.prefijo, apiBase: 'http://localhost:3001/api' };
fs.writeFileSync(path.join(aqui, 'credencial.local.json'), JSON.stringify(local, null, 2));
console.log('ok  marca/demo-integracion/credencial.local.json');
if (process.argv.includes('--estatico')) {
  const destino = path.resolve(raiz, '../fe-estatico-seguridad/browser/demo-integracion');
  fs.mkdirSync(destino, { recursive: true });
  for (const f of ['index.html', 'credencial.local.json']) fs.copyFileSync(path.join(aqui, f), path.join(destino, f));
  console.log('ok  ' + destino + ' (abrir http://localhost:4200/demo-integracion/index.html)');
}
