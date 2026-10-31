"""face_render_signal_check.py
Scores a prompt for photorealistic vs. painterly face-render signals.

Source: art_01M64VKDBYKTJ5C5FYZ35GY6HC r2
Finding: with identical props (steampunk valve wheel, masked man),
face rendering language decides whether frames read as filmed or painted.

Usage:
    from face_render_signal_check import score, classify
    ph, pa, ph_hits, pa_hits = score(my_prompt)
    print(classify(ph, pa))
"""
import re
from typing import List, Tuple

PHOTO_SIGNALS: List[str] = [
    "photorealistic", "photographed", "shot on", "shot with", "film grain",
    "skin texture", "pore detail", "subsurface scatter", "RAW photo",
    "hyperrealistic", "lifelike", "candid", "documentary", "lens flare",
    "bokeh", "depth of field", "ISO", "f/", "mm lens",
]

PAINTERLY_SIGNALS: List[str] = [
    "painted", "painterly", "oil painting", "watercolor", "illustrated",
    "concept art", "brush stroke", "artistic", "stylized", "render",
    "matte painting", "digital art", "gouache", "impressionist",
    "graphic novel", "comic", "cel-shaded", "animation",
]

def normalise(text: str) -> str:
    """Collapse hyphens/underscores and lowercase for consistent matching."""
    return re.sub(r"[-_]", " ", text.lower())

def score(prompt: str) -> Tuple[int, int, List[str], List[str]]:
    """Return (photo_count, paint_count, photo_hits, paint_hits)."""
    n = normalise(prompt)
    ph_hits = [s for s in PHOTO_SIGNALS if s in n]
    pa_hits = [s for s in PAINTERLY_SIGNALS if s in n]
    return len(ph_hits), len(pa_hits), ph_hits, pa_hits

def classify(photo: int, paint: int) -> str:
    """Classify the face-render lean of a prompt."""
    if photo == 0 and paint == 0:
        return "UNGUIDED (ambiguous)"
    if photo > paint:
        return "PHOTO-LEAN"
    if paint > photo:
        return "PAINTERLY-LEAN"
    return "MIXED"

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "A severe-faced woman at a brass steampunk valve wheel, steam rising, "
        "a masked man at a pressure-gauge panel, dramatic industrial lighting."
    )
    ph, pa, ph_hits, pa_hits = score(prompt)
    print(f"Photo signals : {ph} {ph_hits}")
    print(f"Paint signals : {pa} {pa_hits}")
    print(f"Read          : {classify(ph, pa)}")