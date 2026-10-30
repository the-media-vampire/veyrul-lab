"""
test_safe_frame.py
MIT License — see LICENSE

Runnable test suite for safe_frame.norm_box_to_pixels.
No third-party dependencies.

Usage:
    python test_safe_frame.py

All three cases must print PASS for the module to be considered correct.
"""

from safe_frame import norm_box_to_pixels

W, H = 1024, 1024
passed = 0
failed = 0


def check(label, fn, *args, expect_value=None, expect_error=None):
    global passed, failed
    try:
        result = fn(*args)
        if expect_error is not None:
            print(f"FAIL  {label}: expected {expect_error.__name__}, got result {result}")
            failed += 1
        elif result == expect_value:
            print(f"PASS  {label}: {result}")
            passed += 1
        else:
            print(f"FAIL  {label}: got {result}, expected {expect_value}")
            failed += 1
    except Exception as exc:
        if expect_error is not None and isinstance(exc, expect_error):
            print(f"PASS  {label}: raised {type(exc).__name__}: {exc}")
            passed += 1
        else:
            print(f"FAIL  {label}: unexpected {type(exc).__name__}: {exc}")
            failed += 1


# Case 1: Centered 50 % box
check(
    "centered 50%",
    norm_box_to_pixels,
    W, H, 0.5, 0.5, 0.5, 0.5,
    expect_value=(256, 256, 768, 768),
)

# Case 2: Boundary box — full frame
check(
    "boundary full-frame",
    norm_box_to_pixels,
    W, H, 0.5, 0.5, 1.0, 1.0,
    expect_value=(0, 0, 1024, 1024),
)

# Case 3: Out-of-bounds — right edge at 0.9+0.25=1.15
check(
    "out-of-bounds right",
    norm_box_to_pixels,
    W, H, 0.9, 0.5, 0.5, 0.5,
    expect_error=ValueError,
)

print(f"\n{passed} passed, {failed} failed.")
if failed:
    raise SystemExit(1)