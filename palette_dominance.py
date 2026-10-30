"""palette_dominance.py
Baseline scorer for the palette-dominance claim.
Source: art_01M64VKGMQ5BD4BMXVFP0VJPZA r2

Usage:
  Fill in real reviewer frame notes in simulated_frame_desc.
  A scene passes if stated_hits > ref_hits.
  The 'drowning stair' case needs care: 'red' and 'black' also appear in
  reference-image descriptions, so use more specific terms like 'crimson'
  or 'obsidian' in the prompt and note to disambiguate.

Known limit: keyword matching is naive. A colour synonym ('scarlet' vs 'red')
will miss. Extend the stated_palette list with synonyms for robustness.
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class ScenePaletteCase:
    scene: str
    stated_palette: List[str]        # exact or synonym keywords
    reference_palette_hint: List[str] # colours the ref image might contribute
    simulated_frame_desc: str        # replace with real frame note


cases = [
    ScenePaletteCase(
        scene="drowning stair",
        # Use specific terms to avoid collision with ref-image generic 'red/black'
        stated_palette=["crimson", "obsidian", "red", "black"],
        reference_palette_hint=["warm", "neutral", "brown", "beige"],
        simulated_frame_desc="REPLACE WITH REAL FRAME NOTE",
    ),
    ScenePaletteCase(
        scene="black coils",
        stated_palette=["violet", "black", "purple"],
        reference_palette_hint=["warm", "neutral", "brown", "beige"],
        simulated_frame_desc="REPLACE WITH REAL FRAME NOTE",
    ),
    ScenePaletteCase(
        scene="reliquary hall",
        stated_palette=["white", "gold", "ivory", "gilt"],
        reference_palette_hint=["warm", "neutral", "brown", "beige"],
        simulated_frame_desc="REPLACE WITH REAL FRAME NOTE",
    ),
    ScenePaletteCase(
        scene="ice-cutting floor",
        stated_palette=["glacier blue", "blue", "gold", "cyan"],
        reference_palette_hint=["warm", "neutral", "brown", "beige"],
        simulated_frame_desc="REPLACE WITH REAL FRAME NOTE",
    ),
    ScenePaletteCase(
        scene="riverbed",
        stated_palette=["brown", "deep red", "ochre", "burgundy"],
        reference_palette_hint=["warm", "neutral", "beige"],
        simulated_frame_desc="REPLACE WITH REAL FRAME NOTE",
    ),
]


def score_palette(desc: str, keywords: List[str]) -> tuple[int, List[str]]:
    hits = [kw for kw in keywords if re.search(re.escape(kw), desc, re.IGNORECASE)]
    return len(hits), hits


def run(cases):
    print(f"{'Scene':<20} {'Stated hits':>12} {'Ref bleed':>10} {'Palette wins?':>14}")
    print("-" * 60)
    passes, failures = [], []
    for c in cases:
        if "REPLACE" in c.simulated_frame_desc:
            print(f"{c.scene:<20} {'(no note)':>12}")
            continue
        stated_n, _ = score_palette(c.simulated_frame_desc, c.stated_palette)
        ref_n, _ = score_palette(c.simulated_frame_desc, c.reference_palette_hint)
        wins = stated_n > ref_n
        (passes if wins else failures).append(c.scene)
        flag = "PASS" if wins else "FAIL"
        print(f"{c.scene:<20} {stated_n:>4}/{len(c.stated_palette):<7} "
              f"{ref_n:>4}/{len(c.reference_palette_hint):<5} {flag:>14}")
    print()
    print(f"Pass: {len(passes)}  Fail/ambiguous: {len(failures)}")
    if failures:
        print(f"Needs review: {failures}")
    print()
    print("Limit: keyword match; add synonyms to stated_palette for coverage.")
    print("Next: replace simulated_frame_desc with real reviewer frame notes.")


if __name__ == "__main__":
    run(cases)