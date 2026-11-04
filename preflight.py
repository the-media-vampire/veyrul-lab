"""Preflight checker for Story2Board → StorySync prompt hand-off.

MIT License. No model calls; validates the prompt-level contract only.
Inputs are the outputs of Story2Board's LLM split step.
"""
from __future__ import annotations
import re


def check_handoff(
    reference_prompt: str,
    scene_prompts: list[str],
    *,
    warn_multi_subject: bool = True,
) -> dict:
    """Validate that scene_prompts are safe to pass to StorySync.

    Returns a dict with keys:
        ok: bool
        errors: list[str]
        warnings: list[str]
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not reference_prompt.strip():
        errors.append("reference_prompt is empty")

    if not scene_prompts:
        errors.append("scene_prompts is empty")

    # Contract rule 1: character token echo
    # Use the first noun phrase of reference_prompt as the anchor token.
    anchor = reference_prompt.strip().split()[0].lower().rstrip(",.;:") if reference_prompt.strip() else ""
    for i, sp in enumerate(scene_prompts):
        if anchor and anchor not in sp.lower():
            errors.append(
                f"scene_prompts[{i}] does not contain anchor token "
                f"'{anchor}' from reference_prompt; character token drift."
            )

    # Contract rule 3: multi-subject flag
    if warn_multi_subject:
        # Naive heuristic: count capitalized proper-noun-like tokens
        cap_tokens = re.findall(r'\b[A-Z][a-z]+\b', reference_prompt)
        if len(cap_tokens) >= 2:
            warnings.append(
                f"reference_prompt contains {len(cap_tokens)} capitalized tokens "
                "({' '.join(cap_tokens)}); Story2Board propagates entanglement "
                "rather than fixing it — inspect panels with two or more named subjects."
            )

    # Strip storyboard wrapper if present (rule 2)
    cleaned: list[str] = []
    wrapper_re = re.compile(
        r'A storyboard of .+? \(top\) and (.+?) \(bottom\)', re.IGNORECASE
    )
    for sp in scene_prompts:
        m = wrapper_re.search(sp)
        cleaned.append(m.group(1).strip() if m else sp)

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "cleaned_scene_prompts": cleaned,
    }


if __name__ == "__main__":
    import json
    # Example: fox cub character from art_01M6JVA6953NB4JPRSYWSK7AW5 rev 1 sketch
    ref = "a small fox cub wearing a red scarf"
    scenes = [
        "A storyboard of a small fox cub wearing a red scarf (top) and the fox cub sitting by a river (bottom)",
        "A storyboard of a small fox cub wearing a red scarf (top) and the fox cub running through snow (bottom)",
        "the wolf stands in the forest",  # deliberate drift: missing anchor
    ]
    result = check_handoff(ref, scenes)
    print(json.dumps(result, indent=2))