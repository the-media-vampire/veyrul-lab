# Learning-Path Experiment: Cheatsheet vs. Header Scan

**Source:** art_01M6Q6PZWS3BYDS2A1RZQB7E0H r1 | FAQ lines 43, 45, 103; README line 125
**Commit pinned:** 4bfb72d
**Status:** design-only; not compiled or run

## Intention
The FAQ names the cheatsheet as a primary reference (line 43) and the header
or source as a teaching aid (line 103). The experiment tests whether these two
paths produce different first-attempt correctness for three specific calls:

  1. DrawTextureRec (texture rendering)
  2. DrawTextPro (text with rotation)
  3. GenTextureCellular (procedural texture)

## Conditions

| | Condition C (Cheatsheet) | Condition H (Header) |
|---|---|---|
| Reference | raylib.h cheatsheet PDF / HTML | raylib.h raw header, grep-only |
| Task | Write a minimal compilable call for each of the 3 functions | Same |
| Allowed time | 5 minutes per function | 5 minutes per function |
| Output | attempt_c_{fn}.c | attempt_h_{fn}.c |

## Fixed variables
- raylib commit 4bfb72d (same as source record)
- Compiler: gcc with -lraylib, no IDE autocomplete
- Window: 320x240, same InitWindow/CloseWindow scaffold (scaffold.c)
- Judge: compile_check.sh; pass = zero compiler errors

## Discriminating outcome
- If error rates differ by function: the gap identifies which calls the
  cheatsheet covers well vs. poorly — actionable for example authors.
- If rates are equal: cheatsheet and header are interchangeable starting
  points for these calls; the FAQ's preference is a style choice only.
- If Condition H wins on any call: the header's type signatures are more
  precise than the cheatsheet summary — worth noting in example CONVENTIONS.

## What would change our conclusion
A single function where Condition C succeeds but Condition H fails (or vice
versa) is more informative than aggregate pass rates.