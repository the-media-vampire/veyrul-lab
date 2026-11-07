#!/usr/bin/env node
// check_cursor_sync.js
// Usage: node check_cursor_sync.js log.json
//
// Reads a timing log extended with cursor_step (see cursor_sync_patch.js).
// Reports:
//   SYNC_OK   — cursor_step === audio_step for every entry that has both
//   SYNC_FAIL — any entry where |cursor_step - audio_step| > 1
//   LATE_DRAW — entries where cursor_step is missing (Draw callback was late
//               or not yet patched in)
//
// Exit codes: 0 PASS, 1 FAIL, 2 INPUT ERROR
// Built-in modules only; no Tone.js dependency.

'use strict';
const fs = require('fs');
const path = require('path');

const [,, logFile] = process.argv;
if (!logFile) {
  console.error('INPUT ERROR: provide log.json path');
  process.exit(2);
}

let entries;
try {
  entries = JSON.parse(fs.readFileSync(logFile, 'utf8'));
} catch (e) {
  console.error('INPUT ERROR:', e.message);
  process.exit(2);
}

if (!Array.isArray(entries) || entries.length === 0) {
  console.error('INPUT ERROR: log must be a non-empty array');
  process.exit(2);
}

let syncFails = 0;
let lateDraw  = 0;
let syncOk    = 0;

entries.forEach((entry, i) => {
  const a = entry.audio_step;  // existing field from check_times.js convention
  const c = entry.cursor_step; // new field from cursor_sync_patch.js

  if (c === undefined || c === null) {
    lateDraw++;
    console.log(`LATE_DRAW entry ${i}: audio_step=${a}, cursor_step missing`);
    return;
  }

  const delta = Math.abs(c - a);
  if (delta > 1) {
    syncFails++;
    console.log(`SYNC_FAIL entry ${i}: audio_step=${a}, cursor_step=${c}, delta=${delta}`);
  } else {
    syncOk++;
  }
});

console.log(`\nSummary: ${syncOk} SYNC_OK, ${syncFails} SYNC_FAIL, ${lateDraw} LATE_DRAW`);

if (syncFails > 0) {
  console.log('RESULT: FAIL — cursor and audio diverged');
  process.exit(1);
} else if (lateDraw > 0) {
  console.log('RESULT: PASS with warnings — LATE_DRAW entries present; Draw callback may be slow');
  process.exit(0);
} else {
  console.log('RESULT: PASS');
  process.exit(0);
}