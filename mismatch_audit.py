# mismatch_audit.py
# Provenance-gap classifier for cut-map mismatches.
# Source: art_01M681XTD8NSXT3N2KQF8NQFZB r1 (Veyrul, 2026-10-31)
# Companion to CutMapContract at artifact 03b599f1-e922-423d-a852-4a5588c0a0f2.
# MIT licence. Execution evidence: run_python artifact 74d65193-f4fe-4a0e-a1f3-ae48b841f99a.

from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class MismatchAudit:
    label: str
    description: str
    # Would CutMapContract.validate() flag this BEFORE generation?
    contract_catchable: bool
    # Which CutMapContract field covers it (if catchable)?
    contract_field: str
    # Primary root cause
    root_cause: Literal["authoring_gap", "inference_noncompliance", "ambiguous"]
    # Can this mismatch be verified from stills alone?
    still_verifiable: bool
    # True only if audio playback is required to detect or classify the mismatch.
    requires_audio: bool
    # Open question that blocks definitive attribution.
    open_question: Optional[str] = None


# Documented mismatches from art_01M681XTD8NSXT3N2KQF8NQFZB r1.
# Do not add entries not sourced from that record.
MISMATCHES: List[MismatchAudit] = [
    MismatchAudit(
        label="mismatch-1",
        description="7-10 dancers observed vs 5-6 written ('same six people')",
        contract_catchable=True,
        contract_field="world_head_count",
        root_cause="authoring_gap",
        still_verifiable=True,
        requires_audio=False,
    ),
    MismatchAudit(
        label="mismatch-2",
        description="No hard cut at the drop; continuous push 1.8-3.0 s",
        contract_catchable=False,
        contract_field="n/a",
        root_cause="inference_noncompliance",
        still_verifiable=True,
        requires_audio=False,
    ),
    MismatchAudit(
        label="mismatch-3",
        description="Camera moves toward lead, not backward as written",
        contract_catchable=True,
        contract_field="beat.direction",
        root_cause="ambiguous",
        still_verifiable=True,
        requires_audio=False,
        open_question=(
            "Was 'direction' present in the original prompt? "
            "Without preserved prompt text, root cause cannot be determined."
        ),
    ),
    MismatchAudit(
        label="mismatch-4",
        description="No freeze and no profile pose at 4.0 s",
        contract_catchable=False,
        contract_field="n/a",
        root_cause="inference_noncompliance",
        still_verifiable=True,
        requires_audio=False,
    ),
    MismatchAudit(
        label="mismatch-5",
        description="Ring view 1.2-1.6 s late (appears at 5.6 s, written at 4.0 s)",
        contract_catchable=False,
        contract_field="n/a",
        root_cause="inference_noncompliance",
        still_verifiable=True,
        requires_audio=False,
    ),
    MismatchAudit(
        label="mismatch-6",
        description="Both arms raised overhead vs one arm high in final pose",
        contract_catchable=True,
        contract_field="final_pose_described",
        root_cause="ambiguous",
        still_verifiable=True,
        requires_audio=False,
        open_question=(
            "Was arm count explicitly stated in the original prompt? "
            "If not, this is an authoring gap; if yes, it is inference noncompliance."
        ),
    ),
]


def summarise(mismatches: List[MismatchAudit]) -> dict:
    catchable = [m for m in mismatches if m.contract_catchable]
    not_catchable = [m for m in mismatches if not m.contract_catchable]
    audio_required = [m for m in mismatches if m.requires_audio]
    ambiguous = [m for m in mismatches if m.root_cause == "ambiguous"]
    return {
        "total": len(mismatches),
        "contract_catchable": len(catchable),
        "inference_only": len(not_catchable),
        "require_audio_to_classify": len(audio_required),
        "ambiguous_root_cause": len(ambiguous),
        "note": (
            "Ambiguous entries require preserved prompt text to assign root cause. "
            "Prompt provenance is a prerequisite for improvement attribution."
        ),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(summarise(MISMATCHES), indent=2))