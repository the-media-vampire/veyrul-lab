# Verdict sheet

**Run ID:** RUN001  
**Evaluator initials:** ___  
**Date:** ___

## Technical observations (falsifiable)

| Question | Config A | Config B |
|---|---|---|
| Label centroid at visual midpoint of segment? (Y/N per bar: 1,2,3,4) | | |
| Any label clipped by bar boundary? | | |
| White text legible at arm's length? | | |
| Shortest bar: label still fits? | | |

## Decision: does `stackY2({y: "midpoint"})` place labels at the visual midpoint?

- [ ] **PASS** — all 4 bars in Config B land at midpoint; Config A does not.
- [ ] **PARTIAL** — some bars pass, record which failed and direction (high/low).
- [ ] **FAIL** — midpoint placement is not distinguishable from Config A baseline.
- [ ] **INDETERMINATE** — could not render or bars too short to judge.

**Verdict:** ___  
**Reason:** ___

## What this does not settle

A PASS here confirms the documented claim for this dataset only.
Short bars (height < font-size in px) may still clip labels — that is a
separate open question from art_01M6MH8DFE1KD1GQA0A0VTGENT r3.