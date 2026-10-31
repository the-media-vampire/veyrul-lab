"""
shot_clause_check.py v2
Orientation-rule reinforcement checker for multi-shot AI video prompts.

Motivation (art_01M6815JBN1Q0KJ0FNYFG9B38R r1):
  A rule restated in 2 positions (orientation section + physics law)
  did not prevent a mismatch in one sampled frame. The recipe skeleton
  says: state which face of the key object is toward the lens IN the
  shot action list, not only in global law sections.

This tool checks how many of three reinforcement positions contain a
given keyword for a given shot block. Fully reinforced = all three.

Usage:
  Instantiate ShotBlock with plain-text content from your prompt.
  Call check_rule(block, keyword) with the orientation keyword you care about.
  Risk: HIGH (<2 positions), MEDIUM (2 positions), LOW (all 3).

Limits:
  Keyword matching only; synonyms and paraphrases are not caught.
  Normalises hyphens/underscores to spaces before matching (v2 fix).
  Does not read prompt files; caller supplies text strings.
  No claim is made about model compliance from score alone.
"""
import re
from dataclasses import dataclass

POSITIONS = ["orientation_section", "shot_action_list", "physics_law"]

@dataclass
class ShotBlock:
    name: str
    orientation_section: str   # global orientation/geography block text
    shot_action_list: str      # the shot's own action list text
    physics_law: str           # post-shot physics law section text

def normalise(text: str) -> str:
    """Collapse hyphens and underscores to spaces for loose matching."""
    return re.sub(r"[-_]", " ", text.lower())

def check_rule(block: ShotBlock, keyword: str) -> dict:
    """
    Returns a dict with:
      shot, keyword, positions_hit (0-3), fully_reinforced (bool),
      detail (per-position bool), risk ('HIGH'|'MEDIUM'|'LOW')
    """
    kw = normalise(keyword)
    results = {}
    for pos in POSITIONS:
        text = normalise(getattr(block, pos))
        results[pos] = bool(re.search(re.escape(kw), text))
    count = sum(results.values())
    return {
        "shot": block.name,
        "keyword": keyword,
        "positions_hit": count,
        "fully_reinforced": count == 3,
        "detail": results,
        "risk": "HIGH" if count < 2 else ("MEDIUM" if count == 2 else "LOW"),
    }


if __name__ == "__main__":
    # Reproduce the three-case comparison from the article finding.
    # Source: art_01M6815JBN1Q0KJ0FNYFG9B38R r1

    case_partial = ShotBlock(
        name="Shot_04_baseline_law_only",
        orientation_section="phone flat on the table edge, tipping over",
        shot_action_list="figure punches through the glass; glass shatters outward",
        physics_law="broken screen face must face the lens during the fall",
    )
    case_medium = ShotBlock(
        name="Shot_07_orientation_plus_law_only",
        orientation_section="screen face toward camera as phone falls",
        shot_action_list="phone tumbles through air; figure visible below on floor",
        physics_law="screen face must face the lens",
    )
    case_full = ShotBlock(
        name="Shot_07_all_three_positions",
        orientation_section="screen face toward camera as phone falls",
        shot_action_list="phone falls screen-face toward lens, growing in frame; figure below",
        physics_law="screen face must face the lens",
    )

    keyword = "screen face"
    blocks = [case_partial, case_medium, case_full]

    print(f"{'Shot':<44} {'Hits':>4}  {'Risk':<6}  Fully?")
    print("-" * 72)
    for b in blocks:
        r = check_rule(b, keyword)
        print(f"{r['shot']:<44} {r['positions_hit']:>4}  {r['risk']:<6}  {r['fully_reinforced']}")
        for pos, hit in r['detail'].items():
            print(f"    {'checkmark' if hit else 'cross'} {pos}")