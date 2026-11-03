# MiniMax-H3 Few-Step LoRA: Loader Guard & Dispatch Contract

Source: `art_01M6FG17EJ5VRRZ6BNZKEMXN8M` r1. Not executed.

## The shared failure mode

Every variant risks a **silent no-op**: the LoRA loads without error but patches
nothing because its key layout does not match the loader. The PDMD 4-step
original is the documented case (diffusers keys matched nothing in ComfyUI).

**Guard**: read the patch-count log line before trusting any output.

| Variant | Expected log signal (record-stated) |
|---|---|
| pdmd_4step_comfyui | 208 keys, shapes match, numerically identical |
| pdmd_2step_comfyui | 468 numeric checks pass (exact fp32) |
| taomate_3step | 208 patches attached, no missing-key warnings |
| turbo | none stated in records |
| pdmd_4step_original | do not use in ComfyUI — use comfyui conversion |

## Boundary 1 — file → loader node
- File identity (v6 bf16 / fp32 / v4 EMA) and base checkpoint must be confirmed
- Strength = 1.0 for PDMD and TaoMate; Turbo allows small nudges
- Loader: LoraLoaderModelOnly (PDMD); either (TaoMate); between-loader-and-sampler (Turbo)

## Boundary 2 — loader → sampler
- Steps: 4/2/3-8/3 per variant (see Spec)
- CFG: ~0 (PDMD, Turbo); exactly 1.0 (TaoMate — >1.0 corrupts distilled ODE)
- Scheduler: H3 shift 12/3 (PDMD); simple (Turbo); Euler+simple/linear FlowMatch (TaoMate)

## Open gap
Records do not map each LoRA file to a specific base checkpoint (FL2VA,
ref2va int8_convrot, bf16, int8_convrot, pruned int8). A wrong-base load
may still pass the patch-count check if key names match.

## Licence labels (record-stated; not rights determinations)
Apache-2.0 on PDMD variants and Turbo preview; MiniMax H3 Community License
Agreement on TaoMate; MiniMax H3 base weights keep their own terms.