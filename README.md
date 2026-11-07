# lut3d interpolation discriminator

Experiment brief for `art_01M6VM5DCRRQ32378328NBG3XF` revision 1.

## Open questions being tested

| # | Question | Why it matters |
|---|----------|----------------|
| Q1 | What is the default interpolation? | The manual does not say; assuming trilinear could silently change results. |
| Q2 | Do nearest / trilinear / tetrahedral produce measurably different pixels on a smooth gradient? | Visible stepping is the documented risk; a pixel-level diff is the discriminating test. |

## Intention vs. contrasting alternative

- **Intention:** apply a colour-transform LUT (lift highlights) with `interp=trilinear` — smooth, commonly expected.
- **Contrasting alternative:** same LUT with `interp=nearest` — cheap, prone to stepping on gradients.

A gradient PNG is used because it maximises the chance of revealing interpolation artefacts.

## How to run

```bash
# 1. Synthesise the gradient test image (requires Python + Pillow)
python3 make_gradient.py

# 2. Run all six command variants (see lut3d_commands.sh)
bash lut3d_commands.sh

# 3. Compare frames
ffmpeg -i out_lift_nearest.png -i out_lift_trilinear.png \
  -filter_complex "[0][1]blend=all_mode=difference,eq=brightness=5" diff_n_vs_tl.png

ffmpeg -i out_lift_trilinear.png -i out_lift_tetrahedral.png \
  -filter_complex "[0][1]blend=all_mode=difference,eq=brightness=5" diff_tl_vs_tet.png
```

## Expected discriminating outcomes

| Outcome | Interpretation |
|---------|----------------|
| diff_n_vs_tl is non-black | nearest differs from trilinear on this gradient — stepping is real |
| diff_tl_vs_tet is all-black | trilinear ≈ tetrahedral here; either is safe for most work |
| diff_tl_vs_tet is non-black | tetrahedral adds visible refinement; worth the extra cost |
| All diffs are black | LUT has insufficient resolution to reveal interpolation differences on this gradient |

## Technical observations (taste-free)

- The FFmpeg manual lists five modes: nearest, trilinear, tetrahedral, pyramid, prism. Default unspecified.
- A synthetic gradient isolates interpolation; a real log clip adds colour-space uncertainty (undocumented in the manual).
- A 2×2 LUT (8 corners only) maximises interpolation gaps; a 33×33×33 LUT reduces them.

## Taste note (separated)

Tetrahedral is widely regarded as the industry default for quality; nearest is for speed inspection only. These are community conventions, not from the FFmpeg manual.