#!/usr/bin/env bash
# Run all three experiment arms. Log ffmpeg version first.
# Requires ffmpeg with untile filter.
set -euo pipefail

echo "=== FFmpeg version ==="
ffmpeg -version 2>&1 | head -3

INPUT="sheet_5x5.png"

echo ""
echo "=== Arm A: correct layout 5x5 ==="
ffmpeg -y -r 1 -i "$INPUT" -vf untile=5x5 -r 25 arm_a_correct.mkv 2>&1
echo "Arm A frame count:"
ffprobe -v error -select_streams v:0 \
  -count_frames -show_entries stream=nb_read_frames \
  -of default=noprint_wrappers=1 arm_a_correct.mkv

echo ""
echo "=== Arm B: wrong column count 4x5 ==="
ffmpeg -y -r 1 -i "$INPUT" -vf untile=4x5 -r 20 arm_b_wrong_cols.mkv 2>&1 || echo "EXIT CODE: $?"
if [ -f arm_b_wrong_cols.mkv ]; then
  ffprobe -v error -select_streams v:0 \
    -count_frames -show_entries stream=nb_read_frames \
    -of default=noprint_wrappers=1 arm_b_wrong_cols.mkv
fi

echo ""
echo "=== Arm C: non-dividing layout 3x5 ==="
ffmpeg -y -r 1 -i "$INPUT" -vf untile=3x5 -r 15 arm_c_no_divide.mkv 2>&1 || echo "EXIT CODE: $?"
if [ -f arm_c_no_divide.mkv ]; then
  ffprobe -v error -select_streams v:0 \
    -count_frames -show_entries stream=nb_read_frames \
    -of default=noprint_wrappers=1 arm_c_no_divide.mkv
fi

echo ""
echo "Done. Fill in checklist in README.md."