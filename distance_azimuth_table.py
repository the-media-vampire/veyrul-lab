"""distance_azimuth_table.py

Computes combined PannerNode gain (inverse distance model × equalpower panning)
for two refDistance scenes across three azimuths and several distances.

Formulas are taken verbatim from the Web Audio specification as documented in
art_01M6SGCBMEEBQYN1Z8T18ANGPA revision 1 (source_inspected; browser steps untested).
No audio is rendered; no browser is required. Needs only the Python standard library.

Usage:
    python distance_azimuth_table.py

Interesting question this table answers:
    At what distance does the -3.01 dB straight-ahead panning tax
    become smaller than the scene-unit shift from changing refDistance?
    Answer: immediately — refDistance 20 vs refDistance 1 differs by >20 dB at d=10.
    That is the discriminating observation: the panning correction is a rounding
    error compared with an unconsidered refDistance.
"""
import math

# --- formulas from spec (art_01M6SGCBMEEBQYN1Z8T18ANGPA rev 1) ---

def inverse_gain(d, ref=1.0, rolloff=1.0):
    """ref / (ref + rolloff * (max(d, ref) - ref))"""
    d_eff = max(d, ref)
    denom = ref + rolloff * (d_eff - ref)
    if denom == 0:
        return float('inf')
    return ref / denom

def equalpower_lr(azimuth_deg):
    """Returns (left_gain, right_gain) for equalpower panner.
    Spec: x = (azimuth+90)/180, L=cos(x*pi/2), R=sin(x*pi/2).
    Azimuth clamped to [-90, 90] by the spec (behind folds to front).
    """
    az = max(-90.0, min(90.0, azimuth_deg))  # spec folds >90 onto front
    x = (az + 90.0) / 180.0
    left  = math.cos(x * math.pi / 2.0)
    right = math.sin(x * math.pi / 2.0)
    return left, right

def to_db(gain):
    if gain <= 0:
        return float('-inf')
    return 20.0 * math.log10(gain)

# --- experiment parameters ---

SCENES = [
    {"label": "refDist=1  (default)",  "ref": 1.0,  "rolloff": 1.0},
    {"label": "refDist=20 (three.js example)", "ref": 20.0, "rolloff": 1.0},
]

DISTANCES = [1, 2, 5, 10, 20, 50, 100]

AZIMUTHS = [
    ("ahead  ( 0°)",   0.0),
    ("right (45°)",   45.0),
    ("hard-R(90°)",   90.0),
]

# --- print table ---

print("\nPannerNode combined level: inverse model × equalpower panning")
print("Source: art_01M6SGCBMEEBQYN1Z8T18ANGPA rev 1 (browser steps untested)")
print("Columns: dist_gain_dB | L_pan_dB | R_pan_dB | L_total_dB | R_total_dB")
print("")

for scene in SCENES:
    ref     = scene["ref"]
    rolloff = scene["rolloff"]
    print(f"=== Scene: {scene['label']} ===")
    hdr = f"{'dist':>6}  {'azimuth':<14}  {'dist(dB)':>9}  {'L-pan(dB)':>10}  {'R-pan(dB)':>10}  {'L-tot(dB)':>10}  {'R-tot(dB)':>10}"
    print(hdr)
    print("-" * len(hdr))
    for d in DISTANCES:
        dg = inverse_gain(d, ref=ref, rolloff=rolloff)
        dg_db = to_db(dg)
        for az_label, az in AZIMUTHS:
            lg, rg = equalpower_lr(az)
            l_total_db = to_db(dg * lg)
            r_total_db = to_db(dg * rg)
            print(
                f"{d:>6}  {az_label:<14}  "
                f"{dg_db:>+9.2f}  "
                f"{to_db(lg):>+10.2f}  "
                f"{to_db(rg):>+10.2f}  "
                f"{l_total_db:>+10.2f}  "
                f"{r_total_db:>+10.2f}"
            )
    print("")

print("KEY OBSERVATIONS (computed, not measured in browser):")
print("  1. Straight-ahead: L and R each -3.01 dB (not 0 dB) — the panning tax.")
print("  2. Hard-right (90°): L = -inf dB (silent), R = 0 dB relative to dist gain.")
print("  3. refDist=20 vs refDist=1 at d=10: dist gain is 0 dB vs -20 dB — 20 dB shift.")
print("     The panning correction (-3.01 dB) is negligible by comparison.")
print("  4. This is the discriminating test: which variable dominates your mix error?")
print("     Answer from this table: an unconsidered refDistance, not azimuth panning.")