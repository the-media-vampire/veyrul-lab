"""Gemini API tier-gate contract.

Encodes the rights posture from art_01M6668GYBV9RJW3PX59D4KBBR r1
as a typed, checkable object. Not a legal opinion.

Key documented facts (source: art_01M6668GYBV9RJW3PX59D4KBBR r1):
  - Google 'won't claim ownership' of generated content.
  - Google does NOT state the user owns outputs.
  - Unpaid tier: inputs/outputs used to improve Google products;
    human reviewers may read them.
  - Paid tier: inputs/outputs NOT used for product improvement;
    logged for limited period only (violation detection).
  - Commercial use of outputs: not addressed in the terms text.
  - Image models / watermarking / indemnity: not mentioned.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class GeminiTier(Enum):
    UNPAID = "unpaid"   # AI Studio + free quota
    PAID   = "paid"     # billing-linked Cloud project


class OwnershipGap(Enum):
    """The gap between 'no claim' and 'user owns'."""
    NO_CLAIM_NO_GRANT = "google_wont_claim_but_user_not_stated_to_own"


@dataclass
class GeminiOutputProvenance:
    tier: GeminiTier
    # Fields caller must supply; none have defaults.
    prompt_contains_sensitive_data: bool
    intended_use_commercial: bool
    source_record: str = "art_01M6668GYBV9RJW3PX59D4KBBR r1"
    ownership_posture: OwnershipGap = field(
        default=OwnershipGap.NO_CLAIM_NO_GRANT, init=False
    )

    def training_exposure(self) -> str:
        if self.tier == GeminiTier.UNPAID:
            return (
                "INPUT_AND_OUTPUT_MAY_TRAIN_GOOGLE_PRODUCTS; "
                "human reviewers may access"
            )
        return "NOT_USED_FOR_PRODUCT_IMPROVEMENT; limited violation-detection log"

    def sensitive_data_warning(self) -> Optional[str]:
        if self.tier == GeminiTier.UNPAID and self.prompt_contains_sensitive_data:
            return (
                "BLOCKED: unpaid tier + sensitive data. Terms advise against "
                "submitting confidential or personal information on unpaid tier."
            )
        return None

    def commercial_use_status(self) -> str:
        if self.intended_use_commercial:
            return (
                "UNRESOLVED: terms text does not address commercial use of outputs. "
                "Ownership gap: %s. Seek legal review before publication."
                % self.ownership_posture.value
            )
        return "non_commercial_use; ownership_gap still applies"

    def is_publish_blocked(self) -> bool:
        """Hard gate: block publication if any critical condition is unresolved."""
        return (
            self.sensitive_data_warning() is not None
            or self.intended_use_commercial  # commercial = unresolved until reviewed
        )

    def summary(self) -> dict:
        return {
            "tier": self.tier.value,
            "training_exposure": self.training_exposure(),
            "sensitive_data_warning": self.sensitive_data_warning(),
            "commercial_use_status": self.commercial_use_status(),
            "ownership_posture": self.ownership_posture.value,
            "publish_blocked": self.is_publish_blocked(),
            "source_record": self.source_record,
        }


# --- Open-weight comparison interface (for Apache-2.0 models) ---
# Qwen-Image-Edit-2511: Apache-2.0 (art_01M5Z9WPX7FY4WPTTW9T1VXS34)
# FLUX.2 klein 4B:      Apache-2.0, commercial use allowed (art_01M5Z8GBK4E8122A4EZXZYQPWR)
# FLUX.1 Kontext dev:   FLUX.1-dev Non-Commercial; outputs personal/scientific/commercial
#                        per card, but weights non-commercial (src_01M569CC9H9QD4PQH3YX037GNB)
# FLUX.2 klein 9B:      FLUX Non-Commercial; output commercial status not addressed
#                        (art_01M5ZAFS2Z0A54WCZ18WQM4H57)
# Fibo 2.0:             Non-commercial unless BRIA agreement (art_01M62J20F9N2DNA0A84TTAD9Y7)

@dataclass
class OpenWeightOutputProvenance:
    model_id: str
    weight_license: str          # e.g. "Apache-2.0", "FLUX.1-dev Non-Commercial"
    output_commercial_allowed: Optional[bool]  # None = not established
    source_record: str

    def is_publish_blocked(self) -> bool:
        # Block if commercial status unknown or explicitly disallowed.
        if self.output_commercial_allowed is None:
            return True  # gap: not established
        return not self.output_commercial_allowed

    def summary(self) -> dict:
        return {
            "model_id": self.model_id,
            "weight_license": self.weight_license,
            "output_commercial_allowed": self.output_commercial_allowed,
            "publish_blocked": self.is_publish_blocked(),
            "source_record": self.source_record,
        }