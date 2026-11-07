#!/usr/bin/env bash
# FFmpeg GIF stats_mode isolation experiment
# Companion to artifact f20e0b08 (dither experiment)
# Source: art_01M6TXQ4AJ3RFQYC0DGQHJ20SG revision 1
#
# WHAT IS HELD FIXED: input clip, scale, fps, dither (sierra2_4a), max_colors (256)
# VARIABLE UNDER TEST: palettegen stats_mode = full | diff | single
#
# NOT EXECUTED HERE. Run against your own clip and record results in statsmode_rubric.md

set -euo pipefail

INPUT="${1:-input.mkv}"
SCALE=320
FPS=15
DITHER="sierra2_4a"
MAX_COLORS=256

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: input file not found: $INPUT"
  echo "Usage: $0 path/to/clip.mkv"
  exit 1
fi

echo "=== FFmpeg version ==="
ffmpeg -version | head -1
echo "=== Input: $INPUT | scale: ${SCALE}px | fps: $FPS | dither: $DITHER ==="

for MODE in full diff single; do
  PALETTE="palette_${MODE}.png"
  OUTPUT="out_statsmode_${MODE}.gif"

  echo "--- Pass 1: palettegen stats_mode=${MODE} ---"
  ffmpeg -y -i "$INPUT" \
    -vf "fps=${FPS},scale=${SCALE}:-1:flags=lanczos,palettegen=max_colors=${MAX_COLORS}:stats_mode=${MODE}" \
    "$PALETTE"

  echo "--- Pass 2: paletteuse dither=${DITHER} ---"
  ffmpeg -y -i "$INPUT" -i "$PALETTE" \
    -lavfi "fps=${FPS},scale=${SCALE}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=${DITHER}" \
    "$OUTPUT"

  SIZE=$(du -k "$OUTPUT" | cut -f1)
  PALETTE_SIZE=$(du -k "$PALETTE" | cut -f1)
  echo "RESULT stats_mode=${MODE}: gif=${SIZE}KB palette_png=${PALETTE_SIZE}KB"
done

echo "=== All three runs complete. Fill statsmode_rubric.md with the RESULT lines above. ==="