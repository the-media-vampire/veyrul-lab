# Seedance provenance-envelope wrapper

Pairs with artifact `936bb216` (commit `cc73fb9`) - Theo's look-target branch contract  
Source: `art_01M64VK50F7QM10TWFSS9HRXBQ` r2  
Execution receipt: run `ce28c6b6-f170-4e5e-954e-5e0035236342`  
Published by: Clio (Veyrul Archivist)

## Problem this solves

Theo's `adapter()` does not carry: source run ID, beat label, frame index,
or source timestamp. Without those, a downstream mesh or composite cannot
be traced back to its origin video run.

## Envelope fields

| Field | Type | Example |
|---|---|---|
| source_run_id | str | exp_01M64VCHNCCB3HP8DAXC7TX2DP |
| beat_label | str | two_shot |
| frame_index | int | 4 |
| source_timestamp_s | float | 7.5 |

None is accepted; the gap is flagged in provenance_note, not silently dropped.

## Usage

```python
from provenance_envelope import ProvenanceEnvelope, wrapped_adapter
env = ProvenanceEnvelope("exp_01M64VCHNCCB3HP8DAXC7TX2DP", "two_shot", 4, 7.5)
result = wrapped_adapter("3d_cinematic", env)  # stub used by default
# To use the real adapter: wrapped_adapter("3d_cinematic", env, adapter_fn=real_adapter)
```

## Blocking gaps inherited from artifact 936bb216

- Pixel format at Seedance output boundary (not stated)
- Model-output license for redistribution (not stated)

Open research: rqr_01M6BMWP0E4ZM2M3KKHKBBGPJG, rqr_01M6BVS0SR836JZKM0MQSY0J3H