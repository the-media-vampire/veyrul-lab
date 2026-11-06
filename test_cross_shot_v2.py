"""Baseline vs. Jaccard comparison on four documented test cases.

Run: python test_cross_shot_v2.py
Expected output: All 4 cases passed.

Baseline / improved summary:
  Case | Scenario                        | exact-string flags | Jaccard flags
  1    | identical notes                 | 0                  | 0
  2    | paraphrase (word-order change)  | 1 (false positive) | 0
  3    | genuine costume change          | 1 (correct)        | 1 (correct)
  4    | scene_break suppresses flag     | 0                  | 0
"""
from cross_shot_v2 import Shot, cross_shot_check, jaccard

THRESHOLD = 0.5

def test_case_1_identical():
    shots = [Shot('S01','Maya','red wool coat gold belt'), Shot('S02','Maya','red wool coat gold belt')]
    r = cross_shot_check(shots, THRESHOLD)
    assert not r[0].flagged and r[0].similarity == 1.0

def test_case_2_paraphrase():
    sim = jaccard('red wool coat gold belt', 'gold belt red wool coat')
    assert sim == 1.0, f'Expected 1.0 got {sim}'
    shots = [Shot('S01','Maya','red wool coat gold belt'), Shot('S02','Maya','gold belt red wool coat')]
    r = cross_shot_check(shots, THRESHOLD)
    assert not r[0].flagged, f'False positive: {r[0]}'

def test_case_3_genuine_change():
    shots = [Shot('S01','Maya','red wool coat gold belt'), Shot('S02','Maya','blue leather jacket')]
    r = cross_shot_check(shots, THRESHOLD)
    assert r[0].flagged and r[0].similarity < THRESHOLD

def test_case_4_scene_break():
    shots = [Shot('S01','Maya','red wool coat gold belt'), Shot('S02','Maya','blue leather jacket', scene_break=True)]
    r = cross_shot_check(shots, THRESHOLD)
    assert not r[0].flagged and r[0].reason == 'scene_break suppressed'

if __name__ == '__main__':
    test_case_1_identical()
    test_case_2_paraphrase()
    test_case_3_genuine_change()
    test_case_4_scene_break()
    print('All 4 cases passed.')
    print('Case 2: paraphrase Jaccard=1.0 — exact-string would have flagged; Jaccard does not.')