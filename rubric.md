# Scoring Rubric — GIF Dither Experiment

Source: art_01M6TXQ4AJ3RFQYC0DGQHJ20SG revision 1

## What is held fixed
- Input clip, trim length, scale (320px wide), fps (15), max_colors (256), stats_mode=full
- One shared palette (palette_shared.png) used for all four outputs

## Variable under test
dither = none | bayer (scale 3) | sierra2 | sierra2_4a

## Falsifiable predictions to check
1. `none` will show the most visible banding on smooth gradients.
2. `bayer` will show a regular crosshatch pattern on flat areas; it should be smallest or similar in size to `none`.
3. `sierra2` and `sierra2_4a` will appear smoother on gradients but may show a moving noise pattern on still areas.
4. File size ordering (largest to smallest) is predicted: sierra2 >= sierra2_4a > bayer >= none.

## Technical observations (record separately from taste)
| Treatment | File size (KB) | Banding visible? | Pattern visible? | Transparency OK? |
|-----------|---------------|-----------------|-----------------|------------------|
| none      |               |                 |                 |                  |
| bayer_s3  |               |                 |                 |                  |
| sierra2   |               |                 |                 |                  |
| sierra2_4a|               |                 |                 |                  |

## Discriminating test
If file sizes do NOT follow prediction 4, that is informative:
- Smaller error-diffusion file would suggest the specific clip has low temporal variation.
- Larger bayer file would suggest the crosshatch pattern confuses GIF LZW compression.

## Taste judgments (record separately)
Note preferred output and why, after filling the technical table.

## Repeat with stats_mode=diff if background is mostly static
Change STATS_MODE=diff in the script; keep all other variables fixed.
Compare palette_shared.png visual appearance between runs.