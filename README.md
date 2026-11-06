# Morris 1895 spacing note — CSS constraint contract

Source: art_01M6Q9V6AWKE9BM6MDAGT34K8V r1. File: eBook 31596, pg31596.txt, lines 136–165, 178.

## Four rules → four CSS custom properties

| Property | Source lines | Pass condition |
|---|---|---|
| `--letter-fit` | 136, 138 | ≤ 0 (tracking not opened) |
| `--word-spacing` | 138–143 | single uniform token |
| `--line-leading` | 145–151 | ≤ 1.2 proposed ceiling (WARN); >1.5 ERROR |
| `--margin-order` | 152–157 | four numbers: inner ≤ top ≤ outside ≤ bottom |

## Assumption log

- **A1** `--letter-fit=0` maps metal face/body to CSS letter-spacing neutral. No source number.
- **A2** River detection needs a layout engine; only non-uniform tokens flagged here.
- **A3** 1.2 ceiling derived from "thin/hair" language (lines 148–149). Not a source measurement.
- **A4** "20 per cent" second-hand report (lines 158–161) has no base; not encoded.
- **A5** All CSS connections are curator inference, untested (source Limits section).

## What breaks when combining with another system

A fluid/variable-font type scale produces continuous size steps; R3 leading threshold (A3) may fire spuriously if line-height is computed dynamically. Resolve before combining.