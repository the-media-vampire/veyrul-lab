"""Tests for ltx23_i2v_footprint.py
Run: python test_ltx23_i2v_footprint.py
Source: art_01M6BYD28NTGF22DVC33XQ60FH revision 2
"""
from ltx23_i2v_footprint import FILES, footprint_report


def test_file_count():
    assert len(FILES) == 5, "Template declares 5 files"


def test_mandatory_count():
    mandatory = [f for f in FILES if f["mandatory"]]
    assert len(mandatory) == 4, "4 files are mandatory"


def test_optional_count():
    optional = [f for f in FILES if not f["mandatory"]]
    assert len(optional) == 1, "1 file is optional (Gemma LoRA)"


def test_text_encoder_size_unknown():
    te = [f for f in FILES if "gemma" in f["name"] and "lora" not in f["folder"].lower() or
          f["name"] == "gemma_3_12B_it_fp4_mixed.safetensors"]
    assert any(f["size_gb"] is None for f in FILES if "text_encoders" in f["folder"]), \
        "Text encoder size must be None (not stated)"


def test_partial_sum():
    r = footprint_report()
    # Record states 31.2387 GB for the four files with known sizes
    assert abs(r["partial_sum_4_files_gb"] - 31.2387) < 0.001, \
        f"Partial sum mismatch: {r['partial_sum_4_files_gb']}"


def test_mandatory_known_vs_optional():
    r = footprint_report()
    # Mandatory known: 27.14 + 2.55 + 0.9496 = 30.6396
    assert abs(r["mandatory_known_gb"] - 30.6396) < 0.001
    # Optional: 0.5991 GB
    assert abs(r["optional_skippable_gb"] - 0.5991) < 0.001


if __name__ == "__main__":
    tests = [test_file_count, test_mandatory_count, test_optional_count,
             test_text_encoder_size_unknown, test_partial_sum, test_mandatory_known_vs_optional]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")