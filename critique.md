# Tess critique of Forge preflight (5bc9c30b)

**Sources:** art_01M6F7TCQVEMH8F3CVTBBWF9V3 r2, art_01M5MDSVYME727XZZHF3QFYFYB r1
**Forge artifact:** 5bc9c30b-029d-408a-b5b8-df719a038fdb (source, not executed)

## What Forge gets right

- Contract table matches the tool's enforced rules (ValueError names are
  correct per r2 source inspection).
- Pause/silence event design correctly cited from r2.
- offset.py branch is flagged `execution=not_run` — honest.

## Unsafe assumptions I found

**A1 — Op1 rounding is stated, not enforced.**
Forge says `round(x * 1000 / 10) * 10` is "needed" but the decision tree
does not say *who* applies it. If the upstream agent passes raw float-seconds
without converting, the tool raises ValueError on the first word. The gate
must convert *before* the contract check, not after a failure.

**A2 — offset.py reliability is unestablished.**
The tree routes F4-type failures to offset.py, but that artifact
(art_01M6SNVGQ86GDSESP316R61M6Q r1) has execution=not_run. Using it as
a repair step treats an unexecuted script as a reliable tool. The tree should
read: "attempt offset.py; if exit 1 OR script untested, re-transcribe."

**A3 — Op2 cue-splitting is called a downstream concern, not a preflight gate.**
Forge defers sentence pre-splitting to the caller. That is correct, but the
decision tree gives no measurable criterion for *when* splitting is needed.
Without a character or word-count threshold, an agent cannot act mechanically.
Suggested gate: if any sentence word-span > 12 words or > 60 characters,
pre-split before calling tool.

**A4 — Boolean guard is listed in contract but not in the decision tree.**
If a caller passes `{"text": "hi", "start_ms": true, "end_ms": 500}`,
the tool raises ValueError. Op1 diagnosis should include a type-check step.

## Unresolved checks (not changed by this synthesis)

- Visual render quality: static tests are not video frames
  (art_01M6F7TCQVEMH8F3CVTBBWF9V3 r2, tag `not-rendered`).
- Font fallback, YCbCr Matrix=None, libass presence: unresolved per r2.
- Variable-speed drift: no tool in this record set handles it.
- WhisperX dictionary-excluded tokens: re-alignment or human review only
  (art_01M5MDSVYME727XZZHF3QFYFYB r1).

## Practical next step

A receiving agent should run fixtures F1–F5 (fixtures.jsonl) against
subtitle_workflow.py to confirm contract rejection/acceptance before
committing to a long run. This is a proposed test sequence, not an
executed one.