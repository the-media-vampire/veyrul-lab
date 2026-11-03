# MagCache + NetDist — Integration Contract

Source: art_01M6FFSA60BEJ8YJHKARKE2QB3 r1 (documented, not run)

## What each pack contributes

| Concern | MagCache | NetDist |
|---|---|---|
| Unit of work | Single model inference, speed-up via caching | Dispatch of a full workflow JSON to a remote ComfyUI instance |
| Node position | Between Load Diffusion Model and sampler | Wraps the *entire* workflow from one instance to another |
| State it holds | In-process cache keyed to timestep magnitude | HTTP queue to remote; latent .npy or image base64 |
| Licence | Apache 2.0 (as stated in licence file) | Apache 2.0 (as stated in licence file) |

## Combination ordering — the critical constraint

MagCache node must live **inside** the worker instance that holds the model.
NetDist queue/fetch nodes live on the **dispatcher** instance.

Valid ordering (per README statements, not tested):

```
[Dispatcher instance]
  Queue Simple → FetchRemote

[Worker instance]
  Load Diffusion Model
    └─ MagCache node         ← cache is local to this process
         └─ (optional) Compile Model node
              └─ sampler → VAE decode → Save Image
```

Invalid: placing MagCache on the dispatcher. The cache is in-process;
shipping the model across the network boundary defeats the mechanism.

## Interface points

### 1. Workflow JSON boundary (NetDist advanced mode)
NetDist advanced nodes accept a workflow JSON as input.
That JSON must include the MagCache node with its three parameters:
- `magcache_thresh`
- `retention_ratio`
- `magcache_K`

These are per-model values. The README provides a table;
the table values must travel with the workflow JSON to each worker.
If a worker runs a different model family, the parameters are wrong
and the README says to decrease thresh and K when quality is low.

### 2. Latent handoff (NetDist latent nodes)
NetDist can pass latents between instances via .npy files.
MagCache operates before the sampler, on the model not on latents,
so this boundary is downstream of MagCache — compatible by design.

### 3. Seed / duplicate-image risk
NetDist README warns: reusing a seed across multiple queue calls
causes duplicate images. MagCache caches by timestep magnitude, not seed.
These are orthogonal; no interaction failure is documented.

## Shared assumptions that must both hold

1. **Same model family per worker.** MagCache parameters are per-model.
   NetDist can send the same workflow to multiple workers.
   If workers run different model families, the MagCache table values
   will be wrong on at least one worker — the README gives no fallback.

2. **No progress bar on FetchRemote.** NetDist README states this explicitly.
   A long MagCache compile (torch.compile, first run) will appear as silence
   on the dispatcher side. Users need to monitor the worker directly.

3. **Compile Model node first-run latency.**
   torch.compile on the worker adds significant first-run time.
   NetDist timeout behaviour is not documented in the README;
   this is an unresolved gap (see research request).

4. **Licence compatibility.** Both packs are Apache 2.0 as stated.
   Model weights (FLUX, Wan2.1, HunyuanVideo, Chroma) carry their own
   licences which were NOT read in the source record — non-commercial
   terms may apply and must be checked separately before distribution.

## What this contract does NOT resolve

- NetDist timeout value (not stated in README)
- Per-model-family MagCache parameter values (table not repeated in source)
- Model weight licences (not read in source record)
- Whether torch.compile output is reused across NetDist re-queues