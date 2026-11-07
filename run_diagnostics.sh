#!/usr/bin/env bash
# hf CLI failure-mode diagnostic runner
# Source: art_01M6V3QCJ14FJA43G1632JNGJS r1
# NOT EXECUTED — fill in OWNER/REPO and COMMIT_HASH before running.
# Usage: bash run_diagnostics.sh 2>&1 | tee diagnostics_$(date +%Y%m%d_%H%M%S).log

set -euo pipefail

REPO="OWNER/REPO"          # replace
COMMIT="COMMIT_HASH"       # replace with a real commit sha
TIMEOUT_SECS="1"           # intentionally short to trigger failure 3

echo "=== hf version ==="
hf --version 2>&1 || echo "PROBE1_FAILED: hf not found"

echo "=== Failure 2: gated repo dry-run (expect 401 or access denied) ==="
hf download meta-llama/Llama-2-7b --dry-run 2>&1 | head -20 || true

echo "=== Failure 3: forced short timeout ==="
HF_HUB_DOWNLOAD_TIMEOUT="$TIMEOUT_SECS" \
  hf download "$REPO" --dry-run 2>&1 | tail -5 || true

echo "=== Failure 4A: unmatched pattern ==="
hf download "$REPO" --include "*NOMATCH*.gguf" --dry-run 2>&1 || true

echo "=== Failure 4B: broad pattern line count ==="
hf download "$REPO" --include "*.gguf" --dry-run 2>&1 | wc -l || true

echo "=== Failure 5: unpinned vs pinned diff ==="
hf download "$REPO" --dry-run 2>&1 > /tmp/unpinned.txt || true
hf download "$REPO" --revision "$COMMIT" --dry-run 2>&1 > /tmp/pinned.txt || true
diff /tmp/unpinned.txt /tmp/pinned.txt || echo "DIFF_NON_EMPTY: revision matters"

echo "=== done ==="