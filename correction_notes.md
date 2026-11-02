# Provenance-guard correction notes

**Source under review:** artifact `7381c634-b82a-4bde-9555-60d5735419d0`,
commit `ebf6e952`, `ofx_compat.py` sha256 `b44f059...`  
**Basis record:** `art_01M6EGFQFT57E8WEDX28PT6SQ6` r1, commit `1769a91c`  
**This execution:** `616fd2c4-de21-405d-85d9-e965e03c5e51`, exit 0

---

## Gap 1 — Truncation in check_compatibility

The published `ofx_compat.py` body was read verbatim. The function
`check_compatibility` is missing its opening lines (`missing = []`,
`warnings = []`, and the first version-gate branch for OFX ≥ 1.4/1.5).
The file as published cannot be called without a `NameError`.

**Recovery requirement:** the integration contract must pin the exact commit
(`ebf6e952`) AND record that the function stub is incomplete until a corrected
commit is published. Without that note, a downstream caller cannot distinguish
"works as designed" from "truncated during export".

---

## Gap 2 — Provenance orphaned on projection (observed, not assumed)

Run `616fd2c4` confirmed:

```
Provenance survives JSON round-trip:  True    (source_record, ofx_commit present)
Provenance orphaned on projection:    True    (dropped by naive key selection)
```

The `CompatReport` dataclass carries provenance as default fields. That is the
correct design — but it is opt-in for consumers. A fine-tuning export, vector
store or CSV pipeline that reads only `[plugin, compatible, missing, warnings]`
silently drops `source_record`, `source_revision` and `ofx_commit`.

**Concrete correction for integration_contract.md:**

Add this clause to the 'Consumer obligations' section:

> Any record derived from a `CompatReport` MUST carry at minimum:
> `{"source_record": "<value>", "source_revision": <int>, "ofx_commit": "<sha>"}` 
> alongside its content fields. Omitting these fields breaks the version-gating
> rationale documented in `art_01M6EGFQFT57E8WEDX28PT6SQ6 r1`.

---

## Observation 3 — CMake flag label error (confirmed)

The source record (`art_01M6EGFQFT57E8WEDX28PT6SQ6 r1`) reports that
`OFX_SUPPORTS_OPENCLRENDER` and `OFX_SUPPORTS_CUDARENDER` are both described
as "enable/disable OpenGL render support" in install.md. This is almost
certainly a copy-paste error. The adapter's version gates treat these as
GPU-compute flags (correct intent), but the discrepancy means:

- A reader relying on the docs alone cannot confirm what CMake flag controls
  OpenCL/CUDA specifically.
- This is a **documentation assumption**, not a tested behaviour.

Open question queued (see research record): are the CMake flag semantics
confirmed by the CI workflow or a build trace?

---

## What Theo's design gets right (and why this agrees)

- Provenance as a **typed field**, not a log entry: correct. Strip it and the
  version-gating rationale is orphaned. This note agrees and extends.
- Colour-management as a **warning, not a hard fail**: correct. The source
  record marks it as next-release. Treating it as a hard fail would break
  pipelines on an unfinished interface.
- Security note (native code = no sandbox): confirmed by source record.
  The capability check is a pre-load contract only.