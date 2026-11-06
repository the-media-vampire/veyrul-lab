/**
 * Colour Harmony Validator (untested proposal)
 * Source: art_01M6QDZ8PTSJH0WF5DH44GFVFZ r1
 */
function readVar(n){
  return getComputedStyle(document.documentElement).getPropertyValue(n).trim();
}
function hueDiff(a,b){const d=Math.abs(a-b)%360;return d>180?360-d:d;}

export function validateHarmonyContract(){
  const r=[];
  const aS=parseFloat(readVar('--ch-accent-sat-max'));
  const gS=parseFloat(readVar('--ch-ground-sat-max'));
  r.push({rule:'saturation-moderation',pass:aS<=85&&gS<=35,
    note:`accent=${aS}% ground=${gS}%`,lines:'3070-3080'});

  const dH=parseFloat(readVar('--ch-dominant-hue'));
  r.push({rule:'dominant-light',pass:!isNaN(dH),
    note:`hue=${dH}deg`,lines:'3155-3174'});

  const pA=parseFloat(readVar('--ch-pair-a-hue'));
  const pB=parseFloat(readVar('--ch-pair-b-hue'));
  const pd=hueDiff(pA,pB);
  r.push({rule:'complementary-pair',pass:pd>=150&&pd<=210,
    note:`diff=${pd}deg`,lines:'3087-3090'});

  const off=parseFloat(readVar('--ch-near-complement-offset'));
  r.push({rule:'near-complement-offset',pass:off>0&&off<=45,
    note:`offset=${off}deg`,lines:'3109-3114'});

  const tA=parseFloat(readVar('--ch-triad-a-hue'));
  const tB=parseFloat(readVar('--ch-triad-b-hue'));
  const tC=parseFloat(readVar('--ch-triad-c-hue'));
  r.push({rule:'three-colour-balance',
    pass:hueDiff(tA,tB)>=90&&hueDiff(tB,tC)>=90&&hueDiff(tA,tC)>=90,
    note:`${tA}/${tB}/${tC}deg`,lines:'3116-3124'});

  return r;
}
// console.table(validateHarmonyContract());