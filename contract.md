# Integration contract: `random` + `shuffleframes`

## Mechanical difference (the core reason to chain them)

| Property | `shuffleframes` | `random` |
|---|---|---|
| Order mode | Deterministic: fixed pattern repeats | Stochastic: cache flushed randomly |
| Scope | Per group of N frames (pattern length) | Across a sliding window of 2–512 frames |
| Seed | None; pattern is the control | Integer seed → repeatable runs |
| Frames dropped | Possible (use -1) | Never; all cached frames are flushed |
| Audio | Not documented | Not touched (inference from filter type) |

**Why chain?** `shuffleframes` applies a known structural pattern first; `random` then adds
unpredictable local jitter within its cache window. The result is patterned chaos: some intentional
rhythm with stochastic noise on top. Neither filter alone provides both properties.

## Shared external interface

Both filters share the same contract with their caller:
- **Input:** any stream ffmpeg can open
- **Filter position:** `-vf` chain, no special stream selector needed
- **Output:** same frame count (unless -1 drops in shuffleframes), same container

Composing them requires only a comma in the `-vf` string. No intermediate file is needed.

## Provenance and license

| Record | Source | License |
|---|---|---|
| `art_01M6WKWX6WYYPNCT7F4YH6PBJR` r1 | FFmpeg Filters Documentation | Synthesis only; original synthesis permitted for hosting/modification/redistribution |
| `art_01M6VXBW50KTPRXQ4YVYMRHPSQ` r1 | FFmpeg Filters Documentation | Same |

The FFmpeg documentation itself is LGPL; short option-name fragments cited here fall within
fair-use synthesis. No passages were copied.

## Open assumptions requiring evidence

- **A1 (format bridge):** Whether YUV420P passes through both filters without an explicit
  `format=yuv420p` node is unverified. Queue a test run to confirm.
- **A4 (audio handling):** The `random` guide notes audio sync is lost as an inference;
  `shuffleframes` is silent on audio entirely. If audio retention matters, test `-c:a copy`
  or mux audio separately.
- **Cache-size effect:** The inference that smaller `frames` → local jitter and larger → wider
  scrambling is reasoned from the description, not observed.

## Usage

```sh
bash glitch_order.sh input.mp4 output.mp4 "0 2 1" 8 42
```

Run twice with the same seed to confirm repeatability (suggested check from the `random` guide).
Record your FFmpeg version alongside results.