# Word-highlighted captions: preflight decision tree

Sources: art_01M6F7TCQVEMH8F3CVTBBWF9V3 r2, art_01M6SNVGQ86GDSESP316R61M6Q r1, art_01M5MDSVYME727XZZHF3QFYFYB r1.

## Minimal input contract (gate before all four operations)

| Field | Requirement |
|---|---|
| `duration_ms` | Positive int, multiple of 10 ms |
| `width`, `height` | Positive integers |
| `words` | Non-empty array, ordered, non-overlapping |
| `text` | Non-blank; no backslash, CR, LF, NUL, surrogate |
| `start_ms`/`end_ms` | Integer; `0 <= start < end <= duration`; multiples of 10 ms |
| Boolean guard | `true`/`false` rejected as integers; validate types explicitly |

Adjacent words allowed. Tool does not sort, round, or extend times.

## Decision tree

**Step 1 — Contract valid?** (check all fields above)

- NO → **Op 1 failure: timestamp acquisition**
  - Missing start/end on words → WhisperX drops timing for out-of-dict chars (numbers, currency) [art_01M5MDSVYME727XZZHF3QFYFYB r1]; re-align or ask for missing evidence
  - Out-of-order or overlapping → ASR or post-sort bug; fix before proceeding
  - Times not multiples of 10 ms → convert seconds→ms with explicit rounding
  - No words array → upstream transcription failed entirely

- YES → Run `subtitle_workflow.py`

**Step 2 — Tool exits 0?**

- NO → Inspect error message; it names the violated field. Fix JSON, not tool.
- YES → ASS written. Continue to ops 2–4.

**Op 2 — Cue splitting**
- Tool emits one full sentence per Dialogue event. No auto line-break or size-to-fit.
- Style (DejaVu Sans, bottom-centre) is declared, NOT measured [art_01M6F7TCQVEMH8F3CVTBBWF9V3 r2].
- Fix: pre-split input JSON into shorter sentence groups before calling tool.
- Unresolved: renderer-specific wrap behaviour untested.

**Op 3 — Timing after edits/cuts**
- Tool accepts times as given; cannot detect a shifted timebase.
- If audio was trimmed after transcription: run `offset.py` [art_01M6SNVGQ86GDSESP316R61M6Q r1] to measure constant offset, then adjust JSON times.
- If `offset.py` exits 1 → no reliable offset; re-transcribe edited audio.
- Unresolved: art_01M6SNVGQ86GDSESP316R61M6Q r1 execution=not_run. Variable-speed drift unhandled.

**Op 4 — Rendering / highlighting**
- Static tests verified ASS tag structure against parsed timestamps only — NOT video frames.
- Unresolved: font presence/fallback, glyph coverage, YCbCr Matrix=None, contrast in actual player pipeline, FFmpeg requiring libass.
- Action: validate with target renderer on a short clip before long run.

## When to reuse vs. act otherwise

| Situation | Action |
|---|---|
| Valid JSON, no audio edits | Reuse `subtitle_workflow.py` directly |
| Missing timestamps on words | Re-align; do not pass partial JSON |
| Audio trimmed after transcription | Run `offset.py`, fix JSON times, then tool |
| Long sentences overflowing | Pre-split JSON into sentence groups |
| Visual quality uncertain | Test in target renderer; static pass ≠ visual pass |

## Unresolved checks (explicit)

1. Word-timestamp quality: not established by ASS tool tests (different system)
2. Visual render quality: tags checked against parsed data only, not frames
3. Font: DejaVu Sans declared; install/fallback unverified
4. Variable-speed timebase drift: unhandled
5. `offset.py`/`cuts.py`: execution=not_run in source record