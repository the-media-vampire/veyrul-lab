"""video-use EDL rule checker.
Checks hard rules from art_01M6A85SJY0G5TRQ3EM89Q67VW r1.
No ffmpeg, ElevenLabs, or footage required.

EDL schema (dict):
  subtitle_pass_last: bool           # subtitles must be last global step
  concat_strategy: str               # must be 'lossless_copy_concat'
  segments: list of dicts:
    cut_start_ms / word_start_ms     # leading pad (30–200 ms)
    cut_end_ms   / word_end_ms       # trailing pad (30–200 ms)
    audio_fade_ms                    # minimum 30 ms
    subtitles_after_overlays: bool   # True = subtitles after all overlays
    overlays: list of dicts:
      id: str
      frame_0_offset_ms: int         # must be 0

Usage:
  from edl_rule_check import check_edl
  violations = check_edl(my_edl_dict)
  if violations:
      for v in violations:
          print('VIOLATION:', v)
"""

MIN_PAD_MS = 30
MAX_PAD_MS = 200
MIN_FADE_MS = 30
REQUIRED_CONCAT = "lossless_copy_concat"


def check_edl(edl: dict) -> list:
    """Return list of violation strings; empty means clean."""
    violations = []
    segments = edl.get("segments", [])

    for i, seg in enumerate(segments):
        sid = f"segment[{i}]"

        # Word-pad: leading edge
        cs = seg.get("cut_start_ms")
        ws = seg.get("word_start_ms")
        if cs is not None and ws is not None:
            pad = ws - cs
            if pad < MIN_PAD_MS:
                violations.append(
                    f"{sid}: leading pad {pad}ms < {MIN_PAD_MS}ms (cuts inside or too close to word)"
                )
            if pad > MAX_PAD_MS:
                violations.append(
                    f"{sid}: leading pad {pad}ms > {MAX_PAD_MS}ms maximum"
                )

        # Word-pad: trailing edge
        ce = seg.get("cut_end_ms")
        we = seg.get("word_end_ms")
        if ce is not None and we is not None:
            pad = ce - we
            if pad < MIN_PAD_MS:
                violations.append(
                    f"{sid}: trailing pad {pad}ms < {MIN_PAD_MS}ms (cuts inside or too close to word)"
                )
            if pad > MAX_PAD_MS:
                violations.append(
                    f"{sid}: trailing pad {pad}ms > {MAX_PAD_MS}ms maximum"
                )

        # Audio fade
        fade = seg.get("audio_fade_ms", 0)
        if fade < MIN_FADE_MS:
            violations.append(
                f"{sid}: audio_fade_ms={fade} (must be >= {MIN_FADE_MS})"
            )

        # Subtitle ordering within segment
        if not seg.get("subtitles_after_overlays", True):
            violations.append(
                f"{sid}: subtitles_after_overlays=False "
                "(subtitles must come after all overlays in filter chain)"
            )

        # Overlay frame alignment
        for ov in seg.get("overlays", []):
            offset = ov.get("frame_0_offset_ms", 0)
            if offset != 0:
                violations.append(
                    f"{sid} overlay '{ov.get('id', '?')}': "
                    f"frame_0_offset_ms={offset} (must be 0; frame 0 must land at window start)"
                )

    # Global: subtitle pass ordering
    if not edl.get("subtitle_pass_last", False):
        violations.append(
            "global: subtitle_pass_last is not True "
            "(subtitles must be the final filter step globally)"
        )

    # Global: concat strategy
    concat = edl.get("concat_strategy", "")
    if concat and concat != REQUIRED_CONCAT:
        violations.append(
            f"global: concat_strategy='{concat}' "
            f"(must be '{REQUIRED_CONCAT}', not a single filtergraph pass)"
        )

    return violations


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Usage: python edl_rule_check.py edl.json")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        edl = json.load(f)
    issues = check_edl(edl)
    if not issues:
        print("OK: no rule violations found")
    else:
        for v in issues:
            print("VIOLATION:", v)
        sys.exit(2)