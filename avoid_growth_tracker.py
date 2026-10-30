# avoid_growth_tracker.py
# Source: art_01M67ACYEDW3GH3RZKZRKQF0RN r1 (Veyrul)
# MIT License
"""
Track the growth of a prompt Negative sentence across takes.
Input : [(label: str, avoid_count: int), ...] in chronological order.
Output: monotonicity status, per-step deltas, and any regressions.
"""

from typing import List, Tuple


def track_avoid_growth(take_sequence: List[Tuple[str, int]]) -> dict:
    """
    Parameters
    ----------
    take_sequence : list of (label, count) in chronological order

    Returns
    -------
    dict with keys:
      counts           – {label: count}
      deltas           – {"A->B": delta}
      weakly_monotone  – True if no delta < 0
      strictly_increasing – True if every delta > 0
      regressions      – [(from_label, to_label, delta)] where delta < 0
    """
    if len(take_sequence) < 2:
        raise ValueError("Need at least two takes to compare.")
    if any(c < 0 for _, c in take_sequence):
        raise ValueError("Avoid-item counts must be non-negative.")

    labels  = [l for l, _ in take_sequence]
    counts  = [c for _, c in take_sequence]
    deltas  = [counts[i+1] - counts[i] for i in range(len(counts) - 1)]
    delta_labels = [f"{labels[i]}->{labels[i+1]}" for i in range(len(deltas))]

    regressions = [
        (labels[i], labels[i+1], deltas[i])
        for i, d in enumerate(deltas) if d < 0
    ]

    return {
        "counts":              dict(zip(labels, counts)),
        "deltas":              dict(zip(delta_labels, deltas)),
        "weakly_monotone":     all(d >= 0 for d in deltas),
        "strictly_increasing": all(d > 0  for d in deltas),
        "regressions":         regressions,
    }


FALSIFYING_CONDITIONS = [
    "Any future take whose Avoid-list count is LOWER than the previous take's count.",
    "A take where a failure is fixed upstream (continuity sentence) and the Avoid list shrinks.",
    "A take regenerated from a new seed that resets the count to a lower baseline.",
    "Evidence of de-duplication: two items covering the same failure collapse into one.",
]