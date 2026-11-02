"""adapter.py — TrueScope interface contract helpers.
Source: art_01M6D2YB2J8Q7XXSY91CCNZ1DG r1. Nothing run against TrueScope."""

TRUESCOPE_AXIS_MAX = 1023
TRUESCOPE_CAPTURE_MAX = 255
TRUESCOPE_HISTOGRAM_BINS = 256
TRUESCOPE_CLIP_THRESHOLD = 0.0158  # 1.58% of frame pixels (documented default)


def pixel_to_axis(value_8bit: int) -> float:
    """Map 8-bit pixel value to TrueScope's 0-1023 display axis."""
    assert 0 <= value_8bit <= 255
    return value_8bit * (TRUESCOPE_AXIS_MAX / TRUESCOPE_CAPTURE_MAX)


def compute_histogram(channel: list[int], bins: int = TRUESCOPE_HISTOGRAM_BINS) -> list[int]:
    """Bin 8-bit channel values into TrueScope's 256-bin histogram."""
    counts = [0] * bins
    for v in channel:
        counts[min(v * bins // 256, bins - 1)] += 1
    return counts


def integration_check(meta: dict) -> list[str]:
    """Check image metadata against TrueScope's documented assumptions.
    Keys: bit_depth (int), post_ocio (bool), has_fxaa (bool), post_processing_flag (bool)."""
    issues = []
    if meta.get("bit_depth", 8) != 8:
        issues.append(f"Bit depth {meta['bit_depth']} != 8: TrueScope captures 8-bit.")
    if not meta.get("post_ocio", False):
        issues.append("Colour space: image is pre-OCIO; TrueScope measures post-OCIO.")
    if meta.get("has_fxaa", False):
        issues.append("AA: image has FXAA; TrueScope is pre-FXAA. Edge counts will differ.")
    if not meta.get("post_processing_flag", True):
        issues.append("Post-processing flag off: TrueScope cannot capture in this mode.")
    return issues or ["All documented assumptions satisfied."]


if __name__ == "__main__":
    print(pixel_to_axis(0))    # 0.0
    print(pixel_to_axis(255))  # 1023.0
    good = {"bit_depth": 8, "post_ocio": True, "has_fxaa": False, "post_processing_flag": True}
    bad  = {"bit_depth": 16, "post_ocio": False, "has_fxaa": True, "post_processing_flag": True}
    print(integration_check(good))
    print(integration_check(bad))