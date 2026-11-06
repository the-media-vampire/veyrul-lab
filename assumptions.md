# Assumptions and failure modes

## What this contract assumes (not observed, not tested)

- ChucK executes `spork ~` to launch concurrent shreds sharing the audio graph.
  This is *not* demonstrated in the four source files; it is a standard ChucK
  pattern inferred from public documentation (not verified here).
- `Gain` nodes sum their inputs; two branches into `master` will mix, not replace.
- `s =< sinBranch` disconnects before the SinOsc goes out of scope; if ChucK
  garbage-collects `s` before explicit disconnect, the disconnect is redundant but harmless.

## Failure modes when combining

| Failure | Trigger | Signal |
|---------|---------|--------|
| Clipping | micBranch + sinBranch gains exceed master budget | Distortion at dac |
| Zombie shred | Infinite loop shred not removed before exit | Process hangs |
| Timing drift | Chained `=> now` advances accumulate scheduling latency | Clock print drifts |
| License gap | Example files not covered by MIT/GPL2+ declaration | Redistribution risk |

## Interface boundary: what ChucK exposes vs. what is hidden

Exposed: `=>`, `=<`, `now`, `second`, `ms`, `<<<`, `>>>`, `spork ~`.
Hidden: audio buffer size, sample rate, OS scheduling policy, actual latency.
Any workflow combining ChucK with an external DAW or OSC controller must negotiate
these hidden parameters explicitly.