# FFmpeg amplify — contributor brief sheet

Source: `art_01M6WFBNWS1FQ8BREZZMD93F9G` revision 1  
Evidence status as of that revision: documentary review only; no command was run.

---

## What this research gives you

A desk-curated parameter reference assembled from the FFmpeg filters manual (captured 2026-11-07).  
What it does **not** give you: any observed output, timing, visual result, or confirmed example.

---

## Decision table — which parameter to reach for first

| Symptom / goal | Parameter | Direction | Watch out for |
|---|---|---|---|
| No visible effect | `factor` | Raise (default 2; try 6–20) | Noisy mess above ~30 |
| Noisy mess | `factor` | Lower | |
| Tiny differences ignored | `tolerance` | Lower toward 0 | May amplify sensor noise |
| Large motion areas look wrong | `threshold` | Raise | Leaves large differences unaltered |
| Flicker over several frames | `radius` | Raise (default 2; max 63) | Longer radius = more temporal blur |
| Limit clipping artefacts | `low` / `high` | Set below 65535 | Both default to max |

---

## Usability tradeoffs for a first contributor

**Low barrier:**  
- Any FFmpeg build with the amplify filter (check with `ffmpeg -filters | grep amplify`).  
- A short, mostly static clip (locked-off shot, timelapse frame range).  
- One new output filename per trial — the guide explicitly flags this.

**What stops most people:**  
- The manual gives no worked example with real output. The article command (`amplify=radius=2:factor=6:threshold=20`) is assembled, not tested.  
- No baseline output to compare against means a contributor can't tell whether their result is typical.

**Attribution:**  
Option names and short syntax fragments only are reproduced from the FFmpeg filters documentation (LGPL project). No passages were copied. Original synthesis layer is MIT (this sheet). The FFmpeg project's own license terms apply to the tool itself.

---

## Combining with the stack guide

The article recommends a side-by-side comparison ("the stack guide"). That pairing is a suggestion, not a documented step. A contributor who runs both and reports what the comparison actually shows fills the largest gap in the current evidence chain.

---

## Scoped research request — the most useful next contribution

**Question:** Does `ffmpeg -i in.mp4 -vf amplify=radius=2:factor=6:threshold=20 out.mp4` produce a visibly amplified result on a known-static clip, and what does the side-by-side comparison look like?

**Why bounded:** One command, one clip, one comparison. No subscription or special access needed beyond an FFmpeg build.  
**What to report:** FFmpeg version (`ffmpeg -version`), clip description (resolution, fps, content type), factor used, what changed visually, what did not.  
**Evidence gap it closes:** Every claim in the article currently sits at "assembled or our suggestion". A single run with reported version and observations moves at least one row to "contributor-tested".

**Participation note:** Report the FFmpeg version with results. The manual states no page version; build differences can change filter behaviour.