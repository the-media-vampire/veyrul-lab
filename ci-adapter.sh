#!/usr/bin/env sh
# ci-adapter.sh — thin POSIX adapter between tt3.config.json and Tweego.
# Mirrors the build section of the extension so CI reproduces the same output.
# USAGE: sh ci-adapter.sh [--test]
#
# INTERFACE CONTRACT
#   Input  : src/**/*.twee + .storyformats/<format>-<major>-<minor>-<patch>/format.js
#   Output : build/my-story.html   (matches outputFilename above)
#   Env    : TWEEGO_PATH points to the tweego binary; STORY_FORMAT names the format
#
# ASSUMPTIONS (must hold for parity with the extension build)
#   1. Tweego version supports the same Twee 3 subset as the extension.
#   2. .storyformats/ layout is formatname-x-y-z/format.js — same as extension convention.
#   3. Passages tagged Twine.private must be stripped BEFORE invoking Tweego if the
#      pipeline needs to honour that tag; Tweego itself does not know the tag.
#   4. disabledDiagnostics has no Tweego equivalent — linting is extension-only.

set -eu

TWEEGO="${TWEEGO_PATH:-tweego}"
FORMAT="${STORY_FORMAT:-chapbook}"
OUT_DIR="build"
OUT_FILE="my-story.html"
SRC="src"
FORMAT_DIR=".storyformats"
TEST_FLAG=""

if [ "${1:-}" = "--test" ]; then
  TEST_FLAG="--test"
fi

mkdir -p "$OUT_DIR"

# Strip Twine.private passages via a simple grep-based pre-filter.
# WARNING: this is line-oriented and fragile for nested content; see ASSUMPTIONS.
TMPSRC=$(mktemp -d)
trap 'rm -rf "$TMPSRC"' EXIT
for f in "$SRC"/*.twee "$SRC"/**/*.twee 2>/dev/null; do
  [ -f "$f" ] || continue
  # Passages beginning :: Name [Twine.private ...] are dropped block-by-block.
  python3 - "$f" "$TMPSRC/$(basename $f)" <<'PY'
import sys, re, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
passages = re.split(r'(?m)^(?=::)', src)
kept = [p for p in passages if 'Twine.private' not in p.split('\n')[0]]
pathlib.Path(sys.argv[2]).write_text(''.join(kept))
PY
done

"$TWEEGO" \
  --format="$FORMAT" \
  --format-dir="$FORMAT_DIR" \
  --output="$OUT_DIR/$OUT_FILE" \
  $TEST_FLAG \
  "$TMPSRC"

echo "Built: $OUT_DIR/$OUT_FILE"