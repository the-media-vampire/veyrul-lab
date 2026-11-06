# Baseline comparison guide

Source: art_01M6MH8DFE1KD1GQA0A0VTGENT rev 2 — documented, not tested.
This file tells you *what to break* to verify each checklist rule.

## Experiment table

| Rule | Line to change | Expected failure |
|------|---------------|------------------|
| Coerce types | Remove `String(d.year)` | year→number, Plot infers linear scale, bars smear across a continuous axis |
| Band scale | Same as above | No discrete band; bars may overlap or disappear |
| group transform | Duplicate a row in `data`, do not use `groupX` | Double-counted bar; use `groupX({y:"sum"},{x:"year",...})` to fix |
| stack implicit | Remove `fx:"region"` from both marks | Bars stack instead of sitting side-by-side |
| zero domain | Remove `zero:true` from y scale | Y axis may start above 0, bars appear taller than they are |
| tickFormat | Add `tickFormat: d=>d` and change data years to 2000–2001 | Years print with no separator by default; set tickFormat to format explicitly |
| text mark | Remove the `Plot.text(...)` mark | Labels disappear; axis alone remains |

## How to run

```bash
npm install @observablehq/plot d3
# Then paste plot-grouped-bar.js into an Observable notebook cell,
# or run in Node 18+ ESM context.
```

## Limits
- Code is not executed in the lab; it is source only.
- Each experiment is a proposal until someone runs it and reports the observed output.
- Text mark pixel alignment is explicitly flagged as unverified by the source docs.