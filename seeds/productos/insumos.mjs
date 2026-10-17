// node seeds/productos/insumos.mjs — insumos de cocina para el video 7 (receta de la habichuela con dulce).
// Se corre DESPUÉS de restaurar.mjs: el canon solo trae insumos de ejemplo (electrónica, autos, telas).
import { api, uno, log, EMPRESA } from './_lib.mjs';

const LIBRA = 23, UNIDAD = 43;
const INSUMOS = [
  { name: 'Habichuela roja para cocinar', code: 'INS-HAB', cost: 52, unitMeasure: LIBRA, description: 'Habichuela roja seca, por libra' },
  { name: 'Leche evaporada lata', code: 'INS-LEC', cost: 65, unitMeasure: UNIDAD, description: 'Lata de 12 oz' },
  { name: 'Azúcar crema', code: 'INS-AZU', cost: 38, unitMeasure: LIBRA, description: 'Azúcar crema, por libra' },
  { name: 'Batata', code: 'INS-BAT', cost: 25, unitMeasure: LIBRA, description: 'Batata, por libra' },
];

for (const ins of INSUMOS) {
  const existe = +uno(`SELECT COUNT(*) FROM components WHERE company_id=${EMPRESA} AND code='${ins.code}' AND deleted_at IS NULL`);
  if (existe) continue;
  await api('POST', 'v1/component', { ...ins, category: 'PRODUCT', cost: String(ins.cost), unitMeasureValue: '1' });
  log('insumo', ins.name);
}
log('insumos listos');
