# Blind Scoring Sheet: Reduction-Ratio Lettering Trial

Companion to `1156693e-c075-46f5-b760-79b34f0cf7b6` (Scout, commit 58d8624).

## What this is
A fillable scoring instrument for the 10-pair blind comparison described in
`checklist.md`. Keeps measurement separate from experiment setup.

## Decision rule (from Scout's brief, reproduced here for self-containment)
> Blind evaluator, 10 paired comparisons, >60% correct identification
> = quality difference real.

That threshold = **7 out of 10** correct identifications.

## Files
| File | Purpose |
|------|---------|
| `scoring_sheet.tsv` | Fill in during the trial; one row per pair |
| `tally.md` | Copy results here; compute pass/fail |
| `notes_template.md` | Freeform observations, kept separate from scores |

## How to run
1. Evaluator receives 10 unlabelled pairs (A=reduced, B=same-size, order randomised).
2. For each pair, record `chosen` (which panel they think is the reduced one) and `confidence` (1=guess, 2=moderate, 3=certain).
3. Scorer fills `correct` column after reveal.
4. Copy totals to `tally.md`.
5. Apply decision rule.

## Source
art_01M6QCDTKQ6Q9D5QFVA01NF6ZM rev 1 (Veyrul). Treatise lines 2437-2449.