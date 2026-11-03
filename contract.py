"""MovieAgent shot-plan -> generator adapter contract.
Shapes follow the plan-field table in arXiv 2503.07314v1 (CC BY 4.0).
This is an interface sketch; nothing is executed here.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CharacterEntry:
    name: str
    role_label: str
    portrait_slot: str  # opaque path; images named by role only
    # audio_slot: held - not described per lane policy

    def validate(self) -> List[str]:
        errors = []
        if not self.name: errors.append("CharacterEntry.name empty")
        if not self.portrait_slot: errors.append(f"{self.name}: portrait_slot missing")
        return errors

@dataclass
class ShotEntry:
    shot_id: str
    scene_id: str
    characters: List[str]  # must exist in CharacterEntry set
    plot: str
    camera_movement: str
    shot_type: str
    lighting: str
    subtitle_text: Optional[str] = None  # dialogue as text; audio held
    visual_effects: Optional[str] = None

    def validate(self, known: set) -> List[str]:
        errors = []
        for n in self.characters:
            if n not in known:
                errors.append(f"{self.shot_id}: '{n}' not in bank")
        for f in ("plot","camera_movement","shot_type","lighting"):
            if not getattr(self, f):
                errors.append(f"{self.shot_id}: '{f}' empty")
        return errors

def validate_plan(bank: List[CharacterEntry], shots: List[ShotEntry]) -> List[str]:
    """Return all errors; empty list = safe to pass to generators."""
    errors, known = [], set()
    for e in bank:
        errors.extend(e.validate()); known.add(e.name)
    for s in shots:
        errors.extend(s.validate(known))
    return errors

TMPL = ("{shot_type}, {camera_movement}. "
        "Characters: {characters}. Scene: {plot}. "
        "Lighting: {lighting}.{vfx}")

def shot_to_prompt(shot: ShotEntry) -> str:
    """Serialise to free-text prompt for a downstream generator.
    Assumption: generator accepts plain text. Replace with dict serialiser
    if the generator has a structured API.
    """
    vfx = f" VFX: {shot.visual_effects}." if shot.visual_effects else ""
    return TMPL.format(shot_type=shot.shot_type,
                       camera_movement=shot.camera_movement,
                       characters=", ".join(shot.characters),
                       plot=shot.plot, lighting=shot.lighting, vfx=vfx)