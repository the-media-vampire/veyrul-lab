"""OFX plug-in / host compatibility adapter (stub).

Derived from properties and version gating documented in
art_01M6EGFQFT57E8WEDX28PT6SQ6 r1 (commit 1769a91c).
No plug-in is built, loaded or linked here.

License notes (as documented, not interpreted):
  - OFX headers and support lib: BSD-3-Clause
  - README, install.md, CONTRIBUTING.md: SPDX CC-BY-4.0 per file headers
"""
from dataclasses import dataclass, asdict, field
from typing import List
import json


@dataclass
class PluginCaps:
    """Declarative capability record modelled on OFX image-effect properties."""
    name: str
    # Added in OFX 1.5.1 (art_01M6EGFQFT57E8WEDX28PT6SQ6 r1)
    cpu_render: bool        # kOfxImageEffectPropCPURenderSupported
    thumbnail: bool         # kOfxImageEffectPropThumbnailRender
    no_spatial_awareness: bool  # kOfxImageEffectPropNoSpatialAwareness
    # Added in OFX 1.5
    gpu_opencl: bool        # OFX_SUPPORTS_OPENCLRENDER
    gpu_cuda: bool          # OFX_SUPPORTS_CUDARENDER
    gpu_metal: bool         # Metal support
    draw_suite: bool        # OfxDrawSuite (on-screen drawing without OpenGL)
    dialog_suite: bool      # Dialog Suite (added 1.4)
    # Next-release (unstable per source)
    colour_managed: bool    # kOfxParamPropColourManagement


@dataclass
class HostReqs:
    """What the host demands from a plug-in at discovery time."""
    min_ofx_version: tuple  # e.g. (1, 5)
    needs_gpu: bool
    needs_draw_suite: bool
    needs_colour_management: bool


@dataclass
class CompatReport:
    plugin: str
    compatible: bool
    missing: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    # Provenance: always carry the source so downstream knows
    # which version of the docs this logic derives from.
    source_record: str = "art_01M6EGFQFT57E8WEDX28PT6SQ6"
    source_revision: int = 1
    ofx_commit: str = "1769a91c"
    stub_note: str = "No plug-in was built, loaded or linked"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


def check_compatibility(p: PluginCaps, h: HostReqs) -> CompatReport:
    """Match plug-in capabilities against host requirements.

    Version gating follows the documented feature timeline:
      1.4  DialogSuite, OfxProgressSuiteV2, ofxOld.h
      1.5  DrawSuite, GPU (OpenCL/CUDA/Metal), GPU flag on release bundles
      1.5.1 kOfxImageEffectPropCPURenderSupported, ThumbnailRender,
            NoSpatialAwareness
      NEXT kOfxParamPropColourManagement  <-- treat as unstable
    """
    missing: List[str] = []
    warnings: List[str] = []

    if h.min_ofx_version >= (1, 5) and h.needs_gpu:
        if not (p.gpu_opencl or p.gpu_cuda or p.gpu_metal):
            missing.append(
                "No GPU render declared; host requires GPU (feature added 1.5, "
                "OFX_SUPPORTS_OPENCLRENDER / OFX_SUPPORTS_CUDARENDER / Metal)"
            )

    if h.min_ofx_version >= (1, 5) and h.needs_draw_suite and not p.draw_suite:
        missing.append(
            "OfxDrawSuite required by host but not declared by plug-in "
            "(added OFX 1.5)"
        )

    # Colour management: next-release, warn but don't hard-fail
    if h.needs_colour_management and not p.colour_managed:
        warnings.append(
            "kOfxParamPropColourManagement required by host; this property "
            "is in next-release notes only — treat as unstable interface "
            "(art_01M6EGFQFT57E8WEDX28PT6SQ6 r1)"
        )

    if not p.cpu_render:
        warnings.append(
            "kOfxImageEffectPropCPURenderSupported not declared (added 1.5.1); "
            "thumbnail pipelines may silently assume CPU fallback"
        )

    return CompatReport(
        plugin=p.name,
        compatible=(len(missing) == 0),
        missing=missing,
        warnings=warnings,
    )