# Limits

- All values are **author statements** from eleven archived card texts (art_01M66JVTQPRBASJFZ4PK2DM74A r1). Nothing was run or measured.
- InstantID uses `ip_adapter_scale=0.8` and `controlnet_conditioning_scale=0.8`; it is an adapter with a ControlNet, not a LoRA. Not included in `check()`.
- Four cards (Lightning variants and Photo-to-Anime) give steps/sigmas/CFG instead of a strength. `no_data` is the honest status.
- `anything2real` gives a strength for Qwen Edit 2511 only; the card states no separate strength for its Flux2 Klein files in the text read.
- `lcm_lora_sd15`: the `strength=0.6` in the card's img2img example is the **denoising** strength, not the LoRA scale. The ControlNet example sets `scale=1`.
- `viggle_turbo_v0_3`: the ~30% merge loss figure is a card claim, not a measurement.
- No general rule across models is stated or inferred.