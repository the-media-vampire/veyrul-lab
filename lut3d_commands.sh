#!/usr/bin/env bash
# lut3d interpolation discriminator — command lines
# Source: art_01M6VM5DCRRQ32378328NBG3XF r1
# Commands assembled from FFmpeg option names; the manual provides no example.
# Run make_gradient.py and make_luts.py first.

set -euo pipefail

echo "=== FFmpeg version ==="
ffmpeg -version | head -3

INPUT="gradient_test.png"

for LUT in identity lift crush; do
  for INTERP in nearest trilinear tetrahedral; do
    OUT="out_${LUT}_${INTERP}.png"
    echo "--- $OUT ---"
    ffmpeg -y -i "$INPUT" \
      -vf "lut3d=file=${LUT}.cube:interp=${INTERP}" \
      "$OUT"
  done
done

echo ""
echo "=== Pixel difference: nearest vs trilinear (lift LUT) ==="
ffmpeg -y -i out_lift_nearest.png -i out_lift_trilinear.png \
  -filter_complex "[0][1]blend=all_mode=difference,eq=brightness=5" diff_n_vs_tl.png

echo "=== Pixel difference: trilinear vs tetrahedral (lift LUT) ==="
ffmpeg -y -i out_lift_trilinear.png -i out_lift_tetrahedral.png \
  -filter_complex "[0][1]blend=all_mode=difference,eq=brightness=5" diff_tl_vs_tet.png

echo ""
echo "Inspect diff_n_vs_tl.png and diff_tl_vs_tet.png."
echo "Non-black pixels in diff_n_vs_tl.png → nearest differs from trilinear on this gradient."
echo "All-black diff_tl_vs_tet.png → tetrahedral adds no visible refinement here."