# Orchestrator patch: inserting the Dialogue-Spec agent

Agents' Room uses a deterministic orchestrator (Section 3 of arXiv 2410.02603).
The patch adds one step between planning and writing phases.

## Modified execution order

```
[Original planning phase]
  1. conflict_agent     → scratchpad[CONFLICT]
  2. character_agent    → scratchpad[CHARACTER]
  3. setting_agent      → scratchpad[SETTING]
  4. plot_agent         → scratchpad[PLOT]

[New step — Dialogue-Spec agent]
  5. dialogue_spec_agent → scratchpad[DIALOGUE_SPEC]
     Input:  scratchpad[CONFLICT], scratchpad[CHARACTER],
             scratchpad[SETTING], scratchpad[PLOT]
     Output: the DIALOGUE_SPEC block from dialogue_spec.md,
             instantiated with any character-voice notes from CHARACTER
             and any tense-moment flags from PLOT.
     This agent can be a prompted LLM or a deterministic template fill.

[Original writing phase — now reads DIALOGUE_SPEC]
  6. exposition_agent        → reads DIALOGUE_SPEC + plan entries
  7. rising_action_agent     → reads DIALOGUE_SPEC (crisis_resources optional)
  8. climax_agent            → reads DIALOGUE_SPEC (crisis_resources required)
  9. falling_action_agent    → reads DIALOGUE_SPEC (crisis_resources optional)
 10. resolution_agent        → reads DIALOGUE_SPEC
```

## Interface assumptions (explicit)

| Assumption | Risk if wrong | Check |
|---|---|---|
| Writing agents accept additional labeled scratchpad sections | Agents ignore unknown labels | Inspect actual agent prompt templates from the paper's appendix (not yet read; research queued) |
| `plot_agent` output names scenes or moments that can be classified as 'tense' | CLIMAX agent cannot know when to apply resource_1 | Read plot agent prompt template |
| Dialogue-Spec agent runs zero-shot (no fine-tuning needed) | Quality gap vs. fine-tuned agents in the paper | Treat as a baseline; fine-tune if evaluation shows gap |
| Dowst's properties are exhaustive for quality dialogue | They are early-20th-century prescriptions, not empirically validated | Use as a checklist, not a guarantee; paper evaluation covers overall story quality, not dialogue specifically |

## What this does NOT fix

- Dialect handling (Dowst says this is a matter of material, not technique;
  the CHARACTER agent is the right place to store dialect notes).
- Amount of dialogue (Dowst names this; the orchestrator currently has no
  word-budget mechanism per section).
- The caution: dialogue quality alone avails nothing if the whole story's
  situations are not built up — that is a planning-phase concern.