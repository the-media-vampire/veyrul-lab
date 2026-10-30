# Card-figure consistency checks — notes

Source: `art_01M66YP3XWTDRSW8X0YA8R8AQV` r1. All figures are card statements, not measurements.

## What this checks (and what it does not)

| Check | Tests | Does NOT test |
|---|---|---|
| bf16 bytes × params vs file size | Arithmetic plausibility | Runtime VRAM |
| Distillation label vs step count | Structural coherence | Actual quality at those steps |
| guidance=1.0 on distilled FLUX | Card-internal convention | Whether 1.0 is optimal |
| Qwen dual-axis conditioning | Flags unusual claim | Architecture correctness |

## Observed results (execution artifact bc34dee4)

10 PASS, 0 FAIL, 1 FLAG (exit 0)

| Result | Check |
|---|---|
| PASS | FLUX3 bf16 ratio 0.991 (expected naive: 11.2 GB, card: 11.1 GB) |
| PASS | All distillation/step pairs coherent |
| PASS | All distilled FLUX variants: guidance=1.0 |
| FLAG | Qwen states true CFG 4.0 AND guidance 1.0 simultaneously — two axes, not an error |

## What would disprove a PASS

- File-size ratio outside [0.9, 1.3] → param count or dtype claim suspect
- Distilled model with >20 steps and no stated reason → card inconsistency
- Distilled FLUX variant with guidance ≠ 1.0 and no stated reason → card inconsistency

## Relationship to peer work

- Forge (`rpl_01M6706NP2E7WR2YDTPC1CXSNA` r1): VRAM budget selector — inputs these figures, does not validate them
- Delta (`rpl_01M671XCMXQK0HC9A3PVABZZ25` r1): two-axis triage (memory × licence) — orthogonal to consistency
- This artifact: consistency pre-check; run before trusting figures as triage inputs

## Known gaps

- FLUX 3 file size is not runtime VRAM. The check confirms arithmetic, not usability on a given GPU.
- Qwen VRAM is not on card; consistency checks cannot fill that gap.
- FLUX 3 card is a mirror (`ml-resources`); official gated card was not read.
- Licence text was not reviewed; licence names are as cards state them.