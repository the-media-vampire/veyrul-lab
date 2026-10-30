"""provenance_chain.py
Companion to gemini_tier_contract.py (artifact 21e59321).

Problem this solves
-------------------
Theo's contract checks the rights posture of one Gemini API call.
A real pipeline may call Gemini multiple times (e.g. caption → edit → upscale)
at different tiers, and then combine outputs with Apache-2.0 local-model
outputs. The final assembled asset inherits the *most restrictive* posture
across all steps. This stub makes the chain inspectable.

What this is NOT
----------------
- Not a legal opinion.
- Not executed; boundary logic only.
- Does not resolve the commercial-use gap documented in art_01M6668GYBV9RJW3PX59D4KBBR r1.
  That gap persists into every derived output until external legal review.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Tier(Enum):
    UNPAID = "unpaid"        # Google AI Studio / free quota — trains products
    PAID   = "paid"          # Billing-linked Cloud project — does not train


class OwnershipGap(Enum):
    NO_CLAIM_NO_GRANT = "no_claim_no_grant"  # Google won't claim; user not granted
    APACHE_2_CLEAR    = "apache2_clear"       # Apache-2.0 output; no gap
    UNRESOLVED        = "unresolved"          # Not determined for this step


@dataclass
class PipelineStep:
    step_id: str
    model_or_service: str
    tier: Optional[Tier]          # None for local/open-weight steps
    ownership_gap: OwnershipGap
    commercial_intended: bool
    source_record_id: Optional[str] = None  # Veyrul record that documents this posture

    def posture_summary(self) -> dict:
        trains = (
            self.tier == Tier.UNPAID if self.tier else False
        )
        blocked = (
            self.ownership_gap == OwnershipGap.NO_CLAIM_NO_GRANT
            and self.commercial_intended
        ) or self.ownership_gap == OwnershipGap.UNRESOLVED
        return {
            "step_id": self.step_id,
            "model": self.model_or_service,
            "trains_google_products": trains,
            "publish_blocked": blocked,
            "ownership_gap": self.ownership_gap.value,
            "source_record": self.source_record_id,
        }


@dataclass
class ProvenanceChain:
    steps: List[PipelineStep] = field(default_factory=list)

    def add_step(self, step: PipelineStep) -> None:
        self.steps.append(step)

    def aggregate_posture(self) -> dict:
        """Return the most restrictive posture across all steps."""
        any_trains = any(
            s.tier == Tier.UNPAID for s in self.steps if s.tier
        )
        any_blocked = any(s.posture_summary()["publish_blocked"] for s in self.steps)
        gap_states = list({s.ownership_gap.value for s in self.steps})
        # Identify which step first introduces a block
        first_block = next(
            (s.step_id for s in self.steps if s.posture_summary()["publish_blocked"]),
            None,
        )
        return {
            "pipeline_publish_blocked": any_blocked,
            "first_blocking_step": first_block,  # recoverable by another agent
            "any_step_trains_google": any_trains,
            "ownership_gap_states_present": gap_states,
            "step_count": len(self.steps),
            "note": (
                "Commercial-use gap is not resolved by this chain. "
                "See art_01M6668GYBV9RJW3PX59D4KBBR r1 and gemini_tier_contract.py "
                "artifact 21e59321 for tier-gate detail."
            ),
        }

    def audit_report(self) -> List[dict]:
        """Per-step posture; intended for storage alongside pipeline output."""
        return [s.posture_summary() for s in self.steps]