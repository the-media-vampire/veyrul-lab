# Integration contract: vaguedenoiser vs hqdn3d

## Sources
- `art_01M6VYVD4GZ3456R6E6S083BCM` r1 — vaguedenoiser, documented options
- FFmpeg filters documentation (hqdn3d section, same manual)

## Mechanism comparison

| Property | vaguedenoiser | hqdn3d |
|---|---|---|
| Domain | Wavelet (CDF 9/7 per frame) | Spatial + temporal blur |
| Temporal awareness | None (per-frame only) | Yes (temporal luma/chroma params) |
| Key strength param | threshold (default 2) | luma_spatial (default ~4) |
| Overfilter symptom | Waxy/plasticky (source-documented) | Blurry/motion-smeared |
| Format dependency | Accepts luma/chroma planes separately | Same |
| nsteps constraint | 1–32; resolution-limited | No equivalent |

## Shared interface (the adapter)
- Both take: input file, output file, strength tier.
- Both output: a filtered video file.
- Strength tiers map to documented parameter ranges, not empirically tuned values.

## Combination: sequential chain
If you chain them (`vaguedenoiser` then `hqdn3d`), the second filter
operates on already-denoised coefficients. Expected result: more
aggressive smoothing, higher risk of detail loss. Recommended only at
low strength on both. The chain is: `-vf vaguedenoiser=threshold=1,hqdn3d=2:1`.
This is assembled; not run.

## Evidence gaps (queued for research)
1. Does vaguedenoiser accept a YUV420P stream from hqdn3d without an
   explicit `format=` node, or does it error?
2. At what threshold does vaguedenoiser match hqdn3d mid-strength
   perceptually? No empirical data exists.
3. Does the wavelet-then-temporal chain introduce visible ringing on
   edges that neither filter alone produces?

## Provenance and license
- vaguedenoiser: FFmpeg project, LGPL 2.1+. Options: original synthesis,
  redistribution and modification permitted (art_01M6VYVD4GZ3456R6E6S083BCM r1).
- hqdn3d: FFmpeg project, LGPL 2.1+. Options assembled from same manual.
- This adapter: MIT. Reuse with attribution.

## What is NOT established
- Which filter is better for a given noise type.
- Real timing, PSNR or SSIM values.
- Correct strength equivalences across the two filters.