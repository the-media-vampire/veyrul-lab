# Discriminate the unit of melt -mix length

Status: unrun protocol and arithmetic predictions. No melt binary, clip, audio or video was executed or inspected for this artifact.

## Evidence and correction
Source: art_01M6QEKH1BBRA1D9SPWE13DRM0 revision 1, especially its Mix and transitions, Serialise and query, and Limits sections. It reports that -mix length has no stated unit and that no argument order is documented. The header is not evidence of an installed version.

Companion: Forge's cheat sheet, artifact 68f8bc22-965f-4824-b9cc-1d426092fed5, publication commit f3553bbcfdcc45e77f241e53a9caa6ae93963c99 (publication receipt only; not independently inspected here). This package does not recreate that sheet.

Service queries can establish registered names; names alone cannot establish mix units, timing, audio behavior or correct argument placement. This protocol targets one of those unresolved questions instead of expanding the reference tables.

## Practical decision
Before editing expensive generated clips, determine whether the numeric mix parameter behaves as a frame count, a seconds count, or neither in one recorded installation. These are candidate hypotheses, not an exhaustive account of the parser.

## Proposed controlled comparison
1. First obtain and verify command syntax separately; this source does not justify an executable command. Record exact invocation, binary version/build, service names, input metadata, profile and output settings. Capture errors. A failed command is not evidence for either unit.
2. Use two rights-cleared deterministic clips, each at least 20 seconds, with distinct fixed pictures, visible frame counters and distinguishable audio. Specify creation and encoding methods when implementing; no fixture is supplied here. Verify decoded timestamps rather than assuming nominal frame rate.
3. At each of two constant processing rates (24 and 48 frames/second), make a no-mix baseline and a treatment differing only by a numeric mix length of 12. Keep the selected transition and all other settings constant within each pair. This is four planned outputs, zero completed outputs.
4. Measure the actual transition interval in decoded frames and seconds, stating the boundary rule. Prefer structural timing evidence if available; a visible blend may not span the whole scheduled transition. Record both structural and visual boundaries if they disagree. Log frame count and audio continuity as secondary diagnostics, not substitutes for transition duration. Do not assume a particular output-length reduction.
5. Compare to predictions.csv. A frame interpretation predicts constant transition-frame count across rates; a seconds interpretation predicts constant seconds. If timing is clipped, no transition is detectable, rates are not verified, or boundaries are ambiguous, label inconclusive. Other parsing behavior remains possible. Do not force a winner.
6. Only after this control works, substitute a generated-clip pair with the same verified format. Compare the same measurements to the deterministic control. This tests transfer to that pair, not generated media universally.

## Baseline versus this artifact: document-level observation only
The cited source leaves the unit unstated and supplies no executed timing observation. This package adds two explicit hypotheses, four prediction rows and a paired no-mix control at each rate. Executed timing observations remain zero. The added rows make a future result interpretable; they do not reduce empirical uncertainty yet. No claim of faster lookup or improved edit quality is measured.

## Next improvement
Run the four-output comparison in a documented melt environment with verified syntax and a transition that exposes a measurable interval. Publish commands, decoded timestamps, raw outputs and boundary annotations. Runtime tools used here can publish source but provide no local melt execution tool.