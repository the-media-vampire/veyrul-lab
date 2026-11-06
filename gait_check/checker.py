"""Minimal walk-order checker.

Usage:
    result = check_stride(stride)

See contract.md for the full interface specification.
Source: art_01M6Q6TWNDRV36VHATTZYMPYYE rev 2 (eBook 37743, Muybridge lecture).
"""

EXPECTED_WALK = ["LH", "LF", "RH", "RF"]


def check_stride(stride: dict) -> dict:
    """Check one stride dict against the reported walk order."""
    contacts = stride.get("contacts", [])
    observed = [c["foot"] for c in contacts]
    flags = []

    # Flag ambiguous labels
    if "?" in observed:
        flags.append("ambiguous_frame")
        observed = [f for f in observed if f != "?"]

    # Normalise to one cycle: strip repeated tail that wraps back to start
    cycle = _extract_one_cycle(observed, EXPECTED_WALK)

    missing = [f for f in EXPECTED_WALK if f not in cycle]
    extra = [f for f in cycle if f not in EXPECTED_WALK]
    if missing:
        flags.append("missing_contact")
    if extra:
        flags.append("extra_contact")

    match = (cycle == EXPECTED_WALK) and not flags
    if cycle and cycle != EXPECTED_WALK and "wrong_order" not in flags:
        if not missing and not extra:
            flags.append("wrong_order")

    return {
        "stride_id": stride.get("stride_id", ""),
        "expected_cycle": EXPECTED_WALK,
        "observed_cycle": cycle,
        "match": match,
        "flags": flags,
    }


def _extract_one_cycle(observed: list, expected: list) -> list:
    """Return the first complete pass through the expected set, in order seen."""
    seen = []
    remaining = list(expected)
    for foot in observed:
        if foot in remaining:
            seen.append(foot)
            remaining.remove(foot)
        if not remaining:
            break
    return seen