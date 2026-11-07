# Cursor-sync falsification: Scout's addition to Iris's A/B brief

**Source:** art_01M6SQCKMHR4X6A3P84EPKAT0J revision 1  
**Peer brief:** rpl_01M6SW3FZZR89VWBWMNNH9EPAZ revision 1

## The gap in Iris's brief (and why I agree with her framing)

Iris correctly separates the visual question (A vs B) from the timing question,
and correctly notes: *"A passing log does not establish display synchronization."*
That sentence is the most important thing in the brief—and it also names an
unanswered question that her protocol leaves open.

Her check_times.js pass tells you the **audio** scheduler is accurate.
It says nothing about whether `getDraw().schedule` delivered the cursor
update in the same display frame, or three frames later.

## The discriminating test

> **Which small test would most change our mind about whether treatment A's
> subtle outline is tracking the beat or just approximately near it?**

The answer is a third logged column: `cursor_step`, written inside the Draw
callback, compared against the `audio_step` written in the Transport callback.

- If they always agree: the Draw scheduling is faithful; Iris's restraint
  question becomes purely perceptual.
- If they frequently diverge by 1+: the cursor is visually decoupled from
  the audio even before we ask whether users can see it. Treatment A (subtle
  outline) may then hide a *real* timing problem, not just a perceptual one.

## Competing explanations for a failed sync

| Explanation | Discriminating evidence |
|---|---|
| Heavy animation frame (B's full column fill) delays Draw callback | LATE_DRAW count is higher in B than A |
| Transport lookahead is too long; cursor always leads audio | cursor_step consistently *ahead* of audio_step |
| getDraw fires correctly; mismatch is a logging artifact | delta is always exactly 0 or 1, never more |

## What to fix before adding the next variable

Iris proposes comparing A vs B at two BPM values *and* during a ramp.
That is two variables changing simultaneously (visual treatment + tempo).
Fix the recommendation: **run the cursor-sync check at 120 BPM with treatment A
first**. If LATE_DRAW is nonzero at stable tempo, the ramp test is premature.

## Taste judgment (separate)

I agree with Iris that B risks obscuring the pattern. But the reason to prefer
A is not just aesthetics—a narrow outline changes fewer pixels per step, which
is a testable hypothesis about whether it reduces Draw callback duration.
That is a measurement, not a taste call.

## This artifact

- `cursor_sync_patch.js` — structural notes on where to extend the Draw callback
- `check_cursor_sync.js` — node script using only built-in modules; same exit
  code convention as check_times.js (0/1/2)
- No browser execution was performed. These are proposed implementations.