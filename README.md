# MovieAgent shot-plan adapter contract

Source: arXiv 2503.07314v1 (CC BY 4.0, Wu, Zhu and Shou). Plan-field shapes
taken from art_01M6HQ3ZP3450N3AHCA0N7XAJ1 rev 1 (Veyrul reading guide).

## Explicit assumptions
1. Generator accepts free-text prompt; structured API needs a dict serialiser.
2. Character names are stable across all planning levels (bank is single source of truth).
3. Audio/lip-sync are out of scope; subtitle_text carries dialogue as text only.
4. No inter-level confirmation hook - MovieAgent as described lacks one.
   Add a human gate between validate_plan and each generator call if needed
   (cf. VideoClaw six-stage model, art_01M6GRXZP2F7EG4ZA4XXZACHT1 rev 1).
5. Portrait images passed as opaque path strings; not manipulated here.

## What breaks on combination
- Generator with its own identity mechanism (LoRA per actor) conflicts with
  bank slot paths unless assets are shared.
- Chain-of-thought is internal to each planning agent; not in shot output.
  Downstream auditors cannot reconstruct planning rationale from shot entry alone.

## Missing evidence (flagged for research)
- Code repo terms: github.com/showlab/MovieAgent not fetched.
- Generator API schemas (StoryDiffusion, CogVideoX, Magic-Me) not read.
- Whether shot entries are JSON in released code is unknown to this lane.