# Decision protocol

Apply after all arms are logged. Answer each question in order and stop at the first disqualifier.

## Step 1 — Technical gate

Does this arm show eyelash or lip boundary softening relative to control?
- YES → Disqualified for this portrait use. Record reason and stop.
- NO → Continue.

## Step 2 — Chroma diagnostic (Scout's question)

Is colour noise changed in `all_planes` (p=7) but NOT in `restrained` (p=1)?
- YES → Chroma is part of the texture problem. Sigma-only tuning was targeting the wrong plane. Note this and prioritise planes axis in next iteration.
- NO → Chroma contribution is negligible; sigma axis is the right lever.

## Step 3 — Temporal gate

Does this arm show visible texture flicker during the blink or head turn?
- YES → Disqualified for motion use. Record reason and stop.
- NO → Continue.

## Step 4 — Expression gate (Iris's criterion)

Do the eyes remain the dominant feature, and does the expression feel readable?
- NO → Reject even if technically clean. Record reason.
- YES → Continue.

## Step 5 — Selection

Among arms passing steps 1–4, prefer the arm with the least smoothing (lowest sigma or narrowest planes). If the control passes all gates, keep the control.

## Step 6 — Record

- Selected arm:
- Reason (one sentence):
- Reviewer:
- Date observed:
- FFmpeg version used: