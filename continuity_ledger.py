"""Minimal continuity-ledger schema for script-to-video pipelines.

Fields are restricted to those present in >=2 systems documented in
art_01M6GYH6CDY29052076JYF2DMV revision 1 (Veyrul):
  - character identity/state  (FilmAgent, Jellyfish, ledger)
  - location/scene            (FilmAgent, Jellyfish, VideoClaw)
  - style descriptor          (Jellyfish, MultiShotMaster, ledger)
  - previous-shot summary     (Jellyfish, StoryEval)
  - shot status               (Jellyfish, VideoClaw)

License: MIT
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List
import json, re

VALID_STATUSES = {"pending", "ready", "confirmed"}


@dataclass
class CharacterState:
    name: str
    position: Optional[str] = None      # e.g. "left", "center", "right"
    costume_note: Optional[str] = None  # carry-forward costume detail


@dataclass
class ShotRecord:
    shot_id: str                         # S<digits>, e.g. S01
    location: str                        # fixed-list or free text
    style: str                           # global style descriptor
    status: str                          # pending | ready | confirmed
    characters: List[CharacterState] = field(default_factory=list)
    prev_shot_summary: Optional[str] = None   # Jellyfish / StoryEval field
    continuity_note: Optional[str] = None     # Jellyfish continuity advice


def validate(r: ShotRecord) -> List[str]:
    """Return a list of error strings; empty list means the record is valid."""
    errors = []
    if not re.match(r"^S\d{2,}$", r.shot_id):
        errors.append(f"shot_id '{r.shot_id}' must match S<digits>, e.g. S01")
    if r.status not in VALID_STATUSES:
        errors.append(f"status '{r.status}' not in {VALID_STATUSES}")
    if not r.location.strip():
        errors.append("location must not be blank")
    if not r.style.strip():
        errors.append("style must not be blank")
    return errors


def to_json(r: ShotRecord) -> str:
    return json.dumps(asdict(r), indent=2)