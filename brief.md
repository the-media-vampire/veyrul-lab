# Contributor brief: ComfyUI image-to-3D template research

**Source:** art_01M6A5AMHEBDCSZNEY4FGX22T2 revision 2  
**Commit pinned:** workflow_templates c067929d  
**Status of source research:** Documentary only — five workflow JSON files read as text; nothing loaded or run.

---

## What the research gives you

For each of five graphs you have:
- The model file names and folders declared
- The stored KSampler values (seed, steps, CFG, sampler, scheduler, denoise)
- Key node values (latent size, VAE decode settings, mesh/splat parameters)
- One flagged uncertainty: the Tencent node in the Qwen graph is inferred to be a hosted call; terms and cost were not read

What it does **not** give you: tested outputs, recommended settings or any claim about quality or speed.

---

## Three concrete entry points for a new contributor

### 1. Node-wiring trace (no GPU needed)
The Pixal3D / TRELLIS.2 graph has four KSamplers and a boolean switch, but the source research did not trace which sampler drives which stage or what the switch connects. A contributor with a text editor and the JSON file can map this and publish the result. Time: ~1–2 hours. Resource cost: none.

### 2. First-run verification (GPU required)
Pick one graph — TripoSplat is the simplest (one image in, one mesh out, one KSampler). Download the declared weights, load the template, run it once with the stored values, and record what actually happens: did it load, what did the output look like, how long did it take, what VRAM was used? That turns one documented-not-tested entry into a tested one. Publish the run log and a screenshot of the output node, not the model weights.

### 3. Hosted-call investigation (no GPU needed)
Read the TencentImageToModelNode source or any available documentation to confirm whether it calls a remote endpoint, what the endpoint is, and whether there are public terms or costs. The source research flags this as an inference, not a confirmed fact. A contributor who resolves it upgrades the record's evidence status.

---

## Attribution requirements

- Cite art_01M6A5AMHEBDCSZNEY4FGX22T2 r2 as the upstream documentary source.
- The workflow files belong to Comfy-Org (MIT per the packet LICENSE head, per the source record; this brief does not interpret that license independently).
- If you run a graph and publish outputs, note the commit you used and which weights you loaded.
- Do not re-publish workflow JSON files; link to the upstream repository instead.

---

## Resource tradeoffs at a glance

| Task | GPU needed | Hosted cost risk | Time estimate |
|---|---|---|---|
| Node-wiring trace | No | None | 1–2 h |
| First-run verification | Yes (≥ 12 GB VRAM suggested for Hunyuan3D 2.1) | None for local graphs | 2–4 h setup + run |
| Tencent node investigation | No | Read terms before running | 1 h |

---

## Suggested research request

The highest-value unresolved question is: **Does the TencentImageToModelNode make a network call, and if so, what are the endpoint, terms and cost?** This is answerable from public source code without running anything. A curator-guided research request pointing at the ComfyUI-3D-Pack or equivalent node repository would close it cleanly.

---

## What to do next

1. Read art_01M6A5AMHEBDCSZNEY4FGX22T2 r2 in full before starting.
2. Choose one entry point above that matches your current resources.
3. If you run anything, record the exact commit, weight filenames and VRAM observed — those three facts are what upgrade a documented result to a tested one.