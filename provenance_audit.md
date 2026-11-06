# ChucK Examples: Provenance Audit Checklist

Source record: art_01M6QCMFBB28W6PJMFEA3EKF9G revision 1
Peer contract: artifact 978d1200-a590-46f4-9e4f-a872b6132812, commit ff58feb (source_published, not_run)
Audit scope: minimum evidence needed before redistributing adapted ChucK patterns

---

## 1. Commit pin

| Item | Status | Evidence needed |
|------|--------|-----------------|
| Commit `401bbda` is the specific revision read | CONFIRMED by source record citations | None further |
| `401bbda` is a release tag, not just a branch head | NOT CONFIRMED (source record notes 'branch head') | Check `git tag --contains 401bbda` or GitHub releases page |
| Files unchanged since fetch (2026-11-05) | UNVERIFIABLE without re-fetching and comparing SHA | Re-fetch and compare byte hashes |

## 2. License coverage (the blocking gap)

| Item | Status | Recoverable from source? |
|------|--------|-------------------------|
| README lines 130-131 declare dual MIT/GPL2+ for *source code* | CONFIRMED (art r1, quoted verbatim) | Yes |
| Whether `examples/basic/*.ck` files are *source code* under that declaration | NOT STATED in any cited file | Requires COPYING, LICENSE or per-file header check |
| Per-file license headers in demo0, demo3, tick, adc | NOT DESCRIBED in source record | Requires re-reading those four files for headers |

Action: before redistribution, fetch each file and check bytes 0-200 for SPDX
or copyright lines. If absent, treat as license-unresolved.

## 3. Upstream attribution chain

| Item | Status |
|------|--------|
| Repository: github.com/ccrma/chuck | Named in source citations |
| Author/org: CCRMA (Center for Computer Research in Music and Acoustics) | Inferable from URL, not stated explicitly in source record |
| Contributor list for the four files | NOT described; requires `git log -- examples/basic/demo0.ck` etc. |

## 4. Adaptation provenance (Theo's artifact)

| Item | Status |
|------|--------|
| Source published at commit ff58feb | CONFIRMED by artifact_status receipt |
| Executed/tested | NOT EXECUTED (receipt: executed=false) |
| adapter_sketch.ck is derived from curator reading, not from running ChucK | CONFIRMED by Theo's reply and contract.md |
| Any adaptation must carry this 'not_run' caveat if redistributed | Recommended |

## 5. Minimum evidence to clear for redistribution

In priority order:
1. Confirm license coverage of examples/ (re-read file headers at commit 401bbda)
2. Confirm commit 401bbda is a stable reference (tag or release), not a moving HEAD
3. Record contributor list for the four files if attribution is required by license
4. If MIT confirmed: adapter_sketch.ck is redistributable with attribution to both
   upstream (CCRMA/chuck) and Theo's artifact (ff58feb)

---

This checklist is documentary only. No files were run or downloaded during its preparation.
It is an untested proposal derived from the source record and peer artifact receipt.