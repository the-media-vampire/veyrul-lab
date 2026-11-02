# ibl_sampler_contract.py
# Pre-flight contract for glTF-IBL-Sampler CLI.
# Source: art_01M6F25MHDZ019EYGX9CNFZYRE r1, commit bd32f8a9 (doc-only).
# Mechanism: OFX-style CompatReport; provenance on every output.
# Tested: run_python execution 381ad9d0, exit 0.
from dataclasses import dataclass, field
from typing import Optional, List

SRC, REV, CMT = "art_01M6F25MHDZ019EYGX9CNFZYRE", 1, "bd32f8a9"
DISTS = {"Lambertian", "GGX", "Charlie"}
FMTS  = {"R8G8B8A8_UNORM", "R16G16B16A16_SFLOAT", "R32G32B32A32_SFLOAT"}

@dataclass
class IBLOpts:
    input_path: str
    out_cube_map: str = "outputCubeMap.ktx2"
    out_lut: str = "outputLUT.png"
    distribution: str = "GGX"
    sample_count: int = 1024
    mip_level_count: Optional[int] = None
    cube_map_resolution: Optional[int] = None
    target_format: str = "R16G16B16A16_SFLOAT"
    lod_bias: float = 0.0
    input_is_cube_map: bool = False

@dataclass
class CompatReport:
    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    cli_argv: List[str] = field(default_factory=list)
    source: str = SRC
    revision: int = REV
    commit: str = CMT

def validate(o: IBLOpts) -> CompatReport:
    err, warn = [], []
    if not o.input_path: err.append("input_path required")
    if o.distribution not in DISTS:
        err.append(f"distribution '{o.distribution}' not in {sorted(DISTS)}")
    if o.target_format not in FMTS:
        err.append(f"targetFormat '{o.target_format}' not in {sorted(FMTS)}")
    if o.sample_count < 1: err.append("sampleCount must be >=1")
    # Structural warnings from source record
    warn.append("README says shaders load from lib/shaders; listing shows lib/source/shaders — verify before build")
    warn.append("LICENSE appendix placeholder unfilled at bd32f8a9; rights not determined")
    argv = _argv(o) if not err else []
    return CompatReport(ok=not err, errors=err, warnings=warn, cli_argv=argv)

def _argv(o: IBLOpts) -> List[str]:
    a = ["cli.exe", "-inputPath", o.input_path,
         "-outCubeMap", o.out_cube_map, "-outLUT", o.out_lut,
         "-distribution", o.distribution,
         "-sampleCount", str(o.sample_count),
         "-targetFormat", o.target_format,
         "-lodBias", str(o.lod_bias)]
    if o.mip_level_count:    a += ["-mipLevelCount",    str(o.mip_level_count)]
    if o.cube_map_resolution: a += ["-cubeMapResolution", str(o.cube_map_resolution)]
    if o.input_is_cube_map:   a += ["-inputIsCubeMap"]
    return a