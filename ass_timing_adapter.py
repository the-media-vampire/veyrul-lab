"""ASS timing adapter: quantization guard.

Mechanism: ASS centisecond resolution means floor(ms/10).
A word at [101, 104] ms -> both endpoints = 10 cs = 100 ms -> zero duration -> drop.
This adapter makes the policy explicit before conversion.

Source: art_01M6V2D44ND0QGWCJW3GWYSKXF r1 Case 9.
Fixture: rpl_01M6TVE4ZYHWK5D4FVKFS9ES21 (deterministic check, not reproduced here).
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional

CS = 10  # centisecond in ms

class CollapsePolicy(Enum):
    DROP   = "drop"    # discard zero-duration events (current observed behavior)
    CLAMP  = "clamp"   # extend end to start+1cs (SRT-style display fix)
    MERGE  = "merge"   # merge into adjacent word if available

@dataclass
class WordInterval:
    text: str
    start_ms: int
    end_ms: int

    @property
    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

def quantize(ms: int) -> int:
    """Floor to centisecond boundary (ASS resolution)."""
    return (ms // CS) * CS

def check_collapse(w: WordInterval) -> bool:
    """True if quantization produces zero duration."""
    return quantize(w.start_ms) == quantize(w.end_ms)

def adapt(
    words: List[WordInterval],
    policy: CollapsePolicy = CollapsePolicy.DROP,
) -> List[WordInterval]:
    """Apply collapse policy before ASS conversion."""
    out: List[WordInterval] = []
    for i, w in enumerate(words):
        if not check_collapse(w):
            out.append(w)
            continue
        # zero-duration after quantization
        if policy == CollapsePolicy.DROP:
            continue  # silent drop — matches observed converter behavior
        elif policy == CollapsePolicy.CLAMP:
            # extend quantized end by 1 centisecond
            q_start = quantize(w.start_ms)
            out.append(WordInterval(w.text, q_start, q_start + CS))
        elif policy == CollapsePolicy.MERGE:
            if out:  # extend previous word's end
                prev = out[-1]
                out[-1] = WordInterval(prev.text + " " + w.text,
                                       prev.start_ms, w.end_ms)
            elif i + 1 < len(words):  # pull into next
                pass  # next iteration will absorb
            else:
                continue  # nowhere to merge, drop
    return out

# --- Fixture from Case 9 ---
if __name__ == "__main__":
    fixture = WordInterval(text="test", start_ms=101, end_ms=104)
    print(f"Input: [{fixture.start_ms}, {fixture.end_ms}] ms, "
          f"duration={fixture.duration_ms} ms")
    print(f"Quantized: [{quantize(fixture.start_ms)}, {quantize(fixture.end_ms)}] ms")
    print(f"Collapses: {check_collapse(fixture)}")
    for policy in CollapsePolicy:
        result = adapt([fixture], policy)
        print(f"Policy={policy.value}: {result}")