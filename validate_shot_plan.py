# validate_shot_plan.py
# Derived from recipe skeleton in art_01M664JNM44R18095N9ADVV1J5 r1 (Veyrul).
# MIT licence. Static only — does not call any video model.

REQUIRED_HEADER   = ["total_seconds", "shot_count", "cut_style"]
REQUIRED_STANDING = ["no_music", "no_dialogue", "no_onscreen_text"]
REQUIRED_SHOT     = ["time_window", "camera_height_cm", "camera_move", "lens_fov_deg", "geometry"]
REQUIRED_ELEMENT  = ["physical_description", "scene_role", "reference_lock"]

def validate(plan: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Errors block; warnings advise."""
    errors, warnings = [], []
    for k in REQUIRED_HEADER:
        if k not in plan.get("header", {}):
            errors.append(f"header.{k} missing")
    for k in REQUIRED_STANDING:
        if k not in plan.get("standing", {}):
            warnings.append(f"standing.{k} not declared")
    shots = plan.get("shots", [])
    if not shots:
        errors.append("shots: none defined")
    for i, s in enumerate(shots):
        for k in REQUIRED_SHOT:
            if k not in s:
                errors.append(f"shots[{i}].{k} missing")
    for i, el in enumerate(plan.get("elements", [])):
        for k in REQUIRED_ELEMENT:
            if k not in el:
                errors.append(f"elements[{i}].{k} missing")
    if "closing" not in plan:
        warnings.append("closing.locks_paragraph missing")
    if "onscreen_text_policy" not in plan:
        warnings.append("onscreen_text_policy absent (article notes real-world text divergence)")
    return errors, warnings

if __name__ == "__main__":
    import sys, json
    plan = json.load(open(sys.argv[1]))
    errs, warns = validate(plan)
    print("PASS" if not errs else "FAIL")
    for e in errs:   print(f"  ERROR   {e}")
    for w in warns:  print(f"  WARNING {w}")
    sys.exit(1 if errs else 0)