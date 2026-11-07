#!/usr/bin/env bash
# FFmpeg drawtext starter templates
# Source: art_01M6V6Y1W89GFEMP1VAF0HBY5M r1 (documented patterns, not run here)
# Replace: INPUT, OUTPUT, path/to/font.ttf, and any text values.
# Test on a short clip first: add -t 5 before the output filename.

INPUT="input.mp4"
FONT="path/to/FreeSerif.ttf"   # mandatory when fontconfig is disabled
OUTPUT_CENTRE="out_centre.mp4"
OUTPUT_LOWER="out_lower.mp4"
OUTPUT_TIMED="out_timed.mp4"

# 1. Centred text — from manual centred-text pattern
ffmpeg -i "$INPUT" \
  -vf "drawtext=fontfile='${FONT}':text='Hello world':fontsize=30\
:x=(w-text_w)/2:y=(h-text_h)/2" \
  -c:a copy "$OUTPUT_CENTRE"

# 2. Lower-third — position from arithmetic in art_01M6V6Y1W89GFEMP1VAF0HBY5M r1
#    fontsize=h/30 → 36 px on 1080p; y places text above bottom edge
ffmpeg -i "$INPUT" \
  -vf "drawtext=fontfile='${FONT}':text='Lower Third Label'\
:fontsize=h/30:box=1:boxcolor=black@0.5:boxborderw=5\
:x=(w-text_w)/2:y=(h-text_h*2)" \
  -c:a copy "$OUTPUT_LOWER"

# 3. Timed blink — enable expression from the manual (1 s on, 2 s off in a 3 s cycle)
ffmpeg -i "$INPUT" \
  -vf "drawtext=fontfile='${FONT}':text='Timed caption'\
:fontsize=30:x=(w-text_w)/2:y=50\
:enable=lt(mod(t\\,3)\\,1)" \
  -c:a copy "$OUTPUT_TIMED"

# After running, check:
#   - Text appears where x/y expressions place it
#   - Font matches the named file
#   - Box (if used) covers text with readable contrast
#   - Timed text appears and disappears per the enable expression