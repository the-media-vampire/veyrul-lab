"""Minimal adapter: parse a rose-window run descriptor and validate
required fields against the staging contract.

This is a schema-checking stub, not an execution harness.
No model calls, no frame reading; inputs are human-supplied metadata.
"""
from dataclasses import dataclass, field
from typing import Literal, Optional

OpeningFigure = Literal["tiny", "standing_pair", "two_silhouettes", "unknown"]
TerminalPhase = Literal["silhouette_bend", "absent", "unknown"]
Provenance = Literal["confirmed", "unconfirmed", "unknown"]


@dataclass
class RoseWindowRun:
    run_id: str
    opening_figure: OpeningFigure
    linked_image: bool
    linked_video: bool
    likeness_hold: bool       # prompt requests face/colour match
    medium_only: bool         # prompt requests medium only
    terminal_phase: TerminalPhase
    audio_reviewed: bool
    seed: Optional[int]
    provenance_image: Provenance
    provenance_video: Provenance
    notes: str = ""

    def gaps(self) -> list[str]:
        """Return a list of unresolved interface gaps for this run."""
        g = []
        if not self.audio_reviewed:
            g.append("audio_reviewed=False: audio not checked")
        if self.seed is None:
            g.append("seed=None: cannot separate seed from asset variance")
        if self.provenance_image != "confirmed":
            g.append(f"provenance_image={self.provenance_image}: rights basis unresolved")
        if self.linked_video and self.provenance_video != "confirmed":
            g.append(f"provenance_video={self.provenance_video}: rights basis unresolved")
        if self.likeness_hold and self.medium_only:
            g.append("likeness_hold and medium_only both True: prompt contradiction")
        return g


# -- Example: populate from art_01M64VKK2MPWCZP03XDVGKHM5S r2 observations --
if __name__ == "__main__":
    runs = [
        RoseWindowRun(
            run_id="exp_candidate_1",
            opening_figure="tiny",
            linked_image=True,
            linked_video=False,
            likeness_hold=False,
            medium_only=True,
            terminal_phase="unknown",  # not reported in article
            audio_reviewed=False,
            seed=None,
            provenance_image="unconfirmed",
            provenance_video="unknown",
        ),
        RoseWindowRun(
            run_id="exp_candidate_2",
            opening_figure="standing_pair",
            linked_image=True,
            linked_video=True,
            likeness_hold=True,
            medium_only=False,
            terminal_phase="silhouette_bend",
            audio_reviewed=False,
            seed=None,
            provenance_image="unconfirmed",
            provenance_video="unconfirmed",
        ),
        RoseWindowRun(
            run_id="exp_candidate_3",
            opening_figure="two_silhouettes",
            linked_image=True,
            linked_video=True,
            likeness_hold=True,
            medium_only=False,
            terminal_phase="silhouette_bend",
            audio_reviewed=False,
            seed=None,
            provenance_image="unconfirmed",
            provenance_video="unconfirmed",
        ),
    ]
    for r in runs:
        print(f"\n{r.run_id}")
        g = r.gaps()
        print(f"  gaps ({len(g)}):")
        for item in g:
            print(f"    - {item}")