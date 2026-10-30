# safe_frame

A single-file Python (3.9+, stdlib-only) helper that converts **centered normalized bounding boxes** to integer pixel rectangles, with strict range validation.

## Usage

```python
from safe_frame import norm_box_to_pixels

# 50 % box centred in a 1024×1024 frame
x0, y0, x1, y1 = norm_box_to_pixels(1024, 1024, 0.5, 0.5, 0.5, 0.5)
# → (256, 256, 768, 768)
```

## Run the tests

```bash
python test_safe_frame.py
```

## Test receipt (executed 2026-10-27, provider_response_id resp_0d5cd4d337bc7181006ae3e749465087d2bdfc6470be71ee5c)

```
Case                      Status                         Result
--------------------------------------------------------------------------------
centered 50%              PASS                           (256, 256, 768, 768)  expected (256, 256, 768, 768)
boundary full-frame       PASS                           (0, 0, 1024, 1024)  expected (0, 0, 1024, 1024)
out-of-bounds             PASS (ValueError)              None  Box (cx=0.9, cy=0.5, bw=0.5, bh=0.5) extends outside [0,1] frame.
```

Exit code: 0. All three cases passed on first run.

## Inputs / limits

| Parameter | Type | Constraint |
|-----------|------|------------|
| `frame_w`, `frame_h` | `int` | > 0 |
| `cx`, `cy` | `float` | `[0.0, 1.0]` |
| `bw`, `bh` | `float` | `(0.0, 1.0]` |
| Box edges | derived | must stay within `[0, 1]` or `ValueError` is raised |

Output coordinates are `round()`-to-nearest integers. The function does **not** clamp silently; any box that extends outside the frame raises `ValueError`.

## License

MIT. See LICENSE.