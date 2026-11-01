"""beat_frame_selector.py
Proposal only — not run against a live Seedance output.
Models the frame selection logic described in the interface contract:
given 12 sampled frames at ~1.7s apart, identify beat 3 (close-up)
as the candidate for single-image-to-3D input.

Input format assumed: list of dicts with keys
  {"frame_index": int, "beat_label": str, "timestamp_s": float}
where beat_label is one of: "wide_open", "metalwork", "closeup", "hands", "wide_close".
This schema is inferred from art_01M64VK8QZGMMWD7HW0B566NTP r2; actual export
format is unknown and this script will need adjustment.
"""

from typing import Optional

BEAT_PRIORITY = ["closeup", "hands", "metalwork", "wide_close", "wide_open"]


def select_best_frame(frames: list[dict]) -> Optional[dict]:
    """
    Return the frame most suitable for single-image-to-3D.
    Priority: closeup > hands > metalwork > wide_close > wide_open.
    Ties broken by earliest timestamp.
    Returns None if frames is empty.
    """
    if not frames:
        return None
    for beat in BEAT_PRIORITY:
        candidates = [f for f in frames if f.get("beat_label") == beat]
        if candidates:
            return min(candidates, key=lambda f: f["timestamp_s"])
    # fallback: first frame
    return min(frames, key=lambda f: f["timestamp_s"])


if __name__ == "__main__":
    # Example with the observed beat order from the article
    example_frames = [
        {"frame_index": 0, "beat_label": "wide_open", "timestamp_s": 0.0},
        {"frame_index": 1, "beat_label": "wide_open", "timestamp_s": 1.7},
        {"frame_index": 2, "beat_label": "metalwork", "timestamp_s": 3.4},
        {"frame_index": 3, "beat_label": "metalwork", "timestamp_s": 5.1},
        {"frame_index": 4, "beat_label": "closeup", "timestamp_s": 6.8},
        {"frame_index": 5, "beat_label": "closeup", "timestamp_s": 8.5},
        {"frame_index": 6, "beat_label": "hands", "timestamp_s": 10.2},
        {"frame_index": 7, "beat_label": "wide_close", "timestamp_s": 11.9},
    ]
    best = select_best_frame(example_frames)
    print(f"Selected frame: {best}")
    # Expected: frame_index=4, closeup at 6.8s