"""disc_prompt_scorer.py
Prompt discipline scorer for single-prop Seedance scene coverage.

Derived from observations in art_01M64VKZ36V70FHZ5PHSM9651S revision 2:
  - one place anchors all eight shots
  - exactly one yellow disc at all times
  - one named anchor character (orange tee/tank top)

Usage:
  from disc_prompt_scorer import score
  result = score(my_prompt)   # {score: int, max: 4, ...flags}

A score of 4/4 is fully disciplined; < 3 is a warning.
This is a text heuristic, not a rendering guarantee.
"""
import re

PLACE_TOKENS = [
    "red-brick school", "ramp", "lawn", "step", "walkway", "railing",
]
DISC_TOKENS = [
    "yellow disc", "yellow flying disc", "one disc", "single disc",
    "single yellow disc", "one yellow disc",
]
MULTI_DISC_PATTERNS = [
    r"\bdiscs\b", r"\btwo discs\b", r"\bseveral discs\b", r"\bmultiple discs\b",
]
ANCHOR_CHAR_TOKENS = ["orange tee", "orange tank top", "orange shirt"]


def score(prompt: str) -> dict:
    """Return discipline scores for a single prompt string."""
    p = prompt.lower()
    place      = any(t in p for t in PLACE_TOKENS)
    single_disc = any(t in p for t in DISC_TOKENS)
    multi_disc  = any(re.search(pat, p) for pat in MULTI_DISC_PATTERNS)
    anchor_char = any(t in p for t in ANCHOR_CHAR_TOKENS)

    total = sum([place, single_disc, not multi_disc, anchor_char])
    return {
        "score":       total,
        "max":         4,
        "place":       place,
        "single_disc": single_disc,
        "no_multi":    not multi_disc,
        "anchor_char": anchor_char,
        "warning":     total < 3,
    }


def report(prompt: str) -> None:
    r = score(prompt)
    print(f"Score {r['score']}/{r['max']}  warning={r['warning']}")
    print(f"  place={r['place']}  single_disc={r['single_disc']}  "
          f"no_multi={r['no_multi']}  anchor_char={r['anchor_char']}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        report(" ".join(sys.argv[1:]))
    else:
        report("Outside the red-brick school, the single yellow disc rests on the ramp; "
               "a man in an orange tee reaches down to pick it up.")