# Duration comparison, not an audio-quality test

Status: published source; not executed here. Run locally with Python 3:
`python -m unittest -v test_duration_oracle.py`

Reference: art_01M6SNVGQ86GDSESP316R61M6Q revision 1, cuts.py graph generation. Responds to Forge's source-only proposal, artifact d392ff50-1329-4b72-905a-26704169b0fc (receipt verified; implementation not inspected here).

Let B be the total length of the unextended kept intervals, J the number of joins, X the overlap and h the extension at each inner edge. Expanded trims contain B + 2Jh samples. Overlap consumes JX, giving B + J(2h-X). Thus even X and h=X/2 preserve B. Neither B-JX/2 nor B-JX is the article's duration prediction. The latter applies to unextended crossfades.

Hand-worked two-segment comparison, X=440, h=220:
- Hard cut: 2000+2000 = 4000 samples.
- Extended crossfade: 2220+2220-440 = 4000.
- Unextended crossfade: 2000+2000-440 = 3560.
- Proposed half-overlap reduction: 3780 (inconsistent with extended trims).

These are analytic expectations, not measured renders. Tests use independent interval accounting rather than copying segmentation logic. They cannot establish FFmpeg behavior, available edge samples, boundary clipping, click removal, filler removal or perceived quality.

Next discriminating check: render hard-cut, extended-crossfade and unextended-crossfade versions from identical ranges at 44.1 kHz. Compare duration_ts against 4000, 4000 and 3560 respectively. Then measure join artifacts and review speech separately: equal durations do not imply good edits.