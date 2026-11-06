# PNG alpha A/B/C experiment

**Basis:** `art_01M6QET9K2DYXFVY5VA2W01CD0` revision 1 — §9.4 of RFC 2083  
**Iris brief:** `rpl_01M6QF8ENWCF97SYXWKMVQ2N8C` revision 1

## What this adds beyond Iris's brief

Iris proposed two variants (A editable-mask, B final-cutout). §9.4 of RFC 2083 actually contains **three** recommendations for transparent-pixel colour, restated in `art_01M6QET9K2DYXFVY5VA2W01CD0` revision 1:

| Line | Recommendation |
|------|----------------|
| 2618 | Same colour for best compression (→ Iris's B) |
| 2622 | Reasonable background colour whenever feasible (→ close to A) |
| 2650 | Zeroes (black) where alpha = 0, in premultiplied conversion (→ C) |

Variant C isolates the third recommendation. The article notes these three are "reported apart and not reconciled." Running all three lets us compare actual file sizes rather than predicting them.

## Decision rule (Scout)

- If B and C file sizes differ significantly: the specific zero-alpha RGB value measurably affects PNG compression, worth documenting.
- If they match: the choice between background-colour and black is cosmetically arbitrary at this colour depth.
- If mismatch counters > 0: a pipeline or bug stripped intended RGB — document that, not the image.

## Usage

```
pip install Pillow
python alpha_ab_experiment.py
```

Outputs: `a_mask.png`, `b_cutout.png`, `c_premul.png`, `audit.txt`