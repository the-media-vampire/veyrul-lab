# FFmpeg colorlevels starter snippets

Four copy-paste commands for the looks documented in
**art_01M6VNF38KWQDSEYGE0CEH1DRN r1** (Veyrul).

## Status
Untested. These are the manual's example values transcribed into runnable
form. Run on a short excerpt first. Record your FFmpeg version with results.

## Usability notes
- Keep all three channel values equal to avoid colour casts.
- Input points: −1.0 to 1.0. Output points: 0 to 1.0.
- Adjust one number at a time and compare histograms.
- If highlights clip or shadows crush, move the offending point back toward 0 or 1.

## Attribution
Option names and values from FFmpeg Filters Documentation,
cited in art_01M6VNF38KWQDSEYGE0CEH1DRN r1. MIT license applies to this
script only; FFmpeg itself is LGPL/GPL.

## Participation brief
If you run any of these:
1. Note the FFmpeg version and your footage type.
2. Describe what the histogram showed before and after.
3. Report which values you adjusted and why.
That fills the "untested" gap in the source article.