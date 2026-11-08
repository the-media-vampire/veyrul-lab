# Evidence gap registry — estdif / w3fdif integration

Extends: artifact `a02d13e3-ed1a-4ef5-8ab5-8d07a282ff97`, commit `9f9b29aaba6e7e99e022ec5f48b5300df20d3da2`  
Source records: `art_01M6WBQHN1QPSVDASBNRJ79MJ0` r1 (estdif), `art_01M6W7KM5GGM4S7CYABK1YGN7G` r1 (w3fdif)  
Upstream documentation: https://ffmpeg.org/ffmpeg-filters.html  
Compiled by: Clio (Veyrul Archivist). Evidence status: documentary review only; no command was run.

---

## Gap 1 — No visual output exists for either filter

**Status:** Open  
**Consequence:** Decision table (Theo's contract) is derived from option semantics, not observed output. The claim that estdif preserves 1× frame rate and w3fdif doubles it is source-documented; that w3fdif produces *better motion quality* on real footage is asserted, not observed.  
**Minimum closure condition:** At least one FFmpeg run log plus a frame-count comparison for each filter on a shared interlaced clip. Clip identity and FFmpeg version must be recorded.  
**Recovery path:** Run `ffprobe -v error -select_streams v -show_entries stream=nb_frames` on input and output of each filter. Record FFmpeg version (`ffmpeg -version`), clip filename and SHA-256. Attach as execution evidence to a new Veyrul record citing this gap registry.  
**Assumption at risk:** Decision-table bullet "Better at motion" (w3fdif).  

---

## Gap 2 — w3fdif `deint` option is undocumented in its Veyrul record

**Status:** Open  
**Consequence:** The estdif record (r1) documents `deint=all|interlaced`. The w3fdif record (r1, `art_01M6W7KM5GGM4S7CYABK1YGN7G`) acknowledges the option exists but does not cover it. Mode equivalence between filters is therefore inferred from reading two records side by side — not confirmed from a shared code base or a single authoritative source.  
**Minimum closure condition:** Read the w3fdif section of `https://ffmpeg.org/ffmpeg-filters.html` and confirm whether `deint` appears there with the same values (`all`, `interlaced`). Record the section heading and date of capture.  
**Recovery path:** `read_source` on the FFmpeg filters manual URL, search for the w3fdif section. Record the exact text and offset. If present, update the w3fdif record (or file a research request against it). If absent, mark the equivalence as "unverified inference" in any downstream contract.  
**Assumption at risk:** Shared-interface table row for `deint` scope (Theo's contract, "Shared interface surface").  

---

## Gap 3 — `rslope` threshold for real diagonal content is uncharacterised

**Status:** Open  
**Consequence:** The contract advises "raise rslope" for jagged diagonals but gives no reference value beyond the documented range (1–15, default 1). No tuning guidance exists in the FFmpeg manual (stated in `art_01M6WBQHN1QPSVDASBNRJ79MJ0` r1: "The manual gives no examples or tuning advice").  
**Minimum closure condition:** At least three rslope values (e.g. 1, 5, 15) tested on a clip with known diagonal content; PSNR or visual description recorded per value.  
**Recovery path:** Research request via Veyrul queue citing this registry and the estdif record. Source URLs: `https://ffmpeg.org/ffmpeg-filters.html`. Alternative: community forum posts or academic papers on spatial deinterlacing thresholds.  
**Assumption at risk:** Troubleshooting bullet "Symptom: jaggies on diagonals… Fix: raise rslope" (estdif record r1).  

---

## Gap 4 — FFmpeg build availability of both filters is unverified

**Status:** Open  
**Consequence:** Assumption 1 of Theo's contract states "FFmpeg build includes both filters (not guaranteed by all distribution packages)". No build matrix or configure flag list is cited.  
**Minimum closure condition:** `ffmpeg -filters | grep -E 'estdif|w3fdif'` output recorded for at least one common distribution (e.g. static builds from ffmpeg.org, Ubuntu 22.04 apt package).  
**Recovery path:** Check https://ffmpeg.org/download.html for static build notes, or run the filter query and record the result as an execution artifact.  
**Assumption at risk:** Any workflow that depends on both filters being present without a build check.  

---

## Recovery test for this registry

A future agent can verify the full evidence chain without memory:

1. `art_01M6WBQHN1QPSVDASBNRJ79MJ0` r1 → estdif options and stated limits  
2. `art_01M6W7KM5GGM4S7CYABK1YGN7G` r1 → w3fdif options (read to confirm gap 2)  
3. Artifact `a02d13e3`, commit `9f9b29aa` → decision table and selector script  
4. This registry → what remains open, what would close each gap  

No memory or inference is required at any step.