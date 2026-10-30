from dataclasses import dataclass, field
from typing import Literal, List
import json

# Sources:
#   Observed structure: art_01M64VKF6MVCCAAVV3YZS2A2TY r2
#   Timed-beat block:  art_01M67CGQR5M8AXXN18VH6Z4ETM r1 (block 5)

ShotKind = Literal["wide", "portrait", "two_shot"]

@dataclass
class Beat:
    label: str
    t: float          # approx start time in seconds
    kind: ShotKind
    chars: List[str] = field(default_factory=list)  # characters named (for continuity binding)

@dataclass
class BeatOrderContract:
    """Integration contract: wide -> portrait x>=2 -> wide/two_shot.

    Plug Beat instances into block 5 of a twelve-block prompt as
    timed-sequence entries. Each portrait beat must name at least one
    character so the continuity block (block 3) can bind state.
    """
    dur: float
    beats: List[Beat]

    def validate(self) -> List[str]:
        errs = []
        if not self.beats:
            return ["no beats defined"]
        if self.beats[0].kind != "wide":
            errs.append(f"opening must be 'wide', got '{self.beats[0].kind}'")
        if self.beats[-1].kind not in ("wide", "two_shot"):
            errs.append(f"closing must be 'wide' or 'two_shot', got '{self.beats[-1].kind}'")
        # Check for >=2 consecutive portrait beats in middle
        mid = self.beats[1:-1]
        runs, run = [], []
        for b in mid:
            if b.kind == "portrait":
                run.append(b.label)
            else:
                if run:
                    runs.append(run)
                    run = []
        if run:
            runs.append(run)
        if not any(len(r) >= 2 for r in runs):
            errs.append("need >=2 consecutive portrait beats in middle section")
        # Time ordering
        for i in range(1, len(self.beats)):
            if self.beats[i].t <= self.beats[i-1].t:
                errs.append(f"beat '{self.beats[i].label}' must start after '{self.beats[i-1].label}'")
        # Continuity: portrait beats must name a character
        for b in self.beats:
            if b.kind == "portrait" and not b.chars:
                errs.append(f"portrait beat '{b.label}': no character named (continuity gap)")
        return errs

    def to_contract(self) -> dict:
        return {
            "observed_in": "art_01M64VKF6MVCCAAVV3YZS2A2TY r2",
            "timed_beat_slot": "art_01M67CGQR5M8AXXN18VH6Z4ETM r1 block5",
            "structure": "wide -> portrait x>=2 -> wide/two_shot",
            "clip_duration_s": self.dur,
            "beats": [
                {"label": b.label, "t_s": b.t, "kind": b.kind, "chars": b.chars}
                for b in self.beats
            ],
            "assumptions": [
                "Model compliance with timed beats is unverified; compliance failures documented in art_01M67CGQR5M8AXXN18VH6Z4ETM r1.",
                "Portrait timing window ~9-14 s is descriptive, not a hard constraint.",
                "Two-shot satisfies the closing-wide slot.",
                "Four runs, no seed set; this encodes a description, not a proven rule.",
            ],
        }