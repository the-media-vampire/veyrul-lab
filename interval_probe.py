"""interval_probe.py — Vera verification artifact
Source: art_01M6S6H21MK5NVE4FB3NJ4YFCM r1
Companion to Forge artifact ff8620e2 (per_arm + verdict harness).

This probe targets Claim C: the read() confidence-interval formula
for the worked-example actual results.

Stated (from article):
  A: 311 conversions / 3890 delivered
  B: 360 conversions / 3996 delivered
  alpha: 0.05
  Expected interval: -0.22 to +2.24 percentage points
  Expected verdict: INCONCLUSIVE
  smallest_lift: 0.02 (2 percentage points)

Not executed — proposal until run on Python 3.
If a check fails at the last decimal, check rounding tolerance before
concluding the article is wrong; printed values may be truncated.
"""
import math
from statistics import NormalDist

Z = NormalDist().inv_cdf
TOL = 0.005  # 0.005 pp tolerance for printed truncation

def run_interval_probe():
    # Worked-example actual results (article-stated)
    na, ca = 3890, 311
    nb, cb = 3996, 360
    alpha = 0.05
    lift = 0.02

    pa = ca / na
    pb = cb / nb
    diff = pb - pa
    half = Z(1 - alpha / 2) * math.sqrt(
        pa * (1 - pa) / na + pb * (1 - pb) / nb
    )
    low_pct  = (diff - half) * 100
    high_pct = (diff + half) * 100

    print(f"pa={pa*100:.4f}%  pb={pb*100:.4f}%")
    print(f"diff={diff*100:+.4f} pp")
    print(f"half-width={half*100:.4f} pp")
    print(f"interval: {low_pct:+.2f} to {high_pct:+.2f} pp")

    # Claim C checks
    article_low  = -0.22
    article_high = +2.24
    checks = [
        ("low  within tolerance of -0.22", abs(low_pct  - article_low)  <= TOL),
        ("high within tolerance of +2.24", abs(high_pct - article_high) <= TOL),
    ]

    # Verdict check: low<0 and high reaches lift => inconclusive
    verdict_inconclusive = (low_pct < 0) and (high_pct >= lift * 100)
    checks.append(("verdict is INCONCLUSIVE", verdict_inconclusive))

    passed = 0
    for label, result in checks:
        status = "PASS" if result else "FAIL"
        if result:
            passed += 1
        print(f"  {status}  {label}")

    print(f"\n{passed}/{len(checks)} checks passed")
    if passed < len(checks):
        print("FAIL — at least one Claim C check failed; inspect tolerance or article rounding.")
        return False
    print("OK — Claim C interval matches article within tolerance.")
    return True

if __name__ == "__main__":
    run_interval_probe()