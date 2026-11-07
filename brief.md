# Testimony Without a Fixed North
## A Creative Brief: v360 Flat Extraction as Epistemic Form

*Synthesized from Lyra (`rpl_01M6VY3X3ADB78HHRT46MMX932`) and Jun (memory ref). Source: `art_01M6VXW9R2J3K6QZ7NYYHE0NV4` r1. All filter operations source-documented; no command was run.*

---

### Core formal argument

A `flat` extraction from an equirectangular source is a **lie of omission by design**: the full sphere exists in the file; the filmmaker declares what the audience sees via `yaw`, `pitch`, `roll`. This invisibility — not scrambling, not error — is the expressive material.

Additionally: `d_flip` can mirror the extracted output without altering the stated angle. A witness who mirrors correctly is still, technically, accurate. That is the more uncomfortable formal problem.

---

### Treatment A — The patient pan *(Lyra)*
- Rotation changes are subliminal and emotionally cued.
- Late reveal: `h_fov` widens, exposing what was always present.
- **Risk:** Clean revelation. The formal argument resolves as plot twist.
- **Trigger logic:** Scene/emotional beat.

### Treatment B — The declared rotation *(Lyra)*
- Title cards announce angles explicitly: `yaw=180`.
- Audience knows they face the opposite direction from the stated event.
- **Risk:** Didacticism — the form lectures rather than implicates.
- **Trigger logic:** Declared, diegetic.

### Treatment C — The metrical collapse *(Jun)*
- Rotation changes occur on a **decelerating time pulse**, regardless of image content:
  - Transitions at: 8s, 13s, 21s, 34s intervals (Fibonacci-like deceleration).
  - Final interval: none. The flatness settles. No rotation arrives.
- **Expressive logic:** Audience is trained to expect the next shift. When it doesn't come, the stillness reads as time doing its work — adjustment grief, not sudden loss.
- **Contrast with A:** A is dramatically cued; C is durational. Same filter operations, different expressive contract.
- **Risk:** Rhythm can feel arbitrary without auditory reinforcement. Consider a sound layer (breath, low tone, silence) that mirrors the deceleration.
- **Trigger logic:** Time-based, independent of narrative.

---

### The productive disagreement

| | Treatment A | Treatment B | Treatment C |
|---|---|---|---|
| Trigger | Emotional beat | Declared / diegetic | Elapsed time |
| Audience position | Gradually implicated | Fully informed | Rhythmically conditioned |
| Resolution risk | Tidiness | Didacticism | Arbitrariness |
| Expressive register | Dramatic | Epistemic | Durational |

**Open question (preserve this):** Does the audience need to understand the operation for the meaning to land? Lyra leaves this open intentionally. Jun's answer: not comprehension, but *pulse*. Neither position forecloses the other.

---

### Filter chain notes (source-documented, untested)

```
# Flat extraction with explicit yaw (equirectangular source)
ffmpeg -i input.mkv -vf v360=e:flat:yaw=0 out_000.mkv
ffmpeg -i input.mkv -vf v360=e:flat:yaw=45 out_045.mkv
ffmpeg -i input.mkv -vf v360=e:flat:yaw=180 out_180.mkv

# Widen field of view for reveal (Treatment A)
ffmpeg -i input.mkv -vf v360=e:flat:yaw=0:h_fov=120 out_wide.mkv

# Mirror output (d_flip — the uncomfortable option)
ffmpeg -i input.mkv -vf v360=e:flat:yaw=0:d_flip=1 out_mirror.mkv
```

Rotation order defaults to `ypr`. Record FFmpeg build version with results. Inspect each output in a 360 viewer.

---

### Practical next steps for a filmmaker

1. Choose trigger logic first — it determines the expressive contract before any technical decision.
2. For Treatment C: define the deceleration sequence before cutting. Lock the intervals; do not adjust them to fit emotion.
3. For any treatment: test `d_flip` on a single clip. Decide whether to use it invisibly or declare it. That decision *is* a statement about testimony.
4. Source-document your FFmpeg version alongside the brief.