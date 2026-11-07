#!/usr/bin/env bash
# compile_check.sh
# Usage: ./compile_check.sh attempt_c_DrawTextureRec.c
# Outputs: PASS or FAIL + compiler stderr
# NOT run; source-publication only.
set -euo pipefail

SRC="${1:-}"
if [[ -z "$SRC" ]]; then
  echo "Usage: $0 <source_file.c>" >&2
  exit 1
fi

TMPBIN="$(mktemp)"
if gcc -o "$TMPBIN" "$SRC" -lraylib -lm 2>compile_err.txt; then
  echo "PASS: $SRC"
else
  echo "FAIL: $SRC"
  cat compile_err.txt
fi
rm -f "$TMPBIN"