#!/usr/bin/env bash
# FFmpeg freezedetect and mpdecimate: threshold contrast commands
# Source: art_01M6V5FHGEDS4GN22K8GCZJ0J5 revision 1
# Status: assembled from documented option descriptions; not run
# Record your FFmpeg version before comparing results.

INPUT="in.mp4"

# --- 1. Freeze detection (default thresholds) ---
# noise=-60dB (0.001 as ratio), duration=2s
# Logs lavfi.freezedetect.freeze_start metadata key when picture holds.
ffmpeg -i "$INPUT" -vf freezedetect -f null -

# --- 2. Freeze detection (short freeze sensitivity) ---
# Lower duration catches shorter holds; raise noise to tolerate compression.
ffmpeg -i "$INPUT" -vf freezedetect=noise=0.003:duration=0.5 -f null -

# --- 3. mpdecimate: loose thresholds (default) ---
# hi=64*12=768, lo=64*5=320, frac=0.33
# Drops frames similar to previous; targets compression artifacts.
ffmpeg -i "$INPUT" -vf mpdecimate mpdecimate_loose.mp4

# --- 4. mpdecimate: tight thresholds ---
# hi=64*4=256 — drops frames with very small inter-frame differences.
# CAUTION (source-documented): can drop genuine slow-motion frames.
# Expressive use: makes the algorithm's indifference to slow movement visible.
ffmpeg -i "$INPUT" -vf mpdecimate=hi=256:lo=192:frac=0.2 mpdecimate_tight.mp4

# --- 5. framestep: fixed ratio decimation ---
# Keeps 1 frame every N; default N=1 (no drop). Use N=3 for ~10fps from 30fps.
ffmpeg -i "$INPUT" -vf framestep=step=3 framestep_3.mp4

# --- 6. Frame count comparison (before/after) ---
ffprobe -v error -select_streams v:0 \
  -count_frames -show_entries stream=nb_read_frames \
  -of default=nokey=1:noprint_wrappers=1 "$INPUT"

# Run the same command on mpdecimate_loose.mp4 and mpdecimate_tight.mp4
# to compare frame counts and verify the threshold contrast.