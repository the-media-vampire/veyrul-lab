#!/usr/bin/env bash
# lenscorrect_trial.sh
# Operationalises art_01M6V5QZG15J2GQABEBQVQ8GBK r1
# Usage: ./lenscorrect_trial.sh input.mp4 [k1] [k2]
# Defaults: k1=-0.2 k2=0 (illustrative trial values, not from the manual)
# Requires: ffmpeg with lenscorrection filter (check: ffmpeg -filters | grep lenscorrection)
# Outputs: baseline_<input>, corrected_k1_<k1>_k2_<k2>_<input>
# MIT licence.

set -euo pipefail

INPUT="${1:-}"
K1="${2:--0.2}"
K2="${3:-0}"

if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 input.mp4 [k1] [k2]" >&2
  exit 1
fi

if ! ffmpeg -filters 2>/dev/null | grep -q lenscorrection; then
  echo "ERROR: lenscorrection not found in this ffmpeg build." >&2
  echo "Run: ffmpeg -version  to check your build." >&2
  exit 1
fi

BASENAME="$(basename "$INPUT")"
BASELINE="baseline_${BASENAME}"
CORRECTED="corrected_k1_${K1}_k2_${K2}_${BASENAME}"

echo "=== Step 1: Baseline (k1=0 k2=0 — no change expected) ==="
ffmpeg -i "$INPUT" \
  -vf "lenscorrection=k1=0:k2=0:i=bilinear" \
  -c:a copy \
  "$BASELINE" \
  && echo "Baseline written: $BASELINE" \
  || { echo "Baseline failed."; exit 1; }

echo ""
echo "=== Step 2: Correction (k1=$K1 k2=$K2) ==="
ffmpeg -i "$INPUT" \
  -vf "lenscorrection=k1=${K1}:k2=${K2}:i=bilinear" \
  -c:a copy \
  "$CORRECTED" \
  && echo "Corrected written: $CORRECTED" \
  || { echo "Correction failed."; exit 1; }

echo ""
echo "=== Verification prompts ==="
echo "1. Play $BASELINE and $CORRECTED side by side."
echo "   ffplay -i $BASELINE  &  ffplay -i $CORRECTED"
echo "2. Confirm baseline matches source (straight lines unchanged)."
echo "3. Check corrected: straight lines near edges should bow less."
echo "4. If lines bow the WRONG way, flip the sign: k1=$(echo "$K1" | sed 's/^-//' | sed 's/^\([^-]\)/-\1/')"
echo "5. If edges show black fill, crop or add: :fc=black@0 (default)."
echo "6. Record ffmpeg version: $(ffmpeg -version 2>&1 | head -1)"
echo ""
echo "Next: try k1 values -0.1, -0.2, -0.3 one at a time (source-documented range: -1 to 1)."
echo "For calibrated values, extract k1,k2 from an OpenCV calibration matrix."