#!/usr/bin/env node
// Tramos de imagen quieta medidos sobre lo GRABADO (segmentos), con el texto
// del subtítulo que suena en cada tramo. Sirve para decidir dónde poner una
// marca o estirar un durante_ms.
//
//   node seeds/_puertas/huecos.mjs <modulo> [seg=10]
import path from 'node:path';
import { leerGrabacion, leerSrt, huecosGrabados, fmt, corto } from './comun.mjs';

const [modulo, umbralArg] = process.argv.slice(2);
if (!modulo) { console.error('uso: node seeds/_puertas/huecos.mjs <modulo> [seg=10]'); process.exit(2); }
const umbral = Number(umbralArg ?? 10);

const g = leerGrabacion(modulo);
if (!g) { console.error(`no hay salida/${modulo}/grabacion/segmentos`); process.exit(2); }
const srt = leerSrt(path.join(g.salida, 'video.srt'));

/** Lo que dice la voz entre a y b (segundos del video): subtítulos o, sin srt, palabras. */
function dicho(a, b) {
  if (srt.length) return srt.filter(c => c.b > a && c.a < b).map(c => c.texto).join(' ');
  return g.pasos.filter(p => !p.falta).flatMap(p => (p.audio.palabras || [])
    .filter(w => p.t0 + w.t >= a && p.t0 + w.t < b).map(w => w.texto)).join(' ');
}

const lista = huecosGrabados(g, umbral);
console.log(`${modulo} · video ${fmt(g.total)} · tramos quietos > ${umbral} s: ${lista.length}`);
for (const h of lista) {
  console.log(`\n  ${fmt(h.a)} – ${fmt(h.b)}  (${h.dur.toFixed(1)} s)  ${h.pasos.map(x => `${x.id} ${x.a.toFixed(1)}–${x.b.toFixed(1)} s`).join(' + ')}`);
  console.log(`    «${corto(dicho(h.a, h.b), 400)}»`);
}
