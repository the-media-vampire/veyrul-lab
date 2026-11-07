# Step sequencer timing-protocol runner

Source: `art_01M6SQCKMHR4X6A3P84EPKAT0J` rev 1  
Extends: Scout artifact `c0094c0f-5f21-4361-9390-c404862fad2f` (`check_cursor_sync.js`)

## What this adds

`run_protocol.json` encodes the **phase order** and **numeric thresholds** missing from earlier proposals:  
- Stable-BPM baseline (phases 1–2) must pass before ramp phases (3–4) are reached.  
- `LATE_DRAW` tolerance is set to ≤ 5 % of log entries (adjustable in the JSON).  
- `SYNC_FAIL` tolerance is 0 — any step mismatch is a hard stop.  

`validate_protocol.js` reads a `check_cursor_sync.js` output file and exits 0/1/2.  
It does **not** replace `check_times.js` from the article; run both.

## Canonical run order

```
# Phase 1 — Treatment A, 120 BPM, 8 bars, no ramp
node check_cursor_sync.js log_A_stable.json > result_A_stable.json
node validate_protocol.js result_A_stable.json "Phase 1 — A stable"  # must exit 0
node check_times.js log_A_stable.json

# Phase 2 — Treatment B, 120 BPM, 8 bars, no ramp
node check_cursor_sync.js log_B_stable.json > result_B_stable.json
node validate_protocol.js result_B_stable.json "Phase 2 — B stable"  # must exit 0
node check_times.js log_B_stable.json

# Phases 3-4 only if phases 1 and 2 both exit 0
node check_cursor_sync.js log_A_ramp.json > result_A_ramp.json
node validate_protocol.js result_A_ramp.json "Phase 3 — A ramp"
node check_cursor_sync.js log_B_ramp.json > result_B_ramp.json
node validate_protocol.js result_B_ramp.json "Phase 4 — B ramp"
```

## Separation of outcomes (from Iris's brief)

| Output | Instrument | Separation |
|---|---|---|
| Audio timing | `check_times.js` | Independent of cursor |
| Cursor sync | `check_cursor_sync.js` | Independent of audio |
| Protocol gate | `validate_protocol.js` | Reads cursor-sync result |
| Viewer ID errors | Paper log | Collected separately from preference |
| Viewer preference | Paper log | Never treated as timing evidence |

## No execution
No browser execution was performed. All files are source only.