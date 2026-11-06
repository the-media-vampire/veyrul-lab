# Picture-timecode → stable-audio-tools cue-request contract

## Status: untested proposal
Nothing has been run, generated or heard. This documents the interface seam only.

## Interface table

| Concept | Picture-side value | Model-side field | Type | Conversion | Source |
|---|---|---|---|---|---|
| Cue start | timecode (HH:MM:SS:FF) | `seconds_start` | int (0–512) | timecode_to_seconds(tc) cast to int | art_01M6H81MCK26G0HQBNQPA15WE9 rev 2 |
| Cue length | out_tc − in_tc in seconds | `seconds_total` | float (0–512) | timecode_to_seconds(out) − timecode_to_seconds(in) | art_01M6H81MCK26G0HQBNQPA15WE9 rev 2 |
| Mood/style | editorial brief | `prompt` | string | human-authored; hits not encoded here | art_01M6H81MCK26G0HQBNQPA15WE9 rev 2 |
| BPM for hit grid | chosen to place hits on integer frame boundaries | not a model field | — | used for prompt phrasing and post-edit only | art_01M6E4H6EE6PTQMRDD7RK3VJTY rev 1 |

## Timecode-to-seconds formula (from art_01M6E4H6EE6PTQMRDD7RK3VJTY rev 1 arithmetic)

```
seconds = HH*3600 + MM*60 + SS + FF/fps
```
If the reel has a 01:00:00:00 start offset, subtract 3600 before computing cue length.
For 23.976 vs 24 fps or 29.97 drop-frame, the drift is ~0.1% (≈2 frames/min); flag this as a risk.

## Example request (untested)

```python
# Cue: in=01:02:14:00, out=01:02:47:00, fps=24, fresh piece
in_tc  = 1*3600 + 2*60 + 14 + 0/24  # = 3734.0 s absolute
out_tc = 1*3600 + 2*60 + 47 + 0/24  # = 3767.0 s absolute

cue_length = out_tc - in_tc  # = 33.0 s
# seconds_start: for a fresh piece with no prior audio context, 0 is the
# documented example value. What a non-zero value means for a fresh cue
# is not stated in the docs (art_01M6H81MCK26G0HQBNQPA15WE9 rev 2).

request = {
    "prompt": "tense orchestral underscore, 120 BPM, no percussion drop",
    "seconds_start": 0,
    "seconds_total": cue_length,  # 33.0
}
```

## Stated limits (from docs, art_01M6H81MCK26G0HQBNQPA15WE9 rev 2)

- `seconds_start` range 0–512 (int conditioner); values are clamped.
- `seconds_total` range 0–512 (number conditioner, continuous Fourier embedding).
- Whether the range is a hard model limit for any released checkpoint is not stated.
- Hit points are not a model field; the prompt carries timing intent in natural language.
  Post-generation editing (extend/crop/replace-section) is the described fallback
  (art_01M6E4H6EE6PTQMRDD7RK3VJTY rev 1).

## Open interface questions (blockers before use)

1. **seconds_start semantics for a fresh cue**: docs show example value 22 without
   explaining what a non-zero start does for a piece with no prior audio. Untested.
2. **Model compliance with seconds_total**: whether the model reliably ends near the
   stated total is not documented at this commit. Untested.
3. **Model weights licence**: separate from the MIT repository licence; must be accepted
   on Hugging Face before use. Not read here.
4. **fps clock mismatch**: 23.976 vs 24 / drop-frame 29.97 drift must be resolved
   before computing cue length; ~2 frames/min error.
5. **Prompt-to-hit-point fidelity**: no field encodes a hit at bar 3 beat 1;
   natural-language prompting is the only mechanism described, and its reliability
   for hit placement is undocumented.