# ACE-Step VRAM Planning Cases

> Hypotheses only. "Weights fit" ≠ "generation succeeds end-to-end."
> Source: live README 2026-11-07T11:28Z + src_01M569EH7T3ETK0TS4BRR8QX9A r2.

## Case A — 4 GB VRAM

**Target**: v1.5 base with maximum offload + quantization.

- Upstream claims <4 GB VRAM is achievable. Likely requires most aggressive offload.
- **What fails in practice**: OOM during DiT diffusion steps on songs >2 min; slow generation from CPU offload bandwidth.
- **Do not assume**: The <4 GB claim does not state tested song length. Activation peaks for longer songs may push beyond 4 GB.
- **Practical first step**: Generate a 10-second clip, monitor peak VRAM (`nvidia-smi dmon`). Establish OOM boundary before longer targets.
- **LoRA training**: Not viable (12 GB cited minimum).
- **Verification signal**: Successful OOM-free completion at 10 s → 30 s → 60 s → 120 s.

## Case B — 8 GB VRAM

**Target**: v1.5 base; XL is out of scope.

- Base weights (~4.7 GB) leave ~3 GB headroom for activations — likely sufficient for short-to-medium songs at standard diffusion steps.
- **What fails in practice**: Multi-song batch OOM; LoRA training likely fails (12 GB cited); songs >5 min may require offload.
- **Do not assume**: 3 GB headroom is not validated for full 10-min generation.
- **Practical first step**: Monitor peak VRAM at 2 min, 5 min, 10 min durations. Set offload flag when headroom drops below 1 GB.
- **Verification signal**: 5-min song completes without OOM in a single-song run.

## Case C — 12 GB VRAM

**Target**: v1.5 XL at minimum threshold (offload+quant); v1.5 base comfortable.

- XL minimum per upstream claim is ≥12 GB with offload+quantization. This is the floor, not comfortable headroom.
- Base at 12 GB should allow full 10-min range and LoRA training (3090 12 GB is the documented case).
- **What fails in practice**: XL + long duration + batch >1 likely OOMs. XL DiT LoRA training not documented.
- **Practical first step for XL**: Start with 10-second clips, single batch. Increment duration only after confirming headroom.
- **Practical first step for base LoRA**: Run 8-song LoRA job and report actual peak VRAM — this is the closest to a documented test case.
- **Verification signal**: XL generates 10-second clip cleanly; base completes LoRA training without OOM.

## Recurring question for all cases

> What fails in practice, and how will we know the fix worked?

Answer: OOM is the primary failure mode. Measure peak VRAM at the target duration before committing to that configuration. A successful short clip is not proof a long song will fit.