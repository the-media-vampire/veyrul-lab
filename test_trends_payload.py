"""Inline tests – run with: python test_trends_payload.py"""
from trends_payload import build_interest_by_region_payload

def test_valid_call():
    r = build_interest_by_region_payload(
        ["AI video", "text to video", "generative AI"],
        location="US",
        property="youtube",
    )
    assert r["valid"]
    assert r["payload"]["estimated_credits"] == 5

def test_empty_keywords():
    r = build_interest_by_region_payload([], property="web")
    assert not r["valid"]
    assert any("1" in e for e in r["errors"])

def test_over_limit():
    r = build_interest_by_region_payload(["a","b","c","d","e","f"])
    assert not r["valid"]

def test_bad_property():
    r = build_interest_by_region_payload(["AI"], property="tiktok")
    assert not r["valid"]
    assert any("property" in e for e in r["errors"])

def test_max_keywords():
    r = build_interest_by_region_payload(["a","b","c","d","e"], property="news")
    assert r["valid"]

if __name__ == "__main__":
    for fn in [test_valid_call, test_empty_keywords, test_over_limit,
               test_bad_property, test_max_keywords]:
        fn()
        print(f"  PASS  {fn.__name__}")
    print("All tests passed.")