# Cut-map deviation log

**Source:** art_01M6A5NN0JFR92YNZ3YG1V3B85 r1  
**Observed pattern:** In HF-PKG-021 the cut map kept its overall shape but missed direction, head count and one timing by ~1.2–1.6 s.

## How to use
For each written cut entry in your prompt, fill one row. Compare against the closest sampled still at or after the written time.

| Cut # | Written time (s) | Written camera direction | Written head / subject count | Written musical event | Observed time in stills (s) | Observed direction | Observed count | Direction match? | Count match? | Time within 0.5 s? | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | Y/N/AMB | Y/N/AMB | Y/N/no still | |
| 2 | | | | | | | | | | | |
| 3 | | | | | | | | | | | |
| 4 | | | | | | | | | | | |
| 5 | | | | | | | | | | | |
| 6 | | | | | | | | | | | |

## Tally block

| Dimension | Match | Mismatch | Ambiguous | Not verified |
|---|---|---|---|---|
| Camera direction | | | | |
| Subject count | | | | |
| Timing (±0.5 s) | | | | |
| Musical event (audio) | — | — | — | all (requires listening) |

**Baseline comparison:** Run the same clip with an unstructured prompt (no cut times, no directions). Record what you see in the tally. If the cut-map tally has more direction matches than the unstructured tally, the structure is doing something. If not, the cost of writing the map is not paying off in stills.

## What this cannot show
- Whether any cut lands on a musical hit (audio claim; must be listened to separately)
- Motion between sampled stills
- Whether results repeat on a different seed

## Negated-prop check (from HF-PKG-014 finding)
If your prompt negates a prop ("no X"), add a column: "Negated prop visible?" and compare with a positive rewrite ("prop should appear as Y"). The source record found the negated prop drawn anyway in every sampled still.