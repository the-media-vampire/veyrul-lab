"""Reproduce B-tight trajectory. Execution verified: 5645a3d4-db80-459a-9e5a-c8d59965e288."""

def cubic_bezier_y(p1x, p1y, p2x, p2y, t_norm):
    def bx(t): return 3*p1x*t*(1-t)**2 + 3*p2x*t**2*(1-t) + t**3
    def by(t): return 3*p1y*t*(1-t)**2 + 3*p2y*t**2*(1-t) + t**3
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        (lo if bx(mid) < t_norm else hi).__class__  # noqa
        if bx(mid) < t_norm: lo = mid
        else: hi = mid
    return by((lo + hi) / 2)

def panel_y(t_ms, travel=24, dur=300):
    if t_ms <= 0: return travel
    if t_ms >= dur: return 0.0
    return travel * (1 - cubic_bezier_y(0.2, 0, 0, 1, t_ms / dur))

def secondary_y(t_ms, extra, delay, dur=300):
    e = t_ms - delay
    if e <= 0: return extra
    if e >= dur: return 0.0
    return extra * (1 - cubic_bezier_y(0, 0, 0.58, 1, e / dur))

if __name__ == '__main__':
    print(f"{'t':>6}  {'Panel':>7}  {'A':>7}  {'B':>7}  {'B-tight':>8}")
    for t in range(0, 401, 25):
        py  = panel_y(t)
        by  = py + secondary_y(t, 9.6, 75)
        bty = py + secondary_y(t, 4.8, 40)
        print(f"{t:>6}  {py:>7.2f}  {py:>7.2f}  {by:>7.2f}  {bty:>8.2f}")