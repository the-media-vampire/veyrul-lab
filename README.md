# Colour Harmony → CSS Adapter

Source: art_01M6QDZ8PTSJH0WF5DH44GFVFZ r1 (Veyrul)  
Underlying text: Helmholtz, *Popular Lectures on Scientific Subjects*,  
Gutenberg eBook 77725 (released 2026-01-17; original publication 1908)

## Interface table

| Variable(s) | Rule | Source lines |
|---|---|---|
| `--ch-accent-sat-max`, `--ch-ground-sat-max` | Saturation moderation | 3070–3080 |
| `--ch-dominant-hue`, `--ch-shadow-tint-strength` | Dominant light tints shadow | 3155–3174 |
| `--ch-pair-a-hue`, `--ch-pair-b-hue` | Complementary pair (brightening) | 3087–3090 |
| `--ch-near-complement-offset` | Shifted complement (more pleasing) | 3109–3114 |
| `--ch-triad-{a,b,c}-hue` | Three-colour balance | 3116–3124 |

## Explicit assumptions

1. Source rules describe **pigment behaviour** (painter's RYB wheel). These variables use HSL degrees (RGB wheel). Mapping is approximate.
2. The 90° minimum triad spacing is a **proposal**, not a source claim.
3. Near-complement offset range (1–45°) is a **proposal** from the phrase "near the complement with a distinct difference".
4. The source states rules are **not yet firm**; treat every threshold as a starting point.

## Known gap

Lecture closing summary (after line 3188) is noted as a gap in the source record.