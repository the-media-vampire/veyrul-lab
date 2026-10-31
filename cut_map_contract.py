from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Beat:
    t: float                  # timestamp in seconds
    music_event: str          # e.g. "kick", "snare", "hi-hat roll"
    camera_move: str          # e.g. "push in", "whip-pan", "orbit"
    cut_type: str             # e.g. "hard cut", "speed-ramp"
    direction: Optional[str] = None  # e.g. "toward", "backward", "clockwise"

@dataclass
class CutMapContract:
    audio_ref: str                         # fenced audio reference, e.g. "@Audio 1"
    fence_negatives: List[str]             # must include >= 3 negatives around the audio block
    genre: Optional[str]                   # stated once in the prompt
    tempo_bpm: Optional[int]               # stated once in the prompt
    world_head_count: Optional[int]        # declared cast size in world block
    clip_duration_s: float                 # declared clip length in seconds
    beats: List[Beat]                      # ordered list of timecoded beats
    final_pose_described: bool             # whether final pose is precisely described
    loopable_end: bool                     # whether loopable end is declared

def validate(c: CutMapContract) -> List[str]:
    """Return a list of authoring errors. Empty list = contract passes."""
    errs = []
    if not c.audio_ref.strip():
        errs.append("audio_ref empty")
    if len(c.fence_negatives) < 3:
        errs.append(f"need >= 3 fence negatives, got {len(c.fence_negatives)}")
    if not c.genre:
        errs.append("genre not stated")
    if c.tempo_bpm is None:
        errs.append("tempo_bpm not stated")
    if not c.beats:
        return errs + ["cut map has no beats"]
    for i in range(1, len(c.beats)):
        if c.beats[i].t <= c.beats[i-1].t:
            errs.append(
                f"beat {i} ({c.beats[i].t}s) not after beat {i-1} ({c.beats[i-1].t}s)"
            )
    for b in c.beats:
        if not (0 <= b.t <= c.clip_duration_s):
            errs.append(f"beat at {b.t}s outside declared duration {c.clip_duration_s}s")
        for attr in ("music_event", "camera_move", "cut_type"):
            if not getattr(b, attr, "").strip():
                errs.append(f"beat {b.t}s missing {attr}")
    no_dir = [b.t for b in c.beats if not b.direction]
    if no_dir:
        errs.append(
            f"camera direction unspecified for beats at {no_dir} "
            "(mismatch-3 risk: model may move toward instead of backward)"
        )
    if c.world_head_count is None:
        errs.append("world_head_count not declared (mismatch-1 risk: dancer count drift)")
    if not c.final_pose_described:
        errs.append("final pose not precisely described (mismatch-6 risk: arm count wrong)")
    if not c.loopable_end:
        errs.append("loopable_end not declared")
    return errs