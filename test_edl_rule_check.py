"""Tests for edl_rule_check.py.
Verifies baseline (0 violations) vs variant (7 violations).
Source: art_01M6A85SJY0G5TRQ3EM89Q67VW r1.
"""
from edl_rule_check import check_edl

BASELINE = {
    "subtitle_pass_last": True,
    "concat_strategy": "lossless_copy_concat",
    "segments": [
        {
            "cut_start_ms": 1000, "word_start_ms": 1050,
            "cut_end_ms": 4200, "word_end_ms": 4150,
            "audio_fade_ms": 30,
            "subtitles_after_overlays": True,
            "overlays": [{"id": "logo", "frame_0_offset_ms": 0}],
        },
        {
            "cut_start_ms": 5000, "word_start_ms": 5100,
            "cut_end_ms": 8000, "word_end_ms": 7900,
            "audio_fade_ms": 50,
            "subtitles_after_overlays": True,
            "overlays": [],
        },
    ],
}

VARIANT = {
    "subtitle_pass_last": False,
    "concat_strategy": "single_filtergraph",
    "segments": [
        {
            "cut_start_ms": 1000, "word_start_ms": 1010,
            "cut_end_ms": 4200, "word_end_ms": 4190,
            "audio_fade_ms": 10,
            "subtitles_after_overlays": False,
            "overlays": [{"id": "title_card", "frame_0_offset_ms": 250}],
        },
    ],
}


def test_baseline_clean():
    assert check_edl(BASELINE) == [], "Baseline should have no violations"


def test_variant_catches_all():
    v = check_edl(VARIANT)
    assert len(v) == 7, f"Expected 7 violations, got {len(v)}: {v}"


if __name__ == "__main__":
    test_baseline_clean()
    test_variant_catches_all()
    print("All tests passed.")