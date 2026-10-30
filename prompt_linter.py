"""Prose prompt linter — section checker and Negative-item counter.

Source: art_01M67ACYEDW3GH3RZKZRKQF0RN r1 (recipe skeleton).
License: MIT.
"""
import re
from typing import List, Tuple

SECTION_PATTERNS = {
    "sound_rule":  re.compile(r"\b(no music|diegetic|ambient sound|sound of)\b", re.I),
    "camera_law":  re.compile(r"\b(does not zoom|does not follow|does not pan|camera (stays?|is locked|is fixed))\b", re.I),
    "weather_law": re.compile(r"\b(rain|snow|dust|smoke).{0,60}(fall|land|settle|streak|ring)\b", re.I | re.S),
    "timed_beats": re.compile(r"\b\d+(\.\d+)?\s*(second|sec|\bs\b)", re.I),
    "continuity":  re.compile(r"\b(stays? (in place|where|crooked)|never (see|seen|change)|keep their shape)\b", re.I),
    "avoid_list":  re.compile(r"\bAvoid\b.{0,400}?,", re.I | re.S),
}


def count_negative_items(prompt: str) -> int:
    """Count comma-separated items in the first Avoid clause."""
    m = re.search(r"\bAvoid[:\s]+(.+?)(?:\.\s*$|$)", prompt, re.I | re.S)
    if not m:
        return 0
    return len([i for i in m.group(1).split(",") if i.strip()])


def lint(prompt: str) -> Tuple[List[str], List[str], int]:
    """Return (found_sections, missing_sections, negative_item_count)."""
    found = [s for s, p in SECTION_PATTERNS.items() if p.search(prompt)]
    missing = [s for s in SECTION_PATTERNS if s not in found]
    return found, missing, count_negative_items(prompt)


if __name__ == "__main__":
    import sys
    text = sys.stdin.read()
    found, missing, neg = lint(text)
    print(f"Sections found : {found}")
    print(f"Sections missing: {missing}")
    print(f"Negative items : {neg}")
    if missing:
        print("INCOMPLETE")
    else:
        print("OK")