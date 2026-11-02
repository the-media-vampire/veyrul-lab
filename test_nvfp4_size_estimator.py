"""Tests for nvfp4_size_estimator.py — run with pytest or python."""
from nvfp4_size_estimator import estimate_nvfp4_size, PID_CALIBRATED_BF16_FRACTION


def test_pid_self_check():
    """Calibrated estimate must reproduce the PiD card numbers within 1%."""
    result = estimate_nvfp4_size(2.61e9, bf16_fraction=PID_CALIBRATED_BF16_FRACTION)
    # Card states 1,091,499,246 bytes (art_01M6EA07T9KRDAS7559V91MCA7 r1)
    assert abs(result["estimated_nvfp4_bytes"] - 1_091_499_246) < 1_091_499_246 * 0.01
    assert result["saving_pct"] == 58.2


def test_pure_fp4_lower_bound():
    """bf16_fraction=0 → pure FP4 group-16: ratio should be 0.3125."""
    result = estimate_nvfp4_size(1e9, bf16_fraction=0.0)
    assert result["blended_ratio"] == 0.3125


def test_no_quantization():
    """bf16_fraction=1.0 → no quantization: ratio should be 1.0."""
    result = estimate_nvfp4_size(1e9, bf16_fraction=1.0)
    assert result["blended_ratio"] == 1.0
    assert result["saving_pct"] == 0.0


def test_reference_table():
    """Saving percentage is constant regardless of file size (linear)."""
    sizes = [1e9, 5e9, 10e9, 24e9]
    ratios = [estimate_nvfp4_size(s)["blended_ratio"] for s in sizes]
    assert len(set(ratios)) == 1, "Ratio must be size-independent"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"{name}: PASSED")