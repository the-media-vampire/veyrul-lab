# Integration Contract: Agents' Room ↔ Re3/DOC

Documented proposal only. Not run. Source: art_01M6H154J7KBB907MQWZ73VV2F r2 (CC BY 4.0 paraphrase).

## 1. Interface comparison

### Agents' Room
| Point | Type | Notes |
|---|---|---|
| Planning agents input | `prompt: str` | Starts from writing prompt on scratchpad |
| Scratchpad | `dict[label, str]` | Mutable shared store; each agent appends under its label |
| Orchestrator | deterministic sequence | Fixed order in fiction variant; learned orchestrator is future work |
| Writing agents input | `scratchpad_snapshot` | Each agent reads the whole scratchpad at call time |
| HITL seam | between planning and writing phases | Paper explicitly names this |
| Final output | `story: str` | Concatenation of writing-agent sections |

### Re3/DOC (art_01M5NP2YWX6Y9VTZ9B8NQFAFJV, art_01M5MC0A5RK5E5HM7J9WA1A6TB)
| Point | Type | Notes |
|---|---|---|
| Premise | `str` | Single seed |
| Plan | `List[scene_summary]` | Hierarchical; DOC controller can rewrite |
| Draft loop | `(scene, context) → str` | Sequential; Re3 re-reads prior context |
| Rewrite pass | `(draft, plan) → revised` | Re3 rewrite; DOC controller substitutes |
| Final output | `story: str` | Concatenated scenes |

## 2. Structural difference

```
Agents' Room:  prompt → [specialist planners] → scratchpad → [specialist writers] → story
Re3/DOC:       premise → single planner → [scene-draft loop + rewrite] → story
```

The scratchpad is label-addressable (each planner writes under its own key); Re3's context is a growing text prefix. These are structurally equivalent but not format-compatible without an adapter.

## 3. Adapter assumptions

To feed an Agents' Room scratchpad into a Re3-style scene loop:
- The `plot` scratchpad entry must be line-separated scene summaries (UNTESTED; prompt templates in appendix not opened).
- Flattening: `"[LABEL]\n{text}"` concatenated for all entries gives Re3 a usable context prefix.
- Re3's drafter must accept a flat text prefix (assumed from art_01M5NP2YWX6Y9VTZ9B8NQFAFJV; not confirmed against a JSON-plan variant).

## 4. Failure modes

| Assumption | Failure if wrong |
|---|---|
| `plot` entry is line-separated scenes | Adapter raises or returns nonsense scene list |
| Concatenation produces coherent sections | Seam artifacts at chapter length (paper only tests 1-2k tokens) |
| Scratchpad complete before writing phase | If orchestrator is non-deterministic, ordering not guaranteed |
| `character` entry alone holds consistency | Character drift across chapters; no cross-section canon agent exists in paper |

## 5. Provenance and license

- Agents' Room summary: art_01M6H154J7KBB907MQWZ73VV2F r2, CC BY 4.0 paraphrase of arXiv 2410.02603 (Huot et al.)
- Re3/DOC: art_01M5NP2YWX6Y9VTZ9B8NQFAFJV, art_01M5MC0A5RK5E5HM7J9WA1A6TB
- This contract: MIT

## 6. Missing evidence

1. Actual prompt templates (appendices not opened)
2. Exact scratchpad label schema per agent
3. Re3/DOC plan input format
4. Evaluation of either system beyond ~2,000 tokens