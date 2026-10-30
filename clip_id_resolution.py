"""ClipIdResolution: candidate vs stable ID distinction.

Addresses gap named in rpl_01M66191Q4C7JGH44FG7PZZXDF r1:
  clip_id fields use candidate URLs, not stable resolved IDs.
Source: art_01M64VKXMVEZ9Y84F54KMW6ZF7 r2.
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class IdStatus(str, Enum):
    CANDIDATE = "candidate"      # from source citation; unconfirmed
    RESOLVED = "resolved"        # confirmed by read_record
    UNRESOLVABLE = "unresolvable"

@dataclass
class ClipIdResolution:
    clip_id: str
    status: IdStatus
    resolved_id: Optional[str] = None
    resolved_at: Optional[str] = None   # ISO-8601
    resolver_agent: Optional[str] = None
    resolution_note: str = ""

    def is_stable(self) -> bool:
        return self.status == IdStatus.RESOLVED and self.resolved_id is not None

court_lawn_resolutions = [
    ClipIdResolution(
        clip_id="exp_01M64VHHFXDAZTSDB4C8NWSTJV",
        status=IdStatus.CANDIDATE,
        resolution_note="Source: 'candidate; Main resolves to a record ID'",
    ),
    ClipIdResolution(
        clip_id="exp_01M64VH7Z81MJ2V7DD44D0HYWA",
        status=IdStatus.CANDIDATE,
        resolution_note="Source: 'candidate; Main resolves to a record ID'",
    ),
    ClipIdResolution(
        clip_id="exp_01M64VHDN2EWMQFSGSVWDS6S2X",
        status=IdStatus.CANDIDATE,
        resolution_note="Source: 'candidate; Main resolves to a record ID'",
    ),
]

def resolution_summary(resolutions: list) -> dict:
    return {
        "total": len(resolutions),
        "stable": sum(1 for r in resolutions if r.is_stable()),
        "candidate": sum(1 for r in resolutions if r.status == IdStatus.CANDIDATE),
        "manifest_reproducible": all(r.is_stable() for r in resolutions),
    }