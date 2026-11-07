"""Generate a 512x32 black-to-white ramp PNG for lut1d banding tests.

This image has maximum sensitivity to interpolation stepping:
a pure luminance ramp exercises every code value the LUT maps.
Requires Pillow. Output: gradient.png
"""
import sys
try:
    from PIL import Image
except ImportError:
    sys.exit("Install Pillow: pip install Pillow")

W, H = 512, 32
img = Image.new("RGB", (W, H))
px = img.load()
for x in range(W):
    v = int(x / (W - 1) * 255)
    for y in range(H):
        px[x, y] = (v, v, v)
img.save("gradient.png")
print("Wrote gradient.png (512x32 luminance ramp)")