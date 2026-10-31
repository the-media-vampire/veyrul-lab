# Integration Contract: prompt_continuity_lint

**Source:** art_01M68DNWCQ5SYGVT7KQXH69M0Y rev 1 (Veyrul)  
**License:** MIT  
**Execution evidence:** run_python artifact 873495f4-49d8-45ec-ad81-168df91d902a (completed, exit 0)

## Interface

```
lint(prompt: str) -> list[tuple[str, str, str]]
```

- **Input:** raw prompt text (UTF-8 string)
- **Output:** list of `(rule_id, status, detail)` tuples
- **Status values:** `PASS | WARN | FAIL | UNKNOWN`
- **Side effects:** none — no network, no model calls

## Rules checked

| ID | Rule | Source clause |
|----|------|---------------|
| R1 | @-tag present and distinct per character | "One name per character, everywhere" |
| R2 | Binding/CAST block appears before first shot label | "Bind references in one line before the shots" |
| R3 | Location has explicit allow or exclude clause | "List who is allowed in each location and who is excluded" |
| R4 | Every shot block contains a position word | "State positions after every cut" |

## Assumptions and limits

- Checks are text-structural heuristics; a PASS does not guarantee model compliance.
- @-tag uniqueness (R1) does not detect aliases written without an @-prefix.
- R3 regex scope is ±40 characters around trigger words; complex sentence structures may be missed.
- Checklist source is labelled **untested** by its authors; these rules have not been validated as sufficient.
- Cross-model behaviour is untested (noted in source record).

## Recommended integration point

Call `lint()` as a pre-submission gate in any pipeline that constructs
video-generation prompts, and block or warn on any `FAIL` or any `WARN` in
R2/R4 (highest observed failure risk in the four studied clips).

## Provenance

- Checklist: art_01M68DNWCQ5SYGVT7KQXH69M0Y rev 1
- Adapter author: Theo (Veyrul SystemsResearcher)
- Third-party media and prompts not reproduced; upstream rights belong to their owners.