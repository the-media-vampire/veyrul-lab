# Assumptions and blockers

## Assumptions made by this contract

A. The picture-side BPM and timecode arithmetic from art_01M6E4H6EE6PTQMRDD7RK3VJTY rev 1
   produces a correct cue length in seconds.
B. seconds_total accepts a float and the model uses it as a conditioning signal;
   the docs describe a continuous Fourier embedding for numbers (art_01M6H81MCK26G0HQBNQPA15WE9 rev 2).
C. seconds_start = 0 is a safe default for a fresh cue; this is the documented example
   default but the semantic is not fully explained.
D. The repository code matches the docs at commit 3241adba; the code was not read.

## Blockers ranked

1. HARD: Model weights licence not read. Cannot redistribute or use the model without it.
2. HARD: seconds_start semantics for non-zero values unknown. Any use beyond 0 is a guess.
3. MEDIUM: Model compliance with seconds_total unverified. Post-generation trimming
   must be planned as a default step, not an exception.
4. MEDIUM: Hit-point encoding has no model field. Prompt-only approach is best effort.
5. LOW: fps clock mismatch (23.976/29.97); solvable with explicit fps parameter.

## Licence provenance

- stable-audio-tools repository: MIT, copyright 2023 Stability AI
  (art_01M6H81MCK26G0HQBNQPA15WE9 rev 2, as the LICENSE file reads).
- Model weights: separate gated licence on Hugging Face; not read.
- This contract: MIT (new original work, no repository code reproduced).