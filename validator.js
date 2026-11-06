/**
 * Spine-panel lettering validator
 * Reads CSS custom properties from :root and reports pass/WARN/ERROR
 * per the Cockerell integration contract (contract.md).
 *
 * Source: art_01M6QDBQN448XJGKMPFN7C85ES r1 (Gutenberg 26672, ch. XV)
 * License: MIT
 *
 * ASSUMPTIONS: All numeric thresholds are proposals, not Cockerell's stated values.
 * Run in a browser or inject via JSDOM for server-side use.
 */
function getCSS(prop, fallback) {
  const v = getComputedStyle(document.documentElement)
    .getPropertyValue(prop).trim();
  return v !== '' ? v : fallback;
}

function validateSpinePanel() {
  const results = [];

  // R1: fill ratio
  const fillRatio = parseFloat(getCSS('--spine-fill-ratio', '0'));
  if (fillRatio < 0.75 || fillRatio > 0.95) {
    results.push({ rule: 'R1', status: 'WARN',
      msg: `fill-ratio ${fillRatio} outside [0.75, 0.95]; adjust lettering size.` });
  } else {
    results.push({ rule: 'R1', status: 'PASS', msg: `fill-ratio ${fillRatio} OK` });
  }

  // R2: exactly 4 size steps
  const sizeSteps = getCSS('--spine-size-steps', '').split(',').filter(Boolean);
  if (sizeSteps.length !== 4) {
    results.push({ rule: 'R2', status: 'WARN',
      msg: `${sizeSteps.length} size steps defined; Cockerell says four serve every book.` });
  } else {
    results.push({ rule: 'R2', status: 'PASS', msg: '4 size steps defined.' });
  }

  // R3: mixed sizes
  const mixedSizes = getCSS('--spine-mixed-sizes', 'false') === 'true';
  const special = getCSS('--spine-special-binding', 'false') === 'true';
  if (mixedSizes) {
    results.push({ rule: 'R3', status: special ? 'WARN' : 'WARN',
      msg: 'Mixed type sizes in title; avoid when possible (Cockerell 3903-3904).' });
  } else {
    results.push({ rule: 'R3', status: 'PASS', msg: 'Single type size.' });
  }

  // R4: single font family — hard constraint
  const families = getCSS('--spine-font-families', '').split(',').filter(Boolean);
  if (families.length > 1) {
    results.push({ rule: 'R4', status: 'ERROR',
      msg: `${families.length} font families in use; Cockerell: on no account whatever (3904-3905).` });
  } else {
    results.push({ rule: 'R4', status: 'PASS', msg: 'Single font family.' });
  }

  // R5: single-word narrow spine
  const wordCount = parseInt(getCSS('--spine-word-count', '2'), 10);
  const widthIn = parseFloat(getCSS('--spine-width-in', '1'));
  if (wordCount === 1 && widthIn <= 0.625) {
    results.push({ rule: 'R5', status: 'WARN',
      msg: `One-word title on spine <= 5/8 in; likely illegible at small size (3892-3894).` });
  } else {
    results.push({ rule: 'R5', status: 'PASS', msg: 'Word-count/width combination OK.' });
  }

  // R6: orientation
  const orientation = getCSS('--spine-orientation', 'horizontal');
  if (orientation === 'vertical') {
    results.push({ rule: 'R6', status: 'WARN',
      msg: 'Vertical orientation; use only when necessary (3897-3899).' });
  } else {
    results.push({ rule: 'R6', status: 'PASS', msg: 'Horizontal orientation.' });
  }

  // R8: very thin book
  if (widthIn < 0.25) {
    results.push({ rule: 'R8', status: 'ERROR',
      msg: `Spine width ${widthIn} in < 0.25 in; consider side labelling (3914-3916). Threshold is proposed, not Cockerell's.` });
  } else {
    results.push({ rule: 'R8', status: 'PASS', msg: `Spine width ${widthIn} in OK.` });
  }

  return results;
}

// Export for Node/JSDOM
if (typeof module !== 'undefined') module.exports = { validateSpinePanel };