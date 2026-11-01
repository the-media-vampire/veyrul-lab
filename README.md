# SoundCraft Dual-Interface Adapter Contract v0.1

Source: art_01M6B3RV7EFBS0HCVAMR4AM492 rev 1 (documented, not run).  
SoundCraft repo: storytold/soundcraft commit 4179cf88, license MIT OR Apache-2.0 (named, not interpreted).

## Two transports, one command model

| Property    | MCP / stdio                        | TCP control channel            |
|-------------|-------------------------------------|--------------------------------|
| Invoked by  | `soundcraft-cli mcp <session>`      | Desktop app (must be running)  |
| Confinement | `--read-root` / `--write-root`      | Incompatible with `--connect`  |
| Headless?   | Yes                                 | No                             |
| Dialogs?    | Never (uses defaults/selection)     | Never                          |

## Known failure modes
- Exit code 1: missing file, unknown command, app not running
- Output path == input path: usage error regardless of spelling
- G-01: no duplex stream / disk recording; G-02: no MIDI I/O; G-03: no AAF/OMF
- macOS signed builds: third-party VST3 refused (issues 153, 149)
- README vs gap-list disagree on audio interface choice at 0.15.0 (unresolved)

## Open assumptions requiring evidence
1. Exact TCP port and full message schema for `engine.execute`
2. Full engine command list (`soundcraft-cli commands` not read)
3. Whether `--no-audio` suppresses input recording or only output playback
4. Which source (README or gap list) is current for audio interface choice