# Integration contract: colorchannelmixer + curves

## When to use colorchannelmixer alone
- You need a linear cross-channel mix (grayscale, sepia, channel swap).
- You want explicit, arithmetic control over each output channel.
- You need luminance preservation (pc=lum) without a separate filter.

## When to use curves alone
- You need nonlinear tone shaping per channel (gamma, contrast S-curve).
- The color relationships are already correct; only brightness/contrast needs work.

## When to chain them (the composable case)
- Mix first (colorchannelmixer), tone second (curves).
- The interface between them: a decoded RGB pixel stream — no metadata needed.
- Order matters: reversing (curves then mix) changes the result because
  the mix is linear and curves may shift the channel values the mix expects.

## Failure modes to test
- Coefficient sum ≠ 1 in colorchannelmixer → brightness drift; use pc=lum or audit weights.
- Chaining with a YUV-only filter between them breaks the RGB assumption.
- Sepia coefficients with pc=lum at pa<1.0 produce a partial correction; set pa=1.0 for full.

## Evidence status
- colorchannelmixer options and presets: source-documented (art_01M6VJS0YQE8PBGBG1H50KN8MF r1).
- curves interface: documented in same FFmpeg filters source (not independently fetched here).
- Chain behavior and order-dependence: derived by mechanism analysis; untested by run.