# Seedance → ComfyUI Wan 2.2 Coverage Handoff Contract v0.1

Sources: art_01M64VM0M0VAGFKAT46JH85C6J r2 (Seedance session), art_01M5ZQV4H0PD17B0X5AAEN1VM4 r1 (ComfyUI template).

## Interface: what the adapter receives (Seedance side)

| Field | Source | Type | Notes |
|---|---|---|---|
| `shot_id` | Seedance run ID | string | One of six candidate exp IDs |
| `frame_image` | Seedance output frame | file/URL | Used as `start_image` for i2v; rights UNCONFIRMED per source |
| `camera_move` | prompt field | string | e.g. "push-in", "swing through fence" |
| `people_present` | prompt/observation | string[] | e.g. ["young man white tee", "capped man"] |
| `audio_requested` | prompt flag | bool | Audio not reviewed in source; treat as unknown |

## Interface: what the adapter must inject (ComfyUI side)

These four fields are ABSENT from ComfyUI's native workflow JSON and must be filled by the adapter:

| Field | Required value | Failure if absent |
|---|---|---|
| `model_refs` | `[{filename, source_url, license_id}]` — see table below | Filename stays unresolvable outside local deploy |
| `execution_status` | Set from queue API response AFTER run; never pre-fill | Silent crash reads as success |
| `output_spec` | `{path_pattern: "video/ComfyUI_*.mp4", format: "auto", codec: "auto"}` | Downstream consumers get untyped path string |
| `manifest_license` | `"MIT"` (this manifest only) | Consumers conflate manifest license with model weights license |

## Model reference table (from art_01M5ZQV4H0PD17B0X5AAEN1VM4 r1)

| filename | folder | source_url | size | weight_license |
|---|---|---|---|---|
| wan2.2_ti2v_5B_fp16.safetensors | diffusion_models | Comfy-Org/Wan_2.2_ComfyUI_Repackaged | 9.31 GB | SEPARATE — not MIT |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | text_encoders | Comfy-Org/Wan_2.1_ComfyUI_repackaged | 6.27 GB | SEPARATE — not MIT |
| wan2.2_vae.safetensors | vae | Comfy-Org/Wan_2.2_ComfyUI_Repackaged | 1.31 GB | SEPARATE — not MIT |

## Assumptions the adapter must validate before handoff

1. **Frame image rights**: source marks linked inputs as unconfirmed for rights and likeness. An adapter MUST gate on confirmed rights before passing a Seedance output frame as `start_image`.
2. **Audio**: audio was not reviewed in the six runs. The ComfyUI graph has an unconnected audio input on CreateVideo. Adapter should leave audio unconnected unless source audio is confirmed clear.
3. **Single-run variance**: six runs, no seed set. The same prompt will not reproduce the same frame. Adapter contracts should capture the specific frame artifact ID, not regenerate.
4. **Minimum ComfyUI version**: 0.3.46 (from template index, art_01M5ZQV4H0PD17B0X5AAEN1VM4 r1).

## What this contract does NOT cover

- Model weight license terms (must be verified separately at each Comfy-Org repo)
- Likeness/identity rights for the people in the Seedance frames
- VRAM requirements (not stated in source)
- Output quality or timing (not observed; 121 frames @ 24 fps = ~5 s by arithmetic)