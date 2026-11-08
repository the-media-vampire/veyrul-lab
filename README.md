# Zettlr --data-dir + Pandoc: integration contract

**Status:** Documentary skeleton; not run.

## What this is

A concrete interface contract (`contract.json`) and shell adapter (`launch_and_export.sh`) that connect two workflows:

1. **Zettlr profile isolation** via `--data-dir` (source: art_01M6WJTB83S88GF5B1H8H1V5EP r1, Zettlr README commit f2f20646, Hendrik Erz and contributors, GPL v3).
2. **Pandoc batch export** run after Zettlr exits.

## The core mechanism

`--data-dir` redirects Zettlr's config and cache to an absolute path you control. That boundary — one profile folder per project — is the only isolation mechanism. The script exploits a simple sequencing property: Zettlr runs in the foreground, the shell blocks, and Pandoc only starts after the user closes Zettlr. This avoids file-lock races (I2) without any locking protocol.

## Interfaces

| ID | From → To | Must hold |
|----|-----------|----------|
| I1 | User → Zettlr | `--data-dir` is an absolute path; tilde not expanded |
| I2 | Zettlr → Pandoc | Zettlr exits before Pandoc reads `.md` files |
| I3 | Pandoc → LaTeX | `pdflatex` on PATH for PDF; script degrades to DOCX |

## Critical failure not in the elegant diagram

If `--data-dir` receives a relative path, Zettlr resolves it relative to its binary directory (documented failure mode in art_01M6WJTB83S88GF5B1H8H1V5EP r1). Config silently lands somewhere unexpected. The script uses `set -euo pipefail` and assigns paths explicitly; it cannot validate that Zettlr actually wrote config to the right place — that check must be done manually the first time.

## License seam

- Zettlr: GPL v3; brand reserved.
- Pandoc: GPL v2+.
- This adapter (MIT): invokes both as separate processes only. Bundling either binary changes license obligations.

## What was not verified

- Whether Zettlr holds file locks on `.md` files while running (Windows vs Linux behaviour differs).
- Whether Pandoc's default template handles Zettlr's YAML front-matter fields without warnings.
- LaTeX template compatibility with Zettlr-authored front-matter.