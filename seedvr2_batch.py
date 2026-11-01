"""seedvr2_batch.py
SeedVR2 4n+1 batch-size validator and planner.
Source: art_01M6C05XVHXM6QZVT6KJ8NJFCP r1 (README at commit 4490bd1f).

The SeedVR2 README states batch_size must satisfy the 4n+1 pattern:
  valid values: 1, 5, 9, 13, 17, 21, 25, 29, 33, ...
It also documents uniform_batch_size: pads the last batch so every
batch seen by the model has exactly batch_size frames.
Example from README: 45 frames at batch_size=33 -> two batches of 33.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List


def is_valid_batch_size(b: int) -> bool:
    """Return True iff b satisfies the 4n+1 rule (b >= 1, (b-1) % 4 == 0)."""
    return b >= 1 and (b - 1) % 4 == 0


def next_valid(b: int) -> int:
    """Smallest valid batch size >= b."""
    b = max(b, 1)
    r = (b - 1) % 4
    return b if r == 0 else b + (4 - r)


def prev_valid(b: int) -> int:
    """Largest valid batch size <= b (minimum 1)."""
    b = max(b, 1)
    return b - (b - 1) % 4


@dataclass
class Batch:
    index: int
    effective_frames: int   # frames the model sees (padded if needed)
    actual_frames: int      # real source frames in this batch
    padded: bool            # True if trailing frames were padded


def plan_batches(
    total_frames: int,
    batch_size: int,
    uniform: bool = True,
) -> List[Batch]:
    """
    Plan how SeedVR2 will split total_frames into batches.

    Args:
        total_frames: number of source frames.
        batch_size:   must satisfy the 4n+1 rule or ValueError is raised.
        uniform:      if True, pad the last batch to batch_size
                      (uniform_batch_size=true in the node).

    Returns list of Batch objects.
    """
    if not is_valid_batch_size(batch_size):
        raise ValueError(
            f"batch_size={batch_size} violates 4n+1 rule. "
            f"Try {prev_valid(batch_size)} or {next_valid(batch_size)}."
        )
    batches: List[Batch] = []
    cursor = 0
    idx = 0
    while cursor < total_frames:
        actual = min(total_frames - cursor, batch_size)
        padded = uniform and actual < batch_size
        effective = batch_size if padded else actual
        batches.append(Batch(idx, effective, actual, padded))
        cursor += actual
        idx += 1
    return batches


if __name__ == "__main__":
    # Reproduce README example: 45 frames, batch_size=33, uniform=True
    batches = plan_batches(45, 33, uniform=True)
    print("45 frames @ batch_size=33, uniform=True:")
    for b in batches:
        print(f"  {b}")