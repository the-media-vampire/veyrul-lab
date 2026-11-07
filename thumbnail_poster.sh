#!/usr/bin/env bash
# FFmpeg thumbnail filter – starter script
# Source: art_01M6TZ2MCGC1V0FRHAH8Y31G44 r1 (Veyrul)
# Record your FFmpeg version below before sharing results.
#
# Usage:
#   bash thumbnail_poster.sh single  INPUT OUTPUT_PNG [WIDTH HEIGHT]
#   bash thumbnail_poster.sh multi   INPUT OUTPUT_PATTERN [BATCH_N]
#
# Examples:
#   bash thumbnail_poster.sh single  clip.mp4 poster.png 300 200
#   bash thumbnail_poster.sh multi   clip.mp4 thumb_%03d.png 50

set -euo pipefail

# --- record FFmpeg version for attribution ---
FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -1)
echo "FFmpeg: $FFMPEG_VERSION"

MODE="${1:-single}"
INPUT="${2:?Provide an input file as arg 2}"
OUTPUT="${3:?Provide an output name as arg 3}"

case "$MODE" in
  single)
    W="${4:-300}"
    H="${5:-200}"
    # From art_01M6TZ2MCGC1V0FRHAH8Y31G44 r1 – single poster frame
    # Picks the most representative frame from the whole clip.
    # Memory note: default batch covers the full stream; lower n if memory is tight.
    echo "Writing single poster frame → $OUTPUT"
    ffmpeg -i "$INPUT" \
      -vf "thumbnail,scale=${W}:${H}" \
      -frames:v 1 \
      "$OUTPUT"
    echo "Done. Check the frame by eye – the filter picks by its own"
    echo "representativeness measure, not by aesthetic quality."
    ;;

  multi)
    N="${4:-50}"
    # One frame per batch of N frames – remove -frames:v 1 and use a
    # numbered pattern so each batch writes its own file.
    echo "Writing one frame per $N-frame batch → $OUTPUT"
    ffmpeg -i "$INPUT" \
      -vf "thumbnail=${N}" \
      "$OUTPUT"
    echo "Done. Expected image count ≈ total_frames / ${N}."
    echo "If only one image was written, make sure OUTPUT contains %03d or similar."
    ;;

  *)
    echo "Unknown mode '$MODE'. Use 'single' or 'multi'."
    exit 1
    ;;
esac

# --- what to record when sharing results ---
# 1. FFmpeg version (printed above)
# 2. Input clip duration and frame rate  (ffprobe -v quiet -show_streams INPUT)
# 3. Batch size n used
# 4. Output dimensions
# 5. Whether the picked frame looked representative or not, and why
# Cite art_01M6TZ2MCGC1V0FRHAH8Y31G44 r1 in your result.