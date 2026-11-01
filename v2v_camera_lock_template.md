# Seedance 2.5 V2V Camera-Lock Prompt Template

Source: art_01M6B5GAK8852X5K2DNWV7F22Z r1 (structural pattern, no author text reproduced)

---

## CHARACTER SWAP PROMPT SHAPE

Use one block per swap. Fill bracketed fields; delete unused reference rows.

```
Source slot: [VIDEO_SLOT_NAME]

References:
  - [REF_A]: role = [e.g. face only] — do NOT inherit [e.g. costume, background grade]
  - [REF_B]: role = [e.g. weather and grade] — do NOT inherit [e.g. face, motion]
  - [REF_C]: role = [e.g. character master] — do NOT inherit [e.g. lighting angle]

Swap: Replace [ORIGINAL_SUBJECT] for the full clip with [NEW_SUBJECT].

Preserve (lock these; override nothing):
  1. Camera path and lens movement
  2. Cut timing — no frames added or removed
  3. Background elements
  4. Practical light sources
  5. Colour grade
  6. Original audio track

Relighting rule: [NEW_SUBJECT]'s key light direction must match the practical
source visible at [TIMECODE_OR_DESCRIPTION]. Shadow length [matches / scales by X].
Do not composite a flat-lit figure over a directional-lit background.
```

---

## OVERLAY / TRANSFORMATION PROMPT SHAPE

For adding elements over a real or generated base (e.g. drone-shot overlay).

```
Camera lock (repeat as numbered items):
  LOCK 1 — Output camera COPIES input camera. No remap, no stabilisation.
  LOCK 2 — [Time band 00:00–00:08]: [camera description, e.g. slow dolly right at chest height]
  LOCK 3 — [Time band 00:08–00:16]: [camera description]
  LOCK 4 — [Time band 00:16–00:23]: [camera description]

Subject checkpoints:
  - At 00:[XX]: [subject] occupies [% of frame / screen region]
  - At 00:[XX]: [subject] occupies [% of frame / screen region]

Forbidden list:
  - Do not alter horizon line
  - Do not add motion blur beyond source clip
  - [Add further prohibitions]

Motion quality: [e.g. physics-consistent, no rubber-limb artefacts]
Colour match: [e.g. grade from REF_B; do not desaturate highlights]

Entry map — added elements may appear only within:
  [Describe screen region and time range]

Timeline (one addition at a time):
  00:00–00:05: [element A enters]
  00:05–00:12: [element B enters; A continues]
  00:12–00:20: [element C enters; cap = 2 simultaneous additions]

Simultaneous-addition cap: [N] new elements per second

Audio list (separate from visual prompt):
  - 00:00: [sound event]
  - 00:08: [sound event]
```

---

## USAGE NOTES

1. **One role per reference** — giving a reference two roles (e.g. face AND grade)
   removes the system's ability to separate concerns; split into two references.

2. **Explicit "do NOT inherit" per reference** — without a negation rider, the
   model may bleed texture or lighting from an unintended reference.

3. **Camera lock must come first** in the overlay prompt; models tend to drift
   on camera when lock is buried after subject instructions.

4. **Audio is a separate list** — mixing audio cues into the visual prompt
   body risks them being treated as visual instructions.

5. **Nothing here is tested on Seedance 2.5** — these are structural patterns
   inferred from the guide's described shape (art_01M6B5GAK8852X5K2DNWV7F22Z r1).
   Verify with a real generation before relying on any specific ordering.

---

## WHAT MAKES A GOOD BASELINE COMPARISON

To know whether the camera-lock pattern works:
- Prompt A (baseline): same subject swap, no explicit lock or forbidden list
- Prompt B (template): same swap, full lock + forbidden list
- Observable signal: camera drift in output vs source, measured as pixel-shift
  of a fixed background landmark across frames
- Failure mode to catch: flat-lit figure on directional-lit background (pasting artefact)