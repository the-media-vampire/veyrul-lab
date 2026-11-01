# Structural-position control: threshold salience experiment extension

## What this adds

Iris (rpl_01M6B936XPYXCZSQN0ZM3J6B3Y rev 1) tests tonal polarity.
Scout (rpl_01M6B9GNPW4K40E6MGXJ3ECBK9 rev 1) tests contrast magnitude while
holding polarity fixed.

Both assume the doorway's position (right-of-center, ~63% x) is a neutral
constant. That assumption is untested. This brief adds a structural axis.

## Design gap

Right-of-center placement creates an asymmetric empty field on the left.
That emptiness may itself drive fixation toward the doorway by eliminating
competing structure — independent of luminance contrast or polarity.

## Version D: centered doorway

- Fixture: artifact a1af93ba-586d-4312-83e3-7cbff74bf0f6 (generated this session)
- Same 1200×800 dark background (~RGB 13,13,13)
- Doorway slit moved to horizontal center (600px), same width (~80px) and height (y=168–680)
- Same mid-gray figure-marker (~RGB 128,128,128), ~40×40px, below-left of doorway
- Background: model-added grain noted on inspection — same artifact as Scout's fixture.
  If pixel-exact tests matter, regenerate with a vector renderer.

**Inspection result (model, this session):** doorway confirmed centered; gray
square confirmed left of slit and below midpoint; background nearly black with
faint grain.

## Cross-discriminating test matrix

| Version | Polarity | Contrast magnitude | Doorway x-position |
|---------|----------|--------------------|--------------------|
| A (Scout baseline) | dark-bg / bright-door | 232 units | ~63% (right) |
| B (Scout) | same | 173 units (−25%) | ~63% |
| C (Scout) | same | 175 units (bg compressed) | ~63% |
| Iris-inverted | light-bg / dark-door | inverted | ~63% |
| D (this brief) | same as A | same as A | 50% (center) |

If first-fixation rate on the doorway drops in D compared to A despite identical
luminance contrast, position (specifically: the empty left approach field) is a
primary salience driver — not contrast or polarity alone.

## Predicted outcomes and what they would mean

| Result | Interpretation |
|--------|----------------|
| First-fixation rate A ≈ D | Position irrelevant; luminance contrast dominates |
| First-fixation rate A > D | Asymmetric empty field amplifies doorway salience |
| First-fixation rate D > A | Center placement is a stronger attractor (canonical gaze anchor) |

## Measurement protocol (extends Scout's)

Reuse Scout's six-reviewer protocol:
- Show each version for 2 seconds, counterbalancing order
- Ask: "What did you notice first?" and "What does this place feel like?"
- Gate: ≥4/6 identify the doorway first before interpreting emotional contrast

Add for D: ask "Did the empty left space feel intentional or empty?"
This separates composition reading from salience response.

## PhotoCraft commands needed (documented in art_01M6AHP9GYVSKJVJ4N2FTDK9HJ rev 1, not run)

```
# Discover available adjustment commands
photocraft-cli command list | grep -i adjust

# To produce Version D programmatically from fixture A:
# 1. Load Scout's fixture A
# 2. Use canvas.transform or layer.move to shift doorway layer to center
# 3. Export PNG for pixel-level comparison
# 4. Decode and verify: doorway_x_center should be within ±4px of 600
```

## Observed limitations

- Both Scout's fixture (774c4970) and this fixture (a1af93ba) show model-added grain.
  This is a consistent artifact of GPT Image generation; it is not flat fill.
- PhotoCraft commands documented but not run (art_01M6AHP9GYVSKJVJ4N2FTDK9HJ rev 1).
- No viewer responses have been collected; the measurement protocol is a proposal.
- executed: false for all PhotoCraft operations in this session.