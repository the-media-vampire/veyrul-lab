# yadif_preflight.sh

A shell preflight for FFmpeg `yadif` deinterlacing.

## What it does

- Validates `mode`, `parity` and `deint` options against the documented values.
- Probes the source with `ffprobe` for `r_frame_rate` and `field_order` (if file exists on disk).
- Warns on the three documented failure modes from **art_01M6V6CAXJB89TN8NEH6VQXXDD r1**:
  1. Wrong field order → judder (set `parity=tff` or `parity=bff` explicitly)
  2. `deint=interlaced` leaving combing on unflagged frames
  3. `mode=1` or `mode=3` doubling frame rate unexpectedly
- Prints the derived `ffmpeg` command. **Does not run it.**

## Usage

```sh
bash yadif_preflight.sh input.ts output.mp4 [mode] [parity] [deint]
```

### Examples

```sh
# Default: safe baseline
bash yadif_preflight.sh tape.ts out.mp4

# Double frame rate, known BFF source
bash yadif_preflight.sh tape.ts out_50fps.mp4 1 bff all

# Only process flagged frames (mixed source)
bash yadif_preflight.sh mixed.ts out.mp4 0 auto interlaced
```

## Verification

After running the printed command:
1. `ffprobe out.mp4` — confirm `r_frame_rate` matches expectation.
2. Inspect a moving-edge frame — no combing.
3. Watch a motion sequence — no judder.

## Status

Script logic reviewed by reading; **not executed**. Source: art_01M6V6CAXJB89TN8NEH6VQXXDD r1.

## License

MIT