"""pytest harness for Scout artifact 09f9d3c3-06cb-4ef0-b89b-26faa9c79341.

Pre-condition: run Scout's lut3d_commands.sh first so the diff PNGs exist.
Expected outputs under test:
  diff_n_vs_tl.png   -- nearest vs trilinear on the hue-sweep gradient
  diff_tl_vs_tet.png -- trilinear vs tetrahedral on the same gradient

All assertions below are PROPOSALS until a runner produces the PNGs.
Cite: art_01M6VM5DCRRQ32378328NBG3XF r1 (source-documented option names).
"""
import pathlib
import numpy as np
from PIL import Image
import pytest

DIFF_N_TL  = pathlib.Path("diff_n_vs_tl.png")
DIFF_TL_TET = pathlib.Path("diff_tl_vs_tet.png")

# --- helpers ---

def _load_max_channel(path: pathlib.Path) -> int:
    """Return the maximum single-channel value across all pixels."""
    arr = np.array(Image.open(path).convert("RGB"))
    return int(arr.max())

def _load_changed_pixel_count(path: pathlib.Path) -> int:
    """Return the number of pixels where any channel != 0."""
    arr = np.array(Image.open(path).convert("RGB"))
    return int(np.any(arr != 0, axis=-1).sum())

# --- existence tests (run first; failures block later tests) ---

@pytest.mark.order(1)
def test_diff_n_vs_tl_exists():
    """Scout's shell script must have produced the nearest-vs-trilinear diff."""
    assert DIFF_N_TL.exists(), (
        f"{DIFF_N_TL} not found. Run lut3d_commands.sh before pytest."
    )

@pytest.mark.order(1)
def test_diff_tl_vs_tet_exists():
    """Scout's shell script must have produced the trilinear-vs-tetrahedral diff."""
    assert DIFF_TL_TET.exists(), (
        f"{DIFF_TL_TET} not found. Run lut3d_commands.sh before pytest."
    )

# --- quantitative assertions ---

@pytest.mark.order(2)
def test_nearest_differs_from_trilinear():
    """Nearest must differ from trilinear on a 2x2x2 LUT + hue gradient.

    If this fails (all-black diff), the choice of interpolation mode makes
    no measurable difference at this LUT resolution. That is a useful null.
    """
    count = _load_changed_pixel_count(DIFF_N_TL)
    assert count > 0, (
        "nearest == trilinear on this gradient (null result — record it)."
    )

@pytest.mark.order(2)
def test_nearest_vs_trilinear_max_delta():
    """Record the worst-case channel offset between nearest and trilinear.

    No threshold is set here; the value is only printed.
    Running with -s shows it; a future threshold can be added once a
    baseline from a real run is known.
    """
    max_val = _load_max_channel(DIFF_N_TL)
    print(f"\n[OBSERVED] nearest vs trilinear max channel delta: {max_val}/255")
    # Assertion: value must be in range (not a corrupt file).
    assert 0 <= max_val <= 255

@pytest.mark.order(3)
def test_tetrahedral_refinement_over_trilinear():
    """Record whether tetrahedral adds visible refinement over trilinear.

    all-black => tetrahedral has no benefit on this gradient at 2x2x2.
    non-black  => tetrahedral is measurably different; cost may be justified.
    """
    count = _load_changed_pixel_count(DIFF_TL_TET)
    max_val = _load_max_channel(DIFF_TL_TET)
    print(
        f"\n[OBSERVED] trilinear vs tetrahedral: "
        f"{count} differing pixels, max delta {max_val}/255"
    )
    # No pass/fail threshold — emit the observation for the record.
    assert 0 <= max_val <= 255