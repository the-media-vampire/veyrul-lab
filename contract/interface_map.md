# ComfyUI-3D-Pack: Image-to-3D Interface Contract

Source: art_01M6AATGSEDBC6G46272K4Y7Q8 r1 (source_inspected, not_run)

## Shared boundary

Every image-to-3D pipeline in the seven documented workflows accepts one image
and produces one mesh (optionally textured). Stable two-point contract:

  INPUT  : IMAGE  -- a single reference image
  OUTPUT : MESH   -- a 3-D mesh, sometimes with UV texture

## Per-model documented interface (stored values, not run)

| Node type                       | Loader model ID (stored)          | Key widget slots (inferred order)                   |
|---------------------------------|-----------------------------------|-----------------------------------------------------|
| Hunyuan3D 21 ShapeGen           | hunyuan3d-dit-v2-1                | seed, mode, steps=30, cfg=7.5, res=256, bool x2     |
| Hunyuan3D V2 ShapeGen MV        | Hunyuan3D-2mv-Turbo               | seed, mode, steps=5, cfg=5, res=256                 |
| PartCrafter Generate            | (not listed in excerpt)           | n_parts=4, seed, mode, res=1024, steps=50, cfg=7    |
| MVAdapter IG2MV                 | stabilityai/sdxl-base-1.0         | prompt, neg, steps=50, cfg=3, w=768, h=768, seed    |
| TripoSG I23D Model              | VAST-AI/TripoSG                   | seed=42, fixed, cfg=7, steps=50, octree depths x3   |
| Trellis Structured 3D Latents   | jetx/TRELLIS-image-large          | seed, mode, cfg=7.5, steps=12,3,12                  |
| StableGen Trellis Image To 3D   | trellis-normal-v0-1 + dinov2      | mode=single, seed, cfg=7.5, steps=12,3,12, thr=0.95 |

Slot labels are inferred from TripoSG (only file with field names).
Unlabelled slots in other files are positional; treat labels as proposals.

## Combination assumptions that must hold

1. IMAGE format: sRGB uint8 assumed; actual requirement not stated in files.
2. Seed contract: all files store seed + seed_mode. Reproducibility requires
   switching mode from 'randomize' to 'fixed' and recording the seed value.
3. Resolution: stored values differ per model (256, 1024, 768x768). A mesh
   consumer must not assume a fixed resolution.
4. Mesh format: not named in any of the seven files. A converter node is
   required before any downstream renderer that expects a specific format.
5. Texture: only Hunyuan3D 2.1 chains TexGen after ShapeGen. All others
   produce an untextured mesh. Adding texturing to another pipeline requires
   a second loader and a mesh+image input not present in the documented files.
6. VRAM: only Era3D has a stated figure (>=16 GB). Two workflows build a C++
   extension at runtime. Parallel model loading budget is unknown.

## Minimal adapter pattern (not run)

  [KSampler] -> [VAE Decode] -> IMAGE
                                  |
       [Load Diffusers Pipeline: <model_id>]
                                  |
       [<Comfy3D ShapeGen node>: seed, cfg, steps, resolution]
                                  |
                               MESH
                                  |
       [Save Mesh / Decimate Mesh / optional TexGen]

The pipeline loader and its ShapeGen node are a bound pair; do not separate.
The only cross-workflow contract is IMAGE in, MESH out.