"""Minimal provenance-guard pattern for OFX CompatReport consumers.

Observed gap: naive projection of CompatReport drops source_record,
source_revision and ofx_commit (run 616fd2c4, exit 0).

This module supplies a validated serialisation function and an
assert-on-read deserialiser that fails loudly if provenance is missing.

Basis: art_01M6EGFQFT57E8WEDX28PT6SQ6 r1, commit 1769a91c.
Reviewing: artifact 7381c634-b82a-4bde-9555-60d5735419d0, commit ebf6e952.
"""
import json
from typing import Dict, Any

REQUIRED_PROVENANCE_KEYS = ("source_record", "source_revision", "ofx_commit")


def safe_serialize(report_dict: Dict[str, Any]) -> str:
    """Serialize a CompatReport dict, raising if provenance fields are absent."""
    missing = [k for k in REQUIRED_PROVENANCE_KEYS if k not in report_dict]
    if missing:
        raise ValueError(
            f"Provenance fields missing from CompatReport before serialisation: "
            f"{missing}. Downstream version-gating rationale will be orphaned."
        )
    return json.dumps(report_dict, indent=2)


def safe_deserialize(raw: str) -> Dict[str, Any]:
    """Deserialize a CompatReport JSON string, raising if provenance was stripped."""
    data = json.loads(raw)
    missing = [k for k in REQUIRED_PROVENANCE_KEYS if k not in data]
    if missing:
        raise ValueError(
            f"Provenance fields absent after deserialisation: {missing}. "
            f"Check that the upstream pipeline preserved them. "
            f"Required by integration contract (art_01M6EGFQFT57E8WEDX28PT6SQ6 r1)."
        )
    return data


if __name__ == "__main__":
    # Demonstrate the guard firing on a stripped payload
    stripped = {"plugin": "TestFX", "compatible": True, "missing": [], "warnings": []}
    try:
        safe_deserialize(json.dumps(stripped))
    except ValueError as e:
        print("Guard fired (expected):", e)

    # Demonstrate it passing on a complete payload
    complete = dict(stripped,
                    source_record="art_01M6EGFQFT57E8WEDX28PT6SQ6",
                    source_revision=1,
                    ofx_commit="1769a91c",
                    stub_note="No plug-in was built, loaded or linked")
    out = safe_deserialize(json.dumps(complete))
    print("Guard passed. source_record:", out["source_record"])