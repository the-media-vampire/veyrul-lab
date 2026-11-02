# OFX plug-in / host integration contract

Source: `art_01M6EGFQFT57E8WEDX28PT6SQ6` revision 1, commit `1769a91c`.  
Nothing was built, loaded or linked to produce this contract.

## Interface boundary

OpenFX separates *interface definition* (pure C headers under `include/`) from
*runtime* (host process + loaded native plug-in code). That boundary is the only
composable seam this adapter touches.

## Capabilities modelled

| Property | OFX version added | Hard fail if missing? |
|---|---|---|
| `kOfxImageEffectPropCPURenderSupported` | 1.5.1 | No — warning only |
| `kOfxImageEffectPropThumbnailRender` | 1.5.1 | No |
| `kOfxImageEffectPropNoSpatialAwareness` | 1.5.1 | No |
| `OFX_SUPPORTS_OPENCLRENDER` | 1.5 | Yes if host needs GPU |
| `OFX_SUPPORTS_CUDARENDER` | 1.5 | Yes if host needs GPU |
| Metal support | 1.5 | Yes if host needs GPU |
| `OfxDrawSuite` | 1.5 | Yes if host needs draw |
| `DialogSuite` | 1.4 | No (not modelled here) |
| `kOfxParamPropColourManagement` | NEXT (unstable) | No — warning only |

## Provenance assumption

The `CompatReport` carries `source_record`, `source_revision`, and `ofx_commit`
on every output. If a downstream pipeline strips these fields, the version-gating
rationale is orphaned — the same failure mode as stripping a provenance stamp from
an ad-row in a data pipeline.

## Licence (as documented, not interpreted)

- Headers and support library: `BSD-3-Clause`  
  (LICENSE.md, contributing guide)
- README, install.md, CONTRIBUTING.md: `CC-BY-4.0`  
  (SPDX comment in each file; differs from LICENSE.md — reconciliation not performed here)

## Open assumptions (not tested)

1. The duplicate wording for `OFX_SUPPORTS_OPENCLRENDER` and
   `OFX_SUPPORTS_CUDARENDER` (both described as "OpenGL render support" in
   install.md) may reflect a copy-paste error; the actual CMake behaviour
   is not confirmed without a build.
2. `kOfxParamPropColourManagement` is next-release only; its ABI stability
   is unknown.
3. Security model: plug-ins are native code running inside the host process;
   the security policy states loading one is equivalent to running arbitrary
   native code (documented, not independently verified).
4. Supported versions table in the security policy lists `main` and `1.4.x`;
   the release notes begin at `1.5.1` — the discrepancy is noted, not resolved.