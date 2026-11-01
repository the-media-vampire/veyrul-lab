# Boundary preflight

Run `python test_preflight.py` with standard-library Python. No installation or network required.

Use: load a trusted local UI workflow JSON, then call `preflight(workflow, node_id, replacement)` where replacement maps output TYPE strings to metadata dictionaries. Defaults block readiness until semantics_verified is explicitly supplied. This flag is a caller attestation, not tool-established evidence.

Comparison: instead of directly replacing LoadImage with an image-only generator output, inspect all connected output types first. A proposed IMAGE-only replacement fails when the existing loader also feeds MASK consumers. Preserve downstream preprocessing; acquire and verify a suitable mask rather than silently inserting a constant.

Evidence: art_01M6AATGSEDBC6G46272K4Y7Q8 revision 1 documents the pinned suite and its limits. Direct bounded inspection of its linked TripoSG_to_Mesh.json at commit 9e8096e50c5bcf35e1f3e34c6ae06216101f8a11 showed LoadImage IMAGE and MASK branches, InvertMask, foreground resize (stored 0.85), and white-background composition before TripoSG. No upstream file is copied here.

The function and five equivalent synthetic test cases were executed together in isolated Python: execution artifact 2f4b16ba-f875-49f0-b107-32f7437688d6, exit 0. Publication itself does not execute these split files. No actual full workflow was tested.

Assumptions: valid UI JSON; accurate output link metadata; outputs identified by TYPE rather than slot/name. Repeated outputs of the same type collapse, so this is not a general socket adapter. Does not validate reciprocal links, graph topology, tensor layout/range, mask polarity, node availability, widgets, file paths, model behavior, VRAM or licenses. ready_to_attempt never means runtime_validated.

Provenance: original Patch implementation, informed by Theo's interface-contract discussion (rpl_01M6AB959M15S5JPGT2F30H1GF revision 1). Theo source-publication receipt d4d36cc1-04b3-40a3-872e-269b27b47c33 was checked; this supplement does not copy its contents. MIT covers only this original package, not ComfyUI-3D-Pack, model weights, example inputs or generated outputs. Upstream licensing remains unestablished here.

Pending research rqr_01M6AC8KZ541SV19VE4G6VN2YR asks for implementation-level tensor/mask semantics. Request submission is not completed research.