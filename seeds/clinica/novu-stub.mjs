// Novu de mentira para grabar en local: el entorno del contenedor no tiene cuenta de Novu y sin ella el API no
// "envía" correos (el portal del paciente responde «No pudimos enviar el código»). Responde OK a todo y anota
// cada envío en /tmp/claude-0/novu-stub.log. Solo para el entorno local: NOVU_API_URL=http://127.0.0.1:4599
import http from 'node:http';
import fs from 'node:fs';
const LOG = '/tmp/claude-0/novu-stub.log';
http.createServer((req, res) => {
  let body = '';
  req.on('data', c => (body += c));
  req.on('end', () => {
    fs.appendFileSync(LOG, `${new Date().toISOString()} ${req.method} ${req.url} ${body.slice(0, 500)}\n`);
    // Un mismo cuerpo sirve a todas las respuestas que valida el SDK de Novu (@novu/api): el suscriptor de v2
    // (sin envoltura) y el disparo de un evento (envuelto en `data`); zod descarta los campos que no espera.
    const ahora = new Date().toISOString();
    const evento = { acknowledged: true, status: 'processed', transactionId: 'stub-' + Date.now() };
    const cuerpo = req.method === 'GET' && req.url.includes('notifications') ? { data: [] } : {
      _id: 'stub', subscriberId: 'stub', _organizationId: 'stub', _environmentId: 'stub', deleted: false,
      createdAt: ahora, updatedAt: ahora, ...evento, data: evento,
    };
    res.writeHead(req.url.includes('trigger') ? 201 : 200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(cuerpo));
  });
}).listen(4599, '127.0.0.1', () => console.log('novu-stub en :4599'));
