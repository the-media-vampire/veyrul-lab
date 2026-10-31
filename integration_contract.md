# Integration contract: linter + frame_audit/v1

## Workflow position

```
Prompt text
    │
    ▼
[prompt_continuity_lint]   ← artifact 485ad4fc (pre-submission)
    │ FAIL → block
    │ WARN → confirm
    │ PASS ↓
    ▼
Model submission
    │
    ▼
Sampled stills
    │
    ▼
[frame_audit_record()]     ← this artifact (post-generation)
    │
    ▼
log: list[frame_audit/v1]
```

## Shared vocabulary

| Rule | Linter (pre) | Frame audit (post) |
|------|-------------|--------------------|
| R1   | @-tags present & distinct | Tags identifiable in stills |
| R2   | Binding block before shots | N/A (structural only) |
| R3   | Allow/exclude clause present | Excluded looks absent from location |
| R4   | Position word per shot | Position matches prompt in stills |
| R-timing | Not covered | Beat position vs. still timestamp |
| R-orientation | Not covered | Object face direction in stills |

## Interface contract

- **Input to linter:** `str` (plain prompt text)
- **Output of linter:** `list[tuple[rule_id, status, detail]]`
- **Input to frame_audit:** sampled still frame + prompt_source_id + clip_ref
- **Output of frame_audit:** `dict` (frame_audit/v1 JSON)
- **Joining key:** `rule_id` is shared; allows direct comparison of pre vs. post status.

## Failure-mode separation (provenance rationale)

| Failure type | Detected by |
|---|---|
| Rule structurally absent from prompt | Linter FAIL/WARN |
| Rule present but model ignored it | Frame audit MISMATCH |
| Ambiguous or unverifiable in stills | Frame audit AMBIGUOUS / NOT_VERIFIED |

This separation was not instrumented in art_01M68DNWCQ5SYGVT7KQXH69M0Y rev 1.

## Assumptions

1. Stills only; audio, motion and cuts are not captured.
2. Frame IDs are stable references; auditor responsibility to assign them.
3. The source checklist (art_01M68DNWCQ5SYGVT7KQXH69M0Y) is labelled **untested**;
   MATCH here is an observation, not proof of general model compliance.