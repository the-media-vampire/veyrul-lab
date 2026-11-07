# lut1d interpolation discriminator

Experiment targeting the open questions in `art_01M6VT6K73PS2GJWYG5KT58HX0` r1:
- FFmpeg manual does not state the default `interp` mode for `lut1d`.
- No command has been run; visual differences between modes are undocumented.

## Design principle
Hold the LUT file fixed. Vary only `interp`. Any pixel difference is caused by the
interpolation mode alone — one confound at a time.

## Files
| File | Role |
|------|------|
| `make_gradient.py` | 512×32 ramp PNG: black→white single-channel (highest banding sensitivity) |
| `coarse_lift.cube` | Hand-written 4-entry 1D cube: heavy lift at shadows, identity at highlights |
| `run_experiment.sh` | 3 renders (nearest / linear / cubic) + 2 pixel-diff composites |
| `README.md` | This file |

## Discriminating test
```
diff_nearest_vs_linear.png  → non-black pixels = nearest ≠ linear on this ramp
diff_linear_vs_cubic.png    → non-black pixels = cubic adds visible refinement vs linear
```
A 4-entry LUT is a worst case: maximum interpolation gaps. If diffs are all-black,
the choice genuinely does not matter at typical table sizes. That is a *useful null*.

## Expected outcomes (proposals until run)
- `nearest`: likely visible stepping on the ramp — documented risk in the article.
- `linear`: smooth monotone ramp — expected baseline.
- `cubic`: may overshoot at the sharp lift knee; watch for values below black.

## Technical observations (taste-free)
- Five modes documented: nearest, linear, cosine, cubic, spline (art_01M6VT6K73PS2GJWYG5KT58HX0 r1).
- Default mode: not stated in the manual. Run without `interp` to discover it empirically.
- Commands assembled from documented option names; the article states the manual gives no examples.

## Taste note (separated)
Linear is the safest starting point for transfer-function LUTs; cubic is worth
testing when the LUT has a smooth knee. These are practitioner conventions, not FFmpeg documentation.