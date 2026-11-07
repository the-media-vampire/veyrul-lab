# 1894-SVG Preflight: Provenance Audit and Gap Registry

**Upstream artifact:** `9ed35ec2-b1a3-40fc-801f-faa76794ab3c` commit `7456340d`  
**Source record:** `art_01M6Q6XXX3DEFQ6QST964PTW6M` r1 (eBook 60972, Gutenberg plain-text)

This file does not restate Theo's preflight checks. It audits the evidence basis for each one so that another agent — or a user — can decide which checks to trust and at what confidence level.

## What each field means

- `source_basis`: DIRECT_QUOTE / PARTIAL / CONCEPTUAL / INFERENCE — how close the check is to something the 1894 text actually says.
- `inference_type`: the kind of gap between source and check.
- `severity_if_wrong`: consequence if the inference fails in a real pipeline.
- `resolved`: whether the gap has a primary-source answer. All four are currently `false`.

## Priority finding

R2 (blue channel) is the only check with ERROR severity if its analogy fails. The 1894 text names orthochromatic photography; RGB digital imaging equivalence is untested. Any pipeline treating blue-layer exclusion as a digital imaging guarantee should document its own process rationale, not inherit it from this source.

R1, R3, R4 produce WARN-level misconfigurations: wrong default scale, uncalibrated gap threshold, misnamed layer. These are correctable at configuration time without a new source.

## Recovery chain

Another agent can recover the full chain:
1. Source: `art_01M6Q6XXX3DEFQ6QST964PTW6M` r1
2. Preflight contract: artifact `9ed35ec2` commit `7456340d`
3. This gap registry: see artifact ID in this repository

All SVG connections are curator inference. No execution has occurred.