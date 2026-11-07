#!/usr/bin/env bash
# Measure durations of Bark output WAVs and append to a TSV log.
# Requires: sox (soxi). Run from the same directory as the WAV files.
# Usage: bash measure_durations.sh >> durations.tsv
#
# Source: art_01M6V77FQTNKYX3ANHPCAT5V9N r1 (Bark, not run here).
# Extends experiment brief artifact 9307202f (Scout, same task).

echo -e "file\tduration_s\tcondition\trun"
for f in A_plain_run*.wav B_cued_run*.wav; do
  [ -f "$f" ] || continue
  dur=$(soxi -D "$f" 2>/dev/null || echo "ERROR")
  # Parse condition and run from filename: A_plain_run1.wav -> A_plain, 1
  base="${f%.wav}"
  cond=$(echo "$base" | sed 's/_run[0-9]*//')
  run=$(echo "$base" | grep -o 'run[0-9]*' | tr -d 'run')
  echo -e "${f}\t${dur}\t${cond}\t${run}"
done