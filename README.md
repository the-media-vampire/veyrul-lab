# setpts_preflight.sh

Derives the correct FFmpeg `setpts` multiplier from a desired speed ratio and prints the command.

## Source

`art_01M6TZT9NPFRHNSG1H76FJ9MKZ` revision 1 — documentary review of FFmpeg filters manual.

## Key arithmetic

| Goal | Speed factor | setpts multiplier |
|---|---|---|
| 2× faster | 2.0 | 0.5 |
| Half speed | 0.5 | 2.0 |
| 1.5× faster | 1.5 | 0.667 |

Multiplier = `1 / speed_factor`. A common failure is inverting this.

## Usage

```bash
chmod +x setpts_preflight.sh
./setpts_preflight.sh input.mp4 2.0            # 2x faster
./setpts_preflight.sh input.mp4 0.5 slow.mp4   # half speed
```

## What it does
1. Validates the speed factor is a positive number.
2. Computes the PTS multiplier.
3. Warns if the direction looks like an inversion.
4. Probes source duration with `ffprobe` and prints expected output duration (arithmetic, not measured).
5. Flags the audio-mismatch risk and prints the asetpts equivalent.
6. **Prints the command. Does not run FFmpeg.**

## Limits
- Source only; script not executed here.
- Audio retiming is flagged but not solved (unresolved in source).
- Duration estimate is arithmetic; frame dropping/duplication is not observed.
- Tested logic: multiplier formula and inversion guard only.