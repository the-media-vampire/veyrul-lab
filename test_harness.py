"""Inline arithmetic test harness for the two-arm creative comparison.

Tests per_arm() sample-size formula and verdict logic against the expected-check
table in art_01M6S6H21MK5NVE4FB3NJ4YFCM r1. No files, no subprocesses.

Run: python test_harness.py
"""
import math
from statistics import NormalDist, StatisticsError

Z = NormalDist().inv_cdf
LIMIT = 10 ** 12


def per_arm(base, lift, alpha, power):
    p1, p2 = base, base + lift
    mean = (p1 + p2) / 2
    try:
        top = (Z(1 - alpha / 2) * math.sqrt(2 * mean * (1 - mean))
               + Z(power) * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2)))
        return math.ceil((top / lift) ** 2)
    except (OverflowError, StatisticsError):
        return None


def verdict(pa, pb, na, nb, lift, alpha):
    """Return verdict string matching compare.py READING lines."""
    diff = pb - pa
    half = Z(1 - alpha / 2) * math.sqrt(
        pa * (1 - pa) / na + pb * (1 - pb) / nb
    )
    low, high = diff - half, diff + half
    if low > 0:
        label = "B beat A"
        if low < lift:
            label += ", but the lift may be below the size you said matters"
    elif high < 0:
        label = "A beat B"
        if high > -lift:
            label += ", but the gap may be below the size you said matters"
    elif -lift < low and high < lift:
        label = "no difference as large as the smallest lift: keep the cheaper or preferred creative"
    else:
        label = "inconclusive: a lift or a loss of the size you care about is still possible. Keep A, and do not call it a tie"
    return label, round(low * 100, 2), round(high * 100, 2)


FAIL = 0
PASS_COUNT = 0


def check(name, got, expected, note=""):
    global FAIL, PASS_COUNT
    ok = got == expected
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL += 1
    suffix = f"  # {note}" if note else ""
    print(f"{status}  {name}: got {got!r}, want {expected!r}{suffix}")


# --- per_arm arithmetic ---
# Source: article arithmetic: p̄=0.09, result 3,213 per arm
check("per_arm worked example", per_arm(0.08, 0.02, 0.05, 0.8), 3213)

# From expected-check table: audience 3,000 -> FAIL with detectable lift ~3.00 pp
# Verify by finding per_arm at the boundary audience of 3,000 (1,500 per arm)
# The article says detectable lift rounds to 3.00 points for 3,000 audience.
# We test that 1.5pp lift requires MORE than 1,500 per arm (too small)
check("3000 audience too small for 2pp lift",
      per_arm(0.08, 0.02, 0.05, 0.8) > 1500, True,
      "3213 per arm > 1500 half of 3000")

# For 40-subscriber audience: detectable lift reported as 38.24 pp
# per_arm at 20 each. Verify: lift of 0.3824 -> per_arm should be <= 20
check("40 audience: 38pp lift fits in 20 per arm",
      per_arm(0.08, 0.3824, 0.05, 0.8) <= 20, True)
# and 2pp still needs far more
check("40 audience too small for 2pp lift",
      per_arm(0.08, 0.02, 0.05, 0.8) > 20, True)

# --- verdict logic against 4 click scenarios from check table (3,213 per arm) ---
n = 3213
lift = 0.02
alpha = 0.05

# A 257, B 340 -> B beat A; interval +1.17 to +4.00
v, lo, hi = verdict(257/n, 340/n, n, n, lift, alpha)
check("B beat A label", v, "B beat A")
check("B beat A interval low",  lo, 1.17)
check("B beat A interval high", hi, 4.0)

# A 340, B 257 -> A beat B; interval -4.00 to -1.17
v, lo, hi = verdict(340/n, 257/n, n, n, lift, alpha)
check("A beat B label", v, "A beat B")
check("A beat B interval low",  lo, -4.0)
check("A beat B interval high", hi, -1.17)

# A 257, B 262 -> no difference; interval -1.18 to +1.49
v, lo, hi = verdict(257/n, 262/n, n, n, lift, alpha)
check("no difference label",
      v, "no difference as large as the smallest lift: keep the cheaper or preferred creative")
check("no difference interval low",  lo, -1.18)
check("no difference interval high", hi, 1.49)

# A 257, B 290 -> inconclusive; interval -0.34 to +2.39
v, lo, hi = verdict(257/n, 290/n, n, n, lift, alpha)
check("inconclusive label",
      v, "inconclusive: a lift or a loss of the size you care about is still possible. Keep A, and do not call it a tie")
check("inconclusive interval low",  lo, -0.34)
check("inconclusive interval high", hi, 2.39)

# --- worked example actual results: A 311/3890, B 360/3996 -> inconclusive ---
v, lo, hi = verdict(311/3890, 360/3996, 3890, 3996, 0.02, 0.05)
check("worked example verdict",
      v, "inconclusive: a lift or a loss of the size you care about is still possible. Keep A, and do not call it a tie")
check("worked example interval low",  lo, -0.22)
check("worked example interval high", hi, 2.24)

print(f"\n{PASS_COUNT} passed, {FAIL} failed")
if FAIL:
    raise SystemExit(1)