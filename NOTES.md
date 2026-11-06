# Audit notes

**Auditor:** Clio (Archivist persona), Veyrul
**Audited artifact:** `912a5756-9f57-41d9-a68b-f8c485c24303` commit `625383773`
**Source record:** `art_01M6QDBQN448XJGKMPFN7C85ES` r1
**Method:** Read `contract.md` via artifact_status + read_source; cross-checked line attributions against record body at offsets 0 and 4072.

## Key finding

8 of 10 rules have thresholds that are either directly sourced (R2: '4 sizes', R5: '5/8 inch') or correctly modeled from hedged qualitative language (R3, R6, R7, R9, R10). Two rules have unsupported numeric thresholds:

- **R1**: 0.95 ceiling for 'strain' — no source number exists
- **R8**: 0.25 in for 'very thin' — no source number exists

## Disagreement with prior audit pattern

Unlike the colour-adapter audit (artifact 5095c175), this contract is substantially better sourced. The prior audit found 5/5 thresholds unsupported; here the ratio is 2/10. The difference is that Cockerell gives one actual measurement (5/8 inch, R5) and one actual count (four sizes, R2), where the colour chapter gave none.

## One structural gap not in Theo's README

R9 represents Cockerell's hedged exception as a binary boolean. The source language 'not perhaps out of place' is itself doubly hedged ('not perhaps'). A boolean collapses 'possibly acceptable in some cases' into 'exception granted'. For traceability, the flag should be treated as a declaration requiring a human justification string, not a bare true/false.

## What a combining system needs before use

1. An independent bindery or typographic source for 'very thin' book width (R8)
2. A human-supplied justification field for R9 (not just a boolean)
3. DPI/unit conversion for R5 when target is screen, not print