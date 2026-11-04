"""Book-trailer pipeline inter-stage data contract.
Documentary -- reflects art_01M6H5ADPZ1P46TM3CRGGYVTJK rev 2.
Not executed. Three OPEN_GAP markers name undocumented boundaries.
  GAP-A: last-frame export format/resolution (Stage 2->3)
  GAP-B: music licence for other providers / generated audio (Stage 7)
  GAP-C: measurable threshold for 'realistic' disclosure trigger (Stage 9)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional

@dataclass
class CharacterEntry:
    name: str
    role_slot: str
    appearance_wording: str

@dataclass
class LocationEntry:
    name: str
    location_slot: str
    appearance_wording: str

@dataclass
class ContinuityLedger:
    """Stage 1 output; must survive unchanged into Stages 2-5."""
    characters: list[CharacterEntry]
    locations: list[LocationEntry]

@dataclass
class CameraMove:
    style: Literal["comparative", "numeric"]
    description: str

@dataclass
class ShotEntry:
    shot_id: str
    character_names: list[str]
    location_name: str
    plot_summary: str
    camera_move: CameraMove
    last_frame_export: Optional[str] = None  # OPEN_GAP-A
    first_frame_check_passed: bool = False
    invented_event_check_passed: bool = False

@dataclass
class MusicLicenceDecision:
    provider: str
    tier: str
    commercial_use_permitted: Optional[bool] = None   # OPEN_GAP-B
    generated_audio_rights_known: bool = False         # OPEN_GAP-B
    human_approved: bool = False

@dataclass
class PublishingDecision:
    platform: Literal["youtube", "tiktok", "meta", "other"]
    disclosure_required: Optional[bool] = None  # OPEN_GAP-C
    label_placement: Optional[str] = None
    premiere_eligible: Optional[bool] = None
    human_approved: bool = False

@dataclass
class TrailerPipelineState:
    project_id: str
    ledger: ContinuityLedger
    shots: list[ShotEntry] = field(default_factory=list)
    music: Optional[MusicLicenceDecision] = None
    publishing: list[PublishingDecision] = field(default_factory=list)

    def validate_names(self) -> list[str]:
        known_chars = {c.name for c in self.ledger.characters}
        known_locs  = {l.name for l in self.ledger.locations}
        errors: list[str] = []
        for s in self.shots:
            for n in s.character_names:
                if n not in known_chars:
                    errors.append(f"{s.shot_id}: unknown character '{n}'")
            if s.location_name not in known_locs:
                errors.append(f"{s.shot_id}: unknown location '{s.location_name}'")
        return errors

    def open_gaps(self) -> list[str]:
        gaps: list[str] = []
        for s in self.shots:
            if s.last_frame_export is None:
                gaps.append(f"GAP-A: {s.shot_id} last_frame_export undecided")
        if self.music and not self.music.human_approved:
            gaps.append("GAP-B: music licence not human-approved")
        for p in self.publishing:
            if p.disclosure_required is None:
                gaps.append(f"GAP-C: disclosure trigger undecided ({p.platform})")
        return gaps