#!/usr/bin/env bash
# chromahold_trial.sh
# Selective-colour sweep with baseline-first discipline.
# Source: art_01M6VPNKZ6FCHZ0P8HNYSFSFGC r1 (Veyrul)
# NOT executed — source only. Run against your own clip and FFmpeg build.
# Record your FFmpeg version: ffmpeg -version | head -1

set -euo pipefail

# ── CONFIG ────────────────────────────────────────────────────────────────────
INPUT="${1:-in.mp4}"          # first arg or default
COLOR="${2:-red}"             # colour to KEEP (name or hex, e.g. #c0392b)
OUT_DIR="chromahold_out"      # all outputs land here
# ── END CONFIG ────────────────────────────────────────────────────────────────

# Fail early if chromahold is absent from this build
if ! ffmpeg -filters 2>/dev/null | grep -q chromahold; then
  echo "ERROR: chromahold not found in this FFmpeg build. Check your version." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

# ── BASELINE: similarity=0.01 holds almost nothing ────────────────────────────
# Expected result: clip should look almost fully gray.
# If colour bleeds through, the filter is not applying correctly.
echo "[1/4] Baseline (similarity=0.01, blend=0.0) …"
ffmpeg -hide_banner -loglevel warning -i "$INPUT" \
  -vf "chromahold=color=${COLOR}:similarity=0.01:blend=0.0" \
  "${OUT_DIR}/baseline_sim0.01_blend0.0.mp4"

# ── TRIAL SWEEP ───────────────────────────────────────────────────────────────
# Raise similarity until the full object is held.
# Keep blend=0.1 (slight softening) per article guidance on speckled edges.
for SIM in 0.1 0.2 0.3; do
  echo "[sweep] similarity=${SIM}, blend=0.1 …"
  ffmpeg -hide_banner -loglevel warning -i "$INPUT" \
    -vf "chromahold=color=${COLOR}:similarity=${SIM}:blend=0.1" \
    "${OUT_DIR}/sim${SIM}_blend0.1.mp4"
done

echo "Done. Outputs in ${OUT_DIR}/"
echo "Compare baseline to sweep files. Choose the lowest similarity"
echo "that holds the full target object without speckle."