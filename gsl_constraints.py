"""Gaussian-Splat-Lite documented constraints.

Source: art_01M6CXXT85NWH4F1W8NYD08JCQ r1 (files read, library not run).
All values are from the library documentation at commit b85bcca0.
Nothing here runs the library or validates GPU behaviour.
"""

import math
from typing import Tuple

# --- SplatCapture ---

CAPTURE_MAX_PRODUCT = 8192
"""width * height * supersampling must not exceed this value."""

def capture_config_ok(width: int, height: int, supersampling: int) -> bool:
    """Return True if the capture config satisfies the documented cap.

    Documented constraint: width * height * supersampling <= 8192.
    Pixels are returned as RGBA bytes, bottom row first.
    Float targets cannot be read back.
    """
    return width * height * supersampling <= CAPTURE_MAX_PRODUCT


def nearest_valid_supersampling(width: int, height: int) -> int:
    """Return the largest integer supersampling value that keeps w*h*ss within budget."""
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    return max(1, CAPTURE_MAX_PRODUCT // (width * height))


# --- Spherical Harmonics codebook limits (RAD builder) ---

SH_CODEBOOK_MAX_ENTRIES: dict[int, int] = {
    1: 65_536,
    2: 174_763,
    3: 327_680,
}
"""Maximum codebook entries per SH degree for RAD builder output."""

def sh_codebook_limit(degree: int) -> int:
    """Return the documented codebook entry cap for the given SH degree (1-3)."""
    if degree not in SH_CODEBOOK_MAX_ENTRIES:
        raise ValueError(f"SH degree must be 1, 2 or 3; got {degree}")
    return SH_CODEBOOK_MAX_ENTRIES[degree]


# --- Renderer: maxStdDev ---

MAX_STD_DEV_MIN = math.sqrt(4)   # 2.0 — documented lower bound
MAX_STD_DEV_MAX = math.sqrt(9)   # 3.0 — documented upper bound

def max_std_dev_ok(value: float) -> bool:
    """Return True if maxStdDev is within the documented acceptable range."""
    return MAX_STD_DEV_MIN <= value <= MAX_STD_DEV_MAX


# --- RAD builder: lod-base spacing ---

LOD_BASE_SPACING_DEFAULT = 1.75
LOD_BASE_SPACING_MIN = 1.1
LOD_BASE_SPACING_MAX = 16.0

def lod_spacing_ok(value: float) -> bool:
    """Return True if lod-base spacing is within the documented range."""
    return LOD_BASE_SPACING_MIN <= value <= LOD_BASE_SPACING_MAX