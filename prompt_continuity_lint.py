"""prompt_continuity_lint.py

Four-rule structural linter for video-generation prompts.
Contracts derived from art_01M68DNWCQ5SYGVT7KQXH69M0Y rev 1.

Status values: PASS | WARN | FAIL | UNKNOWN
All checks are text-structural; no model is called.

MIT License. See artifact attribution.
"""
import re


def lint(prompt: str) -> list[tuple[str, str, str]]:
    """Return [(rule_id, status, detail), ...] for the supplied prompt text."""
    lines = prompt.splitlines()
    out: list[tuple[str, str, str]] = []

    # --- R1: unique @-tags per character ---
    tags = sorted(set(re.findall(r'@[\w\-]+', prompt)))
    out.append((
        "R1_unique_tags",
        "PASS" if tags else "UNKNOWN",
        f"tags found: {tags or 'none'}"
    ))

    # --- R2: binding/cast block before first shot label ---
    bp = re.compile(r'\b(cast|binding|characters?)\b', re.I)
    sp = re.compile(r'\b(shot\s*\d+|scene\s*\d+)\b', re.I)
    b = next((i for i, l in enumerate(lines) if bp.search(l)), None)
    s = next((i for i, l in enumerate(lines) if sp.search(l)), None)
    if b is None:
        out.append(("R2_binding_before_shots", "WARN", "no CAST/BINDING section found"))
    elif s is not None and b > s:
        out.append(("R2_binding_before_shots", "FAIL",
                    f"binding at line {b+1} appears after first shot at line {s+1}"))
    else:
        out.append(("R2_binding_before_shots", "PASS",
                    f"binding@line {b+1}, first shot@line {s+1 if s else 'none'}"))

    # --- R3: location allow/exclude clauses ---
    excl = bool(re.search(
        r'\b(no|not|exclude|absent)\b.{0,40}\b(location|room|crowd|area)\b', prompt, re.I))
    incl = bool(re.search(
        r'\b(only|allowed?|present)\b.{0,40}\b(location|room|crowd|area)\b', prompt, re.I))
    out.append((
        "R3_location_lists",
        "PASS" if excl or incl else "WARN",
        f"allow={incl} exclude={excl}"
    ))

    # --- R4: position word in every shot block ---
    pos = re.compile(
        r'\b(left|right|center|centre|foreground|background|facing|behind|'
        r'frame.left|frame.right|close.up|wide|medium.shot|two.shot)\b', re.I)
    idxs = [i for i, l in enumerate(lines) if sp.search(l)]
    if not idxs:
        out.append(("R4_positions_after_cuts", "UNKNOWN", "no shot labels found"))
    else:
        missing = []
        for k, i in enumerate(idxs):
            end = idxs[k + 1] if k + 1 < len(idxs) else len(lines)
            if not pos.search("\n".join(lines[i:end])):
                missing.append(i + 1)
        out.append((
            "R4_positions_after_cuts",
            "WARN" if missing else "PASS",
            f"shot blocks missing a position word (start lines): {missing or 'none'}"
        ))

    return out


if __name__ == "__main__":
    DEMO = """\
CAST BINDING
@maya = detective, grey coat
@leo  = suspect, navy hoodie

Shot 1: Wide. @maya frame-left at door. @leo sits center background.
Shot 2: Close-up. @maya faces camera left profile.
Shot 3: Two-shot. @maya and @leo only; no crowd allowed in this room.
"""
    for rule, status, detail in lint(DEMO):
        print(f"[{status:7}] {rule}: {detail}")