#!/usr/bin/env bash
# negate_mix.sh — adapter for negate + colorchannelmixer
# Sources: art_01M6VRHPQXCYKH293R9K1F7KF2 r1, art_01M6VJS0YQE8PBGBG1H50KN8MF r1
# No command has been run; this is a source-derived assembly.
# MIT License.

set -euo pipefail

INPUT="${1:-in.mp4}"
OUTPUT="${2:-out.mp4}"
MODE="${3:-negate_then_sepia}"  # or: sepia_then_negate, luma_negate, rgb_negate_only

# Sepia coefficients from art_01M6VJS0YQE8PBGBG1H50KN8MF r1 (source-documented).
SEPIA="colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"

# Full RGB negate — no component list; source-documented as negating all channels.
NEGATE_FULL="negate"

# RGB-safe channel negate: explicit r,g,b — safe after colorchannelmixer (RGB output).
NEGATE_RGB="negate=components=r+g+b"

# Luma-only negate: ONLY valid in YUV context.
# Do NOT chain directly after colorchannelmixer without a format node.
NEGATE_LUMA="format=yuv420p,negate=components=y,format=rgb24"

case "$MODE" in
  negate_then_sepia)
    # Invert first, then apply sepia matrix.
    # Result: sepia of the colour-inverted image.
    FILTER="${NEGATE_FULL},${SEPIA}"
    ;;
  sepia_then_negate)
    # Apply sepia, then invert all RGB channels.
    # Result: inverted sepia — more predictable for grading workflows.
    FILTER="${SEPIA},${NEGATE_RGB}"
    ;;
  luma_negate)
    # Invert only luminance. Requires explicit YUV conversion.
    # Assumption: input is decodable to yuv420p without quality loss.
    FILTER="${NEGATE_LUMA}"
    ;;
  rgb_negate_only)
    # Simple full negate, no mix. Control case.
    FILTER="${NEGATE_FULL}"
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    echo "Modes: negate_then_sepia | sepia_then_negate | luma_negate | rgb_negate_only" >&2
    exit 1
    ;;
esac

echo "[negate_mix.sh] Mode: $MODE"
echo "[negate_mix.sh] Filter chain: $FILTER"
echo "[negate_mix.sh] Record your FFmpeg version: ffmpeg -version"

# Uncomment to run (requires FFmpeg with negate and colorchannelmixer):
# ffmpeg -i "$INPUT" -vf "$FILTER" "$OUTPUT"
echo "[negate_mix.sh] Command assembled (not run): ffmpeg -i \"$INPUT\" -vf \"$FILTER\" \"$OUTPUT\""