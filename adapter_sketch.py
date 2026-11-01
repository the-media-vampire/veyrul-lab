"""Adapter sketch: pre-check anchor budget before VectorCraft Image Trace.
Documented interface only; not connected to a live VectorCraft instance.
Source: art_01M6C4DQJT443MQZBT1S1F8R8D r1.
"""

ANCHOR_LIMIT_DESKTOP = 8_000_000
ANCHOR_LIMIT_WEB = 2_000_000


def estimate_anchors(width_px: int, height_px: int, noise_px: int = 2) -> int:
    """Heuristic: anchor count ~ (pixel area) / (noise_px^2).
    This is an approximation; actual count depends on image content."""
    return int((width_px * height_px) / max(noise_px ** 2, 1))


def trace_or_tile(
    width_px: int,
    height_px: int,
    noise_px: int = 2,
    web_target: bool = False,
) -> dict:
    """Return a routing decision: direct trace or tile strategy."""
    limit = ANCHOR_LIMIT_WEB if web_target else ANCHOR_LIMIT_DESKTOP
    estimate = estimate_anchors(width_px, height_px, noise_px)
    if estimate <= limit:
        return {"strategy": "direct", "estimated_anchors": estimate, "tiles": 1}
    # Tile into N equal parts so each part is under limit
    import math
    n_tiles = math.ceil(estimate / limit)
    return {
        "strategy": "tile",
        "estimated_anchors": estimate,
        "tiles": n_tiles,
        "assumption": "ASSUMPTION_B: seam merge via linesweeper is lossless",
    }


if __name__ == "__main__":
    cases = [
        (4000, 3000, 2, False),
        (12000, 9000, 2, False),
        (4000, 3000, 2, True),
    ]
    for w, h, noise, web in cases:
        result = trace_or_tile(w, h, noise, web)
        print(f"{w}x{h} noise={noise} web={web}: {result}")