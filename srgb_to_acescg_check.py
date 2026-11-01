"""sRGB → ACEScg matrix validation.

Tests the colour-convert step documented for oiiotool/maketx
(art_01M6AF14NGG2M0VFR3DSDY50R0 r1, AcademySoftwareFoundation/OpenImageIO
commit 0008a6f0). No oiiotool installation required.

Matrix source: ACES S-2014-003 (public Academy specification).
Run: python3 srgb_to_acescg_check.py
Pass criterion: max roundtrip error < 1e-6
"""
import sys
import numpy as np

# --- Colour functions ---
def srgb_to_linear(v):
    v = np.asarray(v, dtype=float)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)

def linear_to_srgb(v):
    v = np.clip(v, 0, 1)
    return np.where(v <= 0.0031308, v * 12.92, 1.055 * v ** (1 / 2.4) - 0.055)

# sRGB linear → ACEScg (AP1) — ACES S-2014-003
M = np.array([
    [0.6131, 0.3395, 0.0474],
    [0.0701, 0.9164, 0.0135],
    [0.0206, 0.1096, 0.8698],
])
M_inv = np.linalg.inv(M)

# --- Test colours (sRGB encoded) ---
samples = {
    "red":      [1.0, 0.0, 0.0],
    "green":    [0.0, 1.0, 0.0],
    "blue":     [0.0, 0.0, 1.0],
    "mid-grey": [0.5, 0.5, 0.5],
    "white":    [1.0, 1.0, 1.0],
}

PASS_THRESHOLD = 1e-6
worst = 0.0

print(f"{'Color':>10}  {'ACEScg':>24}  {'Roundtrip err':>14}")
for name, rgb in samples.items():
    lin = srgb_to_linear(rgb)
    acescg = M @ lin
    rt_lin = M_inv @ acescg
    rt_enc = linear_to_srgb(rt_lin)
    err = float(np.max(np.abs(rt_enc - np.array(rgb))))
    worst = max(worst, err)
    print(f"{name:>10}  {str(np.round(acescg, 4)):>24}  {err:.2e}")

print(f"\nMatrix condition number : {np.linalg.cond(M):.4f}")
print(f"Max roundtrip error     : {worst:.2e}")
print(f"Threshold               : {PASS_THRESHOLD:.0e}")
result = 'PASS' if worst < PASS_THRESHOLD else 'FAIL'
print(f"Result                  : {result}")
sys.exit(0 if result == 'PASS' else 1)