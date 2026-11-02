# Known Assumptions and Open Issues

Source: art_01M6F25MHDZ019EYGX9CNFZYRE r1, commit bd32f8a9

| Assumption | Risk |
|---|---|
| Shader default path in README (`lib/shaders`) differs from file listing (`lib/source/shaders`) | Build may fail or load wrong shaders |
| `IBLSAMPLER_EXPORT_SHADERS` CMake option defaults to OFF | Shaders not copied unless explicitly set |
| LICENSE appendix copyright placeholder is unfilled | Rights determination not performed |
| `.gitmodules` not archived; submodule pins unknown | STB and glslang versions unverified |
| KTX-Software requires manual install with a PR fix | `cmake find_package` may fail without it |
| mipLevelCount and cubeMapResolution have "optimal" defaults | Actual algorithm not verified |
| Nothing was built or run; all options as documented | Actual CLI behaviour untested |