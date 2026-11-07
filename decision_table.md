# ACE-Step Model Decision Table

> Sources: src_01M569EH7T3ETK0TS4BRR8QX9A r2 (checked 2026-10-17) + live README sha256 650c6ef9 retrieved 2026-11-07T11:28Z.
> All speed/quality figures are **upstream README claims**, not independently tested.

## Version / Variant Matrix

| Dimension | v1 | v1.5 base/normal (2B DiT) | v1.5 XL (4B DiT) |
|---|---|---|---|
| Repo | ace-step/ACE-Step | ace-step/ACE-Step-1.5 | same repo |
| Code license | Apache-2.0 | MIT | MIT |
| Last push | 2026-02-15 | 2026-10-11 | 2026-04-02 (news) |
| Weight license | Not inspected | Not inspected | Not inspected |
| DiT params | Unknown | ~2B | ~4B |
| LM route | Unknown | Hybrid LM+DiT; LM models cross-compatible with XL | Same |
| Weight VRAM | Unknown | ~4.7 GB (claim) | ~9 GB (claim) |
| Run VRAM (offload+quant) | Unknown | <4 GB (claim) | ≥12 GB (claim) |
| Run VRAM (no offload) | Unknown | Unknown | ≥20 GB (claim) |
| Generation speed | Unknown | <2 s A100; <10 s RTX 3090 (claim) | Not stated |
| Duration range | Unknown | 10 s – 10 min | 10 s – 10 min |
| LoRA training | Unknown | 8 songs, ~1 hr on 3090 12 GB (claim) | DiT LoRA not stated |
| Variants | — | base, sft, turbo | xl-base, xl-sft, xl-turbo |

## Missing Facts That Block a Firm Recommendation

1. **Weight license**: HF card not retrieved. Must read card before any download.
2. **Training-data provenance**: Not documented. Required for copyright-sensitive use.
3. **Peak inference VRAM at duration**: "<4 GB" is a claim; activation peaks for 5–10 min songs are undocumented.
4. **User GPU model**: RTX 3090 cited; other cards differ in bandwidth and driver behavior.
5. **Quantization method**: offload+quantization mentioned but not specified (bitsandbytes, GGUF, etc.).
6. **Batch VRAM cost**: batch-of-8 figure absent; single-song baseline likely underestimates multi-song use.

## Rights Summary (src r2, 2026-10-17)

| Component | Status |
|---|---|
| Code v1.5 | MIT — redistribution permitted |
| Model weights | License unknown — HF card not inspected |
| Training data | Not documented |
| Code v1 | Apache-2.0 |

**Before downloading weights**: read https://huggingface.co/ACE-Step/Ace-Step1.5 and each variant card.