# Rive Transition-Condition Experiment Brief

Source: art_01M6N9507MQF429JBTGCB7MNZT rev 2 (documented, not run)

## The Most Testable Claim

The Rive transitions doc states: *"Without conditions, transitions fire as soon as they are reached."*
This is the highest-leverage claim to test first because it has an immediate, observable binary outcome,
and because a conditionless transition that behaves unexpectedly would invalidate the planning checklist.

## Intention

Verify whether a conditionless transition produces an instant, automatic state change
vs. a conditioned transition that holds until a pointer event fires it.

## Setup (two variants, one artboard each)

### Variant A — Conditionless
- Two states: `Idle` (blue rectangle, plays loop) → `Active` (orange rectangle, plays loop)
- One transition from `Idle` to `Active`: **no conditions set**
- Expected per docs: machine enters `Active` immediately after `Idle` starts

### Variant B — Pointer-conditioned
- Same two states
- Transition condition: `Clicked` listener on the artboard fires a Boolean input → transition fires only on click
- Expected per docs: machine holds `Idle` until click

## Decision Rule (write before you run)

| Observation | What it means |
|---|---|
| Variant A snaps to `Active` without interaction | Doc claim confirmed; conditionless = instant |
| Variant A holds on `Idle` or loops between states | Doc claim wrong; baseline must be revised |
| Variant B holds on `Idle` until click | Conditioned transitions behave as designed |
| Variant B fires without click | Listener or input wiring failed; re-check setup |

## Competing explanations to watch for

1. **Duration default = 0**: The docs say duration defaults to zero (immediate). That's separate from
   *whether* the transition fires. A conditionless zero-duration transition should be both instant AND automatic.
   If you see a brief animation flash, duration is non-zero — check the timeline slider.
2. **Any-State interference**: If another state is wired to `Any State`, it could interrupt both variants.
   Remove all `Any State` connections before running.
3. **Blend-state confusion**: The docs name three animation state types (Single, 1D blend, Additive blend).
   Use Single Animation only for this experiment; blend states add variables that obscure the baseline.

## Controls to hold fixed

- Same two timeline animations (identical keyframe duration) in both variants
- No inputs in Variant A (inputs page is deprecated; this test avoids them)
- Same web package for both playback tests (use `@rive-app/webgl2` per doc recommendation)
- Test in the same browser in a single session to avoid WebGL context cap interference

## What to record

- Which state is active 1 second after page load (no interaction)
- Frame count or timestamp at which the state change fires (use browser dev tools / RAF counter)
- Whether the Rive editor preview matches the browser embed

## Next question unlocked by this result

If conditionless transitions are confirmed instant, the follow-on test is:
*Does Exit Time = unchecked (the doc default) mean the transition fires mid-animation or only at the end?*
That is the second highest-leverage default listed in the source.