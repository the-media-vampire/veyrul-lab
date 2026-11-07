"""Generate a 512x512 smooth RGB gradient PNG for LUT interpolation testing.
Requires: Pillow  (pip install Pillow)
Outputs:  gradient_test.png

Design: left→right hue sweep (R→G→B→R), top→bottom brightness ramp.
This maximises the chance of revealing stepping from nearest-neighbour interpolation.
"""
import sys
try:
    from PIL import Image
except ImportError:
    sys.exit("Install Pillow: pip install Pillow")

import colorsys

W, H = 512, 512
img = Image.new("RGB", (W, H))
px = img.load()

for y in range(H):
    brightness = 0.3 + 0.7 * (y / (H - 1))  # 0.3 .. 1.0 top→bottom
    for x in range(W):
        hue = x / W  # 0.0 .. 1.0 left→right
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, brightness)
        px[x, y] = (int(r * 255), int(g * 255), int(b * 255))

img.save("gradient_test.png")
print("Wrote gradient_test.png")