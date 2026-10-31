"""Trends by Firecrawl – interest_by_region payload builder.

Source: art_01M68GXHKEFJQ08H328SP4SP3B r1
Documented constraints:
  - 1 to 5 keywords (or topic IDs)
  - category_id >= 0  (0 = all categories)
  - location: empty string = worldwide, ISO country, region, or US metro
  - property: web | images | news | youtube | shopping
  - cost: 5 credits per call

No HTTP calls are made here. Validate before spending credits.
Data terms for Trends are not listed in the provider schedule as of 2026-10-31;
see the source record for the terms caveat.
"""

VALID_PROPERTIES = {"web", "images", "news", "youtube", "shopping"}
ESTIMATED_CREDITS = 5


def build_interest_by_region_payload(
    keywords: list,
    category_id: int = 0,
    location: str = "",
    property: str = "web",
) -> dict:
    """Return {valid, errors, payload}. payload is None when invalid."""
    errors = []
    if not (1 <= len(keywords) <= 5):
        errors.append(f"keywords must be 1-5 items; got {len(keywords)}")
    if any(not str(k).strip() for k in keywords):
        errors.append("all keywords must be non-empty strings")
    if category_id < 0:
        errors.append("category_id must be >= 0 (0 = all categories)")
    if property not in VALID_PROPERTIES:
        errors.append(
            f"property must be one of {sorted(VALID_PROPERTIES)}; got '{property}'"
        )
    if errors:
        return {"valid": False, "errors": errors, "payload": None}
    return {
        "valid": True,
        "errors": [],
        "payload": {
            "keywords": list(keywords),
            "category_id": category_id,
            "location": location,
            "property": property,
            "estimated_credits": ESTIMATED_CREDITS,
        },
    }