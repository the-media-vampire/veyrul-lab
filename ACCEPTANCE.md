# Break-table acceptance criteria

Source: art_01M6MH8DFE1KD1GQA0A0VTGENT rev 2 (checklist),
Forge artifact 914dd5ed-c3b7-4a98-af0d-dfa9e7f50ada (break table, unrun).

Each row pairs a proposed break with an **exact, falsifiable test condition**.
A runner marks PASS if the condition is met in the browser, FAIL otherwise.
An unexpected FAIL or unexpected PASS is new evidence worth reporting.

| # | Break | Proposed failure (Forge) | Acceptance criterion (falsifiable) | Disproof condition |
|---|-------|--------------------------|------------------------------------|-----------------|
| 1 | Remove `String(d.year)` | Linear scale replaces band; bars smear | `plot.scale('x').type === 'linear'` evaluates truthy in devtools; bars render as a continuous range, not discrete columns | x scale type is still `'band'` without the coercion |
| 2 | Remove `fx:"region"` | Regions collapse into stacked bars | `barY` output has no `fx` facet channel; bars from different regions share the same x position and stack vertically | Bars remain side-by-side without fx |
| 3 | Remove `zero:true` | Y domain starts above 0 | `plot.scale('y').domain[0] > 0` in devtools; the y-axis baseline is visibly above zero | Baseline stays at 0 without the option |
| 4 | Remove `Plot.text(...)` | No direct labels; axis alone remains | No `<text>` elements with bar-value content appear in the SVG; only axis tick labels remain | Value labels still appear via another mechanism |

## How to run

1. Paste `plot-grouped-bar.js` from artifact 914dd5ed into an Observable notebook.
2. Apply each break in a separate cell, one at a time.
3. For criterion 1–3: open browser devtools and evaluate the stated expression.
4. For criterion 4: inspect the rendered SVG (right-click → Inspect).
5. Record PASS, FAIL or UNEXPECTED and the browser + Plot version.

## Status

All rows are **proposals**. No run has been reported against this spec.
First runner: please note the Observable Plot version and browser used.