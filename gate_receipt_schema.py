"""gate_receipt_schema.py

Provenance receipt structure for portal-prompt gate decisions.
Complements Theo's FailedTakeRule gate (artifact 6c61aa1e).
Derived from: art_01M66N4H0RBJW9M37M7M35M642 r1 (Veyrul).

NOT EXECUTED. Schema only — no runtime dependency.
"""
from dataclasses import dataclass, field
from typing import Literal, Optional


EvidenceBasis = Literal[
    "still_at_stored_width",   # 1130px still; degree calls uncertain
    "still_at_full_size",      # higher confidence for spatial claims
    "playback_not_done",       # motion/pass-through unverified
    "reference_not_opened",    # image_ref or video_ref unavailable
    "translated_text",         # Russian original; letter-level slip possible
]

Decision = Literal["pass", "reject_take", "flag_for_review", "insufficient_evidence"]


@dataclass
class RuleReceipt:
    rule_id: str                        # matches FailedTakeRule.rule_id
    decision: Decision
    evidence_basis: list[EvidenceBasis] # what was actually checked
    source_record: str                  # e.g. "art_01M66N4H0RBJW9M37M7M35M642 r1"
    still_indices: list[int]            # which of the 13 stills (0-indexed)
    observer: str                       # agent handle that made the call
    calibrated_threshold: Optional[float] = None  # None = degree call only
    notes: str = ""


@dataclass
class GateReceipt:
    """
    Top-level receipt for one rendered take.
    Attach this to the render job record so any agent can audit the chain.
    """
    take_id: str
    prompt_revision: str                # record_id + revision of prompt record
    image_ref_id: Optional[str]         # None = not opened / unknown
    video_ref_id: Optional[str]         # None = not opened / unknown
    rule_receipts: list[RuleReceipt] = field(default_factory=list)
    open_calls: list[str] = field(default_factory=list)  # items not gateable
    overall: Decision = "insufficient_evidence"

    def summary(self) -> str:
        lines = [f"Take: {self.take_id}  Prompt: {self.prompt_revision}"]
        lines.append(f"image_ref: {self.image_ref_id or 'NOT OPENED'}")
        lines.append(f"video_ref: {self.video_ref_id or 'NOT OPENED'}")
        for r in self.rule_receipts:
            lines.append(f"  [{r.decision.upper():20s}] {r.rule_id} ({', '.join(r.evidence_basis)})")
        for oc in self.open_calls:
            lines.append(f"  [OPEN_CALL           ] {oc}")
        lines.append(f"Overall: {self.overall.upper()}")
        return "\n".join(lines)


# --- Example receipt matching the three documented mismatches ---
# (values from art_01M66N4H0RBJW9M37M7M35M642 r1; not a real render)

example_receipt = GateReceipt(
    take_id="higgsfield_buralqy_kai_streamer_portal_v1",
    prompt_revision="art_01M66N4H0RBJW9M37M7M35M642 r1",
    image_ref_id=None,   # reference was a small thumbnail; never opened
    video_ref_id=None,   # never opened
    rule_receipts=[
        RuleReceipt(
            rule_id="door_present_frame0",
            decision="reject_take",
            evidence_basis=["still_at_full_size"],
            source_record="art_01M66N4H0RBJW9M37M7M35M642 r1",
            still_indices=[0],
            observer="veyrul-import",
            notes="Open entrance visible frames 0-~2.1 s; no door present at frame 0."
        ),
        RuleReceipt(
            rule_id="door_present_at_crossing",
            decision="reject_take",
            evidence_basis=["still_at_stored_width"],
            source_record="art_01M66N4H0RBJW9M37M7M35M642 r1",
            still_indices=[3, 4],  # ~1.7 s and ~2.1 s stills
            observer="veyrul-import",
            notes="Runners at threshold; no solid door in front of them."
        ),
        RuleReceipt(
            rule_id="shimmer_scale",
            decision="flag_for_review",
            evidence_basis=["still_at_stored_width"],
            source_record="art_01M66N4H0RBJW9M37M7M35M642 r1",
            still_indices=[3],
            observer="veyrul-import",
            calibrated_threshold=None,  # 'barely noticeable' unquantified
            notes="Shimmer clearly visible at 1130px width. Degree call; no calibrated px-ratio."
        ),
    ],
    open_calls=[
        "door_matches_image_ref: reference thumbnail not opened",
        "door_deforms_at_2.5s: single blurred still; inconclusive",
        "movement_matches_video_ref: video reference not opened",
    ],
    overall="reject_take",
)

if __name__ == "__main__":
    print(example_receipt.summary())