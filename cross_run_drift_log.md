# Cross-Run Beat Drift Log

**Source:** `art_01M64VK6KWRB2EV6BSZKABD55X r2`  
**Purpose:** Accumulate B5 (two-shot) first-seen times across runs to test the early-arrival claim.

---

## Historical Rows (from source article, H01 observations)

| Run ref | Look target | B3 first-seen (s) | B5 first-seen (s) | Early? | Notes |
|---------|-------------|-------------------|-------------------|--------|-------|
| Runs 1–6 (grouped) | Mixed | ~7.5 | ~15.9 | No | Baseline group |
| Early run A | Unknown | ~4.2 | ~10.9 | Yes | ~5 s ahead on B5 |
| Early run B | Unknown | ~7.5 est. | ~14.2 | Yes | ~1.7 s ahead on B5 |

*These rows are H01 retrospective observations, not independently verified.*

---

## New Rows (add per scored run)

| Run ref | Look target | B3 first-seen (s) | B5 first-seen (s) | Early? | Notes |
|---------|-------------|-------------------|-------------------|--------|-------|
| | | | | | |

---

## Threshold Proposal (unfilled — requires evidence before use)

- **On-time:** B5 within 14.2–17.6 s  
- **Early by 1 sample:** B5 at 12.5–14.1 s  
- **Early by 2+ samples:** B5 at ≤ 12.4 s  

Thresholds are proposals derived from the 8-run sample. Do not treat as rules until ≥ 16 runs are logged.

---

## Next Improvement

Fill one new row using `beat_timing_sheet.md` for a *fresh* run with the same prompt.  
Compare B5 first-seen against the 15.9 s baseline.  
If it falls in the early window, record which look target and whether B3 also arrived early (Early Run A pattern) or B3 was on-time (Early Run B pattern).