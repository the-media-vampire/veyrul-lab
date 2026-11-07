# colorchannelmixer ↔ curves adapter

Sources: art_01M6VJS0YQE8PBGBG1H50KN8MF r1 (colorchannelmixer),
FFmpeg filters documentation (curves filter).

## Interface contract

| Property | colorchannelmixer | curves |
|---|---|---|  
| Input | any RGB/RGBA pixel stream | any RGB/RGBA pixel stream |
| Output | same pixel dimensions, same colorspace | same pixel dimensions, same colorspace |
| Operation | linear cross-channel weighted sum per pixel | per-channel tone curve (nonlinear) |
| Coefficient range | -2.0 to 2.0 per term | 0.0–1.0 input/output control points |
| Alpha handling | explicit ra/ga/ba/aa terms; defaults leave alpha unchanged | not mixed across channels |
| Luminance preservation | pc=lum option, pa 0.0–1.0 | none built-in; needs lut3d or separate filter |
| Grayscale | documented preset (.3/.4/.3) | achievable via equal R=G=B curves |
| Sepia | documented preset (.393/.769/.189 …) | requires 3 separate asymmetric curves |

## Assumption list

1. Both filters act on decoded pixel data; colorspace and bit depth must match.
2. colorchannelmixer coefficients are linear; curves can encode gamma-aware adjustments.
3. Luminance preservation (pc=lum) in colorchannelmixer is applied after the mix.
4. Neither filter changes frame rate, resolution or container.
5. Chaining is valid: colorchannelmixer before curves for mix-then-tone workflows.

## Provenance and license

- colorchannelmixer: FFmpeg project, LGPL 2.1+. Option names and coefficient sets
  are factual interface descriptions, not copyrightable.
- curves: same project, same license.
- This adapter script: MIT (see LICENSE).