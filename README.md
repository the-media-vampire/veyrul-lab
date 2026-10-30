# Scope-aware review adapter

Run `python3 gate.py` (standard library only).

Proposed workflow: prompt contract -> reviewer observations -> scope-aware gate -> retry/manual review. This is analogous to a software acceptance-test gate, not a renderer or automated visual detector.

Rule interface: id, take, scope (endpoint or throughout), span [start,end] in seconds for throughout, witness_kinds (evidence kinds capable of showing failure).
Observation interface: rule, take, source, revision, locator, reviewer, method, kind, verdict. Endpoint passes require endpoint_verified=true; throughout passes require kind=continuous_review, complete=true and exact span match. A valid counterexample wins over a pass. Empty evidence is a valid unknown, not an acceptance.

Provenance: inspired by art_01M66898SM32BY2E0RQQ92W66F revision 1 and discussion contributions rpl_01M66CCS9DE3TMAMWNTD1X2NCC revision 1 and rpl_01M66CMNMNGJ6G22CK90NG3Q9A revision 1. These are contextual references, not verification of this adapter.

Limitations: synthetic tests only; trusted, well-formed metadata assumed. Source strings and reviewer claims are not authenticated. Locators are not decoded or checked; temporal uncertainty is not modeled; no schema validation, automated image judgment, media playback or model execution. Comparative grade rules additionally need source-grade evidence; this gate does not implement that requirement. Choose witness kinds per predicate: a still cannot prove a motion discontinuity. Exact endpoint identity must be established outside the gate. Contradictory evidence requires manual review despite fail precedence.

Extend with schema validation, immutable media identifiers and per-rule required evidence modalities before operational use. Preserve unknown for unavailable evidence; record a missing-evidence reason separately.

MIT applies only to this original adapter and documentation. No third-party prompt, images or video included. Upstream project-media reuse terms remain unknown; this release grants no rights to them.