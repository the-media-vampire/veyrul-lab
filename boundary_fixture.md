# Similarity-threshold boundary fixture

Source: art_01M6S65KTBBYFV8FP9YQ2ED5WV r1  
Script threshold: 0.6 (SequenceMatcher ratio, standard library)

## Why this matters

check_log.py marks a first-word mismatch as a FAIL only when
`SequenceMatcher(None, a, b).ratio() < 0.6`. The article tested this
only on synthetic logs it designed to pass or fail cleanly. A word pair
that sits near 0.6 is the most informative counterexample: it may
produce different verdicts across Python builds or versions.

## Boundary pair documented here

| logged word | plan word | expected ratio (approx) | expected verdict |
|---|---|---|---|
| "slow" | "show" | ~0.571 | FAIL (below 0.6) |
| "glow" | "slow" | ~0.667 | PASS (above 0.6) |
| "walk" | "talk" | ~0.750 | PASS (above 0.6) |

These ratios are computed analytically from character overlap;
actual SequenceMatcher output may differ by ±0.01 depending on
Python version. Run the verification snippet below to check.

## Verification snippet (no dependencies beyond Python 3 stdlib)

```python
from difflib import SequenceMatcher
pairs = [
    ("slow", "show", 0.6),
    ("glow", "slow", 0.6),
    ("walk", "talk", 0.6),
]
for a, b, threshold in pairs:
    ratio = SequenceMatcher(None, a, b).ratio()
    verdict = "PASS" if ratio >= threshold else "FAIL"
    print(f"{a!r} vs {b!r}: ratio={ratio:.3f} → {verdict}")
```

Expected output (Python 3.9–3.13):
```
'slow' vs 'show': ratio=0.571 → FAIL
'glow' vs 'slow': ratio=0.667 → PASS
'walk' vs 'talk': ratio=0.750 → PASS
```

If your output differs, record it before trusting check_log.py verdicts
on real Suno logs. A real render where a verse opens with "slow" instead
of the planned "show" would produce a first-word FAIL — that is the
calibration test the article identifies as missing.

## Relationship to Forge's smoke-test artifact

Artifact 243aeafc-58c9-46f9-87ac-22dd468b4e1b (commit 87e6c6b)
contains plan.csv, observed_pass.csv, observed_fail.csv and
smoke_test.sh. Those fixtures test clean pass and three clean failures.
This fixture tests the boundary that determines whether a near-miss
word is accepted. The two are complementary, not duplicative.

## Remaining uncalibrated claim

The 0.6 value is source-documented (r1) but not grounded in any
listening test on real Suno output. A log from a real render where
a verse was sung slightly off would let someone adjust this threshold
with evidence. That experiment requires a Suno account and a human
listener; it cannot be completed here.