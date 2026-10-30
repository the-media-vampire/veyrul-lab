"""interval_check.py — shot coverage gap checker (MIT).

Usage:
    python interval_check.py

Function:
    check_intervals(intervals, total_duration=10.0) -> dict

Limits:
    - start < end required; 0 <= start, end <= total_duration.
    - Floating-point times; input need not be sorted.
    - Rejects any interval that violates validation; no partial analysis.
    - Does not handle NaN, Inf or negative total_duration.
    - Sweep counts open/close events; adjacent touching intervals (e.g. (0,5),(5,10))
      are gap-free, not overlapping (correct for frame-cut shot plans).
"""
import json


def check_intervals(intervals, total_duration=10.0):
    """Check shot intervals for gaps, overlaps and invalid entries.

    Args:
        intervals: list of (start, end) float-or-int pairs (seconds).
        total_duration: expected end of the shot plan (default 10.0 s).

    Returns:
        dict with keys:
          valid            – bool; False if any interval fails validation.
          invalid_intervals – list of offending (start, end) pairs.
          gaps             – list of (gap_start, gap_end) uncovered ranges.
          overlaps         – list of (overlap_start, overlap_end) ranges
                             covered by more than one interval.
          coverage         – float, non-overlapping seconds covered.
    """
    invalid = []
    valid_ivals = []

    for iv in intervals:
        s, e = iv
        if s >= e or s < 0 or e > total_duration:
            invalid.append(iv)
        else:
            valid_ivals.append((s, e))

    if invalid:
        return {
            "valid": False,
            "invalid_intervals": invalid,
            "gaps": [],
            "overlaps": [],
            "coverage": 0.0,
        }

    sorted_ivals = sorted(valid_ivals, key=lambda x: x[0])

    events = []
    for s, e in sorted_ivals:
        events.append((s, +1))
        events.append((e, -1))
    events.sort()

    gaps, overlaps = [], []
    depth, prev_t, coverage = 0, 0.0, 0.0

    for t, delta in events:
        if t > prev_t:
            if depth == 0:
                gaps.append((prev_t, t))
            elif depth == 1:
                coverage += t - prev_t
            else:  # depth > 1
                overlaps.append((prev_t, t))
                coverage += t - prev_t
        depth += delta
        prev_t = t

    if prev_t < total_duration and depth == 0:
        gaps.append((prev_t, total_duration))

    return {
        "valid": True,
        "invalid_intervals": [],
        "gaps": gaps,
        "overlaps": overlaps,
        "coverage": round(coverage, 6),
    }


# ── Self-test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    TOTAL = 10.0
    cases = [
        {"name": "gap_free",        "intervals": [(0, 5), (5, 10)],
         "expect_valid": True,  "expect_gaps": [],          "expect_overlaps": []},
        {"name": "gap",             "intervals": [(0, 4), (5, 10)],
         "expect_valid": True,  "expect_gaps": [(4.0, 5.0)], "expect_overlaps": []},
        {"name": "overlap",         "intervals": [(0, 6), (5, 10)],
         "expect_valid": True,  "expect_gaps": [],          "expect_overlaps": [(5.0, 6.0)]},
        {"name": "reversed_invalid","intervals": [(7, 3)],
         "expect_valid": False, "expect_gaps": [],          "expect_overlaps": []},
    ]
    receipt = {"total_duration": TOTAL, "cases": []}
    all_passed = True
    for case in cases:
        r = check_intervals(case["intervals"], TOTAL)
        ok = (r["valid"] == case["expect_valid"]
              and r["gaps"] == case["expect_gaps"]
              and r["overlaps"] == case["expect_overlaps"])
        all_passed = all_passed and ok
        receipt["cases"].append({"name": case["name"], "passed": ok, "result": r})
    receipt["all_passed"] = all_passed
    print(json.dumps(receipt, indent=2))
    assert all_passed, "Test failure — see receipt"