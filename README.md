# Pygfx transparency contrast predictor

Predicts WCAG luminance contrast ratios for three conditions in a pygfx
transparency experiment before rendering anything.

**Source:** [art_01M6F68R6DTRP106T3W8BRANEK, revision 3]

## Observed output (exit 0, run via `run_python`)

```
Condition      Focal:Surround   Focal:BG
--------------------------------------------
Control              1.07:1      8.57:1
A (sel. transp)      2.81:1      8.57:1
B (shared transp)    1.05:1      2.89:1
```

## What this tells us

- **Control is a near-zero focal/surround contrast problem (1.07:1).**
  Amber and cyan have almost identical luminance. The cube is
  distinguishable by hue only — luminance gives no help.
- **Condition A raises focal:surround to 2.81:1** by dimming the cyan panels.
  Transparency is doing real luminance work here, not just aesthetic work.
- **Condition B collapses both contrasts**, eliminating focal:BG pop (8.57→2.89)
  while barely changing focal:surround (1.07→1.05). Shared transparency
  is a strict regression on every measurable axis.
- **The decision rule in Iris's brief** (prefer A only if it preserves core
  priority) is testable: A clearly wins on focal:surround; the question is
  whether the retained focal:BG edge (8.57:1) still reads at thumbnail size.

## Scout's proposed D-condition

Swap focal/surround hues: blue-grey cube, amber panels. If the same
alpha settings flip which object wins the viewer-response question,
hue — not alpha — is load-bearing. If hierarchy disappears entirely,
luminance/alpha control is dominant. One extra still, zero new parameters.

## Usage

```python
from contrast_predict import report
report()                          # default amber/cyan scene
report(focal_rgb=(0.2, 0.5, 0.9), surround_rgb=(1.0, 0.6, 0.0))  # D-condition
```