# Tempo Unit Drift: Discriminating Experiment Brief

**Source:** `art_01M6N8TZAG0W6TZJ6X4N3QKXP7` revision 2  
**Status:** Untested proposal — nothing run here

## The question that most changes our mind

> When you set "120 BPM" in FoxDot and attempt to match that rate in Strudel or TidalCycles using their native cycle-based defaults, does the pattern arrive in phase or does it drift?

If it **stays in phase**: the unit difference is cosmetic; a simple numeric conversion is enough for handoffs.  
If it **drifts**: the unit mismatch is a first-class production problem, not a documentation quirk.

## Why this is the informative test

`art_01M6N8TZAG0W6TZJ6X4N3QKXP7` rev 2 documents four tempo unit styles across six tools and explicitly declines to convert cycles-to-beats (unknown mapping). That gap means every practitioner who hands a loop between tools faces an untested assumption. This brief makes that assumption testable.

## Two conditions (all other variables fixed)

| Variable | Condition A — beats anchor | Condition B — cycle anchor |
|---|---|---|
| Reference tool | FoxDot at 120 BPM (record-stated default) | TidalCycles at 0.5625 cps (record-stated default, 135 BPM equiv per record) |
| Target tool | Strudel `setcpm 60` (1 cps interpretation) | Strudel `setcpm 30` (0.5 cps / 2s cycle interpretation) |
| Pattern | Single kick on beat 1 of a 4-beat loop | Same 4-event pattern |
| Measurement | Clock-align both engines to an external click; record onset times | Same |

Both Strudel defaults come from the same record ("30 cpm" vs "1 cps") — testing both surfaces which documentation statement corresponds to real tool behaviour.

## Pre-run checklist

- [ ] Confirm FoxDot 120 BPM default by reading `Player._dur` in a live session
- [ ] Confirm Strudel's actual startup cpm by evaluating `getCpm()` before any `setcpm` call
- [ ] Confirm TidalCycles `setcps` default by checking BootTidal.hs startup value
- [ ] Record onset timestamps (e.g. MIDI clock or DAW clip grid) for at least 8 cycles/bars
- [ ] Hold constant: audio interface, OS scheduler priority, no other CPU load

## What to log

See `results_log.md` for the template.

## Taste vs observation boundary

- **Observation:** measured onset delta in ms between the two engines at bar 4 and bar 8
- **Taste:** whether a drift of <5 ms is tolerable in a live set context (subjective; note separately)