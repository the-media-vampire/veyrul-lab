"""Abstract video ending classifier: drain vs fill.

Source: art_01M64VKR0GN2KBH19JWXHJ7J4Y revision 2 (Veyrul).
Observed difference documented there:
  drain -> closing frames are black with one short red mark
  fill  -> closing frames are red-dominant

Input: closing_frames: list of dicts with keys r, g, b (0-255 per-frame mean).
Output: dict with verdict ("drain" | "fill" | "ambiguous"), avg_rgb,
        brightness, red_ratio.

Thresholds are a first approximation from two data points.
Calibrate with additional confirmed runs before relying on them.
"""

def classify_ending(closing_frames: list[dict]) -> dict:
    if not closing_frames:
        return {"verdict": "ambiguous", "reason": "no frames supplied"}

    avg_r = sum(f["r"] for f in closing_frames) / len(closing_frames)
    avg_g = sum(f["g"] for f in closing_frames) / len(closing_frames)
    avg_b = sum(f["b"] for f in closing_frames) / len(closing_frames)
    brightness = (avg_r + avg_g + avg_b) / 3
    total = avg_r + avg_g + avg_b
    red_ratio = avg_r / total if total > 0 else 0

    # Drain: dark overall, low absolute red (black bg + faint mark)
    if brightness < 60 and avg_r < 80:
        verdict = "drain"
    # Fill: red channel dominant and bright
    elif red_ratio > 0.60 and avg_r > 100:
        verdict = "fill"
    else:
        verdict = "ambiguous"

    return {
        "verdict": verdict,
        "avg_rgb": [round(avg_r, 1), round(avg_g, 1), round(avg_b, 1)],
        "brightness": round(brightness, 1),
        "red_ratio": round(red_ratio, 3),
    }