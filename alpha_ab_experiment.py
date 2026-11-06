"""PNG alpha A/B/C experiment — Scout, 2026-11-06
Basis: art_01M6QET9K2DYXFVY5VA2W01CD0 revision 1 (§9.4 of RFC 2083)
Iris proposal: rpl_01M6QF8ENWCF97SYXWKMVQ2N8C revision 1

Variants
--------
A  Editable mask:   full amber circle in RGB, alpha exposes only centre strip
B  Final cutout:    zero-alpha pixels set to slate RGB (same as §9.4 case 2)
C  Premultiplied-0: zero-alpha pixels set to RGB (0,0,0) — §9.4 line 2650
   This is Iris's missing third case; §9.4 gives THREE conflicting recommendations
   for transparent-pixel colour. C isolates the black-zeroes recommendation.

Outputs: a_mask.png, b_cutout.png, c_premul.png, audit.txt
Run: python alpha_ab_experiment.py
Requires: Pillow
"""
import os
from PIL import Image

W, H = 512, 512
AMBER   = (232, 154,  48)
SLATE   = ( 32,  40,  48)
BLACK   = (  0,   0,   0)
STRIP_L, STRIP_R = 224, 288   # Iris's vertical strip
CX, CY, R = 256, 256, 160

def in_circle(x, y):
    return (x - CX) ** 2 + (y - CY) ** 2 <= R * R

def in_strip(x):
    return STRIP_L <= x < STRIP_R

# Build base pixel arrays
pixels_A, pixels_B, pixels_C = [], [], []
for y in range(H):
    row_A, row_B, row_C = [], [], []
    for x in range(W):
        circle = in_circle(x, y)
        strip  = in_strip(x)
        rgb    = AMBER if circle else SLATE
        alpha  = 255 if (circle and strip) else 0

        # A: keep original RGB everywhere
        row_A.append(rgb + (alpha,))

        # B: zero-alpha → slate (§9.4 compression recommendation)
        rgb_b = rgb if alpha == 255 else SLATE
        row_B.append(rgb_b + (alpha,))

        # C: zero-alpha → black/zero (§9.4 premultiplied conversion, line 2650)
        rgb_c = rgb if alpha == 255 else BLACK
        row_C.append(rgb_c + (alpha,))

    pixels_A.append(row_A)
    pixels_B.append(row_B)
    pixels_C.append(row_C)

def make_image(pixels):
    img = Image.new('RGBA', (W, H))
    flat = [px for row in pixels for px in row]
    img.putdata(flat)
    return img

imgs = {'a_mask': make_image(pixels_A),
        'b_cutout': make_image(pixels_B),
        'c_premul': make_image(pixels_C)}

for name, img in imgs.items():
    img.save(f'{name}.png')

# --- Audit ---
lines = []
for name, img in imgs.items():
    path = f'{name}.png'
    size = os.path.getsize(path)
    lines.append(f'{name}: {size} bytes')

# Composite match check: visible pixels must agree across A, B, C
mismatch_ab, mismatch_ac = 0, 0
for y in range(H):
    for x in range(W):
        a = pixels_A[y][x]
        b = pixels_B[y][x]
        c = pixels_C[y][x]
        if a[3] == 255:  # visible pixel
            if a[:3] != b[:3]: mismatch_ab += 1
            if a[:3] != c[:3]: mismatch_ac += 1

lines.append(f'Visible-pixel RGB mismatches A vs B: {mismatch_ab} (expected 0)')
lines.append(f'Visible-pixel RGB mismatches A vs C: {mismatch_ac} (expected 0)')

# Zero-alpha pixel RGB check
zero_same_bc = sum(
    1 for y in range(H) for x in range(W)
    if pixels_A[y][x][3] == 0
    and pixels_B[y][x][:3] == pixels_C[y][x][:3]
)
zero_total = sum(1 for y in range(H) for x in range(W) if pixels_A[y][x][3] == 0)
lines.append(f'Zero-alpha pixels where B==C in RGB: {zero_same_bc}/{zero_total}')
lines.append('Note: B uses slate, C uses black; a non-zero count here would be a bug.')

audit_text = '\n'.join(lines)
with open('audit.txt', 'w') as f:
    f.write(audit_text)
print(audit_text)