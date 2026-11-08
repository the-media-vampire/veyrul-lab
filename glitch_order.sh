#!/usr/bin/env bash
# glitch_order.sh — two-stage frame-order adapter
# Stage 1: shuffleframes (deterministic pattern)
# Stage 2: random (stochastic cache-flush, repeatable by seed)
#
# INTERFACE CONTRACT
#   Input  : any file ffmpeg can open
#   Output : scrambled video, audio preserved but visually desynced
#   Caller supplies: INPUT OUTPUT PATTERN FRAMES SEED
#
# ASSUMPTIONS (explicit gaps — none of these have been run)
#   A1. Both filters accept YUV420P without an intervening format= node.
#       If A1 fails: add -vf "format=yuv420p" between the two stages.
#   A2. shuffleframes group size equals length of PATTERN space-list.
#       If A2 fails: index-out-of-range error; recount your indexes.
#   A3. FRAMES is in [2..512]; SEED is in [0..4294967295].
#       If A3 fails: option rejected; clamp to documented range.
#   A4. Audio sync is intentionally sacrificed (video-only filters).
#       Treat audio as a separate editorial decision.
#
# PROVENANCE
#   random filter  : art_01M6WKWX6WYYPNCT7F4YH6PBJR r1
#   shuffleframes  : art_01M6VXBW50KTPRXQ4YVYMRHPSQ r1
#   Both source from FFmpeg Filters Documentation (ffmpeg.org), read as text.
#   No command in either source was run; no output has been observed.

set -euo pipefail

INPUT="${1:-in.mp4}"
OUTPUT="${2:-out.mp4}"
PATTERN="${3:-0 2 1}"     # shuffleframes mapping (quoted, space-separated)
FRAMES="${4:-8}"           # random cache size [2..512]
SEED="${5:-42}"            # random seed [0..4294967295]

ffmpeg -i "$INPUT" \
  -vf "shuffleframes=${PATTERN},random=frames=${FRAMES}:seed=${SEED}" \
  "$OUTPUT"