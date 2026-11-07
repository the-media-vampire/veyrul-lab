# chromahold_trial.sh

Selective-colour sweep script. Keeps one chosen colour; grays the rest.

## Source
art_01M6VPNKZ6FCHZ0P8HNYSFSFGC r1 (Veyrul) — documentary review only; no
command was run in that source. This script is **also not executed**; it is
published as source for you to run against your own clip and FFmpeg build.

## Usage
```bash
bash chromahold_trial.sh in.mp4 red
# or with a hex colour:
bash chromahold_trial.sh in.mp4 '#c0392b'
```

## What it checks before tuning
1. **Build check** — exits with an error if `chromahold` is absent.
2. **Baseline run** — `similarity=0.01` should produce an almost fully-gray
   clip. If colour bleeds through here, something upstream is wrong (wrong
   filter, wrong colour format, yuv accidentally enabled).
3. **Similarity sweep** — 0.1 → 0.2 → 0.3 with `blend=0.1`. Pick the lowest
   value that holds the full target object cleanly.

## Verification condition
Fix is confirmed when:
- Baseline is visually near-gray.
- Chosen sweep step holds the whole object without speckle on the edges.
- No unexpected objects of similar colour are held.

## Limits
- Not executed; no output, timing or visual result observed.
- Trial similarity values (0.1–0.3) are illustrative per the source article.
- Named colours require `yuv` to be OFF (default). Use hex only if yuv is on.
- Record your FFmpeg version alongside any results.

## Next improvement
Add an `ffprobe` luma-mean comparison between baseline and source to make the
"near-gray" check machine-readable instead of visual, so the baseline step
fails loudly if colour is leaking.