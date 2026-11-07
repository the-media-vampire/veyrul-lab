/**
 * preflight.js — 1894 pen-drawing rules as SVG preflight checks
 * Source: art_01M6Q6XXX3DEFQ6QST964PTW6M r1. Curator inference throughout.
 * Not executed. MIT License.
 */
'use strict';
const DEFAULTS = { drawScale:1.5, minGapPx:2, targetW:500, targetH:700, hueMin:210, hueMax:260 };

function r1(vbW, vbH, c=DEFAULTS) {
  const s = Math.min(vbW/c.targetW, vbH/c.targetH);
  if (s >= c.drawScale) return {code:'PASS', rule:'R1', detail:`scale ${s.toFixed(2)}x`};
  if (s >= 1) return {code:'WARN', rule:'R1', detail:`scale ${s.toFixed(2)}x below drawScale ${c.drawScale} (A1)`};
  return {code:'ERROR', rule:'R1', detail:'viewBox smaller than target — strokes will enlarge'};
}

function r2(elements, c=DEFAULTS) {
  const bad = elements.filter(e => e.layer==='guide' && (e.hue<c.hueMin||e.hue>c.hueMax));
  return bad.length===0
    ? {code:'PASS', rule:'R2', detail:'Guide elements in blue range'}
    : {code:'WARN', rule:'R2', detail:`${bad.length} guide element(s) outside blue hue range (A2: analogy only)`};
}

function r3(gaps, c=DEFAULTS) {
  const tight = gaps.filter(g => g<c.minGapPx);
  return tight.length===0
    ? {code:'PASS', rule:'R3', detail:`All gaps >= ${c.minGapPx}px`}
    : {code:'WARN', rule:'R3', detail:`${tight.length} gap(s) below ${c.minGapPx}px (A3: threshold not a source figure)`};
}

function r4(layers) {
  return layers.includes('sketch')
    ? {code:'ERROR', rule:'R4', detail:'Sketch layer present — strip before export (A4: inference)'}
    : {code:'PASS', rule:'R4', detail:'No sketch layer in export'};
}

function runPreflight({vbW, vbH, elements, gaps, layers}, cfg) {
  const results = [r1(vbW,vbH,cfg), r2(elements,cfg), r3(gaps,cfg), r4(layers)];
  return {passed: results.every(r=>r.code==='PASS'), results};
}

module.exports = {runPreflight, r1, r2, r3, r4, DEFAULTS};