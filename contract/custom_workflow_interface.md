# Krita AI Diffusion — Custom Workflow Interface Contract

**Basis:** Maintainer changelog statements in v1.52.0 and v1.53.0 release notes,
as documented in art_01M6A17B8GRMEXFF8JFTSZTYGM revision 1 (source_inspected, not_run).
Nothing here was tested against a running plugin or ComfyUI instance.

---

## The two failure modes the changelog reveals

### Failure A — Architecture mismatch (fixed in v1.52.0)
> "the model architecture not being set correctly from the style in custom workflows"

Mechanism: The plugin reads a *style* object and derives the model architecture
(e.g. SDXL, Flux, SD1.5) from it. In custom workflows this derivation was broken —
meaning the plugin was passing an architecture hint that did not match the loaded model.
Result: the ComfyUI graph received a mismatched loader/sampler pair and presumably
failed silently or produced wrong output.

**Contract assumption A:** The style name selected in Krita must resolve to the same
architecture family as the checkpoint node in the custom workflow. These are two
independent bindings; if only one is changed, the contract breaks.

### Failure B — Duplicate parameter names (warned in v1.53.0)
> "a warning for duplicate parameter names in a custom workflow"

Mechanism: Custom workflows expose named parameters (e.g. `cfg`, `steps`, `seed`)
that Krita maps to its UI controls. If the same parameter name appears more than once
in the workflow JSON, the mapping is ambiguous. Pre-v1.53.0 this was silent.

**Contract assumption B:** Every exposed parameter name in a custom workflow must be
unique within that workflow. Duplicates now produce a warning; behaviour with
duplicates present is not stated (not tested).

---

## Stable interface points (stated across all three releases)

| Boundary | What crosses it | Stated constraint |
|---|---|---|
| Style → Plugin | Architecture tag | Must match checkpoint in workflow |
| Plugin → ComfyUI | Named parameters | Must be unique per workflow |
| ComfyUI → Plugin | IMAGE output | Format not specified in release notes |
| Managed server | CUDA / PyTorch / ComfyUI version | v1.53.0: CUDA 13, PyTorch 2.13, latest ComfyUI |

---

## Version-compatibility break to track

v1.54.0-pre states the plugin no longer works with Krita 5.x. Any custom workflow
build targeting Krita 5 + v1.52.0 or v1.53.0 is not forward-compatible with v1.54.0-pre
without a Krita 6 migration. The Qt5 → Qt6 transition is the stated cause.

---

## Quantisation model note (v1.53.0)

Nunchaku model variants (Flux 1, Flux 1 Kontext, Qwen, Z-Image) were removed from
the managed server. int8, int4 and ConvRot formats are now supported instead.
A custom workflow that loaded a Nunchaku checkpoint path will silently target a
non-existent model after this upgrade unless the path is updated.

**Contract assumption C:** After upgrading to v1.53.0, any custom workflow with a
hardcoded Nunchaku checkpoint path must be updated to an alternative checkpoint.

---

## What this contract does NOT cover

- IMAGE pixel format at the ComfyUI output boundary (not stated in release notes)
- VRAM budget for any model combination (not stated anywhere in these notes)
- Pre-processing requirements (background removal, square crop) — absent from notes
- Behaviour when a warned duplicate parameter is left in place
- Cloud watermarking effect on workflow outputs (stated EU-only, local unaffected)