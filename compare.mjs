import fs from 'node:fs';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';

const hex = /^#[0-9a-f]{6}$/i;
const keys = (o, wanted) => o && typeof o === 'object' && !Array.isArray(o) && Object.keys(o).sort().join('|') === [...wanted].sort().join('|');
export function validate(doc) {
  if (!keys(doc, ['schema','source','cases']) || doc.schema !== 'colour-comparison/v1') throw Error('schema');
  if (!keys(doc.source, ['id','revision']) || doc.source.id !== 'art_01M6QDZ8PTSJH0WF5DH44GFVFZ' || doc.source.revision !== 1) throw Error('source');
  if (!Array.isArray(doc.cases) || doc.cases.length !== 3) throw Error('three cases required');
  const ids = new Set();
  for (const c of doc.cases) {
    if (!keys(c, ['id','ground','accent','accentArea']) || typeof c.id !== 'string' || !/^[a-z][a-z0-9-]{0,39}$/.test(c.id) || ids.has(c.id)) throw Error('case id');
    ids.add(c.id);
    if (!hex.test(c.ground) || !hex.test(c.accent)) throw Error('six-digit sRGB hex required');
    if (typeof c.accentArea !== 'number' || !Number.isFinite(c.accentArea) || c.accentArea <= 0 || c.accentArea >= 1) throw Error('area must be strictly between zero and one');
  }
  const [a,b,c] = doc.cases;
  if (a.ground !== b.ground || a.accent !== b.accent || a.accentArea === b.accentArea) throw Error('pair 1 must change area only');
  if (a.ground !== c.ground || a.accentArea !== c.accentArea || a.accent === c.accent) throw Error('pair 2 must change accent colour only');
  return {structure:'valid', harmony:'unassessed', calibration:'illustrative display colours only'};
}
export function render(doc) {
  const result = validate(doc);
  return '<!doctype html><meta charset="utf-8"><title>Colour comparison</title>' +
    '<style>body{font:16px system-ui;margin:2rem}section{display:inline-block;margin:1rem}.panel{width:280px;height:180px;background:var(--ground)}.accent{height:100%;width:var(--area);background:var(--accent)}</style>' +
    '<h1>Illustrative comparison, not a harmony test</h1><p>Structure: '+result.structure+'; harmony: '+result.harmony+'. Compare case 1 with case 2 for area, and case 1 with case 3 for accent colour. No preference is predicted.</p>' +
    doc.cases.map(c => '<section><h2>'+c.id+'</h2><div class="panel" aria-label="decorative comparison swatch" style="--ground:'+c.ground+';--accent:'+c.accent+';--area:'+(c.accentArea*100)+'%"><div class="accent"></div></div><p>Accent area: '+c.accentArea+'; accent: '+c.accent+'</p></section>').join('');
}
function selfTest() {
  const d = JSON.parse(fs.readFileSync(new URL('./sample.json', import.meta.url), 'utf8'));
  assert.equal(validate(d).harmony, 'unassessed');
  for (const value of [0,1,-1,NaN,Infinity,'0.1']) {
    const bad = structuredClone(d); bad.cases[0].accentArea = value;
    assert.throws(() => validate(bad));
  }
  const invalid = structuredClone(d); invalid.cases[0].accent = 'red;display:none';
  assert.throws(() => validate(invalid));
  const confounded = structuredClone(d); confounded.cases[1].accent = '#ffffff';
  assert.throws(() => validate(confounded));
  const duplicate = structuredClone(d); duplicate.cases[1].id = duplicate.cases[0].id;
  assert.throws(() => validate(duplicate));
  assert.ok(render(d).includes('harmony: unassessed'));
  console.log('Structural tests passed; no perceptual tests performed.');
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv[2] === '--self-test') selfTest();
  else process.stdout.write(render(JSON.parse(fs.readFileSync(process.argv[2] || new URL('./sample.json', import.meta.url), 'utf8'))));
}