# MismatchAudit — provenance-gap classifier

Source: `art_01M681XTD8NSXT3N2KQF8NQFZB` r1 (Veyrul, 2026-10-31).  
Companion to `CutMapContract` at artifact `03b599f1-e922-423d-a852-4a5588c0a0f2` (Theo, Veyrul lab).

## What this does

For each of the six documented mismatches between the cut-map prompt and the 26 stills,
this module assigns:

- `contract_catchable`: whether `CutMapContract.validate()` would flag it **before** generation
- `root_cause`: `authoring_gap`, `inference_noncompliance`, or `ambiguous`
- `still_verifiable`: whether stills alone are sufficient to detect the mismatch
- `requires_audio`: whether playback is needed to classify the mismatch
- `open_question`: what preserved evidence is needed to resolve ambiguous cases

## Key finding (execution: artifact 74d65193)

| Category | Count of 6 |
|---|---|
| CutMapContract would catch | 3 |
| Inference noncompliance only | 3 |
| Ambiguous (prompt text needed) | 2 |
| Require audio to classify | 0 |

**Minimum evidence gap:** The original prompt text must be preserved to resolve
mismatch-3 and mismatch-6 as authoring gaps or inference failures.
Without it, the correct remediation cannot be identified.

## What this does not do

- Does not validate prompt authoring (use `CutMapContract` for that)
- Does not verify audio alignment (playback not done; sound claims not verified)
- Does not predict future generation compliance

## Licence

MIT. See LICENSE.