"""Assertion harness for Scout's circular vs. linear heading RMSE predictions.

Source: art_01M6VDTP1SRA5R2KX5NW9H0D13 r1 (CharForge branch-cut failure)
Extends: artifact 3475b84f-516d-42a4-8258-32c7bc0d9f17 (Scout experiment brief)

SCOPE: This checks the numeric predictions in the brief. It does not replace
the CharForge PR regression suite, test_core, or test_circular.

Inputs (fixed):
  left_toe_A = +179 degrees
  left_toe_B = -179 degrees
  phase samples = [0.0, 0.25, 0.50, 0.75, 1.0]

Predictions under test:
  Linear RMSE   ~= 358 deg  (midpoint at t=0.25 collapses to 0 deg)
  Circular RMSE ~=   2 deg  (shortest-arc, midpoint at t=0.25 ~= +/-180 deg)

Tolerance: 0.5 deg to account for floating-point rounding only.
Any failure means either the formula or the fixture is wrong.
"""

import math
import numpy as np

TOLERANCE = 0.5  # degrees

A = 179.0
B = -179.0
TRUE_HEADING = 179.0  # constant "ground truth" trace; difference should be ~2 deg
PHASES = np.array([0.0, 0.25, 0.50, 0.75, 1.0])


def linear_interp(a, b, t):
    return a + (b - a) * t


def circular_interp(a, b, t):
    """Shortest-arc interpolation. Wraps delta to [-180, 180)."""
    delta = ((b - a) + 180) % 360 - 180
    return a + delta * t


def rmse(predicted, reference):
    residuals = ((predicted - reference + 180) % 360) - 180  # wrap to [-180,180)
    return math.sqrt(np.mean(residuals ** 2))


def run():
    linear_vals = linear_interp(A, B, PHASES)
    circular_vals = circular_interp(A, B, PHASES)
    reference = np.full_like(PHASES, TRUE_HEADING)

    linear_rmse = rmse(linear_vals, reference)
    circular_rmse = rmse(circular_vals, reference)

    # --- midpoint diagnostics (t=0.25 index 1) ---
    linear_mid = linear_vals[1]
    circular_mid = circular_vals[1]

    print(f"Linear   interp values: {np.round(linear_vals, 2)}")
    print(f"Circular interp values: {np.round(circular_vals, 2)}")
    print(f"Linear   RMSE: {linear_rmse:.4f} deg  (predicted ~358)")
    print(f"Circular RMSE: {circular_rmse:.4f} deg  (predicted ~2)")
    print(f"Linear   midpoint at t=0.25: {linear_mid:.2f} deg  (predicted 0)")
    print(f"Circular midpoint at t=0.25: {circular_mid:.2f} deg  (predicted ~+-180)")

    # --- assertions ---
    assert abs(linear_rmse - 358.0) < TOLERANCE, (
        f"FAIL linear RMSE: got {linear_rmse:.4f}, expected ~358 +/- {TOLERANCE}. "
        "Check fixture or formula."
    )
    assert abs(circular_rmse - 2.0) < TOLERANCE, (
        f"FAIL circular RMSE: got {circular_rmse:.4f}, expected ~2 +/- {TOLERANCE}. "
        "Check shortest-arc formula or wrap in rmse()."
    )
    assert abs(linear_mid - 0.0) < TOLERANCE, (
        f"FAIL linear midpoint: got {linear_mid:.4f}, expected 0 +/- {TOLERANCE}."
    )
    assert abs(abs(circular_mid) - 180.0) < TOLERANCE, (
        f"FAIL circular midpoint: got {circular_mid:.4f}, expected +/-180 +/- {TOLERANCE}."
    )

    print("\nAll assertions PASSED. Predictions confirmed by formula.")
    print("NOTE: This does not substitute for running CharForge PR#1 regression suite.")


if __name__ == "__main__":
    run()