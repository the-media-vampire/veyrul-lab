# FFmpeg freezedetect and mpdecimate: threshold contrast commands

**Source:** `art_01M6V5FHGEDS4GN22K8GCZJ0J5` revision 1  
**Status:** Assembled from documented filter options. No command was run; verify against your FFmpeg build.

## Purpose

These commands support creative experiments where the *threshold value* is the expressive choice, not just a technical setting. Two questions drive the contrast:

1. **Freeze detection:** What duration of stillness counts as a hold? (Default 2s vs. 0.5s)
2. **Decimation:** What counts as "different enough" to keep? (Default `hi=768` vs. tight `hi=256`)

## Key documented hazard

`mpdecimate` with tight thresholds can drop genuine slow-motion frames — motion declared redundant by an algorithm calibrated for static compression artifacts. This is noted in the source article. For expressive work, this hazard *is* the point: the tight-threshold version makes the algorithm's indifference to slowness perceptible.

## Workflow

1. Run freeze detection; note `lavfi.freezedetect.freeze_start` timestamps in the log.
2. Run both mpdecimate variants; compare frame counts with `ffprobe`.
3. Play the loose and tight outputs side by side against the original.
4. The difference between loose and tight output is the set of slow-motion frames the algorithm judged dispensable.

## Disagreement worth preserving

- **Freeze as refusal** (Lyra's Treatment A): the held frame chose to stop.
- **Drop as erasure** (Lyra's Treatment B): the machine chose what wasn't worth seeing.
- **Drop as speed judgment** (Jun's Treatment C): the machine chose what wasn't moving fast enough to matter — a subtler, more insidious indifference than a freeze.

These readings are incompatible and productive. The commands here support all three.