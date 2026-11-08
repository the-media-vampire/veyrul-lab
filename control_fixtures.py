"""Synthetic pixel-array fixtures for sanity-checking blur measurements.

These are hand-computable ground-truth cases. Run them against any blur
measurement function (e.g. Delta's compare_luma) before trusting filter
output on real video.

Status: UNEXECUTED — no interpreter has run this code.
Source context: art_01M6WGWVXNKPZGYE6MDK0PPWKB r1
"""

# ---------------------------------------------------------------------------
# Fixture A: flat field — no detail, blur should change nothing
# Expected: detail_ratio = undefined (base detail = 0) or 1.0; MAE = 0
# Disproof: MAE > 0 on a flat field means your measurement has a bug.
# ---------------------------------------------------------------------------
FLAT_BASE  = [[128, 128, 128, 128, 128, 128]] * 4
FLAT_TRIAL = [[128, 128, 128, 128, 128, 128]] * 4

# ---------------------------------------------------------------------------
# Fixture B: hard edge — maximum adjacent-pixel contrast
# Hand-calculated detail for one row [0,0,0,255,255,255]:
#   dx contributions: 0,0,13005,0,0 → sum = 13005
#   For a 1-row array: dy = 0
#   detail = 13005 / (1*5 + 0*6) = 2601.0
#
# Softened edge [0,0,85,170,255,255] (illustrative, not an avgblur output):
#   dx: 0, 7225, 7225, 7225, 0 → sum = 21675
#   detail = 21675 / 5 = 4335.0
#   detail_ratio = 4335 / 2601 ≈ 1.665  ← RATIO > 1: softened ramp has MORE
#   adjacent variance than a step edge in this metric!
# This is the Delta warning: detail_ratio alone does not detect blur correctly
# for all edge profiles. A step→ramp transformation increases MSE gradient.
# ---------------------------------------------------------------------------
EDGE_BASE  = [[  0,   0,   0, 255, 255, 255]]
EDGE_TRIAL = [[  0,   0,  85, 170, 255, 255]]  # illustrative ramp, NOT avgblur

# EXPECTED detail values (hand-calculated, verify before trusting a function):
EDGE_BASE_DETAIL_EXPECTED  = 2601.0
EDGE_TRIAL_DETAIL_EXPECTED = 4335.0
EDGE_RATIO_EXPECTED        = 4335.0 / 2601.0   # ≈ 1.665 — counter-intuitive!

# ---------------------------------------------------------------------------
# Fixture C: sine-like gradient — a smooth signal blur should attenuate
# [0, 64, 128, 192, 255, 192, 128, 64] one cycle
# A 3-tap box blur of this row:
#   averaged: [32, 64, 128, 192, 213, 192, 128, 96] (boundary: reflect or clamp)
# detail should decrease vs original for a smooth signal.
# This is the case where detail_ratio < 1.0 is the expected result.
# ---------------------------------------------------------------------------
SINE_BASE  = [[  0,  64, 128, 192, 255, 192, 128,  64]]
SINE_TRIAL = [[ 32,  64, 128, 192, 213, 192, 128,  96]]  # illustrative 3-tap avg

# ---------------------------------------------------------------------------
# Validation note
# ---------------------------------------------------------------------------
# Fixture B deliberately shows a case where detail_ratio > 1 for a visually
# 'softer' result. This confirms Delta's warning that MAE detects change but
# does not identify blur, and that detail_ratio needs interpretation context.
# Use Fixture C (smooth signal) as the diagnostic case; use Fixture A as the
# zero-effect control. A measurement tool that fails Fixture A has a bug.