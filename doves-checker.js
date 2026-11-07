/**
 * doves-checker.js
 * Machine-readable console linter for Forge's Doves Press integration artifact
 * (artifact 43f89ab4-3ac0-44df-956d-c5fce5e38d67, commit f7c35ce8f57d85404c45d3aec1a335ec7d7d825e).
 *
 * Rules derived from art_01M6Q5QTJRQ9WJC3YF38BTTBYE rev 1:
 *   R1 (file lines 221–222): img border present + all margins >= body font-size
 *   R2 (file line 227): illustration width <= 70% of its offsetParent column width
 *   R3 (file lines 199, 202): verse element is display:block with white-space:pre or pre-wrap
 *
 * Usage: paste into browser console while corrected.html or baseline.html is open,
 *        or add <script src="doves-checker.js"></script> before </body>.
 *
 * Limits:
 *   - R2 uses offsetParent width; nested flex/grid containers may differ from text column.
 *   - R1 margin threshold uses body font-size in px; rem/em computed values are resolved.
 *   - "Same texture as the type" (line 221) is a craft judgment; not machine-checkable.
 *   - Source published, not executed. Results are only valid after browser rendering.
 */

(function dovesCheck() {
  const results = [];
  const bodyFontSizePx = parseFloat(getComputedStyle(document.body).fontSize);

  /* ---- R1: illustration border and margin ---- */
  document.querySelectorAll('img').forEach((img, i) => {
    const cs = getComputedStyle(img);
    const hasBorder = parseFloat(cs.borderTopWidth) > 0
                   || parseFloat(cs.borderRightWidth) > 0
                   || parseFloat(cs.borderBottomWidth) > 0
                   || parseFloat(cs.borderLeftWidth) > 0;
    const marginOk = ['marginTop','marginRight','marginBottom','marginLeft']
      .every(p => parseFloat(cs[p]) >= bodyFontSizePx);
    results.push({
      rule: 'R1',
      element: img.className || `img[${i}]`,
      pass: hasBorder && marginOk,
      detail: `border=${hasBorder}, margins>=${bodyFontSizePx}px: ${marginOk}`
    });
  });

  /* ---- R2: illustration width <= 70% of column ---- */
  document.querySelectorAll('img').forEach((img, i) => {
    const colWidth = (img.offsetParent || document.body).clientWidth;
    const ratio = colWidth > 0 ? img.offsetWidth / colWidth : null;
    results.push({
      rule: 'R2',
      element: img.className || `img[${i}]`,
      pass: ratio !== null && ratio <= 0.70,
      detail: ratio !== null
        ? `${(ratio*100).toFixed(1)}% of column (${colWidth}px)`
        : 'could not measure column width'
    });
  });

  /* ---- R3: verse block and white-space ---- */
  document.querySelectorAll('.verse, blockquote, pre').forEach((el, i) => {
    const cs = getComputedStyle(el);
    const isBlock = cs.display === 'block' || cs.display === 'flex';
    const wsOk = cs.whiteSpace === 'pre' || cs.whiteSpace === 'pre-wrap';
    results.push({
      rule: 'R3',
      element: el.className || el.tagName.toLowerCase() + `[${i}]`,
      pass: isBlock && wsOk,
      detail: `display=${cs.display}, white-space=${cs.whiteSpace}`
    });
  });

  /* ---- Report ---- */
  const passed = results.filter(r => r.pass).length;
  const total  = results.length;
  console.group(`Doves Press Checker — ${passed}/${total} checks passed`);
  results.forEach(r => {
    const fn = r.pass ? console.log : console.warn;
    fn(`[${r.pass ? 'PASS' : 'FAIL'}] ${r.rule} | ${r.element} | ${r.detail}`);
  });
  if (total === 0) console.warn('No matching elements found. Check selectors.');
  console.groupEnd();

  return results; // structured data for programmatic use
})();