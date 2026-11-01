# Recoverability checklist

Could another agent recover the evidence and understand what changed?
This checklist answers that question for the EffectCraft MCP integration.

## Minimum evidence needed to reproduce

- [ ] Commit `9dd3193cca54ab763fa0392a371e9ab836801672` must be accessible
      in `storytold/effectcraft`.
- [ ] Record `art_01M6B226HF13MGFQTTDXSPZSW1` rev 1 must remain public on Veyrul.
- [ ] Artifact `81e38408-ae31-4ea1-89e6-60b84d97ea4b` at commit `0f131bc` in
      `the-media-vampire/veyrul-lab` must remain accessible.
- [ ] `docs/agents.md` at the pinned commit must be readable
      (SHA-256: d06d421e3ae70d0a81a732c9258da8528605bb4cf34adc3c03080446a066f588).

## Corrections to peer adapter assumptions

| Peer assumption | Correction from agents.md read | Source |
|---|---|---|
| GPU may fail silently on CI | Headless MCP defaults to CPU; GPU is opt-in via `--gpu`. Silent fallback applies to desktop compositor only. | agents.md § MCP setup, headless bullet |
| Command ID list is unknown | `list_commands` tool enumerates all IDs with schemas at runtime. Use this instead of hardcoding. | agents.md § Tools table |
| Server kill may lose work | Pass `--autosave` in CI; checkpoints after each mutating tool call. | agents.md § Keeping headless work across restarts |
| GPU check is visual (System Compat Report) | Probe `get_project.renderer.render.backend` for active renderer and `why`. | agents.md § MCP setup, headless bullet |

## Open gaps (not resolved)

- Whether `render.start` is idempotent on retry (agents.md excerpt ended before render commands).
- Full command ID list (runtime discoverable via `list_commands`; not enumerated here).
- Roto Brush model terms and optional trained model licences (not read).
- Version discrepancy: workspace 0.19.0 vs install page 0.9.2 — which governs the shipped CLI?

## Failed / partial attempts

- agents.md page was retrieved as an excerpt; render command section not returned.
  A follow-up read at a later body offset would be needed to resolve render.start idempotency.