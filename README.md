# Tempo Unit Drift: Onset Delta Measurement

**Companion to:** artifact `7a9c0adc` (Scout, Tempo Unit Drift Experiment Brief)  
**Source record:** `art_01M6N8TZAG0W6TZJ6X4N3QKXP7` revision 2  
**Status:** Source only. Not executed.

## Purpose

Turns Scout's two-condition brief into a runnable measurement. Given two
pre-rendered audio files (one per condition), `measure_onset_delta.py` outputs
a CSV of per-bar onset deltas in milliseconds, directly filling the
`results_log.md` template from artifact `7a9c0adc`.

## What you need

1. Two `.wav` files: one FoxDot render at 120 BPM, one Strudel render.
   - Condition A: Strudel `setcpm 60`
   - Condition B: Strudel `setcpm 30`  
   Run the script once per condition; rename `TARGET_WAV` accordingly.
2. Python 3.9+ with `librosa>=0.9`, `numpy`, `soundfile`.

## Failure modes to log

| Failure | Signal | Recovery |
|---|---|---|
| `ImportError` | Missing dependency | `pip install librosa numpy soundfile` |
| `WARNING: Only N bars` | Audio too short or onset detection missed beats | Increase audio length; check kick loudness |
| Both conditions produce identical CSV | Render paths swapped | Verify file identity with `sha256sum` |

## Separation of observations vs. taste

The script outputs **delta_ms only** — a measurement.  
Whether a given delta is *tolerable live* is a separate judgment; do not
enter it into this CSV. Use Scout's `results_log.md` notes column for that.

## Known limitation

librosa onset detection assumes a clean, loud transient on beat 1. If the
kick is quiet or masked, onsets will be missed and bar alignment will slip.
Log any missed-onset warnings; they are part of the trial record.