# Scoring Rubric — GIF stats_mode Experiment

Source: art_01M6TXQ4AJ3RFQYC0DGQHJ20SG revision 1  
Companion: artifact f20e0b08 (dither isolation experiment, Scout)

## What is held fixed
- Input clip, trim length, scale (320px wide), fps (15), max_colors (256)
- Dither: sierra2_4a (the documented default)
- One palettegen + paletteuse round-trip per mode (no shared palette across modes)

## Variable under test
stats_mode = full | diff | single

## Source definitions (art_01M6TXQ4AJ3RFQYC0DGQHJ20SG r1)
- full: histogram over whole frame
- diff: weights pixels that differ from previous frame (best when background is static)
- single: new histogram per frame

## Discriminating prediction
For a clip where most pixels are static (e.g. screen recording, talking-head):
- `diff` should produce a palette better tuned to moving areas → fewer visible colour errors on motion
- `single` may produce the largest file (new palette per frame → worse LZW runs) or the smallest (tighter per-frame palette matching)
- `full` is a neutral baseline

For a clip with constant motion (e.g. camera pan):
- `diff` and `full` should converge; `single` remains the outlier

## Technical observations (fill from RESULT lines printed by the script)
| Treatment   | GIF size (KB) | Palette PNG size (KB) | Colour errors on motion? | Notes |
|-------------|---------------|-----------------------|----------------------------|-------|
| full        |               |                       |                            |       |
| diff        |               |                       |                            |       |
| single      |               |                       |                            |       |

Record FFmpeg version here: ___
Record clip description (static bg? constant motion?): ___

## Interaction with dither (second-order check)
After completing this table, re-run the same three modes with dither=none.
If file size ordering changes, stats_mode and dither interact on this clip.
This cross-run is NOT controlled by this script; note it as a future experiment.

## Taste judgments (record separately after technical table is complete)
Note which output looks best on motion areas, and which on static areas.