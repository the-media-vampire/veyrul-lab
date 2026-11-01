# Baseline Runs Log

**Instrument:** `run_scoring_sheet.md`  
**Source article:** `art_01M64VKA89R1TZMNK0QSJW990E` revision 2

This log collects run verdicts across multiple fills to enable comparison.

---

| Run label | Date (UTC) | Prompt type | Light source? | Flanking? | Verdict | Sheet filled by |
|---|---|---|---|---|---|---|
| H01-A (historical) | 2026-08-28 | text-only, no seed | slab | both sides | holds | H01 (sampled frames) |
| H01-B (historical) | 2026-08-28 | text-only, no seed | line | both sides | holds | H01 (sampled frames) |
| H01-C (historical) | 2026-08-28 | text-only, no seed | wheel | late frames | holds | H01 (sampled frames) |
| *(next run)* | | | | | | |
| *(next run)* | | | | | | |
| *(next run)* | | | | | | |

**Status:** Three historical rows pre-filled from article observations. These are retrospective; no raw frames available to this task. All subsequent rows require direct viewer fill.

---

## Pattern threshold (proposed)

- **Reliable** if flanking appears in ≥8/12 frames across ≥5 independent runs.
- **Emergent bias** if baseline (no explicit terms) matches controlled (explicit terms) within 10 percentage points.
- **Prompt-driven** if controlled exceeds baseline by >20 percentage points consistently.

These thresholds are proposals; adjust after first three filled sheets.