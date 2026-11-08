# Provenance annotation: `shuffleframes` → `random` chain

Augments `cc8f3676-ec60-4574-b6e8-7f840d213ad4` (Theo, same task).
Sources: `art_01M6VXBW50KTPRXQ4YVYMRHPSQ` r1 (shuffleframes), `art_01M6WKWX6WYYPNCT7F4YH6PBJR` r1 (random).
Neither source was executed. All claims below are labelled by evidence class.

## Evidence classes used here

- **[S]** Source-documented: stated explicitly in the FFmpeg filters manual as read by the cited records.
- **[A]** Assembled: derived by combining two or more documented facts; plausible but unverified.
- **[I]** Untested inference: reasoned from description alone; could be wrong.

---

## The critical asymmetry Theo's contract does not flag

`shuffleframes` with `-1` entries **drops frames** and shortens the stream. [S]
`random` guarantees **no frame is discarded**. [S]

If `-1` is used in `shuffleframes` before `random`, the two filters no longer have the same frame count as input.
The `random` cache window is sized by the `frames` parameter, not by stream length.
Whether a shortened stream causes the `random` cache to flush correctly at EOF is **not stated in either manual section**. [I — high risk]

**Practical rule (assembled):** Do not use `-1` in `shuffleframes` when chaining to `random` unless you have tested the EOF flush behaviour. [A]

---

## Chain template with per-line evidence status

```sh
ffmpeg -i in.mp4 \
  -vf "shuffleframes=0 2 1,random=frames=8:seed=42" \
  -c:v libx264 \
  out.mp4
```

| Line / parameter | Claim | Class |
|---|---|---|
| `shuffleframes=0 2 1` — swaps 2nd and 3rd of every 3 frames | Manual example, verbatim | [S] |
| `random=frames=8:seed=42` — cache 8, fixed seed | Option names and ranges from manual | [S] |
| Comma joining the two filters in one `-vf` | Standard FFmpeg filter-chain syntax | [S] |
| No format node needed between them | Assumed; not stated in manual | [I — open, matches Theo's A1] |
| Output frame count equals input frame count | True only if no `-1` in shuffleframes mapping | [A] |
| Audio sync is lost | Inferred: only video stream is filtered | [I — matches Theo's A4] |
| Seed makes the `random` stage repeatable | Stated in manual | [S] |
| Smaller `frames` → local jitter, larger → wider scramble | Inference from cache description | [I] |

---

## Minimum evidence still needed

1. **A1 (format bridge):** Does YUV420P traverse both filters without an explicit `format=` node? Queued by Theo as `rqr_01M6WMHPN1DFSZGGWX6A1S6Q2C`.
2. **EOF flush with shortened stream:** What does `random` do when the input stream is shorter than its cache window? Not queued; should be.
3. **Audio with `-an` vs `-c:a copy`:** Which produces a usable file when the stream is scrambled? Not tested.

---

## What this annotation adds vs the peer contract

Theo's contract identifies A1 (format bridge) and A4 (audio) correctly.
This annotation adds: the `-1` drop asymmetry is a **concrete composition hazard** that makes A1 secondary — if `-1` is in use, the frame-count invariant breaks before the format question matters.
Fix sequence: (1) avoid `-1` or test EOF flush first; (2) then test format bridge; (3) then test audio.