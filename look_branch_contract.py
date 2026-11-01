"""look_branch_contract.py

Two-branch compositing contract keyed on Seedance 2.5 look_target.
Source observation: art_01M64VK50F7QM10TWFSS9HRXBQ r2.
Execution verified: run 931fad90-7ab9-4908-8cb1-f7340c271fbb.

All shading_mode and compositing_hint values are INFERRED from the
visual description in the source article; they are proposals, not
confirmed Seedance output specifications.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class LookBranchContract:
    look_target: str
    shading_mode: str
    compositing_hint: str
    face_geometry: str
    documented_in_source: bool
    open_assumptions: List[str] = field(default_factory=list)

CONTRACTS = {
    "3d_cinematic": LookBranchContract(
        look_target="3d_cinematic",
        shading_mode="physically_based",
        compositing_hint="preserve_normals",
        face_geometry="volumetric",
        documented_in_source=True,
        open_assumptions=[
            "Pixel format at output boundary not stated in source",
            "Whether Seedance exports separate alpha not stated",
            "No stated license for model outputs in source",
        ]
    ),
    "anime_first": LookBranchContract(
        look_target="anime_first",
        shading_mode="flat_cel",
        compositing_hint="posterize_before_key",
        face_geometry="planar",
        documented_in_source=True,
        open_assumptions=[
            "Degree of flatness is not quantified (no pixel metric in source)",
            "Four runs, no seed — variance within anime-first group unknown",
            "Audio behaviour not reviewed in source",
        ]
    ),
}

def adapter(look_target: str) -> dict:
    """Return compositing parameters for the given look_target.

    Raises ValueError for unknown targets.
    All returned values are proposals; verify pixel format before use.
    """
    contract = CONTRACTS.get(look_target)
    if contract is None:
        raise ValueError(
            f"Unknown look_target: {look_target!r}. "
            f"Must be one of {list(CONTRACTS)}"
        )
    return {
        "shading_mode": contract.shading_mode,
        "compositing_hint": contract.compositing_hint,
        "face_geometry": contract.face_geometry,
        "open_assumptions": contract.open_assumptions,
    }