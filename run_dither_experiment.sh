#!/usr/bin/env bash
# FFmpeg GIF Dither Comparison Experiment
# Source: art_01M6TXQ4AJ3RFQYC0DGQHJ20SG revision 1
# Variable held fixed: input clip, scale, fps, max_colors, stats_mode=full
# Variable under test: dither mode (4 treatments)
# Usage: bash run_dither_experiment.sh input.mkv
# Requires: ffmpeg with palettegen and paletteuse filters

set -euo pipefail
INPUT="${1:-input.mkv}"
SCALE="320:-1"       # hold fixed
FPS=15               # hold fixed
MAX_COLORS=256       # hold fixed
STATS_MODE=full      # hold fixed across all runs

echo "FFmpeg version:"
ffmpeg -version | head -1

# --- Pass 1: single shared palette (stats_mode=full, all frames) ---
ffmpeg -y -i "$INPUT" \
  -vf "fps=${FPS},scale=${SCALE}:flags=lanczos,palettegen=max_colors=${MAX_COLORS}:stats_mode=${STATS_MODE}" \
  palette_shared.png
echo "Palette written: palette_shared.png"

# --- Pass 2: four dither treatments, identical palette ---
DITHERS=("none" "bayer" "sierra2" "sierra2_4a")
for DITHER in "${DITHERS[@]}"; do
  EXTRA=""
  if [ "$DITHER" = "bayer" ]; then
    EXTRA=":bayer_scale=3"
  fi
  OUT="out_${DITHER}.gif"
  ffmpeg -y -i "$INPUT" -i palette_shared.png \
    -lavfi "fps=${FPS},scale=${SCALE}:flags=lanczos [x]; [x][1:v] paletteuse=dither=${DITHER}${EXTRA}" \
    "$OUT"
  SIZE=$(du -k "$OUT" | cut -f1)
  echo "dither=${DITHER}${EXTRA}  ->  ${OUT}  (${SIZE} KB)"
done

echo ""
echo "Next: open all four GIFs side-by-side and score with rubric.md"