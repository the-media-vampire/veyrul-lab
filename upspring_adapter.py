"""upspring_adapter.py

Integration contract: Firecrawl Alexandria → hook-analysis workflow.
Documentary sample only. No live API call is made here.

Interface boundary
------------------
Input  : SearchRequest  (free-text brief, optional filters, page limit)
Output : HookPage       (list of AdRow, provenance block, credit cost)

Provenance carried through every row so downstream consumers can
attribute data to Schedule J-1.0.0 (art_01M68F97NN9PTR3SSHK6MZ12QX r1).
"""
from dataclasses import dataclass, field
from typing import Optional
import json

# ── Types ────────────────────────────────────────────────────────────────────

@dataclass
class SearchRequest:
    q: str                          # free-text brief
    limit: int = 25                 # 1-100; 1-50 with descriptors
    vertical: Optional[str] = None
    category: Optional[str] = None
    advertiser: Optional[str] = None
    include_descriptors: bool = False

@dataclass
class Provenance:
    source: str = "Firecrawl Alexandria / Upspring"
    schedule: str = "J-1.0.0"
    effective: str = "2026-10-15"
    veyrul_record: str = "art_01M68F97NN9PTR3SSHK6MZ12QX r1"
    notes: str = (
        "Retain & use for any lawful purpose; no standalone resale. "
        "Ad copyright held by original advertisers (unknown)."
    )

@dataclass
class AdRow:
    media_type: str
    is_active: bool
    started_at: Optional[str]
    dimensions: Optional[str]
    one_line: Optional[str]
    hook_text: Optional[str]
    strength: Optional[str]         # coarse tier, not exact metric
    ad_library_url: Optional[str]
    provenance: Provenance = field(default_factory=Provenance)

@dataclass
class HookPage:
    request: SearchRequest
    rows: list                      # list[AdRow]
    credits_charged: int            # 50 per non-empty page (documented)
    provenance: Provenance = field(default_factory=Provenance)
    warning: str = "Sample shape only; field quality untested."

# ── Cost gate ────────────────────────────────────────────────────────────────

CREDITS_PER_PAGE = 50              # art_01M68F97NN9PTR3SSHK6MZ12QX r1
STANDARD_RATE   = 99 / 100_000    # $/credit at Standard plan (our arithmetic)

def estimated_cost_usd(pages: int) -> float:
    """Rough ceiling only; assumes Alexandria credits == plan credits."""
    return pages * CREDITS_PER_PAGE * STANDARD_RATE

def cost_gate(budget_usd: float, pages_requested: int) -> bool:
    """Return True only if estimated spend fits budget."""
    return estimated_cost_usd(pages_requested) <= budget_usd

# ── Stub call (documentary) ──────────────────────────────────────────────────

def search_ads(req: SearchRequest, api_key: str) -> HookPage:
    """
    STUB. Real call: POST https://api.firecrawl.dev/v1/alexandria/ads/search
    with {q, limit, vertical, category, advertiser} in JSON body
    and Authorization: Bearer <api_key> header.

    Limit must be <=50 when include_descriptors=True.
    Returns HookPage; caller must check HookPage.rows before consuming credits.
    """
    # Enforcement of documented limit
    if req.include_descriptors and req.limit > 50:
        raise ValueError("Descriptor requests capped at 50 ads/page (documented).")

    # Not executed; returns placeholder so contract shape is testable
    stub_row = AdRow(
        media_type="video",
        is_active=True,
        started_at="2026-09-01",
        dimensions="1080x1920",
        one_line="Stub one-liner",
        hook_text="Stub hook text",
        strength="medium",          # coarse tier
        ad_library_url="https://www.facebook.com/ads/library/?id=stub",
    )
    return HookPage(
        request=req,
        rows=[stub_row],
        credits_charged=CREDITS_PER_PAGE,
    )

# ── Quick contract smoke-test ────────────────────────────────────────────────

if __name__ == "__main__":
    req = SearchRequest(q="performance skincare serum", limit=10)
    assert cost_gate(budget_usd=1.00, pages_requested=1), "Budget gate broken"
    page = search_ads(req, api_key="KEY_PLACEHOLDER")
    print(json.dumps({
        "rows": len(page.rows),
        "credits": page.credits_charged,
        "est_cost_usd": round(estimated_cost_usd(1), 4),
        "schedule": page.provenance.schedule,
        "warning": page.warning,
    }, indent=2))