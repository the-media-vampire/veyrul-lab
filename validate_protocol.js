#!/usr/bin/env node
// validate_protocol.js — reads a check_cursor_sync output JSON and
// enforces the thresholds from run_protocol.json.
// Usage: node validate_protocol.js <sync_result.json> <phase_label>
// Exit: 0 = PASS, 1 = FAIL, 2 = INPUT ERROR
// Source only; no browser execution performed.
// Source: art_01M6SQCKMHR4X6A3P84EPKAT0J rev 1
'use strict';
const fs = require('fs');
const path = require('path');

const [,, resultFile, phaseLabel] = process.argv;
if (!resultFile) {
  console.error('INPUT ERROR: usage: node validate_protocol.js <sync_result.json> [phase_label]');
  process.exit(2);
}

let protocol, result;
try {
  protocol = JSON.parse(fs.readFileSync(path.join(__dirname, 'run_protocol.json'), 'utf8'));
} catch (e) {
  console.error('INPUT ERROR: cannot read run_protocol.json:', e.message);
  process.exit(2);
}
try {
  result = JSON.parse(fs.readFileSync(resultFile, 'utf8'));
} catch (e) {
  console.error('INPUT ERROR: cannot read', resultFile, ':', e.message);
  process.exit(2);
}

// Expected fields from check_cursor_sync output
const { total, sync_ok, sync_fail, late_draw } = result;
if ([total, sync_ok, sync_fail, late_draw].some(v => typeof v !== 'number')) {
  console.error('INPUT ERROR: sync_result.json must contain numeric fields: total, sync_ok, sync_fail, late_draw');
  process.exit(2);
}

const { late_draw_max_pct, sync_fail_max_count } = protocol.thresholds;
const late_draw_pct = total > 0 ? (late_draw / total) * 100 : 0;
const label = phaseLabel || resultFile;

console.log(`\nPhase: ${label}`);
console.log(`  total entries : ${total}`);
console.log(`  SYNC_OK       : ${sync_ok}`);
console.log(`  SYNC_FAIL     : ${sync_fail}  (max allowed: ${sync_fail_max_count})`);
console.log(`  LATE_DRAW     : ${late_draw}  (${late_draw_pct.toFixed(1)}%  max allowed: ${late_draw_max_pct}%)`);

const failures = [];
if (sync_fail > sync_fail_max_count)
  failures.push(`SYNC_FAIL ${sync_fail} > ${sync_fail_max_count}`);
if (late_draw_pct > late_draw_max_pct)
  failures.push(`LATE_DRAW ${late_draw_pct.toFixed(1)}% > ${late_draw_max_pct}%`);

if (failures.length === 0) {
  console.log('  Result: PASS');
  process.exit(0);
} else {
  console.log('  Result: FAIL —', failures.join('; '));
  console.log('  Action: do NOT proceed to ramp phases. Diagnose render load before next run.');
  process.exit(1);
}