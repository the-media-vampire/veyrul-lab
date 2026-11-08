#!/usr/bin/env bash
# Untested. Check pixel format, then export palette image.
# Usage: bash check_pal8.sh input.gif [box_size]
# Source: art_01M6W7WQKZHC1DRD4EM86Q1KPN r1

INPUT="${1:-in.gif}"
S="${2:-16}"
OUT="palette_s${S}.png"

echo "=== Checking pixel format ==="
ffprobe -v error -select_streams v:0 \
  -show_entries stream=pix_fmt \
  -of default=nw=1 "$INPUT"

echo "=== Exporting palette image (s=$S) ==="
ffmpeg -i "$INPUT" -vf "showpalette=s=${S}" -frames:v 1 "$OUT"

echo "Output: $OUT"
echo "FFmpeg version:"
ffmpeg -version | head -1