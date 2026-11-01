"""provenance_envelope.py
Traceability wrapper for look_branch_contract.adapter (artifact 936bb216).
Source observation: art_01M64VK50F7QM10TWFSS9HRXBQ r2
Execution receipt: run ce28c6b6-f170-4e5e-954e-5e0035236342

Problem: adapter() routes compositing params by look_target but does not
record which Seedance run, beat or timestamp produced the frame. Without
those fields a future agent cannot reconstruct the mesh-to-video chain.
"""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class ProvenanceEnvelope:
    """Four minimum traceability fields. None = gap recorded, not hidden."""
    source_run_id: Optional[str]       # e.g. exp_01M64VCHNCCB3HP8DAXC7TX2DP
    beat_label: Optional[str]          # e.g. 'two_shot'
    frame_index: Optional[int]         # 0-based within sampled frames
    source_timestamp_s: Optional[float]  # seconds into source video

    def validate(self):
        missing = [f for f, v in asdict(self).items() if v is None]
        if missing:
            return False, f"Incomplete envelope - unresolved: {missing}"
        return True, "OK"

def wrapped_adapter(look_target, envelope, adapter_fn=None):
    """Call adapter_fn(look_target) and attach the provenance envelope."""
    if adapter_fn is None:
        adapter_fn = _stub_adapter
    params = adapter_fn(look_target)
    ok, msg = envelope.validate()
    return {"compositing_params": params,
            "provenance": asdict(envelope),
            "provenance_complete": ok,
            "provenance_note": msg}

def _stub_adapter(look_target):
    """Mirrors artifact 936bb216 contract for isolated testing."""
    branches = {
        "3d_cinematic": {"shading_mode": "physically_based",
                         "compositing_hint": "preserve_normals",
                         "face_geometry": "volumetric"},
        "anime_first":  {"shading_mode": "flat_cel",
                         "compositing_hint": "posterize_before_key",
                         "face_geometry": "planar"},
    }
    if look_target not in branches:
        raise ValueError(f"Unknown look_target: {look_target!r}")
    return {**branches[look_target], "look_target": look_target}