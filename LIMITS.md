# Limits of this spec

- `plot.scale()` is a public Plot API (documented); its availability in a
  notebook cell is assumed but not verified here.
- Criterion 2 (fx facet) depends on how Plot resolves implicit stacking
  when fx is absent; the interaction between barY implicit stack and fx
  channels is documented in the Stack transform page but not tested here.
- Criterion 4 distinguishes value labels from axis labels by content;
  if the axis tick labels happen to equal bar values, manual inspection
  is required to disambiguate.
- These criteria do not cover pixel-level layout (label overlap,
  margin clipping) because the docs state Plot does not measure text
  exactly (art_01M6MH8DFE1KD1GQA0A0VTGENT rev 2).

## Next improvement

After a first run is reported, compare actual vs. proposed failures.
Any row where the proposed failure does not appear is evidence of
a documentation gap or an incorrect inference in the checklist.