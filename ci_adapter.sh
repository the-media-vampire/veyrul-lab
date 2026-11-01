#!/usr/bin/env bash
# EffectCraft CI adapter — reference shell wrapper
# License: MIT
# Documented interface only; not run or validated against a live build.
#
# Usage:
#   ./ci_adapter.sh <project.ecproj> <output.mp4>
#
# Assumptions (see contract.md):
#   - effectcraft-cli is on PATH
#   - footage paths in the .ecproj are relative to the project file
#   - EFFECTCRAFT_READ_ROOT and EFFECTCRAFT_WRITE_ROOT env vars optionally
#     override --automation-read-root / --automation-write-root

set -euo pipefail

PROJECT="${1:?Usage: ci_adapter.sh <project.ecproj> <output.mp4>}"
OUTPUT="${2:?}"
READ_ROOT="${EFFECTCRAFT_READ_ROOT:-$(dirname "$PROJECT")}"
WRITE_ROOT="${EFFECTCRAFT_WRITE_ROOT:-$(dirname "$OUTPUT")}"

ec_cmd() {
  # Send a single JSON engine command over the CLI and capture the reply.
  # Returns non-zero if the reply contains "unknown_outcome" or no result key.
  local cmd="$1"
  local reply
  reply=$(echo "$cmd" | effectcraft-cli mcp \
    --automation-read-root "$READ_ROOT" \
    --automation-write-root "$WRITE_ROOT")
  echo "$reply"
  if echo "$reply" | grep -q 'unknown_outcome'; then
    echo "[ec_cmd] unknown outcome for command: $cmd" >&2
    return 1
  fi
}

echo "[ci_adapter] opening project: $PROJECT"
ec_cmd '{"id":"project.open","params":{"path":"'"$PROJECT"'"}}'

echo "[ci_adapter] queuing render to: $OUTPUT"
ec_cmd '{"id":"render.queue","params":{"format":"h264","output":"'"$OUTPUT"'"}}'

echo "[ci_adapter] starting render"
ec_cmd '{"id":"render.start","params":{}}'

echo "[ci_adapter] done — output expected at $OUTPUT"