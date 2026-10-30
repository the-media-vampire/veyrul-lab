# interval_check.py — Shot Coverage Gap Checker

A small, dependency-free Python utility that validates a list of `(start, end)` shot intervals against a total plan duration. Returns gaps, overlaps and invalid interval details as a plain dict.

## Run the self-test

```bash
python interval_check.py
```

Expected output: JSON receipt with `"all_passed": true` for four built-in cases.

## API

```python
from interval_check import check_intervals

result = check_intervals([(0, 5), (5, 10)], total_duration=10.0)
# result["valid"]    -> True
# result["gaps"]     -> []
# result["overlaps"] -> []
# result["coverage"] -> 10.0
```

### Return keys

| Key | Type | Meaning |
|---|---|---|
| `valid` | bool | False if any interval fails validation (all other keys then reflect that state) |
| `invalid_intervals` | list | Offending `(start, end)` pairs (reversed, negative or exceeding duration) |
| `gaps` | list | `(gap_start, gap_end)` ranges not covered by any interval |
| `overlaps` | list | `(overlap_start, overlap_end)` ranges covered by more than one interval |
| `coverage` | float | Non-overlapping seconds covered |

## Tested cases (execution receipt: run_python 2026-10-29)

| Case | Input | Expected |
|---|---|---|
| gap_free | `[(0,5),(5,10)]` | valid, no gaps, no overlaps |
| gap | `[(0,4),(5,10)]` | valid, gap `(4,5)` |
| overlap | `[(0,6),(5,10)]` | valid, overlap `(5,6)` |
| reversed_invalid | `[(7,3)]` | invalid |

All four assertions passed (exit 0, archive SHA-256 `07f3c4f8…`).

## Limits

- Rejects the **entire** call if any interval is invalid; no partial analysis.
- Touching endpoints (e.g. `(0,5)` and `(5,10)`) are treated as gap-free, not overlapping. This matches frame-cut shot plans where one shot ends exactly where the next begins.
- Floating-point times accepted; input need not be pre-sorted.
- Does not handle `NaN`, `Inf` or negative `total_duration`.
- Missing edge case: a single interval that starts after `t=0` leaves a leading gap — not covered by the four built-in tests.

## License

MIT — see source header.