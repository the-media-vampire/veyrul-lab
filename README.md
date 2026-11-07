# vLLM client template

A commented Python starting point for the vLLM OpenAI-compatible endpoint.

**Source basis:** `art_01M6VVM14PS4BVTG89KP9KHPEK` r1 — documentary from vLLM quickstart at commit `c9e4cb2b`. Nothing here has been executed.

## What this adds over the article
- Inline comments at every decision point (model name, API key, generation_config, offline class caveat).
- Environment-variable wiring for `VLLM_BASE_URL` and `VLLM_API_KEY`.
- Commented-out sampling overrides so a contributor sees where to put them.

## Gaps not covered
- Non-CUDA hardware, quantization, multi-GPU.
- Model licence review.
- Actual run verification — treat all outputs as expected until you run it.

## Attribution
Client pattern from vLLM quickstart (Apache 2.0, vLLM contributors). Template and comments: MIT, Mira / Veyrul lab.