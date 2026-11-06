"""Prompt-state coverage auditor for AI book-trailer shot prompts.

Distinct role in the pipeline:
- acda5f8b: per-record field-format gate (pre-authoring)
- ad06e2e2: cross-shot sequence gate (post-ledger)
- THIS:     prompt-vs-ledger coverage gate (pre-render)

Source basis:
  art_01M6H5ADPZ1P46TM3CRGGYVTJK r3, Stage 3:
    'first-frame rules as states a still can show'
    'check the first still before rendering or judging a long take'
  art_01M6A19D9WCBJFN6YNNXNTP570 r2:
    colour-state rule slipped between prompt and output stills.

Limits:
  - Checks token presence, not semantic accuracy.
  - Exact-string match; paraphrases miss. Same weakness as ad06e2e2 costume_note.
  - Does not query the engine; audits the authored prompt only.
  - scene_break=True shots are still audited (scene openers need states too).

What would disprove the coverage claim:
  A prompt that passes this audit but still produces a first-frame state
  violation in sampled output stills.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class ShotRecord:
    shot_id: str
    character: str
    location: str
    costume_note: str
    status: str = 'draft'
    scene_break: bool = False


@dataclass
class CoverageResult:
    shot_id: str
    covered: List[str] = field(default_factory=list)
    missing: List[str] = field(default_factory=list)

    @property
    def ratio(self) -> float:
        total = len(self.covered) + len(self.missing)
        return len(self.covered) / total if total else 0.0

    @property
    def passed(self) -> bool:
        return len(self.missing) == 0

    def __str__(self) -> str:
        status = 'PASS' if self.passed else 'FAIL'
        return (
            f"{self.shot_id} [{status}] coverage={self.ratio:.0%} "
            f"covered={self.covered} missing={self.missing}"
        )


# Required ledger terms that must appear (case-insensitive) in the prompt.
_REQUIRED_FIELDS = ('character', 'location', 'costume_note')


def audit_prompt(shot: ShotRecord, prompt: str) -> CoverageResult:
    """Return which ledger-mandated terms appear in the prompt text."""
    result = CoverageResult(shot_id=shot.shot_id)
    prompt_lower = prompt.lower()
    checks = {
        'character': shot.character,
        'location': shot.location,
        'costume_note': shot.costume_note,
    }
    for field_name, value in checks.items():
        # Accept any token from the value appearing in the prompt.
        tokens = [t.lower() for t in value.split() if len(t) > 2]
        hit = any(tok in prompt_lower for tok in tokens) if tokens else False
        if hit:
            result.covered.append(field_name)
        else:
            result.missing.append(field_name)
    return result


def audit_sequence(shots_and_prompts: List[tuple]) -> List[CoverageResult]:
    """Audit a list of (ShotRecord, prompt_str) pairs. Returns one result per shot."""
    return [audit_prompt(shot, prompt) for shot, prompt in shots_and_prompts]