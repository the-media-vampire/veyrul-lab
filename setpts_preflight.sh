#!/usr/bin/env bash
# setpts_preflight.sh
# Usage: ./setpts_preflight.sh <input_file> <speed_factor> [output_file]
# speed_factor > 1 = faster (e.g. 2 = 2x speed)
# speed_factor < 1 = slower (e.g. 0.5 = half speed)
# Source: art_01M6TZT9NPFRHNSG1H76FJ9MKZ r1
set -euo pipefail

INPUT="${1:-}"
SPEED="${2:-}"
OUTPUT="${3:-out_retimed.mp4}"

if [[ -z "$INPUT" || -z "$SPEED" ]]; then
  echo "Usage: $0 <input_file> <speed_factor> [output_file]" >&2
  exit 1
fi

# Validate speed is a positive number
if ! awk "BEGIN{exit !($SPEED > 0)}" 2>/dev/null; then
  echo "ERROR: speed_factor must be a positive number, got: $SPEED" >&2
  exit 1
fi

# setpts multiplier is 1/speed (documented arithmetic, art_01M6TZT9NPFRHNSG1H76FJ9MKZ r1)
PTS_MULT=$(awk "BEGIN{printf \"%.6f\", 1/$SPEED}")

echo "=== setpts preflight ==="
echo "Input      : $INPUT"
echo "Speed      : ${SPEED}x"
echo "PTS mult   : $PTS_MULT  (setpts=${PTS_MULT}*PTS)"

# Warn on common inversion mistake
if awk "BEGIN{exit !($SPEED < 1)}"; then
  echo "NOTE: speed < 1 → slower output. PTS multiplier > 1. Correct per manual."
elif awk "BEGIN{exit !($SPEED > 1)}"; then
  echo "NOTE: speed > 1 → faster output. PTS multiplier < 1. Correct per manual."
else
  echo "NOTE: speed = 1 → no change."
fi

# Probe duration if ffprobe available
if command -v ffprobe &>/dev/null && [[ -f "$INPUT" ]]; then
  SRC_DUR=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$INPUT" 2>/dev/null || echo "unknown")
  if [[ "$SRC_DUR" != "unknown" ]]; then
    OUT_DUR=$(awk "BEGIN{printf \"%.2f\", $SRC_DUR / $SPEED}")
    echo "Source dur : ${SRC_DUR}s"
    echo "Expected   : ${OUT_DUR}s  (source / speed, arithmetic only)"
  fi
else
  echo "ffprobe not found or input missing; duration check skipped."
fi

# Audio warning
echo ""
echo "AUDIO: command below drops audio (-an)."
echo "To retime audio separately, add: -af asetpts=${PTS_MULT}*PTS"
echo "Unresolved: audio retiming not covered in source (art_01M6TZT9NPFRHNSG1H76FJ9MKZ r1)."
echo ""

# Print the command — does NOT run it
echo "=== Suggested command (review before running) ==="
echo "ffmpeg -i \"$INPUT\" -vf \"setpts=${PTS_MULT}*PTS\" -an \"$OUTPUT\""
echo ""
echo "Run the above command manually after reviewing the preflight output."