"""Jaccard token-overlap cross-shot costume-note drift checker.

Survey motivation: art_01M6HRDNCF7PCNDKZNAN1K6R1X r3 open problem:
  'inconsistent temporal coherence: frame-to-frame continuity breaks down
   in longer sequences'.

Improvement over exact-string baseline: Jaccard(word_set_A, word_set_B)
>= threshold (default 0.5) means notes are considered consistent, so
paraphrases of the same costume do not trigger false-positive flags.
"""
from __future__ import annotations
from typing import NamedTuple


def _tokens(text: str) -> set[str]:
    return {w.strip('.,;:\'"').lower() for w in text.split() if w.strip('.,;:\'"')}


def jaccard(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


class Shot(NamedTuple):
    shot_id: str
    character: str
    costume_note: str
    scene_break: bool = False


class DriftResult(NamedTuple):
    shot_a: str
    shot_b: str
    character: str
    similarity: float
    flagged: bool
    reason: str


def cross_shot_check(shots: list[Shot], threshold: float = 0.5) -> list[DriftResult]:
    """Flag consecutive same-character shots whose costume_note Jaccard < threshold."""
    results: list[DriftResult] = []
    for i in range(len(shots) - 1):
        a, b = shots[i], shots[i + 1]
        if a.character != b.character:
            continue
        sim = round(jaccard(a.costume_note, b.costume_note), 3)
        if b.scene_break:
            results.append(DriftResult(a.shot_id, b.shot_id, a.character, sim, False, 'scene_break suppressed'))
            continue
        flagged = sim < threshold
        results.append(DriftResult(a.shot_id, b.shot_id, a.character, sim, flagged,
                                   'costume drift' if flagged else 'consistent'))
    return results