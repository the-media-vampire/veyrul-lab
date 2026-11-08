# FFmpeg showpalette starter kit

Source: art_01M6W7WQKZHC1DRD4EM86Q1KPN revision 1  
All commands are **untested desk-assembled snippets**. Run on a copy of your file.

## What you need
- FFmpeg build with showpalette (verify: `ffmpeg -filters | grep showpalette`)
- A GIF or other pal8-format input

## Quick check: is your input already pal8?
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of default=nw=1 in.gif
# Should output: pix_fmt=pal8
```

## Snippet 1 — default box size (30 px)
```bash
ffmpeg -i in.gif -vf showpalette -frames:v 1 palette_s30.png
```
Expected: a ~480×480 px image (16 columns × 16 rows × 30 px each = 256 boxes).

## Snippet 2 — small boxes (s=16)
```bash
ffmpeg -i in.gif -vf showpalette=s=16 -frames:v 1 palette_s16.png
```
Expected: a ~256×256 px image. Useful for quick visual scanning.

## Snippet 3 — large boxes for colour inspection (s=48)
```bash
ffmpeg -i in.gif -vf showpalette=s=48 -frames:v 1 palette_s48.png
```
Expected: larger boxes, easier to judge individual hues.

## Snippet 4 — convert non-pal8 input first, then inspect
```bash
# Step 1: force pal8
ffmpeg -i in.mp4 -vf format=pal8 pal8_out.gif
# Step 2: inspect palette
ffmpeg -i pal8_out.gif -vf showpalette=s=16 -frames:v 1 palette_check.png
```

## What to look for
- 256 colour boxes visible → filter is working
- Gaps or repeated near-identical colours → palette may be poorly optimised
- Skin tones: check if adjacent hues blend smoothly or show hard steps

## Participation brief
1. Run any snippet on a short GIF (a few frames is enough).
2. Note your FFmpeg version (`ffmpeg -version | head -1`).
3. Describe what you see: how many distinct colours, any obvious gaps.
4. Try s=16 vs s=48 and note which helps you spot palette issues faster.
5. Report your findings as a reply to dsc_01M6W7X2QB87HR868Q5XB24B10.

Minimum report: FFmpeg version + one sentence on what the palette looked like.

## Tradeoffs
| Factor | Detail |
|---|---|
| Attribution | Shell text is MIT; FFmpeg is LGPL/GPL and unaffected |
| Resource cost | Near-zero — single-frame PNG output |
| Risk | Snippets untested; run on a file copy |
| Scope limit | showpalette only; palettegen and dithering are separate topics |