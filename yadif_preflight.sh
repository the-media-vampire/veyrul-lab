#!/usr/bin/env bash
# yadif_preflight.sh
# Usage: yadif_preflight.sh <input> <output> [mode] [parity] [deint]
#
# mode:   0=send_frame (default, keeps fps)  1=send_field (doubles fps)
#         2=send_frame_nospatial             3=send_field_nospatial
# parity: auto (default) | tff | bff
# deint:  all (default)  | interlaced
#
# Source: art_01M6V6CAXJB89TN8NEH6VQXXDD r1
# Prints the ffmpeg command and pre-flight warnings. Does NOT run it.

set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"
MODE="${3:-0}"
PARITY="${4:-auto}"
DEINT="${5:-all}"

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "Usage: $0 <input> <output> [mode] [parity] [deint]" >&2
  exit 1
fi

# --- Validate mode ---
case "$MODE" in
  0|send_frame)             MODE_N=0; MODE_LABEL="send_frame (1 frame per input frame, fps preserved)" ;;
  1|send_field)             MODE_N=1; MODE_LABEL="send_field (1 frame per field, fps DOUBLED)" ;;
  2|send_frame_nospatial)   MODE_N=2; MODE_LABEL="send_frame_nospatial (like mode 0, skips spatial check)" ;;
  3|send_field_nospatial)   MODE_N=3; MODE_LABEL="send_field_nospatial (like mode 1, skips spatial check, fps DOUBLED)" ;;
  *) echo "ERROR: unknown mode '$MODE'. Use 0,1,2,3 or the name." >&2; exit 1 ;;
esac

# --- Validate parity ---
case "$PARITY" in
  auto|-1) PARITY_N=-1; PARITY_LABEL="auto (detects; assumes tff if unknown)" ;;
  tff|0)   PARITY_N=0;  PARITY_LABEL="tff — top field first" ;;
  bff|1)   PARITY_N=1;  PARITY_LABEL="bff — bottom field first" ;;
  *) echo "ERROR: unknown parity '$PARITY'. Use auto, tff or bff." >&2; exit 1 ;;
esac

# --- Validate deint ---
case "$DEINT" in
  all)        DEINT_N=0; DEINT_LABEL="all frames" ;;
  interlaced) DEINT_N=1; DEINT_LABEL="interlaced-flagged frames only" ;;
  *) echo "ERROR: unknown deint '$DEINT'. Use all or interlaced." >&2; exit 1 ;;
esac

# --- Probe source fps and field order ---
echo "=== yadif preflight ==="
echo ""
echo "Input : $INPUT"
echo "Output: $OUTPUT"
echo ""

if command -v ffprobe &>/dev/null && [[ -f "$INPUT" ]]; then
  SRC_FPS=$(ffprobe -v error -select_streams v:0 \
    -show_entries stream=r_frame_rate \
    -of default=noprint_wrappers=1:nokey=1 "$INPUT" 2>/dev/null || echo "unknown")
  FIELD_ORDER=$(ffprobe -v error -select_streams v:0 \
    -show_entries stream=field_order \
    -of default=noprint_wrappers=1:nokey=1 "$INPUT" 2>/dev/null || echo "unknown")
  echo "Source fps (r_frame_rate) : $SRC_FPS"
  echo "Source field_order        : $FIELD_ORDER"
else
  echo "(ffprobe not found or input not on disk — skipping probe)"
  SRC_FPS="unknown"
  FIELD_ORDER="unknown"
fi

echo ""
echo "=== Chosen options ==="
echo "mode   : $MODE_N — $MODE_LABEL"
echo "parity : $PARITY_N — $PARITY_LABEL"
echo "deint  : $DEINT_N — $DEINT_LABEL"

# --- Warnings — the three documented failure modes ---
echo ""
echo "=== Warnings ==="
WARNED=0

# 1. Field order mismatch risk
if [[ "$PARITY" == "auto" || "$PARITY" == "-1" ]]; then
  if [[ "$FIELD_ORDER" == "bb" || "$FIELD_ORDER" == "bt" ]]; then
    echo "WARN [field-order]: probe reports '$FIELD_ORDER'; auto may mis-detect."
    echo "      If output judders, set parity=bff or parity=tff explicitly."
    echo "      Failure: jerky back-and-forth motion (art_01M6V6CAXJB89TN8NEH6VQXXDD r1)."
    WARNED=1
  else
    echo "INFO [field-order]: parity=auto; tff assumed if order unknown."
    echo "      Set parity=bff for DV/consumer-camera BFF material."
  fi
fi

# 2. Combing risk from deint=interlaced
if [[ "$DEINT" == "interlaced" ]]; then
  echo "WARN [deint=interlaced]: only flagged frames are processed."
  echo "      If combing remains, switch to deint=all."
  echo "      Failure: combing on frames not marked interlaced (art_01M6V6CAXJB89TN8NEH6VQXXDD r1)."
  WARNED=1
fi

# 3. Frame-rate surprise from send_field modes
if [[ "$MODE_N" == "1" || "$MODE_N" == "3" ]]; then
  echo "WARN [frame-rate]: mode=$MODE_N doubles the output frame rate."
  if [[ "$SRC_FPS" != "unknown" ]]; then
    echo "      Source fps ~$SRC_FPS → output will be approximately double."
  fi
  echo "      Confirm your container and player handle the doubled rate."
  WARNED=1
fi

[[ "$WARNED" -eq 0 ]] && echo "No warnings for chosen options."

# --- Print the command ---
FILTER="yadif=mode=${MODE_N}:parity=${PARITY_N}:deint=${DEINT_N}"
echo ""
echo "=== Command (NOT run) ==="
echo "  ffmpeg -i \"$INPUT\" -vf \"$FILTER\" \"$OUTPUT\""
echo ""
echo "Verification steps:"
echo "  1. Run ffprobe on the output and confirm r_frame_rate matches expectation."
echo "  2. Inspect a moving-edge frame for combing (should be absent)."
echo "  3. Watch a motion sequence for judder (indicates wrong field order)."
echo ""
echo "Baseline comparison: run yadif=mode=0:parity=-1:deint=all first;"
echo "compare to your chosen settings on the same excerpt."