"""adapter_stub.py — Seedance-to-ComfyUI handoff stub (MIT).
Fills the four injected fields; raises on unconfirmed rights.
Not a runnable ComfyUI client; shows the boundary logic only.
"""
from dataclasses import dataclass, field
from typing import Optional

MODEL_REFS = [
    {"filename": "wan2.2_ti2v_5B_fp16.safetensors",
     "source_url": "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged",
     "license_id": "SEPARATE_NOT_MIT"},
    {"filename": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
     "source_url": "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged",
     "license_id": "SEPARATE_NOT_MIT"},
    {"filename": "wan2.2_vae.safetensors",
     "source_url": "https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged",
     "license_id": "SEPARATE_NOT_MIT"},
]

@dataclass
class SeedanceShot:
    shot_id: str
    frame_image_url: str
    camera_move: str
    rights_confirmed: bool  # adapter MUST check; raises if False
    audio_confirmed: bool = False

@dataclass
class ComfyHandoff:
    shot_id: str
    start_image_url: str
    camera_move: str
    model_refs: list = field(default_factory=lambda: MODEL_REFS)
    execution_status: str = "pending"   # filled AFTER queue response
    output_spec: dict = field(default_factory=lambda: {
        "path_pattern": "video/ComfyUI_*.mp4",
        "format": "auto",
        "codec": "auto"
    })
    manifest_license: str = "MIT"       # this manifest only, NOT model weights
    audio_connected: bool = False

def build_handoff(shot: SeedanceShot) -> ComfyHandoff:
    if not shot.rights_confirmed:
        raise ValueError(
            f"Rights unconfirmed for shot {shot.shot_id}. "
            "Source art_01M64VM0M0VAGFKAT46JH85C6J r2 marks inputs as unconfirmed."
        )
    return ComfyHandoff(
        shot_id=shot.shot_id,
        start_image_url=shot.frame_image_url,
        camera_move=shot.camera_move,
        audio_connected=shot.audio_confirmed,
    )

# Example (raises — correct behaviour when rights unconfirmed):
if __name__ == "__main__":
    shot = SeedanceShot(
        shot_id="exp_01M64VHR5SPSVT6Z7R0JWEN2FB",
        frame_image_url="https://example.com/frame.png",
        camera_move="push-in",
        rights_confirmed=False,
    )
    try:
        h = build_handoff(shot)
    except ValueError as e:
        print(f"Blocked (expected): {e}")