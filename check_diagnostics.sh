#!/usr/bin/env bash
# check_diagnostics.sh
# Reads diagnostics.json and prints which checks WOULD run after a real sweep.
# SOURCE ONLY — not executed. No video file or ffprobe output is available here.
# Requires: jq, ffprobe (from an FFmpeg build with chromahold)
# Source: art_01M6VPNKZ6FCHZ0P8HNYSFSFGC r1

set -euo pipefail

DIAG_FILE="${1:-diagnostics.json}"

if ! command -v jq &>/dev/null; then
  echo "ERROR: jq required" >&2; exit 1
fi

if ! ffmpeg -filters 2>/dev/null | grep -q chromahold; then
  echo "ERROR: chromahold not in this FFmpeg build" >&2; exit 2
fi

echo "=== Diagnostic plan from $DIAG_FILE ==="
jq -r '.diagnostics[] | "[\(.id)] Symptom: \(.symptom)" +
  "\n       Metric : \(.metric) \(.threshold)" +
  "\n       Fix    : \(.direction) \(.parameter) by \(.step // \"N/A\")" +
  "\n       Note   : \(.threshold_note)"' "$DIAG_FILE"

echo ""
echo "STATUS: plan printed; no video was analysed (source-only artifact)."
echo "To use: run Forge's sweep (artifact b2a44bb3), then pass each output"
echo "to ffprobe and compare metrics against the thresholds above."