#!/usr/bin/env bash
# adapter.sh — pin a DVC-versioned stem set for a Mixxx session
# Usage: ./adapter.sh <git-ref> [mixxx-profile-dir]
# Example: ./adapter.sh v1.2 ./mixxx-profiles/v1.2
#
# This script is a proposal; it has NOT been run.
# Review assumptions in contract.md before use.

set -euo pipefail

GIT_REF="${1:?Usage: adapter.sh <git-ref> [mixxx-profile-dir]}"
PROFILE_DIR="${2:-./mixxx-profile}"
STEMS_DVC="assets/stems.dvc"

echo "[1/3] Checking out DVC pointer for ref: $GIT_REF"
git checkout "$GIT_REF" -- "$STEMS_DVC"

echo "[2/3] Materialising stems via dvc checkout"
dvc checkout "$STEMS_DVC"

echo "[3/3] Ready. Open Mixxx with isolated profile:"
echo "  mixxx --settingsPath $PROFILE_DIR"
echo ""
echo "WARNING: if Mixxx was previously opened, delete or move"
echo "  $PROFILE_DIR/mixxxdb.sqlite before reopening to force"
echo "  fresh analysis of stem files from the new DVC version."