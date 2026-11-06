# Preview-selection bias probe

**Status:** not executed — experiment brief only
**Source:** art_01M6J3737RQHC1XQ593SN67ZMS r3 (arXiv 2609.12769v3, CC BY 4.0)
Attribution: Nath, Ferres, Petrović, Schulz.

## Paper claim under test

Task 1 (Preview): two model calls — label each scene with a narrative role, then pick a clip satisfying editorial constraints. Evaluated with model judges in a two-alternative clickability test against random and unguided baselines (paper claim, not checked here).

## Untested question

The evaluation does not, as stated, control for scene position. If judges prefer earlier scenes (a known primacy effect in LLM ranking tasks), the role-label step may be decorative: an early "hook" scene wins not because of its role but because of its position.

**Discriminating test:** pit same-role scenes at early vs. late positions. Swap presentation order across pairs to separate prompt-order bias from episode-position bias. Six pairs total — see fixtures.jsonl.

## Decision rules (complete after running)

- P(early) > 0.65 for direct pairs AND P(early) > 0.65 for swapped pairs → prompt-order drives preference
- P(early) > 0.65 for direct pairs AND P(early) < 0.5 for swapped pairs → episode-position drives preference; role label is not the active variable
- P ≈ 0.5 across all pairs → neither bias detected; role may matter but fixture cannot isolate it

## Variables

| Variable | Fixed | Varied |
|---|---|---|
| Narrative role label | same label per pair | — |
| Editorial constraints | duration, dialogue completeness | — |
| Scene position | — | early (pos 1–3) vs. late (pos 8–10) |
| Judge prompt wording | identical across all pairs | — |
| Presentation order | — | swapped in pairs 4–5 |