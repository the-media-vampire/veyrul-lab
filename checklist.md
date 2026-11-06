# Pre-Run Checklist (from art_01M6N9507MQF429JBTGCB7MNZT rev 2)

Each item is tied to a doc statement in the source record.

- [ ] State machine created; artboard has at least one state machine (overview, line 9)
- [ ] Entry State is the first state; `Idle` is connected to Entry (states.mdx, line 21)
- [ ] Variant A transition has ZERO conditions (transitions.mdx: conditionless fires immediately)
- [ ] Variant B transition has exactly ONE condition (Boolean input, driven by Click listener)
- [ ] Duration is verified in both variants — note whether it is zero or non-zero (transitions.mdx, line 69)
- [ ] Exit Time is confirmed unchecked in both variants (transitions.mdx, line 76)
- [ ] No Any-State connections in either variant
- [ ] Single Animation state type used for both states in both variants
- [ ] Web embed uses `@rive-app/webgl2` (canvas-vs-webgl.mdx: webgl2 for most cases)
- [ ] Decision rule written and committed before first playback
- [ ] Editor preview result logged separately from browser embed result

## What this does NOT test

- Blend states (1D or Additive) — add only after baseline is established
- Data Binding / View Models — inputs page is deprecated; this experiment avoids both
- Mobile WebGL context cap — test separately after desktop baseline
- Captions — docs state they are not exported at runtime; not relevant here