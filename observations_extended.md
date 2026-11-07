# Observations — Bark Cue vs. Plain (Extended)

Extends: artifact 9307202f (Scout). Source: art_01M6V77FQTNKYX3ANHPCAT5V9N r1.

## Duration log

Run `bash measure_durations.sh >> durations.tsv` after generation.
Paste TSV here or attach file.

| File | Duration (s) | Condition | Run |
|------|-------------|-----------|-----|
|      |             |           |     |

## Per-clip audio observations (fill before listening more than twice)

For each clip, note in order:
1. Was `[sighs]` rendered as: (a) breath/sigh sound, (b) spoken word "sighs", (c) absent, (d) unclear?
2. Is there an audible pause before "Or so"? (yes / no / uncertain)
3. Clip duration vs. condition-mean: shorter / longer / similar?

## Aggregate (fill after all 6 clips)

- Mean duration A_plain:  s
- Mean duration B_cued:  s
- Duration difference (B−A):  s  — positive = cued is longer
- Cue rendered as sound in N of 3 B runs: /3
- Cue rendered as spoken word in N of 3 B runs: /3

## Preference (separate from above)

Which condition would you use in a final cut, and why?

---

## Seed note

The experiment.py in artifact 9307202f does not set a random seed.
Run-to-run variance is therefore the realistic operating variance, not
a controlled variable. Record it; do not average it away.