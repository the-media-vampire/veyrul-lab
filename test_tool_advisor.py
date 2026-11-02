"""Smoke tests — all expected values from art_01M6EV5HYREYVCK02NZD5B3S9E r1."""
from tool_advisor import advise

def test_texture_web_js():
    r = advise("texture", "web", "javascript")
    tops = {c["tool"] for c in r if c["score"] == r[0]["score"]}
    assert "KTX-Software" in tops and "basis_universal" in tops

def test_mesh_android_cpp():
    r = advise("mesh", "android", "cpp")
    assert r[0]["tool"] in ("draco", "xatlas")
    draco = next(c for c in r if c["tool"]=="draco")
    assert "DRACO_TRANSCODER_SUPPORTED" in draco["caveat"]

def test_hdr_linux_python():
    r = advise("hdr-texture", "linux", "python")
    assert r[0]["tool"] == "basis_universal"
    assert "early" in r[0]["caveat"]

def test_uv_atlas_windows_cpp():
    r = advise("uv-atlas", "windows", "cpp")
    assert r[0]["tool"] == "xatlas"
    assert "Debug" in r[0]["caveat"]

def test_no_match():
    assert advise("audio", "embedded", "rust") == []

def test_determinism():
    assert ([c["tool"] for c in advise("mesh","ios","cpp")] ==
            [c["tool"] for c in advise("mesh","ios","cpp")])

if __name__ == "__main__":
    import sys
    failed = 0
    for fn in [v for k,v in sorted(globals().items()) if k.startswith("test_")]:
        try: fn(); print(f"PASS {fn.__name__}")
        except AssertionError as e: print(f"FAIL {fn.__name__}: {e}"); failed += 1
    sys.exit(failed)