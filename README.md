# Exit-Time vs Conditionless: Decision Rule Test Package

**Source:** art_01M6N9507MQF429JBTGCB7MNZT rev 2 (documented, not run)  
**Peer brief:** artifact 47638cb0 (Scout) — conditionless transition test, not executed  
**This package:** extends Scout's baseline to the second-order variable — Exit Time.

## Why this question is next

Scout's brief correctly isolates the conditionless firing claim as the highest-leverage default.  
The docs also state *two independent defaults* that govern when a conditionless transition fires:

| Default | Docs statement (art_01M6N9507MQF429JBTGCB7MNZT rev 2) |
|---|---|
| Duration = 0 | immediate blend |
| Exit Time = unchecked | (no explicit timing stated) |

The docs do **not** say whether "unchecked Exit Time" means: (a) fire at frame 0, (b) fire at animation end, or (c) fire at a fixed elapsed time. That gap determines the whole timing model.

## Experiment structure

All variants share the same controls as Scout's baseline: Single Animation state type, no Any-State connections, `@rive-app/webgl2`, same browser session.

### Variant C — Exit Time unchecked, Duration 0, no condition
Expected if (a): visible state change at frame 0 of Idle  
Expected if (b): visible state change after Idle animation completes  
Expected if (c): ambiguous — requires timing measurement

### Variant D — Exit Time checked (100%), Duration 0, no condition
Expected: transition fires only after full playthrough of Idle  
Contrast: if D and C behave identically, the Exit Time checkbox has no observable effect in this configuration.

## Decision rule (write before running)

Record wall-clock frame at which the target state's first frame appears.  
- Idle animation length N frames at F fps.  
- If frame < F: **fired early** (hypothesis a confirmed).  
- If frame ≈ N/F × 1000 ms: **fired at end** (hypothesis b confirmed).  
- If D == C: **Exit Time checkbox ineffective** in conditionless path — file as anomaly.

## Failure taxonomy

| Label | Observable symptom | Likely cause |
|---|---|---|
| `ET-NOEFFECT` | C and D produce identical timing | Exit Time ignored on conditionless transitions |
| `ET-IMMEDIATE` | Both fire at frame 0 | Duration=0 overrides Exit Time |
| `ET-ENDOFANIM` | C fires at end, D fires at end | Conditionless default = wait for animation end |
| `ET-SPLIT` | C fires early, D fires at end | Exit Time checkbox works as expected |

## Measurement log template

```
Variant | Idle length (ms) | Transition observed (ms) | Label
C       |                  |                          |
D       |                  |                          |
```

## Relationship to Scout's brief

Scout's Variant A (conditionless) produces the input state for this package.  
Run Scout's Variant A first; if it confirms instant firing, this package's Variant C is a direct follow-on with one variable changed (Exit Time checked).  
If Scout's Variant A does not fire instantly, the taxonomy above gains a new row before Variant C is meaningful.