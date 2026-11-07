# Stop-and-substitution / reversal: interface contract for AI video review

**Source:** art_01M6Q7X8AYY9CB2Y8T6ECAGEW8 r1 (eBook 67972, Talbot 1914, via Project Gutenberg)  
**Status:** Curator analysis, untested. No film viewed, no AI output evaluated, no model named.  
**License:** MIT

## What this is

A minimal integration contract mapping two mechanisms from Talbot's 1914 book on moving pictures to concrete review checkpoints for AI-generated video.

**M1 — Stop-and-substitution:** Camera stops; all non-leaving subjects hold their last-exposed position; a substitute steps in or out; camera restarts.  
**M2 — Reversal:** Action photographed forward; film ordered so last frame plays first (or camera run backward). The book's worked example has a wording disagreement between line 8139 (camera route) and caption lines 8078–8079 (projector route); this contract notes but does not resolve it.

## Interface

```
Inputs:  subject_count, intended_effect, review_unit
Outputs: checkpoints_applicable, cannot_check
```

**intended_effect** values: `substitution` | `disappearance` | `reversal` | `return`  
**review_unit** values: `single_still` | `frame_sequence` | `playback`

## Key invariants

- **Hold-position (M1):** Every non-leaving subject must occupy the same position on both sides of the cut. Drift is the failure signature. *Cannot be checked in a single still.*
- **Full-direction (M2):** Motion direction must be inverted across all frames. Partial inversion is the failure signature. *Requires playback.*

## Explicit gaps

See `explicit_gaps` in `contract.json`. The main ones for AI video:
1. AI interpolation may produce continuous drift rather than a discrete stop — the book's invariant assumes a hard stop.
2. Which reversal route (frame-reorder vs. latent-space inversion) any given AI tool uses is not addressed here.
3. No frame-count minimum is given; no audio claim is made.

## What is NOT here

- Frame-rate / slow-motion / time-lapse mechanisms (covered separately)
- Any claim about replacing a real person, face, voice or likeness
- Any claim that a stop is undetectable in AI output