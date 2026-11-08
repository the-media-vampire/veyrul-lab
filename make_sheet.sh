#!/usr/bin/env bash
# Generates a 5x5 sprite sheet (320x320 px) with labelled tiles.
# Requires ImageMagick `convert` and `montage`.
set -euo pipefail

TILE_W=64
TILE_H=64
COLS=5
ROWS=5
OUT="sheet_5x5.png"

TILES=()
for i in $(seq 1 $((COLS * ROWS))); do
  TMP="/tmp/tile_${i}.png"
  convert -size "${TILE_W}x${TILE_H}" \
    xc:"hsl($((i * 13 % 360)),70%,60%)" \
    -gravity Center \
    -pointsize 18 \
    -annotate 0 "${i}" \
    "$TMP"
  TILES+=("$TMP")
done

montage "${TILES[@]}" \
  -geometry "${TILE_W}x${TILE_H}+0+0" \
  -tile "${COLS}x${ROWS}" \
  "$OUT"

echo "Sheet written: $OUT"
identify -verbose "$OUT" | grep -E 'Geometry|Type'