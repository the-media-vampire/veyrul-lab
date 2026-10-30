# Palette-Dominance Scorer

**Source claim:** art_01M64VKGMQ5BD4BMXVFP0VJPZA r2 — in five Seedance 2.5
runs sharing one reference image, the palette stated in the prompt dominated
the reference image's palette in sampled frames.

## What this is
A keyword-based scorer. Give it a reviewer's frame-description string;
it counts stated-palette keyword hits vs. reference-palette keyword hits.
If stated > ref, the scene passes.

## Known limits
- Keyword matching only; synonyms must be listed explicitly.
- The 'drowning stair' scene uses generic colour words ('red', 'black')
  that can appear in both stated and reference descriptions — see the
  disambiguation note in `palette_dominance.py`.
- Five single runs, no seed set, unconfirmed reference-image rights basis
  (per the source article). This is not a benchmark.

## How to use
1. Run a Seedance scene with a stated palette.
2. Write a plain-text frame note describing what colours you see.
3. Paste it into `simulated_frame_desc` for that case.
4. Run `python palette_dominance.py`.
5. PASS = stated palette keywords outnumber reference-bleed keywords.

## Next improvement
Extend `stated_palette` with colour synonyms, or replace keyword matching
with a small colour-name embedding lookup to catch 'scarlet' for 'red'.