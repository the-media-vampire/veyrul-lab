# ComfyUI custom-node bisect helper

Implements the **manual halving search** from `troubleshooting/custom-node-issues.mdx`
(Comfy-Org/docs commit `4a9f856b`, GPL-3.0). No page text reproduced.
Research record: `art_01M6JVW9DS5T7W9T9659ARG0S2` rev 2 (Veyrul).

## Baseline vs. this script

| Without | With |
|---|---|
| Move folders by hand, no log | Timestamped tar.gz backup before first move |
| No round tracking | JSON session file; `status` shows history |
| No undo path | `reset` restores all staged nodes |
| Suspect identified only by memory | Script prints suspect when one remains |

## Requirements
Bash ≥ 4, Python 3. Present in any standard ComfyUI manual/portable Linux/macOS install.
Windows portable users need WSL or a `.bat` port (not included).

## Usage
```bash
chmod +x bisect.sh
./bisect.sh start /path/to/ComfyUI/custom_nodes /tmp/bisect_staging
# Start ComfyUI normally. Test.
./bisect.sh bad    # issue persists -> culprit in active nodes
./bisect.sh good   # issue gone    -> culprit in staging
# Repeat until suspect named. Then:
./bisect.sh reset  # restore all
```

## Verification step (not automated)
After reset: disable only the suspect node, start ComfyUI, confirm issue absent.
Re-enable it, restart, confirm issue returns. Two-state check = bisect confirmed.

## Limits
- Not tested on a live install; desk-built from documented procedure.
- Does not handle symlinks in `custom_nodes`.
- Staging dir should be on the same partition as `custom_nodes` (shutil.move speed).
- Windows Portable not supported without WSL.