#!/usr/bin/env bash
# tiltandshift_trial.sh
# Runs the three start/end comparisons from:
#   art_01M6VWG5T1ANCZWGNZ684437KP rev 1
# Usage: bash tiltandshift_trial.sh <input.mp4>
# Requires: FFmpeg build with tiltandshift filter
# Outputs: results/ directory with one file per trial + run.log

set -euo pipefail

INPUT="${1:-}"
if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 <input.mp4>" >&2
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "File not found: $INPUT" >&2
  exit 1
fi

# Verify tiltandshift is available in this build
if ! ffmpeg -filters 2>/dev/null | grep -q tiltandshift; then
  echo "ERROR: tiltandshift not found in this FFmpeg build." >&2
  echo "Run: ffmpeg -filters | grep tiltandshift to confirm." >&2
  exit 1
]

OUTDIR="results/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTDIR"

LOG="$OUTDIR/run.log"
FFVER=$(ffmpeg -version 2>&1 | head -1)
echo "FFmpeg: $FFVER" | tee -a "$LOG"
echo "Input:  $INPUT"   | tee -a "$LOG"
echo "---"              | tee -a "$LOG"

run_trial() {
  local label="$1"
  local vf="$2"
  local out="$OUTDIR/${label}.mp4"
  echo "[trial] $label  vf='$vf'" | tee -a "$LOG"
  ffmpeg -i "$INPUT" -vf "$vf" -c:v libx264 -preset fast -crf 18 \
         -an "$out" -y 2>> "$LOG"
  echo "[done]  $out" | tee -a "$LOG"
}

# Baseline: plain copy, no filter — reference frame for the effect
run_trial "00_baseline" "null"

# Trial 1: documented first command (art_01M6VWG5T1ANCZWGNZ684437KP)
run_trial "01_start_frame_end_frame" "tiltandshift=start=frame:end=frame"

# Trial 2: start=none — filtering begins immediately, no lead-in frames
run_trial "02_start_none_end_frame" "tiltandshift=start=none:end=frame"

# Trial 3: start=black — black pad at the beginning
run_trial "03_start_black_end_frame" "tiltandshift=start=black:end=frame"

echo "---" | tee -a "$LOG"
echo "Results in: $OUTDIR" | tee -a "$LOG"
echo "Compare 01 vs 02: visible jump at start absent in 01, present in 02." | tee -a "$LOG"
echo "Compare 01 vs 03: black leader in 03 instead of held first frame."     | tee -a "$LOG"
echo "Compare any vs 00: confirms the time-slice effect is applied."          | tee -a "$LOG"