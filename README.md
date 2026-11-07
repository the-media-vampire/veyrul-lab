# 1894 pen-drawing rules → SVG preflight contract

Source: art_01M6Q6XXX3DEFQ6QST964PTW6M r1 (Harper 1894, eBook 60972, lines 1757–1812).
All SVG mappings are curator inference; the handbook covers no digital practice.
No copyright or public-domain determination is made for the source text.

## Four mechanisms → four SVG interfaces

| ID | 1894 rule (source lines) | SVG interface | Failure mode |
|----|--------------------------|---------------|--------------|
| R1 | Draw larger than the block; reduction ~4× US, two-thirds to one-half larger England (1773–1780) | viewBox vs target size ratio `--draw-scale` | Strokes set at final size fill in on reduction |
| R2 | Blue transfer paper used "since blue will not photograph" (1795–1796) | Guide layer: hue 210–260 only, `data-layer=guide` | Guide marks survive into output raster |
| R3 | Lines must stay "open" after reduction (1808, 1812) | Minimum gap between strokes ≥ `--min-gap-px` at target res | Merged strokes → dirty patches |
| R4 | Do not leave pencil marks; deep marks damage surface (1757–1767) | `data-layer=sketch` absent from export | Under-drawing artefacts in output |

## Assumptions (A1–A4)
- A1: `--draw-scale` defaults to 1.5 (midpoint of English range) — not a source figure.
- A2: "Blue will not photograph" is specific to 1894 orthochromatic process; RGB/laser equivalence is untested.
- A3: "Open" has no source number; `--min-gap-px` is a proposed slot, threshold left to user.
- A4: Sketch-layer rule is inference from the pencil-marks warning; SVG layers are not in the source.

## Key dependency boundary
Variable-stroke-width pipelines (pressure-sensitive tools) make R3 non-computable at SVG-DOM level. Flatten strokes before preflight, or downgrade R3 to advisory. That is the first interface to resolve before combining with such a pipeline.