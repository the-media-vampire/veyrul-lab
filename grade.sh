#!/usr/bin/env bash
# grade.sh — route a clip through colorchannelmixer or curves
# Usage: grade.sh <mode> <input> <output>
#   mode: grayscale | sepia | flat (identity, for curves baseline)
# Provenance: coefficients from FFmpeg filters docs via art_01M6VJS0YQE8PBGBG1H50KN8MF r1.
# License: MIT
set -euo pipefail

MODE="${1:-grayscale}"
INPUT="${2:?Provide input file}"
OUTPUT="${3:?Provide output file}"

case "$MODE" in
  grayscale)
    # colorchannelmixer: equal luminance weights R=G=B per pixel
    # Assumption: linear RGB; pc/pa defaults (no luminance preservation)
    FILTER="colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3"
    ;;
  sepia)
    # colorchannelmixer: warm-tint preset from FFmpeg manual
    FILTER="colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"
    ;;
  sepia_lum)
    # Same sepia mix but with luminance preservation at full strength
    # pc=lum pa=1.0 — corrects brightness shift from non-unity weight sums
    FILTER="colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131:0:lum:1.0"
    ;;
  flat)
    # curves identity — baseline to verify curves pipeline is working
    # Useful control: should produce no visible change
    FILTER="curves=r='0/0 1/1':g='0/0 1/1':b='0/0 1/1'"
    ;;
  mix_then_tone)
    # Chain: grayscale mix THEN a brightening tone curve
    # Demonstrates composability: two independent linear interfaces in sequence
    FILTER="colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3,curves=all='0/0 0.5/0.6 1/1'"
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    exit 1
    ;;
esac

echo "[grade.sh] mode=$MODE filter=$FILTER"
ffmpeg -hide_banner -i "$INPUT" -vf "$FILTER" -c:a copy "$OUTPUT"