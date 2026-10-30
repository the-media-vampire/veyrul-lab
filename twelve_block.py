"""twelve_block.py – adapter schema for the twelve-block prompt contract.
Source: art_01M67CGQR5M8AXXN18VH6Z4ETM r1 (Veyrul)
License: MIT
"""
from dataclasses import dataclass
from typing import List, Optional
import json

@dataclass
class Reference:
    tag: str            # @-tag exactly as written in the prompt
    role: str           # narrative label used in beats and continuity

@dataclass
class ContinuityEntry:
    role: str           # must match a Reference.role
    condition: str      # one declarative sentence
    repeated_in_scene: bool  # True = also present in scene_context

@dataclass
class Beat:
    name: str
    time_seconds: float
    actions: dict       # role -> action string

@dataclass
class CameraSegment:
    start_seconds: float
    end_seconds: Optional[float]  # None = end of clip
    mode: str
    completion_requirement: Optional[str]

@dataclass
class TwelveBlockPrompt:
    scene_context: str           # block 1
    references: List[Reference]  # block 2
    continuity: List[ContinuityEntry]  # block 3
    camera: List[CameraSegment]  # block 4
    beats: List[Beat]            # block 5
    dialogue: List[str]          # block 6
    acting: str                  # block 7
    physics: str                 # block 8
    lighting: str                # block 9
    audio: str                   # block 10
    style: str                   # block 11
    quality: List[str]           # block 12 – positive conditions only


def validate(p: TwelveBlockPrompt) -> List[str]:
    """Return a list of validation error strings (empty = pass)."""
    errors = []
    known_roles = {r.role for r in p.references}
    for entry in p.continuity:
        if entry.role not in known_roles:
            errors.append(f"Continuity role '{entry.role}' not in references")
        if not entry.repeated_in_scene:
            errors.append(
                f"Continuity condition for '{entry.role}' not marked repeated in scene_context"
            )
    starts = [s.start_seconds for s in p.camera]
    if starts != sorted(starts):
        errors.append("Camera segments are out of order")
    neg_words = ["no ", "never ", "without ", "avoid "]
    for q in p.quality:
        if any(q.lower().startswith(w) for w in neg_words):
            errors.append(f"Quality entry may be negative-framed: '{q[:60]}'")
    return errors


def to_contract(p: TwelveBlockPrompt) -> dict:
    """Emit a JSON-serialisable integration contract."""
    errors = validate(p)
    return {
        "schema": "twelve-block/v1",
        "validation_errors": errors,
        "block_count": 12,
        "continuity_entries": [
            {"role": e.role, "condition": e.condition,
             "repeated_in_scene": e.repeated_in_scene}
            for e in p.continuity
        ],
        "beats": [
            {"name": b.name, "time_seconds": b.time_seconds,
             "actions": b.actions}
            for b in p.beats
        ],
        "camera_segments": [
            {"mode": s.mode, "start": s.start_seconds,
             "end": s.end_seconds,
             "completion_requirement": s.completion_requirement}
            for s in p.camera
        ],
        "quality_rules": p.quality,
    }