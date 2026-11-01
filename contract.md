# VectorCraft ↔ Inkscape Batch Pipeline: Integration Contract v0.1

Source: art_01M6C4DQJT443MQZBT1S1F8R8D r1 (documented, not run).

## Compared interfaces

| Concern          | VectorCraft (cf0d4d4a)                        | Inkscape CLI (1.x)                         |
|------------------|-----------------------------------------------|--------------------------------------------|
| Trace input      | Placed raster → Image Trace UI                | `--actions=import;select-all;trace-bitmap` |
| Trace limit      | 8 M anchors (2 M web); hard refusal           | No documented hard limit; silently slow    |
| Trace method     | Abutting (default); Noise 1–100 px            | Potrace: threshold, passes, speckle size   |
| Path booleans    | linesweeper engine                            | lib2geom                                   |
| Plugin scope     | WASM, per-process                             | Python/C++ extension, per-document session |
| PDF write        | craft-pdf (storytold/craft-libs)              | Poppler / Cairo PDF                        |
| Rasterize        | vello_cpu, CPU multithreaded                  | Cairo, CPU single-threaded by default      |
| Dimension tool   | dimension.create(p1, p2 | source)            | No native dimension; via extension         |

## Adapter boundary (proposed)

A WASM plugin loaded per-process in VectorCraft could:
1. Accept a raster path and target anchor budget.
2. Pre-check: estimate anchor count before submitting to VectorCraft Image Trace.
   - If estimate > 8 M: tile the raster, trace tiles, merge with path booleans.
   - Interface assumption: plugin can call VectorCraft path boolean ops via the command registry (~710 commands documented).
3. Emit an SVG path string that Inkscape CLI can ingest via `--actions=import`.

## Limit and assumption register

- ASSUMPTION A: WASM plugin API exposes command registry calls. Not confirmed in the 15 docs read; the architecture page mentions ~710 commands but plugin API surface is undocumented in the read set.
- ASSUMPTION B: Tile-merge via linesweeper is lossless at tile seams. Not tested.
- ASSUMPTION C: Inkscape accepts SVG paths from VectorCraft without layer/namespace conflicts. Plausible; both target SVG, but craft-pdf backend divergence is a risk for round-trip.
- LIMIT: Lettering guide is v0.13.1; "Create Outlines" menu name may have changed in 0.19.0. Any pipeline step using text outlines carries version drift risk.
- LIMIT: Plugin scope is per-process in VectorCraft, per-document in Inkscape. A stateful WASM plugin cannot share state across documents in VectorCraft without re-init.

## License compatibility

- VectorCraft: MIT OR Apache-2.0 (named, not interpreted)
- Inkscape: GPL-2.0+
- craft-pdf / storytold/craft-libs: not confirmed in read set
- A pipeline that shells out to Inkscape CLI avoids linking and likely avoids GPL propagation, but this is a legal question, not a systems claim.

## Concrete next step

The weakest link is ASSUMPTION A. The research queue question is:
"Does VectorCraft's WASM plugin interface expose command registry calls, and which subset is callable from a plugin context?"