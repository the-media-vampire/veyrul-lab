/* MacKellar punct spacing — source: art_01M6Q2PGM0RAKG2T790AEWR19C rev 1, lines 4601-4603
   Comma→thick space after; semicolon/colon→hair before+en after; full stop→em after.
   Unicode approximations only. All mappings are INFERENCE. Modifies text nodes. */
(function(){
  var EN='\u2002', HAIR='\u200A', EM='\u2003';
  var rules=[
    {re:/([,])\s/g,   rep:'$1'+EN},
    {re:/([;:])\s/g,  rep:HAIR+'$1'+EN},
    {re:/([.?!])\s/g, rep:'$1'+EM}
  ];
  function fix(node){
    var t=node.nodeValue;
    rules.forEach(function(r){t=t.replace(r.re,r.rep);});
    node.nodeValue=t;
  }
  function walk(el){
    el.childNodes.forEach(function(c){
      if(c.nodeType===3)fix(c);
      else if(c.nodeType===1&&!/^(SCRIPT|STYLE|CODE|PRE)$/.test(c.tagName))walk(c);
    });
  }
  document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('p,li').forEach(walk);
  });
}());