#!/usr/bin/env bash
# launch_and_export.sh
# Concrete adapter: open a Zettlr profile then export all .md files with Pandoc.
# Documentary skeleton — not run or tested. Adjust DATA_DIR, WORKSPACE, OUTPUT.
#
# Interfaces pinned to contract.json:
#   I1 — DATA_DIR must be absolute; Zettlr owns it while running.
#   I2 — Export runs AFTER Zettlr exits to avoid file-lock / partial-write races.
#   I3 — LaTeX optional; script falls back to DOCX if pdflatex absent.
#
# License: MIT (this script). Zettlr: GPL v3. Pandoc: GPL v2+.
# Zettlr source: art_01M6WJTB83S88GF5B1H8H1V5EP r1, commit f2f20646.

set -euo pipefail

# --- Configuration (edit these) ---
DATA_DIR="/absolute/path/to/ZettlrProfiles/novel"   # I1: must be absolute
WORKSPACE="/absolute/path/to/novel/manuscript"      # I2: where .md files live
OUTPUT_DIR="/absolute/path/to/novel/export"
EXPORT_FORMAT="docx"   # 'docx', 'html', or 'pdf' (pdf needs LaTeX on PATH)

# --- Step 1: Launch Zettlr with isolated profile (foreground; user closes it) ---
echo "[launch_and_export] Opening Zettlr with profile: $DATA_DIR"
echo "[launch_and_export] Close Zettlr when done writing to continue export."
Zettlr "--data-dir=$DATA_DIR"   # I1 contract: absolute path, no tilde
# Script blocks here until Zettlr exits — I2 contract is satisfied automatically.

# --- Step 2: Batch export with Pandoc ---
mkdir -p "$OUTPUT_DIR"

if [ "$EXPORT_FORMAT" = "pdf" ] && ! command -v pdflatex &>/dev/null; then
  echo "[launch_and_export] WARNING: pdflatex not found (I3 unmet); falling back to docx."
  EXPORT_FORMAT="docx"
fi

find "$WORKSPACE" -name '*.md' | while read -r mdfile; do
  base=$(basename "$mdfile" .md)
  outfile="$OUTPUT_DIR/${base}.${EXPORT_FORMAT}"
  echo "[launch_and_export] Exporting $mdfile -> $outfile"
  pandoc "$mdfile" -o "$outfile"
done

echo "[launch_and_export] Done. Outputs in $OUTPUT_DIR"