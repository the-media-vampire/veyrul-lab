"""Flicker analog measurement for AI video output.

Book claim (art_01M6QAFXM1NHAWKJGDSKRG0HWM r1, lines 1502-1506, 1516-1525):
  - Light is shut off while film moves; subject is always still when seen.
  - Illusion depends on persistence of vision (~1/25 s).
  - 'Flicker' = effect of too long a bright period (curator gloss).

AI analog: no shutter exists, but frame-to-frame luminance jumps are
measurable and serve as a proxy for perceived flicker.

Metric: Mean Absolute Luminance Difference (MALD) across consecutive frames.
  - Low MALD  -> smooth brightness continuity (book ideal).
  - High MALD -> abrupt jumps; perceived flicker analog.

This script is NOT executed here. It documents the measurement protocol
so another operator can run it on any rendered MP4.

Usage (requires opencv-python, numpy):
  python flicker_luminance_check.py <video_path> [--threshold 8.0]

Outputs:
  - Per-frame luminance array (mean Y channel, BT.601)
  - MALD scalar
  - Frame indices where |delta_L| > threshold (candidate flicker frames)
  - CSV: frame_index, mean_lum, delta_lum
"""

import argparse
import csv
import sys

# --- protocol constants ---
BT601_R, BT601_G, BT601_B = 0.299, 0.587, 0.114
DEFAULT_THRESHOLD = 8.0  # luminance units (0-255 scale); tune per use


def frame_luminances(video_path: str) -> list:
    """Return mean luminance per frame using BT.601 weights."""
    # Pseudocode body — replace with real cv2 calls:
    #   cap = cv2.VideoCapture(video_path)
    #   while cap.isOpened():
    #       ret, frame = cap.read()  # BGR uint8
    #       if not ret: break
    #       b, g, r = frame[:,:,0], frame[:,:,1], frame[:,:,2]
    #       lum = BT601_R*r + BT601_G*g + BT601_B*b
    #       luminances.append(float(lum.mean()))
    raise NotImplementedError("Implement with cv2.VideoCapture")


def compute_mald(luminances: list) -> dict:
    """Compute MALD and flag candidate flicker frames."""
    deltas = [abs(luminances[i+1] - luminances[i])
               for i in range(len(luminances) - 1)]
    mald = sum(deltas) / len(deltas) if deltas else 0.0
    return {"mald": mald, "deltas": deltas}


def write_csv(path: str, luminances: list, deltas: list) -> None:
    """Write per-frame report."""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["frame_index", "mean_lum", "delta_lum"])
        for i, lum in enumerate(luminances):
            delta = deltas[i] if i < len(deltas) else ""
            w.writerow([i, f"{lum:.3f}", f"{delta:.3f}" if delta != "" else ""])


def main():
    p = argparse.ArgumentParser(description="Flicker analog metric for AI video.")
    p.add_argument("video_path")
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    p.add_argument("--csv_out", default="flicker_report.csv")
    args = p.parse_args()

    lums = frame_luminances(args.video_path)
    result = compute_mald(lums)
    write_csv(args.csv_out, lums, result["deltas"])

    flicker_frames = [i for i, d in enumerate(result["deltas"])
                      if d > args.threshold]
    print(f"MALD: {result['mald']:.3f}")
    print(f"Candidate flicker frames (delta > {args.threshold}): {flicker_frames}")
    print(f"CSV written: {args.csv_out}")


if __name__ == "__main__":
    main()