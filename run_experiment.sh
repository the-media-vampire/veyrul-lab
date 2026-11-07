#!/usr/bin/env bash
# lut1d interpolation discriminator — run_experiment.sh
# Requires: FFmpeg with lut1d, ImageMagick (compare), gradient.png, coarse_lift.cube
# Usage: bash run_experiment.sh
set -euo pipefail

INPUT=gradient.png
LUT=coarse_lift.cube

echo "=== FFmpeg version ==="
ffmpeg -version | head -1   # record for results

echo "=== Render: nearest ==="
ffmpeg -y -i "$INPUT" -vf "lut1d=file=${LUT}:interp=nearest" nearest.png

echo "=== Render: linear ==="
ffmpeg -y -i "$INPUT" -vf "lut1d=file=${LUT}:interp=linear" linear.png

echo "=== Render: cubic ==="
ffmpeg -y -i "$INPUT" -vf "lut1d=file=${LUT}:interp=cubic" cubic.png

echo "=== Render: default (no interp specified) ==="
ffmpeg -y -i "$INPUT" -vf "lut1d=file=${LUT}" default.png

echo "=== Pixel diff: nearest vs linear ==="
# Non-black = modes differ; all-black = indistinguishable on this ramp
convert nearest.png linear.png -compose difference -composite \
    -auto-level diff_nearest_vs_linear.png || \
    echo "WARN: ImageMagick not available; diff skipped"

echo "=== Pixel diff: linear vs cubic ==="
convert linear.png cubic.png -compose difference -composite \
    -auto-level diff_linear_vs_cubic.png || \
    echo "WARN: ImageMagick not available; diff skipped"

echo "=== Pixel diff: linear vs default ==="
convert linear.png default.png -compose difference -composite \
    -auto-level diff_linear_vs_default.png || \
    echo "WARN: ImageMagick not available; diff skipped"

echo ""
echo "Inspect diff_linear_vs_default.png: all-black = default IS linear."
echo "Inspect diff_nearest_vs_linear.png:  non-black = stepping is real."
echo "Inspect diff_linear_vs_cubic.png:    non-black = cubic adds refinement here."