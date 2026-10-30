"""Coverage Cut-Manifest schema and validation stub.

Mechanism: a Seedance multi-run session produces N clips covering one spatial
envelope. This manifest captures the *assembly contract* — which clips can be
cut together, what rights and audio-review gates must clear, and what spatial
continuity assertion the editor is relying on.

Not a render or execution record. No clip bytes are embedded.
Source: art_01M64VKXMVEZ9Y84F54KMW6ZF7 r2.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ClipEntry:
    """One run in the session."""
    clip_id: str                   # experiment record ID or candidate URL
    duration_s: float              # observed duration in seconds
    camera_path: str               # human description of camera movement
    key_action: str                # dominant action in sampled frames
    seed_set: bool                 # was a seed value recorded?
    rights_confirmed: bool         # inputs confirmed in disclosure and rights?
    audio_reviewed: bool           # was audio actually listened to?
    holds_likeness: bool           # linked inputs hold recognisable likeness?


@dataclass
class SpatialContinuityAssertion:
    """The editorial claim that makes the cuts possible."""
    basis: str          # e.g. "sampled-frame inspection by H01"
    scope: str          # what is continuous ("court and lawn as one place")
    generalises: bool   # does the team assert this beyond these three runs?
    evidence_record: str  # record ID that documents the basis


@dataclass
class CutManifest:
    session_id: str
    source_article: str            # record ID + revision
    clips: list[ClipEntry]
    spatial_continuity: SpatialContinuityAssertion
    assembly_note: str

    def validate(self) -> list[str]:
        """Return a list of blocking issues; empty list means assembly is clear."""
        issues: list[str] = []
        for c in self.clips:
            if not c.rights_confirmed:
                issues.append(
                    f"{c.clip_id}: rights unconfirmed — do not distribute assembled cut"
                )
            if c.holds_likeness and not c.rights_confirmed:
                issues.append(
                    f"{c.clip_id}: holds likeness AND rights unconfirmed — hard block"
                )
            if not c.audio_reviewed:
                issues.append(
                    f"{c.clip_id}: audio not reviewed — assembled cut must not include audio"
                )
            if not c.seed_set:
                issues.append(
                    f"{c.clip_id}: no seed — run is unrepeatable; note in edit log"
                )
        if not self.spatial_continuity.generalises:
            issues.append(
                "Spatial continuity is session-specific; do not reuse assertion for other scenes"
            )
        return issues

    def is_assembly_blocked(self) -> bool:
        """Hard block if any likeness + unconfirmed rights issue exists."""
        return any("hard block" in i for i in self.validate())