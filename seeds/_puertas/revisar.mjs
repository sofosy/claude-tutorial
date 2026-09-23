#!/usr/bin/env node
// Puerta ANTES de grabar: predice la línea de tiempo de cada paso a partir del
// guion (voz a 3,0 palabras/s) y aplica las reglas de ritmo y sincronía.
//
//   node seeds/_puertas/revisar.mjs <modulo|ruta.json> [...] [--wps=3.0] [--audio]
//
//   --wps=N   palabras por segundo de la voz (por defecto 3,0)
//   --audio   si salida/<modulo>/audio/<paso>.json existe y cuadra con la
//             narración, usa los tiempos REALES de cada palabra
//
// Sale con código 1 si hay algún ERROR.
import fs from 'node:fs';
import path from 'node:path';
import {
  RAIZ, PAD, ADELANTO, ANTICIPO, ANTICIPO_MARCA, TECLEO, MARCA_MS, HUECO_MAX,
  cargarGuion, tokens, posiciones, tipoDe, selDe, fmt, corto, huecos,
} from './comun.mjs';

const args = process.argv.slice(2);
const WPS = Number((args.find(a => a.startsWith('--wps=')) || '--wps=3').slice(6)) || 3;
const USAR_AUDIO = args.includes('--audio');
const modulos = args.filter(a => !a.startsWith('--'));
if (!modulos.length) {
  console.error('uso: node seeds/_puertas/revisar.mjs <modulo|ruta.json> [...] [--wps=3.0] [--audio]');
  process.exit(2);
}

const PASO_MAX = 120, VIDEO_MIN = 90, VIDEO_MAX = 250;
const BOTON_QUE_CAMBIA = /guardar|crear|abrir|save|create|submit|open|nuev|registrar|confirmar|aceptar|continuar|siguiente|enviar/i;
const ZONA_FAB = /chatbot|\bfab\b|-fab|paginator|footer/i;

/** Tag del último compuesto de un selector («.x tbody tr:nth-child(2)» → «tr»). */
function ultimoTag(sel) {
  const partes = String(sel).replace(/:has(-text)?\([^)]*\)/g, '').trim().split(/\s*[>+~]\s*|\s+/).filter(Boolean);
  const m = (partes.at(-1) || '').match(/^[a-z][a-z0-9-]*/i);
  return m ? m[0].toLowerCase() : '';
}

/** Tiempos de palabra: estimados (WPS) o reales (sidecar de audio). */
function tiemposDe(modulo, paso, extra) {
  const dichas = tokens(paso.narracion || '', extra);
  const est = { dichas, t: dichas.map((_, i) => 0.1 + i / WPS), voz: dichas.length / WPS + 0.2, fuente: `${WPS} p/s` };
  if (!USAR_AUDIO) return est;
  try {
    const a = JSON.parse(fs.readFileSync(path.join(RAIZ, 'salida', modulo, 'audio', `${paso.id}.json`), 'utf8'));
    if (a.palabras?.length === dichas.length) return { dichas, t: a.palabras.map(p => p.t), voz: a.duracion, fuente: 'audio real' };
  } catch { /* sin audio: estimación */ }
  return est;
}

function revisarGuion(arg) {
  const { nombre, ruta, guion } = cargarGuion(arg);
  if (!guion) { console.log(`\n✗ ${arg}: no existe o no se puede leer ${ruta}`); return { errores: 1, avisos: 0 }; }
  const extra = guion.pronunciacion;
  const hallazgos = []; // {nivel, paso, texto}
  const H = (nivel, paso, texto) => hallazgos.push({ nivel, paso, texto });
  const pasosSim = [];
  const cambiosGlobales = [];
  let t0 = 0;

  console.log(`\n═══ ${nombre}  (${guion.titulo || 'sin título'})`);

  // marcas que siguen encendidas al pasar de un paso a otro (el temporizador
  // del motor corre sobre el reloj del maestro, no del paso)
  let marcasVivas = [];

  guion.pasos.forEach((paso, ip) => {
    const pid = paso.id;
    if (paso.tarjeta) {
      const dur = tokens(paso.narracion || '').length / WPS + 0.2 + PAD;
      console.log(`\n── ${pid}  tarjeta · ${dur.toFixed(1)} s · desde ${fmt(t0)}`);
      cambiosGlobales.push([t0, t0 + 0.4], [t0 + dur - 0.4, t0 + dur]);
      pasosSim.push({ id: pid, t0, fin: dur });
      t0 += dur; marcasVivas = [];
      return;
    }
    const W = tiemposDe(nombre, paso, extra);
    const linea = [];      // {t, tipo, que, palabra, tp}
    const cambios = [];    // intervalos locales
    const pulsados = new Set();
    let now = 0;
    let finTecleo = null;
    let ultimaMarca = null;
    const usadas = new Set();

    // un ancla se busca como en grabar._esperar_palabra: la primera aparición
    // posterior a (reloj + anticipo − 0,3); si no hay, el motor toma la
    // primera de todas (ya pasada) y dispara al instante
    const anclar = (clave, anticipo, que) => {
      if (clave == null) return null;
      if (typeof clave === 'number') return { t: clave, palabra: `${clave}s` };
      const pos = posiciones(W.dichas, clave, extra);
      if (!pos.length) { H('ERROR', pid, `al_decir «${clave}» (${que}) no está en la narración: el motor la dispara al inicio`); return null; }
      if (pos.length > 1) H('ERROR', pid, `al_decir «${clave}» (${que}) aparece ${pos.length} veces en la narración: ancla ambigua`);
      const desde = now + anticipo - 0.3;
      let i = pos.find(k => W.t[k] >= desde);
      if (i === undefined) {
        i = pos[0];
        H('ERROR', pid, `al_decir «${clave}» (${que}) ya pasó o la gastó un ancla anterior: la voz la dice a ${W.t[i].toFixed(1)} s y el reloj ya va en ${now.toFixed(1)} s`);
      } else if (usadas.has(i)) {
        H('ERROR', pid, `al_decir «${clave}» (${que}) reutiliza la palabra de un ancla anterior`);
      }
      usadas.add(i);
      return { t: W.t[i], palabra: clave };
    };

    // navegación
    if (paso.navegar) {
      marcasVivas = []; // el motor limpia la marca al navegar
      const a = anclar(paso.al_decir_navegar, ANTICIPO, 'navegar');
      const s = a ? Math.max(ADELANTO, a.t - ANTICIPO) : ADELANTO;
      linea.push({ t: s + 0.3, tipo: 'navegar', que: paso.navegar, palabra: a?.palabra, tp: a?.t });
      cambios.push([s, s + 1.8]);
      now = s + 0.8;
    }
    // marcas del paso anterior que siguen encendidas
    for (const [a, b] of marcasVivas) cambios.push([a - t0, b - t0]);

    const acciones = paso.acciones || [];
    acciones.forEach((acc, ia) => {
      const tipo = tipoDe(acc);
      const sel = selDe(acc);
      const esClic = ['click', 'escribir', 'marcar', 'click_opcional', 'subir', 'seleccionar'].includes(tipo);
      const anticipo = tipo === 'resaltar' ? ANTICIPO_MARCA : ANTICIPO;

      if (tipo === 'esperar_ms') {
        const sig = acciones.slice(ia + 1).find(x => tipoDe(x) !== 'esperar_ms');
        if (sig && sig.al_decir != null) H('ERROR', pid, `esperar_ms ${acc.esperar_ms} delante de «${corto(selDe(sig) || tipoDe(sig), 50)}» que tiene al_decir: retrasa la acción respecto a su palabra`);
        now += acc.esperar_ms / 1000;
        return;
      }
      if (tipo === '?') { H('ERROR', pid, `acción desconocida: ${corto(JSON.stringify(acc), 80)}`); return; }

      const a = anclar(acc.al_decir, anticipo, `${tipo} ${corto(sel || '', 40)}`);
      if (a && finTecleo != null && a.t < finTecleo + 2 && tipo !== 'ritmo')
        H('ERROR', pid, `R2: «${acc.al_decir}» (${a.t.toFixed(1)} s) cae antes de que termine el tecleo anterior + 2 s (${(finTecleo + 2).toFixed(1)} s)`);
      let s = a ? Math.max(now, a.t - anticipo) : (ia === 0 && !paso.navegar ? Math.max(now, ADELANTO) : now);
      if (!a && acc.al_decir != null && typeof acc.al_decir !== 'number') s = Math.max(now, 0);

      if (tipo === 'resaltar' && sel) {
        if (pulsados.has(sel)) H('ERROR', pid, `resaltar sobre «${corto(sel, 50)}», que este mismo paso ya pulsó: la marca llega tarde sobre algo ya usado (o que ya no está en pantalla)`);
        const tag = ultimoTag(sel);
        if (['table', 'tbody', 'mat-table'].includes(tag)) H('ERROR', pid, `R5b: resaltar sobre la tabla entera «${corto(sel, 50)}»: señala una celda o fila concreta`);
        if (['tr', 'mat-row'].includes(tag)) H('AVISO', pid, `resaltar sobre una fila entera «${corto(sel, 50)}»: en tabla ancha sale cortada; prefiere la celda (td:nth-child)`);
      }
      if ((esClic || tipo === 'resaltar') && sel && ZONA_FAB.test(sel))
        H('AVISO', pid, `${tipo} sobre «${corto(sel, 50)}»: zona inferior derecha, puede quedar bajo el .chatbot-fab`);

      let te = s;
      switch (tipo) {
        case 'click': case 'marcar': case 'click_opcional': case 'seleccionar': {
          te = s + ANTICIPO - 0.04;
          cambios.push(BOTON_QUE_CAMBIA.test(sel || '') || /^a[\s[.:]|routerlink/i.test(sel || '') ? [te - 0.6, te + 2] : [te - 0.6, te + 0.8]);
          now = te + 0.18;
          if (sel) pulsados.add(sel);
          break;
        }
        case 'escribir': {
          te = s + ANTICIPO - 0.04;
          const txt = String(acc.escribir?.texto ?? '');
          finTecleo = te + 0.18 + 0.1 + txt.length * TECLEO * 1.1;
          cambios.push([te - 0.6, finTecleo]);
          now = finTecleo + 0.15;
          if (sel) pulsados.add(sel);
          break;
        }
        case 'subir': {
          te = s + ANTICIPO - 0.04;
          cambios.push([te - 0.6, te + 2]);
          now = te + 0.2;
          if (acc.subir?.ancla) pulsados.add(acc.subir.ancla);
          break;
        }
        case 'resaltar': {
          te = s + 0.3;
          const dur = (acc.durante_ms ?? acc.resaltar?.durante_ms ?? MARCA_MS) / 1000;
          if (ultimaMarca && te < ultimaMarca.fin - 0.05)
            H('AVISO', pid, `dos marcas a la vez: «${corto(sel, 40)}» (${te.toFixed(1)} s) se enciende antes de que se apague «${corto(ultimaMarca.sel, 40)}» (${ultimaMarca.fin.toFixed(1)} s); la primera se corta`);
          ultimaMarca = { sel, fin: te + dur };
          cambios.push([te, te + dur]);
          now = te + (acc.cursor === false ? 0.05 : 0.61);
          break;
        }
        case 'presionar': te = s + 0.05; cambios.push([te, te + 0.5]); now = te + 0.1; break;
        case 'quitar_marca': te = s; if (ultimaMarca) { ultimaMarca.fin = Math.min(ultimaMarca.fin, te); } now = s; break;
        case 'plano_general': case 'ritmo': te = s; now = s; break;
      }
      if (tipo === 'quitar_marca') {
        // recorta la marca encendida
        for (const c of cambios) if (c[1] > te && c[0] < te) c[1] = te;
      }
      if (tipo !== 'ritmo') linea.push({ t: te, tipo, que: sel || '', palabra: a?.palabra, tp: a?.t });
    });

    // esperar (selector) a nivel de paso
    if (paso.esperar) {
      const clics = acciones.filter(x => ['click', 'marcar', 'click_opcional'].includes(tipoDe(x)));
      if (clics.length) {
        const grave = paso.navegar || clics.some(x => BOTON_QUE_CAMBIA.test(selDe(x) || ''));
        H(grave ? 'ERROR' : 'AVISO', pid, `R1/R24: \`esperar\` «${corto(paso.esperar, 40)}» en un paso con clics: si el clic cambia de pantalla y el selector no llega, el motor REPITE las acciones`);
      }
    }
    if (paso.pausa_ms) now += paso.pausa_ms / 1000;

    // esquema antiguo: una marca fija por paso
    if (paso.resaltar?.length) {
      const a = anclar(paso.al_decir, ANTICIPO_MARCA, 'marca del paso');
      const te = (a ? Math.max(now, a.t - ANTICIPO_MARCA) : now) + 0.3;
      linea.push({ t: te, tipo: 'resaltar', que: paso.resaltar[0].sel, palabra: a?.palabra, tp: a?.t });
      cambios.push([te, 1e9]);
      now = te + 0.61;
    }

    const fin = Math.max(W.voz + PAD, now + 0.2);
    if (fin > PASO_MAX) H('AVISO', pid, `paso de ${fin.toFixed(0)} s (> ${PASO_MAX} s): pártelo en dos tareas`);
    if (now > W.voz + PAD + 0.3) H('AVISO', pid, `las acciones terminan ${(now - W.voz - PAD).toFixed(1)} s después de la voz: silencio al final`);

    // imprimir la línea de tiempo del paso
    console.log(`\n── ${pid}  voz ${W.voz.toFixed(1)} s (${W.fuente}) · paso ${fin.toFixed(1)} s · desde ${fmt(t0)}`);
    for (const e of linea.sort((x, y) => x.t - y.t)) {
      const pal = e.palabra != null ? `  «${corto(e.palabra, 24)}» ${e.tp != null ? `@${e.tp.toFixed(1)}` : ''}` : '';
      console.log(`   ${e.t.toFixed(1).padStart(6)} s  ${e.tipo.padEnd(13)} ${corto(e.que, 55)}${pal}`);
    }

    for (const [a, b] of cambios) cambiosGlobales.push([t0 + a, t0 + Math.min(b, 1e8)]);
    // las marcas que siguen vivas al terminar el paso pasan al siguiente
    marcasVivas = cambios.filter(([a, b]) => b > fin && b < 1e8).map(([a, b]) => [t0 + fin, t0 + b]);
    pasosSim.push({ id: pid, t0, fin });
    t0 += fin;
  });

  // R0 sobre el video entero: un hueco puede atravesar el corte entre pasos
  const total = t0;
  for (const [a, b] of huecos(cambiosGlobales.map(([x, y]) => [x, Math.min(y, total)]), 0, total, HUECO_MAX)) {
    const en = pasosSim.filter(p => p.t0 < b && p.t0 + p.fin > a)
      .map(p => `${p.id} ${Math.max(0, a - p.t0).toFixed(1)}–${Math.min(p.fin, b - p.t0).toFixed(1)} s`);
    H('ERROR', en.length > 1 ? 'entre pasos' : (en[0] || '').split(' ')[0],
      `R0: ${(b - a).toFixed(1)} s sin que la pantalla cambie (${fmt(a)}–${fmt(b)} del video; ${en.join(' + ')}). Añade una marca, estira un durante_ms o acorta la narración`);
  }

  // siglas sin explicar la primera vez
  const vistas = new Set();
  for (const paso of guion.pasos) {
    const frases = String(paso.narracion || '').split(/(?<=[.!?…])\s+/);
    for (const f of frases) {
      for (const m of f.matchAll(/(?<![\p{L}\p{N}])[A-ZÁÉÍÓÚÑ]{2,}[0-9]*(?![\p{L}\p{N}])/gu)) {
        const s = m[0];
        if (vistas.has(s)) continue;
        vistas.add(s);
        if (!/(^|[^\p{L}])(es|son|significa|o sea)([^\p{L}]|$)|\(|—/iu.test(f))
          H('AVISO', paso.id, `sigla «${s}» sin explicar la primera vez que se dice («${corto(f.trim(), 70)}»)`);
      }
    }
  }

  const primero = guion.pasos.find(p => !p.tarjeta);
  if (primero && !(primero.acciones || []).some(a => a.click === 'button.panel-collapse'))
    H('AVISO', primero.id, 'el primer paso no contrae el menú (click a «button.panel-collapse»): la pantalla sale estrecha');
  if (total < VIDEO_MIN || total > VIDEO_MAX)
    H('AVISO', 'guion', `duración prevista ${fmt(total)} fuera del rango 1:30–4:10`);

  console.log(`\n   Duración prevista: ${fmt(total)}`);
  const errores = hallazgos.filter(h => h.nivel === 'ERROR');
  const avisos = hallazgos.filter(h => h.nivel === 'AVISO');
  for (const h of [...errores, ...avisos]) console.log(`   ${h.nivel.padEnd(5)} [${h.paso}] ${h.texto}`);
  if (!hallazgos.length) console.log('   sin hallazgos');
  console.log(`   → ${errores.length} ERROR · ${avisos.length} AVISO`);
  return { errores: errores.length, avisos: avisos.length };
}

let E = 0, A = 0;
for (const m of modulos) { const r = revisarGuion(m); E += r.errores; A += r.avisos; }
console.log(`\nResumen: ${modulos.length} guion(es) · ${E} ERROR · ${A} AVISO → ${E ? 'NO GRABAR' : 'LISTO PARA GRABAR'}`);
process.exit(E ? 1 : 0);
