"""Write three minimal .cube LUT files for testing.
  identity.cube    — no change; confirms the pipeline works
  lift.cube        — lifts shadows (darkest point → 0.2); reveals interpolation on gradients
  crush.cube       — crushes highlights (brightest → 0.8); contrasting direction

All are 2x2x2 (8 corners only) to maximise interpolation gaps.
Format: Iridas .cube, as listed in art_01M6VM5DCRRQ32378328NBG3XF r1.
"""

def write_cube(path, title, entries):
    """entries: list of 8 (R G B) floats in .cube order (B-major)."""
    with open(path, "w") as f:
        f.write(f"TITLE \"{title}\"\n")
        f.write("LUT_3D_SIZE 2\n")
        for r, g, b in entries:
            f.write(f"{r:.6f} {g:.6f} {b:.6f}\n")
    print(f"Wrote {path}")

# .cube corner order: B inner loop, G middle, R outer (000,001,010,011,100,101,110,111)
identity = [
    (0.0, 0.0, 0.0), (0.0, 0.0, 1.0),
    (0.0, 1.0, 0.0), (0.0, 1.0, 1.0),
    (1.0, 0.0, 0.0), (1.0, 0.0, 1.0),
    (1.0, 1.0, 0.0), (1.0, 1.0, 1.0),
]

LIFT = 0.2
lift = [(r * (1 - LIFT) + LIFT, g * (1 - LIFT) + LIFT, b * (1 - LIFT) + LIFT)
        for r, g, b in identity]

CRUSH = 0.8
crush = [(r * CRUSH, g * CRUSH, b * CRUSH) for r, g, b in identity]

write_cube("identity.cube", "Identity", identity)
write_cube("lift.cube", "Lift shadows to 0.2", lift)
write_cube("crush.cube", "Crush highlights to 0.8", crush)