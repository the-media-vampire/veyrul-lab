# FFmpeg `untile` layout-mismatch experiment

Source: [art_01M6WJRP34989PAK18DZXCT96V, rev 1](https://veyrul.com/articles/art_01M6WJRP34989PAK18DZXCT96V)

## Intention

The article documents the `untile` filter from the FFmpeg manual but marks every
real result as **Untested**. The highest-information gap is the layout-mismatch
failure mode: the article *infers* that a wrong grid produces cropped or mixed
frames. We want to know whether FFmpeg (a) exits with an error, (b) silently
pads/crops, or (c) produces clearly garbled output — because the fix strategy
differs for each.

## Discriminating question

> Does a layout that does **not** evenly divide the image produce a clean error,
> silent corruption, or visually obvious scrambling?

This is the smallest test that most changes what we know.

## Setup

Create a synthetic sprite sheet with ImageMagick so the grid is ground-truth
known. 5 columns × 5 rows of 64×64 px tiles → 320×320 px PNG.

```sh
# generate labelled tiles and montage them (requires ImageMagick)
bash make_sheet.sh
```

Expected output: `sheet_5x5.png` (320×320 px, 25 tiles, left-to-right top-to-bottom).

## Arms

### Arm A — correct layout (control)
```sh
ffmpeg -r 1 -i sheet_5x5.png -vf untile=5x5 -r 25 arm_a_correct.mkv
```
Expected: 25 frames, each showing a single labelled tile in order.

### Arm B — wrong column count (layout does not divide evenly)
```sh
ffmpeg -r 1 -i sheet_5x5.png -vf untile=4x5 -r 20 arm_b_wrong_cols.mkv
```
4 columns × 5 rows = 20 tiles declared, but 320 px / 4 = 80 px tile width
(320 is divisible by 4, so no remainder). Tile labels will appear misaligned
between declared and actual columns. Record whether output is 20 frames,
25 frames, or an error.

### Arm C — layout that does NOT divide the image evenly
```sh
ffmpeg -r 1 -i sheet_5x5.png -vf untile=3x5 -r 15 arm_c_no_divide.mkv
```
320 px / 3 ≈ 106.67 px — not an integer. This is the precise condition the
article says requires a fix. Record whether FFmpeg errors, floors/ceils the
tile size, or truncates the image.

## Observation checklist (fill in after running)

| Arm | Exit code | Frame count | Tile size in output | Visual match to labels | Notes |
|-----|-----------|-------------|--------------------|-----------------------|-------|
| A (5x5 correct) | | | | | |
| B (4x5 wrong cols) | | | | | |
| C (3x5 no-divide) | | | | | |

## Separating observations from taste

- **Technical observation:** exit code, frame count, measured tile dimensions
  (use `ffprobe`).
- **Taste / interpretation:** whether the garbling is "obvious" or "subtle".
  Record separately; do not let visual impression override the frame count.

## What would change our mind

- If Arm C exits with a clear error → the article's inference about silent
  corruption is wrong; the fix is simply to correct the layout before running.
- If Arm C succeeds silently with garbled output → the article's inferred
  failure mode is real; a pre-flight divisibility check is essential.
- If Arm B and Arm C behave identically → column count matters but integer
  divisibility alone does not predict the failure mode.

## FFmpeg version logging (required)

```sh
ffmpeg -version 2>&1 | head -3
```

Paste result here before filing results.