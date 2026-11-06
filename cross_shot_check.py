"""Cross-shot continuity checker for AI book-trailer shot sequences.

Extends prior artifact acda5f8b (Minimal Continuity-Ledger Schema).
Source basis: art_01M6A19D9WCBJFN6YNNXNTP570 r2, art_01M6GYH6CDY29052076JYF2DMV r1.

Limits:
- costume_note compared by exact string; paraphrases false-positive.
- Prop details inside free-text notes are not parsed.
- scene_break must be set by the author; not inferred.
- Checks authored ledger data only; no engine queried.
"""
from dataclasses import dataclass
from typing import List

@dataclass
class ShotRecord:
    shot_id: str
    character: str
    location: str
    costume_note: str
    scene_break: bool = False
    continuity_note: str = ''
    status: str = 'draft'

@dataclass
class Mismatch:
    shot_a: str
    shot_b: str
    field: str
    value_a: str
    value_b: str
    def __str__(self):
        return f"{self.shot_a}->{self.shot_b} [{self.field}] '{self.value_a}' != '{self.value_b}'"

def cross_shot_check(shots: List[ShotRecord]) -> List[Mismatch]:
    """Return mismatches between consecutive shots for the same character.

    Flags costume_note or location changes when scene_break is False.
    """
    out: List[Mismatch] = []
    for i in range(len(shots) - 1):
        a, b = shots[i], shots[i+1]
        if a.character != b.character or b.scene_break:
            continue
        for f in ('costume_note', 'location'):
            va, vb = getattr(a, f), getattr(b, f)
            if va != vb:
                out.append(Mismatch(a.shot_id, b.shot_id, f, va, vb))
    return out