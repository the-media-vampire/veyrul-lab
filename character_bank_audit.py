"""character_bank_audit.py — provenance-audit layer for MovieAgent character bank.
Source: art_01M6HQ3ZP3450N3AHCA0N7XAJ1 rev 1 (Wu, Zhu & Shou, arXiv:2503.07314v1, CC BY 4.0)
Companion to: Theo artifact 04c3112c, commit 09dec496 (MIT)
Source-published, not executed. Audio/voice held per source record.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class CharacterBankEntry:
    """Minimum fields named in paper §3.1. Audio slot intentionally absent (held)."""
    canonical_name: str        # single authoritative form, e.g. 'Dr. Mira'
    role_label: str            # e.g. 'lighthouse keeper'
    portrait_image_slot: str   # path or placeholder; content not inspected here
    confirmed_bases: list[str] = field(default_factory=list)
    # Leave empty until checkpoint-compatibility matrix supplied from upstream.
    # Gap: github.com/showlab/MovieAgent not fetched; schema is inferred from paper text.


def normalise_name(raw: str) -> str:
    """Canonical form: strip, collapse spaces, title-case.
    Catches 'Dr.  Mira' vs 'Dr. Mira' vs 'dr mira'."""
    return " ".join(raw.strip().split()).title()


def audit_bank(entries: list[CharacterBankEntry]) -> list[str]:
    """Return provenance warnings; empty list = no gaps found."""
    warnings: list[str] = []
    seen: dict[str, int] = {}
    for i, e in enumerate(entries):
        norm = normalise_name(e.canonical_name)
        if norm != e.canonical_name:
            warnings.append(
                f"[PC-NAME] Entry {i}: '{e.canonical_name}' normalises to '{norm}'."
            )
        if norm in seen:
            warnings.append(f"[PC-DUP] Entry {i}: duplicate name '{norm}' (also index {seen[norm]}).")
        seen[norm] = i
        if not e.confirmed_bases:
            warnings.append(
                f"[PC-02] Entry {i} ('{e.canonical_name}'): confirmed_bases empty — "
                "base checkpoint compatibility not established. Do not pass to generator."
            )
    return warnings


def cross_check_shot(shot_characters: list[str],
                     bank: list[CharacterBankEntry]) -> list[str]:
    """Return names in a shot entry with no matching bank entry (normalised).
    Companion to Theo's validate_plan(); catches silent identity drift."""
    bank_names = {normalise_name(e.canonical_name) for e in bank}
    return [n for n in shot_characters if normalise_name(n) not in bank_names]