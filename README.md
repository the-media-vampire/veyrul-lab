# Negated-prop falsification classifier

Classifies a set of per-still inspection verdicts for a *negated* prompt constraint
(e.g. "no lid") into one of four compliance patterns:

| Classification | Meaning |
|---|---|
| `always_present` | Negation fully ignored — prop in every still |
| `sometimes_present` | Partial compliance — prop in some stills |
| `never_present` | Negation respected — prop absent from all inspected stills |
| `ambiguous_only` | Cannot determine — all stills inconclusive |

## Source

Drawn from the HF-PKG-014 finding in `art_01M6A5NN0JFR92YNZ3YG1V3B85 r1`:
> "a prop that the constraints negated ('no lid') was drawn anyway in every sampled still"

This classifier operationalises that observation into a reusable verdict form.

## What this does and does not do

- **Does:** distinguish the severity of negation-failure across classification tiers.
- **Does not:** verify whether a still was correctly inspected; verdict quality is the caller's responsibility.
- **Does not:** distinguish stills from the same frame vs. different temporal positions.
- **Limit:** an `ambiguous_only` result yields `falsified=False` and `coverage_pct=0.0` — this is not evidence of compliance, it is absence of evidence.

## Companion tools

- Sampling coverage audit: `7ae60924-2c06-46cd-88f4-25f4e13882c0` (Delta)
- Deviation log and lock-precision form: `99fb4501-249c-4776-b997-df56fc4a9a58` (Forge)

## Execution

Execution receipt: `53b2d852-968f-4e10-8306-6557a275a452`, exit 0.

## Usage

```python
from negated_prop_classifier import classify_negated_prop

result = classify_negated_prop(['present', 'present', 'absent', 'ambiguous'])
print(result['classification'])  # 'sometimes_present'
print(result['falsified'])       # True
```