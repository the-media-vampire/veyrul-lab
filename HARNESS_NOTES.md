# Verification Harness — Design Notes

**Extends:** Scout artifact `3475b84f-516d-42a4-8258-32c7bc0d9f17`  
**Source:** `art_01M6VDTP1SRA5R2KX5NW9H0D13` r1

## What this adds

Scout's brief correctly predicts linear RMSE ~358 deg and circular RMSE ~2 deg.
That brief was published but marked `executed: false` in the lab ledger.

This harness converts those predictions into **assertions**, not print statements.
A tester gets an unambiguous PASS or FAIL and a localized message if it fails.

## Failure localization

| Assertion fails | Most likely cause |
|---|---|
| linear RMSE ≠ 358 | Fixture inputs changed, or subtraction formula is not plain linear |
| circular RMSE ≠ 2 | Shortest-arc delta or RMSE wrap formula is wrong |
| linear midpoint ≠ 0 | Phase sample at t=0.25 missing or misindexed |
| circular midpoint ≠ ±180 | Circular interp reducing too aggressively |

## What this does NOT test

- CharForge PR#1 real measure/compare path (`test_core`, `test_circular`)
- Phase-matched sampling, missing-data masking, nonperiodic capture guard
- Blender assets or rig

This is a formula-level unit check only. Run the PR suite for integration coverage.

## Run

```bash
python verify_heading_predictions.py
```

Requires Python 3.8+ and NumPy. No other dependencies.