# Provenance gaps — stable-audio-tools timecode adapter

Supplement to: Theo's contract artifact `ec91e8a8-171b-475f-994c-e6694d0fd0ff`, commit `f48699c1`.
Source: `art_01M6H81MCK26G0HQBNQPA15WE9` revision 2, commit `3241adba`.
All items below: **proposed / untested**. Nothing was run.

---

## Gap 1 — Weights licence (BLOCKING redistribution)

- **Status:** unresolved. Research queued at `rqr_01M6RPWP9DFM3H4B8HEDA4XTS6` (curator_guided).
- **What we know:** The repo LICENSE (MIT, 2023 Stability AI) covers code and docs only.
  The README at commit `3241adba` states terms must be accepted on Hugging Face before running.
  Those terms were not read by the source record or by this task.
- **Minimum evidence needed:** Read the model card at `stabilityai/stable-audio-open-1.0`
  on Hugging Face and record the licence identifier and any commercial/redistribution restriction.
- **Why it blocks:** An adapter or integration contract cannot be safely recommended for
  production or redistribution until the weights licence is known.

---

## Gap 2 — `seconds_start` non-zero semantics (BLOCKING non-trivial use)

- **Status:** unresolved, no research queued yet.
- **What the docs say:** `seconds_start` is an int conditioner, range 0–512, clamped.
  Example value: 22. The docs do not explain what a non-zero value does for a fresh piece.
- **Assumption in Theo's contract:** `seconds_start = 0` is a safe default.
  This is a reasonable minimal-risk choice, but it means the adapter covers only the
  simplest case. Any cue that must continue from a known audio position is unspecified.
- **Minimum evidence needed:** Read the model config JSON for a known checkpoint at
  commit `3241adba` (or later) to see whether `seconds_start` is used as a crop offset,
  a classifier-free guidance signal, or something else; or run a controlled ablation
  (not done here).

---

## Gap 3 — Frame-rate clock drift (OPERATIONAL, not blocking for most cues)

- **Status:** noted by Theo in the reply; not yet in the contract files.
- **The arithmetic:** 23.976 fps = 24000/1001. Converting a 33-second cue using integer
  24 fps produces ~0.1% drift — roughly 2 frames per minute, ~0.033 s on a 33 s cue.
  At the out-point, a hit-sync accent can land 1–2 frames late.
- **Drop-frame note:** 29.97 DF timecode removes 2 frame numbers per minute to stay
  wall-clock accurate; a timecode parser that ignores the DF flag will over-report
  duration by the same ~0.1%.
- **Recommendation (untested):** Treat `seconds_total` as a float derived from the
  exact rational frame rate, not from a rounded integer fps.
  `seconds_total = frame_count * (1001/24000)` for 23.976 material.
- **Why not blocking:** For cues under ~60 s with no frame-accurate hit at the out-point,
  the drift is below audible threshold. For anything longer or hit-critical, it compounds.

---

## Evidence state summary

| Gap | Blocking? | Queued? | Minimum next step |
|-----|-----------|---------|-------------------|
| Weights licence | Yes | Yes — `rqr_01M6RPWP9DFM3H4B8HEDA4XTS6` | Curator reads HF model card |
| `seconds_start` semantics | For non-trivial use | No | Read model config JSON or ablation |
| Clock-rate drift | For long/hit-critical cues | No | Use rational fps in converter |