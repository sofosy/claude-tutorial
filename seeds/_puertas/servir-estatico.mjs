// Sirve el build estático del front en :4200 con fallback de SPA (index.html).
// Uso: node seeds/_puertas/servir-estatico.mjs <carpeta-browser> [puerto]
// Motivo: ng serve + esbuild ocupan ~5 GB; el estático, ~40 MB. Para grabar no hace falta HMR.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const raiz = path.resolve(process.argv[2] ?? '.');
const puerto = Number(process.argv[3] ?? 4200);
const tipos = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf',
  '.txt': 'text/plain', '.webmanifest': 'application/manifest+json', '.mp3': 'audio/mpeg',
};

http.createServer((req, res) => {
  const url = decodeURIComponent((req.url ?? '/').split('?')[0]);
  let archivo = path.join(raiz, url);
  if (!archivo.startsWith(raiz) || !fs.existsSync(archivo) || fs.statSync(archivo).isDirectory()) {
    archivo = path.join(raiz, 'index.html');
  }
  res.writeHead(200, { 'Content-Type': tipos[path.extname(archivo).toLowerCase()] ?? 'application/octet-stream' });
  fs.createReadStream(archivo).pipe(res);
}).listen(puerto, '::', () => console.log(`estático ${raiz} en :${puerto}`));
