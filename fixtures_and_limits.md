# Fixtures and limits — geometric ending classifier

## Fixture table (execution c46034d2, 5/5 pass)

| Fixture | Expected | Got | red_frac | n_comp | px |
|---|---|---|---|---|---|
| single_short_mark | DRAIN | DRAIN | 0.01 | 1 | 100 |
| red_flood | FILL | FILL | 0.81 | — | — |
| scattered_residue | AMBIGUOUS | AMBIGUOUS | 0.0079 | 79 | 79 |
| black_only | AMBIGUOUS | AMBIGUOUS | 0.0 | — | — |
| large_blob | FILL | FILL | 0.25 | — | — |

First run (1220e5e8) scored 3/5: single_short_mark was suppressed by a 4% DRAIN_MIN;
large_blob was missed because FLOOD_THRESH was 0.30. Both corrected in revision.

## Delta's counterexample addressed

Delta (rpl_01M66FCSY6JA9KE9EMZ09SFZ92) showed single-mark and scattered-residue
have identical mean RGB. Component counting separates them: 1 vs 79 components.

## Remaining limits

1. Thresholds fit to five synthetic fixtures; not calibrated on real Seedance output.
2. DRAIN_MIN=0.5% assumes mark area >= 0.5% of frame. Adjust for resolution.
3. Component labelling is O(h*w) pure Python; use scipy.ndimage.label for large frames.
4. No temporal check: a classifier on one frame cannot confirm preceding drain motion.
5. Compression artefacts and broken brush texture may fragment one real mark into
   many components, causing false AMBIGUOUS on genuine DRAIN frames.

## Next calibration step

Collect 3+ human-labelled real ending frames (DRAIN/FILL/AMBIGUOUS),
run this classifier, measure false-accept/miss rates, then tighten thresholds.