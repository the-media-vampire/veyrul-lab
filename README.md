# music-model-ci-gate

Adapter contract between `check_decision_v5.py` (art_01M6SQH2ECQZH73P9EP9XHKB47 r1)
and a CI/pre-release pipeline.

## Mechanism

The checker is a pure function:
- Input: `record.json` (five parts: code, weights, training_data, output_terms, distributor)
- Output: JSON to stdout + exit code (0 = complete+go, non-zero = stop/hold/errors)
- It knows no model, has no clock, cannot verify quotes.

This adapter adds two things:
1. A **retrieval interface**: fetches or validates that the five source URLs are still
   reachable and that read_on dates are within 30 days of release_on.
2. A **pipeline boundary**: wraps the checker exit code in a gate step that CI systems
   (GitHub Actions, GitLab CI, etc.) can consume without understanding the licence logic.

## Interfaces exposed

| Interface         | Owner           | Changes when…                              |
|-------------------|-----------------|--------------------------------------------|
| record.json schema | check_decision  | Checker is updated; re-read article r1     |
| five part statuses | you (human)    | You read a new licence revision            |
| exit_code -> gate  | this adapter   | CI platform changes                        |
| source URL reachability | adapter   | Publisher moves a file                    |

## Assumptions to test

- The checker exit code is stable: a future check_decision version might renumber it.
- `read_on` within 30 days is enforced by the checker, not the CI: the adapter only
  surfaces the error, it does not re-read the licence.
- CD Baby refusal and CC-BY-NC stops are caught by the checker regex, not by the adapter.
- Qwen upstream and Stable Audio Open Community License gaps produce `unknown` → `hold`;
  the gate blocks release without manual escalation.

## Not covered

- Verifying that quotes are genuine (the checker says so explicitly).
- Reading or auditing training data.
- Legal advice of any kind.