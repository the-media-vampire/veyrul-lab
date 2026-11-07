#!/usr/bin/env bash
# hf CLI dry-run filter comparison
# Source: art_01M6V3QCJ14FJA43G1632JNGJS revision 1
# Usage: REPO=OWNER/REPO REV=<commit> bash run_experiment.sh
# Requires: hf (huggingface_hub)

set -euo pipefail

REPO="${REPO:-OWNER/REPO}"
REV="${REV:-main}"   # replace with a commit hash for reproducibility
OUT_DIR="${OUT_DIR:-hf_dryrun_experiment}"

mkdir -p "$OUT_DIR"

echo "=== Arm A: --include only ==="
hf download "$REPO" --include "*.gguf" --revision "$REV" --dry-run \
  2>&1 | tee "$OUT_DIR/arm_a.txt"

echo ""
echo "=== Arm B: --include + --exclude ==="
hf download "$REPO" --include "*.gguf" --exclude "*fp16*" --revision "$REV" --dry-run \
  2>&1 | tee "$OUT_DIR/arm_b.txt"

echo ""
echo "=== Summary lines ==="
grep -E '(files|bytes|MB|GB|Total)' "$OUT_DIR/arm_a.txt" "$OUT_DIR/arm_b.txt" || true

echo ""
echo "=== Diff (empty = identical output) ==="
diff "$OUT_DIR/arm_a.txt" "$OUT_DIR/arm_b.txt" && echo "[no differences]" || true

echo ""
echo "hf version: $(hf --version 2>/dev/null || echo 'unknown')"
echo "Results saved to $OUT_DIR/"