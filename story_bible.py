# Source: art_01M6HGFBNCDERMNM02HZPN7SYE rev 1 (Make-A-Story arXiv 2211.13319v3, CC0 1.0)
from dataclasses import dataclass, field

@dataclass
class SceneEntry:
    scene_id: int
    story_text: str
    carried_characters: list[str]   # recurring; paper: kept by sentence-similarity weight
    new_characters: list[str]       # introduced; no separate paper rule
    setting: str                    # "same" | "changed: <desc>"
    reference_map: dict[str, str]   # case-sensitive token -> name; paper: memory resolves

@dataclass
class StoryBible:
    title: str
    scenes: list[SceneEntry] = field(default_factory=list)

    def add_scene(self, e: SceneEntry) -> None:
        self.scenes.append(e)

    def baseline_prompt(self, scene_id: int) -> str:
        """Raw story text only. Use as drift baseline."""
        return self._get(scene_id).story_text

    def carry_over_prompt(self, scene_id: int) -> str:
        """Prompt with resolved references and carry-over injected."""
        e = self._get(scene_id)
        text = e.story_text
        for token, name in e.reference_map.items():
            text = text.replace(token, name)
        parts = [f"Scene {e.scene_id}. {text}"]
        if e.carried_characters:
            parts.append("Carry forward: " + "; ".join(e.carried_characters) + ".")
        if e.new_characters:
            parts.append("Introduce: " + "; ".join(e.new_characters) + ".")
        parts.append(
            "Same setting as previous scene."
            if e.setting.startswith("same")
            else "New setting: " + e.setting.removeprefix("changed: ") + "."
        )
        return " ".join(parts)

    def validate(self) -> list[str]:
        """Flag unresolved pronouns (case-insensitive) and missing settings."""
        PRONOUNS = {"he","she","they","him","her","them","his","their"}
        out = []
        for s in self.scenes:
            resolved = {k.lower() for k in s.reference_map}
            words = {w.strip('.,!?').lower() for w in s.story_text.split()}
            unresolved = sorted(PRONOUNS & words - resolved)
            if unresolved:
                out.append(f"Scene {s.scene_id}: unresolved {unresolved}")
            if not s.setting:
                out.append(f"Scene {s.scene_id}: setting missing")
        return out

    def _get(self, scene_id: int) -> SceneEntry:
        for s in self.scenes:
            if s.scene_id == scene_id:
                return s
        raise KeyError(scene_id)