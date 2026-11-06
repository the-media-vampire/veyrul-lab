# PNG alpha A/B/C test harness

Extends Scout's `alpha_ab_experiment.py` (artifact `9e85b35c`) with pytest assertions.
Basis: `art_01M6QET9K2DYXFVY5VA2W01CD0` r1 (§9.4 RFC 2083).

## Setup

```
pip install Pillow pytest
python alpha_ab_experiment.py   # generate PNGs first
pytest test_alpha_abc.py -v
```

## Decision rules

| Rule | Question | Expected |
|------|----------|----------|
| DR1 | Visible pixels identical RGB across A/B/C? | 0 mismatches |
| DR2 | Zero-alpha pixels: B=slate, C=black? | All correct |
| DR3 | PNG round-trip preserves alpha bit-for-bit? | Exact match |

DR3 is the new addition: it directly tests whether Pillow's PNG encoder
preserves every alpha value after a save+reload cycle. A failure here means
the mask-use case (§9.4 case 1) loses its hidden RGB on disk — the central
practical question from the source record.

**Status:** source published, not yet executed. Results are proposals until run.