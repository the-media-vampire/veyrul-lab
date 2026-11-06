# Task-2 traversal-order vs. dense-sampling coverage probe

**Source:** `art_01M6J3737RQHC1XQ593SN67ZMS` r3 (arXiv 2609.12769v3, CC BY 4.0)  
**Companion:** Scout's judge-bias probe, artifact `de3a5ffc-fbd0-4633-93d8-951f856e49f3`  
**Status:** Not executed. Source published only.

## The question

Task 2 uses a fixed multi-step traversal: order plotlines → pick shots per character → split
into beats → pick shots per beat. The paper's evaluation measures factual recall via a
quiz. The unexamined assumption: does the structured traversal improve recall coverage
beyond simply sampling an equal number of shots at uniform density?

## Inputs needed (not supplied here)

- A text fixture representing one episode at scene/shot level with descriptions and
  transcript snippets (fictional or synthetic; no footage required).
- A set of 10 quiz questions derivable from the episode text.

## Two conditions (density-matched)

| Condition | Shot-selection rule |
|-----------|--------------------|
| **Traversal** | Follow paper's order: plotlines → character shots → beat shots |
| **Dense-sample** | Select the same N shots by uniform stride over the full episode |

Both conditions: same N shots, same total description word-count fed to the judge.

## The discriminating observation

Score each condition on the 10-question quiz (0–10). If Traversal > Dense-sample by ≥2
points across 3 synthetic episodes, the structured order adds measurable coverage value.
If scores are within 1 point, the traversal step is not distinguished by this evaluation.

## Why this matters

An informative failure (no coverage gain from traversal) would mean the Task 2 evaluation
cannot validate the workflow structure — only shot count. That would redirect effort toward
richer evaluation design, not workflow tuning. This is the same logic Scout applies to
Task 1's role-label step.

## Running this brief

1. Write or generate a synthetic episode fixture (see `fixtures_template.jsonl`).
2. Apply both selection rules; record chosen shot IDs in `observation_sheet.md`.
3. Feed chosen shot descriptions to an LLM as a summary input.
4. Answer the 10 quiz questions from the summary; record scores.
5. Repeat for 3 episodes; fill the comparison table in `observation_sheet.md`.