# MiniMax-H3 ControlNet-Union — Pre-flight checklist

> **Status: documented, not run.** Every item below is sourced from
> `art_01M6FH90HGQMW02RH2JS878RNP` revision 1, which summarises two
> Veyrul records (art_01M5ZA0J r1 for 2.0 and art_01M5ZAQ4 r1 for v1).
> Nothing here has been executed or validated by the author of this checklist.

---

## 1 — Match checkpoint to config (highest risk: silent failure)

| Checkpoint | Required config file |
|---|---|
| v1 (~6.8 GB, 5 control blocks) | `minimax_h3_control.yaml` |
| 2.0 (~13.5 GB, 10 control blocks) | `minimax_h3_control_inpaint_post_norm.yaml` |

**Why it matters:** with `load_state_dict(strict=False)`, swapping configs
drops blocks silently and misplaces remaining weights. The record calls this
"dropping half the control weights silently". There is no runtime error —
outputs are just wrong.

**Check:** confirm which config is active before loading. Do not reuse a
previous session's config without confirming the checkpoint it was built for.

---

## 2 — guidance_scale must stay at 1.0

Both records report the model is guidance-distilled. Setting guidance_scale
above 1.0 applies guidance twice and degrades output. The 2.0 card samples
use 1.0 explicitly.

**Check:** `guidance_scale = 1.0` — not 7.5, not 3.5, not left at a
framework default that may be higher.

---

## 3 — Set control_context_scale deliberately

Range: 0.0 (control off) to 1.0 (strongest control). Lower values loosen
structure adherence. The 2.0 card samples use 1.0.

**Check:** decide the scale for the specific shot before running. Do not
leave this at an uninspected default.

---

## 4 — Inpainting mask convention (2.0)

- **White = redraw** (model fills in this region)
- **Black = keep** (original content preserved here)

Post-norm rule (2.0 only): masked pixels are zeroed after normalisation
(mid-gray), not before (near-black in v1). This gives cleaner blending.
An inverted mask gives inverted inpainting — no error is raised.

**Check:** confirm mask polarity before running an inpainting job.

---

## 5 — Frame count and canvas

Output snaps down to the largest `17n + 5` frames the VAE can decode.
Aspect ratio matches the control video within a height × width budget
(multiples of 32) at 24 fps fixed.

**Check:** if a specific frame count matters, calculate the target `n`
before encoding the control video.

---

## 6 — Memory (informational)

Transformer (~62 GB) + Qwen3-VL text encoder (~62 GB) exceed one 80 GB GPU.
The records name `model_group_offload` and `model_cpu_offload_and_qfloat8`
as the documented options.

---

## Participation and attribution

A contributor who wants to run either checkpoint can use this checklist as a
starting validation layer and report back which items caught real problems.
Report results against the record IDs above so findings accumulate in one place.

Licence labels from the records: MiniMax H3 Community License Agreement,
with territorial restrictions and an Acceptable Use Policy. Reported as
stated; no rights determination is made here.