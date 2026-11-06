# Stack-midpoint observation log template

Pairs with Scout artifact `9bde72a4-f578-496f-8152-5e6179c30175` (commit `4bc4de16`).
Source claim: art_01M6MH8DFE1KD1GQA0A0VTGENT r3, checklist item 7.

## How to use

1. Open Scout's `index.html` in a browser — no build step needed.
2. Fill `run_log.tsv` once per session (one row per config viewed).
3. Fill `verdict.md` after viewing both Config A and Config B.
4. Keep `taste_notes.md` strictly separate from binary scores.

## Decision rule

Config B passes if the text label centroid is visually closer to the bar segment
midpoint than to either edge, judged independently for all four bars.
If any bar fails, record the bar index and the direction of the error (high/low).

## What this does not test

- Rendering on screens with device-pixel-ratio != 1 (record DPR if you can).
- Print or export — browser canvas only.
- Colour contrast ratio — record legibility as a binary (readable Y/N at arm's length).