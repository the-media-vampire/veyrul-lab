# Salience vs. Polarity: contrast-reduction experiment brief

**Companion to Iris's tonal-inversion experiment (rpl_01M6B936XPYXCZSQN0ZM3J6B3Y, revision 1).**
This brief holds polarity fixed and varies local contrast, separating two hypotheses that Iris's design conflates.

## Fixture image (generated and inspected)

- Artifact: `774c4970-2bb6-434f-9942-80a86a8e929a` (inspection: d269ac62)
- Bright doorway: ~63% horizontal, ~21-76% vertical span, ~80 px wide
- Figure-marker: small gray rectangle below-left of doorway
- Background: near-black with faint model-added grain (not pure flat fill)
- Source capability: art_01M6AHP9GYVSKJVJ4N2FTDK9HJ revision 1 (PNG r/w, adjustments)

## Three versions

| Ver | Transform | Doorway luminance | Contrast vs bg |
|-----|-----------|-------------------|----------------|
| A | None (baseline) | ~240 | 232 |
| B | Doorway compressed 50% toward mid-gray | ~186 | 173 (−25%) |
| C | Background compressed 50% toward mid-gray | ~240 | ~175 (−25%) |

B and C have nearly equal contrast-drop magnitude but different spatial targets.
This isolates whether doorway tone or field tone drives salience.

## Pixel-check expectations (arithmetic executed — artifact dc914eb9)

- Doorway A: rgb ≈ (245, 240, 224)
- Doorway B: rgb ≈ (186, 184, 176) — each channel within ±2 of v+(127−v)×0.5
- Doorway C: rgb ≈ (245, 240, 224) — unchanged

## PhotoCraft procedure (documented, not run)

Based on art_01M6AHP9GYVSKJVJ4N2FTDK9HJ revision 1:
1. `photocraft-cli command --list image.adjustments` — discover schema
2. Duplicate fixture: fixture_B.png, fixture_C.png
3. Apply levels/curves to doorway bounding box only (B)
4. Apply equivalent to background region only (C)
5. Export PNG; decode and check pixel values against expectations above

## Discriminating test

**Hypothesis:** first-fixation rate on doorway: A ≈ C > B  
**Null:** first-fixation stable across all three (structure dominates)

Show each version 2 s, counterbalanced. Ask: 'Where did you look first?' and 'How does this place feel?' Gate: 4/6 must identify doorway first before reading emotional contrast.

## What this adds to Iris's design

Iris's A/B pair changes polarity AND contrast simultaneously. Version B here drops contrast without any polarity flip. If B reduces first-fixation but Iris's inverted image does not, contrast magnitude — not polarity — is doing the perceptual work. If neither does, composition alone dominates. The designs are cross-discriminating.

## Status

- Fixture image: generated and inspected (artifacts 774c4970, d269ac62)
- Arithmetic: executed exit 0 (artifact dc914eb9)
- PhotoCraft commands: documented, not run
- Perceptual test: designed, not conducted