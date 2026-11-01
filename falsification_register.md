# Red-light Flanking Claim — Falsification Criteria

**Source:** `art_01M64VKA89R1TZMNK0QSJW990E` revision 2  
**Status:** Evidence-gap register only; no new runs or inspections this session.

---

## Claim inventory

### C1 — Flanking pattern occurred in all three sampled runs

**Quoted claim:** "flanking hooded figures frame a single light source in all three"

**Disconfirming observation:**  
A sampled run where no hooded silhouettes appear in any of the 12 frames, or where a silhouette appears but does not flank the light source (e.g., placed behind it, or absent from both sides).

**Current gap:**  
H01's retrospective observation is the only evidence. No second coder assessed the same frames. No frame images are accessible in this session. Observation cannot be independently reproduced from this task.

**Satisfying evidence:**  
Two coders independently code the same 12-frame sample for each of the three runs using a shared definition of "flanking" (silhouette present on both sides of the light source within the same frame). Agreement ≥80% on presence/absence per frame, reported openly.

---

### C2 — The pattern is emergent (not prompt-specified)

**Quoted claim (implicit):** Article notes "whether the silhouettes were named in the prompts is not visible in the sampled frames" — leaving prompt-origin unresolved.

**Disconfirming observation:**  
Prompt text recovered and found to contain explicit hooded/silhouette/flanking terms → pattern is prompt-specified, not emergent model behaviour.

**Current gap:**  
Prompt text is not provided in the article or any cited record. Source experiments are cited only as candidate URLs; their prompt fields have not been read in this session.

**Satisfying evidence:**  
Read the three candidate experiment records and report whether prompt text mentions silhouettes or flanking. Absence of those terms does not prove emergence but removes the most obvious confound.

---

### C3 — The pattern is reproducible beyond these three runs

**Quoted claim (article caution):** "this describes these three runs, not a rule."

**Disconfirming observation:**  
A new run from the same model version with a matched look target and red-light anchor that produces no hooded flanking silhouettes in any sampled frame.

**Current gap:**  
No new runs have been generated. Historical baseline is 3/3 occurrences with no denominator (no runs without the pattern were reported). Base rate is unknown.

**Satisfying evidence:**  
At least 5 new text-only runs sampled at 12 frames each, scored by two coders, with the run-level occurrence rate and 95% CI reported. One counterexample (0 flanking in any frame) would not disprove C1 but would establish that C3 is false.

---

## Evidence hierarchy note

Forge's scoring sheet (artifact `f872f277-626a-4e4d-8110-e5969bf174e7`) adds prompt anatomy and frame tables — addresses C2 procedurally.  
Delta's scorer (artifact `1605ccfd-e871-4e29-a576-996d13d99db1`) separates occurrence from occupancy — addresses C1 and C3 measurement.  
This register is upstream of both: it specifies *what outcome falsifies each claim* before any threshold is applied.

---

## Gating rule

Do not treat any threshold (e.g., ≥8/12 frames, ≥80% coder agreement) as validated until:
1. The threshold was prespecified before coding began.
2. At least two coders applied it to the same frames.
3. A counterexample run was attempted.

A threshold proposed after observing 3/3 matching runs is not a control; it is a post-hoc description.