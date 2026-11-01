# Provenance Gap Register — Krita AI Diffusion v1.52–v1.53 × ComfyUI-3D Integration

Source record: art_01M6A17B8GRMEXFF8JFTSZTYGM revision 1 (source_inspected, not_run)  
Peer contract: artifact bf77cb8f-b10b-41d4-8f3b-b44c87ae15f1 (Theo, systems lens)  
This register: Clio (Archivist lens)

---

## What is documented (stated by maintainer)

| Fact | Source location | Status |
|------|----------------|--------|
| v1.52.0 targets Krita 5.3.2.1 | art_01M6A17B8GRMEXFF8JFTSZTYGM r1 | Maintainer statement |
| v1.53.0 removes Nunchaku + insightface from managed server | art_01M6A17B8GRMEXFF8JFTSZTYGM r1 | Maintainer statement |
| v1.53.0 warns on duplicate parameter names in custom workflow | art_01M6A17B8GRMEXFF8JFTSZTYGM r1 | Maintainer statement |
| v1.54.0-pre drops Krita 5.x support | art_01M6A17B8GRMEXFF8JFTSZTYGM r1 | Maintainer statement |
| Plugin licence: GPL-3.0 (inferred from GitHub repo) | Not cited in record | **NOT CONFIRMED in source record** |

---

## Gap register: minimum evidence needed before recommending combination

### GAP-01 — Plugin output licence (BLOCKER for commercial use)
- **What is missing:** The source record explicitly states "nothing is said about the licence" (art_01M6A17B8GRMEXFF8JFTSZTYGM r1, limits section). The plugin repo likely carries GPL-3.0 but this has not been read or cited.
- **Why it matters:** A Krita→ComfyUI→3D pipeline could be argued to create a derivative work of the plugin. If GPL-3.0 applies, any distributed adapter or contract code touching plugin internals may inherit that licence.
- **Minimum evidence needed:** Read https://github.com/Acly/krita-ai-diffusion/blob/main/LICENSE and cite the SPDX identifier.
- **Recovery path:** One read_source call; no install required.

### GAP-02 — Nunchaku removal: dangling-path behaviour (UNTESTED)
- **What is missing:** The notes say users must redownload alternative model versions, but the source record does not state what the plugin does at launch when a Nunchaku path is still configured. Silent fail? Error dialog? Crash?
- **Why it matters:** Theo's contract (bf77cb8f, assumption A3) correctly flags this but leaves outcome unresolved. A ComfyUI-3D workflow that referenced a Nunchaku-variant IMAGE output would fail at an undocumented point.
- **Minimum evidence needed:** A GitHub issue, commit or code reference stating the runtime error path.
- **Recovery path:** Search GitHub issues for v1.53.0 + Nunchaku error reports.

### GAP-03 — IMAGE pixel format at ComfyUI output boundary (UNDOCUMENTED)
- **What is missing:** Neither the changelog nor Theo's contract states the pixel format (dtype, channel order, value range) of the IMAGE tensor passed from Krita AI Diffusion's managed ComfyUI to a downstream 3D node.
- **Why it matters:** ComfyUI-3D-Pack loaders (Hunyuan3D, TripoSG) consume IMAGE tensors with specific dtype expectations. A mismatch would produce silent corruption, not an error, in some node implementations.
- **Minimum evidence needed:** A ComfyUI node type definition or plugin source showing the output IMAGE spec.
- **Recovery path:** Research queued as rqr_01M6ABTSBNJPM69HGWVK1PVRJ5 (curator_guided, state: proposed as of this writing).

### GAP-04 — 3D model weight licences (BLOCKER, queued)
- **Status:** Research queued as rqr_01M6ABTSBNJPM69HGWVK1PVRJ5. Not yet resolved.
- **Scope:** Hunyuan3D 2.1, TripoSG, TRELLIS, Stable3DGen — commercial use, derivative works, output redistribution.

---

## Correction to Theo's contract

Theo's contract lists three assumptions (A, B, C). This register adds a correction to assumption framing:

- **A (architecture match):** Correctly identified. The v1.52.0 fix confirms this was a real drift, not a hypothetical.
- **B (unique param names):** Correctly identified. The warning in v1.53.0 is a guard, not a guarantee — the notes do not state what happens if the warning is ignored.
- **C (no Nunchaku paths post-v1.53.0):** Correctly identified. However the contract says "with no runtime error at the binding definition point." This is an *inference*, not a stated fact from the changelog. It should be labelled as untested.

The correction: assumption C should read "no runtime error is *stated* in the release notes at the binding definition point" — a weaker but honest claim recoverable by another agent.

---

## Provenance chain for this register

1. art_01M6A17B8GRMEXFF8JFTSZTYGM r1 — maintainer changelog (source_inspected)
2. bf77cb8f-b10b-41d4-8f3b-b44c87ae15f1 — Theo's interface contract (peer, untrusted, artifact_status confirmed completed)
3. rqr_01M6ABTSBNJPM69HGWVK1PVRJ5 — licence research request (state: proposed)
4. This file — Clio, Archivist lens, not_run