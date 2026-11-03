"""MiniMax-H3 Few-Step LoRA loader guard.
Source: art_01M6FG17EJ5VRRZ6BNZKEMXN8M r1. NOT EXECUTED; logic only.
Licence labels are record statements, not rights determinations.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

LoRAVariant = Literal[
    "pdmd_4step_original","pdmd_4step_comfyui",
    "pdmd_2step_comfyui","turbo","taomate_3step",
]

@dataclass(frozen=True)
class Spec:
    variant: LoRAVariant
    strength: float
    steps_min: int; steps_rec: int; steps_max: int
    cfg: float
    scheduler: str
    loader_node: str
    patch_signal: str   # record-stated; not measured
    silent_fail: str
    license_label: str

SPECS: dict[LoRAVariant, Spec] = {
    "pdmd_4step_original": Spec(
        "pdmd_4step_original",1.0,4,4,4,0.0,
        "H3 base released config (shift 12/3)",
        "NOT ComfyUI-native — diffusers keys skip silently",
        "N/A — use comfyui conversion",
        "Diffusers key layout; all keys silently skipped by ComfyUI loader",
        "Apache-2.0 (card statement)",
    ),
    "pdmd_4step_comfyui": Spec(
        "pdmd_4step_comfyui",1.0,4,4,4,0.0,
        "H3 (shift 12 video / 3 audio)",
        "LoraLoaderModelOnly",
        "208 target keys present, shapes match, tensors numerically identical",
        "Earlier uploads broken; confirm v6 bf16 file",
        "Apache-2.0; MiniMax H3 weights keep own licence",
    ),
    "pdmd_2step_comfyui": Spec(
        "pdmd_2step_comfyui",1.0,2,2,2,0.0,
        "H3 (shift 12 video / 3 audio)",
        "LoraLoaderModelOnly",
        "468 numeric checks passing against originals (exact fp32)",
        "mlp.fc1 lora_B halves swapped (SwiGLU order fix); fp32 copy larger, no GPU benefit",
        "Apache-2.0; MiniMax-H3 keeps own terms",
    ),
    "turbo": Spec(
        "turbo",1.0,4,6,8,0.0,
        "simple",
        "LoRA node between model-loader and sampler; SamplerCustomAdvanced",
        "(none stated in records)",
        "Preview/still-training; v4 EMA smears at 4 steps with large fast motion",
        "Apache-2.0 (label on preview; base model licence not reviewed in record)",
    ),
    "taomate_3step": Spec(
        "taomate_3step",1.0,3,3,3,1.0,
        "Euler + simple or linear FlowMatch",
        "LoraLoader or LoraLoaderModelOnly",
        "208 patches attached, no missing-key warnings",
        "CFG > 1.0 burns the distilled ODE",
        "MiniMax H3 Community License Agreement (record statement)",
    ),
}

def preflight(variant: LoRAVariant, cfg: float, steps: int, strength: float) -> list[str]:
    """Return constraint violations. Does not load or run anything."""
    s = SPECS[variant]; errors: list[str] = []
    if strength != s.strength:
        errors.append(f"strength {strength} != required {s.strength} (rescales distillation delta)")
    if not (s.steps_min <= steps <= s.steps_max):
        errors.append(f"steps {steps} outside [{s.steps_min},{s.steps_max}]")
    if variant == "taomate_3step" and cfg > 1.0:
        errors.append(f"CFG {cfg} > 1.0 burns distilled ODE")
    if variant == "pdmd_4step_original":
        errors.append("Use pdmd_4step_comfyui for ComfyUI; diffusers keys silently skipped")
    return errors