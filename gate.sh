#!/usr/bin/env bash
# music-model-ci-gate/gate.sh
# Usage: gate.sh record.json [check_decision_v5.py]
# Exit 0 only if checker exits 0 (complete + go).
# Wraps check_decision_v5.py for CI pipelines.
# Source: art_01M6SQH2ECQZH73P9EP9XHKB47 r1
set -euo pipefail

RECORD="${1:-record.json}"
CHECKER="${2:-check_decision_v5.py}"

if [[ ! -f "$RECORD" ]]; then
  echo "GATE ERROR: record not found: $RECORD" >&2
  exit 2
fi
if [[ ! -f "$CHECKER" ]]; then
  echo "GATE ERROR: checker not found: $CHECKER" >&2
  exit 2
fi

# Run checker; capture output and exit code without aborting on non-zero.
set +e
OUTPUT=$(python3 "$CHECKER" "$RECORD" 2>&1)
CODE=$?
set -e

echo "$OUTPUT"

if [[ $CODE -eq 0 ]]; then
  echo "GATE: PASS — record is complete and decision is go."
else
  echo "GATE: BLOCK (exit $CODE) — resolve errors above before release." >&2
  exit "$CODE"
fi