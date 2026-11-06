"""adjust_subs_for_join.py -- source sample, NOT executed.

Shifts subtitle cues for an xfade join at a known offset.
See README.md for preconditions and failure assumptions.
Requires pysubs2 (MIT, per prior proposal; commit 6371ae8b).
"""
from __future__ import annotations
import sys

try:
    import pysubs2
except ImportError:
    sys.exit("pysubs2 not installed")


def adjust_for_xfade(
    srt_path: str,
    out_path: str,
    xfade_offset_s: float,
    xfade_duration_s: float,
    which_clip: int,  # 1 or 2
) -> None:
    """Shift cues to match the joined output timeline.

    Clip-1: cues with .start > offset_ms shift forward by duration_ms.
    Clip-2: all cues shift forward by offset_ms.
    Raises if any cue lands at a negative start (silent failure guard).
    """
    subs = pysubs2.load(srt_path)
    offset_ms = int(xfade_offset_s * 1000)
    duration_ms = int(xfade_duration_s * 1000)

    for line in subs:
        if which_clip == 1:
            if line.start > offset_ms:
                line.start += duration_ms
                line.end += duration_ms
        elif which_clip == 2:
            line.start += offset_ms
            line.end += offset_ms
        else:
            raise ValueError("which_clip must be 1 or 2")
        if line.start < 0:
            raise ValueError(
                f"Negative start {line.start} ms after shift. "
                "Check xfade_offset_s and which_clip."
            )

    subs.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: adjust_subs_for_join.py "
              "<srt_in> <srt_out> <offset_s> <duration_s> <clip 1|2>")
        sys.exit(1)
    adjust_for_xfade(
        sys.argv[1], sys.argv[2],
        float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
    )