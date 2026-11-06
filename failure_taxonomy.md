# Failure Taxonomy — Exit Time Experiment

**Source:** art_01M6N9507MQF429JBTGCB7MNZT rev 2  
**Status:** Pre-run taxonomy. No execution has occurred.

## Why a pre-run taxonomy

A failure taxonomy written before execution prevents post-hoc relabelling of surprising results as expected.  
Each label maps to a distinct next action.

## Labels and next actions

### ET-NOEFFECT
- **Symptom:** Variant C and Variant D show identical timing
- **Interpretation:** Exit Time has no observable effect on conditionless transitions
- **Next action:** Test a *conditioned* transition with Exit Time checked; if the checkbox then has an effect, the conditionless path is a special case
- **Docs gap:** art_01M6N9507MQF429JBTGCB7MNZT rev 2 does not describe this interaction

### ET-IMMEDIATE
- **Symptom:** Both variants fire at or near frame 0 of Idle
- **Interpretation:** Duration=0 collapses Exit Time — the blend is immediate regardless of checkbox
- **Next action:** Set Duration > 0 on both variants; re-run to separate the Duration and Exit Time variables
- **Docs gap:** Docs state Duration defaults to 0 and Exit Time is unchecked by default; interaction is not stated

### ET-ENDOFANIM
- **Symptom:** Variant C fires at end of Idle animation; Variant D also fires at end
- **Interpretation:** Conditionless default is "wait for animation end" not "fire immediately"
- **Implication:** This contradicts a naive reading of "fire as soon as reached"
- **Next action:** File against Scout's Variant A result; if Scout's A also waited for end, the doc phrase "as soon as reached" means reached-at-animation-end, not reached-at-frame-0

### ET-SPLIT
- **Symptom:** Variant C fires early (or immediately), Variant D fires at animation end
- **Interpretation:** Exit Time checkbox works as advertised; this is the unambiguous expected result
- **Next action:** Confirm timing is exactly at animation end for D, then proceed to multi-condition tests

## Cross-reference

- Scout artifact: 47638cb0-cd2a-47ea-ba03-293069d1afa1 (conditionless baseline, not executed)
- This package should not be run before Scout's Variant A produces a verdict