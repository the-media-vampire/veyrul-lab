#!/usr/bin/env bash
# avgblur_trial.sh — FFmpeg avgblur baseline + radius sweep
# Source: art_01M6WGWVXNKPZGYE6MDK0PPWKB r1
# Options documented: sizeX (horiz radius), sizeY (0 = match sizeX), planes (default: all)
# No radius range or default is stated in the manual; sizeX=1 is the minimum useful start.
#
# Usage:
#   bash avgblur_trial.sh input.mp4
#   bash avgblur_trial.sh input.mp4 aniso   # also runs anisotropic test (sizeY=1)
#
# Outputs are named avgblur_<tag>.mp4 for direct side-by-side comparison.
# Record the FFmpeg version with your results: ffmpeg -version | head -1

set -euo pipefail

INPUT="${1:-}"
MODE="${2:-}"

if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 input.mp4 [aniso]" >&2
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "File not found: $INPUT" >&2
  exit 1
fi

run() {
  local tag="$1"; shift
  local filter="$1"; shift
  local out="avgblur_${tag}.mp4"
  echo "--- $tag: $filter"
  ffmpeg -hide_banner -loglevel warning -i "$INPUT" -vf "$filter" -c:a copy -y "$out"
  echo "Written: $out"
}

# BASELINE: sizeX=1, sizeY=0 (equals sizeX per manual)
# Establishes the minimum-effect reference before any creative radius is applied.
# If this looks identical to input, check your FFmpeg build has avgblur.
run "baseline_sx1"   "avgblur=sizeX=1"

# RADIUS SWEEP: one variable at a time, sizeY stays at 0 (symmetric)
for sx in 5 10 20; do
  run "sx${sx}_sym"  "avgblur=sizeX=${sx}"
done

# ANISOTROPIC TEST: horizontal-dominant blur (sizeY=1 keeps vertical near-unblurred)
# Inference from documented radius options — art_01M6WGWVXNKPZGYE6MDK0PPWKB r1 notes this as inference.
if [[ "$MODE" == "aniso" ]]; then
  run "sx20_sy1_aniso" "avgblur=sizeX=20:sizeY=1"
fi

echo ""
echo "Compare outputs with: ffplay avgblur_baseline_sx1.mp4 avgblur_sx20_sym.mp4"
echo "Expected: larger sizeX = softer image. Baseline should be barely perceptible."
echo "If baseline looks unchanged from input: avgblur may not be in your build."