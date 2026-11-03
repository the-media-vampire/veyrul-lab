# adapter_sketch.py -- proposal only, not run
# Connects Agents' Room scratchpad to a Re3-style scene-draft loop.
# Source: art_01M6H154J7KBB907MQWZ73VV2F r2 (CC BY 4.0 paraphrase). MIT.

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Scratchpad:
    """Agents' Room shared memory."""
    entries: Dict[str, str] = field(default_factory=dict)

    def write(self, label: str, text: str) -> None:
        self.entries[label] = text

    def as_context_prefix(self) -> str:
        """Flatten to text prefix a Re3 drafter can consume."""
        return "\n\n".join(
            f"[{k.upper()}]\n{v}" for k, v in self.entries.items()
        )


def scratchpad_to_scene_list(scratchpad: Scratchpad) -> List[str]:
    """
    ASSUMPTION: 'plot' entry is newline-separated scene summaries.
    Untested; actual prompt templates (appendix) were not opened.
    Raises ValueError if 'plot' is absent.
    """
    plot_text = scratchpad.entries.get("plot", "")
    if not plot_text:
        raise ValueError("No 'plot' entry; cannot build scene list.")
    return [line.strip() for line in plot_text.splitlines() if line.strip()]


def re3_draft_loop(
    scenes: List[str],
    context_prefix: str,
    llm_call,          # caller supplies; stub shown below
) -> List[str]:
    """One LLM call per scene, prepending accumulated context."""
    drafted: List[str] = []
    running_ctx = context_prefix
    for scene in scenes:
        prompt = f"{running_ctx}\n\nWrite scene: {scene}"
        draft = llm_call(prompt)        # replace with real call
        drafted.append(draft)
        running_ctx += "\n" + draft
    return drafted


# --- minimal smoke test (no LLM) ---
if __name__ == "__main__":
    sp = Scratchpad()
    sp.write("conflict", "Two siblings contest their mother's estate.")
    sp.write("character", "Maya: pragmatic eldest. Luca: idealistic youngest.")
    sp.write("plot", "Maya discovers hidden will.\nLuca confronts Maya.\nReconciliation at graveside.")

    scenes = scratchpad_to_scene_list(sp)
    prefix = sp.as_context_prefix()
    drafts = re3_draft_loop(scenes, prefix, llm_call=lambda p: f"[STUB: {p[:40]}...]")

    for i, d in enumerate(drafts):
        print(f"Scene {i+1}: {d[:80]}")