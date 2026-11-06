# Integration contract: Finger Ch. VII × Agents' Room

## Sources
- `art_01M6QAW180YXK0WCS8SFGHTSGD` r1 — Finger, *Hints on Writing Short Stories*, Ch. VII (Gutenberg 76438)
- `art_01M6H154J7KBB907MQWZ73VV2F` r2 — Agents' Room (arXiv 2410.02603)

## The mechanism gap

Agents' Room runs planning agents in an order the paper does not constrain within the planning phase:
`conflict → character → setting → plot` (Section 4.1 role table).

Finger Ch. VII (lines 843–846, art_01M6QAW180YXK0WCS8SFGHTSGD r1) states the author's ordering:
1. Create a character first.
2. Supporting characters follow.
3. A situation grows out of them — that situation *is* what the author means by plot.

The structural question: **what changes if the planning-agent execution order is constrained to character-first, and if plot is explicitly derived from a situation that emerges from characters?**

In the default Agents' Room setup, `conflict` runs before `character`. Finger's ordering inverts this: character precedes conflict, which is itself a situation produced by character interaction. The two orderings encode different causal assumptions about story origin.

## Proposed constrained initialization

```
Default order:   conflict → character → setting → plot
Proposed order:  character → conflict → setting → plot
```

Mechanism: the orchestrator already controls agent call order (Section 3). No architectural change is needed; only the call sequence changes. The `character` agent writes to the scratchpad first; the `conflict` agent reads that output before writing.

## Proposed scratchpad field: PLAUSIBILITY_GATE

Finger Ch. VII (lines 933–937, 952–953) dismisses warnings about improbability, holding that a good story holds regardless of subject (ancient reptiles, fairies, devils, angels). This is a **permissive plausibility stance**: the author's claim is that subject-matter improbability does not cause rejection.

Agents' Room has no plausibility field on the scratchpad. A `PLAUSIBILITY_GATE` entry, written by the `character` or `plot` agent and read by writing agents, would make the stance explicit and testable:

```yaml
PLAUSIBILITY_GATE:
  stance: permissive          # or: realistic | genre-constrained
  justification: >            # character-grounded or genre-grounded
    Character X is established as [trait]; the situation that follows
    is a consequence of that trait, not of the external world's rules.
  applies_to: [rising_action, climax, falling_action]
```

Writing agents read `PLAUSIBILITY_GATE.stance` to calibrate whether to flag internal inconsistency or proceed. Without it, each writing agent defaults to its backbone model's implicit plausibility assumptions — which may or may not align with the plan.

## Interface summary

| Interface point | Finger Ch. VII contract | Agents' Room default | Change required |
|---|---|---|---|
| Planning order | character → situation → plot | conflict → character → setting → plot | Reorder orchestrator call sequence |
| Plot origin | derived from characters and situation | outlined as a planning step | `plot` agent prompt reads `character` output first |
| Plausibility stance | explicit, permissive, character-grounded | implicit (backbone model default) | Add `PLAUSIBILITY_GATE` scratchpad field |
| Conflict source | emerges from character interaction | defined first, before characters | Conflict agent reads character scratchpad before writing |