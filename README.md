# TrueScope → External Analysis: Interface Contract

Source: art_01M6D2YB2J8Q7XXSY91CCNZ1DG revision 1 (mh-techart/TrueScope commit 0820239a, Apache-2.0, documentary only — nothing was run).

## TrueScope’s Documented Boundary

- Capture point: after Tonemap pass + after OCIO view transform; pre-FXAA/SMAA
- Bit depth: 8-bit capture; at most 256 distinct values per channel on 0–1023 axis
- Refresh: ~5 Hz (architecture page); earlier phase pages say 2–3 Hz — discrepancy noted
- Scope: last focused level viewport, post-processing show flag must be on
- Not available: wireframe, unlit, most debug view modes
- API surface: editor UI only; no documented IPC, export or extension point

## Interface Mismatch Table

| Dimension       | TrueScope (documented)       | External tool (typical)          |
|-----------------|------------------------------|----------------------------------|
| Trigger         | After-pass callback, ~5 Hz   | On-demand / batch                |
| Bit depth       | 8-bit                        | 8–32-bit                         |
| Colour space    | Post-OCIO view transform     | Configurable; may be pre-OCIO    |
| Anti-aliasing   | Pre-FXAA/SMAA                | Post-AA if from final render     |
| Access          | Editor UI only               | File read or API                 |

## Key Assumptions to Satisfy

1. Images must be saved *after* the OCIO view transform to match TrueScope’s measurement point. UE Movie Render Queue EXR exports are pre-OCIO by default — likely mismatch.
2. Source signal is 8-bit; HDR discrimination from TrueScope histogram data is not valid.
3. Post-processing show flag must be on in the viewport being compared.
4. FXAA/SMAA must be off to get pixel-exact histogram agreement.

## Open Questions (research queue)

- Does TrueScope expose any extension point, delegate or IPC not in the 10 files read?
- What is the fixed analysis resolution? Not stated in read files.
- 9 files unread (phase 4.1, 5.1, 5.2, 6.x, backlog, developer rules) — may affect API surface.
- Windows automation suite not run per architecture page; cross-platform parity unconfirmed.