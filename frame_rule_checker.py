"""Minimal rule/observation scorer for video-generation prompt rules.
Source observations: art_01M6A19D9WCBJFN6YNNXNTP570 r2 (Veyrul)
check_type: 'boolean' | 'exact' | 'contains'
confidence: 'clear' | 'partial' | 'unclear'
"""
from dataclasses import dataclass
from typing import Optional, Any

MATCH, MISMATCH, AMBIGUOUS, NOT_VERIFIED = "MATCH","MISMATCH","AMBIGUOUS","NOT_VERIFIED"

@dataclass
class Rule:
    rule_id: str
    description: str
    check_type: str
    expected: Any

@dataclass
class FrameObs:
    rule_id: str
    observed: Optional[Any]
    confidence: str

def check(rule: Rule, obs: FrameObs) -> str:
    if obs.observed is None or obs.confidence == 'unclear':
        return NOT_VERIFIED
    if obs.confidence == 'partial':
        return AMBIGUOUS
    if rule.check_type == 'boolean':
        return MATCH if bool(obs.observed) == bool(rule.expected) else MISMATCH
    if rule.check_type == 'exact':
        return MATCH if obs.observed == rule.expected else MISMATCH
    if rule.check_type == 'contains':
        return MATCH if rule.expected in str(obs.observed) else MISMATCH
    return NOT_VERIFIED

def score_clip(rules, observations):
    obs_map = {o.rule_id: o for o in observations}
    return [{"rule_id": r.rule_id, "description": r.description,
             "verdict": check(r, obs_map[r.rule_id]) if r.rule_id in obs_map else NOT_VERIFIED}
            for r in rules]