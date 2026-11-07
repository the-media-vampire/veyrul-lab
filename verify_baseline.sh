#!/usr/bin/env bash
# verify_baseline.sh
# Tests the claim: lenscorrection=k1=0:k2=0 produces no change.
# Source: art_01M6V5QZG15J2GQABEBQVQ8GBK r1
# NOT EXECUTED — source publication only.
#
# Usage: ./verify_baseline.sh input.mp4
# Requires: ffmpeg with lenscorrection filter, ffmpeg -f md5 support

set -euo pipefail

INPUT="${1:-}"
if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 input.mp4" >&2
  exit 1
fi

# Confirm lenscorrection is available in this build
if ! ffmpeg -filters 2>/dev/null | grep -q 'lenscorrection'; then
  echo "ERROR: lenscorrection filter not found in this FFmpeg build." >&2
  exit 2
fi

echo "FFmpeg version:"
ffmpeg -version 2>&1 | head -1

# Hash the raw decoded video stream of the source
echo "Computing source stream MD5..."
SRC_MD5=$(ffmpeg -i "$INPUT" -map 0:v:0 -f md5 - 2>/dev/null | grep 'MD5=')
echo "Source:   $SRC_MD5"

# Hash the decoded video stream after the no-op filter
echo "Computing k1=0:k2=0 stream MD5..."
NOOP_MD5=$(ffmpeg -i "$INPUT" -map 0:v:0 -vf 'lenscorrection=k1=0:k2=0' -f md5 - 2>/dev/null | grep 'MD5=')
echo "No-op:    $NOOP_MD5"

# Compare
if [[ "$SRC_MD5" == "$NOOP_MD5" ]]; then
  echo "PASS: baseline matches source. Safe to proceed with trial k1 values."
else
  echo "FAIL: hashes differ. Inspect codec/filter-chain before trusting trial results."
  echo "  Source: $SRC_MD5"
  echo "  No-op:  $NOOP_MD5"
  exit 3
fi