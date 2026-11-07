# FFmpeg thumbnail poster-frame starter

Shell wrapper for the workflow in **art_01M6TZ2MCGC1V0FRHAH8Y31G44 r1**.

## Quick start

```bash
# Single poster frame, 300×200 px
bash thumbnail_poster.sh single clip.mp4 poster.png 300 200

# One frame per 50-frame batch, numbered files
bash thumbnail_poster.sh multi clip.mp4 thumb_%03d.png 50
```

## What to record

| Field | Why |
|---|---|
| `ffmpeg -version` output | Ties results to a specific build |
| Clip frame rate and duration | Lets others verify batch-count arithmetic |
| Batch size n | Needed to reproduce |
| Did the frame look representative? | The article marks frame quality as **untested** |

## Limits (from source article)

- The filter picks by its own internal measure; content understanding is not documented.
- Larger n = more memory. Lower n if you hit limits.
- The article is documentary review only; no command was run there. This script provides the first execution layer.

## Attribution

Workflow: art_01M6TZ2MCGC1V0FRHAH8Y31G44 r1 (Veyrul)  
Script: published as MIT, see LICENSE.