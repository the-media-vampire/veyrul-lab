# Abstract video ending classifier — example and limits

## Source
art_01M64VKR0GN2KBH19JWXHJ7J4Y revision 2

## Usage
```python
from classify_ending import classify_ending

# Supply per-frame RGB means for the last 3-5 frames.
frames = [{"r": 45, "g": 8, "b": 8}, {"r": 52, "g": 6, "b": 7}]
print(classify_ending(frames))  # -> {"verdict": "drain", ...}
```

## Verified behaviour (execution artifact 87e43714-cce8-48c7-a3d2-2fae7a97ad67)
| Input case | Expected | Returned |
|---|---|---|
| Run A (drain) | drain | drain |
| Run B (fill) | fill | fill |
| Mid-case | ambiguous | ambiguous |

## Limits
- Thresholds calibrated on two data points only. Treat "ambiguous" as "needs human check."
- Requires per-frame RGB means; does not read video files directly.
- Does not distinguish audio, motion speed or mid-video behaviour.
- No seed control in the original runs — classification describes outcomes, not causes.

## Next improvement
Add a third threshold parameter: `min_frames_required` (default 3). Currently returns a verdict on even one frame, which is unreliable. After three or more confirmed runs are classified, re-fit brightness and red_ratio thresholds empirically.