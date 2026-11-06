"""Baseline and violation tests. Run: python test_cross_shot.py"""
from cross_shot_check import ShotRecord, cross_shot_check

def test_baseline():
    shots = [ShotRecord('S01','Mira','library','dark blue coat, hair up'),
             ShotRecord('S02','Mira','library','dark blue coat, hair up')]
    r = cross_shot_check(shots)
    assert r == []
    print(f"PASS baseline: {len(r)} mismatches (expected 0)")

def test_costume_conflict():
    shots = [ShotRecord('S01','Mira','library','dark blue coat'),
             ShotRecord('S02','Mira','library','red scarf')]
    r = cross_shot_check(shots)
    assert len(r) == 1 and r[0].field == 'costume_note'
    print(f"PASS costume: caught '{r[0]}'")

def test_location_conflict():
    shots = [ShotRecord('S01','Mira','library','dark blue coat'),
             ShotRecord('S02','Mira','rooftop','dark blue coat')]
    r = cross_shot_check(shots)
    assert len(r) == 1 and r[0].field == 'location'
    print(f"PASS location: caught '{r[0]}'")

def test_scene_break_suppresses():
    shots = [ShotRecord('S01','Mira','library','dark blue coat'),
             ShotRecord('S02','Mira','rooftop','red scarf',scene_break=True)]
    r = cross_shot_check(shots)
    assert r == []
    print(f"PASS scene_break: suppressed, {len(r)} mismatches")

def test_different_characters_ignored():
    shots = [ShotRecord('S01','Mira','library','dark blue coat'),
             ShotRecord('S02','Luca','library','grey jacket')]
    r = cross_shot_check(shots)
    assert r == []
    print(f"PASS diff chars: {len(r)} mismatches")

if __name__ == '__main__':
    test_baseline()
    test_costume_conflict()
    test_location_conflict()
    test_scene_break_suppresses()
    test_different_characters_ignored()
    print("\nAll tests passed.")