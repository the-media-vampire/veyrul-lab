// Morris 1895 spacing — CSS constraint validator
// Source: art_01M6Q9V6AWKE9BM6MDAGT34K8V r1. MIT.
// Assumptions A1–A5 in README.md apply.
function validateSpacing(root) {
  const s = getComputedStyle(root || document.documentElement);
  const get = k => s.getPropertyValue(k).trim();
  const out = [];
  // R1 letter-fit (A1)
  const lf = parseFloat(get('--letter-fit') || '0');
  out.push({ rule:'R1 letter-fit', src:'136,138', status: lf<=0?'PASS':'WARN',
    note:'A1: 0=neutral, no source measurement' });
  // R2 word-spacing (A2)
  const ws = get('--word-spacing'); const tok = ws.split(/\s+/).filter(Boolean);
  out.push({ rule:'R2 word-spacing', src:'138-143', status: tok.length===1?'PASS':'WARN',
    note:'A2: rivers require layout engine, only non-uniform tokens flagged' });
  // R3 line-leading (A3)
  const ll = parseFloat(get('--line-leading') || '1');
  out.push({ rule:'R3 line-leading', src:'145-151',
    status: ll>1.5?'ERROR':ll>1.2?'WARN':'PASS',
    note:'A3: 1.2 ceiling proposed from thin/hair language, not a source number' });
  // R4 margin-order (A4)
  const mv = get('--margin-order').split(/\s+/).map(Number);
  const [i,t,o,b] = mv;
  const ok = mv.length===4 && mv.every(n=>!isNaN(n)) && i<=t && t<=o && o<=b;
  out.push({ rule:'R4 margin-order', src:'152-157',
    status: mv.length!==4||mv.some(isNaN)?'WARN':ok?'PASS':'ERROR',
    note:'A4: 20% report (158-161) has no base, not encoded' });
  return out;
}
if (typeof module!=='undefined') module.exports={validateSpacing};