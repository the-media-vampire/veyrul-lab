"""frame_audit/v1 — post-generation continuity observation log.

Complements prompt_continuity_lint (artifact 485ad4fc) which covers
R1-R4 pre-submission.  This schema adds R-timing and R-orientation,
which require sampled stills, not prompt text.

Source: art_01M68DNWCQ5SYGVT7KQXH69M0Y rev 1 (MIT, redistribution permitted).
Execution confirmed: run_python artifact 2c06a03f, exit 0.
"""

import json

# Rule IDs shared with linter R1-R4; R-timing and R-orientation are new.
RULE_IDS = ["R1", "R2", "R3", "R4", "R-timing", "R-orientation"]
STATUSES = {"MATCH", "MISMATCH", "AMBIGUOUS", "NOT_VERIFIED"}


def frame_audit_record(
    prompt_source_id: str,
    clip_ref: str,
    frame_id: str,
    shot_label: str | None,
    rule_observations: list[dict],
    auditor: str,
) -> dict:
    """Return a single frame-audit record dict.

    Args:
        prompt_source_id: Veyrul record ID + revision, e.g.
            'art_01M68DNWCQ5SYGVT7KQXH69M0Y rev 1'.
        clip_ref:   Project reference, e.g. 'HF-PKG-022'.
        frame_id:   Stable frame identifier, e.g. 'frame_0031'.
        shot_label: Prompt shot label if known, else None.
        rule_observations: List of {rule_id, status, note}.
            rule_id must be in RULE_IDS.
            status must be in STATUSES.
        auditor: Who or what produced this record.

    Returns:
        dict conforming to frame_audit/v1 schema.

    Raises:
        ValueError on unknown rule_id or status.
    """
    bad_rules = [o["rule_id"] for o in rule_observations
                 if o["rule_id"] not in RULE_IDS]
    bad_statuses = [o["status"] for o in rule_observations
                    if o["status"] not in STATUSES]
    if bad_rules:
        raise ValueError(f"Unknown rule IDs: {bad_rules}. Valid: {RULE_IDS}")
    if bad_statuses:
        raise ValueError(f"Unknown statuses: {bad_statuses}. Valid: {STATUSES}")

    return {
        "schema": "frame_audit/v1",
        "prompt_source_id": prompt_source_id,
        "clip_ref": clip_ref,
        "frame_id": frame_id,
        "shot_label": shot_label,
        "rule_observations": rule_observations,
        "auditor": auditor,
        "note": (
            "Stills only; motion, cuts and audio are not observable "
            "from sampled frames."
        ),
    }


def to_json(record: dict, **kwargs) -> str:
    return json.dumps(record, **kwargs)