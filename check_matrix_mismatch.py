"""601-vs-709 colour-matrix round-trip validator.

Demonstrates the shift described in EncodingGuidelines docs:
ffmpeg assumes BT.601 for untagged stills; players decode as BT.709.
Result: measurable per-channel error on chromatic content.

Usage:
    python check_matrix_mismatch.py

No external dependencies beyond numpy.
Source reference: art_01M6CQ0D711XXF9QTA7NVVMCJP rev 2
"""
import numpy as np

# ── ITU matrices (full-range, luma-coefficients only) ────────────────────────
M_601 = np.array([
    [ 0.299,    0.587,    0.114   ],
    [-0.168736,-0.331264, 0.5    ],
    [ 0.5,     -0.418688,-0.081312],
])
M_709 = np.array([
    [ 0.2126,   0.7152,   0.0722  ],
    [-0.114572,-0.385428, 0.5    ],
    [ 0.5,     -0.454153,-0.045847],
])
M_601_inv = np.linalg.inv(M_601)
M_709_inv = np.linalg.inv(M_709)

# ── Test patches (normalised 0-1 linear) ─────────────────────────────────────
PATCHES = {
    'black' :  [0.0,  0.0,  0.0 ],
    'red'   :  [1.0,  0.0,  0.0 ],
    'green' :  [0.0,  1.0,  0.0 ],
    'blue'  :  [0.0,  0.0,  1.0 ],
    'yellow':  [1.0,  1.0,  0.0 ],
    'purple':  [0.5,  0.3,  0.8 ],
    '18grey':  [0.18, 0.18, 0.18],
}

def round_trip(rgb: np.ndarray, enc: np.ndarray, dec: np.ndarray) -> np.ndarray:
    """Encode RGB→YCbCr with enc, decode with dec."""
    return (dec @ (enc @ rgb.T)).T


def run_comparison() -> None:
    data = np.array(list(PATCHES.values()))
    labels = list(PATCHES.keys())

    # Baseline: encode 601 (ffmpeg default), decode 709 (player expectation)
    baseline = round_trip(data, M_601, M_709_inv)
    # Fixed: encode 709, decode 709
    fixed    = round_trip(data, M_709, M_709_inv)

    err_b = np.abs(baseline - data)
    err_f = np.abs(fixed    - data)

    print(f"{'Patch':<10} {'Baseline L1':>12} {'Fixed L1':>10}  Decoded R G B (baseline)")
    print("-" * 65)
    for i, name in enumerate(labels):
        print(f"{name:<10}  {err_b[i].mean():>10.5f}   {err_f[i].mean():>8.5f}"
              f"  {np.round(baseline[i], 4).tolist()}")

    print()
    print(f"Mean over chromatic patches:")
    print(f"  Baseline (601-enc / 709-dec): {err_b.mean():.5f}")
    print(f"  Fixed    (709-enc / 709-dec): {err_f.mean():.8f}")
    print()
    print("Fix: pass -colorspace bt709 -color_primaries bt709 -color_trc iec61966-2-1")
    print("     (sRGB transfer) in ffmpeg when source is sRGB/Rec.709.")


if __name__ == '__main__':
    run_comparison()