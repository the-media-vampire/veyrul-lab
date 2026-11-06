# Prompt-State Coverage Auditor

**Pipeline position:** pre-render gate, distinct from:
- `acda5f8b` — field-format gate (pre-authoring)
- `ad06e2e2` — cross-shot sequence gate (post-ledger)

## What it checks
For each `(ShotRecord, prompt_str)` pair: whether the prompt text contains
tokens from the ledger's `character`, `location` and `costume_note` fields.
Returns a `CoverageResult` with ratio and pass/fail per shot.

## Source basis
- `art_01M6H5ADPZ1K46TM3CRGGYVTJK` r3, Stage 3 — first-frame state check
- `art_01M6A19D9WCBJFN6YNNXNTP570` r2 — colour-state slip between prompt and stills

## Limits
- Token-presence, not semantic accuracy.
- Exact string match; paraphrases false-negative (documented in test).
- Does not query any engine; audits authored prompts only.

## Falsifiability
A prompt passing this audit but producing a first-frame state violation
in sampled stills would disprove the coverage claim.

## Next improvement
Replace token presence with Jaccard overlap ratio (same improvement
Forge named for `ad06e2e2`). Both tools share the same paraphrase weakness;
a single fix applies to both.