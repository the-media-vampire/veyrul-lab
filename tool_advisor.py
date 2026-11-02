"""tool_advisor.py
Tool-selection advisor for KTX-Software, basis_universal, draco, xatlas.
All data is documentation-derived: art_01M6EV5HYREYVCK02NZD5B3S9E r1.
Nothing was built, installed or run from any of the four tools.
Licence notes are reported as written; none is interpreted here.
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ToolProfile:
    name: str
    assets: List[str]
    platforms: List[str]
    bindings: List[str]
    caveat: str
    licence_note: str
    not_tested: List[str]

TOOLS = [
    ToolProfile(
        "KTX-Software",
        assets=["texture","ktx2"],
        platforms=["linux","macos","windows","web","android"],
        bindings=["c","javascript","java","python"],
        caveat="Git LFS required; web=libktx read-only only; licence file is INDEX of 13.",
        licence_note="LICENSES dir: 13 files Apache-2.0..Zlib. Not interpreted.",
        not_tested=["library","subcommands","wrappers","build","licence mixture"],
    ),
    ToolProfile(
        "basis_universal",
        assets=["texture","ktx2","hdr-texture","ldr-texture"],
        platforms=["linux","macos","windows","web","wasi"],
        bindings=["c","cpp","javascript","python"],
        caveat="SSE4.1 speed claim is authors' figure; Python support 'early'.",
        licence_note="LICENSES dir: Apache-2.0, BSD-3-Clause, MIT. Not interpreted.",
        not_tested=["codecs","transcoding targets","tool","build"],
    ),
    ToolProfile(
        "draco",
        assets=["mesh","point-cloud","gltf"],
        platforms=["linux","macos","windows","web","ios","android"],
        bindings=["cpp","javascript"],
        caveat="draco_transcoder needs CMake flag DRACO_TRANSCODER_SUPPORTED=ON + submodules.",
        licence_note="Single LICENSE file. Not interpreted.",
        not_tested=["compression claims","applications","decoders","build"],
    ),
    ToolProfile(
        "xatlas",
        assets=["mesh","uv-atlas"],
        platforms=["any"],
        bindings=["cpp","c"],
        caveat="Integration: add xatlas.cpp+xatlas.h only; Debug on Windows degrades perf (README).",
        licence_note="Single LICENSE file. Not interpreted.",
        not_tested=["atlas quality","api","build"],
    ),
]

def advise(asset: str, platform: str, binding: Optional[str] = None) -> list:
    """Return tools scored by documented match. Higher score = better fit."""
    out = []
    for t in TOOLS:
        score, reasons, flags = 0, [], []
        if asset in t.assets:
            score += 3; reasons.append(f"asset={asset}")
        if platform in t.platforms or "any" in t.platforms:
            score += 2; reasons.append(f"platform={platform}")
        else:
            flags.append(f"platform '{platform}' NOT in documented list")
        if binding:
            if binding in t.bindings:
                score += 1; reasons.append(f"binding={binding}")
            else:
                flags.append(f"binding '{binding}' not documented")
        if score > 0:
            out.append(dict(tool=t.name, score=score, reasons=reasons,
                            flags=flags, caveat=t.caveat,
                            licence_note=t.licence_note,
                            not_tested=t.not_tested))
    return sorted(out, key=lambda x: -x["score"])