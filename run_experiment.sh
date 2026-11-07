#!/usr/bin/env bash
# FFmpeg vibrance intensity x alternate experiment
# Source: art_01M6W6JQ5FA6YDBG4870H0VC7A revision 1
# Commands assembled from documented options; no example exists in the manual.
# USAGE: bash run_experiment.sh in.mp4

set -euo pipefail

INPUT="${1:-in.mp4}"

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: provide an input file as the first argument."
  exit 1
fi

echo "=== FFmpeg build ==="
ffmpeg -version | head -3 | tee ffmpeg_version.txt

echo "\n=== A: baseline (null filter) ==="
ffmpeg -y -i "$INPUT" -vf null out_A_baseline.mp4

echo "\n=== B: intensity=-0.5, alternate=0 (gray-ward prediction) ==="
ffmpeg -y -i "$INPUT" -vf vibrance=intensity=-0.5:alternate=0 out_B_neg_no_alt.mp4

echo "\n=== C: intensity=-0.5, alternate=1 (hue-shift prediction) ==="
ffmpeg -y -i "$INPUT" -vf vibrance=intensity=-0.5:alternate=1 out_C_neg_alt.mp4

echo "\n=== D: intensity=0.5 (positive / orientation check) ==="
ffmpeg -y -i "$INPUT" -vf vibrance=intensity=0.5 out_D_pos.mp4

echo "\n=== Done. Compare A vs B vs C visually and record results in README.md ==="
echo "Key question: do B and C differ? If not, alternate is inert at this intensity."