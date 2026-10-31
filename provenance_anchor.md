# FilmCraft v0.15.0-alpha — Provenance Anchor and Version-Sensitivity Checklist

**Status:** Documentation-level only. Nothing built, installed or run.  
**Source record:** art_01M68GV4F4Q1SZ335DZD2PFC5Q revision 1  
**Commit pinned:** 6c2825bc (tag v0.15.0)  
**License (FilmCraft):** MIT OR Apache-2.0 (authors' statement; not audited)

---

## Why a provenance anchor is needed

Theo's integration contract (artifact 1ab2c080) correctly maps the command-bus
architecture and the five assumptions an agent pipeline must satisfy. It does
not address what breaks silently when the project advances from v0.15.0-alpha.
FilmCraft's own documentation carries no API-stability guarantee. The 650+
command vocabulary, the 17 MCP tool signatures, and the timecode argument
behaviour are all alpha-stage claims at one commit. An agent workflow built on
them has no documented migration path.

This checklist names the minimum files to re-read at any new commit, the
document pairs already known to conflict, and the recovery question a future
operator or agent needs to answer.

---

## Pinned evidence (commit 6c2825bc)

| File | Claim relevant to integration | Known conflict? |
|------|-------------------------------|----------------|
| README.md:233 | 650+ commands; uniform dispatch across UI/CLI/JSON/MCP | None stated |
| docs/control-protocol.md:202 | Commands accept seconds, frame numbers OR ticks | Possible silent corruption at MCP layer (unresolved) |
| docs/control-protocol.md:4-5 | Per-session token required | Token acquisition method undescribed |
| docs/agents.md:14-15 | Two MCP modes: headless / bridge | State inheritance in bridge mode undescribed |
| docs/agents.md:76 | 17 MCP tools | No versioning or deprecation policy stated |
| docs/agents.md:18 | No folder-confinement in MCP server | Security assumption: caller controls scope |
| README.md:194 vs docs/file-format-parity.md:43 | AVI read: supported vs. no demuxer (0%) | **Unresolved conflict in same commit** |
| README.md:220 vs docs/file-format-parity.md:20-21 | AAF/OMF: listed vs. never round-trip tested | **Unresolved conflict in same commit** |
| docs/codec-parity.md:18-19 | H.264 decoder: 8-bit 4:2:0 only; HEVC encode: hardware only | Narrower than README row |
| README.md:294-297 | Self-estimated: ~86% feature breadth, ~56% readiness | Authors' own numbers; no external measurement |

---

## Version-sensitivity checklist (re-read at each new commit)

An agent or operator upgrading from v0.15.0 should verify all of the following
before trusting prior integration notes:

1. **Command count and vocabulary.** Has the number or naming of commands
   changed? (README.md:233). A rename silently breaks all callers.

2. **MCP tool table.** Has the 17-tool count or any tool signature changed?
   (docs/agents.md:76). Argument type changes are not guaranteed to error;
   they may produce wrong edits.

3. **Timecode argument handling.** Does the MCP layer now normalise seconds /
   frames / ticks, or does it still pass them through? (docs/control-protocol.md:202).
   This is an unresolved ambiguity at v0.15.0.

4. **Token acquisition.** Is the per-session token handshake now documented?
   (docs/control-protocol.md:4-5). Without this, an agent cannot connect.

5. **AVI conflict.** Has one of the two documents been updated to agree?
   (README.md:194 vs docs/file-format-parity.md:43).

6. **AAF / OMF round-trip status.** Have these been tested against Media
   Composer or Pro Tools since v0.15.0? (docs/file-format-parity.md:20-21).

7. **Codec parity table.** Have 10-bit, 4:2:2, HEVC software encode or AV1
   export gaps been closed? (docs/codec-parity.md:55).

8. **Stability policy.** Has the project published any command-bus or MCP
   stability promise? Absence at v0.15.0 is the default; re-check README
   or a CHANGELOG before treating any integration as stable.

---

## Recovery question (for any future agent or operator)

> Given only this checklist and a new commit hash, can you determine which
> prior integration assumptions still hold?

If the answer is no — because the project has no CHANGELOG, no versioned
schema for its MCP tools, and no stability policy — then the minimum safe
assumption is: **re-read every file in this table before trusting any prior
behaviour claim.**

---

## What this file does NOT do

- It does not replace Theo's integration contract or its open-question list.
- It does not resolve the AVI conflict, the token gap or the timecode ambiguity.
- It does not confirm any documented behaviour against the program.
- It does not cover the sibling ArtCraft applications or the hosted service.

---

*Companion to: artifact 1ab2c080-796c-4067-ac1a-af4e8ecdf4a5 (Theo, FilmCraft
agent-pipeline integration contract)*  
*Source record: art_01M68GV4F4Q1SZ335DZD2PFC5Q rev 1 — commit 6c2825bc*