#!/usr/bin/env bash
# guided_trial.sh — FFmpeg guided filter trial with baseline
# Source: art_01M6W2ZSB54BVKZ8GR448940YN r1
# NOT EXECUTED — source-only artifact
#
# Usage:
#   ./guided_trial.sh input.png
# Optional second arg: guidance image (must match resolution + pixel format)
#   ./guided_trial.sh input.png guidance.png

set -euo pipefail

INPUT="${1:-}"
GUIDANCE="${2:-}"

if [[ -z "$INPUT" ]]; then
  echo "ERROR: supply an input image as the first argument" >&2
  exit 1
fi

# --- Build check: fail early if guided filter is absent ---
if ! ffmpeg -filters 2>/dev/null | grep -q 'guided'; then
  echo "ERROR: 'guided' filter not found in this ffmpeg build." >&2
  echo "       Confirm build with: ffmpeg -filters | grep guided" >&2
  exit 2
fi

echo "Build check passed: guided filter present."

# --- Baseline: plain guided, all defaults (radius=3, eps=0.01, mode=basic) ---
# Diagnostic purpose: if edges blur at defaults, something is wrong before
# touching creative parameters. Compare this output against the source image.
echo "Running baseline (defaults: radius=3, eps=0.01, mode=basic)..."
ffmpeg -y -i "$INPUT" -vf guided out_baseline.png
echo "Baseline written: out_baseline.png"

# --- Sweep: radius and eps, one variable at a time ---
# Vary radius (eps held at default 0.01)
for R in 1 5 10 20; do
  OUT="out_r${R}_eps0.01.png"
  echo "  radius=$R eps=0.01 -> $OUT"
  ffmpeg -y -i "$INPUT" -vf "guided=radius=${R}:eps=0.01" "$OUT"
done

# Vary eps (radius held at default 3)
for E in 0.001 0.01 0.1 0.5; do
  ETAG=$(echo "$E" | tr '.' 'p')
  OUT="out_r3_eps${ETAG}.png"
  echo "  radius=3 eps=$E -> $OUT"
  ffmpeg -y -i "$INPUT" -vf "guided=radius=3:eps=${E}" "$OUT"
done

# Fast mode with subsampling (for speed comparison)
echo "Running fast mode (radius=3, eps=0.01, sub=4)..."
ffmpeg -y -i "$INPUT" -vf "guided=mode=fast:sub=4" out_fast_sub4.png
echo "Fast mode written: out_fast_sub4.png"

# --- Guidance mode (optional second input) ---
if [[ -n "$GUIDANCE" ]]; then
  echo "Running guidance mode with: $GUIDANCE"
  # Inputs must match resolution and pixel format (see source art_01M6W2ZSB54BVKZ8GR448940YN r1)
  ffmpeg -y -i "$INPUT" -i "$GUIDANCE" \
    -filter_complex "guided=guidance=on" \
    out_guided_mode.png
  echo "Guidance mode written: out_guided_mode.png"
else
  echo "(No guidance image supplied; skipping guidance mode)"
fi

echo ""
echo "Done. Compare all out_*.png against the source image."
echo "Check: flat areas should smooth; edges should hold."
echo "If colour noise persists, add :planes=7 to include chroma planes."