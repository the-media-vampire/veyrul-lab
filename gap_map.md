# SoundCraft Integration: Provenance Gap Map

Source: art_01M6B3RV7EFBS0HCVAMR4AM492 rev 1, commit 4179cf88e6d0  
Companion to: artifact 1f7f647d (Theo, dispatcher.py, published not executed)

## How to use this map

Each row names: (1) the gap, (2) why it blocks real integration, (3) the minimum
evidence that closes it, and (4) the source file that should contain it.
Fill in `Closed by` and `Date` when you verify.

---

## Gap table

| ID   | Gap                              | Blocks                              | Minimum evidence to close              | Source file at commit 4179cf88e6d0             | Closed by | Date |
|------|----------------------------------|-------------------------------------|----------------------------------------|------------------------------------------------|-----------|------|
| E-01 | TCP port not documented in source record | dispatcher.py uses placeholder 7777; TCP path is a sketch | Actual port from control-protocol.md or runtime help output | docs/control-protocol.md | — | — |
| E-02 | engine.execute JSON schema unknown | Cannot validate command payloads; silent failures expected | Full schema or at least field list (command, params, session id) | docs/control-protocol.md | — | — |
| E-03 | Engine command list not read | Only two examples exist (mix.volume, bounce); unknown coverage | soundcraft-cli commands output or docs listing all commands | docs/cli.md, Rust CLI arg files | — | — |
| E-04 | README vs gap-list disagreement on audio interface | G-01 says device/rate/buffer done; README says missing | Confirm against 0.15.0 build or changelog | README.md + docs/gaps.md (review date 2026-10-25) | — | — |
| E-05 | Confinement TOCTOU documented but not scoped | External orchestrators may assume stronger guarantee | Characterise which operations are TOCTOU-exposed vs safe | docs/mcp.md (confinement section) | — | — |
| E-06 | --connect + confinement mutually exclusive (undocumented error form) | TCP path cannot use confinement; agent must choose one | Error message text or exit code from control-protocol.md or CLI help | docs/control-protocol.md | — | — |
| E-07 | No execution receipt exists for either transport path | All contracts are documentary; no observed runtime behaviour | Any CI log, test run, or controlled execution of soundcraft-cli run demo | Not in supplied sources | — | — |

---

## Assumption register

These must hold for Theo's dispatcher to work as written.
Each is an untested assumption, not a confirmed fact.

| ID   | Assumption                                               | Risk if wrong                          |
|------|----------------------------------------------------------|----------------------------------------|
| A-01 | TCP port is 7777                                        | TCP probe connects to wrong service     |
| A-02 | engine.execute accepts {"command": str, "params": dict} | Commands silently rejected or error     |
| A-03 | MCP stdio path is stable across 0.15.x patch releases  | Path breaks on minor update            |
| A-04 | Headless path does not require a real audio device       | soundcraft-cli run may fail without hardware |
| A-05 | Confinement flags are ignored on --connect path, not erroring silently | Error might be swallowed   |

---

## Provenance chain (as of this writing)

```
storytold/soundcraft @ 4179cf88e6d0  (MIT OR Apache-2.0, named not interpreted)
  └─ source-inspected by veyrul-import → art_01M6B3RV7EFBS0HCVAMR4AM492 rev 1
        └─ dispatcher.py contract sketch by Theo → artifact 1f7f647d (published, not executed)
              └─ this gap map by Clio → current artifact (published, not executed)
```

Nothing in this chain has been run. E-07 marks the first execution receipt as an open gap.