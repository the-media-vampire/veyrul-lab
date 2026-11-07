#!/usr/bin/env sh
# FFmpeg colorlevels starter snippets
# Source: art_01M6VNF38KWQDSEYGE0CEH1DRN r1 (documentary review; no command was run)
# Ranges: input points -1.0–1.0 (black default 0, white default 1)
#         output points 0–1.0
# Replace INPUT and OUTPUT with your own filenames.
# Record your FFmpeg version alongside results.

INPUT="input.mp4"

# 1. Contrast — stretch washed-out footage (manual example)
ffmpeg -i "$INPUT" -vf "colorlevels=rimin=0.039:gimin=0.039:bimin=0.039:rimax=0.96:gimax=0.96:bimax=0.96" contrast_out.mp4

# 2. Darker — raise input black point
ffmpeg -i "$INPUT" -vf "colorlevels=rimin=0.058:gimin=0.058:bimin=0.058" darker_out.mp4

# 3. Lighter — lower input white point
ffmpeg -i "$INPUT" -vf "colorlevels=rimax=0.902:gimax=0.902:bimax=0.902" lighter_out.mp4

# 4. Brighter — lift output black point
ffmpeg -i "$INPUT" -vf "colorlevels=romin=0.5:gomin=0.5:bomin=0.5" brighter_out.mp4

# 5. Preview with histogram overlay (chain into histogram filter)
# Replace contrast_out.mp4 with whichever output you want to inspect.
ffmpeg -i contrast_out.mp4 -vf "histogram" -frames:v 1 histogram_check.png