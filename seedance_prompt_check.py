"""Seedance 2.5 multi-cast prompt validator.

Rules from art_01M669GA8H3XAFN94DM0MG7QC5 r1. Static text check only;
does not substitute for a render.
"""
import re, json

SHOT_RE = re.compile(r"^SHOT\s+\d+", re.MULTILINE)
STRUCTURAL = {
    "SHOT","MEDIUM","WIDE","CLOSE","UP","TWO","MASTER","DOOR","STAIRCASE",
    "LEFT","RIGHT","NEVER","ALWAYS","ONLY","EACH","AND","THE","FROM",
    "INTO","BEAT","TURN","CROSS","ROOM","SAME","NEAR","STAY","LOOK","WHO",
    "INT","EXT","DAY","NIGHT","LOCK","RULE","CAST","STYLE","LOCATION",
    "LIGHTING","CONTINUITY","MOVEMENT","DIALOGUE","CHARACTER","PERFORMANCE",
}

def parse_cast_line(prompt):
    cast = {}
    for line in prompt.splitlines():
        if "@Image" in line or "@image" in line:
            for m in re.finditer(r"([A-Z][A-Z0-9_]+)\s*=\s*@\w+", line):
                cast[m.group(1)] = m.group(0)
    return cast

def split_shots(prompt):
    pos = [m.start() for m in SHOT_RE.finditer(prompt)]
    return [prompt[pos[i]:pos[i+1] if i+1 < len(pos) else len(prompt)]
            for i in range(len(pos))]

def strip_dialogue(shot):
    """Drop NAME: "..." lines; lock governs action lines only."""
    return "\n".join(l for l in shot.splitlines()
                    if not re.match(r'^[A-Z][A-Z0-9_]+:\s+"', l))

def check_prompt(label, prompt, cast_names,
                named_objects=("DOOR", "STAIRCASE")):
    issues = []
    parsed = parse_cast_line(prompt)
    if not parsed:
        issues.append("FAIL: No cast-binding line (NAME = @ImageN).")
    bound = set(parsed)
    missing = set(cast_names) - bound
    if missing:
        issues.append(f"FAIL: Names not bound: {sorted(missing)}.")
    shots = split_shots(prompt)
    if not shots:
        issues.append("FAIL: No SHOT N blocks found.")
    for i, shot in enumerate(shots, 1):
        action = strip_dialogue(shot)
        for name in bound | set(cast_names):
            n = len(re.findall(rf"\b{re.escape(name)}\b", action))
            if n > 1:
                issues.append(
                    f"FAIL shot {i}: '{name}' {n}x in action "
                    f"(character lock breach).")
        caps = set(re.findall(r"\b([A-Z]{3,})\b", action))
        unbound = caps - STRUCTURAL - bound - set(cast_names)
        if unbound:
            issues.append(
                f"WARN shot {i}: unbound ALL-CAPS {sorted(unbound)} "
                f"— alias/synonym bug?")
    for obj in named_objects:
        if obj.lower() in prompt and obj not in prompt:
            issues.append(f"WARN: '{obj.lower()}' not capitalised.")
    return {"label": label, "bound": sorted(bound),
            "shots": len(shots),
            "issues": issues or ["OK"]}

if __name__ == "__main__":
    GOOD = """
INT. HALL - DAY.
ALICE = @Image1, BOB = @Image2, CAROL = @Image3
CHARACTER LOCK: each name once per shot.
SHOT 1 - MEDIUM
ALICE steps forward and takes BOB's hand.
ALICE: "We meet at last."
SHOT 2 - CLOSE-UP
BOB hesitates.
BOB: "Indeed."
SHOT 3 - WIDE MASTER
CAROL leaves by the DOOR. ALICE stays near the STAIRCASE.
"""
    BAD = """
INT. HALL - DAY.
ALICE = @Image1, BOB = @Image2, CAROL = @Image3
SHOT 1 - MEDIUM
ALICE steps forward. ALICE turns. PRINCE watches from the staircase.
ALICE: "We meet at last."
SHOT 2 - CLOSE-UP
BOB speaks.
"""
    print(json.dumps([
        check_prompt("A: clean", GOOD, {"ALICE","BOB","CAROL"}),
        check_prompt("B: broken", BAD, {"ALICE","BOB","CAROL"}),
    ], indent=2))