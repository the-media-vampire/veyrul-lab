#!/usr/bin/env bash
# ivtc_pullup.sh — Inverse-telecine helper using FFmpeg pullup
# Source: art_01M6W95VGW89J83N9D1VQP2TPQ r1 (Veyrul)
# License: MIT
#
# Usage:
#   ./ivtc_pullup.sh [options] -i INPUT -o OUTPUT
#
# Options:
#   -r RATE    Input frame rate: 29.97 (default), 30, or 25
#   -s SB      strict_breaks: -1, 0 (default), or 1
#   -j PAD     Junk-edge padding in pixels (applied equally all sides)
#              Left/right rounded to nearest 8 px; top/bottom to 2 lines
#   -p PLANE   Metric plane: l (luma, default), u, v
#   -n         Dry-run: print command only, do not run
#   -h         Help

set -euo pipefail

INPUT=""
OUTPUT=""
RATE="29.97"
SB=0
PAD=0
PLANE="l"
DRYRUN=false

usage() {
  grep '^#' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

while getopts ":i:o:r:s:j:p:nh" opt; do
  case $opt in
    i) INPUT="$OPTARG" ;;
    o) OUTPUT="$OPTARG" ;;
    r) RATE="$OPTARG" ;;
    s) SB="$OPTARG" ;;
    j) PAD="$OPTARG" ;;
    p) PLANE="$OPTARG" ;;
    n) DRYRUN=true ;;
    h) usage ;;
    *) echo "Unknown option -$OPTARG" >&2; exit 1 ;;
  esac
done

[ -z "$INPUT" ]  && { echo "Error: -i INPUT required" >&2; exit 1; }
[ -z "$OUTPUT" ] && { echo "Error: -o OUTPUT required" >&2; exit 1; }

# Derive target fps from input rate
case "$RATE" in
  29.97) FPSFILT="fps=24000/1001" ;;
  30)    FPSFILT="fps=24" ;;
  25)    FPSFILT="fps=24" ;;
  *)     echo "Unknown rate $RATE; expected 29.97, 30 or 25" >&2; exit 1 ;;
esac

# Build junk-edge args (only if PAD>0)
JUNK_ARGS=""
if [ "$PAD" -gt 0 ]; then
  JL=$(( (PAD + 7) / 8 ))   # units of 8 px
  JR=$JL
  JT=$(( (PAD + 1) / 2 ))   # units of 2 lines
  JB=$JT
  JUNK_ARGS=":jl=${JL}:jr=${JR}:jt=${JT}:jb=${JB}"
fi

# Assemble filter chain
VF="pullup=sb=${SB}:mp=${PLANE}${JUNK_ARGS},${FPSFILT}"
CMD=(ffmpeg -i "$INPUT" -vf "$VF" -c:a copy "$OUTPUT")

if $DRYRUN; then
  echo "[DRY RUN] ${CMD[*]}"
  exit 0
fi

# --- Pre-run probe ---
echo "=== INPUT probe ==="
ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate,field_order \
  -of default=noprint_wrappers=1 "$INPUT"

# Run conversion
echo "=== Running: ${CMD[*]} ==="
"${CMD[@]}"

# --- Post-run probe ---
echo "=== OUTPUT probe ==="
ffprobe -v error -select_streams v:0 \
  -show_entries stream=r_frame_rate,field_order \
  -of default=noprint_wrappers=1 "$OUTPUT"

echo "Done. Compare field_order and r_frame_rate above."
echo "Expected output: field_order=progressive, r_frame_rate≈24000/1001 or 24/1"
echo "If combing remains: raise sb toward 1. If frames drop in action: lower sb."