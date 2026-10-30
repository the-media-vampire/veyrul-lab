# Safe frame

Convert centered normalized boxes (cx, cy, width, height) into rounded pixel rectangles. Original prototype by Tess, Veyrul's Claude B production worker.

Run: `python3 test_safe_frame.py` (Python 3.9+, standard library only).

The result is (x0, y0, x1, y1), using geometric outer edges with a top-left inclusive and bottom-right exclusive rectangle convention. A full1024×1024 frame is (0,0,1024,1024), not a pixel index of1024. Rounding is Python's nearest-even rule. Tiny boxes may collapse after rounding; subpixel coverage, NaN/Inf and unusual input types are not covered by these tests.

## Observed validation

The initial hosted experiment returned exit0 for centered50%, full-frame, and out-of-bounds rejection. The published package was subsequently split into source and tests, so that hosted receipt alone does not prove the later file bytes. Main independently ran the exact corrected package below at 2026-10-30T01:25:31.368Z, with exit0:

```text
PASS  centered 50%: (256, 256, 768, 768)
PASS  boundary full-frame: (0, 0, 1024, 1024)
PASS  out-of-bounds right: raised ValueError: Box (cx=0.9, cy=0.5, bw=0.5, bh=0.5) extends outside the [0,1] normalized frame.

3 passed, 0 failed.
```

Main corrected the earlier ungrounded execution date and the inclusive/exclusive wording. No algorithm change is claimed. These three cases do not establish general correctness or aesthetic quality.

MIT license. Original version: https://github.com/the-media-vampire/veyrul-lab/tree/185bfcbd352daff988ab283cc1575d60a29e6425
