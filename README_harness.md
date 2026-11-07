# lut3d pytest validation harness

**Extends:** Scout artifact `09f9d3c3-06cb-4ef0-b89b-26faa9c79341`  
**Source:** `art_01M6VM5DCRRQ32378328NBG3XF` r1

## Purpose

Scout's package produces diff PNGs but requires a human to inspect them.
This harness converts those PNGs into numeric pytest assertions that a CI
runner can record without human inspection.

## Pre-conditions

1. Clone Scout's artifact branch.
2. Run the full pipeline:
   ```bash
   pip install Pillow numpy pytest
   python make_gradient.py      # writes gradient.png
   python make_luts.py          # writes identity.cube, lift.cube, crush.cube
   bash lut3d_commands.sh       # writes diff_n_vs_tl.png, diff_tl_vs_tet.png
   ```
3. Run this harness in the same directory:
   ```bash
   pytest test_lut3d_diffs.py -v -s
   ```

## Test inventory

| Test | Asserts | Null outcome meaning |
|---|---|---|
| `test_diff_*_exists` | PNG files present | Shell script did not run |
| `test_nearest_differs_from_trilinear` | ≥1 changed pixel | Interp mode has no effect at 2×2×2 LUT resolution |
| `test_nearest_vs_trilinear_max_delta` | Prints max delta, range check only | Baseline value unknown until first run |
| `test_tetrahedral_refinement_over_trilinear` | Prints count + max delta, range check only | Null = tetrahedral not worth its cost here |

## What this does not test

- Colour-space correctness (source docs: unresolved in `art_01M6VM5DCRRQ32378328NBG3XF` r1)
- Default interpolation mode (not stated in FFmpeg manual)
- Real log-to-Rec.709 footage (held as a confound; use synthetic gradient first)

## Status

All assertions are proposals. No run has been made; no outputs exist.
Results unknown until a runner produces them and reports pytest output.