# SFZ Drum Kit Template

Structural template. Replace every `sample=` path with real files, then load in an SFZ player.

## Opcodes used and why

| Opcode | Scope | Purpose |
|---|---|---|
| `loop_mode=one_shot` | `<global>` | Play full sample; ignore note-off |
| `lovel`/`hivel` | `<region>` | Velocity layer bounds (0-31,32-63,64-95,96-127) |
| `amp_velcurve_N=1` | `<region>` | Full volume at layer ceiling; counteracts default velocity tracking |
| `seq_length` | `<group>` | Total round-robin count per instrument |
| `seq_position` | `<region>` | Which take this region belongs to |
| `key` | `<group>` | MIDI note (GM: kick=36, snare=38, hihat=42) |

## Verification steps (manual, requires real samples)

1. Trigger each key at velocities 10, 45, 80, 110. Expect four distinct loudness levels.
2. Trigger the same key repeatedly at one velocity. Expect takes to rotate in order, not repeat.
3. Trigger and release quickly. Expect the full sample to finish (one_shot).

## Limits

- Not loaded or auditioned; structural correctness only.
- `amp_velcurve_N` with N=hivel: what `=1` means internally is not explained in the source tutorial (gap noted in art_01M6QBKFBG0E8B1KC9NQBY5RJV r1).
- `lorand`/`hirand` random variant excluded; hi-hat articulations excluded.
- No tuning, pan or release opcodes.
- Fourth velocity layer omits `hivel` relying on default=127 (as documented in source).