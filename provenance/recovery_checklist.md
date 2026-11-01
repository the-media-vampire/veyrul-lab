# Recovery Checklist — What the next agent needs to verify

This checklist is the minimum a future agent must complete before the Krita AI Diffusion × ComfyUI-3D combination can be described as integration-ready rather than merely described.

## Must resolve before recommending
- [ ] GAP-01: Read plugin LICENSE file; cite SPDX identifier
- [ ] GAP-04: Resolve rqr_01M6ABTSBNJPM69HGWVK1PVRJ5 (3D model weight licences)

## Must resolve before wiring outputs
- [ ] GAP-03: Confirm IMAGE tensor dtype/channel/range at ComfyUI boundary
- [ ] GAP-02: Confirm Nunchaku removal runtime error path

## Already resolved
- [x] Custom workflow parameter name check: heuristic scanner in bf77cb8f (not tested against live plugin)
- [x] Architecture/style binding drift: documented as fixed in v1.52.0
- [x] Krita version compatibility: v1.52–v1.53 require Krita 5.x; v1.54.0-pre requires Krita 6.x

## Source IDs to cite in any follow-on record
- art_01M6A17B8GRMEXFF8JFTSZTYGM r1 (primary changelog)
- bf77cb8f-b10b-41d4-8f3b-b44c87ae15f1 (Theo's contract, completed)
- rqr_01M6ABTSBNJPM69HGWVK1PVRJ5 (licence research, pending)