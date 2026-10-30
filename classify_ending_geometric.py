"""classify_ending_geometric.py

Geometric ending classifier for abstract video frames.
Source: art_01M64VKR0GN2KBH19JWXHJ7J4Y r2
Execution receipts: 1220e5e8 (3/5 baseline), c46034d2 (5/5 revised)

Inputs : H x W x 3 uint8 numpy array (one frame, RGB)
Outputs: ('DRAIN'|'FILL'|'AMBIGUOUS', detail_dict)

Limits:
- Thresholds calibrated to synthetic fixtures only; not validated on real video.
- DRAIN_MIN assumes the mark occupies >= 0.5% of the frame area.
  Scale accordingly for higher-resolution source.
- Connected-component labelling is pure Python; slow on large frames.
  Replace with scipy.ndimage.label for production use.
- No temporal context: applies to a single frame, not a motion sequence.
"""
import numpy as np

RED_THRESH    = 100    # R channel minimum
DRAIN_MIN     = 0.005  # minimum red fraction to enter geometry check
FLOOD_THRESH  = 0.25   # red fraction >= this -> FILL
MAX_MARK_PX   = 400    # max red pixels for a 'short mark'
MAX_MARK_COMP = 3      # max connected components for a 'short mark'


def _label_components(mask):
    """4-connectivity union-find; returns (label_array, n_components)."""
    h, w = mask.shape
    labels = np.zeros((h, w), dtype=int)
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            parent[x] = parent.get(parent[x], parent[x])
            x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    cur = 0
    for y in range(h):
        for x in range(w):
            if not mask[y, x]:
                continue
            neighbors = []
            if y > 0 and mask[y - 1, x]:
                neighbors.append(labels[y - 1, x])
            if x > 0 and mask[y, x - 1]:
                neighbors.append(labels[y, x - 1])
            if neighbors:
                lbl = min(neighbors)
                labels[y, x] = lbl
                for n in neighbors:
                    union(lbl, n)
            else:
                cur += 1
                labels[y, x] = cur
                parent[cur] = cur

    roots = {}
    for y in range(h):
        for x in range(w):
            if labels[y, x]:
                r = find(labels[y, x])
                if r not in roots:
                    roots[r] = len(roots) + 1
                labels[y, x] = roots[r]
    return labels, len(roots)


def classify_ending(frame: np.ndarray) -> tuple[str, dict]:
    """Classify one closing frame as DRAIN, FILL, or AMBIGUOUS."""
    r, g = frame[:, :, 0], frame[:, :, 1]
    red_mask = (r.astype(int) - g.astype(int) > 60) & (r > RED_THRESH)
    red_frac = float(red_mask.mean())

    if red_frac < DRAIN_MIN:
        return "AMBIGUOUS", {"red_frac": round(red_frac, 4), "reason": "too little red"}

    if red_frac >= FLOOD_THRESH:
        return "FILL", {"red_frac": round(red_frac, 4), "reason": "flood"}

    _, n_comp = _label_components(red_mask)
    px_count = int(red_mask.sum())

    if n_comp <= MAX_MARK_COMP and px_count <= MAX_MARK_PX:
        return "DRAIN", {"red_frac": round(red_frac, 4), "n_comp": n_comp, "px": px_count}

    return "AMBIGUOUS", {
        "red_frac": round(red_frac, 4),
        "n_comp": n_comp,
        "px": px_count,
        "reason": "geometry unclear",
    }