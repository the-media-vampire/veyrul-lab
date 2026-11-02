"""Tests for gsl_constraints.py.

Run with: python -m pytest test_gsl_constraints.py -v
No network or GPU needed. All expected values from art_01M6CXXT85NWH4F1W8NYD08JCQ r1.
"""

import pytest
from gsl_constraints import (
    capture_config_ok,
    nearest_valid_supersampling,
    sh_codebook_limit,
    max_std_dev_ok,
    lod_spacing_ok,
    CAPTURE_MAX_PRODUCT,
    MAX_STD_DEV_MIN,
    MAX_STD_DEV_MAX,
)


# ── SplatCapture ──────────────────────────────────────────────────────────────

class TestCaptureConfigOk:
    """Boundary and over-limit cases for w * h * ss <= 8192."""

    @pytest.mark.parametrize("w,h,ss", [
        (64,   64,  2),   # 8192 exactly
        (128,  64,  1),   # 8192 exactly
        (32,   32,  8),   # 8192 exactly
        (8192,  1,  1),   # 8192 exactly
        (1,     1,  1),   # trivially fine
    ])
    def test_at_or_below_limit(self, w, h, ss):
        assert capture_config_ok(w, h, ss) is True

    @pytest.mark.parametrize("w,h,ss", [
        (64,   64,  3),   # 12288
        (128,  64,  2),   # 16384
        (32,   32,  9),   # 9216
        (8193,  1,  1),   # 8193
    ])
    def test_over_limit(self, w, h, ss):
        assert capture_config_ok(w, h, ss) is False

    def test_boundary_value(self):
        assert CAPTURE_MAX_PRODUCT == 8192


class TestNearestValidSupersampling:
    def test_64x64(self):
        # 8192 / (64*64) = 2
        assert nearest_valid_supersampling(64, 64) == 2

    def test_128x64(self):
        assert nearest_valid_supersampling(128, 64) == 1

    def test_invalid_dimensions(self):
        with pytest.raises(ValueError):
            nearest_valid_supersampling(0, 64)


# ── SH codebook limits ────────────────────────────────────────────────────────

class TestShCodebookLimit:
    def test_sh1(self):
        assert sh_codebook_limit(1) == 65_536

    def test_sh2(self):
        assert sh_codebook_limit(2) == 174_763

    def test_sh3(self):
        assert sh_codebook_limit(3) == 327_680

    def test_monotonically_increasing(self):
        limits = [sh_codebook_limit(d) for d in (1, 2, 3)]
        assert limits == sorted(limits)

    def test_invalid_degree(self):
        with pytest.raises(ValueError):
            sh_codebook_limit(4)


# ── maxStdDev ─────────────────────────────────────────────────────────────────

class TestMaxStdDev:
    def test_lower_bound(self):
        assert MAX_STD_DEV_MIN == 2.0

    def test_upper_bound(self):
        assert MAX_STD_DEV_MAX == 3.0

    @pytest.mark.parametrize("v", [2.0, 2.5, 3.0])
    def test_in_range(self, v):
        assert max_std_dev_ok(v) is True

    @pytest.mark.parametrize("v", [1.9, 3.1, 0.0])
    def test_out_of_range(self, v):
        assert max_std_dev_ok(v) is False


# ── LOD spacing ──────────────────────────────────────────────────────────────

class TestLodSpacing:
    def test_default_in_range(self):
        from gsl_constraints import LOD_BASE_SPACING_DEFAULT
        assert lod_spacing_ok(LOD_BASE_SPACING_DEFAULT) is True

    @pytest.mark.parametrize("v", [1.1, 1.75, 16.0])
    def test_boundary_values(self, v):
        assert lod_spacing_ok(v) is True

    @pytest.mark.parametrize("v", [1.0, 16.1, 0.0])
    def test_out_of_range(self, v):
        assert lod_spacing_ok(v) is False