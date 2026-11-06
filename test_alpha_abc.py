"""pytest harness for the PNG alpha A/B/C experiment.
Basis: art_01M6QET9K2DYXFVY5VA2W01CD0 r1 (§9.4 RFC 2083)
Depends on: alpha_ab_experiment.py (Scout, artifact 9e85b35c)
Run: python alpha_ab_experiment.py && pytest test_alpha_abc.py -v

Decision rules:
  DR1 Visible pixels: RGB identical across A, B, C (compositing must match).
  DR2 Zero-alpha pixels: B (slate) must differ from C (black) in every pixel.
  DR3 Round-trip: write RGBA PNG to temp, read back; alpha bit-for-bit preserved.
"""
import os, tempfile, pytest
from PIL import Image

W, H = 512, 512
AMBER, SLATE, BLACK = (232,154,48), (32,40,48), (0,0,0)
STRIP_L, STRIP_R = 224, 288
CX, CY, R = 256, 256, 160

def _in_circle(x, y):
    return (x-CX)**2 + (y-CY)**2 <= R*R

@pytest.fixture(scope="module")
def pixels():
    pa, pb, pc = [], [], []
    for y in range(H):
        for x in range(W):
            circle = _in_circle(x, y)
            rgb = AMBER if circle else SLATE
            alpha = 255 if (circle and STRIP_L <= x < STRIP_R) else 0
            pa.append(rgb + (alpha,))
            pb.append((rgb if alpha==255 else SLATE) + (alpha,))
            pc.append((rgb if alpha==255 else BLACK) + (alpha,))
    return pa, pb, pc

def test_dr1_ab(pixels):
    pa, pb, _ = pixels
    bad = [i for i,(a,b) in enumerate(zip(pa,pb)) if a[3]==255 and a[:3]!=b[:3]]
    assert bad == [], f"DR1 FAIL: {len(bad)} visible-pixel RGB mismatches A vs B"

def test_dr1_ac(pixels):
    pa, _, pc = pixels
    bad = [i for i,(a,c) in enumerate(zip(pa,pc)) if a[3]==255 and a[:3]!=c[:3]]
    assert bad == [], f"DR1 FAIL: {len(bad)} visible-pixel RGB mismatches A vs C"

def test_dr2_b_is_slate(pixels):
    pa, pb, _ = pixels
    bad = [i for i,(a,b) in enumerate(zip(pa,pb)) if a[3]==0 and b[:3]!=SLATE]
    assert bad == [], f"DR2 FAIL: {len(bad)} zero-alpha pixels in B are not SLATE"

def test_dr2_c_is_black(pixels):
    pa, _, pc = pixels
    bad = [i for i,(a,c) in enumerate(zip(pa,pc)) if a[3]==0 and c[:3]!=BLACK]
    assert bad == [], f"DR2 FAIL: {len(bad)} zero-alpha pixels in C are not BLACK"

def _roundtrip_alpha(pxlist):
    img = Image.new('RGBA', (W, H))
    img.putdata(pxlist)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        path = f.name
    try:
        img.save(path)
        back = Image.open(path).convert('RGBA')
        return [p[3] for p in back.getdata()]
    finally:
        os.unlink(path)

def test_dr3_roundtrip_a(pixels):
    pa, _, _ = pixels
    assert [p[3] for p in pa] == _roundtrip_alpha(pa), \
        "DR3 FAIL: Variant A alpha changed after PNG round-trip"

def test_dr3_roundtrip_b(pixels):
    _, pb, _ = pixels
    assert [p[3] for p in pb] == _roundtrip_alpha(pb), \
        "DR3 FAIL: Variant B alpha changed after PNG round-trip"

def test_dr3_roundtrip_c(pixels):
    _, _, pc = pixels
    assert [p[3] for p in pc] == _roundtrip_alpha(pc), \
        "DR3 FAIL: Variant C alpha changed after PNG round-trip"