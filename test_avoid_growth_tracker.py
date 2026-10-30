# test_avoid_growth_tracker.py  MIT License
# Documented values from art_01M67ACYEDW3GH3RZKZRKQF0RN r1

from avoid_growth_tracker import track_avoid_growth
import pytest

DOCUMENTED = [
    ("take_1",    8),
    ("final_cut", 15),
    ("take_2",    16),
    ("take_3",    18),
]

def test_documented_takes_are_monotone():
    r = track_avoid_growth(DOCUMENTED)
    assert r["weakly_monotone"] is True
    assert r["strictly_increasing"] is True
    assert r["regressions"] == []

def test_regression_detected():
    seq = [("t1", 8), ("t2", 15), ("t3", 12)]  # synthetic: count drops
    r = track_avoid_growth(seq)
    assert r["weakly_monotone"] is False
    assert len(r["regressions"]) == 1
    assert r["regressions"][0][2] == -3

def test_flat_step_is_weak_monotone_not_strict():
    seq = [("t1", 8), ("t2", 8), ("t3", 10)]
    r = track_avoid_growth(seq)
    assert r["weakly_monotone"] is True
    assert r["strictly_increasing"] is False

def test_negative_count_raises():
    with pytest.raises(ValueError):
        track_avoid_growth([("t1", 8), ("t2", -1)])

def test_single_take_raises():
    with pytest.raises(ValueError):
        track_avoid_growth([("t1", 8)])