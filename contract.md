# ChucK Mechanism Integration Contract

Source: art_01M6QCMFBB28W6PJMFEA3EKF9G revision 1 (curator reading, not tested).
License note: ChucK README lines 130-131 declare dual MIT/GPL2+ for *source code*;
whether examples are covered is not stated in the source record.

## Interface Table

| Mechanism | File | Input | Output | Advance? | Termination |
|-----------|------|-------|--------|----------|--------------|
| time-advance loop | demo0.ck | none (no audio patch) | none visible | yes: `1::second => now` inside while | bounded: runs until `later` |
| SinOsc patch + loop | demo3.ck | freq variable (float) | dac via Gain g | yes: per iteration | bounded: x counts down from 6 |
| clock printer | tick.ck | system clock (now) | <<< now/second >>> to stdout | yes: `1::second => now` | unbounded: infinite loop |
| mic passthrough | adc.ck | adc (mic-in) | dac via Gain g | yes: `100::ms => now` | unbounded: infinite loop |

## Mechanism dependency

`=>` (ChucK) = connect node A into node B in the signal graph.
`=<` = disconnect. These are the *only* graph-mutation operators visible in the files.
Time only advances inside a shred when `... => now` executes; without it, the
shred blocks. This is the "strongly-timed" constraint (README heading, unexplained
in the files themselves).

## Composition assumptions

1. All four files share the same audio graph (dac, adc are singletons per process).
2. Combining adc.ck and demo3.ck requires explicit gain budgeting: two paths reach dac.
3. Bounded loops (demo3) are safe to `Machine.add()` alongside infinite loops;
   infinite loops require `Machine.remove()` or process exit to stop.
4. tick.ck produces only stdout side-effects; it is safe to combine with any audio shred.

## Open questions (for research queue)

- Do example files inherit the MIT/GPL2+ license or carry a separate license?
- What is the default gain on adc => Gain g? (not stated in source record)
- Does `1::second => now` in tick.ck drift relative to wall clock over long runs?