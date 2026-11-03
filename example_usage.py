"""Minimal planning-time check. Nothing is generated."""
from contract import CharacterEntry, ShotEntry, validate_plan, shot_to_prompt

bank = [
    CharacterEntry("Mira", "protagonist", "assets/mira_ref.png"),
    CharacterEntry("Tobias", "supporting", "assets/tobias_ref.png"),
]
shots = [
    ShotEntry("S01-s01","S01",["Mira"],
              "Mira climbs the lighthouse stairs",
              "tracking shot from below","wide","cool pre-dawn blue"),
    ShotEntry("S01-s02","S01",["Mira","Tobias"],
              "Tobias hands Mira the supply crate",
              "static","medium two-shot","warm lantern glow",
              subtitle_text="Here are the parts."),
]
errors = validate_plan(bank, shots)
if errors:
    for e in errors: print("ERROR:", e)
else:
    print("Plan valid.")
    for s in shots:
        print(f"\n[{s.shot_id}]", shot_to_prompt(s))