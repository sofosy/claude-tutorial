#!/usr/bin/env node
// Puerta DESPUÉS de grabar y montar: lee salida/<modulo>/ (informe-video.md,
// grabacion/segmentos/*.json, audio/*.json, video.mp4) y dice por video
// PUBLICABLE o REGRABAR con la lista de fallos.
//
//   node seeds/_puertas/veredicto.mjs <modulo> [...]
//
// Sale con código 1 si algún video queda en REGRABAR.
import fs from 'node:fs';
import path from 'node:path';
import {
  HUECO_MAX, leerGrabacion, leerSrt, huecosGrabados, tokens, posiciones, tipoDe, selDe,
  esSelDialogo, firmaAlerta, fmt, corto,
} from './comun.mjs';

const DESFASE_MAX = 0.9;
const VENTANA_ALERTA = 8;     // una marca sobre el diálogo en ≤ 8 s la explica
const ALERTA_ANTES = 1.5;     // la marca puede llegar un poco ANTES de que la sonda la detecte
// verificar.py empareja así cada acción con su evento
const TIPO_EVENTO = { click: 'clic', escribir: 'clic', marcar: 'clic', resaltar: 'resaltar', seleccionar: 'seleccionar', subir: 'subir' };

const modulos = process.argv.slice(2).filter(a => !a.startsWith('--'));
if (!modulos.length) { console.error('uso: node seeds/_puertas/veredicto.mjs <modulo> [...]'); process.exit(2); }

/** ¿El selector es una fila entera o el pie de formulario? (CORTADO esperable) */
function cortadoEsperable(sel) {
  const s = String(sel);
  if (/footer\.form-layout-footer/.test(s)) return 'CORTADO sobre footer.form-layout-footer (barra fija del formulario)';
  const ult = s.replace(/:has(-text)?\([^)]*\)/g, '').trim().split(/\s*[>+~]\s*|\s+/).at(-1) || '';
  if (/^(tr|mat-row)\b/i.test(ult)) return 'CORTADO sobre una fila `tr` de tabla ancha';
  return null;
}

function veredicto(modulo) {
  const fallos = [], descartes = [], notas = [];
  const g = leerGrabacion(modulo);
  console.log(`\n═══ ${modulo}`);
  if (!g) {
    console.log(`   no hay salida/${modulo}/grabacion/segmentos`);
    console.log('   → REGRABAR');
    return false;
  }
  const video = path.join(g.salida, 'video.mp4');
  const informe = path.join(g.salida, 'informe-video.md');
  if (!g.guion) notas.push(`sin guiones/${modulo}.json: desfases leídos del informe y marcas de 4,5 s`);

  // 1) video al día
  const segMax = Math.max(0, ...g.pasos.filter(p => !p.falta).map(p => p.mtime));
  if (!fs.existsSync(video)) fallos.push('no existe video.mp4 (falta montar: tut montar-video)');
  else if (fs.statSync(video).mtimeMs < segMax) fallos.push('video.mp4 es MÁS VIEJO que los segmentos: hay una regrabación sin montar');
  for (const p of g.pasos.filter(p => p.falta)) fallos.push(`${p.id}: falta su segmento grabado`);

  // 2) errores de la grabación (segmentos) y del informe
  const errSeg = g.pasos.filter(p => p.seg?.error).map(p => ({ id: p.id, e: p.seg.error }));
  for (const { id, e } of errSeg) fallos.push(`${id}: ERROR en la grabación — ${corto(e, 110)}`);
  let lineasInforme = [];
  if (fs.existsSync(informe)) lineasInforme = fs.readFileSync(informe, 'utf8').split(/\r?\n/);
  else fallos.push('no existe informe-video.md');
  for (const l of lineasInforme) {
    if (!/\bERROR\b/.test(l)) continue;
    if (errSeg.some(({ e }) => l.includes(e.slice(0, 40)))) continue; // ya contado por el segmento
    fallos.push(`informe: ${corto(l.replace(/^[-*\s]+/, ''), 120)}`);
  }

  // 3) desfase clic ↔ palabra
  if (g.guion) {
    for (const p of g.pasos.filter(p => !p.falta && p.seg.tipo !== 'tarjeta' && p.paso)) {
      const palabras = p.audio.palabras || [];
      const dichas = palabras.map(w => tokens(w.texto).join(''));
      const eventos = p.seg.eventos || [];
      const usados = new Set();
      for (const acc of p.paso.acciones || []) {
        if (typeof acc.al_decir !== 'string') continue;
        const tipo = tipoDe(acc);
        if (!TIPO_EVENTO[tipo]) continue;
        const sel = tipo === 'subir' ? acc.subir.sel : selDe(acc);
        const i = eventos.findIndex((e, k) => !usados.has(k) && e.que === sel && e.tipo === TIPO_EVENTO[tipo]);
        if (i < 0) continue;
        usados.add(i);
        const ev = eventos[i];
        const cands = posiciones(dichas, acc.al_decir, g.guion.pronunciacion).map(k => palabras[k].t);
        if (!cands.length) continue;
        const tp = cands.reduce((a, b) => Math.abs(b - ev.t) < Math.abs(a - ev.t) ? b : a);
        const d = ev.t - tp;
        if (Math.abs(d) > DESFASE_MAX)
          fallos.push(`${p.id}: ${ev.tipo} en «${corto(sel, 50)}» a ${ev.t.toFixed(2)} s, ${d > 0 ? '+' : ''}${d.toFixed(2)} s respecto a «${acc.al_decir}» (${tp.toFixed(2)} s)`);
      }
    }
  } else {
    let pid = '';
    for (const l of lineasInforme) {
      const h = l.match(/^## (\S+) — /); if (h) pid = h[1];
      const m = l.match(/«(.+)» a ([\d.]+)s, clic a ([\d.]+)s \(desfase ([+-][\d.]+)s\)/);
      if (m && Math.abs(+m[4]) > DESFASE_MAX) fallos.push(`${pid}: clic ${m[4]} s respecto a «${m[1]}»`);
    }
  }

  // 4) imagen quieta > 10 s (sobre el video entero, atravesando cortes)
  const srt = leerSrt(path.join(g.salida, 'video.srt'));
  for (const h of huecosGrabados(g, HUECO_MAX)) {
    const dicho = srt.filter(c => c.b > h.a && c.a < h.b).map(c => c.texto).join(' ');
    fallos.push(`R0: ${h.dur.toFixed(1)} s sin cambios en pantalla ${fmt(h.a)}–${fmt(h.b)} (${h.pasos.map(x => `${x.id} ${x.a.toFixed(1)}–${x.b.toFixed(1)} s`).join(' + ')})` +
      (dicho ? ` · sonaba «${corto(dicho, 90)}»` : ''));
  }

  // 5) alertas sin explicar
  const alertas = [];
  let previas = new Set();
  for (const p of g.pasos.filter(p => !p.falta && p.seg.tipo !== 'tarjeta')) {
    const ev = p.seg.eventos || [];
    const marcas = ev.filter(e => e.tipo === 'resaltar' && esSelDialogo(e.que));
    for (const a of ev.filter(e => e.tipo === 'alerta')) {
      alertas.push({
        p, a, firma: firmaAlerta(a.que),
        arrastre: a.t < 1.5 && previas.has(a.que),
        cubierta: marcas.some(m => m.t >= a.t - ALERTA_ANTES && m.t <= a.t + VENTANA_ALERTA),
        // lo que exige verificar.py (y por tanto lo que el informe reporta):
        // una marca de diálogo en [t, t + 8]
        informe: marcas.some(m => m.t >= a.t && m.t <= a.t + VENTANA_ALERTA && /dialog|snack|alert|toast/.test(m.que)),
      });
    }
    previas = new Set(ev.filter(e => e.tipo === 'alerta').map(e => e.que));
  }
  for (const x of alertas) {
    const donde = `${x.p.id} ${x.a.t.toFixed(1)} s «${corto(x.a.que, 60)}»`;
    if (x.cubierta) {
      if (!x.informe) descartes.push(`alerta señalada milisegundos ANTES de que la sonda la detectara: ${donde}`);
      continue;
    }
    if (x.arrastre) { descartes.push(`mismo diálogo que sigue abierto desde el paso anterior: ${donde}`); continue; }
    const hermanas = alertas.filter(y => y !== x && y.firma === x.firma && y.cubierta);
    if (hermanas.length) { descartes.push(`mismo diálogo reportado varias veces mientras se opera dentro (explicado a ${hermanas[0].p.id} ${hermanas[0].a.t.toFixed(1)} s): ${donde}`); continue; }
    fallos.push(`alerta sin marca que la explique en ≤ ${VENTANA_ALERTA} s: ${donde}`);
  }

  // 6) elemento que no se veía entero
  for (const p of g.pasos.filter(p => !p.falta && p.seg.tipo !== 'tarjeta')) {
    for (const e of (p.seg.eventos || []).filter(e => e.visible === false)) {
      const m = e.medida || {};
      const donde = `${p.id} ${e.t.toFixed(1)} s ${e.tipo} «${corto(e.que, 60)}» (elemento ${m.arriba}..${m.abajo}px, franja ${m.tope}..${m.fondo}px)`;
      const fp = cortadoEsperable(e.que);
      if (fp) descartes.push(`${fp}: ${donde}`);
      else fallos.push(`CORTADO: ${donde}`);
    }
  }

  console.log(`   video ${fmt(g.total)} · ${g.pasos.length} pasos`);
  for (const n of notas) console.log(`   nota: ${n}`);
  if (fallos.length) { console.log(`   FALLOS (${fallos.length}):`); for (const f of fallos) console.log(`    ✗ ${f}`); }
  if (descartes.length) { console.log(`   Descartados — falsos positivos conocidos (${descartes.length}):`); for (const d of descartes) console.log(`    · ${d}`); }
  const ok = !fallos.length;
  console.log(`   → ${ok ? 'PUBLICABLE' : 'REGRABAR'}`);
  return ok;
}

let malos = 0;
for (const m of modulos) if (!veredicto(m)) malos++;
console.log(`\nResumen: ${modulos.length - malos} PUBLICABLE · ${malos} REGRABAR`);
process.exit(malos ? 1 : 0);
