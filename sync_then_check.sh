#!/usr/bin/env bash
# sync_then_check.sh — sample adapter (NOT EXECUTED; illustrative only)
# Connects ffsubsync output to a timing-rule check.
# Requires: ffsubsync (pip install ffsubsync), python3 with pysubs2
# Usage: ./sync_then_check.sh input.srt reference.mp4 output.srt

set -euo pipefail

INPUT="${1:?input SRT required}"
REF="${2:?reference video or SRT required}"
OUT="${3:?output SRT path required}"

# --- Step 1: sync ---
# README: originals untouched by default; -o writes the synced file.
# If quality is too low, ffsubsync skips and writes nothing (--skip-sync-on-low-quality).
ffsubsync "$REF" -i "$INPUT" -o "$OUT"

if [[ ! -f "$OUT" ]]; then
  echo "ERROR: ffsubsync did not produce $OUT (low-quality skip or crash)." >&2
  exit 1
fi

# --- Step 2: timing check ---
# Rules from art_01M5P66MVH8XS2CQPFSHY6AWDT r1 (inference-based; not executed).
python3 - "$OUT" <<'PYEOF'
import sys, pysubs2

CPS_LIMIT = 20       # adult Netflix (record r1)
MIN_DUR_MS = 833     # 5/6 s (record r1)
MIN_GAP_MS = 1000    # BBC 1 s gap (record r1)
MAX_DUR_MS = 7000    # 7 s limit (record r1)

subs = pysubs2.load(sys.argv[1])
warnings = []
for i, ev in enumerate(subs):
    dur_ms = ev.end - ev.start
    text = ev.plaintext.replace('\n', ' ')
    chars = len(text)
    cps = chars / (dur_ms / 1000) if dur_ms > 0 else 0

    if cps > CPS_LIMIT:
        warnings.append(f"Event {i+1}: cps={cps:.1f} > {CPS_LIMIT}")
    if dur_ms < MIN_DUR_MS:
        warnings.append(f"Event {i+1}: duration {dur_ms}ms < {MIN_DUR_MS}ms")
    if dur_ms > MAX_DUR_MS:
        warnings.append(f"Event {i+1}: duration {dur_ms}ms > {MAX_DUR_MS}ms")
    if i > 0:
        gap = ev.start - subs[i-1].end
        if 0 < gap < MIN_GAP_MS:
            warnings.append(f"Gap before event {i+1}: {gap}ms < {MIN_GAP_MS}ms")

if warnings:
    print("Timing warnings (rules from art_01M5P66MVH8XS2CQPFSHY6AWDT r1):")
    for w in warnings:
        print(" ", w)
else:
    print("No timing violations found.")
PYEOF