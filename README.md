# Filler-cut logic fixture

Source: art_01M6SNVGQ86GDSESP316R61M6Q r1 (cuts.py constants and guards).

Run `python test_cuts_logic.py`. No WAV, no FFmpeg required.

Fixture: 44100 Hz, 10 s, words `So um we need uh to start`.
`um` and `uh` are fillers; gap between `need` and `to` is ~1.25 s (> MAXP=0.5).

## What it checks
- `gone()` filler rules match article spelling table
- Segments are non-empty and within file
- Long pause between kept words is shortened
- Hard-cut baseline vs crossfade-adjusted sample delta = joins × X/2
- Guards: >10 ms overlap, removed-overlaps-kept both raise ValueError