# Assumptions and failure modes

| Assumption | Source | Breaks if... |
|---|---|---|
| Orchestrator call order is configurable | art_01M6H154J7KBB907MQWZ73VV2F r2 Section 3: orchestrator is deterministic and decides order | Paper's implementation hard-codes order; config not exposed |
| `character` agent output is parseable by `conflict` agent | Scratchpad holds labelled outputs (Section 3) | Character output is unstructured prose with no parseable anchor; conflict agent ignores it |
| `PLAUSIBILITY_GATE` field is read by writing agents | Agents read scratchpad (Section 4.1) | Writing agent prompt templates have a fixed schema that ignores unknown labels (not yet verified — see open_questions.md) |
| Finger's character-first order improves coherence | Stated author belief, art_01M6QAW180YXK0WCS8SFGHTSGD r1 lines 843–846; not tested | Character-first order produces weaker conflicts when conflict is the natural story seed |
| Permissive plausibility stance is beneficial for genre fiction | Finger's claim, lines 933–937; Agents' Room dataset is mostly sci-fi and fantasy (Section 5) | Realistic-fiction prompts in the dataset are penalised by evaluators who expect coherent causality |

## What this contract cannot fix

Finger Ch. VII (lines 904–906, art_01M6QAW180YXK0WCS8SFGHTSGD r1) says the main matter is portraying character — even through a few light touches. The planning-agent interface produces *descriptions* of characters, not the textual moment-to-moment portrayal. That gap lives in the writing-agent phase. This contract addresses planning-order and stance; portrayal quality depends on writing-agent prompt design, which is outside this contract's scope.