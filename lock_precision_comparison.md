# Lock-precision comparison: seconds-only vs seconds+frame-number

**Source:** art_01M6A5NN0JFR92YNZ3YG1V3B85 r1  
**Variant being tested:** "Compare a lock written only in seconds with one written in seconds and frame numbers, and compare the stills on both sides of the gap against the input."

## Setup (fill in before running)

| Field | Prompt A (seconds only) | Prompt B (seconds + frames) |
|---|---|---|
| Clip length (s) | | |
| Frame rate (fps) | | |
| Total frame count | | |
| Lock start (s) | | same |
| Lock end (s) | | same |
| Lock start (frame #) | — | |
| Lock end (frame #) | — | |
| Model label | | |

## Still comparison rows (one row per sampled still)

| Still # | Time (s) | In locked range? | A: matches input? | B: matches input? | Notes |
|---|---|---|---|---|---|
| 1 | | | MATCH / MISMATCH / AMBIGUOUS | MATCH / MISMATCH / AMBIGUOUS | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Viewer length check:** Record the viewer's displayed length for both outputs. If it differs from the written length, no still can be tied to a specific frame number (per the gap-fill finding in the source record).

| | Prompt A | Prompt B |
|---|---|---|
| Written length (s) | | |
| Viewer displayed length (s) | | |
| Usable frame-number alignment? | yes / no | yes / no |

## What to report
- How many locked-range stills matched / mismatched / were ambiguous in each prompt
- Whether the viewer length matched the written length (prerequisite for frame-number claims)
- One honest sentence on whether the added frame-number precision changed anything visible

## What this cannot show
- Whether the locked frames are pixel-identical to the input (requires opening the input clip and diffing)
- Motion or cuts between sampled stills
- Audio alignment