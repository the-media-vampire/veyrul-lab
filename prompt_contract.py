from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class CameraWindow:
    """One timed segment of a camera plan. Motion and action share the same window."""
    start_s: int
    end_s: int
    motion: str   # camera instruction
    action: str   # matching subject action

@dataclass
class FailedTakeRule:
    """
    A named predicate that, if true in the output, marks the take failed.
    log_key: the key a reviewer or classifier must set in the render-log dict.
    Set to True to fail, False to pass, omit for unknown.
    """
    name: str
    description: str
    log_key: str

@dataclass
class PromptContract:
    """
    Schema for a Seedance-Extend one-take continuation prompt.
    Derived from the block structure observed in THREAD (art_01M66898SM32BY2E0RQQ92W66F r1).
    Not tested against the full prompt or rendered output.
    """
    source_id: str                         # Veyrul record backing this contract
    continuation_anchor: str               # text description of source video last frame
    one_shot: bool = True                  # every framing change reached physically
    closed_room: bool = True               # no exits used
    reference_role: str = "knowledge"      # 'knowledge' | 'framing'
    facing_wall_desc: Optional[str] = None # wall the camera will turn to face
    dialogue_lock: Optional[Tuple[int, str]] = None  # (max_lines, constraint prose)
    lens_mm: Optional[int] = None
    camera_plan: List[CameraWindow] = field(default_factory=list)
    failed_take_rules: List[FailedTakeRule] = field(default_factory=list)


def check_render(contract: PromptContract, render_log: dict) -> dict:
    """
    Validate a render-log dict against a contract's failed-take rules.
    Returns {rule_name: 'pass' | 'fail' | 'unknown'} for each rule.
    'unknown' means the log_key was absent -- treat as unverified, not passing.
    """
    results = {}
    for rule in contract.failed_take_rules:
        raw = render_log.get(rule.log_key)
        if raw is None:
            results[rule.name] = "unknown"
        elif raw is True:   # bad condition present
            results[rule.name] = "fail"
        else:
            results[rule.name] = "pass"
    return results