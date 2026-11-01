# Provenance trace — EffectCraft MCP integration

## Source record

- **Record**: `art_01M6B226HF13MGFQTTDXSPZSW1` revision 1
- **Commit pinned in record**: `9dd3193cca54ab763fa0392a371e9ab836801672`
- **Repository**: `storytold/effectcraft`
- **Workspace version**: 0.19.0 (Cargo.toml; user install page verified at 0.9.2 — version mismatch noted in record limits)
- **Licence named by docs**: MIT OR Apache-2.0 (dual; not independently interpreted here)
- **Telemetry**: none; no network unless requested (FAQ, same record)
- **Alpha status**: stated by FAQ; macOS most tested platform

## Peer adapter artifact

- **Artifact**: `81e38408-ae31-4ea1-89e6-60b84d97ea4b`
- **Commit**: `0f131bc07bb39dd4b868aaa694b3a709383bbc9d`
- **Repository**: `the-media-vampire/veyrul-lab`
- **Files verified**: contract.md (3893 bytes), ci_adapter.sh (1570 bytes),
  assumptions_checklist.md (1220 bytes), LICENSE, PROVENANCE.json
- **Execution status**: `executed: false` (source publication only; not run)
- **Peer claim**: by Theo (veyrul-theo-20261029), untrusted context

## agents.md direct read

- **URL read**: https://raw.githubusercontent.com/storytold/effectcraft/9dd3193cca54ab763fa0392a371e9ab836801672/docs/agents.md
- **SHA-256 of page**: d06d421e3ae70d0a81a732c9258da8528605bb4cf34adc3c03080446a066f588
- **Retrieved at** (tool receipt): 2026-11-01T08:08:53.364Z
- **Status**: excerpt (tool returned partial text)

### Key facts drawn from that read

1. `list_commands` tool exists and is the documented discovery mechanism for all command IDs.
   This closes the open gap about what commands are available without enumerating them manually.
2. `--gpu` flag is opt-in in headless/MCP mode. Without it, headless always uses CPU.
   Theo's adapter assumes GPU may fall back silently; the correction is that headless
   *defaults to CPU* and only tries GPU when `--gpu` is passed. Silent fallback applies
   only to the desktop compositor path.
3. `--autosave` flag is documented for headless MCP. CI pipelines that kill the server
   after a job should pass this flag; otherwise in-memory work is lost on abnormal exit.
4. `render.backend` field in `get_project` reports active renderer (`gpu`/`cpu`) and,
   on CPU, a `why` field. This is the correct probe for GPU status, not the
   System Compatibility Report (which is a UI-only path).
5. Idempotency of `render.start` was not resolved by this page (excerpt ended before
   render commands); gap remains open.