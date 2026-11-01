# Seedance 2.5 → ComfyUI-3D-Pack: Sequential Composition Contract

## Sources
- art_01M64VK8QZGMMWD7HW0B566NTP revision 2 (Seedance blue-hall observations)
- art_01M6AATGSEDBC6G46272K4Y7Q8 revision 1 (ComfyUI-3D-Pack README and workflow JSON, not run)

## What each system produces / consumes

| System | Output type | Key properties (observed) |
|---|---|---|
| Seedance 2.5 | Video frames | ~1.7 s apart, sampled; pixel format unstated; character design: rounded cartoon-3D |
| ComfyUI-3D-Pack | 3D mesh (e.g. TripoSG, TRELLIS, Hunyuan3D) | Input: single IMAGE node; pixel format: unstated in workflow JSON |

The handoff type is IMAGE (one frame extracted from the video). This is the **single binding point** and the first place drift can occur.

## Explicit interface assumptions (must all hold for the pipeline to run)

### A — Pixel format match
The frame extracted from Seedance output must match the pixel format expected by the 3D loader node. Neither record states the pixel format. **This assumption is unverifiable from available evidence.**

### B — Character framing suitability
The blue-hall beat structure places the bearded man in close-up during the third beat. A close-up of a single subject is better suited to single-image-to-3D (TripoSG, TRELLIS, Hunyuan3D 2.1) than a wide shot of ranked figures. Beat selection is a deliberate editorial choice, not automatic.

### C — Background complexity
All three 3D loaders (TripoSG, TRELLIS, Hunyuan3D 2.1) are documented as single-object pipelines. The wide hall frames contain many helmeted figures. Using a wide frame will produce a multi-object mesh or fail silently.

### D — Seed and determinism
Seedance ran without a seed set (art_01M64VK8QZGMMWD7HW0B566NTP r2). The close-up frame will vary across runs. The 3D-Pack workflows store explicit seeds (e.g. TripoSG: 42, fixed; TRELLIS: 685921954948183, randomize). The composition is non-deterministic end-to-end unless Seedance is re-run with a fixed seed.

### E — License chain
Seedance: rights on the article are 'permitted' for hosting and redistribution (no upstream license cited for the model output). ComfyUI-3D-Pack: no license is cited or interpreted in art_01M6AATGSEDBC6G46272K4Y7Q8. **The license chain for any combined output is unknown and must be resolved before redistribution.**

## Failure mode table

| Assumption | Silent failure? | Detection point |
|---|---|---|
| A — pixel format | Yes — wrong color space may produce a distorted mesh with no error | Visual inspection of mesh |
| B — wrong beat selected | Yes — wide frame produces crowd mesh | Frame preview before 3D submission |
| C — background complexity | Partial — mesh is produced but is semantically wrong | Mesh viewer after decimate |
| D — non-determinism | No error, but results are not reproducible | Re-run comparison |
| E — license | No runtime error | Legal review |

## Minimal adapter schema (proposal, untested)

This describes a manual step between the two systems, not executable code:

```
Seedance run
  └─ select beat 3 frame (close-up, ~frames 5–7 of 12 sampled)
       └─ export as PNG, sRGB, square-cropped to subject
            └─ place in ComfyUI input folder
                 └─ load via IMAGE node → TripoSG or TRELLIS workflow
```

The crop step is the only value-adding transform; it isolates the single-subject assumption that all three 3D loaders require.

## What remains unknown (research queue candidates)
1. Pixel format at Seedance video output boundary.
2. Whether ComfyUI-3D-Pack IMAGE nodes accept sRGB or expect linear.
3. License terms for Seedance 2.5 model outputs.
4. Actual VRAM requirements for TripoSG or TRELLIS with a 768×768 input frame.