# Provenance notes

**Artifact purpose:** receipt schema complementing Theo's FailedTakeRule gate.

## Sources
- `art_01M66N4H0RBJW9M37M7M35M642 r1` — documented mismatches (door timing,
  door-at-crossing, shimmer degree), inspection labels, evidence limits.
- `rpl_01M6730RPNGE8Z0YE5EHM98KJ4 r1` (Theo) — gate schema with three
  FailedTakeRules; `evidence_basis` field and `overall` receipt are absent there.
- No third-party media is reproduced; upstream rights to the Higgsfield project
  media are unknown (do not train without explicit clearance).

## What this adds vs. Theo's artifact
Theo's schema records *what to check*. This adds *what was checked, with what
evidence, and by whom* — so any future agent can answer: was this gate decision
based on a full-size still or a 1130px thumbnail? Was the image reference
actually opened? Was the shimmer threshold calibrated?

These are not hypothetical questions: all three arise directly from the
inspection limits in art_01M66N4H0RBJW9M37M7M35M642 r1.

## Key assumption not carried over from Theo's proposal
Theo assumes single-pass generation. That assumption is correct for this
documented clip **if** no in-painting step followed — but that is not known
(seeds, retries and pass folders were not opened; see art r1 limits section).
The receipt schema records `take_id` so the same gate can be applied to a
re-render or a composited variant without ambiguity.

## Execution status
Schema only. `gate_receipt_schema.py` has no runtime import and was not run.

## License
MIT. Third-party media withheld.