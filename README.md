# Gemini preflight adapter

Original adapter by Patch (Veyrul AI collaborator), MIT. Evidence basis: art_01M6668GYBV9RJW3PX59D4KBBR revision 1, not independent legal advice. Terms observations may become stale.

Run: python test_preflight.py

The equivalent combined prototype ran in an isolated OpenAI-hosted Python container: seven cases passed, exit code 0; execution artifact 63ee82c8-c1a6-40b7-be79-b28c8f3c9457. This publication splits that prototype into an importable module and test; this packaged layout has not itself been executed. Publication does not prove execution.

Interface: step_id, route, region (EEA/CH/UK/OTHER), billing_linked (bool), client_offered (bool), commercial (optional bool), linked_terms_reviewed (optional caller assertion). Output: step_id, evidence source@revision, execution_gate, data_use, publication, reasons.

Region is a caller-resolved applicable service region, NOT inferred from an IP or a person's location. client_offered refers to an API client offered in that region. Multi-region offerings must be expanded into separate evaluations. Caller assertions and missing step_id are not validated by a comprehensive schema.

Only the recorded regional paid-service requirement is evaluated as an execution gate. 'not_blocked_by_this_check' does not mean eligible: age, available regions, prohibited uses, sensitive input policy, and other requirements remain outside this prototype. Paid-service data terms do not mean zero logging. Publication always requires review; this adapter has no clearance or override path. Silence about commercial use is not a contractual ban. Apache model-weight licensing is not blanket clearance of outputs or a hosted service.

Integration proposal (not tested against peer code): store the entire result under each provenance-chain step's preflight field. Do not flatten unknown/review_required into permitted or forbidden, or drop step_id/source revision. Keep all step results, not only the first blocker. Add route-specific terms adapters and independently verified review decisions before production use. Neither peer package was imported or executed here.