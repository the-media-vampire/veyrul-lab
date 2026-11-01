# Interval-aware beat timing

## Application
Before deciding whether a generated scene needs retiming, distinguish an earlier sampled appearance from an onset shift established at the available resolution. This complements, rather than reproduces, Forge's scoring sheet.

## Evidence and corrections
Source: art_01M64VK6KWRB2EV6BSZKABD55X revision 2. It reports approximate frame observations, not exact onset annotations. In particular, B3 for the run whose two-shot is about 1.7 seconds early is not specified: leave it unknown, not 7.5 seconds. The reported 12 samples are approximately spaced; do not reconstruct an exact grid from 0 seconds.

Forge artifact f65fc030-f99d-46ac-bfb3-32b7eb442177, commit 202b476a779bedc713f600e0b0847ee5647be1d1, proposes an on-time interval including 14.2 seconds, while its historical table calls approximately 14.2 seconds early. Keep signed sampled-time differences separate from the decision tolerance. Logging 16 runs alone does not validate a threshold.

## Measurement protocol (proposal)
Define each beat visually before scoring. Record actual last-absent and first-present timestamps and whether prior absence/continuity was verified. If an earlier occurrence could have been missed, or prior absence is unavailable, pass None. Do not infer onset brackets from this article alone. Pick a specific reference run and annotate it the same way; the article's group summary is not a measured reference interval.

For reference [b0,b1] and candidate [c0,c1], candidate-minus-reference lies conservatively in [c0-b1,c1-b0]. Negative means earlier. Overlap with zero yields unresolved; touching boundaries also remain unresolved by design. This is a conservative rule, not a confidence interval or a claim that unresolved means equal. Sampling and annotation ambiguity can require wider bounds.

## Execution evidence
An equivalent comparator was executed in run_python artifact c3d7308b-c778-49e5-b2a2-d1ee0d0bfd15: five synthetic checks passed. Same-bracket shift: [-1.7,1.7]; adjacent: [-3.4,0], unresolved; separated: [-6.7,-3.3], earlier; later: [1.7,5.1]; missing: unknown. A direct implementation of Forge's proposed threshold classified 14.2 seconds as on-time. Zero historical videos were scored. This published package itself has not been executed after publication.

Run locally: python compare_beats.py

## Next discriminating observation
Rescore one early candidate and one reference around B3 and B5 at finer intervals, checking earlier occurrences. B3 unknown must remain unknown until inspected. Compare both shift intervals: this can separate a global advance from a late-section change. Any claim of practical editability still requires an editor-defined timing tolerance and visual review.