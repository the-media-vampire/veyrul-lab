"""Pixel-row diff for the discriminating test.
Run after both conditions have produced PNGs.
Python 3 + Pillow required.
"""
from PIL import Image, ImageChops
import sys

def check(a_path, b_path):
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    if a.size != b.size:
        print("SIZE MISMATCH", a.size, b.size)
        sys.exit(1)
    diff = ImageChops.difference(a, b)
    px   = diff.load()
    w, h = diff.size
    # Check border rows (the stress rows)
    border_nonzero = [
        (x, y)
        for y in [0, h-1]
        for x in range(w)
        if px[x, y] != (0, 0, 0)
    ]
    full_nonzero = sum(
        1 for y in range(h) for x in range(w) if px[x,y] != (0,0,0)
    )
    print(f"Border-row non-zero pixels : {len(border_nonzero)}")
    print(f"Full-image non-zero pixels : {full_nonzero}")
    if full_nonzero == 0:
        print("RESULT: conditions are pixel-identical — strategy choice is style only.")
    else:
        print("RESULT: conditions differ — inspect border_nonzero list for bleed.")
        if border_nonzero:
            print("  First differing border pixel:", border_nonzero[0])

if __name__ == "__main__":
    check(
        sys.argv[1] if len(sys.argv) > 1 else "condition_a.png",
        sys.argv[2] if len(sys.argv) > 2 else "condition_b.png",
    )