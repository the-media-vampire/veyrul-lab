# CrowdLocationContract

Validates the location-tagging and crowd-exclusivity mechanism documented in
`art_01M687Y92Z73146YZ2W3CYZKBW` r1 (Seedance 2.5, three-shot comic edit).

## What it checks
1. Every entity has an `@`-prefixed tag and a non-empty look line.
2. Every crowd has an `allow_in` location and ≥1 `deny_in` locations.
3. `LightState.allowed_sources` is non-empty (prohibition alone correlates with mismatch-1).
4. Each shot has a `blocking_prop` and warns when `framing_measurable=False`.
5. Reference-image entities flag `look_only=True` to avoid frame-copy risk.

## Difference from CutMapContract (artifact 03b599f1)
`CutMapContract` validates audio-led, timecoded beat structure.
`CrowdLocationContract` validates spatial/crowd/light structure.
They cover orthogonal interface dimensions and can be combined.

## License
MIT. Analysis cites `art_01M687Y92Z73146YZ2W3CYZKBW` r1; upstream media rights belong to their owners.

## Execution evidence
Sandbox run: `resp_0b71d69f1c4daee0006ae58383ba3087d2a26b7a0bf64dd54d`
- CONFORMING → valid=True, errors=[], warnings=[]
- STUDIED PROMPT APPROX → valid=False, 1 error (allowed_sources empty), 4 warnings (word-only framing x3, look_only=False)
- MISSING DENY → valid=False, 1 error (no deny_in)