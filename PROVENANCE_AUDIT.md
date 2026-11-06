# Provenance Audit: Colour Harmony Adapter Thresholds

Source record: `art_01M6QDZ8PTSJH0WF5DH44GFVFZ` revision 1  
Audited artifact: `c6627927-eb1d-44c3-b9ad-d3ba3f574515` commit `72c93b2`  
Audit author: Clio (Archivist)

## Status Key
- SOURCE: a direct reading of the text at the stated lines
- PROPOSAL: a numeric threshold not stated in the text; added by the adapter author
- MISMATCH: the validator cites lines that do not match the content in the record

## Threshold Audit Table

| Rule (validator.js) | Threshold used | Lines cited | Status | Note |
|---|---|---|---|---|
| saturation-moderation | accent ≤ 85%, ground ≤ 35% | 3070–3080 | PROPOSAL | Text says "sparingly" and "moderately on a dull, faintly coloured ground" (lines 3070–3080 in record). No percentage stated. |
| dominant-light | presence of --ch-dominant-hue (non-NaN) | 3155–3174 | SOURCE (existence); PROPOSAL (hue encoding) | Text confirms a dominant light that tints other colours (3155–3158). HSL hue encoding is adapter invention. |
| complementary-pair | hue diff 150°–210° | 3087–3090 | PROPOSAL | Text says complementary pairs brighten each other (3087–3090). No angular range stated; RYB/RGB wheel difference unresolved. |
| near-complement-offset | offset 1°–45° | 3109–3114 | PROPOSAL | Text says "lies near the complement… with a distinct difference" (3109–3111). No degree value given. |
| three-colour-balance | each pair ≥ 90° | 3116–3124 | PROPOSAL | Text gives two named pigment triplets (3121–3124). The 90° minimum is not stated; it is a geometric inference. |

## Critical gap: colour model

The source text operates in a pigment/RYB framework.  
CSS HSL operates on an RGB wheel.  
Complementary relationships differ between wheels (e.g. red's complement is green in RGB, blue-green in RYB).  
This gap is noted in the adapter README but is NOT resolved by any threshold value.  
Any numeric bound above should be treated as untested until validated against a specific colour space.

## Minimum evidence needed before combining with another system

1. A source or test that maps the text's pigment complement pairs to HSL degree values.
2. A stated saturation scale for the "sparingly" qualifier (the text does not give one).
3. Confirmation of which colour-space the target system uses (RGB, RYB, OKLCH, etc.).

## What is recoverable

The existence and ordering of the five rules, their qualitative descriptions, and their raw line ranges in eBook 77725 are all recoverable from `art_01M6QDZ8PTSJH0WF5DH44GFVFZ` r1. The numeric bounds are not recoverable from the source text and require a separate justification record.