// node seeds/seguridad/preparar.mjs E2a|E6c
// Arma por API, sobre E0 (lo restaura antes), el estado de partida de un video y lo deja listo para fijar:
//   E2a = E0 + roles «Contador externo» (clon del rol del sistema Contador) y «Cobrador» (vacío)   → video 02b
//   E6c = E0 + credencial «Programa del contador» con permisos propios (plantilla SIN «Registrar compras»)
//         → videos 06b y 06c. El secreto queda en credencial.json (demo local; nunca en cámara).
// Después: node seeds/seguridad/fijar.mjs <E#> && node seeds/seguridad/restaurar.mjs E0
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { AQUI, IDS, api, uno, log, leerJson, EMPRESA } from './_lib.mjs';

const estado = process.argv[2];
const ROSA = 'rosa.almanzar';
if (!['E2a', 'E6c'].includes(estado)) { console.error('uso: node seeds/seguridad/preparar.mjs E2a|E6c'); process.exit(2); }
execFileSync('node', [path.join(AQUI, 'restaurar.mjs'), 'E0'], { stdio: 'inherit' });

if (estado === 'E2a') {
  const contador = +uno(`SELECT id FROM roles WHERE company_id IS NULL AND code='ACCOUNTANT'`);
  const desc = uno(`SELECT IFNULL(description,'') FROM roles WHERE id=${contador}`);
  const c = await api(ROSA, 'POST', `role/${contador}/clone`, { name: 'Contador externo', description: desc });
  const b = await api(ROSA, 'POST', 'role', { name: 'Cobrador', description: 'Cobra facturas a domicilio', parentRole: null });
  log('E2a: Contador externo', c.id ?? c.data?.id, '· Cobrador', b.id);
}

if (estado === 'E6c') {
  const r = await api(ROSA, 'POST', 'v1/integration-users', {
    integrationName: 'Programa del contador', integrationDescription: 'Consulta las facturas emitidas para la contabilidad',
  });
  const id = r.user?.id;
  // mínimo privilegio (06a): se le quita «Registrar compras» → la credencial recibe su rol propio (A-043)
  await api(ROSA, 'DELETE', `v1/integration-users/${id}/permissions/PURCHASE_INVOICE_CREATE`);
  const cred = { id, nombre: 'Programa del contador', apiKey: r.credentials.apiKey, apiSecret: r.credentials.apiSecret, prefijo: r.credentials.apiKeyPrefix };
  fs.writeFileSync(path.join(AQUI, 'credencial.json'), JSON.stringify(cred, null, 2));
  const ids = leerJson(IDS, {});
  ids.credenciales = { ...(ids.credenciales ?? {}), contador: cred };
  fs.writeFileSync(IDS, JSON.stringify(ids, null, 2));
  const rol = uno(`SELECT id FROM roles WHERE company_id=${EMPRESA} AND integration_user_id=${id} AND is_integration_role=1`);
  log('E6c: credencial', id, 'rol propio', rol, '→ credencial.json');
}
log(`listo: node seeds/seguridad/fijar.mjs ${estado}`);
