// Utilidades compartidas por las puertas de calidad (revisar, veredicto, huecos).
// Sin dependencias npm: solo node:fs y node:path. Replica la lógica del motor
// Python (tutorial/grabar.py, narrar.py, rutas.py) que hace falta para predecir
// o medir; si el motor cambia, este archivo es el que hay que ajustar.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

// ── constantes del motor (grabar.py) ─────────────────────────────────────────
export const PAD = 0.6;          // respiro tras cada narración
export const ADELANTO = 0.45;    // primera acción sin al_decir
export const MOVER = 0.55;       // viaje del cursor (MOVER_MS)
export const ANTICIPO = MOVER + 0.45; // lo que el motor adelanta un clic a su palabra
export const ANTICIPO_MARCA = 0.25;
export const TECLEO = 0.045;     // TECLEO_MS entre teclas
export const MARCA_MS = 4500;    // resaltar sin durante_ms
export const HUECO_MAX = 10;     // R0

// ── PRONUNCIACION: se lee de narrar.py para no divergir; copia de respaldo ──
const PRONUNCIACION_RESPALDO = {
  ITBIS: 'itebís', NCF: 'ene-ce-efe', RNC: 'erre-ene-ce', DGII: 'de-ge-i-i',
  ARS: 'a-erre-ese', SRL: 'ese-erre-ele', B01: 'be cero uno', B02: 'be cero dos',
  B03: 'be cero tres', B04: 'be cero cuatro',
};

function leerPronunciacion() {
  try {
    const src = fs.readFileSync(path.join(RAIZ, 'tutorial', 'narrar.py'), 'utf8');
    const bloque = src.match(/PRONUNCIACION\s*=\s*\{([\s\S]*?)\n\}/);
    if (!bloque) return PRONUNCIACION_RESPALDO;
    const mapa = {};
    for (const m of bloque[1].matchAll(/"([^"]+)"\s*:\s*"([^"]+)"/g)) mapa[m[1]] = m[2];
    return Object.keys(mapa).length ? mapa : PRONUNCIACION_RESPALDO;
  } catch { return PRONUNCIACION_RESPALDO; }
}
export const PRONUNCIACION = leerPronunciacion();

const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** narrar.para_voz: la sigla suelta se reemplaza por cómo se pronuncia. */
export function paraVoz(texto, extra) {
  const mapa = { ...PRONUNCIACION, ...(extra || {}) };
  let t = String(texto);
  for (const [sigla, dicho] of Object.entries(mapa)) {
    t = t.replace(new RegExp(`(?<![\\p{L}\\p{N}_-])${escRe(sigla)}(?![\\p{L}\\p{N}_-])`, 'gu'), dicho);
  }
  return t;
}

/** grabar._normal: minúsculas y solo letras/dígitos. */
export const normal = w => [...String(w).toLowerCase()].filter(c => /[\p{L}\p{N}]/u.test(c)).join('');

/** Palabras que dirá la voz (edge-tts no emite límites para «—», «/», «·»). */
export function tokens(texto, extra) {
  return paraVoz(texto, extra).split(/\s+/).map(normal).filter(Boolean);
}

/** Todas las posiciones (índice de palabra) donde la narración dice `clave`. */
export function posiciones(dichas, clave, extra) {
  const b = tokens(String(clave), extra);
  const r = [];
  if (!b.length) return r;
  for (let i = 0; i + b.length <= dichas.length; i++) {
    let ok = true;
    for (let k = 0; k < b.length; k++) if (dichas[i + k] !== b[k]) { ok = false; break; }
    if (ok) r.push(i);
  }
  return r;
}

// ── carga del guion como rutas.cargar_guion (config + local + guion, campos) ──
function leerJson(ruta) {
  try { return JSON.parse(fs.readFileSync(ruta, 'utf8')); } catch { return null; }
}

function expandirCampos(paso) {
  if (!paso.campos) return [paso];
  const base = Object.fromEntries(Object.entries(paso).filter(([k]) => !['campos', 'id', 'acciones', 'vista'].includes(k)));
  const entradas = [];
  if (paso.vista) entradas.push(['0', paso.vista, null]);
  paso.campos.forEach((c, i) => entradas.push([String(i + 1), c, c.sel]));
  return entradas.map(([suf, dato, sel], n) => {
    const p = { ...base, id: `${paso.id}-${suf}` };
    p.acciones = (n === 0 ? (paso.acciones || []) : []).concat(dato.acciones || []);
    p.narracion = dato.narracion;
    p.texto_pantalla = dato.texto_pantalla;
    if (dato.al_decir) p.al_decir = dato.al_decir;
    p.resaltar = sel ? [{ sel, estilo: dato.estilo || 'caja' }] : [];
    if (n > 0) { delete p.navegar; delete p.setup; }
    return p;
  });
}

/** Acepta el nombre del módulo o una ruta a un .json. Devuelve {nombre, ruta, guion}. */
export function cargarGuion(arg) {
  let ruta = arg;
  if (!/\.json$/i.test(arg)) ruta = path.join(RAIZ, 'guiones', `${arg}.json`);
  else if (!path.isAbsolute(arg)) ruta = path.resolve(process.cwd(), arg);
  const propio = leerJson(ruta);
  if (!propio) return { nombre: path.basename(ruta, '.json'), ruta, guion: null };
  const guion = {};
  for (const capa of [leerJson(path.join(RAIZ, 'config.json')), leerJson(path.join(RAIZ, 'config.local.json')), propio]) {
    if (!capa) continue;
    for (const [k, v] of Object.entries(capa)) if (!k.startsWith('_')) guion[k] = v;
  }
  guion.pasos = (guion.pasos || []).flatMap(expandirCampos);
  return { nombre: path.basename(ruta, '.json'), ruta, guion };
}

/** Tipo de acción de una entrada de `acciones`. */
export const TIPOS = ['click', 'escribir', 'resaltar', 'subir', 'seleccionar', 'marcar',
  'click_opcional', 'presionar', 'esperar_ms', 'quitar_marca', 'plano_general'];
export const tipoDe = acc => TIPOS.find(k => k in acc) || ('al_decir' in acc ? 'ritmo' : '?');
export const selDe = acc => {
  const t = tipoDe(acc), v = acc[t];
  return typeof v === 'string' ? v : (v && typeof v === 'object' ? (v.sel || v.ancla || null) : null);
};

// ── utilidades de salida ────────────────────────────────────────────────────
export const fmt = s => {
  if (s == null || !isFinite(s)) return '  —  ';
  const m = Math.floor(s / 60), r = s - m * 60;
  return `${m}:${r.toFixed(1).padStart(4, '0')}`;
};
export const corto = (s, n = 70) => (s = String(s ?? '')).length > n ? s.slice(0, n - 1) + '…' : s;

/**
 * Tramos sin cambios de pantalla: `cambios` son intervalos [a, b] (segundos de
 * una misma línea de tiempo) en los que algo se mueve; `ini`/`fin` son los
 * bordes. Devuelve los huecos [a, b] con b - a > umbral.
 */
export function huecos(cambios, ini, fin, umbral) {
  const iv = cambios.map(([a, b]) => [Math.max(ini, a), Math.min(fin, Math.max(a, b))])
    .filter(([a, b]) => b >= a).sort((x, y) => x[0] - y[0]);
  const res = [];
  let cursor = ini;
  for (const [a, b] of iv) {
    if (a - cursor > umbral) res.push([cursor, a]);
    cursor = Math.max(cursor, b);
  }
  if (fin - cursor > umbral) res.push([cursor, fin]);
  return res;
}

// ── lectura de lo grabado (salida/<modulo>/) ────────────────────────────────
export function leerGrabacion(modulo) {
  const salida = path.join(RAIZ, 'salida', modulo);
  const segdir = path.join(salida, 'grabacion', 'segmentos');
  if (!fs.existsSync(segdir)) return null;
  const { guion } = cargarGuion(modulo);
  // orden: el del guion si existe (así se monta el video); si no, alfabético
  const ids = guion?.pasos?.length
    ? guion.pasos.map(p => p.id)
    : fs.readdirSync(segdir).filter(f => f.endsWith('.json')).map(f => f.slice(0, -5)).sort();
  const pasos = [];
  let t0 = 0;
  for (const id of ids) {
    const ruta = path.join(segdir, `${id}.json`);
    const seg = leerJson(ruta);
    if (!seg) { pasos.push({ id, falta: true, t0 }); continue; }
    const audio = leerJson(path.join(salida, 'audio', `${id}.json`)) || {};
    const paso = guion?.pasos?.find(p => p.id === id) || null;
    pasos.push({ id, seg, audio, paso, t0, mtime: fs.statSync(ruta).mtimeMs });
    t0 += seg.duracion;
  }
  return { modulo, salida, guion, pasos, total: t0 };
}

/** video.srt → [{a, b, texto}] en segundos del video final. */
export function leerSrt(ruta) {
  if (!fs.existsSync(ruta)) return [];
  const aS = x => { const [h, m, s] = x.replace(',', '.').split(':'); return +h * 3600 + +m * 60 + +s; };
  return fs.readFileSync(ruta, 'utf8').replace(/\r/g, '').split(/\n\n+/).map(b => {
    const l = b.trim().split('\n');
    const m = (l[1] || '').match(/(\S+)\s*-->\s*(\S+)/);
    return m ? { a: aS(m[1]), b: aS(m[2]), texto: l.slice(2).join(' ') } : null;
  }).filter(Boolean);
}

const DIALOGO = /dialog|snack|alert|toast|swal|modal|aviso|notif|mensaje/i;
export const esSelDialogo = s => DIALOGO.test(String(s || ''));

/** Firma de una alerta: sus primeras palabras (el título del diálogo). */
export const firmaAlerta = texto => String(texto).split(/\s+/).slice(0, 4).join(' ').toLowerCase();

/**
 * Intervalos de «pantalla cambiando» medidos sobre un segmento grabado, en
 * segundos locales del segmento. Una marca dura su `durante_ms` (del guion,
 * emparejada por orden y selector; 4,5 s si no se sabe). Una alerta cuenta
 * solo si es nueva (el mismo diálogo que sigue abierto del paso anterior no
 * mueve nada).
 */
export function cambiosDeSegmento(p, alertasPrevias = new Set()) {
  const seg = p.seg;
  if (seg.tipo === 'tarjeta') return [[0, 0.4], [seg.duracion - 0.4, seg.duracion]];
  const iv = [];
  const marcasGuion = (p.paso?.acciones || []).filter(a => 'resaltar' in a);
  const usadas = new Set();
  let ultimoClic = {};
  for (const ev of seg.eventos || []) {
    const t = ev.t;
    switch (ev.tipo) {
      case 'navegar': iv.push([t - 0.3, t + 1.5]); break;
      case 'clic': iv.push([t - MOVER - 0.05, t + 0.8]); ultimoClic[ev.que] = t; break;
      case 'escribir': iv.push([(ultimoClic[ev.que] ?? t - 0.5), t + 0.2]); break;
      case 'subir': iv.push([t - MOVER - 0.05, t + 1.0]); break;
      case 'resaltar': {
        const i = marcasGuion.findIndex((a, k) => !usadas.has(k) &&
          (typeof a.resaltar === 'string' ? a.resaltar : a.resaltar?.sel) === ev.que);
        let dur = MARCA_MS / 1000;
        if (i >= 0) { usadas.add(i); dur = (marcasGuion[i].durante_ms ?? marcasGuion[i].resaltar?.durante_ms ?? MARCA_MS) / 1000; }
        else if ((p.paso?.resaltar || []).some(m => m.sel === ev.que)) dur = seg.duracion; // esquema vista+campos
        iv.push([t - 0.3, t + dur]);
        break;
      }
      case 'alerta':
        if (!(t < 1.5 && alertasPrevias.has(ev.que))) iv.push([t - 0.3, t + 0.5]);
        break;
      default: iv.push([t - 0.3, t + 0.5]);
    }
  }
  return iv;
}

/** Huecos de imagen quieta sobre TODO el video (atraviesan los cortes entre pasos). */
export function huecosGrabados(g, umbral = HUECO_MAX) {
  const cambios = [];
  let previas = new Set();
  for (const p of g.pasos) {
    if (p.falta) continue;
    for (const [a, b] of cambiosDeSegmento(p, previas)) cambios.push([p.t0 + a, p.t0 + b]);
    previas = new Set((p.seg.eventos || []).filter(e => e.tipo === 'alerta').map(e => e.que));
  }
  return huecos(cambios, 0, g.total, umbral).map(([a, b]) => ({ a, b, dur: b - a, pasos: pasosEn(g, a, b) }));
}

export function pasosEn(g, a, b) {
  return g.pasos.filter(p => !p.falta && p.t0 < b && p.t0 + p.seg.duracion > a)
    .map(p => ({ id: p.id, a: Math.max(0, a - p.t0), b: Math.min(p.seg.duracion, b - p.t0) }));
}
