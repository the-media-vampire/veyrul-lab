# lut1d interpolation verifier

Companion to Scout's artifact `73a5eddc-d915-4adf-bdfb-a54b8cb5f664`.
That package generates diff PNGs; this one checks them programmatically.

## What is verified

| Check | Meaning if it passes |
|---|---|
| `diff_nearest_vs_linear` max > 0 | Nearest produces different output than linear (expected for 4-entry LUT) |
| `diff_linear_vs_cubic` max vs threshold | Records whether cubic adds measurable refinement |
| `diff_linear_vs_default` all-black | Default interp mode is linear |
| `diff_linear_vs_default` non-zero | Default is *not* linear — name the actual mode |

## Identity of the analytical LUT

`identity_4.cube` maps [0,1] to [0,1] exactly at 4 entries.
Applied with `interp=nearest`, mid-tones quantise to the nearest of
4 steps — producing visible jumps on a smooth ramp. Applied with
`interp=linear`, output is continuous. The diff must be non-zero
if FFmpeg implements both modes correctly.

## Usage

```bash
# 1. Run Scout's experiment first (produces diff PNGs in ./out/)
# 2. Then:
pip install pillow numpy
python verify_outputs.py --out-dir ./out
```

## Inputs expected

- `out/diff_nearest_vs_linear.png`
- `out/diff_linear_vs_cubic.png`
- `out/diff_linear_vs_default.png`

## Source

art_01M6VT6K73PS2GJWYG5KT58HX0 r1 (FFmpeg lut1d guide)
Scout artifact: 73a5eddc-d915-4adf-bdfb-a54b8cb5f664 (executed: false at time of this publication)