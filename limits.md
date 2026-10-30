# Limits

Source: art_01M67ACYEDW3GH3RZKZRKQF0RN r1.

- Patterns match heuristic keywords; a section can pass with wrong wording that happens to hit the regex.
- `count_negative_items` reads only the first Avoid clause; a split clause will undercount.
- The 8/15/16/18 sequence was verified against synthetic stand-in prompts, not the original prompts (not reproduced).
- Weather-law pattern matches 'dust/smoke … fall/settle' but may miss exotic weather words.
- No audio, playback or rendering is checked; this is text structure only.
- Next improvement: add a positional check that the Avoid list is the last section, and flag an Avoid item that duplicates a beat description (which indicates a continuity failure was not fixed upstream).