#!/usr/bin/env bash
# graph_check.sh — signalstats + drawgraph with pre-pass range probe
# Source: art_01M6WKQRQ6EZX1MWKZ4H6AF7MM r1 (Veyrul)
# Usage: ./graph_check.sh <input> [min] [max] [output]
# Defaults: min=0 max=255 output=graph.mp4

set -euo pipefail

INPUT="${1:-}"
MIN="${2:-0}"
MAX="${3:-255}"
OUTPUT="${4:-graph.mp4}"

if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 <input> [min] [max] [output]" >&2
  exit 1
fi

echo "=== Pre-pass: probing actual YAVG range ==="
echo "(reads every frame; may be slow on long clips)"

# Dump lavfi.signalstats.YAVG values via ffprobe
ffprobe -f lavfi \
  -i "movie=${INPUT},signalstats" \
  -show_entries frame_tags=lavfi.signalstats.YAVG \
  -of csv=p=0 \
  2>/dev/null | awk '
    BEGIN { mn=99999; mx=-99999; n=0 }
    /^[0-9]/ {
      v=$1+0; n++
      if (v < mn) mn=v
      if (v > mx) mx=v
    }
    END {
      if (n==0) { print "No YAVG values found — check that input path is correct"; exit 1 }
      printf "Frames sampled : %d\n", n
      printf "Observed YAVG  : min=%.2f  max=%.2f\n", mn, mx
    }
  '

echo ""
echo "Graph will use  : min=${MIN}  max=${MAX}"
echo "Recommendation  : if observed range falls outside [${MIN},${MAX}], adjust before rendering."
echo ""

# Confirm before rendering
read -rp "Proceed with rendering? [y/N] " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted. Adjust min/max and re-run."
  exit 0
fi

echo "=== Rendering graph ==="
ffmpeg -i "$INPUT" \
  -vf "signalstats,drawgraph=lavfi.signalstats.YAVG:min=${MIN}:max=${MAX}:size=1280x256" \
  -an "$OUTPUT"

echo ""
echo "Output: $OUTPUT"
echo "Verify: graph line should stay within the frame for most frames if min/max matches observed range."