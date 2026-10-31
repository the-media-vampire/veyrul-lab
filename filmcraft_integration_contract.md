# FilmCraft v0.15.0 — Agent Pipeline Integration Contract
## Source: art_01M68GV4F4Q1SZ335DZD2PFC5Q revision 1 (documentation-level; nothing run)

---

## 1. Two interfaces, one command surface

Documentation says all 650+ engine commands are dispatched identically
whether the caller is the UI, CLI, JSON control channel, or MCP server
(README.md:233). That is the composability premise: agents can route
through either interface without needing different command vocabularies.

| Interface | Mode | Auth | Notes (doc claims) |
|-----------|------|------|--------------------|
| MCP stdio — headless | in-process session | none stated | Own process; no running desktop needed |
| MCP stdio — bridge | drives running desktop | per-session token | Same MCP tools, different backend |
| JSON control channel | TCP loopback only | per-session token | max 16 conn; oversized lines closed |

**Explicit doc-stated gap:** loopback alone does not restrict to the
desktop owner's account (docs/control-protocol.md:19). Any local process
can attempt connection; the per-session token is the only guard.

**Explicit doc-stated gap:** MCP server has no folder-confinement option;
it can read/write wherever the user can (docs/agents.md:18).

---

## 2. Integration assumptions that must hold

1. **Shared command vocabulary is stable.** If the MCP tool surface (17
   tools, docs/agents.md:76) diverges from the CLI, agents depending on
   one interface break silently on the other.
2. **Token delivery is out-of-band.** A pipeline must acquire the
   per-session token before issuing commands; the mechanism is not
   described in the excerpts.
3. **Timecode arithmetic uses integer ticks.** Callers must convert frame
   numbers or seconds to the 254,016,000,000-ticks/s base before
   submitting timeline commands (README.md:92; docs/control-protocol.md:202
   says seconds/frames are also accepted — verify which is canonical).
4. **Export is a background job.** Render commands return a job handle;
   the caller must poll progress and handle cancel (README.md:209-211).
   An agent that blocks awaiting a synchronous return will stall.
5. **Interchange round-trips are unconfirmed.** AAF and OMF output was
   never opened in Media Composer or Pro Tools as of the parity table
   (docs/file-format-parity.md:20-21). A pipeline expecting confirmed
   round-trips must test independently or avoid these formats.

---

## 3. Codec / format preconditions for agent-driven export

An agent must validate media before queuing a job:

- Software delivery codec: H.264 only (README.md:304). H.265 requires
  hardware encoder presence; AV1 export is not yet supported.
- H.264 decode: 8-bit 4:2:0 only per parity table (docs/codec-parity.md:18).
  10-bit or 4:2:2 inputs are a known gap.
- AVI: README lists it as supported; file-format-parity table lists AVI
  read as "no" (docs/file-format-parity.md:43). An agent must not assume
  AVI input will demux until this is resolved in code.
- Safe interchange output: FCPXML 1.9-1.11, OpenTimelineIO, CMX 3600 EDL
  (85% Premiere-parity estimate), FCP 7 XML (75% estimate). Premiere
  project format is not readable or writable.

---

## 4. Minimal agent call sequence (documented behaviour only)

```
1. START  — launch headless MCP server (stdio)
2. INSPECT — call sequence-inspection MCP tool; record tick-rate metadata
3. LOAD   — open project via MCP command
4. VALIDATE — check input codec/bit-depth against known parity limits
5. COMMAND — dispatch edit commands (same vocabulary as CLI)
6. RENDER  — dispatch render command; receive job handle
7. POLL   — query job progress until complete or cancelled
8. EXPORT  — retrieve output path; emit FCPXML or EDL for downstream NLE
```

Each step has a documented failure mode; steps 4 and 8 carry the
highest gap risk given the AVI and interchange ambiguities above.

---

## 5. License and provenance

FilmCraft: dual MIT / Apache-2.0 at user's option (README.md:455).
No GPL/LGPL code claimed by project (README.md:465; not audited).
This contract file: MIT (see parent artifact).
No code from FilmCraft is reproduced here; this is a protocol sketch
derived from documentation excerpts in art_01M68GV4F4Q1SZ335DZD2PFC5Q r1.

---

## 6. Open questions for research queue

- Token acquisition mechanism for the control channel / MCP bridge mode
- Whether MCP tool arguments accept raw ticks or only seconds/frame numbers
- AVI demux status (README vs. parity table conflict)
- Whether FCPXML 1.11 round-trips have been tested against Final Cut Pro