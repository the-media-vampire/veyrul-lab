"""Tests for aframe_validator. All fixtures are static strings; nothing is run or rendered."""
from aframe_validator import baseline_check, structured_check

FIXTURES = [
    ("valid_minimal", 0, 0, """
<html><head><script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script></head>
<body><a-scene><a-box position="-1 0.5 -3"></a-box></a-scene></body></html>
"""),
    ("missing_ascene", 1, 1, """
<html><head><script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script></head>
<body><a-box position="0 0 -3"></a-box></body></html>
"""),
    ("bad_gltf_src", 0, 1, """
<html><head><script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script></head>
<body><a-scene><a-entity gltf-model="mymodel.obj"></a-entity></a-scene></body></html>
"""),
    ("bad_renderer_prop", 0, 1, """
<html><head><script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script></head>
<body><a-scene renderer="shadowEnabled: true; antialias: true"><a-box></a-box></a-scene></body></html>
"""),
    ("asset_item_no_id", 0, 1, """
<html><head><script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script></head>
<body><a-scene><a-assets><a-asset-item src="model.glb"></a-asset-item></a-assets></a-scene></body></html>
"""),
    ("no_aframe_include", 0, 1, """
<html><body><a-scene><a-box></a-box></a-scene></body></html>
"""),
]

def test_all():
    for name, exp_base, exp_struct, html in FIXTURES:
        b = baseline_check(html)
        s = structured_check(html)
        assert len(b) == exp_base, f"{name}: baseline expected {exp_base}, got {len(b)}: {b}"
        assert len(s) == exp_struct, f"{name}: structured expected {exp_struct}, got {len(s)}: {s}"
        print(f"PASS {name}")

if __name__ == "__main__":
    test_all()
    print("All tests passed.")