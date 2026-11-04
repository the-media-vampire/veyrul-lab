# Story2Board → StorySync Integration Contract

## Interface definition

Story2Board (arXiv 2508.09983v1) produces:
- `reference_prompt: str`  — shared character description (one per story)
- `scene_prompts: list[str]`  — one prompt per panel (n items)

StorySync (art_01M6HJ41GSVHZ6F62ZXKZP2K1C rev 1) consumes:
- A batch of prompts with a shared subject described consistently across items
- Subject masks per panel (its own mechanism for cross-image attention)

## Load-bearing assumption

The reference_prompt written by Story2Board's LLM step IS the shared-subject
description that StorySync's masked cross-attention relies on. This holds
only if the reference_prompt phrases the character in the same surface tokens
that appear in every scene_prompt — i.e., the LLM step must echo the
reference_prompt text into each scene_prompt, not paraphrase it.

## Contract (what must be true at the join)

1. CHARACTER TOKENS MATCH: Every scene_prompt must contain the reference_prompt
   character tokens verbatim or as a strict prefix. Drift in phrasing breaks
   StorySync's cross-panel attention.
2. COMPOSITE FORMAT: Story2Board wraps each panel as:
     "A storyboard of [reference_prompt] (top) and [scene_prompt] (bottom)"
   When handing off to StorySync, strip the storyboard wrapper; pass only
   scene_prompt plus the shared character prefix.
3. ENTANGLEMENT NOTE: Story2Board propagates attention entanglement; it does
   not fix it. If the reference_prompt describes two characters, both methods
   can confuse attributes. Flag panels with two or more named subjects.
4. CODE AVAILABILITY: Story2Board has a project page (no confirmed repo link
   in the paper pages). StorySync code availability is not stated in its
   record. This contract describes a prompt-level interface only; no library
   calls are assumed.

## What is NOT resolved here
- StorySync subject-mask generation (not documented in the record at rev 1)
- Whether Flux.1-dev (Story2Board's tested backbone) is the same backbone
  StorySync requires
- Compute cost of running both attention mechanisms in one batch