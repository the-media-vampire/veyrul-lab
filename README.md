# Histogram population fixture

Run: `python3 compare_hist.py` (Python standard library).

Original synthetic companion to Theo's metadata adapter, not a replacement or a plugin API. Input: two arrays of 256 nonnegative integer counts for ONE channel, each with positive total. Output: normalized total variation, equal-total flag, and explicitly hypothetical clipped-display diagnostics. No image decoding, colour transform, resampling or engine access is implemented.

The executed prototype receipt is 2f9688ff-5ca8-40b8-8f4f-886ebfd48efe: exit 0, TV=0.4 with modeled display difference=0; population scaling TV=0 with unequal totals; disjoint TV=1; four malformed inputs rejected. This publication repackages that prototype; publication is not execution of these exact file bytes.

## Integration contract
Before comparison require matching capture point, frame identity, crop, OCIO configuration/transform, signal encoding, full/legal range, quantization and binning. Record actual analysis path, engine version, plugin commit and analysis dimensions. Unknown metadata means INCONCLUSIVE, not PASS. Different sample grids may change normalized populations; normalization alone cannot correct this.

Only compare raw counts after metadata checks. Equal normalized histograms do not establish equal images or spatial placement. Exact count parity requires the same samples and totals. No universal TV acceptance tolerance is proposed. A screenshot-only check remains qualitative, especially when bins saturate.

## Provenance and rights
Documentary basis: art_01M6D2YB2J8Q7XXSY91CCNZ1DG revision 1, inspected TrueScope commit 0820239a6ff47ae69f3d2a87718560472214ef01. It reports 256 bins and a default histogram clip threshold of 1.58% of frame pixels. Our gain=1 display equation is a hypothesis, not source-verified behavior.

TrueScope is documented as Apache-2.0; no plugin code is included or relicensed. This original fixture is MIT. Theo's independent MIT contract artifact 8862c827-40d1-4994-8ecb-2ea715bb9e14 (commit 4f8936f940c5760546e695310390b16b9a3c5d45) supplied the metadata-contract starting point; its source publication was verified, not executed here. No DaVinci Resolve code/assets are distributed, and no automated Resolve interface is asserted.