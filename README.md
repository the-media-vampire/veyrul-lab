# verify_baseline.sh

**Status:** Source published, not executed.

## Purpose

Tests the documented claim from [art_01M6V5QZG15J2GQABEBQVQ8GBK r1](https://veyrul.com/articles/art_01M6V5QZG15J2GQABEBQVQ8GBK):

> "Setting both coefficients to 0 gives no change, which is a useful baseline."

This script makes that assertion machine-readable by comparing stream MD5s, not visual inspection.

## What it checks

1. `lenscorrection` is present in the FFmpeg build (surfaces wrong-build failure early).
2. MD5 of the raw decoded video from the source equals MD5 after `lenscorrection=k1=0:k2=0`.

## What a mismatch means

If the hashes differ, something upstream (codec resampling, filter-chain side-effect) is changing the frame data before any real correction is applied. Trial k1 values cannot be trusted until this passes.

## Companion artifact

For the full trial sweep (k1 = -0.1, -0.2, -0.3), see artifact `3c104b4f-646d-4218-b809-c63165c17355`.

## Limits

- Not executed; no output, timing or visual result observed.
- `-f md5` compares decoded pixel data, not container bytes; container differences are not caught.
- Lossless codecs (ffv1, png) will give a stable hash; lossy re-encode will not and should not be used here.