#!/usr/bin/env bash
# denoise_adapter.sh — shared interface for vaguedenoiser and hqdn3d
# Source: art_01M6VYVD4GZ3456R6E6S083BCM r1 (vaguedenoiser, documented options)
# hqdn3d options assembled from FFmpeg filters documentation.
# NO COMMAND WAS RUN. All filter chains are illustrative.
#
# Usage:
#   ./denoise_adapter.sh INPUT OUTPUT DENOISER STRENGTH
#   DENOISER: vague | hqdn3d
#   STRENGTH: low | mid | high
#
# Shared interface contract:
#   - INPUT:    any file ffmpeg can open
#   - OUTPUT:   new filename per trial (never overwrite source)
#   - DENOISER: selects filter; both operate per-frame on luma+chroma
#   - STRENGTH: maps to documented parameter ranges; see table below
#
# Strength mapping (source-documented defaults/ranges only):
#
# | Strength | vaguedenoiser              | hqdn3d                     |
# |----------|----------------------------|----------------------------|
# | low      | threshold=1:method=garrote | luma_spatial=2:chroma=1    |
# | mid      | threshold=2:method=garrote | luma_spatial=4:chroma=3    |
# | high     | threshold=4:method=soft    | luma_spatial=8:chroma=6    |
#
# Key assumption: both filters accept RGB24 or YUV420P without an
# explicit format= node. Verify on your FFmpeg build; a format mismatch
# produces an option error or silent no-op (untested, evidence gap).

set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"
DENOISER="${3:-vague}"
STRENGTH="${4:-mid}"

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "Usage: $0 INPUT OUTPUT [vague|hqdn3d] [low|mid|high]" >&2
  exit 1
fi

case "${DENOISER}:${STRENGTH}" in
  vague:low)  VF="vaguedenoiser=threshold=1:method=garrote" ;;
  vague:mid)  VF="vaguedenoiser=threshold=2:method=garrote" ;;
  vague:high) VF="vaguedenoiser=threshold=4:method=soft" ;;
  hqdn3d:low)  VF="hqdn3d=luma_spatial=2:chroma_spatial=1" ;;
  hqdn3d:mid)  VF="hqdn3d=luma_spatial=4:chroma_spatial=3" ;;
  hqdn3d:high) VF="hqdn3d=luma_spatial=8:chroma_spatial=6" ;;
  *) echo "Unknown DENOISER or STRENGTH" >&2; exit 1 ;;
esac

echo "[dry-run] ffmpeg -i '$INPUT' -vf '$VF' '$OUTPUT'"
# Remove 'echo' and the quotes around the command to execute for real.
# Record your FFmpeg version: ffmpeg -version