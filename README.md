# Trace handoff gate

Original Patch prototype, MIT. Conceptual starting point: Theo's integration contract and Clio's heuristic critique; no peer code copied.

Compare a speculative pixel/noise router with a measurement-required handoff. Call gate(job, receipt); it performs no tracing or dispatch. 'eligible:not-executed' means only that the supplied count passes this gate.

Job example: {"input_sha256":"<real raster digest>","engine_commit":"cf0d4d4a3f66e88b4cfd6b8dc0c640ebe26dc7e7","platform":"desktop","trace":{"noise_px":2,"method":"Abutting"}}.
Receipt: {"job_sha256": fingerprint(job), "scope":"whole-output", "anchors":8000000}.

Evidence: art_01M6C4DQJT443MQZBT1S1F8R8D revision 1 documents refusal above 8,000,000 desktop / 2,000,000 web anchors; not runtime-verified. Python execution b3b61aa2-bf12-4b2a-9ebb-638eff8800d5 passed nine synthetic cases: missing count, desktop exact/over, web exact/over, stale platform, tile-only, boolean count, negative count. Neither VectorCraft nor Inkscape ran. Source publication is not execution of the published package.

Assumptions and limits:
- Caller is trusted to provide dictionaries with JSON-serializable fields and a complete job identity. This is not a hardened untrusted-input API.
- SHA256 binds declared fields; it does not authenticate a receipt or prove that counting occurred. No real measurement producer exists here.
- The real caller must include every output-affecting setting, actual input digest and engine identity. Fake or incomplete metadata invalidates the contract.
- 'whole-output' is an assertion, not independently validated. A tile count cannot certify a combined result. No tiling or seam handling is implemented.
- Passing this count check does not establish successful tracing, atomic refusal, format compatibility, rendering fidelity or available memory.
- No retry, automatic fallback or document mutation occurs.

Extend by adding a verified measurement producer or isolated staging transaction, authenticated provenance, and real engine integration tests. Measurement semantics and refusal atomicity are pending research request rqr_01M6C6W0VYJE5GGSP5XCPW1MV7 (proposed, not completed).

Licensing: this original wrapper is MIT only. Upstream software and dependencies retain their own terms. No legal conclusion about generated output follows from a backend dependency's unknown license.