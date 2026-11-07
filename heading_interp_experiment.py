"""Experiment brief: circular vs. linear heading interpolation

Intention: Hold everything fixed except interpolation strategy.
Measure RMSE for the +179 / -179 boundary pair under each strategy.
Expected outcome: linear RMSE ~358 deg, circular RMSE ~2 deg.
This is the discriminating test described in art_01M6VDTP1SRA5R2KX5NW9H0D13 r1.

Not a CharForge install. Pure Python + NumPy. No GPU, no seed, no network.
"""
import numpy as np

# --- Shared fixture (hold all variables fixed except interpolation) ---
phases = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
ref_heading = np.full(5, 179.0)   # reference trace: toe at +179 deg
test_heading = np.full(5, -179.0) # test trace:      toe at -179 deg


def linear_interp_rmse(ref, test):
    """Scalar subtraction; no branch-cut awareness."""
    residuals = ref - test
    return float(np.sqrt(np.mean(residuals ** 2)))


def circular_rmse(ref, test):
    """Wrap residuals to [-180, 180) before squaring."""
    residuals = ref - test
    residuals = (residuals + 180.0) % 360.0 - 180.0
    return float(np.sqrt(np.mean(residuals ** 2)))


def midpoint_linear(a, b, t=0.25):
    """Linear blend; can produce 0 for antipodal inputs."""
    return a + t * (b - a)


def midpoint_circular(a, b, t=0.25):
    """Shortest-arc blend; correct for near-antipodal inputs."""
    diff = (b - a + 180.0) % 360.0 - 180.0
    return a + t * diff


# --- Run ---
rmse_linear = linear_interp_rmse(ref_heading, test_heading)
rmse_circular = circular_rmse(ref_heading, test_heading)
mid_linear = midpoint_linear(179.0, -179.0)
mid_circular = midpoint_circular(179.0, -179.0)

print(f"Linear RMSE:    {rmse_linear:.1f} deg  (expect ~358)")
print(f"Circular RMSE:  {rmse_circular:.1f} deg  (expect ~2)")
print(f"Linear midpoint at t=0.25:   {mid_linear:.1f} deg  (expect 0)")
print(f"Circular midpoint at t=0.25: {mid_circular:.1f} deg  (expect ~179)")
print()
print("PASS" if abs(rmse_linear - 358.0) < 1 and abs(rmse_circular - 2.0) < 1
      else "UNEXPECTED RESULT — recheck fixture")