# EffectCraft ↔ CI Render Pipeline — Integration Contract

## Interface boundary

EffectCraft exposes every action as a JSON engine command with a stable `id`
and `params` field, delivered over MCP (stdio or bridge mode on port 9877) or
the CLI.  This is the only stable interface documented at commit 9dd3193c.

The CI side sends commands; EffectCraft replies with a result or an **unknown
outcome** error (documented: engine commands, UI edits and unknown methods
whose transmission or reply fails report an unknown outcome).

```
CI runner  ──JSON command──▶  effectcraft-cli mcp  ──engine──▶  compositor
           ◀──JSON result───                        ◀──result──
```

## Provenance and license

- EffectCraft: MIT OR Apache-2.0 (as named in Cargo.toml / workspace manifest
  at 9dd3193c; not independently interpreted).  No telemetry; no network access
  unless requested.
- This adapter contract: MIT.
- EffectCraft is self-declared alpha; macOS is the most-tested platform.
- After Effects (.aep/.aepx) projects cannot be opened; AE plug-ins do not run.

## Assumptions that must hold

1. **Headless mode available**: `effectcraft-cli mcp` starts an in-process
   session with no window.  Bridge mode adds screenshot/UI tools on port 9877.
2. **Relative footage paths**: since 0.8.0 the engine looks next to the project
   file in addition to its own CWD.  CI must place footage relative to the
   .ecproj file or supply `--automation-read-root DIR`.
3. **GPU fallback is silent by default**: on Windows 11 with some NVIDIA GPUs
   the DirectX 12 compositor fails and falls back to CPU without aborting the
   session.  CI cannot assume GPU rendering without checking the System
   Compatibility Report output.
4. **Output format is build-dependent**: the Output Module menu lists formats
   the current build can export.  CI must not hard-code a format without
   verifying the build's capability list at setup time.
5. **Dragging onto the window does not work in Wayland sessions**: footage
   must be imported via the `File > Import` engine command, not UI drag.

## Failure propagation

| Failure | Mechanism | CI consequence |
|---------|-----------|----------------|
| GPU compositor fails (DX12 on RTX) | Falls back to CPU silently | Slow render; CI timeout if not sized for CPU throughput |
| Footage missing | Engine command fails; relink needed via File Dependencies | Render job blocked; CI must pre-validate paths |
| Unknown outcome reply | Transmission or reply failed | Retry is safe only if the command is idempotent; comp.new is; add_keyframe may not be |
| Format not in build | Output Module returns empty or error | CI must capture and surface this; not a crash |

## Minimal command sequence (documented, not run)

```jsonc
// 1. New composition
{ "id": "comp.new",
  "params": { "name": "Intro", "width": 1920, "height": 1080,
              "frame_rate": 30, "duration": 4 } }

// 2. Import footage (relative path; requires footage next to .ecproj)
{ "id": "file.import",
  "params": { "path": "./footage/hero.mp4" } }

// 3. Apply effect
{ "id": "effect.apply",
  "params": { "layer": 1, "category": "Blur & Sharpen",
              "effect": "Gaussian Blur" } }

// 4. Queue and render
{ "id": "render.queue",
  "params": { "format": "h264", "output": "./out/intro.mp4" } }
{ "id": "render.start", "params": {} }
```

Command IDs above are derived from the docs' description of engine commands
and the agents.md session examples; exact IDs are not exhaustively listed in
the summarised docs and must be verified against the full docs/agents.md.

## Open evidence gaps (queued for research)

- Exact engine command ID list from docs/agents.md (only a subset is in the
  summarised record).
- Confirmed output format enumeration for a given build.
- Whether `render.start` is idempotent on an unknown-outcome retry.