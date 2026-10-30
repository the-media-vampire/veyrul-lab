"""RightsAttestation: dated operator record replacing bare boolean.

Addresses gap from Clio audit artifact 1a47e024, commit 97418508:
  'a boolean is indistinguishable from a toggled flag'.
Additive: ClipEntry.rights_confirmed stays as gate bool.
Source: art_01M64VKXMVEZ9Y84F54KMW6ZF7 r2.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class RightsAttestation:
    clip_id: str
    confirmed: bool
    confirmed_at: Optional[str] = None   # ISO-8601
    operator_id: Optional[str] = None
    basis: Optional[str] = None
    likeness_scope: Optional[str] = None
    audio_scope: Optional[str] = None

    def is_legible(self) -> bool:
        if not self.confirmed:
            return True
        return all([self.confirmed_at, self.operator_id, self.basis])

court_lawn_attestations = [
    RightsAttestation(
        clip_id="exp_01M64VHHFXDAZTSDB4C8NWSTJV",
        confirmed=False, likeness_scope="cast unconfirmed",
        audio_scope="not reviewed; spoken lines requested",
    ),
    RightsAttestation(
        clip_id="exp_01M64VH7Z81MJ2V7DD44D0HYWA",
        confirmed=False, likeness_scope="cast unconfirmed",
        audio_scope="not reviewed",
    ),
    RightsAttestation(
        clip_id="exp_01M64VHDN2EWMQFSGSVWDS6S2X",
        confirmed=False, likeness_scope="cast unconfirmed",
        audio_scope="not reviewed",
    ),
]

def attestation_gate(clip_id: str, attestations: list) -> dict:
    for a in attestations:
        if a.clip_id == clip_id:
            return {"clip_id": clip_id, "confirmed": a.confirmed,
                    "legible": a.is_legible(), "blocked": not a.confirmed,
                    "missing_attestation": False}
    return {"clip_id": clip_id, "confirmed": False, "legible": False,
            "blocked": True, "missing_attestation": True}