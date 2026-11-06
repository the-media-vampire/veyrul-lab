# Integration contract: Mixxx workflow ↔ ChucK timed-loop

## Sources
- Mixxx: `art_01M6N9PCZTJSX3MA9442WEFFDX` revision 3 (source_inspected, not_run)
- ChucK: `art_01M6QCMFBB28W6PJMFEA3EKF9G` revision 1 (source_inspected, not_run)

## Interface table

| Interface point | Mixxx side | ChucK side | Mismatch / gap |
|---|---|---|---|
| Tempo unit | BPM float, set by SYNC / Sync Lock | Logical time `1::second`, `0.5::second` | Different units; need BPM→duration conversion: `dur beat = (60.0/bpm)::second` |
| Beat trigger | Beatgrid + QUANTIZE button | `=> now` advance inside shred | Mixxx triggers are UI/MIDI events; ChucK expects `spork`ed shred. Bridge: OSC or MIDI out from Mixxx, OSC in on ChucK |
| Termination model | Auto DJ playlist exhausted → stop | Bounded shred (counter loop) or unbounded shred | Unbounded ChucK shred + finite Mixxx playlist = zombie shred risk; needs explicit kill signal |
| Effect routing | FX unit 1-4, dry/wet mix knob, after faders | `dac => FX => dac` chain via `=>` and `=<` | Mixxx effects run inside the app; ChucK effects run in its own graph — cannot share audio graph without an external bus (e.g., JACK or virtual device) |
| Recording | Mixxx records main output by default; Start/Stop via UI or Options menu | No built-in recorder in staged files | Either route: (a) use Mixxx recorder exclusively, (b) route ChucK dac to virtual device Mixxx captures |
| Cue / intro detection | Analyzer places intro start at first sound above −60 dBFS | No cue detection in staged files | ChucK can replicate: poll `SinOsc.last()` threshold, but not demonstrated in sources |
| License | No license file staged; conf.py copyright 2011-2026 Mixxx Dev Team | License gap flagged in `rqr_01M6QD9G5ZTQ26GF3JWBGKRVQR` | Both unresolved; no redistribution conclusion drawn here |

## Critical assumptions
1. A MIDI or OSC bridge exists between Mixxx and ChucK — not documented in either source.
2. JACK or a virtual audio device is available to share the audio bus — untested.
3. BPM detected by Mixxx is accurate (manual states errors cause sync difficulty).
4. ChucK `1::second => now` accumulates no meaningful jitter at DJ timescales — unknown from sources.
5. Music rights rest with the operator; neither system asserts rights to tracks.

## Failure modes
- Mixxx beatgrid error → Sync Lock drifts → ChucK shred timing misaligned
- Zombie shred: Mixxx Auto DJ stops; ChucK unbounded shred keeps running
- Clipping: Mixxx gain + ChucK gain budget unsynchronized → red meters
- License gap in ChucK examples blocks redistribution of adapter patterns