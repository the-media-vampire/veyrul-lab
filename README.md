# Cover Spread Preflight

Sources: printer specs from **art_01M6K1452AX5GW86HWQAVGQBNE rev 1** (2026-11-03).

## Interface
`SpreadSpec` -> `validate()` -> `List[Finding(severity, rule, detail)]`

## Does NOT
- Compute spine width (use printer's own calculator/template).
- Validate colour space or ICC profile.
- Guarantee printer acceptance.

## Combining with outpainting
Run `validate()` on your *intended* `SpreadSpec` **before** the outpaint step.
A `FAIL` on `canvas_width`/`canvas_height` means the target canvas is wrong —
cheaper to fix than re-running the model. Re-run after flattening to confirm
`has_alpha=False`.