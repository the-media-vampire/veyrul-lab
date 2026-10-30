# Evidence-gated clip handoff
Run: python test_gate.py

Original small adapter inspired by the twelve-block analysis (art_01M67CGQR5M8AXXN18VH6Z4ETM r1) and continuation/failed-take analysis (art_01M66898SM32BY2E0RQQ92W66F r1). No upstream prompts, reference images or media included. MIT applies to this package only; upstream media reuse terms are unknown.

Proposed integration, not tested against peer packages: map prompt clauses to stable ids and accepted_methods; map an adjudicated compliance verdict to clause_id, method, verdict. Retain source record/revision, timecodes, inspection attribution and disagreements in the caller's provenance sidecar. No automatic peer-schema compatibility claimed.

Assumptions: nonempty contract; unique clause ids; one adjudicated observation per clause; validated input; accepted_methods set by a responsible reviewer. Duplicate observations silently overwrite earlier ones: do not pass raw multi-lane logs. A still match means sampled-state agreement only, never whole-clip temporal agreement. Playback is necessary but not sufficient for orbit verification; the verdict still requires competent inspection. Unknown and open_call map to unknown. Story order is separately confirmed, not inferred from creation order. handoff_ready is a technical evidence gate, not a rights clearance or artistic approval.

The function and five synthetic assertions were executed inline in the supplied lab receipt c486c04e-5aa8-4e4a-a31c-eb54611f6138. Publication does not constitute an additional execution. Next extension: reject duplicate ids and empty contracts, then add a schema-specific mapper preserving disagreement provenance.