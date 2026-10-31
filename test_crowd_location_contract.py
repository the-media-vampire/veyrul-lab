from crowd_location_contract import (
    CrowdLocationContract, PromptSpec, EntityTag, CrowdRule,
    LightState, ShotBlock
)

c = CrowdLocationContract()

def test_conforming():
    r = c.validate(PromptSpec(
        entities=[EntityTag('@ControlRoom', 'brutalist concrete'),
                  EntityTag('@LectureHall', 'reference, benches', look_only=True),
                  EntityTag('@Operators', 'two men')],
        crowd_rules=[CrowdRule('@Operators', '@ControlRoom', ['@LectureHall'])],
        light_state=LightState(['emergency strip only'], ['NO screens', 'POWER OUT']),
        shots=[ShotBlock('Shot1', 0, 1, 'strip', 'desk',
                         'shoulders-up, faces fill 60% frame height', True),
               ShotBlock('Shot3', 2.5, 7, 'warm', 'bench',
                         '30 degrees off bench centre-line', True)],
    ))
    assert r.valid, r.errors

def test_studied_prompt_gaps():
    """Approximates authoring gaps correlated with mismatches 1-3 in art r1."""
    r = c.validate(PromptSpec(
        entities=[EntityTag('@ControlRoom', 'brutalist'),
                  EntityTag('@LectureHall', 'reference, benches', look_only=False),
                  EntityTag('@Operators', 'two men')],
        crowd_rules=[CrowdRule('@Operators', '@ControlRoom', ['@LectureHall'])],
        light_state=LightState([], ['POWER IS ALREADY OUT', 'NO screens lit']),
        shots=[ShotBlock('Shot1', 0, 1, 'power-out', 'desk',
                         'a CLOSE-UP two-shot of their faces', False),
               ShotBlock('Shot2', 1, 2.5, 'warm', 'bench', '3/4 angle', False),
               ShotBlock('Shot3', 2.5, 7, 'warm', 'bench', 'lower-rows angle', False)],
    ))
    assert not r.valid
    assert any('allowed_sources' in err for err in r.errors)
    assert any('word-only' in w for w in r.warnings)

def test_missing_deny():
    r = c.validate(PromptSpec(
        entities=[EntityTag('@Room', 'dark'), EntityTag('@C', 'ops')],
        crowd_rules=[CrowdRule('@C', '@Room', [])],
        light_state=LightState(['strip'], ['NO screens']),
        shots=[ShotBlock('S1', 0, 3, 'strip', 'desk', 'medium', True)],
    ))
    assert not r.valid
    assert any('deny_in' in err for err in r.errors)