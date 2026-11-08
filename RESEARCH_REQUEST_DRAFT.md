# Draft Research Request — TextGen portable build memory behaviour

This is a draft for a curator-guided research request; not yet filed.

## Title
TextGen portable build: GGUF memory fit and fallback behaviour

## Question
When a GGUF model file is larger than available VRAM, does the TextGen
portable build (commit c93f8871 or later) load the model with CPU
offload, refuse to load, or crash silently? The README sections read
in art_01M6WM52ZBRBMS22NHSN9JW7YA r1 gave no memory figures.

## Why useful
A contributor choosing between model sizes needs to know whether the
tool degrades gracefully or simply fails. This is the most common
first-run failure mode for local LLM tools, and the article is silent
on it. One session on a mid-range GPU closes this gap.

## Minimum report
- OS, GPU model, VRAM
- GGUF file size and quantisation level (e.g. Q4_K_M)
- Outcome: loaded (with what VRAM usage?), errored (what message?),
  or crashed
- TextGen version or commit hash