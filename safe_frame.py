"""
safe_frame.py
MIT License — see LICENSE

Normalized safe-frame bounding-box → pixel coordinate converter.

Input convention (YOLO / ComfyUI mask style):
  cx, cy  — box center, normalized [0, 1] relative to frame.
  bw, bh  — box width / height, normalized (0, 1].

Output:
  (x0, y0, x1, y1) — integer pixel rectangle, top-left inclusive,
  bottom-right exclusive (geometric outer edges), guaranteed within [0, frame_w] x [0, frame_h].

Raises ValueError for any out-of-bounds or nonsensical input.
No third-party dependencies; Python 3.9+.
"""


def norm_box_to_pixels(
    frame_w: int,
    frame_h: int,
    cx: float,
    cy: float,
    bw: float,
    bh: float,
) -> tuple[int, int, int, int]:
    """Convert a centered normalized bounding box to pixel coordinates.

    Parameters
    ----------
    frame_w, frame_h : int
        Frame dimensions in pixels (must be positive integers).
    cx, cy : float
        Box centre, normalized in [0.0, 1.0].
    bw, bh : float
        Box width and height, normalized in (0.0, 1.0].

    Returns
    -------
    (x0, y0, x1, y1) : tuple[int, int, int, int]
        Pixel rectangle.  Each value is rounded to the nearest integer.

    Raises
    ------
    ValueError
        If frame dimensions are not positive, any normalized value is
        outside [0, 1], box size is zero/negative, or the box edge
        extends beyond the normalized unit frame.
    """
    if not isinstance(frame_w, int) or not isinstance(frame_h, int):
        raise ValueError("frame_w and frame_h must be int.")
    if frame_w <= 0 or frame_h <= 0:
        raise ValueError(
            f"Frame dimensions must be positive; got {frame_w}x{frame_h}."
        )
    for name, v in (("cx", cx), ("cy", cy), ("bw", bw), ("bh", bh)):
        if not (0.0 <= v <= 1.0):
            raise ValueError(
                f"Normalized value '{name}' must be in [0, 1]; got {v}."
            )
    if bw <= 0 or bh <= 0:
        raise ValueError(f"Box size must be > 0; got bw={bw}, bh={bh}.")

    half_w = bw / 2.0
    half_h = bh / 2.0

    if (
        cx - half_w < 0.0
        or cx + half_w > 1.0
        or cy - half_h < 0.0
        or cy + half_h > 1.0
    ):
        raise ValueError(
            f"Box (cx={cx}, cy={cy}, bw={bw}, bh={bh}) "
            "extends outside the [0,1] normalized frame."
        )

    x0 = round((cx - half_w) * frame_w)
    y0 = round((cy - half_h) * frame_h)
    x1 = round((cx + half_w) * frame_w)
    y1 = round((cy + half_h) * frame_h)
    return x0, y0, x1, y1