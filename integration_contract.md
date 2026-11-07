# Integration contract: negate + colorchannelmixer

Sources: art_01M6VRHPQXCYKH293R9K1F7KF2 r1 (negate), art_01M6VJS0YQE8PBGBG1H50KN8MF r1 (colorchannelmixer)

## Shared interface

Both filters consume and emit a decoded pixel frame. No metadata handshake.
The connecting medium is the libavfilter graph — a stream of AVFrame structs.

## Format-boundary assumption (load-bearing)

- `colorchannelmixer` operates on RGB pixel formats.
- `negate` component names depend on pixel format:
  - `y, u, v` are valid only in YUV formats.
  - `r, g, b` are valid only in RGB formats.
- **Consequence:** chaining colorchannelmixer into negate=components=y will produce
  an option error or silent no-op because `y` does not exist in the RGB output
  of colorchannelmixer. The source manual does not state what happens; the safest
  fix is an explicit format conversion node between them.
- If you use negate=components=r,g,b (or no component list) after colorchannelmixer,
  no format conversion is needed — both are RGB-compatible.

## Arithmetic consequences of order

- **negate → colorchannelmixer:** The mix matrix operates on already-inverted values.
  Sepia applied after negate will produce a warm inverted image, not a sepia of the original.
- **colorchannelmixer → negate:** The mix transforms colours first, then negate inverts.
  This is the more predictable composition for grading-then-invert workflows.
- Neither order is universally correct; the choice is a declared design decision.

## Evidence status

| Claim | Status |
|-------|--------|
| Component names (y,u,v,r,g,b,a) | Source-documented (negate article) |
| colorchannelmixer is RGB-domain | Source-documented (mixer article) |
| Format-boundary error behaviour | Mechanism-derived; untested |
| Arithmetic order-dependence | Mechanism-derived; untested |
| Any real run result | Not run |

## Provenance and license

- FFmpeg filters documentation: FFmpeg project, public documentation.
  No passages copied; synthesis only.
- Both source articles: original synthesis, modification and redistribution
  permitted per their rights fields.
- This contract: MIT (see LICENSE).