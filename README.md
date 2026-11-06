# Cross-Shot Continuity Checker

Extends Minimal Continuity-Ledger Schema (artifact acda5f8b) with semantic
cross-shot validation.

## What it checks
`cross_shot_check(shots)` flags `costume_note` or `location` changes between
consecutive shots of the same character when `scene_break=False`.

## Expected test results
| Scenario | Mismatches |
|---|---|
| Consistent sequence (baseline) | 0 |
| Costume note changed | 1 |
| Location changed | 1 |
| scene_break=True | 0 |
| Different characters | 0 |

## Limits
- Exact-string comparison on `costume_note`; paraphrases false-positive.
- Props inside free text not parsed.
- `scene_break` must be set by author; not inferred.
- No engine queried; ledger data only.

## Next improvement
Fuzzy token-overlap on `costume_note` to reduce paraphrase false-positives.